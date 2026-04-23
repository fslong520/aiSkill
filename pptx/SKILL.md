---
name: pptx
description: 创建、读取、编辑PowerPoint文件(.pptx)，支持模板编辑、从头创建、格式转换等
license: Proprietary

metadata:
  trigger: PowerPoint、pptx、幻灯片、演示文稿、模板、PPT生成、PPT编辑
---

## Keywords

PowerPoint, pptx, 幻灯片, 演示文稿, 模板, PPT生成, PPT编辑, 幻灯片设计

## Summary

markitdown读取内容，pptxgenjs从头创建，解包→编辑→打包修改模板。

## Strategy

1. **读取内容**：markitdown或thumbnail.py
2. **从头创建**：pptxgenjs（见pptxgenjs.md）
3. **编辑模板**：unpack→编辑→pack（见editing.md）
4. **视觉检查**：转图片后检查问题

## AVOID

**设计禁忌**：
- AVOID 纯文字幻灯片，必须有视觉元素
- AVOID 标题下加装饰线，AI生成的标志
- AVOID 默认蓝色（#0070C0），选择匹配主题的颜色
- AVOID 重复相同布局，每张应有变化
- AVOID 居中正文，只标题居中
- AVOID 低对比度，确保文字/图标与背景对比明显

**层次禁忌**：
- AVOID 所有文字同样大小，必须有层次
- AVOID 所有文字同样颜色，主次不分
- AVOID 标题字号 < 正文字号 × 1.5

**留白禁忌**：
- AVOID 内容占比 > 70%，必须留白
- AVOID 边距 < 0.5 英寸，太挤
- AVOID 元素间距不均匀，显得乱

**配色禁忌**：
- AVOID 单页颜色 > 4 种，变成彩虹糖
- AVOID 高饱和度大面积使用，刺眼
- AVOID 文字与背景对比度不足，看不清

**字体禁忌**：
- AVOID 使用宋体/楷体，这是文档味
- AVOID 字号 < 12pt，投影看不清
- AVOID 中英文混用不同风格字体

---

## 快速参考

| 任务 | 方法 |
|------|------|
| 读取内容 | `python -m markitdown presentation.pptx` |
| 视觉预览 | `python scripts/thumbnail.py presentation.pptx` |
| 从头创建 | pptxgenjs（见pptxgenjs.md） |
| 编辑模板 | unpack→编辑→pack（见editing.md） |

## 前置依赖

```bash
# Python 依赖（用于读取和预览）
pip install markitdown[pptx] Pillow

# Node.js 依赖（用于生成 PPT）
npm install -g pptxgenjs

# html2pptx 工作流依赖
npm install pptxgenjs playwright sharp
npx playwright install chromium  # 首次运行必需！

# LibreOffice (soffice) 用于转PDF
# pdftoppm (poppler-utils) 用于转图片
```

**注意**：`npx playwright install chromium` 是首次使用 html2pptx 的必需步骤，否则会报错 "Executable doesn't exist"。

## 设计原则

### ⚠️ 核心铁律：代码生成 ≠ 好看

**pptxgenjs 是工具，不是设计师。** 代码只能控制位置和颜色，无法保证美感。

**推荐优先级**：
1. **模板编辑**（首选）→ 基于专业设计的模板修改内容
2. **代码生成**（次选）→ 仅用于简单/批量场景，且必须严格遵循设计规范

---

### 一、PPT设计四大原则（CPRA）

基于《写给大家看的设计书》的四大核心原则：

#### 1. 对比（Contrast）

**目的**：建立视觉层次，突出重点

| 对比类型 | 应用方法 | 具体数值 |
|---------|---------|---------|
| **字号对比** | 标题 ≥ 正文 × 2 | 主标题 44-60pt，正文 16-20pt |
| **字重对比** | 标题 Bold，正文 Regular | 至少两级字重差 |
| **色彩对比** | 主色 vs 辅色 vs 背景 | 对比度 ≥ 4.5:1 |
| **空间对比** | 密集 vs 留白 | 关键内容周围留白 30% |

**禁忌**：
- 所有文字同样大小 → 无层次
- 所有元素同样粗细 → 无重点
- 颜色过于接近 → 看不清

#### 2. 重复（Repetition）

**目的**：建立视觉统一性，形成品牌识别

| 重复元素 | 应用方法 |
|---------|---------|
| **色彩** | 全篇使用同一套配色（主色+辅色+强调色） |
| **字体** | 不超过 2 种字体，建立严格层级 |
| **图形** | 统一图标风格、分隔线样式 |
| **布局** | 同类页面保持结构一致 |

**80/20法则**：80% 严格重复，20% 适度变化

#### 3. 对齐（Alignment）

**目的**：创造秩序感和专业感

| 对齐类型 | 适用场景 |
|---------|---------|
| **左对齐** | 正文、列表（最常用） |
| **居中对齐** | 封面、标题页、短句 |
| **右对齐** | 数字、日期、价格 |

**网格系统**：
- 使用 4、6 或 12 列网格
- 所有元素沿网格线对齐
- 元素间距保持一致

#### 4. 亲密性（Proximity）

**目的**：通过空间关系表现信息关联

| 应用方法 | 具体数值 |
|---------|---------|
| **相关元素间距** | 0.2-0.3 英寸 |
| **不相关元素间距** | ≥ 0.5 英寸 |
| **组内间距** | 组间距的 1/4 到 1/2 |
| **留白占比** | 30%-40% |

**原则**：相关内容靠近，不相关内容远离

---

### 二、视觉层次（最重要！）

**每页必须有清晰的层次结构**：

| 层次 | 字号 | 颜色 | 粗细 | 用途 |
|------|------|------|------|------|
| 主标题 | 44-60pt | 主色/深色 | Bold | 封面标题、核心观点 |
| 副标题 | 24-32pt | 主色 | Bold | 章节标题、关键信息 |
| 正文 | 16-20pt | 深灰(#333) | Regular | 内容描述 |
| 辅助说明 | 12-14pt | 浅灰(#666) | Light | 注释、来源 |

**⚠️ 禁止**：所有文字用同样大小、同样颜色 → 没有层次感

---

### 三、留白黄金比例

**留白是设计的灵魂，不是浪费空间。**

**2024年极简设计趋势**：
- 留白占比：40%-50%（比以往更多）
- 内容聚焦：每页只传达一个核心信息
- 呼吸感：元素周围必须有足够的空白

**安全边距**（16:9 幻灯片）：
- 左右边距：0.8-1.0 英寸
- 上下边距：0.6-0.8 英寸
- 内容占比：不超过 60%，留出 40% 空白

**元素间距**：
- 标题与正文：0.4-0.6 英寸
- 段落之间：0.3-0.4 英寸
- 卡片之间：0.4-0.5 英寸
- 组内元素：0.2-0.3 英寸

**⚠️ 禁止**：把内容塞满整个页面 → 拥挤感，让人窒息

---

### 四、配色心理学

**一套配色 = 主色 + 辅色 + 强调色 + 背景色**

| 主题 | 主色 | 辅色 | 强调色 | 背景 | 适用场景 |
|------|------|------|--------|------|---------|
| 森林绿 | #2C5F2D | #97BC62 | #F5F5F5 | #FFFFFF | 教育、环保 |
| 午夜商务 | #1E2761 | #CADCFC | #FFFFFF | #F8F9FA | 商务、科技 |
| 珊瑚活力 | #F96167 | #F9E795 | #2F3C7E | #FFF5F5 | 创意、营销 |
| 暖陶土 | #B85042 | #E7E8D1 | #A7BEAE | #FAFAF0 | 艺术、生活 |
| 极简黑白 | #000000 | #666666 | #FFFFFF | #FFFFFF | 设计、时尚 |

**配色铁律**：
- 主色占比：10-20%（标题、重点）
- 辅色占比：20-30%（卡片、图标）
- 强调色占比：5-10%（按钮、高亮）
- 背景色占比：40-60%（页面底色）

**⚠️ 禁止**：
- 使用默认蓝色（#0070C0）→ "PPT味"
- 一页超过 4 种颜色 → "彩虹糖"
- 高饱和度大面积使用 → "刺眼"

---

### 四、字体规范

**中文字体**：思源黑体 > 微软雅黑 > 方正兰亭黑

**英文字体**：Helvetica > Arial > Calibri

**字号规范**：
| 元素 | 字号 | 行距 |
|------|------|------|
| 封面主标题 | 48-60pt | 1.2 |
| 页面标题 | 32-44pt | 1.2 |
| 副标题 | 20-28pt | 1.3 |
| 正文 | 16-20pt | 1.5 |
| 辅助说明 | 12-14pt | 1.4 |

**⚠️ 禁止**：使用宋体/楷体 → "文档味"

---

### 五、布局模板库

#### 封面页
```
┌─────────────────────────────────────┐
│                                     │
│         【大标题居中】              │
│         【副标题】                  │
│                                     │
│         【Logo/装饰】               │
│                                     │
└─────────────────────────────────────┘
```

#### 标题+列表页
```
┌─────────────────────────────────────┐
│  【页面标题】                       │
│  ─────────────────────────────────  │
│  • 要点1                           │
│  • 要点2                           │
│  • 要点3                           │
│                                     │
└─────────────────────────────────────┘
```

#### 双栏对比页
```
┌─────────────────────────────────────┐
│  【页面标题】                       │
│  ┌──────────┐  ┌──────────┐        │
│  │  左栏    │  │  右栏    │        │
│  │  内容    │  │  内容    │        │
│  └──────────┘  └──────────┘        │
└─────────────────────────────────────┘
```

#### 三列卡片页
```
┌─────────────────────────────────────┐
│  【页面标题】                       │
│  ┌────┐  ┌────┐  ┌────┐           │
│  │卡1 │  │卡2 │  │卡3 │           │
│  └────┘  └────┘  └────┘           │
└─────────────────────────────────────┘
```

#### 数据展示页
```
┌─────────────────────────────────────┐
│  【页面标题】                       │
│  ┌─────────┐  ┌─────────┐          │
│  │ 大数字  │  │ 大数字  │          │
│  │ 说明    │  │ 说明    │          │
│  └─────────┘  └─────────┘          │
└─────────────────────────────────────┘
```

---

### 六、AI 审美检查清单

生成 PPT 后，必须逐项检查：

**视觉层次**：
- [ ] 每页有 3-4 个明确的层次（标题/副标题/正文/辅助）
- [ ] 标题字号 ≥ 正文字号 × 1.5
- [ ] 重要信息使用主色或加粗

**留白**：
- [ ] 内容占比 ≤ 70%
- [ ] 边距 ≥ 0.5 英寸
- [ ] 元素间距均匀

**配色**：
- [ ] 单页颜色 ≤ 4 种
- [ ] 无默认蓝色（#0070C0）
- [ ] 文字与背景对比度足够

**字体**：
- [ ] 无宋体/楷体
- [ ] 最小字号 ≥ 12pt
- [ ] 中英文字体风格统一

**布局**：
- [ ] 每页布局不同
- [ ] 无纯文字幻灯片
- [ ] 对齐方式一致

---

### 七、设计迭代方法论

从 V1 到 V4 的专业设计进化路径：

**V1 - 基础原型**：
- 确定内容结构和信息架构
- 选择基础配色方案
- 完成基本布局

**V2 - 内容优化**：
- 翻译和本地化
- 修复文字溢出问题
- 尝试图片集成

**V3 - 布局修复**：
- 精确计算元素位置
- 调整卡片尺寸和间距
- 优化配色细节

**V4 - 专业重构**：
- 统一视觉语言（如三色顶栏、章节编号、页码系统）
- 建立清晰的信息层级（颜色、大小、位置区分重要性）
- 添加装饰元素增强设计感
- 确保呼吸感（适当留白，避免拥挤）

**统一视觉语言示例**：
```css
/* 三色顶栏系统 */
.top-bar { background: #ff6b6b; width: 240pt; }
.top-bar2 { background: #4ecdc4; width: 240pt; left: 240pt; }
.top-bar3 { background: #a855f7; width: 240pt; left: 480pt; }

/* 章节编号系统 */
.section-num { font-size: 14pt; color: #666; }
```

**信息层级设计**：
- 主标题：最大字号 + 主色 + Bold
- 副标题：中等字号 + 主色/辅色
- 正文：标准字号 + 深灰色
- 辅助信息：小字号 + 浅灰色

---

### 颜色选择（旧版保留）
不要默认蓝色，选择匹配主题的调色板：

| 主题 | 主色 | 辅色 | 强调色 |
|------|------|------|--------|
| 午夜商务 | 1E2761 | CADCFC | FFFFFF |
| 森林绿 | 2C5F2D | 97BC62 | F5F5F5 |
| 珊瑚活力 | F96167 | F9E795 | 2F3C7E |
| 暖陶土 | B85042 | E7E8D1 | A7BEAE |

### 字体搭配

| 标题字体 | 正文字体 |
|---------|---------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Impact | Arial |

### 字号规范

| 元素 | 字号 |
|------|------|
| 幻灯标题 | 36-44pt 粗体 |
| 章节标题 | 20-24pt 粗体 |
| 正文 | 14-16pt |
| 说明文字 | 10-12pt |

### 间距规范

- 最小边距：0.5英寸
- 内容块间距：0.3-0.5英寸
- 留白，不要填满

### 布局变化

每张幻灯片应有不同的布局：
- 双栏（左文字右图）
- 图标+文字行
- 2x2或2x3网格
- 半出血图片+内容叠加
- 大数字统计
- 对比列（前后/优缺点）

## 常见错误

### 一般错误

| 错误 | 正确做法 |
|------|---------|
| 纯文字幻灯片 | 添加图片/图标/图表 |
| 标题下装饰线 | 用留白或背景色 |
| 默认蓝色 | 选择匹配主题的颜色 |
| 重复相同布局 | 每张变化布局 |
| 居中正文 | 左对齐，只标题居中 |
| 低对比度 | 确保文字/图标与背景对比明显 |

### html2pptx 特定错误

当使用 html2pptx 工作流（HTML/CSS → Playwright → PPTX）时，可能遇到以下错误：

| 错误信息 | 原因 | 解决方案 |
|----------|------|---------|
| `Cannot find module 'pptxgenjs'` | node_modules 不在当前目录 | 运行 `npm install pptxgenjs playwright sharp` |
| `Executable doesn't exist at ...chromium` | Playwright 浏览器未安装 | 运行 `npx playwright install chromium` |
| `CSS gradients are not supported` | html2pptx 不支持 CSS 渐变 | 使用纯色背景或预渲染的渐变图片 |
| `Text element <p> has border` | 文本元素不支持 border 属性 | 将 border 移到单独的 `<div>` 元素 |
| `HTML content overflows body by XXpt horizontally` | 内容总宽度超过 720pt | 精确计算：边距 + (卡片宽 × 数量) + (间距 × (数量-1)) < 720 |
| `Text box ... ends too close to bottom edge` | 内容太靠近边缘 | 减小 padding、调整 font-size、确保 36pt 安全边距 |
| 中文文件名读取失败 | Windows 路径编码问题 | 重命名为英文文件名 |
| 图片位置不准 | 坐标计算错误 | 使用公式：英寸 = 点数 / 72 |

### 调试技巧

1. **逐页测试**：先单独测试每页，确认无误后再批量生成
2. **浏览器预览**：直接在浏览器中打开 HTML 文件预览效果
3. **控制台日志**：在脚本中添加详细日志追踪问题
4. **检查依赖**：确保 `npm install` 和 `npx playwright install chromium` 已执行

## QA检查（必须执行）

### 内容检查
```bash
python -m markitdown output.pptx
# 检查缺失内容、错别字、顺序错误
```

### 检查占位符残留
```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum"
```

### 视觉检查
转图片后检查：
```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

检查项目：
- 元素重叠
- 文字溢出/被裁切
- 间距不均匀
- 边距不足(<0.5")
- 对齐不一致
- 低对比度

## 验证循环

1. 生成→转图片→检查
2. 列出问题（没找到就是检查不够仔细）
3. 修复问题
4. 重新验证受影响的幻灯片
5. 重复直到无新问题

---

## 完整示例：从零创建产品介绍PPT

### 需求
创建一个5页的产品介绍PPT，主题是"智能家居系统"。

### Step 1: 初始化项目

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = '智国学堂';
pres.title = '智能家居系统介绍';
```

### Step 2: 设计配色方案

选择"森林绿"主题：
- 主色：#2C5F2D（深绿）
- 辅色：#97BC62（浅绿）
- 强调色：#F5F5F5（浅灰）

### Step 3: 创建幻灯片

```javascript
// 第1页：封面（大标题+副标题）
let slide1 = pres.addSlide();
slide1.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: '100%', h: '100%', fill: { color: '2C5F2D' } });
slide1.addText("智能家居系统", { x: 0.5, y: 2, w: 9, h: 1.5, fontSize: 44, color: "FFFFFF", bold: true, align: "center" });
slide1.addText("让生活更智能、更便捷", { x: 0.5, y: 3.5, w: 9, h: 0.5, fontSize: 20, color: "97BC62", align: "center" });

// 第2页：产品特点（图标+文字行布局）
let slide2 = pres.addSlide();
slide2.addText("核心特点", { x: 0.5, y: 0.3, w: 9, h: 0.8, fontSize: 32, color: "2C5F2D", bold: true });
slide2.addText([
  { text: "🏠 远程控制", options: { breakLine: true } },
  { text: "📱 语音交互", options: { breakLine: true } },
  { text: "🔒 安全防护", options: { breakLine: true } },
  { text: "⚡ 节能环保", options: { breakLine: true } }
], { x: 0.5, y: 1.5, w: 9, h: 3.5, fontSize: 24, color: "363636" });

// 第3页：数据统计（大数字+说明）
let slide3 = pres.addSlide();
slide3.addText("市场数据", { x: 0.5, y: 0.3, w: 9, h: 0.8, fontSize: 32, color: "2C5F2D", bold: true });
slide3.addText("100万+", { x: 1, y: 1.5, w: 3, h: 1, fontSize: 48, color: "2C5F2D", bold: true });
slide3.addText("活跃用户", { x: 1, y: 2.5, w: 3, h: 0.5, fontSize: 16, color: "666666" });
slide3.addText("99.9%", { x: 5, y: 1.5, w: 3, h: 1, fontSize: 48, color: "2C5F2D", bold: true });
slide3.addText("系统稳定性", { x: 5, y: 2.5, w: 3, h: 0.5, fontSize: 16, color: "666666" });

// 第4页：对比优势（双栏布局）
let slide4 = pres.addSlide();
slide4.addText("传统 vs 智能", { x: 0.5, y: 0.3, w: 9, h: 0.8, fontSize: 32, color: "2C5F2D", bold: true });
slide4.addText("传统家居", { x: 0.5, y: 1.3, w: 4, h: 0.5, fontSize: 20, color: "666666", bold: true });
slide4.addText("手动操作\n效率低\n能耗高", { x: 0.5, y: 1.8, w: 4, h: 2, fontSize: 16, color: "666666" });
slide4.addText("智能家居", { x: 5.5, y: 1.3, w: 4, h: 0.5, fontSize: 20, color: "2C5F2D", bold: true });
slide4.addText("自动控制\n高效便捷\n节能环保", { x: 5.5, y: 1.8, w: 4, h: 2, fontSize: 16, color: "2C5F2D" });

// 第5页：联系方式（简洁收尾）
let slide5 = pres.addSlide();
slide5.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: '100%', h: '100%', fill: { color: '2C5F2D' } });
slide5.addText("联系我们", { x: 0.5, y: 1.5, w: 9, h: 1, fontSize: 36, color: "FFFFFF", bold: true, align: "center" });
slide5.addText("www.example.com\n400-123-4567", { x: 0.5, y: 2.8, w: 9, h: 1, fontSize: 18, color: "97BC62", align: "center" });
```

### Step 4: 保存文件

```javascript
pres.writeFile({ fileName: "智能家居系统介绍.pptx" });
```

### Step 5: QA检查

```bash
# 内容检查
python -m markitdown 智能家居系统介绍.pptx

# 视觉检查
python scripts/thumbnail.py 智能家居系统介绍.pptx

# 检查占位符残留
python -m markitdown 智能家居系统介绍.pptx | grep -iE "xxxx|lorem|ipsum"
```

### 检查清单

- [ ] 每页布局不同（封面→列表→数字→对比→收尾）
- [ ] 颜色统一使用森林绿主题
- [ ] 无纯文字幻灯片
- [ ] 标题左对齐，正文左对齐
