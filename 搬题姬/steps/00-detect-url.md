# Step 0: 检测输入类型

## 🎯 目标

判断用户输入是**URL地址**、**文件路径**还是**直接文本**，并判断是单题还是多题。

---

## 🔍 输入类型判断

| 类型 | 判断条件 | 示例 |
|------|---------|------|
| **URL地址** | 以 `http://` 或 `https://` 开头 | `https://atcoder.jp/contests/abc123/tasks` |
| **文件路径** | 以 `/` 或 `./` 或 `~/` 开头，或包含文件扩展名 | `/home/user/problem.md`、`./题目.txt` |
| **直接文本** | 既不是URL也不是文件路径 | 用户直接给出的题面描述 |

---

## 📊 判断结果与下一步跳转

### ✅ URL 地址

| URL 特征 | 类型 | 👉 下一步 |
|---------|------|----------|
| 结尾是 `/tasks` 或 `/problems` | 比赛地址 | `steps/contest/01-list.md` |
| 其他格式 | 单题地址 | `steps/02-get-info.md` |

---

### ✅ 文件路径

**先读取文件内容，再判断是单题还是多题**：

**判断方法**：
1. 检查是否包含多个 `---` 分割线
2. 检查是否包含多个题号标记（如 `## A -`、`## B -` 等）
3. 检查是否是比赛题面汇总格式（`<div class="water">` 包裹）

| 文件内容特征 | 类型 | 👉 下一步 |
|-------------|------|----------|
| 包含多道题（分割线、多题号） | 多题文件 | `steps/contest/03-move.md`（逐题搬运） |
| 单道题面 | 单题文件 | `steps/01-init.md` → `steps/02-get-info.md` |

---

### ✅ 直接文本

**判断方法**：
1. 检查是否包含多个题目分隔
2. 检查是否包含多个题号标记

| 文本特征 | 类型 | 👉 下一步 |
|---------|------|----------|
| 包含多道题 | 多题文本 | `steps/contest/03-move.md`（逐题搬运） |
| 单道题面 | 单题文本 | `steps/01-init.md` → `steps/02-get-info.md` |

---

## 🔧 流程图

```
用户输入
    ↓
┌───判断输入类型───┐
│                  │
├─ URL地址 ────────┼─ 比赛地址 → Contest Step 1（获取列表）
│                  │  单题地址 → Step 2（获取信息）
│                  │
├─ 文件路径 ───────┼─ read_file 读取内容
│                  │  ↓
│                  │  ┌─ 多题 → Contest Step 3（逐题搬运）
│                  │  └─ 单题 → Step 1 → Step 2
│                  │
├─ 直接文本 ───────┼─ 解析文本
│                  │  ↓
│                  │  ┌─ 多题 → Contest Step 3（逐题搬运）
│                  │  └─ 单题 → Step 1 → Step 2
│                  │
└──────────────────┘
```

---

## 🔧 多题判断伪代码

```python
def is_multi_problem(content):
    # 判断是否包含多道题
    
    # 方法1：检查分割线数量（超过1个分割线 = 多题）
    if content.count("---") >= 2:
        return True
    
    # 方法2：检查题号标记（A、B、C... 多个题号）
    problem_markers = ["## A -", "## B -", "## C -", "## D -", "## E -"]
    if sum(1 for m in problem_markers if m in content) >= 2:
        return True
    
    # 方法3：检查比赛格式包裹
    if "<div class=\"water\">" in content and content.count("---") >= 2:
        return True
    
    return False
```