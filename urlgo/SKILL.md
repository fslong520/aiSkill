---
priority: 1000
name: urlgo
description: "🌐 浏览器控制技能 | 所有网络操作必须通过此技能！禁止裸用 browser_use！
触发关键字：https://、http://、www.、.com、.cn、.org、ftp://、mp.weixin、github、baidu、bing、google、搜索、访问、打开网页、读取文章、截图网页
"
metadata: {"builtin_skill_version": "4.1.0", "copaw": {"emoji": "🌐", "requires": {}, "auto_load": true, "global": true}}
---

# 🌐 urlgo - 浏览器控制技能

> **⚠️⚠️⚠️ 最高优先级铁律 ⚠️⚠️⚠️**
> 
> ## 🔴 强制使用规则
> 
> | 场景 | 正确做法 | 错误做法（违规！） |
> |------|----------|-------------------|
> | 打开网页 | ✅ 先用 urlgo 连接浏览器 | ❌ 直接 browser_use start/open |
> | 访问网站 | ✅ 先 connect_cdp | ❌ 直接 action="open" |
> | 截图网页 | ✅ connect_cdp → open → screenshot | ❌ 直接 screenshot |
> | 读取微信文章 | ✅ urlgo 流程 | ❌ browser_use open |
> | 抓取网页内容 | ✅ urlgo 流程 | ❌ 直接 snapshot |
> | 任何网络操作 | ✅ 先读 steps/01-detect-cdp.md | ❌ 直接调用 browser_use |
> 
> **违规惩罚**：每次裸用 browser_use 都要记录到 MEMORY.md 的血泪教训！

---

## 🚨 强制触发条件

**只要满足以下任一条件，必须使用 urlgo 技能：**

| 触发词/场景 | 示例 |
|------------|------|
| 🌐 打开网页 | "访问xxx.com"、"打开网页"、"浏览网站" |
| 📰 阅读文章 | "读一下这篇文章"、"打开微信文章"、"看这个链接" |
| 🔍 搜索信息 | "搜索xxx"、"百度一下"、"Google搜索" |
| 📸 截图网页 | "截个图"、"网页截图"、"保存页面" |
| 🤖 网页自动化 | "自动登录"、"填表单"、"点击按钮" |
| 💰 查看价格/数据 | "查股价"、"看价格"、"刷数据" |
| 📧 登录邮箱 | "登录邮箱"、"查看邮件" |
| 🛒 电商操作 | "查看商品"、"下单"、"比价" |
| 📱 社交媒体 | "刷抖音"、"看微博"、"发帖" |
| 📄 读取文档 | "打开PDF"、"看Word文档"（在线版） |

---

## 📋 标准执行流程（4步）

```
┌─────────────────────────────────────────────────────────────────┐
│  🌐 urlgo 标准流程                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  【第1步】读取入口文档                                            │
│  📄 read_file("steps/01-detect-cdp.md")                         │
│          ↓                                                        │
│  【第2步】检测 CDP 端口                                           │
│  💻 curl -s http://localhost:9022/json/version                  │
│          ↓                                                        │
│       ┌────┴────┐                                                │
│       ↓         ↓                                                │
│    已开启      未开启                                             │
│       ↓         ↓                                                │
│  【第3步】    【第3步】                                            │
│  连接CDP      检测OS                                              │
│  connect     → 启动                                               │
│  _cdp        browser                                             │
│          ↓         ↓                                                │
│  【第4步】执行任务                                                │
│  open / snapshot / click / screenshot 等                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚡ 快速检查清单（每次浏览器操作前必读）

```
┌──────────────────────────────────────────────────────────────┐
│  🔍 操作前自检                                                  │
├──────────────────────────────────────────────────────────────┤
│  Q1: 这个任务需要浏览器吗？                                      │
│      → YES → 必须用 urlgo！                                    │
│                                                                  │
│  Q2: 是否已读取 steps/01-detect-cdp.md？                       │
│      → NO → 先读取！                                           │
│                                                                  │
│  Q3: 是否检测过 CDP 端口？                                      │
│      → NO → 先检测！                                           │
│                                                                  │
│  Q4: 是否 connect_cdp 了？                                      │
│      → NO → 先连接！                                           │
│                                                                  │
│  ✅ 全部 YES → 可以执行 open/snapshot 等操作                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔧 快速启动（直接复制用）

### 场景1：CDP 已开启（常见情况）
```
1. 读取：read_file("steps/01-detect-cdp.md")
2. 检测：execute_shell_command("curl -s http://localhost:9022/json/version")
3. 连接：browser_use(action="connect_cdp", cdp_url="http://localhost:9022")
4. 打开：browser_use(action="open", url="https://xxx.com", page_id="xxx")
5. 获取：browser_use(action="snapshot", page_id="xxx")
```

### 场景2：CDP 未开启
```
1. 读取：read_file("steps/01-detect-cdp.md")
2. 检测：execute_shell_command("curl -s http://localhost:9022/json/version")
3. 未开启 → 读取 steps/02-detect-os.md
4. 读取 steps/03-start-browser.md
5. 启动：browser_use(action="start", cdp_port=9022)
6. 读取 steps/04-connect-cdp.md
7. 连接：browser_use(action="connect_cdp", cdp_url="http://localhost:9022")
8. 执行任务
```

---

## 🚫 常见违规模式（绝对禁止）

| ❌ 错误写法 | ✅ 正确写法 |
|-----------|------------|
| `browser_use(action="start")` | 读取 steps/01-detect-cdp.md 开始 |
| `browser_use(action="open", url="...")` | 先 connect_cdp 再 open |
| 直接用 snapshot | 先 open 再 snapshot |
| 直接 screenshot | 先 connect_cdp 再 screenshot |
| 用 browser_use 开任何网页 | 都必须先走 urlgo 流程！ |

---

## 📖 文档结构

```
urlgo/
├── SKILL.md              # 本文件 - 入口和快速参考
└── steps/
    ├── 01-detect-cdp.md  # 第1步：检测 CDP 端口
    ├── 02-detect-os.md   # 第2步：检测操作系统（CDP未开启时）
    ├── 03-start-browser.md # 第3步：启动浏览器（CDP未开启时）
    └── 04-connect-cdp.md # 第4步：建立 CDP 连接
```

---

## 🔑 核心概念

| 概念 | 解释 |
|------|------|
| **CDP** | Chrome DevTools Protocol，浏览器调试协议 |
| **connect_cdp** | 连接到已运行的浏览器（复用已有标签页、登录态） |
| **browser_use start** | 启动新浏览器（私有模式，无 cookies） |
| **9022 端口** | CDP 默认监听端口 |

---

**版本**: 4.0.0
**更新**: 2026-04-18
**变更**：
- v4.0.0: 大幅强化！新增强制触发条件表、快速检查清单、常见违规模式对照表
- v3.1.0: 按步骤入口、按需读取
- 早期版本: 初始版本
