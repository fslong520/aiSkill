# Step 2: 获取题目信息

## 🎯 目标

根据输入来源获取题目信息（PID、标题、题面内容）。

---

## 🔍 来源类型判断

| 来源类型 | 处理方式 |
|---------|---------|
| **URL链接** | 使用 urlgo 技能访问页面，snapshot 获取内容 |
| **题号** | 直接匹配 PID 格式 |
| **文件内容** | 解析文件提取题目信息 |
| **直接文本** | 解析用户给出的文本 |

---

## 🔧 PID 提取规则

| 平台 | URL 格式 | PID 规则 | 示例 |
|------|---------|---------|------|
| AtCoder | `/contests/abc451/tasks/abc451_a` | `{contest}_{problem}` | `abc451a` |
| Codeforces | `/contest/71/problem/A` | `cf{contest}{problem}` | `cf71a` |
| LeetCode | `/problems/two-sum` | `lc{题号}` | `lc1` |
| Luogu | `/problem/P1001` | `p{题号}` | `p1001` |

**无法提取题号时**：PID 填 `null`（YAML null 值，不是字符串"null"）

---

## 📝 操作场景示例

### 场景A：URL单题

```
用户: 搬运 https://atcoder.jp/contests/abc451/tasks/abc451_a
处理: urlgo访问 → snapshot → 解析题面 → 提取PID: abc451a
```

### 场景B：文件单题

```
用户: 搬运 ./题目.txt
处理: read_file读取 → 解析题面 → 无PID → pid: null
```

### 场景C：直接文本

```
用户: [直接给出题面描述]
处理: 解析文本 → 提取题目描述、数据范围、样例
```

---

## 📊 下一步跳转

### ✅ 信息获取成功

**获得信息**：PID、标题、题面内容、数据范围、样例

**👉 下一步**：读取 `steps/03-gesp.md` 进行 GESP 难度判定

---

### ❌ 信息获取失败

**处理**：
1. URL 无法访问 → 询问用户是否提供其他来源
2. 题面解析失败 → 手动询问用户关键信息