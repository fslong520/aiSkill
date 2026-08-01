# 工作流与模式

## 通用原则

非流程。视任务性质择路，可调序、可跳过、可重复。

| 考虑点 | 引导 |
|--------|------|
| 先做什么？ | 明确目标后，查清当前画布状态再动手 |
| 选哪个入口？ | 单次编辑走 /exec，常驻行为走 /script-workspace |
| 验几次？ | 至少一次。不确定则可多验。无人催你 |
| 报多细？ | 引 doc id/name、改了什么形状、一次验证结果 |

## 单次编辑（/exec）

适合：挪位置、改样式、标文字、建连接。

**箭头连接：**
- 用 `helpers.createArrowBetweenShapes(fromId, toId, options)`——两端皆有真实绑定
- 不建裸 arrow（除非刻意装饰性标记，可用）
- `helpers.getLints()` 可查连接完整性，视情况修

## 常驻脚本（/script-workspace）

适合：点触响应、动画循环、响应式布局、"打开即运行"逻辑。

**起步：**
1. `POST /api/doc/:id/script-workspace` 暴露路径
2. 读 `mainJsPath`（若 `isDefaultScript=false` 说明有既有脚本——扩充勿覆盖）
3. 写 `script/main.js`
4. `script-status` 查状态：
   - `"applied"` ✅
   - `"pending"` → 轮询等（文件已存，watcher 未处理完）
   - `"error"` → 读 `lastApplyError`/`errorLogPath`

**编辑前**先读 `mainJsPath` 内容。记得 `helpers.saveDoc()`。

**可参考的 recipe（`api.recipes` 查）：**
- `add-durable-behavior-with-a-document-script`
- `clickable-card-or-button-ui`
- `animation-simulation-loop`
- `connection-dependent-behavior`

## 可编辑家具 + 锚定内部件

适用：用户可调布局但脚本内部件跟随的场景。

```js
// 用 createShapeIfMissing / createShapesIfMissing 建用户可见部件
// 选一个可见锚点（如轨道、桌面）
// helpers.onShapeTranslate(anchorId, ({dx, dy}) => ..., { signal })
// 脚本内部件用 helpers.translateShapes(ids, dx, dy) 跟随（不记 undo 历史）
// 其他脚本写操作用 editor.run(fn, { history: 'ignore' })
```

勿用宽泛的 `store.listen` 响应所有形状变化——脚本自身写操作会触发自身。

## 自定义形状/工具/叠加层（config.js）

`script/config.js` 放 `main.js` 旁，默认 export 接收 `{ config }` 返回修改后的 config。

```js
// config.js 在编辑挂载前执行。main.js 在其后
// 向 config.shapeUtils / tools 等数组 push 自定义构造器
// 自定义形状 extends ShapeUtil；叠加层 extends OverlayUtil（均 from 'tldraw'）
// 定义在兄弟文件再 import，因 config.js 与 main.js 模块图独立
```

- 存 `config.js`（或其 import 的文件）→ 重建 store 和编辑器（文档/镜头/选区保留，undo 历史重置）
- 存 `main.js` → 不重建
- 启动逻辑放 `main.js`；`config.js` 只管配环境
- 参考 recipe：`custom-shape-config-js`、`custom-binding-config-js`、`custom-overlay-config-js`

## 窗口关闭 / 文档异常

若目标 docId 请求回 "Window closed" 或 "Document not found" 或超时：
1. 调 `api.getDocs()` 重查
2. 按 **名称**（+ `documentId` 若有）匹配找回
3. 名称匹配 → 用新 `id` 继续
4. 名称不匹配 或 只剩一个你没开过的文档 → **停**，报给用户

**批量/破坏性操作前**：`api.getShapes()` 确认形状数和内容是否与你预期一致。
如果不一致——你可能站在别人的文档上，停。

## 报告格式

| 要素 | 示例 |
|------|------|
| 文档 | docs/plan.tldraw（id: doc_xxx） |
| 改了什么 | 新建 shape(r1)、移动 shape(box_a) to (200,300) |
| 验证 | api.getShapes() 确认数增 1 |
| 异常 | 错误原文或 error.log 行 |
