# Step 2: 获取题目信息

## 目标

根据输入来源获取题目信息（PID、标题、题面内容）。

## 来源类型

| 类型 | 处理 |
|------|------|
| URL | urlgo 访问页面，snapshot 获取内容 |
| 题号 | 直接匹配 PID 格式 |
| 文件 | 解析文件提取题目信息 |
| 文本 | 解析用户给出的文本 |

## PID 提取

| 平台 | URL 格式 | PID 规则 |
|------|---------|---------|
| AtCoder | `/contests/abc451/tasks/abc451_a` | `abc451a` |
| Codeforces | `/contest/71/problem/A` | `cf71a` |
| LeetCode | `/problems/two-sum` | `lc1` |
| Luogu | `/problem/P1001` | `p1001` |

无法提取时 PID 填 `null`。

## 下一步

成功 → `03-gesp.md`

失败 → 询问用户其他来源
