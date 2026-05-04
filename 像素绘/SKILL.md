---
name: 像素绘
version: 1.1.0
description: 像素艺术 + 彩色 Emoji 合成插图生成器。5 种艺术风格（Default MC像素/沙雕搞笑/可爱Q版/暗黑硬核/极简黑白），根据用户故事情节生成合成插图。
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  trigger: 用户需要生成插图、像素画、场景示意图、MC风格配图、沙雕搞笑图
---

# 像素绘 - Pixel Art + Emoji Composite Illustrator

## 这个技能是做什么的？

**一句话**：根据故事场景，生成 MC 像素风人物/地形 + 彩色 Emoji 自然元素的合成插图。

**工作流程**：
```
用户故事/场景 → AI 分析 12 维度 → Python 生成像素底图 → PangoCairo 渲染彩色 Emoji → 合成输出 PNG
```

**技术栈**：
- **像素绘制**：PIL/Pillow (像素方块、人物、地形)
- **彩色 Emoji**：PangoCairo + Noto Color Emoji (云、树、花、动物)
- **合成**: 500×281 底图 → 4x NEAREST → 2000×1124 (16:9)
- **字体**: DejaVuSans + 中文字体 (招牌文字)

---

## 核心理念

**像素做骨架，Emoji 做血肉。风格定灵魂。**

| 元素 | 绘制方式 | 原因 |
|------|----------|------|
| 人物 | 像素绘制 (风格决定比例) | 需要精确控制姿态、表情 |
| 地形/建筑 | 像素方块 (12×12 网格) | MC 风格的核心视觉 |
| 天空/植物/动物 | Noto Color Emoji | 原生彩色、细节丰富 |
| 文字 | PIL 字体渲染 | 中文招牌/标题 |
| 风格 | 由 `style` 维度控制 | 见下方 🎨 艺术风格体系 |

---

## 🎨 艺术风格体系

像素绘支持多种艺术风格，AI 根据场景内容自动选择或用户指定。

### 风格总览

| 风格 | 特征 | 人物比例 | 颜色 | 适用场景 |
|------|------|----------|------|----------|
| **Default** 🏗️ | MC 像素风 + Emoji 自然元素 | Steve 头12×12 身高32px | 自然系 | OJ 题图、教程配图 |
| **沙雕** 🤪 | 夸张大头、爆笑表情、特效环绕 | 大头18×18 身高24px | 超高饱和 | 搞笑题、整活、社区娱乐 |
| **可爱** 🎀 | Q 版 2 头身、圆润、柔和 | 大头14×14 身高20px | 粉嫩/暖色 | 儿童教育、入门题 |
| **暗黑** 🌑 | 深色系、冷色调、硬朗线条 | MC 比例 + 护甲 | 暗灰/紫/红 | BOSS 战、困难题、挑战 |
| **极简** ◻️ | 纯黑白 + 单色 emoji | 火柴人 8×16px | 黑/白/灰 | 算法图解、流程图场景 |

### 各风格详细说明

#### 1️⃣ Default 🏗️（经典 MC 像素风）

```
配色：自然系 (草绿 100-120, 天蓝 145-200, 泥土棕 115-160)
人物：Steve 比例 (头12×12, 身体10×12, 手臂3×10, 腿4×8)
表情：标准像素脸 (2px 眼, 4px 嘴微笑)
特效：无额外表情符号
Emoji：自然元素为主 (🌲🍓☀️☁️🕊️🌸🦋)
```

#### 2️⃣ 沙雕 🤪（夸张搞笑风）

```
配色：超高饱和 (草绿 100-255, 天蓝 100-255, 衣服纯红 255-50)
人物：大头版 (头18×18, 身体14×12, 手臂夸张挥舞)
表情：超大眼睛 (4×6px 白底), 大张嘴 (8×3px 带舌头/牙齿)
特效：💦汗 💡灯泡 ❓问号 ⭐星星 ⚡闪电 环绕头部
Emoji：全部可用 + 😎😱😂 表情贴纸
招牌：可加 🚧 🔥 ⚠️ 等装饰
太阳：☀️+😎 太阳戴墨镜
色彩过饱和、对比强烈
```

**绘制要点：**
```python
def shadiao_head(x, y, skin, hair, expression='happy'):
    # 头 18×18 - 比 default 大 50%
    for iy in range(18):
        for ix in range(18):
            if abs(ix-9)+abs(iy-9) <= 11: pix(x+ix, y+iy, skin)
    # 超大眼睛 (4×6)
    rect(x+4, y+6, x+8, y+11, P['wh'])
    pix(x+5, y+7, P['eye']); pix(x+6, y+7, P['eye']); pix(x+7, y+7, P['eye'])
    # 大嘴/大笑/尖叫
    rect(x+5, y+13, x+13, y+15, P['bl'])
    rect(x+7, y+14, x+11, y+16, (220,60,60))  # 舌头
    # 腮红
    rect(x+1, y+9, x+3, y+12, (255,120,140))
```

#### 3️⃣ 可爱 🎀（Q 版萌系）

```
配色：粉嫩/暖色 (草绿 150-220, 天蓝 180-240, 粉色点缀)
人物：Q 版比例 (头14×14, 身体10×10, 手臂2×8, 腿3×6)
表情：星星眼 (✨ 或 4px 闪亮眼), 小嘴 (2px), 腮红
特效：🌸✨💕 飘落
Emoji：🌸💕✨🎀🐰🌈
线条柔和、色彩温暖
```

#### 4️⃣ 暗黑 🌑（硬核挑战风）

```
配色：暗色系 (草地灰绿: 60-100, 天空暗紫/灰, 泥土深棕)
人物：MC Steve + 铁甲/钻石甲 (盔甲覆盖身体)
表情：冷酷 (单线眼, 无嘴或紧嘴)
特效：🌑💀⚡🔥 粒子
Emoji：🌑💀🔥⚡👹
对比强烈、高光锐利
```

#### 5️⃣ 极简 ◻️（算法图解风）

```
配色：纯黑白 + 单色 (仅用 3-4 色)
人物：火柴人 (头 8×8, 身体 4×10, 手臂/腿 2×6)
表情：· · (点眼)  — (线嘴)
Emoji：仅用黑白单色 emoji 或图标
无渐变、无抖动纹理、纯平涂
适用于流程图、算法示意图
```

---

## 思考维度框架（13 维度）

生成插图时，按以下维度逐层思考：

### 0️⃣ 艺术风格 Style（新增 — 首选确定）

| 参数 | 选项 |
|------|------|
| 风格 | **Default** 🏗️ / **沙雕** 🤪 / **可爱** 🎀 / **暗黑** 🌑 / **极简** ◻️ |
| 选择逻辑 | 根据故事氛围自动选择，或用户指定 |
| 风格影响 | 决定整个流程的人物比例、配色、表情规范 |

### 1️⃣ 场景 Scene
| 问题 | 说明 |
|------|------|
| 故事发生在哪里？ | 田野、森林、海边、城市… |
| 什么时间？ | 白天、黄昏、夜晚… |
| 天气如何？ | 晴天、多云、雨… |

### 2️⃣ 天空 Sky (L0)
| 参数 | 选项 |
|------|------|
| 天空渐变 | 从(顶色)到(底色) |
| 太阳 ☀️ | XS/S/M/L |
| 云朵 ☁️ | 数量、大小(远小近大) |
| 飞鸟 🕊️ | 数量、位置（用 🕊️ 白鸽，不用 🐦） |

### 3️⃣ 远景 Background (L1)
| 参数 | 选项 |
|------|------|
| 远山 | 像素绘制 (正弦波) |
| 远树 🌲 | Emoji, 尺寸XS/S |
| 远景填充 | 与草地过渡色 |

### 4️⃣ 地形 Terrain (L2)
| 参数 | 选项 |
|------|------|
| 方块体系 | 12×12 像素网格 |
| 草地色 | 顶面色、侧面色、阴影色 |
| 泥土色 | 浅→深多层 |
| 层数 | 草地→泥土 3-4 层 |

### 5️⃣ 建筑 Structure (L2)
| 参数 | 选项 |
|------|------|
| 栅栏 | 柱子(每4格) + 横栏(满宽) |
| 棚屋/房屋 | 像素方块搭建 |
| 招牌 | 像素方块 + 中文文字 |

### 6️⃣ 中景 Midground (L2)
| 参数 | 选项 |
|------|------|
| 近树 🌲 | Emoji, 尺寸M/L/XL |
| 灌木/草丛 | 像素点 |
| 其他建筑 | 像素方块 |

### 7️⃣ 近景 Foreground (L3)
| 参数 | 选项 |
|------|------|
| 小路 | 像素方块 (泥土色) |
| 作物 🍓🌽 | Emoji, 尺寸S/M/L (远小近大) |
| 花草 🌸🌼🌺 | Emoji, 尺寸S/M |

### 8️⃣ 人物 Characters (L4)
| 参数 | 选项 |
|------|------|
| 数量 | 1-N 个 |
| 比例 | **Default**: Steve 头12×12 身高32px / **沙雕**: 大头18×18 身高24px / **可爱**: Q头14×14 身高20px / **暗黑**: Steve+盔甲 / **极简**: 火柴人8×16px |
| 姿态 | 站立、举手、奔跑、提物、挥舞 |
| 表情 | 像素绘制 (风格决定: 标准眼/超大眼睛/星星眼/冷酷眼) |
| 位置 | 在场景中的坐标 |

### 9️⃣ 点缀 Details (L5)
| 参数 | 选项 |
|------|------|
| 蝴蝶 🦋 | Emoji, 尺寸S/M |
| 花朵 | Emoji, 位置在草地 |
| 小草块 | 像素绿点 |

### 🔟 色调 Palette
| 参数 | 说明 |
|------|------|
| 风格基调 | **Default**: 自然系 / **沙雕**: 超高饱和 / **可爱**: 粉嫩暖色 / **暗黑**: 暗灰冷色 / **极简**: 黑白灰 |
| 主色调 | 草地绿、泥土棕、天空蓝（风格决定饱和度） |
| 角色色 | 皮肤、衣服、头发（风格决定亮度） |
| Emoji 色 | 由 Noto Color Emoji 自带 |

### 1️⃣1️⃣ 图层 Layers
```
L0: 天空渐变
L1: 远景 (远山、云、鸟、太阳)
L2: 中景 (地形方块、栅栏、棚屋、树)
L3: 近景 (小路、作物、招牌)
L4: 角色 (像素绘制)
L5: 点缀 (花、蝶、草)
```

### 1️⃣2️⃣ 画面参数

| 参数 | 默认 | 说明 |
|------|------|------|
| aspect_ratio | 16:9 | 画面比例 |
| base_size | 500×281 | 像素底图尺寸 |
| scale | 4x | NEAREST 缩放 |
| output_size | 2000×1124 | 最终输出尺寸 |

---

## 生成流程

### Step 1: 理解故事

分析用户提供的场景描述，提取关键元素：
- 主要人物、动作、表情
- 环境、地形、建筑
- 植物、动物、自然元素
- 氛围、时间、天气

### Step 2: 维度填充

按 12 维度框架逐一填充内容，确定：
- 每个元素用什么方式绘制（像素/emoji）
- 尺寸大小（远小近大）
- 位置坐标
- 配色方案

### Step 3: 生成 Python 脚本

`generate.py` 包含以下模块：

```python
#!/usr/bin/env python3
"""Auto-generated by 像素绘 skill"""

# 1. Emoji Renderer (PangoCairo + Noto Color Emoji)
def render_emoji(text, size):
    """Render color emoji as RGBA PIL Image."""
    # Cairo ARGB32 → BGRA bytes → un-premultiply → RGBA PIL

# 2. Emoji cache
CACHE = {}
# Pre-render at sizes: XS(22), S(28), M(36), L(44), XL(52)

# 3. Paste helper
def paste_e(im, x, y, e, s='M'):
    """Paste color emoji centered at (x,y) with alpha compositing."""

# 4. Pixel helpers
def rect(), pix(), tb(), mch() ...

# 5. Layer 0-5 drawing (scene-specific pixel art)

# 6. Scale up + Emoji compositing
big = img.resize(...).convert('RGBA')
# paste_e() for each emoji element

# 7. Save
big.save('output.png')
```

### Step 4: 执行脚本

```bash
python3 generate.py
```

### Step 5: 交付

将生成的 PNG 放入题目包的 `additional_file/` 目录。

---

## 像素人物绘制规范

### MC Steve 比例 (1 方块 = 12×12px)

```
头:   12×12 px (方形)
身体: 10×12 px
手臂:  3×10 px (细)
腿:    4×8  px
鞋:    5×3  px
总高:  32 px ≈ 2.7 方块
```

### 面部绘制
```
眼睛: 2px 宽, 棕色/黑色
嘴巴: 4px 宽, 微笑线
头发: 覆盖头顶 4px, 侧边 1px
腮红: (可选) 粉红色块
```

### 动作设计
```
✌️ 胜利手势: 手臂抬起, 两指分开
🧺 提篮子: 手臂伸出, 方块篮子
👋 招手: 手臂举起, 手掌朝前
👉 指向: 手臂前伸, 食指伸出
```

---

## Emoji 尺寸规范

| 尺寸 | 字号 | 使用场景 |
|------|------|----------|
| XS | 22pt | 太阳、云、鸟(最远) |
| S | 28pt | 远树、后排水稻/草莓 |
| M | 36pt | 中树、中排作物、蝴蝶 |
| L | 44pt | 近树、前排作物 |
| XL | 52pt | 最近元素 |

**远小近大原则**：
```
Sky ☀️☁️🕊️ → XS
Hill 🌲    → S/M
Ground 🍓  → S(后) / M(中) / L(前) / XL(最前)
Front 🦋🌸 → M
```

---

## 坐标系统

- **底图画布**: 500×281 px
- **网格**: 12×12 px 方块 (约 42×23 块)
- **y 参考**:
  - y=0-118: 天空
  - y=118-126: 远山
  - y=126-144: 草地过渡
  - y=144+ (行12+): 地形方块
  - 角色 y=150-190: 人物站立位置

**Emoji 粘贴**: 在 4x 缩放后的图像上合成 (2000×1124)
- 坐标 = 底图坐标 × 4
- `paste_e(big, x*S, y*S, "☀️", 'M')`

---

## 图层渲染顺序 (重要)

```
1. L0:  天空渐变 (全画幅底色)
2. L1:  远山、云、太阳、鸟 (从上到下)
3. L2:  地形方块、栅栏、棚屋、树
4. L3:  小路、招牌、作物
5. L4:  像素人物 (前景覆盖)
6. L5:  花、蝴蝶、草 (最上层点缀)
7.      放大 4x + Emoji 合成叠加
```

⚠️ **Emoji 必须在缩放后合成**，否则 NEAREST 缩放会破坏 emoji 细节。

---

## 环境准备

### 系统依赖

```bash
# Ubuntu/Debian
sudo apt install -y python3-pip python3-numpy python3-gi python3-gi-cairo \
  fonts-noto-color-emoji fonts-dejavu-core fonts-noto-cjk \  
  libcairo2-dev libpango1.0-dev

# 检查关键字体
fc-list | grep -i "Noto Color Emoji"  # 必须存在
fc-list | grep -i "DejaVu Sans"       # 必须存在
fc-list | grep -i "CJK\|GB18030"      # 用于中文文字

# Python 包
pip install Pillow numpy pycairo
```

### 字体内置 (推荐)

字体随技能打包在 `assets/` 目录，无需系统安装：

| 文件名 | 大小 | 用途 |
|--------|------|------|
| `NotoColorEmoji.ttf` | 10MB | 彩色 Emoji (PangoCairo) |
| `DejaVuSans.ttf` | 742KB | Emoji 回退 (PIL 备用) |
| `GB_ST_GB18030.ttf` | 19MB | 中文招牌文字 |

**脚本内字体路径**（使用技能目录的相对路径）：
```python
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SKILL_DIR, 'assets')

# PangoCairo Noto Color Emoji (用系统 fontconfig 发现)
fd = Pango.font_description_from_string(f'Noto Color Emoji {size}')

# PIL 中文回退
FONT_CN = os.path.join(ASSETS, 'GB_ST_GB18030.ttf')
ft = ImageFont.truetype(FONT_CN, 16)

# PIL Emoji 回退 (PangoCairo 不可用时)
FONT_EMOJI = os.path.join(ASSETS, 'DejaVuSans.ttf')
```

### 自检脚本

首次使用前运行检查：

```python
def check_env():
    import gi, cairo, numpy, PIL
    print(f"Pillow: {PIL.__version__}")
    print(f"Cairo: {cairo.version}")
    print(f"NumPy: {numpy.__version__}")
    # 检查字体
    import subprocess
    r = subprocess.run(['fc-list', ':lang=zh'], capture_output=True, text=True)
    print(f"中文字体: {'✓' if r.stdout else '✗ 缺少'}")
    r = subprocess.run(['fc-list', 'Noto Color Emoji'], capture_output=True, text=True)
    print(f"Emoji字体: {'✓' if 'Noto' in r.stdout else '✗ 缺少'}")
```

---

## 技术要点

### PangoCairo 渲染 Emoji
```python
# Cairo ARGB32 → BGRA → 去预乘 → RGBA PIL
arr = np.frombuffer(buf, np.uint8).reshape(h, w, 4)
af = arr[:,:,3].astype(np.float32)/255.0
r = np.clip(arr[:,:,2].astype(np.float32)/af, 0, 255).astype(np.uint8)
g = np.clip(arr[:,:,1].astype(np.float32)/af, 0, 255).astype(np.uint8)
b = np.clip(arr[:,:,0].astype(np.float32)/af, 0, 255).astype(np.uint8)
return Image.fromarray(np.stack([r,g,b,arr[:,:,3]],2), 'RGBA')
```

### Alpha 合成 (PIL paste)
```python
img_big.paste(emoji_img, (x, y), emoji_img)  # 第三个参数作 mask
```

### 地形方块 3D 效果
```python
def tb(bx, by, top_c, side_c, dark_c):
    # 顶面 4px: 使用 top_c, (ix+iy)%5 产生抖动纹理
    # 侧面 8px: 使用 side_c, (ix+iy)%4 产生抖动阴影
```

---

## 示例

### 示例 1: Default 🏗️

**用户输入** | 五一假期小明去草莓园，不能摘相邻垄，用 DP 算法决定怎么摘最多。

**AI 输出**
```
风格: Default 🏗️
生成 2000×1124 PNG:
- L0: 蓝天渐变 + ☀️(XS) + ☁️(XS) + 🕊️(XS)
- L1: 远山 + 草地过渡
- L2: 草方块地形 + 栅栏 + 棚屋 + 🌲(S/M/L/XL)
- L3: 泥土小路 + 🍓(S/M/L/XL 六排) + 招牌"草莓"
- L4: 👦小明(✌️+🧺) + 👩妈妈(👋) + 👦表弟(👉🍓)
- L5: 🌸🌼🌺 花朵 + 🦋 蝴蝶
```

### 示例 2: 沙雕 🤪

**用户输入** | 赤石科技：铁傀儡机 p×a 个，草羊机 q×b 个，大钟 c×r 个，各需 x/y/z 分钟，总时间？

**AI 输出**
```
风格: 沙雕 🤪 (超高饱和配色)
生成 2000×1124 PNG:
- L0: 蓝天 + ☀️😎 太阳戴墨镜 + ☁️(S) + 🕊️(XS)
- L2: 三个彩色平台 + ⚙️🤖💥 / ⚙️🐑💨 / 🔔🔔🎵
- L3: 招牌"🚧 赤石科技 施工中 🚧"
- L4: 🧑 大头孙义淳 (18×18头 巨眼大嘴) + 思考气泡 p×a×x+q×b×y+c×r×z=?
- L4: 💦💡❓⭐⚡ 表情环绕
- L5: 🌸🌼🌺🌻 + 🦋
```

---

## 注意事项

1. **Emoji 必须缩放后合成** — 在底图上直接渲染 emoji 再 NEAREST 缩放会破坏细节
2. **Cairo 字节序** — FORMAT_ARGB32 是 BGRA 顺序，需转换为 RGBA
3. **Alpha 去预乘** — Cairo 使用预乘 alpha，需还原
4. **PangoCairo 后端** — 需设置 `os.environ['PANGOCAIRO_BACKEND'] = 'fontconfig'`
5. **字体路径** — Noto Color Emoji: `/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf`
6. **坐标一致性** — 先计算底图坐标 (500×281)，缩放时 ×4
7. **版权** — 生成的角色/场景注意版权问题

---

## 更新记录

- 2026-04-30: v1.0 初始版本，基于五一采摘园案例抽象
