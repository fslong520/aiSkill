---
name: 文件读取
description: "Read and summarize text-based file types only. Prefer read_file for text formats; use execute_shell_command for type detection when needed. PDF/Office/images/archives are handled by other skills."
metadata:
  slug: file_reader
  builtin_skill_version: "1.1"
  trigger: 读取文件、文件内容、file reader、read file、文本文件
  copaw:
    emoji: "📄"
    requires: {}
---

# File Reader Toolbox

## Summary

读取和摘要文本文件：txt/md/json/yaml/csv/log/sql/代码文件。PDF/Office/图片/音视频由其他技能处理。

## Keywords

文件读取、文本文件、read file、file reader、文件摘要

## Strategy

1. **类型检测**：`file -b --mime-type "/path/to/file"` 确认文件类型
2. **选择工具**：文本文件用read_file，大文件用tail提取
3. **读取内容**：获取相关部分，避免全量读取大文件
4. **摘要输出**：展示关键部分或摘要给用户

## AVOID

- AVOID 处理PDF/Office/图片/音视频文件，这些由其他技能处理
- AVOID 直接读取超大文件全部内容，应用tail提取关键部分
- AVOID 执行不可信文件，存在安全风险
- AVOID 忽略文件类型检测，应先用file命令确认类型

## 文本文件类型

适用：`.txt`, `.md`, `.json`, `.yaml/.yml`, `.csv/.tsv`, `.log`, `.sql`, `.ini`, `.toml`, `.py`, `.js`, `.html`, `.xml` 等源代码

## 大文件处理

```bash
tail -n 200 "/path/to/file.log"
```

摘要最后的错误/警告和值得注意的模式。

## 超出范围

以下文件类型由专门技能处理：
- PDF → pdf技能
- Office (docx/xlsx/pptx) → docx/xlsx/pptx技能
- 图片 → 图片处理技能
- 音视频 → 音视频技能
