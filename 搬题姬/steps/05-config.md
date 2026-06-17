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
score: 1200
tag:
  - "字符串"
  - "模拟"
  - "GESP 1级"
```

## 注

1. pid 按规而判，非无脑填 null
2. title 必用 `中文(英文)` 格式
3. **score 分数必填**：
   - 范围 800~3500（与 Codeforces Rating 对齐）
   - 按 Step 03-gesp.md「第三步：定分」规则计算
   - 比赛中已知分数直接采用（如 CF 的 Rating）
   - 原创题由出题人设定
4. **tag 必含多项**：
   - 1~3 个**知识点标签**（如"字符串""动态规划""图论""贪心""模拟""前缀和"等，贵精不贵多）
   - 1 个**等级标签**（`GESP X级`，注意 X 与数字间有空格）
   - **禁**只写一个等级标签完事

## 测试数据分组配置

测试数据之分组（HydroOJ subtask）在 `{WORK_DIR}/testdata/config.yaml` 中配，
详见 **Step 07-testdata.md → 配置文件（HydroOJ subtask 格式）**。

## 测试数据分组配置

测试数据的分组（HydroOJ subtask）在 `testdata/config.yaml` 中配置，
详见 **Step 07-testdata.md → 配置文件（HydroOJ subtask 格式）**。

## 下一步

成 → `06-std.md`
