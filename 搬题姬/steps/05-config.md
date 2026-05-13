# Step 5: 写配置

## 目标

写入 `{WORK_DIR}/problem.yaml`。

## pid 命名

```
用户指定 > 比赛自命名 > null
```

### 比赛自命名

格式：`{比赛简称}{场次}{题号}`

| 来源 | 例 |
|------|------|
| AtCoder ABC | `abc453a` |
| AtCoder ARC | `arc123a` |
| Codeforces | `cf789a` |
| LeetCode | `lc1234` |
| Luogu | `lgP1001` |

### 无比赛信息

单题搬运且无定来源：`pid: null`

## 配置格式

```yaml
pid: abc453a
title: "移除前导o(Trimo)"
tag:
  - "GESP一级"
  - "字符串"
```

## 注

1. pid 按规而判，非无脑填 null
2. title 必用 `中文(英文)` 格式
3. tag 必含 `GESPX级`

## 测试数据分组配置

测试数据之分组（HydroOJ subtask）在 `{WORK_DIR}/testdata/config.yaml` 中配，
详见 **Step 07-testdata.md → 配置文件（HydroOJ subtask 格式）**。

## 下一步

成 → `06-std.md`
