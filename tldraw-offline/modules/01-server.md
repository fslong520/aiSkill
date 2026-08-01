# 服务器配置

## 端口

默认 `http://localhost:7236`。若端口不通，读：

```
/home/fslong/.config/tldraw/server.json → .port
```

退出清理 `server.json`；下次启动重写。`server.json` 亦录 `pid`、`startedAt`。
若文件在但该端口请求失败——推为旧文件，app未运行。

## 认证

除 `GET /` 和 `/readme` 外，每请求需 `server.json` 中之 `token`：

```
-H "authorization: Bearer <token>"
```

## 重要：Bash 每调用刷一新 shell

```bash
# 每调用顶上这两行，不可省
PORT=$(jq -r .port '/home/fslong/.config/tldraw/server.json')
TOKEN=$(jq -r .token '/home/fslong/.config/tldraw/server.json')
```

环境变量跨调用不持久。莫想"export 一次复用"——会 401。

## 助手：`tq`

```bash
sh "$HOME/skills/tldraw-offline/tq" <METHOD> <path> [body]
```

自己读 port + token，省心省事。

| 参数 | 说明 |
|------|------|
| METHOD | GET / POST |
| path | 如 `/api/search` |
| body（可选） | `{`开头⇒JSON，否则 text/plain |

**示例：**

```bash
sh "$HOME/skills/tldraw-offline/tq" POST /api/search '{"code":"return await api.getDocs()"}'
sh "$HOME/skills/tldraw-offline/tq" POST /api/doc/DOC_ID/exec 'return editor.getCurrentPageShapes().length'
sh "$HOME/skills/tldraw-offline/tq" GET  /api/doc/DOC_ID/script-status
```

**`tq` 缺失时**，退到裸 `curl` + PORT/TOKEN 读法。以下各例均可用 `tq` 替之。

## 环境注入

子 agent 启动时若 app 已装 agent hook，base URL + token 会被注入到上下文。有则直接用，无则按上述读法。
