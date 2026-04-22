---
name: pdf
description: PDF文件处理，包括读取、提取文本/表格、合并、拆分、旋转、水印、加密、OCR等
license: Proprietary

metadata:
  trigger: PDF、文档处理、文本提取、表格提取、合并PDF、拆分PDF、OCR
---

Domain keywords: PDF, 文档处理, 文本提取, 表格提取, 合并, 拆分, OCR

Summary: pypdf用于基础操作，pdfplumber用于提取，reportlab用于创建，qpdf用于命令行处理。

Strategy:
1. 读取PDF：pypdf或pdfplumber
2. 提取内容：pdfplumber提取文本/表格
3. 创建PDF：reportlab
4. 合并/拆分：pypdf或qpdf
5. OCR扫描件：pytesseract+pdf2image

AVOID:
- AVOID 用Unicode上下标字符，ReportLab字体不支持
- AVOID 不检查表格是否为空，可能报错
- AVOID 用data_only=True保存，公式会丢失

---

## 快速参考

| 任务 | 工具 |
|------|------|
| 合并/拆分 | pypdf |
| 提取文本 | pdfplumber |
| 提取表格 | pdfplumber |
| 创建PDF | reportlab |
| 命令行 | qpdf/pdftotext |
| OCR | pytesseract |

## 前置依赖

```bash
pip install pypdf pdfplumber reportlab
# poppler-utils: pdftotext, pdftoppm, pdfimages
# qpdf: PDF操作
```

## 读取PDF

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## 提取表格

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # 检查非空
                for row in table:
                    print(row)
```

## 合并PDF

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

## 创建PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter
c.drawString(100, height - 100, "Hello World!")
c.save()
```

## 上下标（重要）

**禁止使用Unicode上下标**，用ReportLab标签：
```python
from reportlab.platypus import Paragraph

# 正确：用<sub>/<super>标签
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])
squared = Paragraph("x<super>2</super>", styles['Normal'])
```

## 命令行工具

```bash
# 提取文本
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt  # 保留布局

# 合并
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# 拆分
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf

# 旋转
qpdf input.pdf output.pdf --rotate=+90:1

# 解密
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

## OCR扫描件

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = ""
for image in images:
    text += pytesseract.image_to_string(image)
```

## 水印

```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

## 加密

```python
writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```
