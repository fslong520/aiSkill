# 模块 03 - 主动模式（定时触发回忆整理）

## 触发方式

结合定时任务/cron周期性执行:

```bash
# 主动回忆整理入口脚本
python3 scripts/memory_core.py capsule check-expired && \
python3 scripts/memory_core.py forget --low-freq 1 --auto && \
python3 scripts/memory_core.py stats
```

## 主动执行流程

### 1. 检查到期时间胶囊

```bash
python3 scripts/memory_core.py capsule check-expired
```

- 如果存在到期胶囊 → **生成回忆回顾**
- 解封胶囊内容，向用户推送回顾
- 格式示例:

> 🎋 记忆胶囊解封提醒
> 你于 2025-03-15 封存了一个胶囊，今天是解锁日！
>
> 封存内容: "今天和AI讨论了一个关于…"
> 封存时的心情: 🟠 兴奋
>
> 打开看看吗？

### 2. 自动发现记忆关联

分析现有记忆，寻找隐藏关联:

- 检索每条记忆，查看 `recall --expand` 的结果
- 如果发现新的强关联（关联分数 > 0.7）
- 主动向用户报告:

> "我注意到你关于 A 和 B 的记忆似乎存在一些联系…"

### 3. 遗忘曲线处理

低优先级记忆自动归档:

```bash
python3 scripts/memory_core.py forget --before "2025-01-01" --low-freq 1 --auto
```

- 将低频、低 recall 的旧记忆标记为 archived
- 不删除，只是降低检索优先级
- 保留高情绪记忆不归档

### 4. 记忆整理报告

生成统计摘要:

```bash
python3 scripts/memory_core.py stats
```

向用户报告:
- 总记忆数
- 本周新增记忆
- 到期解除的胶囊数
- 归档的记忆数

## 建议定时频率

| 任务 | 频率 | 说明 |
|------|------|------|
| 胶囊检查 | 每天一次 | 检查到期的时间胶囊 |
| 遗忘归档 | 每周一次 | 归档低频旧记忆 |
| 关联发现 | 每次对话后 | 对话结束时自动发现新关联 |
| 统计报告 | 每周一次 | 生成记忆整理报告 |

## 对话结束语自动触发

每当用户结束一次较长的对话，可以主动:

1. 提取对话中的重点记忆
2. 自动存储到 Chroma
3. 检查是否有胶囊到期
