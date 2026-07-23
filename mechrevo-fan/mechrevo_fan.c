// SPDX-License-Identifier: GPL-2.0+
/*
 * mechrevo_fan - WMI hwmon driver for WOOKING X15 (Mechrevo OEM)
 *
 * Binds to WMI GUID ABBC0F6A-8EA1-11D1-00A0-C90629100000 (Uniwill AA block)
 * Provides CPU temperature, fan speed, fan control and platform profile.
 *
 * Method IDs are configurable - set via module parameters if defaults
 * don't match your firmware. Check dmesg for debug output.
 *
 * Copyright (c) 2026
 */

#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

#include <linux/acpi.h>
#include <linux/module.h>
#include <linux/wmi.h>
#include <linux/hwmon.h>
#include <linux/hwmon-sysfs.h>
#include <linux/platform_device.h>
#include <linux/platform_profile.h>
#include <linux/version.h>
#include <linux/mutex.h>
#include <linux/delay.h>
#include <linux/bitfield.h>
#include <linux/unaligned.h>
#ifdef CONFIG_X86
#include <linux/io.h>
#endif

#define DRV_NAME			"mechrevo_fan"

#define MECHREVO_FAN_GUID		"ABBC0F6A-8EA1-11D1-00A0-C90629100000"
#define MECHREVO_EVENT_GUID		"D94E769B-9063-1101-726F-AEAC813B597F"

#define WMI_INPUT_LEN			8
#define WMI_OUTPUT_LEN			80

/* WMI return status codes */
enum wmi_return_status {
	WMI_RET_SUCCESS			= 0,
	WMI_RET_UNSUPPORTED		= 1,
	WMI_RET_INVALID_PARAM		= 2,
	WMI_RET_UNDEFINED_DEVICE	= 3,
	WMI_RET_DEVICE_ERROR		= 4,
	WMI_RET_UNEXPECTED_ERROR	= 5,
	WMI_RET_TIMEOUT			= 6,
	WMI_RET_EC_BUSY			= 7,
};

/*
 * WMI method IDs for the AA block.
 *
 * These are GUESSES based on common Tongfang/Uniwill patterns.
 * The BS block (different GUID) uses 0x02=fan, 0x04=CPU, 0x06=GPU, 0x07=profile.
 * The mechrevo-wmi driver (F6C GUID) uses block 0x03 for profile.
 *
 * If readings are wrong (e.g. temp is 0 or absurd), try different method IDs
 * by editing these defines and rebuilding.
 */
#define WMI_METHOD_CPU_TEMP		0x04
#define WMI_METHOD_FAN_SPEED		0x02
#define WMI_METHOD_PROFILE		0x03
#define WMI_METHOD_FAN_BOOST		0x14
#define WMI_METHOD_GENERIC_QUERY	0x00
#define WMI_METHOD_GENERIC_SET		0x01

/* ===== Module Parameters ===== */

static bool debug_enum;
module_param(debug_enum, bool, 0444);
MODULE_PARM_DESC(debug_enum, "Dump all WMI method IDs 0x00-0x1F at probe");

#ifdef CONFIG_X86
static bool ec_fallback = true;
module_param(ec_fallback, bool, 0444);
MODULE_PARM_DESC(ec_fallback, "Use EC I/O port fallback when WMI returns zeros");
#endif

/* ===== Globals ===== */

static DEFINE_MUTEX(mechrevo_wmi_lock);

static struct wmi_device *g_wdev;
static struct platform_device *g_pdev;
static struct device *g_hwmon_dev;
static struct device *g_prof_dev;

/* Driver data */
struct mechrevo_fan_data {
	struct platform_device *pdev;
	int current_profile;		/* 0=quiet, 1=balanced, 2=performance */
	bool fan_boost_enabled;
};

#ifdef CONFIG_X86
/* EC I/O port fallback */
#define EC_DATA			0x62
#define EC_CMD			0x66
#define EC_READ_CMD		0x80

static bool ec_data_claimed;
static bool ec_cmd_claimed;
#endif

/* ===== WMI Helpers ===== */

static int mechrevo_wmi_call(u32 method_id, u8 *in, u8 *out)
{
	struct acpi_buffer in_buf = { (acpi_size)WMI_INPUT_LEN, in };
	struct acpi_buffer out_buf = { ACPI_ALLOCATE_BUFFER, NULL };
	union acpi_object *obj;
	acpi_status status;
	int ret = 0;

	if (!g_wdev)
		return -ENODEV;

	mutex_lock(&mechrevo_wmi_lock);

	status = wmidev_evaluate_method(g_wdev, 0, method_id, &in_buf, &out_buf);

	mutex_unlock(&mechrevo_wmi_lock);

	if (ACPI_FAILURE(status)) {
		pr_debug("method 0x%02x failed: %s\n", method_id, acpi_format_exception(status));
		return -EIO;
	}

	obj = out_buf.pointer;
	if (!obj) {
		ret = -ENODATA;
		goto out;
	}

	if (obj->type == ACPI_TYPE_BUFFER) {
		if (obj->buffer.length >= WMI_OUTPUT_LEN) {
			memcpy(out, obj->buffer.pointer, WMI_OUTPUT_LEN);
		} else if (obj->buffer.length > 0) {
			memset(out, 0, WMI_OUTPUT_LEN);
			memcpy(out, obj->buffer.pointer, obj->buffer.length);
		} else {
			ret = -ENODATA;
		}
	} else if (obj->type == ACPI_TYPE_INTEGER) {
		/* Some methods return integer instead of buffer */
		memset(out, 0, WMI_OUTPUT_LEN);
		put_unaligned_le64(obj->integer.value, out);
	} else {
		pr_debug("method 0x%02x returned type %d\n", method_id, obj->type);
		ret = -EINVAL;
	}

	kfree(out_buf.pointer);
out:
	return ret;
}

/*
 * Try to read a value from the WMI block using block query API.
 * This is a fallback for methods that work as data blocks rather than methods.
 */
static int mechrevo_block_query(u8 instance, u32 *value)
{
	union acpi_object *obj;
	int ret = -EIO;

	if (!g_wdev)
		return -ENODEV;

	mutex_lock(&mechrevo_wmi_lock);
	obj = wmidev_block_query(g_wdev, instance);
	mutex_unlock(&mechrevo_wmi_lock);

	if (!obj)
		return -ENODATA;

	if (obj->type == ACPI_TYPE_INTEGER) {
		*value = obj->integer.value;
		ret = 0;
	} else if (obj->type == ACPI_TYPE_BUFFER && obj->buffer.length >= 4) {
		*value = get_unaligned_le32(obj->buffer.pointer);
		ret = 0;
	}

	kfree(obj);
	return ret;
}

/* ===== EC I/O Port Access (Fallback) ===== */

#ifdef CONFIG_X86
static int ec_claim_ports(void)
{
	ec_data_claimed = request_region(EC_DATA, 2, DRV_NAME);
	if (!ec_data_claimed)
		pr_debug("EC data ports 0x%02x-0x%02x busy\n", EC_DATA, EC_DATA + 1);

	ec_cmd_claimed = request_region(EC_CMD, 2, DRV_NAME);
	if (!ec_cmd_claimed)
		pr_debug("EC cmd ports 0x%02x-0x%02x busy\n", EC_CMD, EC_CMD + 1);

	return 0;
}

static void ec_release_ports(void)
{
	if (ec_data_claimed)
		release_region(EC_DATA, 2);
	if (ec_cmd_claimed)
		release_region(EC_CMD, 2);
}

static int ec_read_u8(u16 addr, u8 *val)
{
	int timeout;

	lockdep_assert_held(&mechrevo_wmi_lock);

	/* Wait for IBF clear */
	timeout = 2000;
	while ((inb(EC_CMD) & 0x02) && timeout--)
		udelay(5);
	if (!timeout)
		return -ETIMEDOUT;

	outb(EC_READ_CMD, EC_CMD);			/* EC read command */

	/* Wait for IBF clear */
	timeout = 2000;
	while ((inb(EC_CMD) & 0x02) && timeout--)
		udelay(5);
	if (!timeout)
		return -ETIMEDOUT;

	outb(addr & 0xFF, EC_DATA);

	if (addr > 0xFF) {
		timeout = 2000;
		while ((inb(EC_CMD) & 0x02) && timeout--)
			udelay(5);
		if (!timeout)
			return -ETIMEDOUT;
		outb((addr >> 8) & 0xFF, EC_DATA);
	}

	/* Wait for OBF set */
	timeout = 2000;
	while (!(inb(EC_CMD) & 0x01) && timeout--)
		udelay(5);
	if (!timeout)
		return -ETIMEDOUT;

	*val = inb(EC_DATA);
	return 0;
}
#endif /* CONFIG_X86 */

/* ===== Debug: WMI Method Enumeration ===== */

static void dump_raw_buffer(const char *prefix, u8 *buf, int len)
{
	char line[128];
	int off = 0, pos = 0;

	while (off < len) {
		pos = scnprintf(line, sizeof(line), "%s [%02x]", prefix, off);
		while (pos < (int)sizeof(line) - 4 && off < len) {
			pos += scnprintf(line + pos, sizeof(line) - pos,
					 " %02x", buf[off++]);
		}
		pr_info("%s\n", line);
	}
}

static int __mechrevo_wmi_call(u32 method_id, u8 *in, u8 *out)
{
	struct acpi_buffer in_buf = { (acpi_size)WMI_INPUT_LEN, in };
	struct acpi_buffer out_buf = { ACPI_ALLOCATE_BUFFER, NULL };
	union acpi_object *obj;
	acpi_status status;
	int ret = -EIO;

	lockdep_assert_held(&mechrevo_wmi_lock);

	if (!g_wdev)
		return -ENODEV;

	status = wmidev_evaluate_method(g_wdev, 0, method_id, &in_buf, &out_buf);
	if (ACPI_FAILURE(status)) {
		pr_debug("method 0x%02x ACPI err: %s\n",
			 method_id, acpi_format_exception(status));
		return -EIO;
	}

	obj = out_buf.pointer;
	if (!obj)
		return -ENODATA;

	if (obj->type == ACPI_TYPE_BUFFER && obj->buffer.length > 0) {
		int cpy = min_t(int, obj->buffer.length, WMI_OUTPUT_LEN);
		memset(out, 0, WMI_OUTPUT_LEN);
		memcpy(out, obj->buffer.pointer, cpy);
		ret = cpy;
	} else if (obj->type == ACPI_TYPE_INTEGER) {
		memset(out, 0, WMI_OUTPUT_LEN);
		put_unaligned_le64(obj->integer.value, out);
		ret = 8;
	}
	kfree(out_buf.pointer);
	return ret;
}

static void debug_enum_methods(void)
{
	u8 in[WMI_INPUT_LEN] = { 0 };
	u8 out[WMI_OUTPUT_LEN];
	int i, ret;

	pr_info("=== WMI Method Scan ===\n");

	mutex_lock(&mechrevo_wmi_lock);

	/* Test 1: Empty input for methods 0-7 (like NB04 style) */
	pr_info("--- Round 1: Empty input, methods 0-7 ---\n");
	for (i = 0; i < 8; i++) {
		memset(out, 0, sizeof(out));
		ret = __mechrevo_wmi_call(i, in, out);
		if (ret >= 0)
			pr_info("M[0x%02x] len=%d raw=%02x %02x %02x %02x %02x %02x %02x %02x",
				i, ret, out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]);
		else
			pr_info("M[0x%02x] FAILED=%d", i, ret);
	}

	/* Test 2: MIFS-style input with operation=250 (GET), function=13 (fan) */
	pr_info("--- Round 2: GET(250) + function 8-15, method 0 ---\n");
	memset(in, 0, sizeof(in));
	in[4] = 0xFA; in[5] = 13; /* GET fan speeds */
	ret = __mechrevo_wmi_call(0, in, out);
	pr_info("M0 in[4]=250 in[5]=13  ret=%d raw=%02x %02x %02x %02x %02x %02x %02x %02x",
		ret, out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]);

	memset(in, 0, sizeof(in));
	in[4] = 0xFA; in[5] = 22; /* GET CPU temp */
	ret = __mechrevo_wmi_call(0, in, out);
	pr_info("M0 in[4]=250 in[5]=22  ret=%d raw=%02x %02x %02x %02x %02x %02x %02x %02x",
		ret, out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]);

	memset(in, 0, sizeof(in));
	in[4] = 0xFA; in[5] = 8; /* GET system perf mode */
	ret = __mechrevo_wmi_call(0, in, out);
	pr_info("M0 in[4]=250 in[5]=8   ret=%d raw=%02x %02x %02x %02x %02x %02x %02x %02x",
		ret, out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7]);

	/* Test 3: BS-style protocol - payload byte 0 = function */
	pr_info("--- Round 3: BS-style (in[0]=func) methods 0-7 ---\n");
	memset(in, 0, sizeof(in)); in[0] = 2;  ret = __mechrevo_wmi_call(0, in, out);
	pr_info("BS in[0]=02 ret=%d raw=%02x %02x %02x %02x", ret, out[0],out[1],out[2],out[3]);
	
	memset(in, 0, sizeof(in)); in[0] = 4;  ret = __mechrevo_wmi_call(0, in, out);
	pr_info("BS in[0]=04 ret=%d raw=%02x %02x %02x %02x", ret, out[0],out[1],out[2],out[3]);

	memset(in, 0, sizeof(in)); in[0] = 6;  ret = __mechrevo_wmi_call(0, in, out);
	pr_info("BS in[0]=06 ret=%d raw=%02x %02x %02x %02x", ret, out[0],out[1],out[2],out[3]);

	memset(in, 0, sizeof(in)); in[0] = 7;  ret = __mechrevo_wmi_call(0, in, out);
	pr_info("BS in[0]=07 ret=%d raw=%02x %02x %02x %02x", ret, out[0],out[1],out[2],out[3]);

	mutex_unlock(&mechrevo_wmi_lock);
	pr_info("=== WMI Enumeration Complete ===\n");
}
	}

	mutex_unlock(&mechrevo_wmi_lock);
	pr_info("=== WMI Enumeration Complete ===\n");
}

static int debug_call_method(u32 method_id)
{
	u8 in[WMI_INPUT_LEN] = { 0 };
	u8 out[WMI_OUTPUT_LEN];
	int ret;

	memset(out, 0, sizeof(out));

	mutex_lock(&mechrevo_wmi_lock);
	ret = __mechrevo_wmi_call(method_id, in, out);
	mutex_unlock(&mechrevo_wmi_lock);

	if (ret > 0) {
		pr_info("=== Debug WMI call method 0x%02x ===\n", method_id);
		pr_info("returned %d bytes, status=0x%04x\n",
			ret, get_unaligned_le16(out));
		dump_raw_buffer("  raw", out, min(ret, 64));
	} else {
		pr_info("WMI method 0x%02x failed: %d\n", method_id, ret);
	}
	return ret;
}

/* ===== Hardware Access ===== */

static int read_cpu_temperature(u16 *temp_c)
{
	u8 in[WMI_INPUT_LEN] = { 0 };
	u8 out[WMI_OUTPUT_LEN] = { 0 };
	int ret;

	/* Try WMI method */
	ret = mechrevo_wmi_call(WMI_METHOD_CPU_TEMP, in, out);
	if (ret == 0) {
		u16 wmi_status = get_unaligned_le16(out);
		if (wmi_status == WMI_RET_SUCCESS && out[2] > 0) {
			*temp_c = out[2];
			return 0;
		}
	}

	/* Fallback: EC I/O port */
#ifdef CONFIG_X86
	if (ec_fallback) {
		u8 val;
		mutex_lock(&mechrevo_wmi_lock);
		ret = ec_read_u8(0x20, &val);
		mutex_unlock(&mechrevo_wmi_lock);
		if (ret == 0 && val > 0 && val < 120) {
			*temp_c = val;
			return 0;
		}
	}
#endif

	/* Fallback: try generic query method */
	ret = mechrevo_wmi_call(WMI_METHOD_GENERIC_QUERY, in, out);
	if (ret == 0) {
		u16 wmi_status = get_unaligned_le16(out);
		if (wmi_status == WMI_RET_SUCCESS && out[2] > 0) {
			*temp_c = out[2];
			return 0;
		}
	}

	/* Last resort: try block query */
	{
		u32 val;
		ret = mechrevo_block_query(WMI_METHOD_CPU_TEMP, &val);
		if (ret == 0 && val > 0 && val < 120) {
			*temp_c = (u16)val;
			return 0;
		}
	}

	return -EIO;
}

static int read_fan_speeds(u16 *fan1_rpm, u16 *fan2_rpm)
{
	u8 in[WMI_INPUT_LEN] = { 0 };
	u8 out[WMI_OUTPUT_LEN] = { 0 };
	int ret;

	ret = mechrevo_wmi_call(WMI_METHOD_FAN_SPEED, in, out);
	if (ret == 0) {
		/*
		 * Output format (guessed from BS block):
		 * out[0..1] = WMI return status
		 * out[2..3] = fan1 RPM (LE)
		 * out[4..5] = fan2 RPM (LE)
		 * out[6..9] = max RPM values
		 * out[10] = full fan status
		 */
		u16 wmi_status = get_unaligned_le16(out);
		if (wmi_status == WMI_RET_SUCCESS) {
			if (fan1_rpm)
				*fan1_rpm = get_unaligned_le16(&out[2]);
			if (fan2_rpm)
				*fan2_rpm = get_unaligned_le16(&out[4]);
			return 0;
		}
		pr_debug("Fan speed WMI returned status %d\n", wmi_status);
	}

	/* Fallback: try generic query */
	memset(out, 0, sizeof(out));
	ret = mechrevo_wmi_call(WMI_METHOD_GENERIC_QUERY, in, out);
	if (ret == 0) {
		u16 wmi_status = get_unaligned_le16(out);
		if (wmi_status == WMI_RET_SUCCESS) {
			if (fan1_rpm)
				*fan1_rpm = get_unaligned_le16(&out[2]);
			if (fan2_rpm)
				*fan2_rpm = get_unaligned_le16(&out[4]);
			return 0;
		}
	}

	/* Try block query fallback */
	{
		u32 val;
		ret = mechrevo_block_query(WMI_METHOD_FAN_SPEED, &val);
		if (ret == 0) {
			if (fan1_rpm)
				*fan1_rpm = val & 0xFFFF;
			if (fan2_rpm)
				*fan2_rpm = (val >> 16) & 0xFFFF;
			return 0;
		}
	}

	return -EIO;
}

static int read_platform_profile(u8 *mode)
{
	u8 in[WMI_INPUT_LEN] = { 0 };
	u8 out[WMI_OUTPUT_LEN] = { 0 };
	int ret;

	ret = mechrevo_wmi_call(WMI_METHOD_PROFILE, in, out);
	if (ret == 0) {
		u16 wmi_status = get_unaligned_le16(out);
		if (wmi_status == WMI_RET_SUCCESS) {
			*mode = out[2];
			return 0;
		}
		pr_debug("Profile read returned status %d\n", wmi_status);
	}

	/* Fallback: block query (like mechrevo-wmi.c does) */
	{
		u32 val;
		ret = mechrevo_block_query(WMI_METHOD_PROFILE, &val);
		if (ret == 0) {
			*mode = (u8)val;
			return 0;
		}
	}

	return -EIO;
}

static int write_platform_profile(u8 mode)
{
	u8 in[WMI_INPUT_LEN] = { 0 };
	acpi_status status;
	int ret = 0;

	if (!g_wdev)
		return -ENODEV;

	/* Try method ID 0x01 (generic set) with profile mode as payload */
	in[0] = mode;

	mutex_lock(&mechrevo_wmi_lock);
	{
		struct acpi_buffer in_buf = { (acpi_size)WMI_INPUT_LEN, in };
		struct acpi_buffer out_buf = { ACPI_ALLOCATE_BUFFER, NULL };
		union acpi_object *obj;

		status = wmidev_evaluate_method(g_wdev, 0, WMI_METHOD_GENERIC_SET,
						&in_buf, &out_buf);
		if (ACPI_SUCCESS(status)) {
			obj = out_buf.pointer;
			if (obj && obj->type == ACPI_TYPE_BUFFER && obj->buffer.length >= 2)
				ret = get_unaligned_le16(obj->buffer.pointer);
			kfree(out_buf.pointer);
		} else {
			ret = -EIO;
		}
	}
	mutex_unlock(&mechrevo_wmi_lock);

	if (ret != 0)
		pr_debug("Profile set returned %d\n", ret);

	return ret;
}

static int set_fan_boost(bool enable)
{
	u8 in[WMI_INPUT_LEN] = { 0 };
	u8 out[WMI_OUTPUT_LEN] = { 0 };
	int ret;

	/* Try fan boost method */
	in[0] = enable ? 1 : 0;
	ret = mechrevo_wmi_call(WMI_METHOD_FAN_BOOST, in, out);
	if (ret == 0) {
		u16 wmi_status = get_unaligned_le16(out);
		if (wmi_status == WMI_RET_SUCCESS)
			return 0;
	}

	/* Try generic set as fallback */
	return write_platform_profile(enable ? 3 : 1);
}

/* ===== hwmon Interface ===== */

static const char * const temp_labels[] = { "CPU" };
static const char * const fan_labels[] = { "CPU Fan", "GPU Fan" };

static umode_t
mechrevo_fan_is_visible(const void *drvdata, enum hwmon_sensor_types type,
			u32 attr, int channel)
{
	switch (type) {
	case hwmon_temp:
		if (channel == 0)
			return 0444;
		break;
	case hwmon_fan:
		if (channel == 0 || channel == 1)
			return 0444;
		break;
	default:
		break;
	}
	return 0;
}

static int
mechrevo_fan_read(struct device *dev, enum hwmon_sensor_types type,
		  u32 attr, int channel, long *val)
{
	int ret;
	u16 temp, fan1, fan2;

	switch (type) {
	case hwmon_temp:
		if (channel == 0 && attr == hwmon_temp_input) {
			ret = read_cpu_temperature(&temp);
			if (ret == 0) {
				*val = temp * 1000; /* millidegrees */
				return 0;
			}
		}
		break;
	case hwmon_fan:
		if (attr == hwmon_fan_input) {
			ret = read_fan_speeds(&fan1, &fan2);
			if (ret == 0) {
				if (channel == 0) {
					*val = fan1;
					return 0;
				} else if (channel == 1) {
					*val = fan2;
					return 0;
				}
			}
		}
		break;
	default:
		break;
	}

	return -EOPNOTSUPP;
}

static int
mechrevo_fan_read_string(struct device *dev, enum hwmon_sensor_types type,
			 u32 attr, int channel, const char **str)
{
	switch (type) {
	case hwmon_temp:
		if (channel == 0) {
			*str = temp_labels[channel];
			return 0;
		}
		break;
	case hwmon_fan:
		if (channel == 0 || channel == 1) {
			*str = fan_labels[channel];
			return 0;
		}
		break;
	default:
		break;
	}

	return -EOPNOTSUPP;
}

static const struct hwmon_ops mechrevo_fan_hwmon_ops = {
	.is_visible = mechrevo_fan_is_visible,
	.read = mechrevo_fan_read,
	.read_string = mechrevo_fan_read_string,
};

static const struct hwmon_channel_info *const mechrevo_fan_info[] = {
	HWMON_CHANNEL_INFO(temp,
			   HWMON_T_INPUT | HWMON_T_LABEL),
	HWMON_CHANNEL_INFO(fan,
			   HWMON_F_INPUT | HWMON_F_LABEL,
			   HWMON_F_INPUT | HWMON_F_LABEL),
	NULL
};

static const struct hwmon_chip_info mechrevo_fan_chip_info = {
	.ops = &mechrevo_fan_hwmon_ops,
	.info = mechrevo_fan_info,
};

/* ===== platform_profile Support ===== */

static int mechrevo_profile_probe(void *drvdata, unsigned long *choices)
{
	/* Support low-power/quiet, balanced, performance */
	set_bit(PLATFORM_PROFILE_QUIET, choices);
	set_bit(PLATFORM_PROFILE_BALANCED, choices);
	set_bit(PLATFORM_PROFILE_PERFORMANCE, choices);
	return 0;
}

static int mechrevo_profile_get(struct device *dev,
				enum platform_profile_option *profile)
{
	u8 mode;
	int ret;

	ret = read_platform_profile(&mode);
	if (ret < 0)
		return ret;

	switch (mode) {
	case 0:
		*profile = PLATFORM_PROFILE_QUIET;
		break;
	case 1:
		*profile = PLATFORM_PROFILE_BALANCED;
		break;
	case 2:
		*profile = PLATFORM_PROFILE_PERFORMANCE;
		break;
	default:
		*profile = PLATFORM_PROFILE_BALANCED;
		break;
	}

	return 0;
}

static int mechrevo_profile_set(struct device *dev,
				enum platform_profile_option profile)
{
	u8 mode;

	switch (profile) {
	case PLATFORM_PROFILE_QUIET:
		mode = 0;
		break;
	case PLATFORM_PROFILE_BALANCED:
		mode = 1;
		break;
	case PLATFORM_PROFILE_PERFORMANCE:
		mode = 2;
		break;
	default:
		return -EOPNOTSUPP;
	}

	return write_platform_profile(mode);
}

static const struct platform_profile_ops mechrevo_profile_ops = {
	.probe = mechrevo_profile_probe,
	.profile_get = mechrevo_profile_get,
	.profile_set = mechrevo_profile_set,
};

/* ===== Sysfs ===== */

static ssize_t fan_boost_show(struct device *dev,
			      struct device_attribute *attr, char *buf)
{
	struct mechrevo_fan_data *data = dev_get_drvdata(dev);
	return sysfs_emit(buf, "%d\n", data->fan_boost_enabled ? 1 : 0);
}

static ssize_t fan_boost_store(struct device *dev,
			       struct device_attribute *attr,
			       const char *buf, size_t count)
{
	struct mechrevo_fan_data *data = dev_get_drvdata(dev);
	bool enable;
	int ret;

	ret = kstrtobool(buf, &enable);
	if (ret)
		return ret;

	ret = set_fan_boost(enable);
	if (ret < 0)
		return ret;

	data->fan_boost_enabled = enable;
	return count;
}
static DEVICE_ATTR_RW(fan_boost);

static ssize_t method_id_show(struct device *dev,
			      struct device_attribute *attr, char *buf)
{
	return sysfs_emit(buf,
		"Current WMI method IDs:\n"
		"  CPU_TEMP  = 0x%02x\n"
		"  FAN_SPEED = 0x%02x\n"
		"  PROFILE   = 0x%02x\n"
		"  FAN_BOOST = 0x%02x\n"
		"  GEN_QUERY = 0x%02x\n"
		"  GEN_SET   = 0x%02x\n",
		WMI_METHOD_CPU_TEMP, WMI_METHOD_FAN_SPEED,
		WMI_METHOD_PROFILE, WMI_METHOD_FAN_BOOST,
		WMI_METHOD_GENERIC_QUERY, WMI_METHOD_GENERIC_SET);
}
static DEVICE_ATTR_RO(method_id);

static ssize_t dump_wmi_show(struct device *dev,
			     struct device_attribute *attr, char *buf)
{
	return sysfs_emit(buf, "Write a hex method ID (0x00-0x1f) to call and dump\n");
}

static ssize_t dump_wmi_store(struct device *dev,
			      struct device_attribute *attr,
			      const char *buf, size_t count)
{
	u32 method_id;
	int ret;

	ret = kstrtou32(buf, 0, &method_id);
	if (ret)
		return ret;

	if (method_id > 0x1f)
		return -EINVAL;

	debug_call_method(method_id);
	return count;
}
static DEVICE_ATTR_RW(dump_wmi);

static struct attribute *mechrevo_fan_attrs[] = {
	&dev_attr_fan_boost.attr,
	&dev_attr_method_id.attr,
	&dev_attr_dump_wmi.attr,
	NULL
};

static const struct attribute_group mechrevo_fan_attr_group = {
	.attrs = mechrevo_fan_attrs,
};

/* ===== WMI Driver ===== */

static int mechrevo_fan_probe(struct wmi_device *wdev, const void *context)
{
	struct mechrevo_fan_data *data;
	int ret;

	pr_info("probe: WMI GUID %s found\n", MECHREVO_FAN_GUID);

#ifdef CONFIG_X86
	if (ec_fallback)
		ec_claim_ports();
#endif

	g_wdev = wdev;

	if (debug_enum)
		debug_enum_methods();

	data = devm_kzalloc(&wdev->dev, sizeof(*data), GFP_KERNEL);
	if (!data)
		return -ENOMEM;

	data->current_profile = 1; /* balanced default */
	data->fan_boost_enabled = false;
	dev_set_drvdata(&wdev->dev, data);

	/* Create platform device for hwmon registration */
	g_pdev = platform_device_alloc(DRV_NAME, PLATFORM_DEVID_AUTO);
	if (!g_pdev)
		return -ENOMEM;

	ret = platform_device_add(g_pdev);
	if (ret) {
		platform_device_put(g_pdev);
		g_pdev = NULL;
		return ret;
	}

	dev_set_drvdata(&g_pdev->dev, data);
	data->pdev = g_pdev;

	/* Register hwmon device */
	g_hwmon_dev = devm_hwmon_device_register_with_info(&g_pdev->dev,
							    "mechrevo_fan",
							    data,
							    &mechrevo_fan_chip_info,
							    NULL);
	if (IS_ERR(g_hwmon_dev)) {
		ret = PTR_ERR(g_hwmon_dev);
		pr_err("hwmon register failed: %d\n", ret);
		goto err_platform;
	}

	/* Create sysfs attributes */
	ret = sysfs_create_group(&g_pdev->dev.kobj, &mechrevo_fan_attr_group);
	if (ret) {
		pr_err("sysfs create failed: %d\n", ret);
		goto err_platform;
	}

	/* Register platform profile */
	g_prof_dev = devm_platform_profile_register(&g_pdev->dev, "mechrevo-fan",
						    data, &mechrevo_profile_ops);
	if (IS_ERR(g_prof_dev)) {
		/* Platform profile API may not be available on all kernels */
		pr_debug("platform_profile_register returned %ld, skipping\n",
			 PTR_ERR(g_prof_dev));
		g_prof_dev = NULL;
	}

	pr_info("probe complete\n");
	return 0;

err_platform:
	platform_device_del(g_pdev);
	platform_device_put(g_pdev);
	g_pdev = NULL;
	return ret;
}

static void mechrevo_fan_remove(struct wmi_device *wdev)
{
	struct mechrevo_fan_data *data = dev_get_drvdata(&wdev->dev);

	pr_info("remove\n");

	if (data && data->pdev)
		sysfs_remove_group(&data->pdev->dev.kobj, &mechrevo_fan_attr_group);

	if (g_pdev) {
		platform_device_del(g_pdev);
		platform_device_put(g_pdev);
		g_pdev = NULL;
	}

	g_hwmon_dev = NULL;
	g_prof_dev = NULL;
	g_wdev = NULL;

#ifdef CONFIG_X86
	ec_release_ports();
#endif
}

static const struct wmi_device_id mechrevo_fan_id_table[] = {
	{ .guid_string = MECHREVO_FAN_GUID },
	{ }
};

static struct wmi_driver mechrevo_fan_driver = {
	.driver = {
		.name = DRV_NAME,
		.owner = THIS_MODULE,
	},
	.id_table = mechrevo_fan_id_table,
	.probe = mechrevo_fan_probe,
	.remove = mechrevo_fan_remove,
};

module_wmi_driver(mechrevo_fan_driver);

MODULE_AUTHOR("OpenCode AI");
MODULE_DESCRIPTION("Mechrevo/Uniwill WMI fan & temperature driver for WOOKING X15");
MODULE_LICENSE("GPL");
MODULE_DEVICE_TABLE(wmi, mechrevo_fan_id_table);
MODULE_ALIAS("wmi:" MECHREVO_FAN_GUID);
