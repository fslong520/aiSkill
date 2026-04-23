---
name: ojimport
description: 从 OJ 平台搬运题目，生成标准化题目文件包
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - BrowserUse

metadata:
  trigger: OJ题目、搬题、算法题搬运、竞赛题目、AtCoder、Codeforces、GESP、题目导入
---

## Keywords

OJ题目、搬题、算法题搬运、AtCoder、Codeforces、GESP

## Summary

从 OJ 平台搬运题目，生成标准化文件包（题面+标程+数据）。

## Strategy

### 单题搬运

1. 读取 steps/00-detect-url.md → 检测类型
2. 初始化：cp -r question work
3. 获取题面：urlgo 访问 → snapshot → 解析（urlgo不可用时用 BrowserUse/WebFetch）
4. 读取 steps/03-gesp.md → 判定等级
5. 读取 steps/04-problem.md → 生成题面
6. 读取 steps/05-config.md → 写配置
7. 实现标程 std.cpp
8. 读取 steps/07-testdata.md → 生成数据
9. 打包：zip -r problem.zip work

### ⚠️ 比赛搬运（必须先创建题面汇总文件）

1. 读取 steps/contest/01-list.md → 创建题面汇总文件 `{contest_id}.md`
2. 读取 steps/contest/02-problem.md → **逐题翻译并追加写入汇总文件**
3. 读取 steps/contest/03-move.md → **从文件读取题面**，逐题生成完整题包

## AVOID

- AVOID 不读步骤文档就执行
- AVOID 不按模板格式
- AVOID 测试数据只写样例
- AVOID GESP等级乱判
- AVOID 忘清理 work 目录
- AVOID PID 格式错误（用小写 abc451a）
- ⚠️ **AVOID 比赛搬运时跳过题面汇总文件，直接逐题搬运**
- ⚠️ **AVOID 从对话上下文记忆题面，必须从文件读取**

---

## 入口

读取 steps/00-detect-url.md
