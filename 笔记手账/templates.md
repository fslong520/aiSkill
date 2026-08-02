# 笔记手账 - 布局规范与Prompt模板（templates.md）

> 本文件为 SKILL.md 之附属，定义页面布局规范与 Prompt 输出框架。生成 Prompt 前按页面类型（封面/知识/练习/答案解析）取用对应布局与模板。色值按所选风格取自 styles.md。

## 布局规范

### 整体布局原则

| 元素       | 规范                         |
| ---------- | ---------------------------- |
| **页边距** | 上下左右留白均匀，内容不贴边 |
| **对齐**   | 左对齐为主，标题居中         |
| **间距**   | 题目间等距，选项间等距       |
| **分栏**   | 练习题页严格双栏，左右等宽   |

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

| 元素         | 规范                                       |
| ------------ | ------------------------------------------ |
| **题目编号** | 墨蓝手绘实心圆圈，白色数字，居中，中等字号 |
| **题目文字** | 铅笔手写，紧跟编号后，**中等字号**         |
| **选项排列** | 每行2个选项，A和B一行，C和D一行            |
| **选项对齐** | 左对齐，选项间留足间距，**小字号**         |
| **题目间距** | 题目间等距，约1.5倍行高                    |
| **栏间距**   | 左右栏之间留明显分隔                       |

### 字号规范

| 元素          | 字号 | 说明                 |
| ------------- | ---- | -------------------- |
| **主标题**    | 大   | 页面焦点，最醒目     |
| **副标题**    | 中   | 补充说明             |
| **分区标题**  | 中   | 内容分隔             |
| **题目文字**  | 中   | 需清晰可读           |
| **正文/选项** | 小   | 次要信息，不喧宾夺主 |
| **装饰文字**  | 小   | 便利贴、标签等       |

---

## 输出框架

按页面类型输出以下框架（色值按所选风格替换）：

### 封面页

```
[style]: elegant [风格字体] calligraphy notebook, torn paper edge, hole punches, minimal decoration
[style_theme]: [选择风格]
[background]: [主题背景色] paper texture, subtle shadow
[title]: "[主标题]" in BOLD [主题标题色] [风格字体], centered, thin 柠檬黄 underline
[subtitle]: "[副标题]" in [主题副标题色] [风格字体], centered
[layout]: centered composition, generous whitespace, clean and refined, perfectly aligned
[decorations]: 墨蓝 tag top-left, 柠檬黄 sticky note top-right, small 暖金/柠檬黄 stars in corners, 暖金 page-footer icon
[icons]: minimal hand-drawn preview icons at bottom
[aspect_ratio]: 3:4
```

### 知识页

```
[style]: elegant [风格字体] calligraphy notebook, consistent with cover, minimal decoration
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: 墨蓝 tag left, 柠檬黄 sticky note right
[title]: "Day XX | [主题]" in BOLD [主题标题色] [风格字体], centered
[sections]:
  - 墨蓝 header "一、[小节名]" in [风格字体] + white card with subtle shadow, 双色条 (黛蓝 main + 暖金 thin) + 黛蓝 icon + [风格字体] bullet points
  - repeat structure
[special_sections]: 高频易错点 (lightbulb, 暖金) + 一句话记忆 (target, 青碧), side by side at bottom
[decorations]: small 暖金/柠檬黄 stars in corners, thin 暖金 separators between sections, 暖金 page-footer icon
[aspect_ratio]: 3:4
```

### 练习题页

```
[style]: elegant [风格字体] calligraphy notebook, clean layout like exam paper
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: 墨蓝 tag left, 柠檬黄 sticky note right
[title]: "Day XX | 配套练习" in [主题标题色] [风格字体], centered
[tip]: small lightbulb + "建议先独立完成，再看答案解析。" in 暖金, centered
[topic]: "[主题] (N题)" in 墨蓝, centered
[layout]: TWO COLUMNS, equal width
  left: ①-⑤ questions
  right: ⑥-⑩ questions
  each question: number + text + 2x2 option grid (A B / C D) in [风格字体]
[footer]: "做完后再看下一张解析图。" with 青碧 arrow, centered
[decorations]: small 暖金/柠檬黄 stars in corners, 暖金 page-footer icon
[aspect_ratio]: 3:4
```

### 答案解析页

```
[style]: elegant [风格字体] calligraphy notebook, clean and refined
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: 墨蓝 tag left, 柠檬黄 sticky note right
[title]: "Day XX | 答案解析" in [主题标题色] [风格字体], centered
[layout]: TWO COLUMNS, equal width
  left: answers 1-5
  right: answers 6-10
  each answer: 青碧 checkmark + number + letter + explanation in [风格字体]
[footer]: "易错题回顾" section in 暖金 box
[decorations]: small 暖金/柠檬黄 stars in corners, thin 暖金 separators between answers, 暖金 page-footer icon
[aspect_ratio]: 3:4
```

---

## Prompt模板（可直接复制）

以下模板以**墨蓝手账风格（默认）**示范。使用时将 **[风格字体]** 替换为所选风格的对应字体风格描述（见 styles.md），将 **[用户标题]** / **[用户副标题]** 替换为步骤1中用户提供的内容。

### 封面页模板

```
Clean, elegant cover page in notebook scrapbook style. Warm cream paper (#FFF9E6) with torn left edge and hole punches. Spiral binding at bottom. ALL TEXT IN BOLD THICK [风格字体] STYLE. Neat, orderly, graceful.

Top: 墨蓝 tag "[打卡标签]" straight on left, 柠檬黄 sticky note "[便利贴文字]" straight on right.
Title "[用户标题]" in EXTRA BOLD 墨蓝 [风格字体], centered, with straight 柠檬黄 underline and simple 雾蓝(#A9BFD9) highlight block.
Subtitle "[用户副标题]" in BOLD 黛蓝(#3E5C76) [风格字体], centered.

Center: "每日知识卡 + 配套练习" in 青碧(#00CEC9) rounded box with calendar icon, perfectly centered, 暖金(#E8A33D) border.

Bottom: Three mini preview icons related to the topic, evenly spaced. A few small warm-gold/lemon stars in the corners. Warm-gold small icon (pencil) at bottom-right.

ELEGANT RULES:
- Perfectly aligned, straight elements, no tilting
- Refined decoration (tags, sticky notes, stars, warm-gold page-footer icon), generous whitespace
- Palette: 墨蓝 #26355D main, 黛蓝 #3E5C76 and 雾蓝 #A9BFD9 cool accents, 青碧 #00CEC9 detail, 柠檬黄 #FFC312 and 暖金 #E8A33D warm accents, warm cream background
- Typography hierarchy: title > subtitle > info
- [风格字体]: font style matching the chosen theme (AI selects best available system font)

Style: elegant [风格字体] notebook, ink-blue and graceful. Aspect ratio 3:4.
```

### 知识页模板

```
Clean, elegant knowledge page in notebook scrapbook style. Warm cream paper (#FFF9E6) with torn left edge and hole punches. ALL TEXT IN BOLD THICK [风格字体] STYLE. Neat, orderly, generous whitespace.

Top: 墨蓝 tag straight on left, 柠檬黄 sticky note "Day XX 第X页" straight on right.
Title "Day XX | [用户标题]" in EXTRA BOLD 墨蓝 [风格字体], centered, LARGE FONT, with straight 柠檬黄 underline.

Section 1: 墨蓝 header "一、[小节名]" in BOLD [风格字体], MEDIUM FONT, straight. White card below with subtle shadow and 双色条 (黛蓝(#3E5C76) main bar + thin 暖金(#E8A33D) accent line). 黛蓝 hand-drawn icon. Bullet points in BOLD [风格字体] with SMALL FONT, key terms in 柠檬黄 with fluorescent highlighter stroke.

Section 2: Same structure, 雾蓝(#A9BFD9) main bar + thin 暖金 accent line.

[Repeat for more sections, thin 暖金 separator lines between sections]

Bottom: Two boxes side by side, same height, aligned:
  Left: "高频易错点" with lightbulb icon, 暖金(#E8A33D) border, SMALL FONT, 柠檬黄 highlighter on key words
  Right: "一句话记忆" with target icon, 青碧(#00CEC9) border, SMALL FONT, 柠檬黄 highlight background

Page footer: small 暖金 book icon at bottom-right corner.

FONT SIZE HIERARCHY:
- Title: LARGE (main focus)
- Section headers: MEDIUM
- Body text, bullets, options: SMALL (secondary)
- Decorative text: SMALL

ELEGANT RULES:
- Perfectly aligned, straight headers and cards, no tilting
- Refined decoration (tags, sticky notes, stars, 暖金 separators, page-footer icon), generous whitespace
- Palette: 墨蓝 #26355D headers, 黛蓝 #3E5C76 and 雾蓝 #A9BFD9 card bars, 青碧 #00CEC9 detail, 柠檬黄 #FFC312 and 暖金 #E8A33D warm accents, warm cream background
- Cards have subtle shadows and 双色条 top bars (main color + thin 暖金 line), not heavy borders
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, ink-blue and graceful. Aspect ratio 3:4.
```

### 练习题页模板

```
Clean, elegant practice page in notebook scrapbook style. Warm cream paper (#FFF9E6) with torn left edge and hole punches. ALL TEXT IN BOLD THICK [风格字体] STYLE. Neat exam-paper layout, precise grid.

Top: 墨蓝 tag "[用户标题]" straight on left, 柠檬黄 sticky note "Day XX 第X页" straight on right.
Title "Day XX | 配套练习" in EXTRA BOLD 墨蓝 [风格字体], centered, LARGE FONT, with thin 柠檬黄 underline.

Small tip box: lightbulb icon + "建议先独立完成，再看答案解析。" in 暖金(#E8A33D), centered, minimal border, SMALL FONT.

Topic "[用户标题] (N题)" in 墨蓝, centered, MEDIUM FONT.

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

Bottom: "做完后再看下一张解析图。" with small 青碧(#00CEC9) arrow, centered, SMALL FONT. Warm-gold small icon (pencil) at bottom-right.

FONT SIZE HIERARCHY:
- Title: LARGE
- Question numbers and text: MEDIUM
- Options, tip, footer: SMALL

ELEGANT RULES:
- Precise alignment, clean grid, equal spacing
- Refined decoration: corner stars, warm-gold page-footer icon, thin 暖金 separator between topic and questions; generous whitespace
- Palette: 墨蓝 #26355D question circles, 青碧 #00CEC9 arrow, 暖金 #E8A33D tip, warm cream background
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, ink-blue and graceful. Aspect ratio 3:4.
```

### 答案解析页模板

```
Clean, elegant answer page in notebook scrapbook style. Warm cream paper (#FFF9E6) with torn left edge and hole punches. ALL TEXT IN BOLD THICK [风格字体] STYLE. Neat, refined, precise grid.

Top: 墨蓝 tag "[用户标题]" straight on left, 柠檬黄 sticky note "Day XX 第X页" straight on right.
Title "Day XX | 答案解析" in EXTRA BOLD 墨蓝 [风格字体], centered, LARGE FONT, with thin 柠檬黄 underline.

TWO COLUMNS, equal width, clean vertical separation:

Left column (Questions 1-5):
  Each answer block:
  - 青碧(#00CEC9) checkmark ✓ + "① 答案字母" in MEDIUM FONT (letter in 墨蓝 bold)
  - "解析：[简要解释]" in SMALL FONT, [风格字体]
  - Thin horizontal line separator

  Example:
  ✓ ① C
  解析：[简要解释]
  ─────────────────────────────────

Right column (Questions 6-10):
  Same structure, numbers continue

Bottom: "易错题回顾" section in 暖金(#E8A33D) box with lightbulb icon, listing commonly mistaken questions and key points. Warm-gold small icon (book) at bottom-right.

FONT SIZE HIERARCHY:
- Title: LARGE
- Answer letters: MEDIUM
- Explanations: SMALL
- Footer notes: SMALL

ELEGANT RULES:
- Each answer clearly marked with 青碧 checkmark
- Explanations concise but complete
- Thin 暖金 separators between answers
- Refined decoration: corner stars, warm-gold page-footer icon; generous whitespace
- Palette: 墨蓝 #26355D answer letters, 青碧 #00CEC9 checkmarks, 暖金 #E8A33D box, warm cream background
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, ink-blue and graceful. Aspect ratio 3:4.
```

---

**文档版本**: 3.2
**最后更新**: 2026-08-02
