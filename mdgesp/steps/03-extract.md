# 03-extract — 提取PDF全文 & 检查插图

## 文本提取

```bash
pdftotext -layout "{pdf_path}" "{txt_path}"
```

参数说明：
- `-layout`：保持版面布局（选择题选项对齐）
- 输出文件编码：UTF-8

## 检查流程图（三级专用）

三级试卷常有流程图题（如 `flowchart_q*.jpg`）。检查方法：

```bash
pdftoppm -png -r 300 -f {page} -l {page} "{pdf_path}" /tmp/check_page
```

翻页查看可疑页面的图片内容：
- `look_at` 工具读取生成的 PNG
- 确认是否有流程图、表格、图片等非文本内容

若有流程图，按命名规范保存：
```
{dir_name}/{file_prefix}-flowchart_q{题号}.jpg
```

## 提取答案表

PDF 第一页顶部通常有选择题答案表。`pdftotext` 输出中可见：

```
题号 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
答案 A B A B D A B D A  B   C   A   A   A   C
```

判断题答案 PDF **通常不提供**，需自行分析。

## 验证

- [ ] `txt_path` 文件存在且行数 > 100
- [ ] 答案表已正确提取（与图片核对）
- [ ] 三级：已检查所有页面，流程图已保存（如有）
- [ ] 若 pdftotext 输出异常（乱码、缺字），改用图片校对
