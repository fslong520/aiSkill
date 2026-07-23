#!/bin/bash
# Install mechrevo_fan kernel module
set -e

SRC="/home/fslong/.config/opencode/skills/mechrevo-fan"
DST="/usr/src/mechrevo-fan"
VER="1.0.0"
MOD="mechrevo_fan"

# Check root
if [ "$(id -u)" -ne 0 ]; then
    echo "请以 root 运行：sudo $0"
    exit 1
fi

echo "==> 复制源码到 $DST"
mkdir -p "$DST"
cp "$SRC/$MOD.c" "$DST/"
cp "$SRC/Makefile" "$DST/"
cp "$SRC/dkms.conf" "$DST/"

echo "==> 注册 DKMS"
dkms add "$MOD/$VER" 2>/dev/null || dkms add "$DST"
dkms build "$MOD/$VER"
dkms install "$MOD/$VER"

echo "==> 加载模块"
modprobe "$MOD" || true

echo "==> 验证"
lsmod | grep "$MOD" && echo "[OK] 模块已加载" || echo "[!] 模块未加载"
echo ""
echo "查看传感器：sensors"
echo "查看温度：cat /sys/class/hwmon/hwmon*/temp1_input"
echo "查看风扇：cat /sys/class/hwmon/hwmon*/fan1_input"
echo "查看日志：dmesg | grep mechrevo_fan"
