---
priority: 1000
name: urlgo
description: 浏览器控制 CLI
metadata: {"builtin_skill_version": "6.2.0", "copaw": {"emoji": "🌐", "requires": {}, "auto_load": true, "global": true}}
---

Domain keywords: https://, http://, www., 浏览器, CDP, 截图, 网页, mp.weixin

Summary: 连接 CDP 浏览器的 CLI 工具，支持打开网页、截图、执行 JS。

Strategy:
1. `urlgo status` → 检查 CDP，未开启则 `urlgo start` 启动浏览器
2. `urlgo open <url>` → 打开页面，返回 page id
3. 用户选择操作 → 截图/读取/点击/输入/执行 JS
4. 返回结果

AVOID:
- AVOID 未检查 CDP 状态就操作，应该先 status/start
- AVOID 忘记安装 websockets，截图和 JS 执行需要它
- AVOID 用 WebFetch 读网页，应该用 urlgo snapshot（见 memory）

---

## 命令

| 命令 | 说明 |
|------|------|
| `urlgo status` | 检查 CDP |
| `urlgo start` | 启动浏览器 |
| `urlgo list` | 查看页面 |
| `urlgo open <url>` | 打开网页 |
| `urlgo screenshot <id> <file>` | 截图 |
| `urlgo snapshot <id>` | 读取内容 |
| `urlgo eval <id> "<js>"` | 执行 JS |
| `urlgo click <id> "<sel>"` | 点击 |
| `urlgo type <id> "<sel>" "<text>"` | 输入 |

## 示例

```bash
urlgo start
urlgo open https://example.com
urlgo snapshot 1
urlgo screenshot 1 /tmp/a.png
```

## 依赖

curl, websockets(Python)
