# 理论依据

## 论文

From Procedural Skills to Strategy Genes: Towards Experience-Driven Test-Time Evolution

作者：Junjie Wang, Yiming Ren, Haoyang Zhang（清华 × EvoMap）

arXiv: https://arxiv.org/abs/2604.15097

### 核心发现

1. 信息密度：完整文档 ≠ 高控制密度，信号被稀释了
2. Token 实验：Gene（230 token）比 Skill（2500 token）高 3.0pp
3. 结构有效：只有 Strategy 真正起作用，Overview 是最大负贡献
4. 失败经验：最佳形态是独立的「AVOID xxx」语句

---

## 实践文章

《Skill 101：如何写好 Skill》— Henry Li

https://my.feishu.cn/wiki/LWazwBXDUipUZVkYCK2c8JK3nEc

### 原则

1. Skill 是给 AI 看的，不是给人看的
2. 渐进式披露：SKILL.md 只放索引，≤100 行
3. 脚本优先于 prompt，可靠一个数量级
4. Human-in-the-Loop：适当引入交互
5. 持续迭代：用 → 失败 → 改

---

## Gene 四要素

```
keywords  - 触发词
summary   - 一句话
strategy  - 可执行步骤（核心）
AVOID     - 失败经验（高价值）
```

## 负贡献

| 内容 | 处理 |
|------|------|
| Overview | 删除 |
| 冗长背景 | 删除或外置 |
| 为人类可读的材料 | 删除 |
| 重复信息 | 删除 |

## 最佳实践

Token ≤ 300，信号密度 > 80%，Gene 四要素齐全，渐进披露。
