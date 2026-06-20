---
name: qiaomu-ai-prd
description: |
  Generate AI-implementable product requirement documents (PRDs) from one-line product ideas, vague app/site/tool requests, or feature concepts. Use when the user asks for PRD, 产品需求文档, 需求文档, AI 可执行 PRD, 产品规格, MVP 方案, app/site/tool planning, or developer handoff docs for AI coding assistants.
---

# Qiaomu AI PRD

把一句模糊产品想法，写成产品经理、人类开发者和 AI 编程助手都能直接执行的 PRD。

Copyright (c) 向阳乔木
X: https://x.com/vista8
GitHub: https://github.com/joeseesun/

## Operating Mode

Run as a production-lite product specification skill.

Default assumptions:

- The user usually wants a finished PRD, not a questionnaire.
- If the input is only one sentence, infer the best conservative product direction and continue.
- Ask only when the answer would materially change product category, platform, safety, legal risk, budget, data ownership, or implementation scope.
- When a choice is needed, make the best default decision and give the reason inside the relevant chapter.
- Do not start implementation unless the user explicitly asks; this skill produces the PRD.
- Write Chinese-first unless the user asks for English.
- Output all 11 required chapters in order. Do not skip chapters, even in compact mode.
- Add an `AI 速读卡` before the chapters so an implementing agent can grasp the product in 10 lines or fewer.
- Keep implementation details out unless they affect product behavior, architecture risk, data contracts, verification, or AI handoff.
- Do not invent current competitor, API, platform, or package facts. If current facts matter and cannot be verified, mark them as unresolved or use `未知`.
- Treat fuzzy product words as direction, not proof. Translate them into concrete UI states, measurable targets, outputs, and acceptance criteria.
- Separate each important instruction into `硬约束`, `推荐默认`, or `发挥空间` so implementation agents know what must hold and where they can improve freely.

## Workflow

1. Parse user input and optional mode tags. Mode tags are strings like `[深度模式]` anywhere in the input. If multiple tags conflict, apply the priority rule in `Optional Modes` section.
2. Decide the likely product category, target users, primary platform, and MVP surface.
3. Decide the product's `硬约束`, `推荐默认`, and `发挥空间`.
4. Identify facts that must be verified, assumptions that can be used safely, and unknowns that must be represented honestly.
5. Generate the PRD following the chapter contract defined in `Output Contract` section.
6. For each module, include realistic ASCII UI/state diagrams, normal flow, at least two failure paths, states, dependencies, and 1-3 real product decisions or `无`.
7. Add `超预期机会`: 2-4 product moments that can make the implementation feel memorable without bloating P0.
8. For differentiation and technical choices, explain structural causes and tradeoffs instead of saying competitors "did not think of it".
9. Give numeric performance targets with measurement methods and degradation thresholds.
10. Finish chapter 11 as a direct note to the implementing AI assistant using second person `你`, including acceptance scripts it can run or manually verify.
11. Run the self-check in `Quality Bar` section before final output.
12. If the PRD is saved to a file, verify required chapters exist and no placeholders remain.

## Output Contract

When the user gives a product idea, output the PRD directly. Use this order:

1. `# [产品名] PRD`
2. `## AI 速读卡`
3. `## 第一章：产品概述`
4. `## 第二章：整体布局与导航`
5. `## 第三章：核心模块详细设计`
6. `## 第四章：超越竞品的差异化功能`
7. `## 第五章：数据模型`
8. `## 第六章：技术架构`
9. `## 第七章：交互细节`
10. `## 第八章：导出与输出系统`
11. `## 第九章：开发优先级`
12. `## 第十章：性能指标`
13. `## 第十一章：开发者交接说明`

Do not add a long preface. If assumptions are needed, place them inside the relevant chapter, usually `1.3 可行性边界`, module `待决问题`, or `第十一章 d) 已知的未知项`.

### AI 速读卡必含字段

AI 速读卡必须包含以下字段，每项一行，共不超过 10 行：

```
产品名：[名称]
一句话：[用一句话描述产品核心价值]
目标用户：[主要用户群体]
核心场景：[用户使用产品的首要场景]
平台：[Web/iOS/Android/桌面/多端]
关键差异：[与同类产品最大的区别]
P0功能：[最小可用版本包含的核心功能，3-5个]
技术栈：[主要技术选型]
风险项：[最大的技术或市场风险]
```

### 各章交付物定义

| 章节 | 必须包含 | 可选 |
|------|----------|------|
| 第一章：产品概述 | 产品定义、目标用户画像、可行性边界 | 商业模式、市场数据 |
| 第二章：整体布局与导航 | 页面结构图、导航逻辑 | 信息架构分析 |
| 第三章：核心模块详细设计 | 每个模块的ASCII图、正常流程、2+失败路径、状态定义 | 边界案例分析 |
| 第四章：超越竞品的差异化功能 | 差异点说明、结构性原因分析 | 竞品详细对比 |
| 第五章：数据模型 | JSON数据结构（含注释和version字段） | 数据库schema |
| 第六章：技术架构 | 架构图、技术选型及理由 | 性能基准测试方案 |
| 第七章：交互细节 | 交互流程图、状态机 | 微交互动画描述 |
| 第八章：导出与输出系统 | 支持格式、输出流程 | 批量导出方案 |
| 第九章：开发优先级 | P0/P1/P2功能列表、MVP定义 | 开发时间估算 |
| 第十章：性能指标 | 数字指标、测量方法、降级阈值 | 压测方案 |
| 第十一章：开发者交接说明 | 验收剧本、已知未知项、给AI的说明 | 环境配置指南 |

## Optional Modes

Recognize these tags anywhere in the user request:

- `[深度模式]`: add boundary-case analysis to each major module.
- `[精简模式]`: keep every chapter, but focus detailed design on P0; mark lower tiers as `待扩展`.
- `[前端视角]`: add component decomposition and state-management guidance where product-relevant.
- `[后端视角]`: add API design and database schema where product-relevant.
- `[移动优先]`: make all layout diagrams mobile-first unless the product is clearly desktop-only.
- `[竞品深挖]`: deepen competitor weakness analysis and product blind-spot reasoning.
- `[商业化]`: add pricing, paid feature, and monetization implications where appropriate.
- `[开源友好]`: prefer permissive open-source libraries, especially MIT, when the choice does not harm the product.

### 模式优先级与冲突处理

当多个模式同时出现时，按以下规则处理：

**优先级规则：**
1. 视角类模式互斥：`[前端视角]` 和 `[后端视角]` 不同时使用，若同时出现则只应用 `[前端视角]`
2. 深度类叠加：`[深度模式]`、`[竞品深挖]`、`[商业化]` 可叠加
3. 平台类优先：`[移动优先]` 覆盖其他平台假设
4. 复杂度类互斥：`[精简模式]` 与其他深度类冲突时，以 `[精简模式]` 为准
5. 开放类独立：`[开源友好]` 可与任何模式组合

**示例：**
- `[深度模式][商业化]` → 每个模块加边界案例，整体加商业模式分析
- `[移动优先][前端视角]` → 移动布局图 + 组件拆分
- `[精简模式][深度模式]` → 只详细设计P0，但P0部分有边界案例分析

## Quality Bar

A strong PRD from this skill:

- makes product decisions instead of pushing every ambiguity to the user
- gives an implementing agent a short `AI 速读卡`
- distinguishes `硬约束`, `推荐默认`, and `发挥空间`
- contains realistic ASCII diagrams with actual labels and representative content
- names meaningful competitor differences instead of filling a comparison table with obvious parity
- defines module states, data flows, failure paths, and open decisions
- includes a small set of `超预期机会` that invite tasteful implementation beyond the baseline
- uses data structures with commented JSON fields and a top-level `version`
- explains technical choices and package-size uncertainty honestly
- explains when a technical choice is replaceable and what must remain invariant
- prioritizes by user behavior impact, not implementation difficulty
- turns performance expectations into exact numbers and measurement methods
- tells the implementing AI what to build first, what not to reinterpret, what to freely improve, what remains unknown, and how to verify the first build

### 质量自检清单

输出PRD前，逐项检查：

- [ ] AI速读卡字段完整（9个必填项）
- [ ] 11章全部存在，无跳过
- [ ] 无占位符（`[产品名]`、`按钮 A`、`TODO`、`待补充`等）
- [ ] 无模糊性能用语（`快`、`流畅`、`轻量`、`可扩展`等），全部替换为数字
- [ ] 每章有`硬约束`/`推荐默认`/`发挥空间`标注
- [ ] 第三章每个模块有ASCII图、正常流程、2+失败路径
- [ ] 第五章数据结构有JSON字段注释和version字段
- [ ] 第十章性能指标有具体数字、测量方法、降级阈值
- [ ] 第十一章有验收剧本和已知未知项
- [ ] 未编造竞品信息、API事实、平台限制

### 拒绝或修订规则

遇到以下情况时，按顺序执行：

1. **占位符/模糊用语** → 直接替换为合理默认值，并在对应章节标注"默认填充"
2. **事实性错误** → 标记为`未知`或移除，不编造
3. **缺少验收剧本** → 自动生成基础验收脚本
4. **P0功能过多** → 建议裁剪至3-5个核心功能，询问用户确认
5. **章节缺失** → 自动补充缺失章节

执行后在PRD末尾添加一行：`[质量修订] 已自动修正以下问题：xxx`
