---
name: docx
description: 创建、读取、编辑Word文档(.docx)，支持格式化、表格、图片、页眉页脚、目录等
license: Proprietary

metadata:
  trigger: Word、docx、文档生成、文档编辑、Word文档
---

Domain keywords: Word, docx, 文档生成, 文档编辑, 表格, 目录

Summary: 使用docx-js创建新文档，通过解包→编辑XML→打包的方式编辑现有文档。

Strategy:
1. 新建文档：使用docx-js生成
2. 编辑文档：unpack→编辑XML→pack
3. 读取内容：pandoc提取文本
4. 格式转换：LibreOffice转PDF/图片

AVOID:
- AVOID 不设置页面尺寸，docx-js默认A4
- AVOID 使用\n换行，必须用单独Paragraph
- AVOID 使用unicode符号做列表，必须用LevelFormat.BULLET
- AVOID 表格不设宽度，必须同时设columnWidths和cell.width
- AVOID 使用WidthType.PERCENTAGE，必须用DXA

---

## 快速参考

| 任务 | 方法 |
|------|------|
| 读取内容 | `pandoc document.docx -o output.md` |
| 新建文档 | docx-js（见下方模板） |
| 编辑文档 | `unpack → 编辑XML → pack` |
| 转换PDF | `soffice --headless --convert-to pdf document.docx` |

## 前置依赖

```bash
npm install -g docx          # 新建文档
pip install python-docx      # 编辑文档
soffice (LibreOffice)        # 格式转换
pandoc                       # 文本提取
```

## 新建文档模板

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, LevelFormat, AlignmentType, WidthType, BorderStyle,
        ShadingType, PageBreak, Header, Footer, PageNumber } = require('docx');

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal",
        run: { size: 32, bold: true },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }
      ] }
    ]
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    headers: { default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] }) },
    children: [/* 内容 */]
  }]
});

Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

## 关键规则

| 规则 | 说明 |
|------|------|
| 页面尺寸 | US Letter: 12240×15840 DXA，默认A4 |
| 列表 | 用LevelFormat.BULLET，不用unicode符号 |
| 表格 | 同时设columnWidths和cell.width，用DXA不用PERCENTAGE |
| 图片 | ImageRun必须指定type参数 |
| 分页 | PageBreak必须放在Paragraph内 |
| 目录 | 标题必须用HeadingLevel，不能自定义样式 |

## 表格模板

```javascript
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [4680, 4680],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: { top: border, bottom: border, left: border, right: border },
          width: { size: 4680, type: WidthType.DXA },
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

## 编辑现有文档

### Step 1: 解包
```bash
python scripts/office/unpack.py document.docx unpacked/
```

### Step 2: 编辑XML
编辑`unpacked/word/document.xml`

**追踪修改**：
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>插入文本</w:t></w:r>
</w:ins>
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>删除文本</w:delText></w:r>
</w:del>
```

### Step 3: 打包
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

## 页面尺寸参考

| 纸张 | 宽度(DXA) | 高度(DXA) |
|------|----------|----------|
| US Letter | 12,240 | 15,840 |
| A4 | 11,906 | 16,838 |

**DXA单位**：1440 DXA = 1英寸
