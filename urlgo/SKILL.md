---
priority: 1000
name: urlgo
description: "🌐 浏览器控制技能 | 连接已有 CDP 浏览器，简单 CLI 命令
触发关键字：https://, http://, www., .com, .cn, .org, mp.weixin, 打开网页、截图、读取文章
"
metadata: {"builtin_skill_version": "6.1.0", "copaw": {"emoji": "🌐", "requires": {}, "auto_load": true, "global": true}}
---

# 🌐 urlgo - 浏览器控制 CLI

> **简单粗暴！** 自动查找浏览器，连接 CDP，直接操作。

---

## 🚀 快速开始

```bash
# 1. 检查状态
urlgo status

# 2. 启动浏览器（自动查找 Edge/Chrome/Chromium）
urlgo start

# 3. 操作
urlgo list                           # 查看所有页面
urlgo open https://www.baidu.com     # 打开网页
urlgo screenshot <id> /tmp/test.png  # 截图
```

---

## 📋 命令速查

| 命令 | 说明 |
|------|------|
| `urlgo status` | 检查 CDP 状态 |
| `urlgo start` | 查找并启动浏览器 |
| `urlgo list` | 查看所有页面 |
| `urlgo open <url>` | 打开新页面 |
| `urlgo activate <id>` | 激活页面 |
| `urlgo close <id>` | 关闭页面 |
| `urlgo screenshot <id> <file>` | 截图 |
| `urlgo snapshot <id>` | 读取页面内容 |
| `urlgo eval <id> "<js>"` | 执行 JS |
| `urlgo click <id> "<sel>"` | 点击元素 |
| `urlgo type <id> "<sel>" "<text>"` | 输入文字 |

---

## ⚡ 示例

### 检查状态并启动

```bash
urlgo status          # 检查 CDP 是否开启
urlgo start           # 自动查找 Edge/Chrome/Chromium 并启动
```

### 打开网页并截图

```bash
urlgo open https://www.zhihu.com
urlgo screenshot <id> /tmp/zhihu.png
```

### 自动搜索

```bash
urlgo open https://www.baidu.com
urlgo type <id> "input.s_ipt" "搜索内容"
urlgo click <id> "input.s_btn"
```

---

## 🔧 常用 JS 操作

| 功能 | JS 代码 |
|------|---------|
| 获取标题 | `document.title` |
| 获取 URL | `window.location.href` |
| 获取元素文本 | `document.querySelector('#id').innerText` |
| 滚动页面 | `window.scrollBy(0, 500)` |

---

## 🔄 状态处理

### CDP 已开启

```
urlgo status
✅ CDP 已开启
   浏览器: Edg/147.0.3912.60
   端口: 9022
   页面数: 5
```

### CDP 未开启

```
urlgo status
❌ CDP 未开启

启动方式:
  1. 运行: urlgo start
  2. 手动启动: microsoft-edge --remote-debugging-port=9022 &
```

### urlgo start 行为

- **CDP 已开启** → 提示已开启，不重复启动
- **CDP 未开启** → 自动查找 Edge → Chrome → Chromium 并启动

---

## 📁 文件结构

```
urlgo/
├── SKILL.md      # 本文档
├── urlgo         # CLI 工具
└── steps/        # 详细步骤文档
```

---

## ⚠️ 依赖

- `curl` - 基础操作
- `websockets` (Python) - 截图、执行 JS（未安装会提示）

---

**版本**: 6.1.0
**更新**: 2026-04-21
**变更**: 新增 status、start 命令，自动查找 Edge/Chrome/Chromium
