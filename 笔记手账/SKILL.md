---
name: 笔记手账
version: 1.9.5
description: 笔记手账风格教育知识卡片Prompt生成器。输入知识点，输出优雅简洁的手写体结构化Prompt，支持8套风格主题（含二次元/动漫风格、少女粉风格、我的世界像素风等）。字体自动匹配系统可用字体。
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  slug: note-journal
  trigger: 笔记手账、知识卡片、打卡海报、教学插图、CSP-J风格、瘦金体、科幻风格、活力手账、青绿新生、蔚蓝格调、二次元风格、动漫风格、JK制服、洛丽塔、女仆装、魔法少女、萌系、少女粉、粉色系、少女风格、像素风、我的世界、Minecraft、像素
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
| **基底** | 米白/宣纸色纸张底纹，轻微纤维纹理，撕纸毛边，活页孔，螺旋装订 |
| **风格** | 经典风格（默认）：复古学院风，温润雅致，墨朱赭绿和谐共处。另有科幻/活力手账/青绿新生/蔚蓝格调/二次元/动漫/少女粉/我的世界像素风 |
| **字体** | 各风格字体方向见「风格体系」，AI自动匹配系统可用字体。**一律加粗渲染（BOLD），笔画饱满丰腴、优雅流畅，禁用细瘦字重** |
| **装饰** | 手绘箭头↗、涂鸦圈、微倾斜便利贴、波浪高亮划痕、错落小星⋆、回形针、和纸胶带、朱红圆形编号、小叶片🍃——灵动摇曳，错落有致 |
| **布局** | 留白充裕，呼吸感强；标题/标签/便利贴微倾斜错落，动感而不乱；信息层级分明 |
| **质感** | 手绘感与精致感平衡，温润不粗糙，灵动不呆板 |

### 风格体系

每套风格不惟配色，更定义视觉语言全貌——装饰元素、背景质感、整体氛围各具面貌。

> **创作自由**：以下风格元素为方向指引，非铁律。AI 可根据主题灵活搭配、自由发挥，不必拘泥于列表中的具体装饰项。少即是多，留白也是美。

> **字体匹配**：各风格标注字体风格方向而非具体字体名。AI 根据目标系统可用字体自动选择最匹配者——如系统有楷体用楷体、无则用手写感黑体替代。宁可美观兼容，不苛求名称一致。

#### 经典风格（默认）

**视觉特征**：复古学院风，温润雅致而灵动醒目。取法传统文人笔墨与现代手账美学之交融——墨色为主，朱赭点睛，青绿为辅。标题大字带手绘色块，重点以荧光笔划痕高亮，装饰错落倾斜，张弛有度。
**字体**：**瘦金体风格（加粗渲染）**——笔画瘦劲锋利，锋芒劲挺，骨力洞达，瘦而不弱、劲而有韵。AI自动匹配系统瘦金体或近瘦金手写字体，**一律加粗渲染（BOLD），增其分量而不损其锋棱，忌过细无力、忌肥肿圆钝**。字号层级分明，标题大气，正文收敛。
**装饰元素**：手绘箭头↗、涂鸦圈⭕、微倾斜便利贴（旋转 2~5°）、波浪高亮划痕、错落小星⋆、回形针📎、和纸胶带、小叶片🍃、朱红圆形编号①。装饰灵动摇曳、错落有致，每页点缀三四处，醒目而不杂乱。
**背景质感**：宣纸米色底纹，极轻微纤维感，无重肌理。撕纸边缘自然柔和，活页孔细线框。留白开阔，不染杂色。
**氛围**：安静、专注、书卷气。不争不抢，内容为王。

| 颜色 | 色值 | 用途 |
|------|------|------|
| 墨黑 | #2D2D2D | 主标题、正文、主标签 |
| 朱红 | #C23B22 | 编号、重点标记、装饰点缀 |
| 赭黄 | #D4A34A | 下划线、便利贴、高亮标记 |
| 青绿 | #7BA892 | 副标题、对勾、箭头、记忆框 |
| 鸦青 | #4A5B7A | 二级标签、边框、辅助文字 |
| 宣纸米 | #F2EDE4 | 背景纸张 |
| 雪白 | #FAFAF8 | 内容卡片底色 |

#### 科幻风格

**视觉特征**：洁净未来科技感，极简冷冽，线条利落。
**字体**：**无衬线黑体风格**——笔画等宽平直，棱角分明，冷冽科技感。AI自动匹配系统黑体或近黑无衬线字体。
**装饰元素**：几何光点、细线框、全息标签、科技纹路、编码条纹、发光线框。
**背景质感**：深空色底或纯白底配微细网格，金属质感边角，荧光线分隔。
**氛围**：冷静、精准、未来感。

| 颜色   | 色值    | 用途               |
| ------ | ------- | ------------------ |
| 冰蓝   | #4FC3F7 | 标题、标签、主色   |
| 银灰   | #B0BEC5 | 副标题、图标、边框 |
| 电光紫 | #7C4DFF | 重点、编号、装饰   |
| 深空   | #0D1117 | 背景纸张           |
| 铁灰   | #161B22 | 卡片背景           |
| 冷白   | #E6EDF3 | 正文文字           |

#### 活力手账风格

**视觉特征**：热情元气，笔触活泼，色彩鲜明。
**字体**：**手写圆体风格**——圆润饱满，转角柔和，有手写温度。AI自动匹配系统圆体或近圆手写字体。
**装饰元素**：手绘涂鸦、波浪线、感叹号、贴纸感元素、圆点、彩色回形针、气泡框。
**背景质感**：奶油色暖调纸，轻微纹理，可见纤维感。
**氛围**：活力、积极、轻松。

| 颜色   | 色值    | 用途                 |
| ------ | ------- | -------------------- |
| 活力橙 | #FF6B35 | 标题、标签、主色     |
| 珊瑚红 | #FF4757 | 副标题、重点、装饰   |
| 薄荷绿 | #2ED573 | 箭头、记忆框、图标   |
| 柠檬黄 | #FFC312 | 下划线、便利贴、星星 |
| 奶油白 | #FFF9E6 | 背景纸张             |
| 浅灰   | #F5F5F5 | 内容卡片             |

#### 青绿新生风格

**视觉特征**：自然清新，东方素雅，宁静中生趣。
**字体**：**行楷风格**——行书之流畅兼楷书之法度，笔画连带自然，温润如玉。AI自动匹配系统行楷或连笔手写字体。
**装饰元素**：叶片纹路、水墨感点缀、细枝线条、露珠、留白晕染。
**背景质感**：米白纸，极轻水彩纹理，边缘自然渗化。
**氛围**：清透、成长、安宁。

| 颜色 | 色值    | 用途               |
| ---- | ------- | ------------------ |
| 青绿 | #00B894 | 标题、标签、主色   |
| 深青 | #006266 | 副标题、图标、边框 |
| 浅绿 | #55E6C1 | 重点、装饰、箭头   |
| 米白 | #F8F9FA | 背景纸张           |
| 浅灰 | #E9ECEF | 内容卡片           |
| 深灰 | #2D3436 | 正文文字           |

#### 蔚蓝格调风格

**视觉特征**：海洋灵感，专业冷静，干练整洁。
**字体**：**宋体风格**——横细竖粗，起落有装饰角，端正典雅，专业感强。AI自动匹配系统宋体或近宋衬线字体。
**装饰元素**：水波纹、细线分隔、几何标签、清爽圆点、锚点符号、气泡。
**背景质感**：浅灰蓝纸，细腻平滑，轻微水彩晕染底纹。
**氛围**：专业、从容、理性。

| 颜色   | 色值    | 用途               |
| ------ | ------- | ------------------ |
| 蔚蓝   | #0984E3 | 标题、标签、主色   |
| 深蓝   | #0652DD | 副标题、图标、边框 |
| 天蓝   | #74B9FF | 重点、装饰、箭头   |
| 浅灰蓝 | #DFE6E9 | 背景纸张           |
| 白色   | #FFFFFF | 内容卡片           |
| 深灰   | #2D3436 | 正文文字           |

#### 二次元/动漫风格

**视觉特征**：日系动漫美学，大眼萌系，梦幻粉嫩，漫画感十足，人物精致可爱。
**字体**：**手写圆体风格**——圆润饱满，转角柔和，有手写温度。AI自动匹配系统圆体或近圆手写字体。
**装饰元素**：
- **人物元素**：Q版萌系角色（大眼睛、尖下巴、夸张表情）、傲娇脸(‵ε′)、害羞脸(*/ω＼*)、星星眼✨、猫耳娘、兔耳娘、魔法少女
- **服装元素**：JK制服、水手服、洛丽塔裙、女仆装、和服、领结、蝴蝶结丝带、荷叶边、蕾丝花边
- **配饰元素**：猫耳🐱、兔耳🐰、发卡、发饰、丝带🎀、长筒袜、过膝袜、手套、珍珠项链、星星权杖⭐
- **道具元素**：魔法杖、变身器、魔法阵、应援棒、荧光棒、棒棒糖、气球
- **漫画特效**：闪亮✨、爱心❤、星星☆、光效、速度线、集中线、漫画对话框、拟声词（わぁ！、キラキラ）
- **场景元素**：樱花树🌸、教室、天台、海边、星空、彩虹🌈、云朵☁
- **边框装饰**：蕾丝边框、荷叶边框、丝带边框、蝴蝶结边框、珍珠边框

**背景质感**：渐变粉蓝或粉紫色梦幻背景，星光点点，樱花飘落效果，漫画分格效果，轻微光晕，渐变彩虹条。
**氛围**：可爱、梦幻、少女心、治愈、萌系、元气、甜美。

| 颜色     | 色值    | 用途                         |
| -------- | ------- | ---------------------------- |
| 樱花粉   | #FFB7C5 | 标题、重点、爱心装饰、腮红   |
| 天空蓝   | #87CEEB | 副标题、标签、边框、水手服   |
| 薰衣草紫 | #E6E6FA | 编号、装饰、星星、洛丽塔     |
| 薄荷绿   | #98FB98 | 箭头、记忆框、图标、清新元素 |
| 柠檬黄   | #FFFACD | 高频易错点、闪亮特效、星星眼 |
| 奶油白   | #FFFEF7 | 背景纸张、蕾丝、荷叶边       |
| 浅灰     | #F5F5F5 | 内容卡片、丝带               |
| 腮红粉   | #FF9999 | Q版角色腮红、害羞效果        |

#### 少女粉风格

**视觉特征**：纯粉甜美少女风，温柔治愈，干净粉嫩。
**字体**：**手写圆体风格**——圆润饱满，转角柔和，有手写温度。AI自动匹配系统圆体或近圆手写字体。
**人物元素参考**（AI自由发挥，可选配）：Q版小女生（双马尾/丸子头）、猫耳娘、兔耳娘、穿JK制服/水手服的小人、星星眼表情、害羞脸红、比心手势、抱玩偶的小女孩。
**装饰元素参考**（AI自由搭配，不必全用）：蝴蝶结🎀、爱心💕、星星☆、花朵🌸、蕾丝、丝带、圆点、珍珠、云朵☁、彩虹🌈等甜美元素。
**背景质感**：粉白渐变纸张，极淡珠光纹理，蕾丝花边边缘，轻微光泽。
**氛围**：甜美、温柔、少女心、治愈、干净。

| 颜色 | 色值 | 用途 |
|------|------|------|
| 樱花粉 | #FFB7C5 | 标题、标签、主色 |
| 玫瑰粉 | #FF6B8A | 重点、编号、装饰 |
| 奶油白 | #FFF5F5 | 背景纸张 |
| 薰衣草紫 | #E8D5F5 | 副标题、箭头、记忆框 |
| 珍珠白 | #FFFAFA | 内容卡片 |
| 浅灰粉 | #FCE4EC | 标签底色 |

#### 我的世界像素风

**视觉特征**：Minecraft 像素方块美学，低分辨率块状质感，粗犷复古，色彩饱和明快，棱角分明。
**字体**：**像素字体**——等宽方块字，锯齿边缘，每个字符在网格内以像素点阵呈现，无曲线无抗锯齿，硬朗复古游戏感。
**装饰元素**：草方块🌱、泥土块、钻石💎、铁剑🗡、苦力怕脸💥、TNT方块、工作台、末影珍珠、红石粉、小村民角色、血量条❤、经验条、背包格子、木牌告示牌。
**背景质感**：草绿色/泥土色像素化底纹，可见独立像素点（4×4或8×8像素块），天空蓝渐变色块天幕，云朵为锯齿方块堆叠。
**氛围**：沙盒冒险、自由创造、探索感、怀旧复古。

| 颜色       | 色值    | 用途                     |
| ---------- | ------- | ------------------------ |
| 草绿       | #5B8731 | 标题、标签、主色         |
| 钻石蓝     | #3DC7F0 | 编号、重点、高亮         |
| 泥土棕     | #8B6B4A | 副标题、箭头、卡片背景   |
| 炽焰橙     | #FF6B35 | 提醒框、警告、易错标记   |
| 金块黄     | #FFD700 | 下划线、便利贴、星星     |
| 天空蓝     | #87CEEB | 背景天幕                 |
| 像素白     | #F0F0F0 | 内容卡片、对话框         |
| 石质灰     | #808080 | 边框、砖石纹路           |

### 手写体规范

字体风格随风格切换，AI自动匹配系统可用字体。各风格字体方向见「风格体系」中"字体"行。

| 元素       | 描述                                                 |
| ---------- | ---------------------------------------------------- |
| **主标题** | 风格对应字体，风格主色，**加粗（BOLD）**，字号大，最醒目 |
| **副标题** | 风格对应字体，风格副色，**加粗（BOLD）**，字号中等 |
| **正文**   | 风格对应字体，深灰色，**加粗（BOLD）**，**字号偏小** |
| **重点**   | 风格对应字体加粗，风格强调色，加粗下划线，字号同正文 |
| **便利贴** | 风格对应字体，便利贴色上手写，**加粗（BOLD）**，字号小 |
| **标签**   | 风格对应字体，标签色上白色手写，**加粗（BOLD）**，字号小 |
| **选项**   | 风格对应字体，A/B/C/D选项，**加粗（BOLD）**，**字号偏小** |

### 内容模块

| 模块           | 用途       | 样式                                             |
| -------------- | ---------- | ------------------------------------------------ |
| **标题区**     | 主题名称   | 风格对应字体加粗 + 主题色手绘色块/波浪下划线，醒目吸睛 |
| **分区卡片**   | 知识点讲解 | 白色/浅色卡片 + 主题色顶部条/角标 + 错落编号标签 |
| **高频易错点** | 常见错误   | 手绘灯泡涂鸦 + 橙色手绘虚线框 + 荧光笔高亮重点 |
| **一句话记忆** | 核心口诀   | 手绘靶心涂鸦 + 绿色手绘边框 + 黄色高亮底色 |
| **学习计划**   | 任务清单   | 手绘螺旋笔记本 + 手绘复选框                      |
| **练习题页**   | 配套练习   | 双栏布局 + 绿色手绘编号圆圈 + 提示框             |
| **答案解析页** | 答案与解析 | 双栏布局 + 绿色对勾 + 简要解析                   |
| **装饰元素**   | 氛围营造   | 手绘星星、纸夹、便利贴、涂鸦箭头                 |
| **风格** | 视觉风格 | 经典/科幻/活力手账/青绿新生/蔚蓝格调/二次元/动漫/少女粉/我的世界像素风 |

---

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
| **题目编号** | 绿色手绘实心圆圈，白色数字，居中，中等字号 |
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

## 执行流程

### 步骤1：理解需求

确认以下信息（如用户已提供则跳过）：
- 封面页标题？（如："STL容器：C++的工具箱"，必填）
- 封面副标题？（如："CSP-J初赛必会知识点"，可选）
- 知识点主题？（如：栈和队列、二叉树遍历、排序算法，用于知识页标题）
- 用途？（知识卡片 / 打卡海报 / 讲解配图）
- 页数？（单页 / 多页系列）
- 风格主题？（经典 / 科幻 / 活力手账 / 青绿新生 / 蔚蓝格调 / 二次元/动漫 / 少女粉 / 我的世界像素风）
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

| 维度            | 内容                                             |
| --------------- | ------------------------------------------------ |
| **layout**      | 居中构图，留白充足，简洁优雅                     |
| **title**       | 墨黑马克笔手写，居中，赭黄细下划线               |
| **subtitle**    | 青绿马克笔手写，居中                             |
| **decorations** | 蓝色标签（左上），黄色便利贴（右上），角落小星星 |
| **background**  | 米色纸张纹理，轻微阴影                           |

#### 知识页维度

| 维度                 | 内容                                          |
| -------------------- | --------------------------------------------- |
| **section_header**   | 朱红马克笔手写标签 + 微倾斜，**中等字号**，加粗              |
| **content_card**     | 白色卡片，轻微阴影，顶部主题色细条/角标                  |
| **icon_style**       | 手绘简笔画，鸦青/青绿，灵动涂鸦感                         |
| **text_hierarchy**   | 标题大而醒目 → 正文小 → 重点荧光笔高亮，层级清晰            |
| **body_text**        | 手写钢笔体，**加粗（BOLD）**，**字号偏小**，粗线                  |
| **special_sections** | 高频易错点（朱红荧光笔高亮）+ 一句话记忆（赭黄高亮底），底部并列，**小字号** |

#### 练习题页维度

| 维度         | 内容                                           |
| ------------ | ---------------------------------------------- |
| **layout**   | 双栏等宽，网格对齐                             |
| **question** | 绿色手绘编号圆圈 + 题目文字，**中等字号**      |
| **options**  | 2×2网格排列（A B / C D），对齐精确，**小字号** |
| **spacing**  | 题目间等距，选项间等距                         |
| **footer**   | 提示语居中，绿色箭头，**小字号**               |

### 步骤4：输出

---

## [方案名称] Prompt（[主题]主题）

### 封面页

```
[style]: elegant [风格字体] calligraphy notebook, torn paper edge, hole punches, minimal decoration
[style_theme]: [选择风格]
[background]: [主题背景色] paper texture, subtle shadow
[title]: "[主标题]" in BOLD [主题标题色] [风格字体], centered, thin 赭黄 underline
[subtitle]: "[副标题]" in [主题副标题色] [风格字体], centered
[layout]: centered composition, generous whitespace, clean and refined
[decorations]: 鸦青 tag top-left, 赭黄 sticky note top-right, small stars in corners only
[icons]: minimal hand-drawn preview icons at bottom
[aspect_ratio]: 3:4
```

### 知识页

```
[style]: elegant [风格字体] calligraphy notebook, consistent with cover, minimal decoration
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: 鸦青 tag left, 赭黄 sticky note right
[title]: "Day XX | [主题]" in BOLD [主题标题色] [风格字体], centered
[sections]:
  - 朱红 header "一、[小节名]" in [风格字体] + white card with subtle shadow + 鸦青 icon + [风格字体] bullet points
  - repeat structure
[special_sections]: 高频易错点 (lightbulb, 朱红) + 一句话记忆 (target, 青绿), side by side at bottom
[decorations]: minimal, only small stars in corners
[aspect_ratio]: 3:4
```

### 练习题页

```
[style]: elegant [风格字体] calligraphy notebook, clean layout like exam paper
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: 鸦青 tag left, 赭黄 sticky note right
[title]: "Day XX | 配套练习" in [主题标题色] [风格字体], centered
[tip]: small lightbulb + "建议先独立完成，再看答案解析。" in 朱红, centered
[topic]: "[主题] (N题)" in 墨黑, centered
[layout]: TWO COLUMNS, equal width
  left: ①-⑤ questions
  right: ⑥-⑩ questions
  each question: number + text + 2x2 option grid (A B / C D) in [风格字体]
[footer]: "做完后再看下一张解析图。" with 青绿 arrow, centered
[decorations]: minimal, only corner stars
[aspect_ratio]: 3:4
```

### 答案解析页

```
[style]: elegant [风格字体] calligraphy notebook, clean and refined
[style_theme]: [选择风格]
[background]: [主题背景色] paper, torn left edge, hole punches
[header]: 鸦青 tag left, 赭黄 sticky note right
[title]: "Day XX | 答案解析" in [主题标题色] [风格字体], centered
[layout]: TWO COLUMNS, equal width
  left: answers 1-5
  right: answers 6-10
  each answer: 青绿 checkmark + number + letter + explanation in [风格字体]
[footer]: "易错题回顾" section in 朱红 box
[decorations]: minimal, only corner stars
[aspect_ratio]: 3:4
```

---

## Prompt模板（可直接复制）

以下模板以**经典风格**示范。使用时将 **[风格字体]** 替换为所选风格的对应字体风格描述，将 **[用户标题]** / **[用户副标题]** 替换为步骤1中用户提供的内容。

### 封面页模板

```
Clean, elegant cover page in notebook scrapbook style. Warm rice paper (#F2EDE4) with torn left edge and hole punches. Spiral binding at bottom. ALL TEXT IN BOLD THICK [风格字体] STYLE. Minimalist and refined.

Top: 鸦青 tag "[打卡标签]" tilted slightly on left, 赭黄 sticky note "[便利贴文字]" rotated on right.
Title "[用户标题]" in EXTRA BOLD 墨黑 [风格字体], centered, with hand-drawn 赭黄 wave underline and subtle 墨黑 highlight block.
Subtitle "[用户副标题]" in BOLD 青绿 [风格字体], centered.

Center: "每日知识卡 + 配套练习" in 鸦青 rounded box with calendar icon, slightly tilted.

Bottom: Three mini preview icons related to the topic. Hand-drawn arrows and scattered stars in corners, playful but refined.

ELEGANT RULES:
- Generous whitespace, lively composition with slight tilts
- Playful yet refined decoration, scattered accents
- Typography hierarchy: title > subtitle > info
- [风格字体]: font style matching the chosen theme (AI selects best available system font)

Style: elegant [风格字体] notebook, refined simplicity. Aspect ratio 3:4.
```

### 知识页模板

```
Clean, elegant knowledge page in notebook scrapbook style. Warm rice paper (#F2EDE4) with torn left edge and hole punches. ALL TEXT IN BOLD THICK [风格字体] STYLE. Minimalist with generous whitespace.

Top: 鸦青 tag tilted on left, 赭黄 sticky note "Day XX 第X页" rotated on right.
Title "Day XX | [用户标题]" in EXTRA BOLD 青绿 [风格字体], centered, LARGE FONT, with hand-drawn 赭黄 wave underline.

Section 1: 朱红 header "一、[小节名]" in BOLD [风格字体], MEDIUM FONT, slightly tilted. White card below with subtle shadow and 朱红 top color bar. 鸦青 hand-drawn icon. Bullet points in BOLD [风格字体] with SMALL FONT, key terms in 朱红 with fluorescent highlighter stroke.

Section 2: Same structure, 青绿 header.

[Repeat for more sections]

Bottom: Two boxes side by side:
  Left: "高频易错点" with lightbulb icon, 朱红 border, SMALL FONT, 朱红 highlighter on key words
  Right: "一句话记忆" with target icon, 青绿 border, SMALL FONT, 赭黄 highlight background

FONT SIZE HIERARCHY:
- Title: LARGE (main focus)
- Section headers: MEDIUM
- Body text, bullets, options: SMALL (secondary)
- Decorative text: SMALL

ELEGANT RULES:
- Clean vertical rhythm with playful tilts on tags and notes
- Playful yet refined decoration, scattered hand-drawn accents
- Cards have subtle shadows and colored top bars, not heavy borders
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, clean and refined. Aspect ratio 3:4.
```

### 练习题页模板

```
Clean, elegant practice page in notebook scrapbook style. Warm rice paper (#F2EDE4) with torn left edge and hole punches. ALL TEXT IN BOLD THICK [风格字体] STYLE. Minimalist layout with generous whitespace.

Top: 鸦青 tag "[用户标题]" on left, 赭黄 sticky note "Day XX 第X页" on right.
Title "Day XX | 配套练习" in EXTRA BOLD 青绿 [风格字体], centered, LARGE FONT, with thin 赭黄 underline.

Small tip box: lightbulb icon + "建议先独立完成，再看答案解析。" in 朱红, centered, minimal border, SMALL FONT.

Topic "[用户标题] (N题)" in 墨黑, centered, MEDIUM FONT.

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

Bottom: "做完后再看下一张解析图。" with small 青绿 arrow, centered, SMALL FONT.

FONT SIZE HIERARCHY:
- Title: LARGE
- Question numbers and text: MEDIUM
- Options, tip, footer: SMALL

ELEGANT RULES:
- Generous whitespace between elements, playful tilts on tags
- Precise alignment, clean grid
- Playful yet refined decoration, scattered hand-drawn accents
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, refined simplicity. Aspect ratio 3:4.
```

### 答案解析页模板

```
Clean, elegant answer page in notebook scrapbook style. Warm rice paper (#F2EDE4) with torn left edge and hole punches. ALL TEXT IN BOLD THICK [风格字体] STYLE. Minimalist with generous whitespace.

Top: 鸦青 tag "[用户标题]" on left, 赭黄 sticky note "Day XX 第X页" on right.
Title "Day XX | 答案解析" in EXTRA BOLD 青绿 [风格字体], centered, LARGE FONT, with thin 赭黄 underline.

TWO COLUMNS, equal width, clean vertical separation:

Left column (Questions 1-5):
  Each answer block:
  - 青绿 checkmark ✓ + "① 答案字母" in MEDIUM FONT
  - "解析：[简要解释]" in SMALL FONT, [风格字体]
  - Thin horizontal line separator

  Example:
  ✓ ① C
  解析：[简要解释]
  ─────────────────────────────────

Right column (Questions 6-10):
  Same structure, numbers continue

Bottom: "易错题回顾" section in 朱红 box with lightbulb icon, listing commonly mistaken questions and key points.

FONT SIZE HIERARCHY:
- Title: LARGE
- Answer letters: MEDIUM
- Explanations: SMALL
- Footer notes: SMALL

ELEGANT RULES:
- Each answer clearly marked with 青绿 checkmark
- Explanations concise but complete
- Thin separators between answers
- Playful yet refined decoration, scattered accents
- [风格字体]: font matching the chosen style's character

Style: elegant [风格字体] notebook, clean and refined. Aspect ratio 3:4.
```

---

## 风格速查

| 风格        | 视觉特征                                         | 字体                 | 氛围                     | 主色                   |
| ----------- | ------------------------------------------------ | -------------------- | ------------------------ | ---------------------- |
| 经典        | 复古学院风，温润雅致而灵动醒目                 | 瘦金体（加粗，瘦劲锋棱） | 安静、灵动、醒目         | 墨黑+朱红+赭黄+青绿     |
| 科幻        | 洁净未来科技感，极简冷冽                         | 无衬线黑体风格（硬朗科技感） | 冷静、精准               | 冰蓝+银灰+电光紫       |
| 活力手账    | 热情元气，笔触活泼                               | 手写圆体风格（圆润饱满） | 活力、积极               | 活力橙+珊瑚红+薄荷绿   |
| 青绿新生    | 自然清新，东方素雅                               | 行楷风格（流畅温润）     | 清透、安宁               | 青绿+深青+浅绿         |
| 蔚蓝格调    | 海洋灵感，专业冷静                               | 宋体风格（端正典雅） | 专业、从容               | 蔚蓝+深蓝+天蓝         |
| 二次元/动漫 | 日系动漫美学，大眼萌系，漫画感 | 手写圆体风格（圆润饱满） | 可爱、梦幻、萌系、少女心 | 樱花粉+天空蓝+薰衣草紫 |
| **少女粉** | **纯粉甜美少女风，温柔治愈，干净粉嫩** | **手写圆体风格（圆润饱满）** | **甜美、温柔、少女心、治愈** | **樱花粉+玫瑰粉+薰衣草紫** |
| 我的世界像素风 | Minecraft 像素方块美学，低分辨率块状质感 | 像素字体风格（等宽方块字） | 沙盒冒险、怀旧复古 | 草绿+钻石蓝+泥土棕 |

---

## Principles

| 原则     | 说明                                     |
| -------- | ---------------------------------------- |
| 优雅简洁 | 留白充足，元素克制，不杂乱               |
| 风格一致 | 同系列图保持配色、布局、装饰元素统一     |
| 清晰优先 | 信息层级分明，标题→正文→重点一目了然     |
| 对齐精确 | 双栏等宽，选项网格对齐，间距均匀         |
| 适龄匹配 | 面向12岁学生，活泼但不幼稚，专业但不枯燥 |
| 中文优先 | 所有文字内容默认中文                     |
| 代码规范 | 含C++代码时需使用OI竞赛风格（见下）      |

---

## OI代码风格规范（含代码的知识卡专用）

当知识卡包含C++代码时，必须按以下OI竞赛风格格式化。适用于所有风格主题。

### 1. 代码格式规范

| 规范 | 要求 | 示例 |
|:----|:-----|:------|
| **头文件** | 使用具体头文件，禁用 `bits/stdc++.h` | `#include <iostream>` |
| **命名空间** | 写 `using namespace std;` | |
| **变量作用域** | **全局变量**优先（竞赛标配） | `int n, a[105], sum;` |
| **变量命名** | 5字符以内短名 | `n, m, x, sum, mx, mn, ans, pos, cnt` |
| **数据结构** | 固定数组替代 vector | `a[105]` 而非 `vector<int>` |
| **左大括号** | **另起一行**（竞赛标准） | `for(...)\n{` 而非 `for(...){` |
| **缩进** | 4空格 | |
| **主函数** | 完整 `int main()` + `return 0;` | |
| **输入输出** | `cin`/`cout`，必要时用 `scanf`/`printf` | |
| **代码注释** | 关键步骤加中文注释 | `// ✨ 累加求和` |

### 2. OI风格代码模板

```
#include <iostream>
using namespace std;

int n, a[105], ans;

int main()
{
    // ✨ 输入
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    
    // ✨ 核心逻辑
    for (int i = 1; i <= n; i++)
    {
        // 处理
    }
    
    // ✨ 输出
    cout << ans;
    return 0;
}
```

### 3. 代码在Prompt中的描述

生成含代码的知识卡Prompt时，按以下方式描述：

```
Card "💻 代码" with computer icon, [风格对应配色] header. Code in SMALL FONT (OI style):
「#include <iostream>
 using namespace std;

 int n, a[105], ans;

 int main()
 {
     cin >> n;
     for (int i = 1; i <= n; i++)
     {
         // ✨ 核心代码
     }
     cout << ans;
     return 0;
 }」
```

### 4. 高频易错点提示

OI风格常见错误，在知识卡底部"高频易错点"中提醒：
- 全局变量自动初始化为0，局部变量不会
- `return 0;` 用于提前结束程序（查找场景）
- 数组下标从1开始还是从0开始需明确

---

## AVOID

- 避免装饰过多导致杂乱
- 避免元素拥挤，留白不足
- 避免对齐不精确，间距不均
- 避免风格突变（同系列保持一致）
- 避免使用"我有个朋友"、"众所周知"等AI痕迹表达

---

**更新日期**: 2026-08-01

**变更记录**：
- 2026-08-01: v1.9.5 经典字体定稿：回归瘦金体并加粗渲染——瘦劲锋利、锋芒劲挺，增其分量而不损锋棱，忌过细无力、忌肥肿圆钝
- 2026-08-01: v1.9.4 设计升级：灵动+醒目——标题带手绘色块/波浪下划线，重点荧光笔高亮，标签/便利贴微倾斜（2~5°）错落，卡片加主题色顶部条/角标，装饰错落有致
- 2026-08-01: v1.9.3 经典风格字体定稿：改"加粗手写钢笔体"——钢笔笔触流畅自然，字形舒展端庄，优雅利落不卡通，BOLD 加粗渲染、笔锋分明
- 2026-08-01: v1.9.2 经典风格字体再调：弃楷体，改"加粗手写圆体"——笔画圆润饱满、转角柔和，手写温度与手账气质相合，BOLD 加粗渲染保持清晰
- 2026-08-01: v1.9.1 经典风格字体微调：由"粗楷体"改为"加粗手写楷体"——保留 BOLD 加粗渲染，字形圆润丰腴、优雅流畅，忌粗犷生硬，回归手账温润气质
- 2026-08-01: v1.9.0 全风格字体默认加粗（BOLD/THICK STROKE）：经典风格"瘦金体"改为"粗楷体"，笔画浑厚饱满；手写体规范、Prompt模板、维度填充、风格速查表同步更新，杜绝细瘦字重
- 2026-07-31: v1.8.0 经典风格配色改革（深蓝/橙/绿 → 墨黑+朱红+赭黄+青绿，宣纸米底纹），模板配色引用同步更新；新增"我的世界像素风"风格（Minecraft 像素方块美学，像素字体，草绿+钻石蓝+泥土棕配色），触发词新增"像素风、我的世界、Minecraft、像素"；全篇表格格式对齐
- 2026-07-25: v1.8.0 字体全面解绑，不再指定具体字体名（如瘦金体/清秀宋体），改为风格方向描述，AI自动匹配系统可用字体；新增字体匹配说明
- 2026-07-25: v1.7.0 新增少女粉风格（纯粉甜美少女风）+ OI代码风格规范（含代码知识卡专用，全局变量/短名/大括号另起一行等竞赛标准）
- 2026-07-24: v1.6.0 新增二次元/动漫风格：日系动漫美学，大眼萌系，可爱圆体字体，樱花粉+天空蓝+薰衣草紫配色，Q版萌系角色/JK制服/洛丽塔/女仆装/猫耳/蝴蝶结/魔法杖/漫画对话框等丰富二次元元素，梦幻少女心氛围。触发词新增"二次元风格、动漫风格、JK制服、洛丽塔、女仆装、魔法少女、萌系"。
- 2026-07-24: v1.5.1 封面标题改为用户输入而非写死，步骤1新增封面标题/副标题为必填询问项，模板中死字标题全部替换为[用户标题]占位符
- 2026-07-24: v1.5.0 配色主题全面升级为风格体系：赛博朋克→科幻风格（配色与视觉元素重设），各风格新增视觉特征/字体/装饰元素/背景质感/氛围描述。字体不再固定瘦金体，各风格配独立字体（经典瘦金体/科幻硬朗黑体/活力圆体/青绿行楷/蔚蓝宋体）。配色速查表改为风格速查表含字体列，全篇引用更新。
- 2026-07-23: v1.4.0 新增四套风格：赛博朋克、活力手账、青绿新生、蔚蓝格调
- 2026-07-23: v1.3.0 优化字号层级，正文字体偏小，标题突出
- 2026-07-23: v1.2.0 风格升级为优雅简洁，强化留白、对齐、克制装饰
- 2026-07-23: v1.1.0 全面升级为手写体风格，所有文字和装饰元素均为手绘质感
- 2026-07-23: v1.0 初始版本，基于CSP-J初赛60天打卡系列视觉风格
