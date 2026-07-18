#!/bin/bash
# blaze-fan.sh — 炽风智能风扇调速
# 检测最热设备，指数曲线调风扇转速
# 支持 Clevo 直控 (clevo-indicator) / nbfc-linux 双后端
#
# 用法: sudo ./blaze-fan.sh [间隔秒数]

set -e

# ============ 可调参数 ============
BASE=40          # 最低风扇转速 %
POWER=2          # 指数 (2=二次, 3=更陡)
TEMP_START=60    # 开始提速温度 °C
TEMP_MAX=75      # 满速温度 °C
INTERVAL=${1:-5} # 采样间隔 秒
# ================================

FAN_CLEVO="/usr/bin/clevo-indicator"
FAN_NBFC="/usr/bin/nbfc"

# ---------- 环境检测 ----------
die() { echo "[错误] $*" >&2; exit 1; }
warn() { echo "[警告] $*" >&2; }
info() { echo "[信息] $*"; }

need_cmd() { command -v "$1" >/dev/null 2>&1 || die "需安装 $1"; }
need_cmd sensors
need_cmd bc
[ "$(id -u)" = "0" ] || die "需 root 权限"

# ---------- 检测风扇后端 ----------
detect_backend() {
    if [ -x "$FAN_CLEVO" ]; then
        echo "clevo"
    elif [ -x "$FAN_NBFC" ]; then
        echo "nbfc"
    else
        die "无可用风扇后端。Clevo 本: yay -S clevo-indicator-git；其它本: yay -S nbfc-linux"
    fi
}

BACKEND=$(detect_backend)
info "后端: $BACKEND"

# ---------- 设风扇转速 ----------
set_fan() {
    local duty=$1
    case "$BACKEND" in
        clevo) "$FAN_CLEVO" "$duty" >/dev/null 2>&1 ;;
        nbfc)  "$FAN_NBFC" set -s "$duty" >/dev/null 2>&1 ;;
    esac
}

# ---------- 检测最热设备 ----------
# 遍历所有传感器，取 temp*_input 最大值
get_hottest_temp() {
    sensors -u 2>/dev/null | awk '
        /_input/ {
            val = $2
            if (val > max) {
                max = val
                name = prev_name
            }
        }
        /^[a-zA-Z]/ {
            gsub(/-.*$/, "", $1)
            if ($1 != "") prev_name = $1
        }
        END {
            if (max != "") printf "%s %.0f\n", name, max
            else print "unknown 50"
        }
    '
}

# ---------- 指数曲线 ----------
calc_duty() {
    local t=$1
    if (( $(echo "$t <= $TEMP_START" | bc -l) )); then
        echo "$BASE"; return
    fi
    if (( $(echo "$t >= $TEMP_MAX" | bc -l) )); then
        echo "100"; return
    fi
    local range=$(( TEMP_MAX - TEMP_START ))
    local progress=$(echo "scale=4; ($t - $TEMP_START) / $range" | bc)
    local exp_val=$(echo "scale=6; $progress ^ $POWER" | bc)
    local duty=$(echo "scale=0; $BASE + (100 - $BASE) * $exp_val" | bc)
    echo "$duty"
}

# ============ 主循环 ============
info "炽风启动 — 目标: 最热设备 | 曲线: ${TEMP_START}°C↑ ${BASE}% → ${TEMP_MAX}°C 100%^${POWER}"
info "间隔: ${INTERVAL}s | 后端: $BACKEND"
echo "----------------------------------------"

# 先写一次 50% 激活手动模式
set_fan 50

while true; do
    read -r hottest_sensor hottest_temp < <(get_hottest_temp)
    duty=$(calc_duty "$hottest_temp")
    [ -z "$duty" ] && duty=$BASE
    [ "$duty" -lt "$BASE" ] && duty=$BASE
    [ "$duty" -gt 100 ] && duty=100

    set_fan "$duty"
    echo "[$(date +%H:%M:%S)] ${hottest_sensor} ${hottest_temp}°C → ${duty}%"
    sleep "$INTERVAL"
done
