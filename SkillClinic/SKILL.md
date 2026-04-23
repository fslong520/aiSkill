---
name: 技能诊所
description: "🏥 技能诊所 | 诊断优化 + 创建技能。触发：技能体检、技能诊断、创建技能"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion

metadata:
  priority: 750
  slug: skillclinic
  version: "2.1.0"
  trigger: 技能体检、技能诊断、技能评估、技能优化、技能检查、创建技能、设计技能、新建技能、skill clinic
  copaw:
    emoji: "🏥"
---

# 🏥 技能诊所

## Keywords

技能体检、技能诊断、技能创建、Gene结构、metadata.trigger

## Summary

诊断优化现有技能 + 从零创建新技能。

## Strategy

1. 询问用户意图（诊断 or 创建）
2. **诊断**：读取 modules/01-diagnose.md → 检查结构 → 算分评级 → 开处方
3. **创建**：读取 modules/02-create.md → 收集需求 → 选择模板 → 创建文件 → 验证质量

## Language（评分项，15分）

| 得分 | 标准 |
|------|------|
| 15 | 极致简练，无废话，每句话有信息增量 |
| 10 | 较简练，有少量冗余 |
| 5 | 冗余较多 |
| 0 | 废话连篇 |

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

---

## 功能模块

| 模块 | 触发 | 流程 |
|------|------|------|
| 诊断优化 | 体检、诊断、评估 | modules/01-diagnose.md |
| 创建技能 | 创建、设计、新建 | modules/02-create.md |

## 评分标准

| 维度 | 分值 | 检测项 |
|------|------|--------|
| 结构 | 30 | Keywords(8) + Summary(8) + Strategy(8) + AVOID(6) |
| 触发 | 10 | metadata.trigger |
| 内容 | 35 | 语言简练(15) + 信号密度(10) + 可执行性(10) |
| 实践 | 25 | 渐进式披露(10) + Human-in-the-Loop(10) + CLI友好(5) |

| 等级 | 分数 |
|------|------|
| S | ≥80 |
| A | 70-79 |
| B | 60-69 |
| C | <60 |

## 参考

- 评分标准：reference/criteria.md
- 使用示例：examples/demo.md
