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
3. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo open <url>` → 打开页面（仅限首页/入口 URL）
4. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo screenshot <id> <file>` → 截图
5. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo snapshot <id>` → 读取页面内容（纯文字）
6. `python3 /home/fslong/.config/opencode/skills/urlgo/urlgo source <id>` → 获取页面 HTML 源码

> ⚠️ **导航铁律：页面内点击，禁止手工拼接 URL。**
> 进站后的一切跳转（翻页、点链接、点按钮、选试卷、提交表单）必须：
> 1. `source <id>` 取源码，从 HTML 里找到目标链接/按钮；
> 2. `click <id> "<selector>"` 或 `eval <id> "document.querySelector('...').click()"` 在页面内点击；
> 3. 严禁手工拼接带参 URL 再用 `open` 打开——`&` 会被截断、Referer 校验会失败、会话/登录态丢失，三害俱全。
> `open` 只用于初始入口（首页、登录页）。

## 标签页管理（硬规矩）

每次 `open` 新页前先 `list` 查标签页数。**超过 5 个必须先清理再开新页**：

1. 逐页判断：该页当前是否在用于测试、演示、或哥哥要看操作过程？
   - 是 → **必留**，不得关；
   - 纯残留、与本回合任务无关的旧页 → `close <id>` 关掉。
2. 拿不准的页宁留勿关；宁少关不误关。
3. 清理后再开新页，保持总数 ≤5。

> ⚠️ 只关真正没用的冗余页，禁一刀切全关。

AVOID:
- AVOID 标签页超 5 个还继续 `open`，必须先按「标签页管理」清理冗余页
- AVOID 不检查 CDP 就操作，先 status/start
- AVOID 直接用 `urlgo` 命令（PATH 可能没有），必须用完整 Python 路径
- AVOID 用 WebFetch 读网页，应该用 urlgo snapshot 代替
- AVOID 用 snapshot 读源码（它只返回纯文本），取源码用 urlgo source
- AVOID 多次 start（会检测到已启动而跳过）
- AVOID 手工拼接带参 URL（含 `?` `&`）再用 open 打开——会被截断或 Referer 拦截，必须页面内点击（见上方导航铁律）
- AVOID 复制源码里的 href 后自己重新拼 URL 访问，直接 click 原链接

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