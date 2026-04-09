---
priority: 999
name: edgeuse
description: "🌐 Edge/Chrome CDP Connector — 一键唤醒你的浏览器！跨平台支持 Linux/Windows/macOS，Edge 和 Chrome 自动切换。所有网页相关任务必须使用本技能。"
metadata:
  {
    "builtin_skill_version": "2.0",
    "copaw":
      {
        "emoji": "🌐",
        "requires": {},
        "auto_load": true,
        "global": true,
        "trigger_keywords": [
          "http", "https", "www.", ".com", ".cn", ".org", ".net", ".io",
          "打开", "访问", "浏览", "进入", "去", "上",
          "查", "看", "搜", "刷", "找",
          "登录", "截图", "自动操作",
          "网页", "网站", "页面", "网址", "网上", "在线",
          "知乎", "公众号", "小红书", "微博", "B站",
          "东方财富", "同花顺", "雪球", "天天基金",
          "淘宝", "京东", "拼多多", "抖音", "快手"
        ]
      }
  }
---

# 🌐 Edge/Chrome CDP Connector

> **让 AI 成为你的浏览器副驾驶**

---

## ⚠️ 铁律

**所有网页相关任务必须使用本技能！禁止直接使用 `browser_use` 的 start/open 操作！**

---

## 🔧 执行流程（按步骤读取文档）

```
Step 1: 检测 CDP 端口 ──► 读取 steps/01-detect-cdp.md
    ├─ 已开启 ──► 直接跳到 Step 5
    └─ 未开启 ──► 继续 Step 2

Step 2: 断开旧连接 ──► browser_use action="stop"

Step 3: 检测操作系统 ──► 读取 steps/02-detect-os.md

Step 4: 定位并启动浏览器 ──► 读取 steps/03-start-browser.md
    ├─ Edge 可用 ──► 启动 Edge
    └─ Edge 不可用 ──► 启动 Chrome

Step 5: 建立 CDP 连接 ──► 读取 steps/04-connect-cdp.md

Step 6: 开始操作 ──► 使用 browser_use 执行任务
```

---

## 📁 步骤文档位置

| 步骤 | 文档 | 内容 |
|------|------|------|
| Step 1 | `steps/01-detect-cdp.md` | CDP 端口检测命令 |
| Step 2 | — | 直接执行 `browser_use action="stop"` |
| Step 3 | `steps/02-detect-os.md` | 操作系统检测命令 |
| Step 4 | `steps/03-start-browser.md` | 浏览器查找和启动命令（分平台） |
| Step 5 | `steps/04-connect-cdp.md` | CDP 连接命令 |

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

- ❌ 禁止绕过本技能直接使用 `browser_use` 的 start/open
- ❌ 禁止跳过连接步骤直接执行网页操作
- ❌ 禁止使用其他工具替代本技能访问网页

---

## 📝 版本

| 版本 | 更新内容 |
|------|----------|
| 2.0.0 | 模块化重构，按步骤读取文档 |
| 1.5.0 | 新增 macOS 支持，Edge/Chrome 自动切换 |
