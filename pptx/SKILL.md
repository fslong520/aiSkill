---
name: pptx
description: 创建、读取、编辑PowerPoint文件(.pptx)，支持模板编辑、从头创建、格式转换等
license: Proprietary
---

Domain keywords: PowerPoint, pptx, 幻灯片, 演示文稿, 模板

Summary: markitdown读取内容，pptxgenjs从头创建，解包→编辑→打包修改模板。

Strategy:
1. 读取内容：markitdown或thumbnail.py
2. 从头创建：pptxgenjs（见pptxgenjs.md）
3. 编辑模板：unpack→编辑→pack（见editing.md）
4. 视觉检查：转图片后检查问题

AVOID:
- AVOID 纯文字幻灯片，必须有视觉元素
- AVOID 标题下加装饰线，AI生成的标志
- AVOID 默认蓝色，选择匹配主题的颜色
- AVOID 重复相同布局，每张应有变化
- AVOID 居中正文，只标题居中

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
pip install markitdown[pptx] Pillow
npm install -g pptxgenjs
# LibreOffice (soffice) 用于转PDF
# pdftoppm (poppler-utils) 用于转图片
```

## 设计原则

### 颜色选择
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

| 错误 | 正确做法 |
|------|---------|
| 纯文字幻灯片 | 添加图片/图标/图表 |
| 标题下装饰线 | 用留白或背景色 |
| 默认蓝色 | 选择匹配主题的颜色 |
| 重复相同布局 | 每张变化布局 |
| 居中正文 | 左对齐，只标题居中 |
| 低对比度 | 确保文字/图标与背景对比明显 |

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
