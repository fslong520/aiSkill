# Step 4: 建立 CDP 连接

## 🎯 目标

通过 `browser_use` 工具建立 CDP 连接。

---

## 🔧 命令

```
browser_use action="connect_cdp" cdp_url="http://localhost:9022"
```

---

## 📊 判断结果与下一步跳转

### ✅ 连接成功

**输出示例**：
```json
{
  "ok": true,
  "message": "Connected to Chrome via CDP at http://localhost:9022",
  "pages": ["page_0", "page_1", ...]
}
```

**👉 下一步**：开始执行任务（open、snapshot、click 等）

---

### ❌ 连接失败

**输出示例**：
```json
{
  "ok": false,
  "error": "A Playwright-managed browser is currently running..."
}
```

**处理流程**：
1. 执行 `browser_use action="stop"` 断开旧连接
2. 关闭占用 9022 端口的浏览器进程：
   ```bash
   # Linux
   kill $(lsof -ti:9022) 2>/dev/null
   
   # macOS
   lsof -ti:9022 | xargs kill 2>/dev/null
   ```
3. 等待 2 秒让端口释放
4. **👉 回到** `steps/01-detect-cdp.md` 重新检测

---

## 🚀 连接后可用操作

| 操作 | 命令 |
|------|------|
| 打开网页 | `browser_use action="open" url="https://..."` |
| 页面快照 | `browser_use action="snapshot"` |
| 点击元素 | `browser_use action="click" ref="xxx"` |
| 输入文本 | `browser_use action="type" text="xxx"` |
| 截图 | `browser_use action="screenshot" path="xxx.png"` |

---

## ⚠️ 注意事项

- 连接后浏览器保持运行，不会关闭
- 可以复用已有的登录态和书签
- 断开连接用 `browser_use action="stop"`，不会关闭浏览器