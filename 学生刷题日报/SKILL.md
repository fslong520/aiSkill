---
name: OJDaily
description: 监控智国OJ学生刷题情况，生成精美的Markdown和HTML日报，支持自定义时间范围
allowed-tools:
  - edgeuse
  - browser_use
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - execute_shell_command

metadata:
  trigger: 学生刷题日报、智国OJ、刷题统计、OJ日报、学生做题
---

Domain keywords: 智国OJ, 刷题日报, 学生做题, 提交统计

Summary: 使用edgeuse复用浏览器，抓取智国OJ学生提交数据，生成日报（总榜单+学生单独讲解文件）。

Strategy:
1. 建立CDP连接（edgeuse复用浏览器）
2. 访问/status页面抓取指定时间范围数据
3. 过滤管理员/教师账号，统计学生AC/未AC
4. 查看学生代码，生成针对性题解
5. 输出Markdown+HTML双格式报告

AVOID:
- AVOID 不用edgeuse就启动新浏览器，必须复用已登录的
- AVOID 只抓第1页，必须翻页直到超出时间范围
- AVOID 教师账号出现在日报中，必须在数据处理阶段过滤
- AVIEW 未AC判断错误，只统计最终没AC的题目
- AVOID 不看学生代码就脑补题解，必须访问submission-detail

---

## 核心配置

| 配置项 | 值 |
|-------|-----|
| OJ地址 | https://fslong.iok.la |
| 管理员账号 | long long |
| 排除名单 | MEMORY.md中的管理员/教师列表 |
| 输出目录 | ~/Desktop/智国OJ刷题日报/ |

## 使用方式

| 用户输入 | 时间范围 |
|---------|---------|
| 生成刷题日报 | 1天（默认） |
| 最近3天做题情况 | 3天 |
| 本周学生做题统计 | 7天 |
| 本月刷题日报 | 30天 |

## 工作流程

### Step 1: CDP连接（edgeuse）

```bash
# 检测CDP端口
curl -s http://localhost:9022/json/version || echo "CDP_NOT_RUNNING"

# 已运行→直接连接
browser_use action=connect_cdp cdp_url=http://localhost:9022

# 未运行→启动Edge
nohup /opt/microsoft/msedge/msedge --remote-debugging-port=9022 &
```

### Step 2: 抓取数据

访问`/status`页面，翻页抓取指定时间范围内的提交记录。

**时间判断**：
| 格式 | 判断 |
|------|------|
| "X分钟前"/"X小时前" | ✅在范围内 |
| "X天前" | 判断X≤用户指定天数 |

### Step 3: 数据处理

1. **过滤管理员/教师**：MEMORY.md排除名单中的账号完全不显示
2. **统计AC数**：每个学生今日AC题数
3. **判断未AC**：某题目今天的最后一次提交不是Accepted→列入未AC

**未AC判断示例**：
- P1001: WA→WA→AC → ✅不列入（最终AC了）
- P1002: WA→TLE→WA → ❌列入（最终没AC）

### Step 4: 查看代码生成题解

对每个未AC题目：
1. 访问`/submission-detail/{RunID}`查看学生代码
2. 访问`/problem/{ProblemID}`了解题意
3. 分析错误原因，给出参考代码

### Step 5: 生成报告

**总榜单文件**：
- `智国OJ刷题日报_YYYY-MM-DD.md`
- `智国OJ刷题日报_YYYY-MM-DD.html`

**学生单独讲解文件**（仅有未AC题目的学生）：
- `{学生ID}_YYYY-MM-DD.md`
- `{学生ID}_YYYY-MM-DD.html`

内容包含：题目分析、思路分析、错误原因、参考代码、训练重点点评

## 质量检查

- [ ] 使用edgeuse建立CDP连接
- [ ] 翻页抓取所有指定时间范围数据
- [ ] 排除管理员/教师账号
- [ ] 未AC判断正确（最终AC的不算）
- [ ] 访问submission-detail查看学生代码
- [ ] 题解基于实际代码分析
- [ ] 为有未AC题目的学生生成单独文件
- [ ] HTML代码转义（<、>、& → &lt;、&gt;、&amp;）
- [ ] 打印分页（总榜单后分页，每个学生单独一页）

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 直接启动新浏览器 | 使用edgeuse复用已登录的 |
| 只抓第1页 | 翻页直到超出时间范围 |
| 教师账号出现在日报 | 数据处理阶段就过滤掉 |
| 把WA后AC的题目算未AC | 只统计最终没AC的 |
| 不看代码就写题解 | 访问submission-detail分析 |
