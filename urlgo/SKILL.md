---

name: 浏览器控制
description: 浏览器控制 CLI
metadata:
  slug: urlgo
  priority: 1000
  builtin_skill_version: "6.3.0"
  trigger: urlgo、浏览器、CDP、截图、网页、打开网页、网页截图、https://、http://
  copaw:
    emoji: "🌐"
    requires: {}
    auto_load: true
    global: true
---

## Keywords

https://, http://, www., 浏览器, CDP, 截图, 网页, mp.weixin, 打开网页, 网页截图

## Summary

连 CDP，开网页，截图，执行 JS。

## Strategy
1. `urlgo status` → CDP 开了没？没开就 `urlgo start`
2. `urlgo open <url>` → 打开页面
3. 截图/读取/点击/输入/执行 JS
4. 返回结果

AVOID:
- AVOID 不检查 CDP 就操作，先 status/start
- AVOID 忘装 websockets，截图和 JS 要用它
- AVOID 用 WebFetch 读网页，应该用 urlgo snapshot 代替

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
