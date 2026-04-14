# 用户画像格式规范

> 文件路径：`db/user_profile.txt`

## KV 格式说明

```
=== identity ===
primary_role: 主身份
secondary_roles: 次身份1,次身份2
confidence: 0.XX

=== action:<type> ===
count: N
topics: 主题1,主题2,主题3
```

## 字段说明

### identity 块

| 字段 | 说明 |
|------|------|
| `primary_role` | 推断的主身份（如：信奥竞赛教练） |
| `secondary_roles` | 次身份列表（如：算法学习者,C++开发者） |
| `confidence` | 推断置信度（0.0-1.0） |

### action 块

| 字段 | 说明 |
|------|------|
| `=== action:<type> ===` | 行为类型块标题 |
| `count` | 该行为发生次数 |
| `topics` | 该行为涉及的主题（逗号分隔） |

## 行为类型枚举

| action 类型 | 说明 | 触发场景 |
|-------------|------|---------|
| `ask_concept` | 询问概念 | 用户问"什么是..." |
| `ask_method` | 询问方法 | 用户问"怎么做..." |
| `write_code` | 写代码 | 用户让 AI 写代码 |
| `explain_code` | 解释代码 | 用户让 AI 解释代码 |
| `搬题` | 搬题行为 | 用户使用搬题姬 |
| `算法讲解` | 算法讲解 | AI 讲解算法给用户 |

## 示例

```
=== identity ===
primary_role: 信奥竞赛教练
secondary_roles: 算法学习者,C++开发者
confidence: 0.85

=== action:ask_concept ===
count: 15
topics: 前缀和,差分,树状数组

=== action:搬题 ===
count: 8
topics: ABC450A,ABC450B

=== action:算法讲解 ===
count: 5
topics: 快速排序,二分查找
```

## AI 操作要点

1. **初始化画像**：用户首次提问时创建 `identity` 块
2. **更新行为统计**：每次触发墨池时，更新对应 `action` 块的 `count` 和 `topics`
3. **推断身份**：根据行为分布推断用户身份，更新 `identity` 块
4. **置信度调整**：行为数据越多，置信度越高