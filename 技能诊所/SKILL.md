---
name: skillclinic
description: "🏥 技能诊所 | 诊断优化 + 创建技能 + 先例研究 + 评估门禁 + 运维反馈。触发：技能体检、技能诊断、创建技能、查重、门禁、反馈"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Bash

metadata:
  priority: 750
  slug: skillclinic
  version: "3.0.0"
  trigger: 技能体检、技能诊断、技能评估、技能优化、技能检查、创建技能、设计技能、新建技能、skill clinic、查重、先例研究、技能门禁、技能验证、技能反馈
  copaw:
    emoji: "🏥"
---

# 🏥 技能诊所

## Keywords

技能体检、技能诊断、技能创建、先例研究、评估门禁、运维反馈、Gene结构、metadata.trigger

## Summary

诊断优化现有技能 + 从零创建新技能 + 先例研究 + 评估门禁 + 运维反馈。

## Strategy

1. 询问用户意图（诊断/创建/查重/门禁/反馈）
2. **诊断**：读取 modules/01-diagnose.md → 检查结构 → 算分评级 → 开处方
3. **创建**：读取 modules/03-precedent.md（先例研究）→ 读取 modules/02-create.md → 收集需求 → 选择模板 → 创建文件 → 读取 modules/05-gate.md（门禁验证）
4. **查重**：读取 modules/03-precedent.md → 搜索 → 输出建议
5. **门禁**：读取 modules/05-gate.md → 执行验证 → 输出结果
6. **反馈**：读取 modules/04-feedback.md → 记录 → 分析 → 建议

## Language（评分项，15分）

| 得分 | 标准 |
|------|------|
| 15 | 极致简练，无废话，每句话有信息增量，Token≤200 |
| 12 | 较简练，有少量冗余，Token≤300 |
| 10 | 良好，Token≤500 |
| 8 | 可接受，需精简，Token≤700 |
| 5 | 过长，需重构，Token≤1000 |
| 0 | 冗长，信号稀释，Token>1000 |

**要求**：
- 用表格/列表代替段落
- 去掉"请"、"可以"、"能够"等虚词
- 不解释显而易见的事

## AVOID

- AVOID 只读SKILL.md就下结论
- AVOID 只改SKILL.md不改其他文档
- AVOID 给了分不给建议
- AVOID 忽略metadata.trigger检查
- AVOID 冗余描述、废话连篇
- AVOID Strategy 写死、无裁量空间

---

## 功能模块

| 模块 | 触发 | 流程 |
|------|------|------|
| 诊断优化 | 体检、诊断、评估 | modules/01-diagnose.md |
| 创建技能 | 创建、设计、新建 | modules/02-create.md |
| 先例研究 | 查重、类似、有没有 | modules/03-precedent.md |
| 评估门禁 | 门禁、验证、发布检查 | modules/05-gate.md |
| 运维反馈 | 反馈、失败、漂移 | modules/04-feedback.md |

## 评分标准

| 维度 | 分值 | 检测项 |
|------|------|--------|
| 结构 | 30 | Keywords(8) + Summary(8) + Strategy(8) + AVOID(6) |
| 触发 | 10 | metadata.trigger |
| 内容 | 40 | 语言简练(15) + 信号密度(10) + 可执行性(10) + **裁量空间(5)** |
| 实践 | 20 | 渐进式披露(10) + Human-in-the-Loop(5) + CLI友好(5) |

| 等级 | 分数 |
|------|------|
| S | ≥80 |
| A | 70-79 |
| B | 60-69 |
| C | <60 |

## 参考

- 评分标准：reference/criteria.md
- 使用示例：examples/demo.md
