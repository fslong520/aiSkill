# Step 0: 检测输入类型

## 目标

判断输入是 URL、文件路径还是直接文本，单题还是多题。

## ⚠️ 比赛搬运铁律

如果检测到是比赛 URL（如 `/contests/abc454`）：

1. **必须先读取 steps/contest/01-list.md** 创建题面汇总文件
2. **必须逐题翻译追加写入汇总文件**
3. **禁止跳过汇总文件直接逐题搬运**
4. **禁止从对话上下文记忆题面**

## 输入类型

| 类型 | 判断条件 |
|------|---------|
| URL | 以 `http://` 或 `https://` 开头 |
| 文件路径 | 以 `/` 或 `./` 或 `~/` 开头 |
| 直接文本 | 既不是 URL 也不是文件路径 |

## URL 跳转

| URL 特征 | 下一步 |
|---------|--------|
| 结尾是 `/tasks` 或 `/problems` | `contest/01-list.md` |
| 其他 | `02-get-info.md` |

## 文件/文本跳转

| 内容特征 | 下一步 |
|---------|--------|
| 多道题（多个 `---` 或多题号） | `contest/03-move.md` |
| 单道题 | `01-init.md` → `02-get-info.md` |

## 多题判断

```python
def is_multi_problem(content):
    if content.count("---") >= 2:
        return True
    markers = ["## A -", "## B -", "## C -", "## D -", "## E -"]
    if sum(1 for m in markers if m in content) >= 2:
        return True
    return False
```
