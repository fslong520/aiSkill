---
name: system-ctl
description: |
  openKylin 3.0 UKUI 桌面系统控制统一入口。封装 KylinBot 12 个技能（audio/bluetooth/keyboard/mouse/navigations/network-manager/osdserver/panel/power/shortcut-navigations/srceen/touchpad）为单脚本 sysctl，经 gdbus(nmcli/ukui-bluetooth-cli) 控制音量、亮度、屏幕模式、电源电量、触摸板、任务栏、键盘、鼠标、OSD 提示、打开控制中心/系统应用、快捷键、WiFi/有线网络、蓝牙。
  触发词：调音量、音量多少、静音、麦克风、调亮度、屏幕亮度、护眼、夜间模式、缩放、电量、还有多少电、充电、电源模式、触摸板、触控板、任务栏、面板、键盘、按键重复、鼠标速度、光标、系统提示 OSD、打开控制中心、打开设置、打开终端、WiFi、无线网络、蓝牙、连接蓝牙、截图、快捷键。
version: 1.0.0
author: opencode 用户技能（源自 KylinBot/ukui）
tags:
  - 系统控制
  - UKUI
  - openKylin
  - 音量
  - 亮度
  - 电源
  - 触摸板
  - 蓝牙
  - 网络
  - gdbus
---

# 系统控制（openKylin UKUI）

统一封装脚本：`sysctl`。覆盖 KylinBot 12 个技能的**全部** DBus/nmcli 方法，命令全部可从 `/usr/share/kylinbot/.kylinbot/workspace/skills/*/SKILL.md` 溯源。

## 脚本位置

```
~/.config/opencode/skills/系统控制/sysctl
```

依赖：`gdbus`、`nmcli`、`python3`（均在 openKylin 3.0 预装）。蓝牙操作依赖上游 `ukui-bluetooth-cli.py`（`/usr/share/kylinbot/.kylinbot/workspace/skills/bluetooth/ukui-bluetooth-cli.py`），不改动该文件，仅调用。

## 通用用法

```bash
sysctl <域> <子命令> [参数...]   # 执行
sysctl --dry-run <域> <子命令> ...   # 只打印将执行的命令，不实际执行（写操作预览）
sysctl help                       # 列出全部子命令
```

- 读操作为查询，直接输出 gdbus/nmcli 原始返回值。
- 写操作为显式子命令（`set`/`mute`/`on`/`off`/`mode` 等），改变系统状态；不确定影响时先用 `--dry-run`。
- 参数校验严格：音量 0-100、模式 0-2、位置 0-3 等，越界即报错并返回非零。
- 出错返回非零退出码。

## 子命令总览

| 域 | 子命令 | 说明 |
|----|--------|------|
| `volume` | `get` / `set <0-100>` / `mute` / `unmute` / `mute-status` / `device` / `device-set <设备> [端口]` / `mic-get` / `mic-set <0-100>` / `mic-mute` / `mic-unmute` | 音频：输出音量、静音、输出设备、麦克风 |
| `screen` | `brightness` / `brightness-get` / `brightness <0-100>` / `brightness-set <名> <0-100>` / `brightness-all <0-100>` / `mode [模式]` / `eyecare on|off` / `eyecare-status` / `night on|off` / `scale <1.0-2.0>` / `scale-status` / `autobright on|off` / `increase` / `decrease` | 屏幕：亮度、显示模式、护眼、夜间、缩放、自动亮度、内置屏增/减亮 |
| `power` | `status` / `battery` / `state` / `time-empty` / `time-full` / `mode [0|1|2]` / `power-button [动作]` / `lid [动作]` / `screen-timeout-ac [秒]` / `screen-timeout-dc` / `sleep-timeout-ac` / `low-battery` / `low-battery-threshold` / `low-battery-notify` / `show-left-time` / `battery-present` / `lid-present` / `ac-policy` / `dc-policy` | 电源：电量、充电状态、剩余时长、电源模式、按键/合盖动作、息屏/睡眠超时、低电量策略 |
| `touchpad` | `status` / `on` / `off` / `count` / `disable-on-mouse on|off` / `disable-typing on|off` / `tap on|off` / `natural on|off` / `scroll <0|1|2>` / `speed <数字>` | 触摸板：开关、数量、插鼠标禁用、打字禁用、轻触、自然滚动、滚动类型、速度 |
| `panel` | `mergestatus` / `merge <0|1|2>` / `location-status` / `location <0|1|2|3>` / `sizepolicy-status` / `sizepolicy <0|1|2>` / `autohide-status` / `autohide on|off` / `lock-status` / `lock on|off` / `allscreens-status` / `allscreens on|off` / `tray-all on|off` / `taskicons <0|1>` / `taskview on|off` / `search on|off` | 任务栏：图标合并、位置、尺寸、自动隐藏、锁定、多屏、托盘、图标策略、按钮显隐 |
| `kbd` | `repeat-status` / `repeat on|off` / `locktip-status` / `locktip on|off` / `count` | 键盘：按键重复、CapsLock 提示、键盘数量 |
| `mouse` | `cursor-theme [主题]` / `cursor-size <尺寸>` / `speed <数字>` / `accel on|off` / `wheel <值>` / `left-handed on|off` / `natural-scroll on|off` / `locate <0|1|2>` / `double-click <毫秒>` / `middle on|off` / `count` | 鼠标：光标主题/大小、速度、加速、滚轮、左手、自然滚动、指针定位、双击、中键、数量 |
| `osd` | `volume <值> <max>` / `volume-mute <值> <max> <bool>` / `brightness <值> <max>` / `flight on|off` / `flight-osd <bool>` / `touchpad on|off` / `touchpad-osd <bool>` / `mic on|off` / `mic-osd <bool>` / `camera on|off` / `camera-osd <bool>` / `audio on|off` / `audio-osd <bool>` / `power-mode <perf|eco|auto>` / `power-mode-osd <0|1|2>` / `wifi on|off` / `wifi-osd <bool>` / `custom <图标名>` / `bar <id> <值> <max>` | 屏幕提示（OSD）。**仅显示，不改变系统状态**，可放心实测 |
| `nav` | `open <模块>` | 打开系统应用。模块：audio display theme power bluetooth touchpad date shortcut keyboard wlan net userinfo screensaver screenlock notice upgrade security vino printer proxy hotspot area backup autostart login devicemanager monitor clock music video；亦直接接受方法全名如 `OpenUkccAudio` |
| `shortcut` | `volume-up` / `volume-down` / `mute` / `mic-mute` / `bright-up` / `bright-down` / `touchpad-toggle` / `touchpad-on` / `touchpad-off` / `power-down` / `power-off` / `wlan-toggle` / `flight-toggle` / `flight-on` / `flight-off` / `bluetooth-toggle` / `screenshot` / `screenshot-window` / `screenshot-area` / `file-manager` / `calculator` / `email` / `www` / `settings` / `terminal` / `search` / `sidebar` / `window-switch` / `screensaver` / `clipboard` / `kylin-manager` / `screencap` / `display-switch` / `performance-switch` / `ai-assistant` / `camera-toggle` / `media-play` / `media-pause` / `media-playpause` / `media-stop` / `media-next` / `media-prev` / `media-repeat` / `media-shuffle` | 快捷键（44 个方法）：音量/亮度/触摸板/电源/网络/截图/打开应用/媒体键；亦直接接受方法名如 `VolumeUp` |
| `net` | `status` / `connections` / `active` / `scan` / `wifi [on|off]` / `connect <连接>` / `connect-wifi <SSID> [密码]` / `static-ip <连接> <IP/前缀> [网关] [DNS]` / `dhcp <连接>` / `disconnect <连接>` / `ethernet [on|off]` | 网络（nmcli）：设备状态、连接列表、Wi-Fi 扫描/开关/连接、静态 IP、DHCP、断开、有线开关 |
| `bt` | `power on|off` / `tray on|off` / `discoverable on|off` / `active-connection on|off` / `audio-combine on|off` / `scan on|off` / `list` / `connect <地址>` / `info <地址>` | 蓝牙（包装 ukui-bluetooth-cli.py）：电源、托盘图标、可发现性、自动发现音频、组合设备、扫描、列表、连接、信息 |

## 示例

```bash
# 音量
sysctl volume get                # 查输出音量 → (67,)
sysctl volume set 60             # 音量调到 60
sysctl volume mute               # 静音
sysctl volume mic-set 50         # 麦克风音量 50

# 屏幕
sysctl screen brightness         # 查全部显示器亮度 → (@a(suuu) [],)
sysctl screen brightness-get     # 主屏亮度 → (uint32 70,)
sysctl screen brightness 80      # 主屏亮度调到 80
sysctl screen eyecare on         # 开启护眼
sysctl screen scale 1.25         # 缩放 125%

# 电源
sysctl power status              # → 电量 100%，状态 充满，模式 平衡
sysctl power battery             # → (100,)
sysctl power mode 0              # 切到性能模式

# 触摸板 / 键盘 / 鼠标
sysctl touchpad status           # → (true,)
sysctl kbd count                 # → (2,)
sysctl mouse cursor-theme        # → ('dark-sense',)

# 任务栏
sysctl panel mergestatus         # → (0,)  0=始终合并 1=从不 2=窗口满时
sysctl panel merge 2

# OSD（仅显示，低风险）
sysctl osd volume 60 100         # 显示音量条
sysctl osd power-mode perf       # 显示性能模式图标

# 打开应用
sysctl nav open audio            # 打开控制中心-声音
sysctl nav open monitor          # 打开系统监视器
sysctl shortcut terminal         # 打开终端
sysctl shortcut screenshot       # 全屏截图

# 网络
sysctl net status                # nmcli device status
sysctl net scan                  # 扫描 Wi-Fi
sysctl net wifi on               # 开 Wi-Fi
sysctl net connect-wifi MyWifi 密码123
sysctl net static-ip "有线连接 1" 192.168.1.100/24 192.168.1.1 8.8.8.8

# 蓝牙
sysctl bt power on
sysctl bt list
sysctl bt connect AA:BB:CC:DD:EE:FF

# 写操作预览（不执行）
sysctl --dry-run volume set 50
```

## 前置条件

- **系统**：openKylin 3.0（huanghe），UKUI 桌面会话，x86_64。
- **DBus session bus 可达**：`DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus`；桌面会话内自动就绪。
- **服务**：`org.ukui.Framework` 运行中（UKUI 桌面登录后即有）。
- **命令**：`gdbus`、`nmcli`、`python3` 于 PATH。
- **蓝牙**：系统服务 `com.ukui.bluetooth` 运行中，依赖 dbus-python（openKylin 预装）。

## 技术栈说明

- 除蓝牙外全部走 session bus 的 `org.ukui.Framework`，对象路径与接口：
  - `org.ukui.Framework.Devices.{Audio,Screen,Power,Touchpad,Keyboard,Mouse}`
  - `org.ukui.Framework.UI.{Panel,OsdServer}`
  - `org.ukui.Framework.Navigations`
  - `org.ukui.Framework.ShortcutNavigations`
- 网络走 `nmcli`（NetworkManager）。
- 蓝牙走上游 `ukui-bluetooth-cli.py`（system bus `com.ukui.bluetooth`）。

## 注意事项

- **只读来源**：命令源自 `/usr/share/kylinbot/.kylinbot/workspace/skills/*/SKILL.md`，不发明未记载之 DBus 方法。
- **写操作谨慎**：`set`/`mute`/`on`/`off`/`mode` 等会改系统状态；不确定时先 `--dry-run`。脚本不改音量、亮度、开关状态除非显式调用对应写子命令。
- **枚举空值**：`screen brightness`（GetAllScreenBrightness）返回 `@a(suuu) []` 属正常，服务端未枚举到显示器；改查 `brightness-get` 得主屏值。
- **硬件限制**：`kbd locktip-status` 在部分机型报 `The machine does not support`，服务端不支持所致，非脚本故障。
- **多屏错误**：`screen scale-status`（GetScreenScale）在屏幕数量超限时报 `screen count beyond 1`，服务端行为。
- **蓝牙无 disconnect**：上游 `ukui-bluetooth-cli.py` 无断开设备子命令，仅 `power off` 关适配器；未封装不存在的命令。
- **OSD 域仅显示**：`osd` 全部子命令只弹屏幕提示，不改变系统状态，可安全测试。
