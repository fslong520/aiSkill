---
name: AI读书
description: 把整本书提炼成结构化精华内容——按阅读目的决定保留什么，AI 逐章提取关键知识点，构建知识图谱串联概念，多角色答辩式校验摘要。
metadata:
  slug: ai-reader
  trigger: 读书、阅读、提炼、摘要、知识图谱、书摘、拆书
---

## Keywords

读书, 提炼, 知识图谱, 电子书, 结构化笔记

## Summary

用户提供图书文件（EPUB/MD/TXT/PDF），AI 逐章提取关键知识单元，构建跨章节概念关联知识图谱，输出结构化摘要。无需额外配置 LLM 供应商。

## Strategy

1. **文本提取**：用 extract_book.py 解析图书，按章节拆分
2. **逐章精读**：对每章提取关键知识单元（chunks）
3. **概念串联**：跨章节发现相关概念，构建知识图谱
4. **多角校验**：多角色答辩式审查摘要完整性
5. **成果输出**：章节摘要 + 知识图谱 + 全书总览

## Prerequisites

- PDF 解析依赖 `pdftotext`（poppler-utils）：
  ```bash
  sudo apt install poppler-utils    # Ubuntu/Debian
  brew install poppler              # macOS
  ```

## AVOID

- AVOID 跳章阅读，必须逐章处理
- AVOID 一次性读完所有章节再提取——每章读完立即提取
- AVOID 知识图谱过于稀疏——至少 3 条跨章节连线
- AVOID 摘要写成「本书介绍了…」式干瘪官腔
- AVOID 遗漏反直觉或有争议的观点
- AVOID 跳过用户确认直接出结果

---

## 快速开始

```bash
# 提取章节
python3 modules/extract_book.py 图书.pdf --pretty

# 按 modules/02-chunk.md → 03-graph.md → 04-review.md → 05-output.md 依次执行
```

---

## 完整示例

**输入**：`算法启蒙.pdf`，阅读目的 = "关注教育方法"

**执行流程**：

```
① extract_book.py → 7 章节（前言 + ch1-ch6）
② 逐章精读 → 每章提取 4-6 个知识单元 + 反直觉点
③ 概念串联 → 14 条概念连线 + 3 条贯穿线索（"蛇"）
④ 多角校验 → AI 撰写摘要 → 用户提问 → AI 答辩补充
⑤ 输出笔记 → 《算法启蒙书》读书笔记.md
```

**输出片段**（知识图谱）：
```markdown
| 二分策略 | → 实例 → | Wordle 猜词 | ch1 |
| 递归调用栈 | = 天然决策树 | 回溯法数据管理 | ch2 |
| 剪枝 | → 效果 → | 同等时间看得更远 | ch6 |
```

---

## 工作流程

详细步骤见 modules/ 中各文件：

| 阶段 | 文件 | 说明 |
|------|------|------|
| Phase 1 文本提取 | `modules/extract_book.py` | 解析图书为章节 JSON |
| Phase 2 逐章精读 | `modules/02-chunk.md` | 每章提取知识单元 |
| Phase 3 概念串联 | `modules/03-graph.md` | 跨章节构建知识图谱 |
| Phase 4 多角校验 | `modules/04-review.md` | 答辩式审查摘要 |
| Phase 5 成果输出 | `modules/05-output.md` | 结构化读书笔记 |
| — 用户确认节点 | 各阶段开始前 | 询问用户是否满意当前结果 |

**贯穿原则**：每阶段完成后暂停，询问用户是否满意当前结果，确认后再进入下一阶段。

## 参考

- SpineDigest 管线：chunk 提取 → 知识图谱 → 对抗摘要
- 认知心理学：Miller's Law（工作记忆 7±2 组块）
- 知识图谱节点-边模型
