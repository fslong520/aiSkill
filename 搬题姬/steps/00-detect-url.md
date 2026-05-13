# Step 0: 辨输入类

## 目标

辨输入为 URL、文件路径或直文本，单题或赛题。

## ⚠️ 比赛搬运铁律

若测得为比赛 URL（如 `/contests/abc454`）：

1. **必先读 steps/contest/01-list.md** 创题面汇总文件
2. **必逐题译之追加写入汇总文件**
3. **禁跳过汇总文件直逐题搬运**
4. **禁自对话上下文记忆题面**

## 输入类型

| 类型 | 判断条件 |
|------|---------|
| URL | 以 `http://` 或 `https://` 起 |
| 文件路径 | 以 `/` 或 `./` 或 `~/` 起 |
| 直文本 | 非URL亦非文件路径 |

## URL 跳转

| URL 特征 | 下一步 |
|---------|--------|
| 尾为 `/tasks` 或 `/problems` | `contest/01-list.md` |
| 其他 | `02-get-info.md` |

## 文件/文本跳转

| 内容特征 | 下一步 |
|---------|--------|
| 多道题（多个 `---` 或多题号） | `contest/03-move.md` |
| 单道题 | `01-init.md` → `02-get-info.md` |

## 多题判法

```python
def is_multi_problem(content):
    if content.count("---") >= 2:
        return True
    markers = ["## A -", "## B -", "## C -", "## D -", "## E -"]
    if sum(1 for m in markers if m in content) >= 2:
        return True
    return False
```
