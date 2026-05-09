# Step 1: 准备阶段

## 目标

判断输入类型，获取题面信息，确定是单题还是多题。

## 输入类型判断

| 类型 | 判断条件 | 下一步 |
|------|---------|--------|
| 比赛 URL（`/contests/xxx/tasks`） | 多题 | `steps/03-contest.md` |
| 单题 URL（`/contests/xxx/tasks/xxx_a`） | 单题 | `steps/02-single.md` |
| 题面文件（`.md`） | 视内容 | 检测是否为多题 |
| 直接文本 | 单题 | `steps/02-single.md` |
| 用户指定标程路径 | 附代码 | 融入精讲 |

## 题面获取

1. **URL 输入**：使用 urlgo 打开页面 → snapshot 获取内容 → 解析题面
2. **文件输入**：Read 工具读取
3. **文本输入**：直接使用

## 标程获取

若用户在请求中指定了代码文件路径（如 `/path/to/a.cpp`），需读取该文件，在「代码逐行精讲」节中使用。

## 多题判断

```python
def is_multi(content):
    markers = ["## A -", "## B -", "## C -", "## D -", "## E -"]
    return sum(1 for m in markers if m in content) >= 2
```

## 下一步

- 单题 → `steps/02-single.md`
- 多题 → `steps/03-contest.md`
