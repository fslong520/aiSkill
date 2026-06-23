---
priority: 600
name: mdgesp
version: 1.0.0
description: "📋 GESP试卷处理：从官网下载PDF→提取全文→检查流程图→创建标准化文件(.md/.json/答案.md) | 触发：GESP、真题、试卷处理、gesp真题"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob

metadata:
  slug: mdgesp
  trigger: GESP、真题、gesp真题、试卷处理、PDF转真题、GESP试卷、等级考试真题
---

# mdgesp — GESP真题处理

## Keywords
GESP、真题、等级考试、试卷处理、PDF提取、真题Markdown、真题JSON、创题

## Summary
从 GESP 官网下载官方试卷 PDF，提取全文文本，检查流程图（三级），创建标准化真题包（.md 试卷 / .json 结构化 / -答案.md 答案表）。

## Strategy

### 整体流程

1. 读 `steps/01-detect.md` → 解析用户输入（年份、级别、月份），确定文件路径
2. 读 `steps/02-download.md` → urlgo 访问 GESP 官网，取 PDF 链接 → wget 下载
3. 读 `steps/03-extract.md` → pdftotext 提取全文，pdftoppm 转图片查流程图
4. 读 `steps/04-create.md` → 按既有格式创建 .md / .json / -答案.md
5. 验证：核对 PDF 答案表，修正选择题答案

### 目录规范

```
GESP{级别}级真题/
  GESP{级别}{年份}{月份}-真题.md
  GESP{级别}{年份}{月份}-真题.json
  GESP{级别}{年份}{月份}-真题-答案.md
  GESP{级别}{年份}{月份}.pdf
  GESP{级别}{年份}{月份}.txt
```

## Language
- 极致简练，去"请"、"可以"、
- 用列表/表格替代段落
- 每步必有验证

## AVOID
- AVOID 从第三方网站拼凑真题内容（必须以官网PDF为准）
- AVOID 忽略流程图/图片（三级必查）
- AVOID 跳过答案表验证
- AVOID 未读步骤文件就执行
- AVOID 用 playwright 代替 urlgo（本项目用 urlgo）
