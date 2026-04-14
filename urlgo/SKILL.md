---
priority: 1000
name: urlgo
description: "所有联网操作必须通过此 skill 处理，包括：搜索、网页抓取、登录后操作、网络交互等。 触发场景：用户要求搜索信息、查看网页内容、访问需要登录的网站、操作网页界面、抓取社交媒体内容（小红书、微博、推特等）、读取动态渲染页面、以及任何需要真实浏览器环境的网络任务。"
metadata:
  {
    "builtin_skill_version": "2.2.0",
    "copaw":
      {
        "emoji": "🌐",
        "requires": {},
        "auto_load": true,
        "global": true,
        "trigger_keywords": [
          "http", "https", "www.", ".com", ".cn", ".org", ".net", ".io", ".html", ".gov", ".edu",
          "打开", "访问", "浏览", "进入", "跳转", "navigate", "go to",
          "查", "看", "搜", "刷", "查询", "查看", "搜索", "browse", "view", "check",
          "登录", "登陆", "signin", "login",
          "截图", "截屏", "快照", "snapshot", "screenshot", "render",
          "自动操作", "自动化", "automate", "browser",
          "网页", "网站", "页面", "网址", "网上", "在线", "web", "online",
          "url", "link", "链接", "地址", "open",
          "抓取", "爬取", "scrape", "crawl", "fetch",
          "PDF", "pdf", "导出", "export", "生成报告"
        ]
      }
  }
---

# 🌐 Edge/Chrome CDP Connector

> **让 AI 成为你的浏览器副驾驶**

---

## ⚠️ 铁律

**所有网页相关任务必须使用本技能！禁止直接使用 `browser_use` 的 start/open 操作！**

**启动前必须检查旧进程！** 如果浏览器已打开但 **没有开启 9022 端口**，必须关掉旧进程再启动！
因为浏览器机制：已有实例运行时，新启动命令会把 URL 传给旧实例，旧实例没 CDP 就白启动了。
CDP 连不上就按流程处理：stop → kill端口 → 重启 → connect。

**启动浏览器只加 `--remote-debugging-port=9022` 参数！** 不要加 `--headless`、`--disable-gpu`、`--no-sandbox`、`--user-data-dir` 等多余参数，容易导致启动失败。

---

## 🔧 执行流程（按步骤读取文档）

```
Step 1: 检测 CDP 端口 ──► 读取 steps/01-detect-cdp.md
    ├─ 已开启 ──► 直接跳到 Step 4（连接 CDP）
    └─ 未开启 ──► 继续 Step 2

Step 2: 检测操作系统 ──► 读取 steps/02-detect-os.md

Step 3: 定位并启动浏览器 ──► 读取 steps/03-start-browser.md
    ├─ Edge 可用 ──► 启动 Edge（只加 --remote-debugging-port=9022，不杀旧进程！）
    └─ Edge 不可用 ──► 启动 Chrome

Step 4: 建立 CDP 连接 ──► 读取 steps/04-connect-cdp.md

Step 5: 开始操作 ──► 使用 browser_use 执行任务
```

---

## 📁 步骤文档位置

| 步骤 | 文档 | 内容 |
|------|------|------|
| Step 1 | `steps/01-detect-cdp.md` | CDP 端口检测命令 |
| Step 2 | `steps/02-detect-os.md` | 操作系统检测命令 |
| Step 3 | `steps/03-start-browser.md` | 浏览器查找和启动（不杀旧进程，只加 CDP 参数） |
| Step 4 | `steps/04-connect-cdp.md` | CDP 连接命令 |

---

## 🔗 其他技能如何调用本技能

当其他技能（如破晓、新闻搜索等）需要网页操作时，**必须先调用 edgeuse**：

```
1. 先调用 edgeuse 技能（它会完成：CDP 检测 → 浏览器启动 → CDP 连接）
2. edgeuse 完成后，再使用 browser_use action="navigate/snapshot/screenshot" 执行操作

❌ 禁止：其他技能直接调用 browser_use action="open" 或 action="start"
✅ 正确：edgeuse 建立连接 → browser_use action="navigate" 访问页面
```

---

## 🚨 触发场景

- 🟢 打开网页、访问网站、浏览网页
- 🟢 查价格、查股票、查行情、看大盘
- 🟢 看新闻、刷新闻、查资讯
- 🟢 登录网站、自动登录、扫码登录
- 🟢 截图、网页截图、页面截图
- 🟢 自动操作、网页操作、浏览器自动化
- 🟢 东方财富、同花顺、雪球、天天基金
- 🟢 知乎、公众号、小红书、微博
- 🟢 任何需要访问网站的任务

---

## ❌ 禁止行为

- ❌ **任何技能（包括破晓、新闻等）绕过本技能直接调用 `browser_use` 的 start/open**
- ❌ 禁止跳过连接步骤直接执行网页操作
- ❌ 禁止使用其他工具替代本技能访问网页
- ❌ 禁止杀掉已有浏览器进程（`pkill`/`kill`/`killall`）
- ❌ 禁止给浏览器加多余启动参数（只加 `--remote-debugging-port=9022`）
- ❌ **其他技能文档中写了 `browser_use action="open"` 的，必须先调 edgeuse 再 navigate**

---

## 📝 版本

| 版本 | 更新内容 |
|------|----------|
| **2.2.0** | **🔴 priority 提升至 1000（最高），确保优先于破晓等技能触发；新增"其他技能如何调用"章节；明确禁止其他技能绕过 edgeuse 直接调用 browser_use** |
| 2.1.0 | 修复：禁止杀浏览器进程，启动只加 CDP 参数，去掉多余参数 |
| 2.0.0 | 模块化重构，按步骤读取文档 |
| 1.5.0 | 新增 macOS 支持，Edge/Chrome 自动切换 |
