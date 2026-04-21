---
name: 技能诊所
slug: skillclinic
description: AI 技能体检诊断
allowed-tools:
  - Read
  - Glob
  - Write
  - Edit
  - AskUserQuestion
---

Domain keywords: 技能体检, Gene结构, 技能质量

Summary: 技能写得好不好，跑一遍便知。

Strategy:
1. 问用户要体检哪个技能
2. 读 SKILL.md 和目录下其他文档
3. 查 Gene 结构：keywords、summary、strategy、AVOID
4. 算分：结构(40) + 内容(40) + 实践(20) - 负贡献
5. 定等级：S/A/B/C
6. 开处方：提出改进建议（可选鲁迅式半文半白风格），问用户是否执行

AVOID:
- AVOID 只读 SKILL.md 就下结论，目录下其他文档也要看
- AVOID 只改 SKILL.md 不改其他文档，改进要覆盖所有相关文件
- AVOID 给了分不给建议，等于没说
- AVOID 改文档时 AVOID 表述不清，要说清楚"错误行为 + 应该怎样"
- AVOID 自己写得烂还去评价别人，先照照镜子

---

## 入口

问用户：要体检哪个技能？

支持技能名称或完整路径。

## 标准

| 维度 | 满分 | 检测项 |
|------|------|--------|
| 结构分 | 40 | keywords + summary + strategy + AVOID |
| 内容分 | 40 | Token效率 + 信号密度 + 可执行性 |
| 实践分 | 20 | 渐进式披露 + Human-in-the-Loop + CLI友好 |

| 等级 | 分数 |
|------|------|
| S | ≥80 |
| A | 70-79 |
| B | 60-69 |
| C | <60 |

## 参考

详细标准见 reference/criteria.md
