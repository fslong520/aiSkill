# Output Quality

Run this checklist before returning a PRD.

## Required Self-Check

- Every required chapter from one to eleven appears in order.
- `AI 速读卡` appears before the chapters and is short enough to skim.
- Important requirements are separated into `硬约束`, `推荐默认`, and `发挥空间`.
- Every major module has an ASCII diagram with realistic content.
- Module flows include a normal path and at least two failure paths.
- Each module has a state list with trigger condition, visual marker, and exit condition.
- Every differentiation feature explains structural competitor reasons.
- `超预期机会` contains 2-4 product moments that can improve the implementation without bloating P0.
- Every technical selection has a reason; unknown package size is written as `未知`.
- Technical architecture includes `可替换技术原则` so the implementer can adapt to the existing codebase.
- Every performance metric has a number, measurement method, and degradation threshold.
- Data model JSON has comments for every field and a top-level `"version"`.
- P0 is the true smallest usable product, not a wishlist.
- Chapter 11 contains at least one honest known unknown unless the user supplied complete constraints.
- Chapter 11 includes 3-5 `验收剧本` with observable evidence.
- No unresolved placeholders remain.
- No vague performance claim is used where a number is required.

## Common Failure Patterns

### Placeholder-Looking Text

Bad:

```text
按钮 A
[产品名]
此处展示列表
待补充
```

Good:

```text
开始 12 分钟专注复习
WordPulse
今日待复习：18 个词
此处未解决：是否允许用户导入版权词库
```

### Fake Competitor Reason

Bad:

```text
竞品没有这个功能，因为他们没有想到。
```

Good:

```text
竞品以课程售卖为核心，进度和推荐被绑定到固定课包，因此不会优先支持用户自建词库的实时弱项复习。
```

### Vague Performance

Bad:

```text
页面要快，交互要流畅，导出要轻量。
```

Good:

```text
首屏可交互时间 | <= 1200ms | Lighthouse mobile 4G profile | > 2200ms
拖拽延迟 | <= 50ms | Chrome Performance 记录 pointermove 到 paint | > 120ms
导出包大小 | <= 8MB | 生成后读取 zip 文件大小 | > 20MB
```

### Overbuilt P0

Bad P0 includes:

- social feed
- paid plan
- team workspace
- template marketplace
- multi-language content library

Good P0 includes only the shortest loop that proves the product can be used.

### Over-Constrained Implementation

Bad:

```text
必须使用 Next.js、Tailwind、Postgres、Vercel、shadcn，并严格按这个文件结构实现。
```

when the product could be built well with the existing stack.

Good:

```text
推荐默认：React + Canvas 2D。
可替换技术原则：如果项目已有 Phaser 或 PixiJS，可以沿用；不可变的是输入、物理、渲染分层和 50ms 内的触控反馈。
```

### Missing Delight

Bad:

```text
功能完成即可。
```

Good:

```text
超预期机会：Game Over 后生成一张复古街机风分数卡；不进入 P0，但实现成本低时优先做。
```

### Dishonest Unknowns

Bad:

```text
已知的未知项：无。
```

when the input was only one sentence.

Good:

```text
已知的未知项：此处未解决：是否需要账号同步；默认先用本地存储，因为 P0 要先验证学习循环。
```

## Final Repair Rules

If the PRD fails the self-check, repair the document before returning it. Do not tell the user the PRD failed unless you cannot fix it without a risky product decision.

If a fact cannot be known from the prompt and cannot be verified, do one of three things:

1. choose a safe default and say why
2. write `未知`
3. write `此处未解决：[具体问题]`

Do not use confident filler.

If the PRD feels too prescriptive, convert low-risk instructions into `推荐默认` or `发挥空间`. Preserve only the real product constraints as `硬约束`.
