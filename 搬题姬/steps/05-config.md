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

单题搬运且无定来源：`pid: "null"`

## 配置格式

```yaml
pid: "abc453a"
title: "移除前导o(Trimo)"
score:  # AI 判定（03-gesp.md「第四步：CF 档位判定」，逐项判四维锁定档位）800~3500
source: "https://atcoder.jp/contests/abc453/tasks/abc453_a"
tag:
  - "字符串"
  - "模拟"
  - "GESP 1级"
```

## 注

1. pid 按规而判，非无脑填 null
2. title 必用 `中文(英文)` 格式
3. **source 出处必填**：
   - **URL 来源**：填原题 URL（必填），与题面出处行一致；OJ 于题目页渲染为可点击「原题出处」链接
   - **文件/文本来源**：填来源说明（如文件名），无明确出处则 `null`
   - **原创题**（pid 为 null）：`source: null`
4. **score 分数必填（按 03-gesp.md 第四步档位判定）**：
   - 范围 800~3500（与 Codeforces Rating 对齐）
   - 按 **03-gesp.md「第四步：CF 档位判定」** 判定——**逐项判四维（思维拐点/算法门槛/数据规模/实现细节）锁定档位，禁直接给感觉分、禁查速查表、禁套公式、禁按 GESP 等级/星级映射**
   - **水题给分克制**：零思维量者 ≤900，纯语法直套模板者 800
   - 比赛中已知分数直接采用（如 CF 的 Rating）
   - **禁写死默认值**，必须逐题判定后填入
5. **tag 必含多项**：
   - 1~3 个**知识点标签**（如"字符串""动态规划""图论""贪心""模拟""前缀和""线段树"等，贵精不贵多）
   - 1 个**等级标签**——四级体系其一：`GESP X级` / `CSP-J` / `CSP-S` / `NOI`（按 03-gesp.md 第二步锚定）
     - **GESP 大纲有**该知识点 → 写 `GESP X级`（X 与"级"间有空格）
     - **GESP 大纲无（超纲）** → 循跨体系兜底规则（03-gesp.md 2.5）升到 `CSP-J` / `CSP-S` / `NOI`
   - **禁**只写一个等级标签完事

6. **等级标签必读 03-gesp.md 后填写**：
   - ⚠️ 先读 **`03-gesp.md` → 第二步「定级」**，先查 GESP 大纲（2.1~2.3）；**GESP 无此知识点则查 2.4 跨体系锚定表 + 2.5 兜底规则，升到 CSP-J/CSP-S/NOI**
   - ⚠️ 再读 **`03-gesp.md` → 第四步「CF 档位判定」** 判定 score（水题克制，零思维量 ≤900）
   - **禁凭印象填等级**，背包 DP ≠ 四级递推（背包 ∈ 六级）；线段树 ≠ 五级（∈ 八级/CSP-S）
   - `tag` 中的**等级标签**与 `score` 的判定，二者均以 03-gesp.md 为准，缺一不可

## 测试数据分组配置

测试数据之分组（HydroOJ subtask）在 `{WORK_DIR}/testdata/config.yaml` 中配，
详见 **Step 07-testdata.md → 配置文件（HydroOJ subtask 格式）**。

## 测试数据分组配置

测试数据的分组（HydroOJ subtask）在 `testdata/config.yaml` 中配置，
详见 **Step 07-testdata.md → 配置文件（HydroOJ subtask 格式）**。

## 下一步

成 → `06-std.md`
