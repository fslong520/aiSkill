# API 参考

## 核心 endpoint

| Endpoint | 用途 | 说明 |
|----------|------|------|
| POST /api/search | 查文档/形状/绑定/截屏/Editor API | 有 `api` 对象，适合只读操作 |
| POST /api/docs/create | 新建 .tldraw 文件 | JSON body: `{"name":"..."}`，可选 `"directory"` |
| POST /api/doc/:id/exec | 对单文档就地编辑 | 有 `editor` 对象 + `helpers` |
| POST /api/doc/:id/script-workspace | 暴露常驻脚本路径 | 用于 `script/main.js` 等 |
| GET /api/doc/:id/script-status | 查脚本 watcher 状态 | 回 `state: "applied"|"pending"|"error"` |

代码型 POST endpoint 接收裸 JS（content-type: text/plain）或 JSON `{"code": "..."}`，自动包装 async 函数，顶层 await 可用。

## 开局查文档

```bash
PORT=$(jq -r .port '/home/fslong/.config/tldraw/server.json')
TOKEN=$(jq -r .token '/home/fslong/.config/tldraw/server.json')

# 查某文档
curl -s -X POST http://localhost:$PORT/api/search \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $TOKEN" \
  -d '{"code":"return await api.getDocs({ name: \"NAME\" })"}'

# 读当前页面形状（含 id/type/坐标/props/meta）
curl -s -X POST http://localhost:$PORT/api/search \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $TOKEN" \
  -d '{"code":"const doc = await api.getFocusedDoc(); const page = doc ? await api.getShapes(doc.id) : null; return { doc, shapes: page?.shapes.map(s => ({ id: s.id, type: s.type, x: s.x, y: s.y, props: s.props, meta: s.meta })) ?? [] }"}'

# 读绑定（仅连接相关时需要）
curl -s -X POST http://localhost:$PORT/api/search \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $TOKEN" \
  -d '{"code":"const doc = await api.getFocusedDoc(); return doc ? await api.getBindings(doc.id) : []"}'
```

## 新建文档

```bash
curl -s -X POST http://localhost:$PORT/api/docs/create \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $TOKEN" \
  -d '{"name":"Project Plan"}'
```

用 `tq`: `sh "$HOME/skills/tldraw-offline/tq" POST /api/docs/create '{"name":"Project Plan"}'`

不传 `directory` 时存用户 Documents 目录。同名已有文件返回 409，不覆盖。不传 `.tldraw` 扩展名自动加。回复含 `id`、`documentId`、`filePath`、`name`、`windowId`——拿此 `id` 直接喂 `/api/doc/:id/exec`，无需再查。

## 编辑器（/exec）示例

```bash
curl -s -X POST http://localhost:$PORT/api/doc/DOC_ID/exec \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $TOKEN" \
  -d '{"code":"const { createShapeId, toRichText } = await import(\"tldraw\"); const id = createShapeId(\"r1\"); editor.createShape({ id, type: \"geo\", x: 100, y: 100, props: { geo: \"rectangle\", w: 200, h: 100, richText: toRichText(\"Hello\") } }); await helpers.saveDoc(); return { created: [id] }"}'
```

## 形状格式

`api.getShapes()`、`/exec`、脚本皆用原始 tldraw SDK 记录。建形状用常规 partial。

```js
const { createShapeId, toRichText } = await import('tldraw')
editor.createShape({
  id: createShapeId('box1'),
  type: 'geo',
  x: 100,
  y: 100,
  props: { geo: 'rectangle', w: 300, h: 200, richText: toRichText('Label') },
})
await helpers.saveDoc()
```

- `/exec` 片段用 `await import('tldraw')`（不能用 static import）
- 脚本可顶层 `import { createShapeId } from 'tldraw'`
- `helpers` 仅有编辑器便捷方法，不含 SDK 原语——直接 `import 'tldraw'`
- `api.imports`（/api/search）可查全部可导入符号

## 截屏

```js
const shot = await api.getScreenshot(docId, opts?)
// 回 { filePath, width, height, pageName, viewport, bounds, captureMode }
```

`opts`:
- `size`: `'small'|'medium'|'large'|'full'`（默认 small）
- `mode`: `'canvas'`（仅形状，默认）| `'window'`（含 UI chrome）
- `bounds`: `{ x, y, w, h }`（仅 canvas 模式，页面坐标）

`filePath` 为临时文件路径，自行打开查看。优先用 `api.getShapes()` 读记录，截图仅视觉确认或用户要求时用。
