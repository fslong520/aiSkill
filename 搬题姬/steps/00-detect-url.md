# Step 0: 检测输入类型

## 目标

判断输入是 URL、文件路径还是直接文本，单题还是多题。

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
