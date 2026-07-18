---
name: 炽风
description: "🔥💛 通用 EC 风扇调速方法论。不认品牌，只认接口。探 EC→定方案→控风扇。"
metadata:
  slug: blazefan
  priority: 500
  trigger: 风扇、散热、温度高、EC、Embedded Controller、降温、调速、炽风、电脑热
  copaw:
    emoji: "🔥💛"
    requires: {}
    auto_load: false
---

# 🔥💛 炽风 - 通用 EC 风扇调速方法论

> 不关心你是什么品牌。只关心：**EC 暴露了什么接口？**

---

## 〇：问题本质

每台有风扇的电脑都有一颗 **Embedded Controller（EC）**——独立单片机，读温度、控风扇。OS 只能通过 EC 暴露的接口间接控制风扇。

可能的接口只有三种，且优先顺序如下：

```
① sysfs       ── 最安全，系统给你封装好了
② EC寄存器     ── 次之，直接读写 EC 内存空间
③ I/O端口命令  ── 最底层，裸硬件协议
```

方法论就是：**逐个排查，通哪个用哪个。**

---

## 一、排查接口（不依赖品牌的三步排查）

### ═══ Step 1：查 sysfs ═══

内核驱动加载后，风扇接口可能出现在以下位置：

```bash
# PWM 接口（桌面主板 + 部分笔记本）
find /sys/class/hwmon -name 'pwm*' 2>/dev/null

# 风扇转速输入
find /sys/class/hwmon -name 'fan*_input' 2>/dev/null

# ThinkPad 特殊路径（非品牌专属，仅作接口示例）
cat /proc/acpi/ibm/fan 2>/dev/null

# 通用设备树
find /sys/devices -name '*fan*' -type f 2>/dev/null
```

有输出 → 尝试写入：

```bash
# 如果发现 /sys/class/hwmon/hwmonX/pwm1
echo 128 > /sys/class/hwmon/hwmonX/pwm1   # 0=停, 255=满速
```

风扇应声变速 → 走 sysfs 方案。写入无权限 → 需加载对应驱动（`modprobe it87` 或 `modprobe nct6775` 等）。

### ═══ Step 2：查 EC 寄存器空间 ═══

内核提供 `ec_sys` 模块，暴露 EC 全部 256 字节寄存器：

```bash
# 加载模块（写支持需参数）
sudo modprobe ec_sys write_support=1

# 如果模块不存在或加载失败 → 内核未编译此模块，跳至 Step 3

# 查看 EC 寄存器全像
sudo hexdump -C /sys/kernel/debug/ec/ec0/io
```

能读到数据 → EC 内部空间已暴露。

**关键问题来了：哪个字节是温度？哪个是风扇？**

靠**差分法**（纯方法论，不依赖任何品牌知识）：

```bash
# 1. 存空闲状态的 EC
sudo xxd /sys/kernel/debug/ec/ec0/io > /tmp/ec_idle

# 2. 制造负载让 BIOS 自动提风扇
stress -c 4 -t 60 &
sleep 30

# 3. 存负载状态
sudo xxd /sys/kernel/debug/ec/ec0/io > /tmp/ec_load

# 4. 对比——变化的字节就是风扇/温度相关
diff /tmp/ec_idle /tmp/ec_load
```

diff 结果解读：
- 数值升高的 → 可能是温度寄存器（温度↑）
- 数值变化且与风扇声音关联 → 可能是占空比或 RPM 寄存器
- 一般在 `0xC0-0xDF` 范围内（经验，非标准）

**验证**：

```bash
# 假设 0xCE 在风扇加速时从 0x30 变为 0xA0
# 尝试向该地址写入值
echo -n -e '\x80' | sudo dd of=/sys/kernel/debug/ec/ec0/io bs=1 seek=0xCE 2>/dev/null
```

写入成功且风扇变声 → 找到了可控寄存器。写回原值不变 → EC 写保护锁定，此路不通。

### 附：风扇数量检测

确定了一个风扇的寄存器后，**不要假设只有一个风扇**。多数笔记本有 2 个，部分有 3 个。

方法一：查 RPM 寄存器

RPM 寄存器通常是连续的 2 字节对：

```bash
# 惯例：0xD0-0xD1 = 风扇1, 0xD2-0xD3 = 风扇2, 0xD4-0xD5 = 风扇3
# 用差分法确认风扇转速变化时哪些地址变了
for i in 0 2 4; do
  hi=$(sudo xxd -s $((0xD0+i)) -l 1 /sys/kernel/debug/ec/ec0/io | awk '{print $2}')
  lo=$(sudo xxd -s $((0xD1+i)) -l 1 /sys/kernel/debug/ec/ec0/io | awk '{print $2}')
  echo "风扇$((i/2+1)): 0x${hi}${lo}"
done
```

如果读出的值不为 0x0000，或负载下明显变化→该风扇存在。

方法二：I/O 端口试写

如果 EC 使用 I/O 端口命令控制风扇（如 Clevo 协议），逐个风扇索引试写：

```
outb(命令, 0x66)          # 写风扇命令
outb(风扇索引, 0x62)      # 索引 0x01, 0x02, 0x03...
outb(占空比, 0x62)        # 如 128（50%）
```

写完后监听 RPM 寄存器或听声音。有反应 → 该风扇存在且独立可控。

常见规律：

| 风扇 | 控制索引 | RPM 寄存器 |
|------|---------|-----------|
| 风扇 1 | 0x01 | 0xD0-0xD1 |
| 风扇 2 | 0x02 | 0xD2-0xD3 |
| 风扇 3 | 0x03 | 0xD4-0xD5 |

注意：索引和寄存器地址不是标准，每台机器不同。差分法定位是第一位的。

### ═══ Step 3：查 I/O 端口通信 ═══

EC 在 x86 平台上标准占用两个 I/O 端口：

```c
#define EC_SC   0x66   // 状态/命令端口
#define EC_DATA 0x62   // 数据端口
```

标准 EC 读写协议：

```c
// --- 读 EC 寄存器 ---
while (inb(EC_SC) & 2);         // 等待 IBF=0
outb(0x80, EC_SC);              // 发送读命令
while (inb(EC_SC) & 2);         // 等待
outb(register_addr, EC_DATA);   // 指定寄存器地址
while ((inb(EC_SC) & 1) == 0);  // 等待 OBF=1
value = inb(EC_DATA);           // 读取值

// --- 写 EC 寄存器 ---
while (inb(EC_SC) & 2);         // 等待 IBF=0
outb(0x81, EC_SC);              // 发送写命令
while (inb(EC_SC) & 2);         // 等待
outb(register_addr, EC_DATA);   // 指定寄存器地址
while (inb(EC_SC) & 2);
outb(value, EC_DATA);           // 写入值
```

判断 EC 是否响应 I/O 端口命令的方法：

```bash
# 尝试通过标准读协议读取寄存器 0x00
# 如果能读到合理的值（非 0xFF 且每次读一致），说明 EC 在响应
# 这需要写一个小 C 程序或使用 /dev/port
```

注意：**不同 EC 固件可能使用私有命令集**。标准 `0x80`/`0x81` 不一定有效。如果标准命令无响应，可能有厂商自定义命令——这通常需要反向工程，超出方法论范围。

---

## 二、三路接口的取舍

```
sysfs 可用?  ──→  用 sysfs，最安全
否
ec_sys 可写? ──→  用 ec_sys，直接读写寄存器
否
I/O 端口通?  ──→  用 I/O 命令控制
否
└── 此机 EC 不开放手动控制
```

### 关于用户态工具

常见的风扇工具有 `nbfc-linux`、`thinkfan`、`clevo-indicator` 等。它们的本质就是封装了上述三种接口之一。

AI 可以直接尝试：

```bash
# 安装 nbfc-linux（通用性最广）
sudo nbfc update
sudo nbfc config --set auto
sudo nbfc restart -r
nbfc status
```

如果 nbfc 能匹配到配置并正确读数 → 走 nbfc 方案，省去手动探测。

但 AI 的核心能力不是记住哪个工具支持哪款机器，而是**当工具不支持时，能退回手动探测**。

---

## 三、控制循环（架构通用）

不管通过哪种接口控风扇，骨架一样：

```
while true:
    temp = 读最热设备温度       # sensors -u | grep _input 取最高
    duty = 指数曲线(temp)       # 公式见下
    for each 已发现的风扇:
        写入风扇(duty)          # 遍历所有风扇！不只写一个
    sleep 5                     # 持续轮询，防 EC 复位
```

**两个要点**：
- **遍历所有风扇**——只写一个，其他可能停转或保持低速。
- **持续轮询**——EC 有自己的固件策略，可能在几秒后覆盖你的设定。每 5 秒重写一次防止被抢回。

### 指数曲线

```
duty = BASE + (100-BASE) × ((temp - START) / (MAX - START))²

BASE=40（最低），START=60（起调），MAX=75（满速）

≤60°C → 40%
65°C   → 47%
70°C   → 67%
75°C   → 100%
```

优点：低温安静，高温迅速响应。

调参口诀：

| 想要 | 调法 |
|------|------|
| 更凉快 | 降 START/MAX，或提指数 POWER=3 |
| 更安静 | 升 START/MAX，或降 BASE=30 |
| 更敏感 | START 降 5°C |
| 更迟钝 | MAX 升 5°C |

---

## 四、AI 执行工作流

```
用户说电脑热
  │
  ├── sensors ── 确认高温（哪个设备？多少度？）
  │
  ├── Step 1: 查 sysfs
  │   ├─ 有 pwm 接口 → 直接写 → 验证 → sysfs 方案
  │   └─ 无 → 继续
  │
  ├── Step 2: 查 ec_sys
  │   ├─ 能加载 → 差分法找风扇寄存器
  │   │   ├─ 可写 → ec_sys 方案
  │   │   └─ 只读 → 继续
  │   └─ 不能加载 → 继续
  │
  ├── Step 3: 查 I/O 端口
  │   ├─ 标准协议通 → I/O 方案
  │   └─ 不通 → 最后尝试 nbfc/nbfc-linux 工具
  │
  ├── 都不通 → 告知用户此机 EC 封闭，仅 BIOS 自控
  │
  ├── 验证：手动写入，听风扇声音变化 + 看 RPM
  ├── 询问偏好：安静/均衡/性能
  ├── 部署守护循环 + systemd 自启
  └── 观察迭代
```

---

## 五、EC 调速避坑

| 坑 | 实情 |
|----|------|
| 把 `temp*_max` 当温度读 | 那是报警阈值，不是当前温度。读 `temp*_input` |
| 认为 EC 寄存器布局有标准 | **没有**。0xC6 在 A 机器是温度，在 B 机器可能是 RPM。必须差分确认 |
| 写完一次就当成功 | EC 会抢回控制权。必须持续轮询覆盖 |
| `ec_probe write` 对所有 EC 有效 | 仅对 ec_sys 直写型有效。I/O 命令型 EC 不吃这套 |
| 同时跑多个风扇工具 | 抢 EC 控制权，冲突 |

---

## 六、调试命令速查（通用）

```bash
# 看温度
sensors -u | grep _input

# 看 sysfs 风扇接口
find /sys/class/hwmon -name 'pwm*' -o -name 'fan*_input' 2>/dev/null

# 挂载并查看 EC 寄存器
sudo modprobe ec_sys write_support=1 2>/dev/null
sudo hexdump -C /sys/kernel/debug/ec/ec0/io 2>/dev/null

# 监控 EC 寄存器变化
sudo watch -t -n 0.5 'xxd -s 0xC0 -l 32 /sys/kernel/debug/ec/ec0/io' 2>/dev/null

# 写 EC 寄存器（试错法）
echo -n -e '\x80' | sudo dd of=/sys/kernel/debug/ec/ec0/io bs=1 seek=0xCE 2>/dev/null

# 全量差分
sudo xxd /sys/kernel/debug/ec/ec0/io > /tmp/ec_before
# ... 制造负载 ...
sudo xxd /sys/kernel/debug/ec/ec0/io > /tmp/ec_after
diff /tmp/ec_before /tmp/ec_after

# ACPI 方法搜索（极少有结果）
which acpiexec && sudo acpiexec /sys/firmware/acpi/tables/DSDT 2>/dev/null | grep -i fan
```
