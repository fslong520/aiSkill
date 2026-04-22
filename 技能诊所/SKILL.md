---
name: SkillClinic
slug: skillclinic
description: AI 技能体检诊断，检测Gene结构完整性、触发配置、内容质量
allowed-tools:
  - Read
  - Glob
  - Write
  - Edit
  - AskUserQuestion

metadata:
  trigger: 技能体检、技能诊断、技能评估、技能优化、技能检查、skill clinic
---

# 技能诊所

## Summary

技能质量体检：检测Gene结构（keywords/summary/strategy/AVOID）+ 触发配置（metadata.trigger）+ 内容质量，输出评分和改进建议。

## Keywords

技能体检、Gene结构、技能质量、触发配置、metadata.trigger

## Strategy

1. **问用户要体检哪个技能**：支持技能名称或完整路径
2. **读取技能文件**：SKILL.md 和目录下其他文档
3. **检查Gene结构**：keywords、summary、strategy、AVOID
4. **检查触发配置**：metadata.trigger 是否存在（关键！无此字段技能无法触发）
5. **算分**：结构(35) + 触发(10) + 内容(35) + 实践(20) - 负贡献
6. **定等级**：S/A/B/C
7. **开处方**：提出改进建议，问用户是否执行

## AVOID

- AVOID 只读SKILL.md就下结论，目录下其他文档也要看
- AVOID 只改SKILL.md不改其他文档，改进要覆盖所有相关文件
- AVOID 给了分不给建议，等于没说
- AVOID 改文档时表述不清，要说清楚"错误行为 + 应该怎样"
- AVOID 忽略metadata.trigger检查，无此字段技能无法被触发
- AVOID 自己写得烂还去评价别人，先照照镜子

---

## 入口

问用户：要体检哪个技能？

支持技能名称或完整路径。

## 标准

| 维度 | 满分 | 检测项 |
|------|------|--------|
| 结构分 | 35 | keywords + summary + strategy + AVOID |
| 触发分 | 10 | metadata.trigger（无此字段=技能无法触发！）|
| 内容分 | 35 | Token效率 + 信号密度 + 可执行性 |
| 实践分 | 20 | 渐进式披露 + Human-in-the-Loop + CLI友好 |

| 等级 | 分数 |
|------|------|
| S | ≥80 |
| A | 70-79 |
| B | 60-69 |
| C | <60 |

## 参考

详细标准见 reference/criteria.md
