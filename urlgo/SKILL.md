---
name: urlgo
description: 连 CDP，开网页，截图，执行 JS 的浏览器控制 CLI
allowed-tools:
  - Read
  - Write
  - Bash

metadata:
  trigger: 浏览器, CDP, 截图, 网页, 打开网页, 网页截图, 源码, HTML源码
---

# Skill: urlgo

## Keywords

浏览器, CDP, 截图, 网页, 打开网页, HTML源码

## Summary

连 CDP，开网页，截图，执行 JS。

## Strategy

路径：`python3 /home/fslong/.config/opencode/skills/urlgo/urlgo`

1. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo status` → CDP 开了没？
2. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo start` → 启动浏览器（后台运行，脚本退出后浏览器不关）
3. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo open <url>` → 打开页面
4. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo screenshot <id> <file>` → 截图
5. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo snapshot <id>` → 读取页面内容（纯文字）
6. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo source <id>` → 获取页面 HTML 源码

AVOID:
- AVOID 不检查 CDP 就操作，先 status/start
- AVOID 直接用 `urlgo` 命令（PATH 可能没有），必须用完整 Python 路径
- AVOID 用 WebFetch 读网页，应该用 urlgo snapshot 代替
- AVOID 用 snapshot 读源码（它只返回纯文本），取源码用 urlgo source
- AVOID 多次 start（会检测到已启动而跳过）

## 命令

| 命令 | 说明 |
|------|------|
| `status` | 检查 CDP |
| `start` | 启动浏览器（后台运行，进程退出后浏览器不关） |
| `list` | 查看页面 |
| `open <url>` | 打开网页 |
| `activate <id>` | 激活页面 |
| `close <id>` | 关闭页面 |
| `screenshot <id> <file>` | 截图 |
| `snapshot <id>` | 读取内容（纯文字） |
| `source <id>` | 获取 HTML 源码 |
| `eval <id> "<js>"` | 执行 JS |
| `click <id> "<sel>"` | 点击 |
| `type <id> "<sel>" "<text>"` | 输入 |

## 示例

```bash
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo start
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo open https://example.com
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo snapshot 1
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo source 1
python3 /home/fslong/.config/opencode/skills/urlgo/urlgo screenshot 1 /tmp/a.png
```

## 依赖

curl, websockets(Python)
