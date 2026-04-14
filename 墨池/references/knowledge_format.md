# 知识点索引格式规范

> 文件路径：`db/knowledge_index.txt`

## KV 格式说明

使用简单 KV 格式，每个知识点一个块：

```
=== 知识点名称 ===
id: 分类_编号
category: 分类
tags: 标签1,标签2
summary: 一句话摘要
related: 
file: knowledge/分类/知识点名称.md
learning_count: N
mastery: 了解/理解/熟练/精通
first_learned: YYYY-MM-DD
last_learned: YYYY-MM-DD
expires_at: YYYY-MM-DD
status: fresh/aging/stale/permanent
source: 对话学习
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `=== 名称 ===` | ✅ | 知识点标题，唯一标识 |
| `id` | ✅ | 分类缩写_编号，如 `算法_001` |
| `category` | ✅ | 所属分类，决定过期周期 |
| `tags` | ✅ | 2-5 个标签，逗号分隔 |
| `summary` | ✅ | 一句话摘要（不超过 50 字） |
| `related` | ❌ | 关联知识点，逗号分隔 |
| `file` | ✅ | 详情 Markdown 文件路径 |
| `learning_count` | ✅ | 学习次数，每次 +1 |
| `mastery` | ✅ | 了解/理解/熟练/精通 |
| `first_learned` | ✅ | 首次学习日期 |
| `last_learned` | ✅ | 最后学习日期 |
| `expires_at` | ✅ | 过期日期（AI 计算） |
| `status` | ✅ | fresh/aging/stale/permanent |
| `source` | ✅ | 来源：对话学习/任务分析/主动学习 |

## 分类编号规则

| 分类 | 编号前缀 | 示例 |
|------|---------|------|
| 算法数据结构 | `算法_` | `算法_001` |
| 信竞教学 | `信竞_` | `信竞_001` |
| 工具使用 | `工具_` | `工具_001` |
| 计算机基础 | `计算机_` | `计算机_001` |
| 数学 | `数学_` | `数学_001` |
| 生活健康 | `生活_` | `生活_001` |

## 示例

```
=== 差分 ===
id: 算法_001
category: 算法数据结构
tags: 前缀和,区间修改,O1操作
summary: 前缀和的逆运算，用于高效处理区间修改问题
related: 前缀和,树状数组,线段树
file: knowledge/算法数据结构/差分.md
learning_count: 3
mastery: 熟练
first_learned: 2026-03-25
last_learned: 2026-03-27
expires_at: 2027-03-25
status: fresh
source: 用户提问

=== ClawHub技能发布 ===
id: 工具_002
category: 工具使用
tags: ClawHub,技能发布,CLI
summary: 使用clawhub CLI发布技能，tags用英文slug用小写
file: knowledge/工具使用/ClawHub技能发布.md
learning_count: 1
mastery: 了解
first_learned: 2026-03-29
last_learned: 2026-03-29
expires_at: 2026-05-29
status: aging
source: 对话学习
```

## AI 操作要点

1. **添加知识点**：用 `edit_file` append 到文件末尾
2. **更新知识点**：用 `edit_file` 替换整个块
3. **查询知识点**：用 `read_file` 读取，AI 自己解析
4. **删除知识点**：用 `edit_file` 删除整个块（存档后）