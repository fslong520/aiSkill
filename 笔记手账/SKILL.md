---
name: 笔记手账
version: 1.5.1
description: 笔记手账风格教育知识卡片Prompt生成器。输入知识点，输出瘦金体优雅简洁的手写体结构化Prompt，支持5套风格主题。
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  slug: note-journal
  trigger: 笔记手账、知识卡片、打卡海报、教学插图、CSP-J风格、瘦金体、科幻风格、活力手账、青绿新生、蔚蓝格调
---

# 笔记手账 - 教育知识卡片Prompt生成器

## 这个技能是做什么的？

**一句话**：输入知识点/主题，输出符合"笔记手账"风格的AI绘图Prompt。

**适用场景**：
- CSP-J/CSP-S/GESP 教学知识卡片
- 每日打卡海报
- 知识点讲解配图
- 学习计划/总结可视化

---

## 风格定义

### 视觉DNA

| 元素 | 特征 |
|------|------|
| **基底** | 米色/奶油色纸张背景，撕纸边缘，活页孔，螺旋装订 |
| **风格** | 经典风格（默认）：复古温暖学院风，各部配色与装饰统一于风格基调 |
| **字体** | 各风格自有匹配字体，详见「风格体系」 |
| **装饰** | 便利贴、纸夹、和纸胶带、星星☆、手绘箭头、涂鸦标记 |
| **布局** | 简洁优雅，留白充足，对齐精确，无杂乱元素 |
| **质感** | 手绘质感，但整体整洁优雅 |

### 风格体系

每套风格不惟配色，更定义视觉语言全貌——装饰元素、背景质感、整体氛围各具面貌。

#### 经典风格（默认）

**视觉特征**：复古温暖学院风，传统手账质感，稳重大方。
**字体**：**瘦金体**——笔画瘦劲，锋芒明显，纤细有力，典雅劲健。
**装饰元素**：星星☆、纸夹、和纸胶带、手绘箭头、便利贴、回形针。
**背景质感**：米色纸张纹理，轻微做旧边缘，活页孔、螺旋装订。
**氛围**：温馨、专注、学术感。

| 颜色 | 色值 | 用途 |
|------|------|------|
| 深蓝 | #1A3A8A | 标题、标签、图标主色 |
| 橙色 | #F97316 | 编号、重点、装饰 |
| 绿色 | #2D8C3C | 副标题、箭头、记忆框 |
| 黄色 | #FBBF24 | 下划线、便利贴、星星 |
| 米色 | #F5F0E8 | 背景纸张 |
| 白色 | #FFFFFF | 内容卡片 |

#### 科幻风格

**视觉特征**：洁净未来科技感，极简冷冽，线条利落。
**字体**：**硬朗黑体**——无衬线科技感，笔画等宽平直，棱角分明，无手写感。
**装饰元素**：几何光点、细线框、全息标签、科技纹路、编码条纹、发光线框。
**背景质感**：深空色底或纯白底配微细网格，金属质感边角，荧光线分隔。
**氛围**：冷静、精准、未来感。

| 颜色 | 色值 | 用途 |
|------|------|------|
| 冰蓝 | #4FC3F7 | 标题、标签、主色 |
| 银灰 | #B0BEC5 | 副标题、图标、边框 |
| 电光紫 | #7C4DFF | 重点、编号、装饰 |
| 深空 | #0D1117 | 背景纸张 |
| 铁灰 | #161B22 | 卡片背景 |
| 冷白 | #E6EDF3 | 正文文字 |

#### 活力手账风格

**视觉特征**：热情元气，笔触活泼，色彩鲜明。
**字体**：**可爱圆体**——圆润饱满，转角柔和，笔画粗细变化大，有手写温度。
**装饰元素**：手绘涂鸦、波浪线、感叹号、贴纸感元素、圆点、彩色回形针、气泡框。
**背景质感**：奶油色暖调纸，轻微纹理，可见纤维感。
**氛围**：活力、积极、轻松。

| 颜色 | 色值 | 用途 |
|------|------|------|
| 活力橙 | #FF6B35 | 标题、标签、主色 |
| 珊瑚红 | #FF4757 | 副标题、重点、装饰 |
| 薄荷绿 | #2ED573 | 箭头、记忆框、图标 |
| 柠檬黄 | #FFC312 | 下划线、便利贴、星星 |
| 奶油白 | #FFF9E6 | 背景纸张 |
| 浅灰 | #F5F5F5 | 内容卡片 |

#### 青绿新生风格

**视觉特征**：自然清新，东方素雅，宁静中生趣。
**字体**：**行楷**——行书之流畅兼楷书之法度，笔画连带自然，温润如玉。
**装饰元素**：叶片纹路、水墨感点缀、细枝线条、露珠、留白晕染。
**背景质感**：米白纸，极轻水彩纹理，边缘自然渗化。
**氛围**：清透、成长、安宁。

| 颜色 | 色值 | 用途 |
|------|------|------|
| 青绿 | #00B894 | 标题、标签、主色 |
| 深青 | #006266 | 副标题、图标、边框 |
| 浅绿 | #55E6C1 | 重点、装饰、箭头 |
| 米白 | #F8F9FA | 背景纸张 |
| 浅灰 | #E9ECEF | 内容卡片 |
| 深灰 | #2D3436 | 正文文字 |

#### 蔚蓝格调风格

**视觉特征**：海洋灵感，专业冷静，干练整洁。
**字体**：**清秀宋体**——横细竖粗，起落有装饰角，端正典雅，专业感强。
**装饰元素**：水波纹、细线分隔、几何标签、清爽圆点、锚点符号、气泡。
**背景质感**：浅灰蓝纸，细腻平滑，轻微水彩晕染底纹。
**氛围**：专业、从容、理性。

| 颜色 | 色值 | 用途 |
|------|------|------|
| 蔚蓝 | #0984E3 | 标题、标签、主色 |
| 深蓝 | #0652DD | 副标题、图标、边框 |
| 天蓝 | #74B9FF | 重点、装饰、箭头 |
| 浅灰蓝 | #DFE6E9 | 背景纸张 |
| 白色 | #FFFFFF | 内容卡片 |
| 深灰 | #2D3436 | 正文文字 |

### 手写体规范

字体随风格切换，颜色随风格主色。各风格字体定义见「风格体系」中"字体"行。

| 元素 | 描述 |
|------|------|
| **主标题** | 风格对应字体，风格主色，字号大，最醒目 |
| **副标题** | 风格对应字体，风格副色，字号中等 |
| **正文** | 风格对应字体，深灰色，**字号偏小** |
| **重点** | 风格对应字体加粗，风格强调色，加粗下划线，字号同正文 |
| **便利贴** | 风格对应字体，便利贴色上手写，字号小 |
| **标签** | 风格对应字体，标签色上白色手写，字号小 |
| **选项** | 风格对应字体，A/B/C/D选项，**字号偏小** |

### 内容模块

| 模块 | 用途 | 样式 |
|------|------|------|
| **标题区** | 主题名称 | 瘦金体 + 主题色下划线 |
| **分区卡片** | 知识点讲解 | 白色/浅色卡片 + 主题色编号标签 |
| **高频易错点** | 常见错误 | 手绘灯泡涂鸦 + 橙色手绘虚线框 |
| **一句话记忆** | 核心口诀 | 手绘靶心涂鸦 + 绿色手绘边框 |
| **学习计划** | 任务清单 | 手绘螺旋笔记本 + 手绘复选框 |
| **练习题页** | 配套练习 | 双栏布局 + 绿色手绘编号圆圈 + 提示框 |
| **答案解析页** | 答案与解析 | 双栏布局 + 绿色对勾 + 简要解析 |
| **装饰元素** | 氛围营造 | 手绘星星、纸夹、便利贴、涂鸦箭头 |
| **风格** | 视觉风格 | 经典/科幻/活力手账/青绿新生/蔚蓝格调 |

---

## 布局规范

### 整体布局原则

| 元素 | 规范 |
|------|------|
| **页边距** | 上下左右留白均匀，内容不贴边 |
| **对齐** | 左对齐为主，标题居中 |
| **间距** | 题目间等距，选项间等距 |
| **分栏** | 练习题页严格双栏，左右等宽 |

### 封面页布局

```
┌─────────────────────────────────┐
│ [蓝色标签]              [便利贴] │
│                                 │
│         [主标题]                │
│      [黄色下划线]               │
│        [副标题]                 │
│                                 │
│    [每日知识卡 + 配套练习]      │
│                                 │
│  [学习计划] [知识图] [书本]     │
└─────────────────────────────────┘
```

### 知识页布局

```
┌─────────────────────────────────┐
│ [蓝色标签]              [便利贴] │
│                                 │
│      Day XX | [主题]            │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 一、[小节名]                │ │
│ │ • 要点1                     │ │
│ │ • 要点2                     │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 二、[小节名]                │ │
│ │ • 要点1                     │ │
│ │ • 要点2                     │ │
│ └─────────────────────────────┘ │
│                                 │
│ [高频易错点]    [一句话记忆]    │
└─────────────────────────────────┘
```

### 练习题页布局（双栏）

```
┌─────────────────────────────────┐
│ [蓝色标签]              [便利贴] │
│                                 │
│      Day XX | 配套练习          │
│      [黄色下划线]               │
│                                 │
│ 💡 建议先独立完成，再看答案解析。│
│                                 │
│      [主题] (N题)               │
│                                 │
│ ┌──────────────┬──────────────┐ │
│ │ ① 题目      │ ⑥ 题目      │ │
│ │ A. B. C. D. │ A. B. C. D. │ │
│ │              │              │ │
│ │ ② 题目      │ ⑦ 题目      │ │
│ │ A. B. C. D. │ A. B. C. D. │ │
│ │              │              │ │
│ │ ③ 题目      │ ⑧ 题目      │ │
│ │ A. B. C. D. │ A. B. C. D. │ │
│ │              │              │ │
│ │ ④ 题目      │ ⑨ 题目      │ │
│ │ A. B. C. D. │ A. B. C. D. │ │
│ │              │              │ │
│ │ ⑤ 题目      │ ⑩ 题目      │ │
│ │ A. B. C. D. │ A. B. C. D. │ │
│ └──────────────┴──────────────┘ │
│                                 │
│ ⭐ 做完后再看下一张解析图。 →   │
└─────────────────────────────────┘
```

### 练习题排版细节

| 元素 | 规范 |
|------|------|
| **题目编号** | 绿色手绘实心圆圈，白色数字，居中，中等字号 |
| **题目文字** | 铅笔手写，紧跟编号后，**中等字号** |
| **选项排列** | 每行2个选项，A和B一行，C和D一行 |
| **选项对齐** | 左对齐，选项间留足间距，**小字号** |
| **题目间距** | 题目间等距，约1.5倍行高 |
| **栏间距** | 左右栏之间留明显分隔 |

### 字号规范

| 元素 | 字号 | 说明 |
|------|------|------|
| **主标题** | 大 | 页面焦点，最醒目 |
| **副标题** | 中 | 补充说明 |
| **分区标题** | 中 | 内容分隔 |
| **题目文字** | 中 | 需清晰可读 |
| **正文/选项** | 小 | 次要信息，不喧宾夺主 |
| **装饰文字** | 小 | 便利贴、标签等 |

---

## 执行流程

### 步骤1：理解需求

确认以下信息（如用户已提供则跳过）：
- 封面页标题？（如："STL容器：C++的工具箱"，必填）
- 封面副标题？（如："CSP-J初赛必会知识点"，可选）
- 知识点主题？（如：栈和队列、二叉树遍历、排序算法，用于知识页标题）
- 用途？（知识卡片 / 打卡海报 / 讲解配图）
- 页数？（单页 / 多页系列）
- 风格主题？（经典 / 科幻 / 活力手账 / 青绿新生 / 蔚蓝格调）
- 特殊要求？（需包含代码？需对比？需图解？）

**标题为必填项**，其余可省略由AI自动补全。用户未提供标题时，须主动询问不可跳过。

### 步骤2：内容规划

根据主题规划内容结构：

```
封面页（可选）
├── 标题
├── 副标题/主题词
└── 装饰元素

知识页
├── 分区标题（一、二、三...）
├── 各分区内容（卡片式）
├── 高频易错点
└── 一句话记忆

练习页（可选）
├── 题目列表
└── 解答区
```

### 步骤3：填充维度

按以下维度生成Prompt（优雅简洁风格）：

#### 封面页维度

| 维度 | 内容 |
|------|------|
| **layout** | 居中构图，留白充足，简洁优雅 |
| **title** | 深蓝马克笔手写，居中，黄色细下划线 |
| **subtitle** | 绿色马克笔手写，居中 |
| **decorations** | 蓝色标签（左上），黄色便利贴（右上），角落小星星 |
| **background** | 米色纸张纹理，轻微阴影 |

#### 知识页维度

| 维度 | 内容 |
|------|------|
| **section_header** | 橙色马克笔手写标签，**中等字号** |
| **content_card** | 白色卡片，轻微阴影，无重边框 |
| **icon_style** | 手绘简笔画，深蓝/绿色 |
| **text_hierarchy** | 标题大 → 正文小 → 重点小，层级清晰 |
| **body_text** | 铅笔手写，**字号偏小**，细线 |
| **special_sections** | 高频易错点 + 一句话记忆，底部并列，**小字号** |

#### 练习题页维度

| 维度 | 内容 |
|------|------|
| **layout** | 双栏等宽，网格对齐 |
| **question** | 绿色手绘编号圆圈 + 题目文字，**中等字号** |
| **options** | 2×2网格排列（A B / C D），对齐精确，**小字号** |
| **spacing** | 题目间等距，选项间等距 |
| **footer** | 提示语居中，绿色箭头，**小字号** |

### 步骤4：输出

---

## [方案名称] Prompt（[主题]主题）

### 封面页

```
[style]: elegant [风格字体] calligraphy notebook, torn paper edge, hole punches, minimal decoration
[style_theme]: [选择风格]
[background]: [主题背景色] paper texture, subtle shadow
[title]: "[主标题]" in [主题标题色] [风格字体], centered, thin yellow underline
[subtitle]: "[副标题]" in [主题副标题色] [风格字体], centered
[layout]: centered composition, generous whitespace, clean and refined
[decorations]: blue tag top-left, yellow sticky note top-right, small stars in corners only
[icons]: minimal hand-drawn preview icons at bottom
[aspect_ratio]: 3:4
```

### 知识页

```
[style]: elegant [风格字体] calligraphy notebook, consistent with cover, minimal decoration
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: blue tag left, yellow sticky note right
[title]: "Day XX | [主题]" in [主题标题色] [风格字体], centered
[sections]:
  - orange header "一、[小节名]" in [风格字体] + white card with subtle shadow + blue icon + [风格字体] bullet points
  - repeat structure
[special_sections]: 高频易错点 (lightbulb, orange) + 一句话记忆 (target, green), side by side at bottom
[decorations]: minimal, only small stars in corners
[aspect_ratio]: 3:4
```

### 练习题页

```
[style]: elegant [风格字体] calligraphy notebook, clean layout like exam paper
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: blue tag left, yellow sticky note right
[title]: "Day XX | 配套练习" in [主题标题色] [风格字体], centered
[tip]: small lightbulb + "建议先独立完成，再看答案解析。" in orange, centered
[topic]: "[主题] (N题)" in navy blue, centered
[layout]: TWO COLUMNS, equal width
  left: ①-⑤ questions
  right: ⑥-⑩ questions
  each question: number + text + 2x2 option grid (A B / C D) in [风格字体]
[footer]: "做完后再看下一张解析图。" with green arrow, centered
[decorations]: minimal, only corner stars
[aspect_ratio]: 3:4
```

### 答案解析页

```
[style]: elegant [风格字体] calligraphy notebook, clean and refined
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: blue tag left, yellow sticky note right
[title]: "Day XX | 答案解析" in [主题标题色] [风格字体], centered
[layout]: TWO COLUMNS, equal width
  left: answers 1-5
  right: answers 6-10
  each answer: green checkmark + number + letter + explanation in [风格字体]
[footer]: "易错题回顾" section in orange box
[decorations]: minimal, only corner stars
[aspect_ratio]: 3:4
```

---

## Prompt模板（可直接复制）

以下模板以**经典风格（瘦金体）**示范。使用时将 **[风格字体]** 替换为所选风格的对应字体，将 **[用户标题]** / **[用户副标题]** 替换为步骤1中用户提供的内容。

### 封面页模板

```
Clean, elegant cover page in notebook scrapbook style. Cream paper with torn left edge and hole punches. Spiral binding at bottom. ALL TEXT IN [风格字体] STYLE. Minimalist and refined.

Top: blue tag "[打卡标签]" on left, yellow sticky note "[便利贴文字]" on right.
Title "[用户标题]" in bold navy blue [风格字体], centered, with thin yellow underline.
Subtitle "[用户副标题]" in green [风格字体], centered.

Center: "每日知识卡 + 配套练习" in blue rounded box with calendar icon.

Bottom: Three mini preview icons related to the topic. Small decorative stars in corners.

ELEGANT RULES:
- Generous whitespace, centered composition
- Minimal decoration, only essential accents
- Typography hierarchy: title > subtitle > info
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, refined simplicity. Aspect ratio 3:4.
```

### 知识页模板

```
Clean, elegant knowledge page in notebook scrapbook style. Cream paper with torn left edge and hole punches. ALL TEXT IN [风格字体] STYLE. Minimalist with generous whitespace.

Top: blue tag on left, yellow sticky note "Day XX 第X页" on right.
Title "Day XX | [用户标题]" in bold green [风格字体], centered, LARGE FONT.

Section 1: Orange header "一、[小节名]" in [风格字体], MEDIUM FONT. White card below with subtle shadow. Blue hand-drawn icon. Bullet points in [风格字体] with SMALL FONT, key terms underlined in orange.

Section 2: Same structure, green header.

[Repeat for more sections]

Bottom: Two boxes side by side:
  Left: "高频易错点" with lightbulb icon, orange border, SMALL FONT
  Right: "一句话记忆" with target icon, green border, SMALL FONT

FONT SIZE HIERARCHY:
- Title: LARGE (main focus)
- Section headers: MEDIUM
- Body text, bullets, options: SMALL (secondary)
- Decorative text: SMALL

ELEGANT RULES:
- Clean vertical rhythm, consistent spacing
- Minimal decoration, only essential elements
- Cards have subtle shadows, not heavy borders
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, clean and refined. Aspect ratio 3:4.
```

### 练习题页模板

```
Clean, elegant practice page in notebook scrapbook style. Cream paper with torn left edge and hole punches. ALL TEXT IN [风格字体] STYLE. Minimalist layout with generous whitespace.

Top: blue tag "[用户标题]" on left, yellow sticky note "Day XX 第X页" on right.
Title "Day XX | 配套练习" in bold green [风格字体], centered, LARGE FONT, with thin yellow underline.

Small tip box: lightbulb icon + "建议先独立完成，再看答案解析。" in orange, centered, minimal border, SMALL FONT.

Topic "[用户标题] (N题)" in navy blue, centered, MEDIUM FONT.

TWO COLUMNS, equal width, clean vertical separation:

Left column:
  ① Question text (MEDIUM FONT)
     A. option    B. option
     C. option    D. option
     (options in SMALL FONT)

  ② Question text (MEDIUM FONT)
     A. option    B. option
     C. option    D. option
     (options in SMALL FONT)

  [Continue for 5 questions]

Right column:
  ⑥ Question text (MEDIUM FONT)
     A. option    B. option
     C. option    D. option
     (options in SMALL FONT)

  [Continue for 5 questions]

Bottom: "做完后再看下一张解析图。" with small green arrow, centered, SMALL FONT.

FONT SIZE HIERARCHY:
- Title: LARGE
- Question numbers and text: MEDIUM
- Options, tip, footer: SMALL

ELEGANT RULES:
- Generous whitespace between elements
- Precise alignment, clean grid
- Minimal decoration (only small stars in corners)
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, refined simplicity. Aspect ratio 3:4.
```

### 答案解析页模板

```
Clean, elegant answer page in notebook scrapbook style. Cream paper with torn left edge and hole punches. ALL TEXT IN [风格字体] STYLE. Minimalist with generous whitespace.

Top: blue tag "[用户标题]" on left, yellow sticky note "Day XX 第X页" on right.
Title "Day XX | 答案解析" in bold green [风格字体], centered, LARGE FONT, with thin yellow underline.

TWO COLUMNS, equal width, clean vertical separation:

Left column (Questions 1-5):
  Each answer block:
  - Green checkmark ✓ + "① 答案字母" in MEDIUM FONT
  - "解析：[简要解释]" in SMALL FONT, [风格字体]
  - Thin horizontal line separator

  Example:
  ✓ ① C
  解析：[简要解释]
  ─────────────────────────────────

Right column (Questions 6-10):
  Same structure, numbers continue

Bottom: "易错题回顾" section in orange box with lightbulb icon, listing commonly mistaken questions and key points.

FONT SIZE HIERARCHY:
- Title: LARGE
- Answer letters: MEDIUM
- Explanations: SMALL
- Footer notes: SMALL

ELEGANT RULES:
- Each answer clearly marked with green checkmark
- Explanations concise but complete
- Thin separators between answers
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, clean and refined. Aspect ratio 3:4.
```

---

## 风格速查

| 风格 | 视觉特征 | 字体 | 氛围 | 主色 |
|------|---------|------|------|------|
| 经典 | 复古温暖学院风，传统手账质感 | 瘦金体（瘦劲典雅） | 温馨、专注 | 深蓝+橙+绿 |
| 科幻 | 洁净未来科技感，极简冷冽 | 硬朗黑体（等宽平直） | 冷静、精准 | 冰蓝+银灰+电光紫 |
| 活力手账 | 热情元气，笔触活泼 | 可爱圆体（圆润饱满） | 活力、积极 | 活力橙+珊瑚红+薄荷绿 |
| 青绿新生 | 自然清新，东方素雅 | 行楷（流畅温润） | 清透、安宁 | 青绿+深青+浅绿 |
| 蔚蓝格调 | 海洋灵感，专业冷静 | 清秀宋体（端正典雅） | 专业、从容 | 蔚蓝+深蓝+天蓝 |

---

## Principles

| 原则 | 说明 |
|------|------|
| 优雅简洁 | 留白充足，元素克制，不杂乱 |
| 风格一致 | 同系列图保持配色、布局、装饰元素统一 |
| 清晰优先 | 信息层级分明，标题→正文→重点一目了然 |
| 对齐精确 | 双栏等宽，选项网格对齐，间距均匀 |
| 适龄匹配 | 面向12岁学生，活泼但不幼稚，专业但不枯燥 |
| 中文优先 | 所有文字内容默认中文 |

## AVOID

- 避免装饰过多导致杂乱
- 避免元素拥挤，留白不足
- 避免对齐不精确，间距不均
- 避免风格突变（同系列保持一致）
- 避免使用"我有个朋友"、"众所周知"等AI痕迹表达

---

**更新日期**: 2026-07-24

**变更记录**：
- 2026-07-24: v1.5.1 封面标题改为用户输入而非写死，步骤1新增封面标题/副标题为必填询问项，模板中死字标题全部替换为[用户标题]占位符
- 2026-07-24: v1.5.0 配色主题全面升级为风格体系：赛博朋克→科幻风格（配色与视觉元素重设），各风格新增视觉特征/字体/装饰元素/背景质感/氛围描述。字体不再固定瘦金体，各风格配独立字体（经典瘦金体/科幻硬朗黑体/活力圆体/青绿行楷/蔚蓝宋体）。配色速查表改为风格速查表含字体列，全篇引用更新。
- 2026-07-23: v1.4.0 新增四套风格：赛博朋克、活力手账、青绿新生、蔚蓝格调
- 2026-07-23: v1.3.0 优化字号层级，正文字体偏小，标题突出
- 2026-07-23: v1.2.0 风格升级为优雅简洁，强化留白、对齐、克制装饰
- 2026-07-23: v1.1.0 全面升级为手写体风格，所有文字和装饰元素均为手绘质感
- 2026-07-23: v1.0 初始版本，基于CSP-J初赛60天打卡系列视觉风格
