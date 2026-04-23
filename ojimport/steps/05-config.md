# Step 5: 写入配置文件

## 目标

写入 `work/problem.yaml`。

## pid 命名规则

```
用户指定 > 比赛自动命名 > null
```

### 比赛自动命名

格式：`{比赛简称}{场次}{题号}`

| 来源 | 示例 |
|------|------|
| AtCoder ABC | `abc453a` |
| AtCoder ARC | `arc123a` |
| Codeforces | `cf789a` |
| LeetCode | `lc1234` |
| Luogu | `lgP1001` |

### 无比赛信息

单题搬运且无法确定来源：`pid: null`

## 配置格式

```yaml
pid: abc453a
title: "移除前导o(Trimo)"
tag:
  - "GESP一级"
  - "字符串"
```

## 注意

1. pid 按规则确定，不是无脑填 null
2. title 必须用 `中文(英文)` 格式
3. tag 必须包含 `GESPX级`

## 下一步

完成 → `06-std.md`
