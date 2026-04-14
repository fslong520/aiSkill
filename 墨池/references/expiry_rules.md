# 知识过期规则

> AI 自己判断，不用 Python 脚本！

## 过期周期配置

| 分类 | 过期周期 | 原因 |
|------|---------|------|
| 工具使用 | 60 天 | 工具/API 可能随版本变化 |
| 计算机基础 | 90 天 | 技术知识中等周期 |
| 算法数据结构 | 365 天 | 理论知识长期有效 |
| 信竞教学 | 365 天 | 教学知识长期有效 |
| 数学 | 永不过期 | 数学原理不变 |
| 生活健康 | 365 天 | 生活常识长期有效 |
| 测试 | 30 天 | 测试数据短期 |
| 其他 | 90 天 | 默认周期 |

## 状态定义

| 状态 | 英文 | 说明 | 建议操作 |
|------|------|------|---------|
| 🟢 新鲜 | `fresh` | 刚学习或刚验证 | 无需处理 |
| 🟡 老化 | `aging` | 超过半周期 | 建议提前验证 |
| 🔴 需验证 | `stale` | 已过期 | 必须验证 |
| ⚫ 存档 | `archived` | 验证失败 | 等待删除 |
| ⭐ 永不过期 | `permanent` | 基础理论 | 无需处理 |

## 状态流转图

```
🟢 fresh ──(时间流逝)──→ 🟡 aging(半周期) ──→ 🔴 stale(过期)
                              │                    │
                              │                    ├─(验证成功)──→ 🟢 fresh
                              │                    │
                              │                    └─(验证失败)──→ ⚫ archived
                              │
                              └─(用户标记)──→ ⭐ permanent
```

## AI 判断流程

### 判断知识状态

```
1. read_file knowledge_index.txt
2. 遍历每个知识点：
   a. 获取 category 和 last_learned
   b. 计算：当前日期 - last_learned = 已过天数
   c. 查过期周期表，获取该分类的周期
   d. 判断状态：
      - 已过天数 < 呈周期一半 → fresh
      - 已过天数 < 周期 → aging  
      - 已过天数 ≥ 周期 → stale
      - expires_at = 'never' → permanent
3. 输出报告或更新状态
```

### 验证过期知识

```
用户说：/墨池 验证 差分

AI 执行：
1. read_file knowledge_index.txt，找到"差分"
2. 向用户提问："差分知识是否仍有效？内容有无变化？"
3. 用户确认后：
   - 有效 → edit_file 更新 expires_at（重新计算）、status=fresh
   - 无效 → edit_file 更新 status=archived、archived_at=今天
4. append learning_log.txt 记录验证事件
```

## 计算过期日期

**AI 自己计算，写入知识点时自动填入 `expires_at`**

```
过期日期 = last_learned + 过期周期天数

示例：
- last_learned: 2026-03-29
- category: 工具使用（周期 60 天）
- expires_at: 2026-05-29（AI 计算）
```

## 存档清理规则

存档超过 30 天的知识可以删除：

```
1. 遍历 archived 状态的知识点
2. 检查 archived_at 字段
3. 当前日期 - archived_at ≥ 30 天 → 删除
4. 同时删除对应的 knowledge/xxx.md 文件
```