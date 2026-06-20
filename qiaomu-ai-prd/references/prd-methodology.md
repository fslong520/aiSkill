# PRD Methodology

Use this reference when generating a full PRD. The goal is not to fill a template; the goal is to think through the product and express that thinking in a way both humans and AI coding assistants can execute.

## Role

Act as a senior product manager with 10 years of experience and enough frontend architecture and system-design judgment to make product-relevant technical decisions.

The PRD must be:

- precise enough for an AI coding assistant to implement
- flexible enough to surface non-obvious product insights
- structured enough to remove ambiguity
- open enough to allow creative problem solving

## Chapter Contract

Generate chapters in this exact order. Do not skip any chapter.

### AI 速读卡

Before chapter one, add a short implementation card. Keep it to 10 lines or fewer so an AI coding assistant can skim it before building.

Required fields:

- 产品一句话
- 核心循环
- 目标平台
- 硬约束
- 推荐默认
- 发挥空间
- P0 验收
- 最容易翻车
- 超预期机会

Use concrete content, not labels alone. The card is not a replacement for the PRD; it is a map for the implementer.

### 第一章：产品概述

Start with one positioning sentence:

```text
[产品名] 是一款 [品类]，让 [目标用户] 能够 [核心动作]，而无需 [被消除的关键摩擦]。
```

Then include:

#### 1.1 差异化对比表

Compare with the most relevant competitors.

Columns:

| 功能 | 竞品 | 本产品 | 实现方式 |
|---|---|---|---|

Only include rows with real differences. Do not pad with obvious equal features.

#### 1.2 三类用户画像

Each persona includes:

- 角色
- 核心目标
- 对现有工具最大的不满
- 让他们愿意切换的那一个功能

#### 1.3 可行性边界

Use two columns:

| 在范围内（及原因） | 明确排除在外（及原因） |
|---|---|

Be honest about browser, platform, model, mobile, export, file-system, and account limits. Do not promise impossible delivery.

#### 1.4 约束分层

Classify the product requirements into three buckets:

| 硬约束 | 推荐默认 | 发挥空间 |
|---|---|---|

- `硬约束`: the implementation must not violate these, such as safety, privacy, legal boundaries, P0 workflow, platform limits, or critical data semantics.
- `推荐默认`: the best default decision for most implementations; the implementing AI may adjust if project evidence points elsewhere.
- `发挥空间`: areas where the implementing AI should improve taste, details, micro-interactions, visuals, motion, empty states, copy, or architecture quality without changing the product contract.

This table prevents over-constraining the AI while protecting the product's core.

### 第二章：整体布局与导航

Draw the top-level page layout with ASCII boxes. Mark each region with its name and approximate size or proportion. Show hierarchy, not just visual placement.

Box format:

```text
+--------------------------------------------------+
|  区域名称（宽 x 高 或 百分比比例）               |
|  +--------------------+  +--------------------+  |
|  |  子区域 A          |  |  子区域 B          |  |
|  +--------------------+  +--------------------+  |
+--------------------------------------------------+
```

Flow format:

```text
用户操作
    |
    v
系统响应
    |
    +-- 条件 A --> 结果 A
    |
    +-- 条件 B --> 结果 B
```

Hierarchy format:

```text
根节点
+-- 子节点 A
|   +-- 孙节点 A1
|   +-- 孙节点 A2
+-- 子节点 B
```

After the diagram, explain briefly why the layout fits this product and user type.

### 第三章：核心模块详细设计

Create one subsection for each major module. The number of modules depends on the product, not the template.

Use:

```text
### 第 3.x 节 模块名称
```

Each module must include:

#### a) ASCII 图

Show the module UI structure with realistic representative content, not placeholders. Include default, active, empty, and error states when relevant.

#### b) 交互流程

Use arrow diagrams. Cover the normal path and at least two failure paths.

#### c) 状态清单

List every meaningful state. Each state includes:

- 名称
- 触发条件
- 视觉标识
- 退出条件

#### d) 依赖关系

Show what data this module reads, what it writes, and the direction of data flow.

#### e) 待决问题

List 1-3 real unresolved product decisions that affect implementation. Do not invent fake questions. If all clear, write `无`.

### 第四章：超越竞品的差异化功能

For each feature that materially exceeds competitor baseline, create:

```text
### 第 4.x 节 功能名称
```

Write four parts:

1. 竞品为何没有这个功能：explain structural reasons such as historical architecture, business model, platform limits, or organizational blind spots.
2. 本产品如何实现：explain concrete technical or product approach. If multiple approaches exist, weigh them and recommend one.
3. 交互流程：use an ASCII flow diagram showing end-to-end user experience.
4. 风险与应对：name what can fail and the fallback plan.

If facts about competitors were not verified, label the reasoning as `基于公开信息的推断` or `此处未验证`. Do not present guesses as facts.

### 第五章：数据模型

Define core data structures with JSON plus inline `//` comments.

Rules:

- every top-level object includes `"version"`
- every field has a `//` comment explaining purpose and valid range
- required fields include `// 必填`
- default values include `// 默认值: xxx`
- nesting depth does not exceed 4 levels

After the JSON, briefly explain the core design decisions: why this structure, what tradeoffs were made, and what was intentionally excluded.

### 第六章：技术架构

Draw a layered architecture diagram in ASCII. Each layer must state responsibility, not only a name.

Then provide a dependency table:

| 库名 | 用途 | 为何优于替代方案 | 大致包体积 |
|---|---|---|---|

Only list libraries with a clear reason. If package size is unknown, write `未知`. Do not guess.

After the table, explain the biggest architecture risk and how to respond.

Also add a short `可替换技术原则` paragraph:

- state the recommended stack or library
- name acceptable substitutes if the existing project already uses them
- identify the invariants that must not change

Example:

```text
推荐 PixiJS；如果项目已有 Phaser，可用 Phaser；如果只是 MVP，可先 Canvas 2D。
不可变的是：输入、物理、渲染分层，物理 tick 不依赖渲染帧率。
```

### 第七章：交互细节

Include:

#### 7.1 键盘快捷键

Table: 操作 | 快捷键 | 备注

Group by category. Only list non-obvious shortcuts or shortcuts that differ from platform convention.

#### 7.2 右键菜单与上下文菜单

For each context, show the menu structure with ASCII.

#### 7.3 空状态

For each major view, state what users see and what the CTA is.

#### 7.4 错误状态

List the five most likely errors. Each includes:

触发条件 | 用户可见的提示信息 | 恢复操作

#### 7.5 加载状态

State which operations need loading indicators, what indicator type is used, and below what latency threshold the indicator is not shown, for example `< 200ms`.

### 第八章：导出与输出系统

Include:

#### 8.1 支持的输出格式

Table: 格式 | 使用场景 | 质量选项 | 备注

#### 8.2 输出文件结构

Show a typical export package directory tree with real filenames, not placeholders.

#### 8.3 批量处理流程

Use an ASCII flow chart to show how multiple items are processed. Mark what can run in parallel and what cannot.

If the product does not export files, redefine "output" as the product's final artifact, share target, report, saved state, API response, or published result.

### 第九章：开发优先级

Use exactly four tiers:

- P0 - 没有这个，产品根本无法使用。交付标准：功能可用，不需要完美。
- P1 - 没有这个，用户第一次体验后不会回来。交付标准：功能完整，体验有连续性。
- P2 - 有了这个，用户会把产品推荐给别人。交付标准：稳定且有辨识度。
- P3 - 有了这个，一部分用户会付费或强烈倡导。交付标准：精致且有完整文档。

Prioritize by impact on user behavior, not implementation difficulty.

### 第十章：性能指标

Every metric must use a concrete number and measurement method.

Format:

| 指标名称 | 目标值 | 测量方法 | 劣化阈值 |
|---|---:|---|---:|

The degradation threshold is the point where product experience visibly worsens, not the crash point.

Do not use vague performance words as a substitute for numbers. Replace them with milliseconds, frame rate, latency, byte size, item count, records, users, requests, export time, or error rate.

### 第十一章：开发者交接说明

Write directly to the implementing AI coding assistant using second person `你`.

Include:

#### a) 实现顺序建议

State which module to build first, why, and what it unlocks.

#### b) 最可能导致返工的三个决策

For each decision:

- 决策是什么
- 安全的默认选择是什么
- 什么信号提示你需要改变方向

#### c) 哪里要严格，哪里可以灵活

Mark each major chapter as `约束` or `建议` and explain why.

#### d) 已知的未知项

List unresolved issues the implementer will encounter. If the document is incomplete, say so. Include at least one honest unknown unless the user supplied unusually complete requirements.

#### e) 验收剧本

Write 3-5 implementation acceptance scripts. Each script should be a realistic user path or verification path the implementing AI can run manually or with tools.

Format:

```text
验收剧本 1：在 [设备/环境] 打开 [入口]，执行 [动作]，应看到 [结果]，并用 [证据] 验证。
```

Prefer executable or observable evidence: screenshots, logs, local storage, exported files, browser console, simulator, network response, or test commands.

## Generation Rules

1. Depth follows importance, not chapter order.
2. ASCII diagrams must include realistic labels, sample content, and actual button/menu text.
3. Make product decisions instead of deferring them.
4. Separate product constraints from implementation details.
5. If something is unclear, write `此处未解决：[具体问题]` and continue.
6. The document must serve both humans and AI coding assistants.
7. Constraints should protect the product; they should not remove useful implementation creativity.
8. Use `超预期机会` for product delight, not feature bloat.
9. When the user provides URLs, current competitors, package choices, API behavior, platform support, legal/rights claims, or pricing facts, verify them when possible. If not verified, say so.
