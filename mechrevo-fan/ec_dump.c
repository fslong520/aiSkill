/* EC register dumper - userspace I/O port access via iopl()
 * Compile: gcc -O2 -o ec_dump ec_dump.c -lioperm -lrt
 * Run: sudo ./ec_dump [start_addr] [end_addr]
 *
 * Uses the same 0x62/0x66 EC protocol as mechrevo_fan kernel module.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/io.h>

#define EC_DATA  0x62
#define EC_CMD   0x66

static int ec_wait_ibf(void)
{
	int timeout = 2000;
	while ((inb(EC_CMD) & 0x02) && timeout--)
		usleep(5);
	return timeout;
}

static int ec_wait_obf(void)
{
	int timeout = 2000;
	while (!(inb(EC_CMD) & 0x01) && timeout--)
		usleep(5);
	return timeout;
}

static int ec_read_u8(uint16_t addr, uint8_t *val)
{
	if (!ec_wait_ibf()) return -1;
	outb(0x80, EC_CMD);  /* EC read command */

	if (!ec_wait_ibf()) return -1;
	outb(addr & 0xFF, EC_DATA);

	if (addr > 0xFF) {
		if (!ec_wait_ibf()) return -1;
		outb((addr >> 8) & 0xFF, EC_DATA);
	}

	if (!ec_wait_obf()) return -1;
	*val = inb(EC_DATA);
	return 0;
}

static void dump_range(uint16_t start, uint16_t end, const char *label)
{
	int width = (end - start + 1);
	printf("\n=== %s (0x%02x-0x%02x) ===\n", label, start, end);

	/* Print header */
	printf("     ");
	for (int i = 0; i < 16 && (start + i) <= end; i++)
		printf(" %02x ", start + i);
	printf("\n");

	/* Print rows */
	for (int row = 0; row * 16 <= (end - start); row++) {
		int base = start + row * 16;
		printf("0x%02x ", base);
		for (int col = 0; col < 16; col++) {
			int addr = base + col;
			if (addr > end) break;
			uint8_t val = 0;
			if (ec_read_u8(addr, &val) == 0) {
				if (val == 0 && (addr == 0x20 || addr == 0xB2 ||
				    addr == 0xB4 || addr == 0xB5))
					printf("?? ");  /* known sensor - should be non-zero */
				else
					printf("%02x ", val);
			} else {
				printf("XX ");
			}
		}
		printf("\n");
	}
}

int main(int argc, char *argv[])
{
	uint16_t start = 0x00, end = 0xFF;

	if (argc >= 3) {
		start = strtoul(argv[1], NULL, 16);
		end   = strtoul(argv[2], NULL, 16);
	} else if (argc >= 2) {
		start = strtoul(argv[1], NULL, 16);
		end   = start + 0x20;
	}

	if (geteuid() != 0) {
		fprintf(stderr, "Need root: sudo %s [start] [end]\n", argv[0]);
		return 1;
	}

	if (iopl(3) < 0) {
		perror("iopl");
		return 1;
	}

	printf("WOOKING X15 EC Register Dump\n");
	printf("Protocol: outb(0x80,0x66) -> outb(addr,0x62) -> inb(0x62)\n\n");

	/* Known working registers */
	{
		uint8_t t;
		printf("=== Quick Verification ===\n");
		if (ec_read_u8(0x20, &t) == 0)
			printf("  CPU Temp (0x20)  = %u C\n", t);
		if (ec_read_u8(0xB2, &t) == 0)
			printf("  Aux Temp (0xB2)  = %u C\n", t);
	}

	/* Dump requested range */
	dump_range(start, end, "EC Dump");

	/* Also dump common fan/temp regions */
	if (start > 0x30 || end < 0x30)
		dump_range(0x20, 0x30, "Temperature sensors");
	if (start > 0xB0 || end < 0xC0)
		dump_range(0xB0, 0xBF, "Aux sensor region");
	if (start > 0xC0 || end < 0xD0)
		dump_range(0xC0, 0xCF, "Fan control region");

	printf("\nDone. Run with address range to dump specific area:\n");
	printf("  sudo %s 0x00 0xFF    # Full dump\n", argv[0]);
	printf("  sudo %s 0x90 0xAF    # Fan speed area\n", argv[0]);

	return 0;
}
