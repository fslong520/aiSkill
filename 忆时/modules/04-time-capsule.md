# 模块 04 - 时间胶囊管理

## 概念

时间胶囊允许将当前时刻的记忆封存，设定一个未来的解锁日期。
到期后可以自动或手动解封，重温当时的记忆和情绪。

## 封存胶囊

```bash
# 封存一个胶囊，30天后解锁（默认）
python3 scripts/memory_core.py capsule lock --summary "今日感悟"

# 封存并指定解锁日期
python3 scripts/memory_core.py capsule lock --unlock-at "2026-12-31" --summary "年度回顾" --content "今天我和AI讨论了关于未来的思考…" --keywords "未来,思考,人生"
```

**关键字段**:

| 参数 | 必填 | 说明 |
|------|------|------|
| --summary | 否 | 摘要，用于列表预览 |
| --content | 否 | 胶囊的详细记忆内容 |
| --keywords | 否 | 关键字 |
| --unlock-at | 否 | 解锁日期 YYYY-MM-DD，默认30天后 |

## 查看胶囊

```bash
python3 scripts/memory_core.py capsule list
```

输出示例:
```
时间胶囊 (3 个)
ID: xxx-xxx
创建: 2025-06-15 | 解锁: 2025-12-31 | 状态: 剩余 205 天
内容: 时间胶囊 - 创建于 2025-06-15, 解锁日期: 2025-12-31
```

## 检查到期

```bash
python3 scripts/memory_core.py capsule check-expired
```

主动模式下每次触发时应运行此命令。

## 解封胶囊

```bash
python3 scripts/memory_core.py capsule unseal --capsule-id <ID>
```

- 如果胶囊已到期 → 直接解封
- 如果尚未到期 → 警告用户并需要确认
- 解封后该记忆变为普通记忆，可以正常检索

## 解封回忆重现

解封时，生成回忆回顾:

> 🎋 时光倒流! 你于 X 天前封存了这段记忆:
>
> [capsule content]
>
> 封存时的心情: 🟠 兴奋
> 关键字: …
>
> 这段记忆已被解封，现在可以随时检索了。
