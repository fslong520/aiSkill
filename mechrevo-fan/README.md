# mechrevo_fan — WOOKING X15 WMI 风扇/温度驱动

## 文件清单

```
mechrevo_fan.c      # 内核模块源码
mechrevo_fan.ko     # 已编译模块（kernel 7.1.3-1-MANJARO）
Makefile             # 编译
dkms.conf            # DKMS
install.sh           # 安装脚本（需 root）
verify.sh            # 校验脚本（加载后运行）
```

## 安装

```bash
sudo ./install.sh
```

或手动：

```bash
# 复制
sudo mkdir -p /usr/src/mechrevo-fan
sudo cp *.c Makefile dkms.conf /usr/src/mechrevo-fan/

# DKMS 编译安装
sudo dkms add mechrevo-fan/1.0.0
sudo dkms build mechrevo-fan/1.0.0
sudo dkms install mechrevo-fan/1.0.0

# 加载
sudo modprobe mechrevo_fan
```

或直接跳 DKMS（快速测试）：

```bash
sudo insmod mechrevo_fan.ko
```

## 加载校验

```bash
# 1. 确认模块已加载
lsmod | grep mechrevo_fan

# 2. 查看新 hwmon 设备
# 模块会添加 1 个新 hwmon，名为 mechrevo_fan
cat /sys/class/hwmon/*/name | grep mechrevo_fan

# 3. 查看传感器
sensors

# 4. 查看 sysfs 风扇控制
ls /sys/devices/platform/mechrevo_fan.*/
cat /sys/devices/platform/mechrevo_fan.*/fan_boost

# 5. 查看日志
dmesg | grep mechrevo_fan

# 6. 验证 platform_profile
cat /sys/firmware/acpi/platform_profile_choices
cat /sys/firmware/acpi/platform_profile
echo "quiet" | sudo tee /sys/firmware/acpi/platform_profile
cat /sys/firmware/acpi/platform_profile
```

## 预期输出

```
$ sensors

mechrevo_fan-* adapter: WMI
temp1:        +45.0°C  (CPU)
fan1:         2400 RPM  (CPU 风扇)
fan2:         1800 RPM  (GPU 风扇)
```

## 方法 ID 调优

若读数异常（温度=0、风扇=0、profile 无反应），需改 `mechrevo_fan.c` 中 method ID 定义：

| 定义 | 默认 | 含义 |
|---|---|---|
| `WMI_METHOD_CPU_TEMP` | 0x04 | CPU 温度 |
| `WMI_METHOD_FAN_SPEED` | 0x02 | 风扇转速 |
| `WMI_METHOD_PROFILE` | 0x03 | 性能模式 |
| `WMI_METHOD_FAN_BOOST` | 0x14 | 风扇强冷 |

常见的替换值：0x05, 0x06（GPU 温度）、0x07（profile）、0x15（fan boost）。

改 `#define` 后 `make` 重新编译即可测试，无需 DKMS 全重装。

## 已绑定的 WMI GUID

| GUID | 对象 | 用途 | 驱动 |
|---|---|---|---|
| ABBC0F6A-8EA1-11D1-00A0-C90629100000 | AA | 本模块目标 | 待绑定 |
| 05901221-D566-11D1-B2F0-00A0C9062910-1 | AB | AB 块 | wmi-bmof |
| 05901221-D566-11D1-B2F0-00A0C9062910-3 | BA | BA 块 | wmi-bmof |
| D94E769B-9063-1101-726F-AEAC813B597F | - | 事件 GUID | 未绑定 |
