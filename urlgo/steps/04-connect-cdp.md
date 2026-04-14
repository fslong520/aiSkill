# Step 5: 建立 CDP 连接

## 🎯 目标

通过 `browser_use` 工具建立 CDP 连接。

---

## 🔧 命令

```
browser_use action="connect_cdp" cdp_url="http://localhost:9022"
```

---

## 📊 判断结果

### 连接成功

**输出示例**：
```json
{
  "ok": true,
  "message": "Connected to Chrome via CDP at http://localhost:9022",
  "pages": ["page_0", "page_1", ...]
}
```

**下一步**：开始执行任务（打开网页、截图、点击等）。

---

### 连接失败

**输出示例**：
```json
{
  "ok": false,
  "error": "A Playwright-managed browser is currently running..."
}
```

**解决方法**：
1. 先执行 `browser_use action="stop"` 断开旧连接
2. 关闭占用 9022 端口的浏览器进程（精确杀端口，不误杀用户其他浏览器）：
   ```bash
   # Linux - 精确杀 9022 端口对应的进程
   kill $(lsof -ti:9022) 2>/dev/null
   # 或 pkill 特定浏览器（二选一）
   pkill -f "msedge.*9022\|chrome.*9022" 2>/dev/null
   
   # Windows
   # 查找占用 9022 端口的 PID 并 kill
   for /f "tokens=5" %a in ('netstat -ano ^| findstr :9022') do taskkill /F /PID %a
   
   # macOS
   lsof -ti:9022 | xargs kill 2>/dev/null
   ```
3. 等待 2 秒让端口释放：`sleep 2`
4. 重新读取 `steps/03-start-browser.md`，启动带 `--remote-debugging-port=9022` 的新浏览器
5. 验证 CDP 端口：`curl -s http://localhost:9022/json/version`
6. 重新执行 `browser_use action="connect_cdp" cdp_url="http://localhost:9022"`

---

## 🚀 连接后可执行的操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 打开网页 | `browser_use action="open" url="https://..."` | 在新标签页打开 URL |
| 页面快照 | `browser_use action="snapshot"` | 获取页面结构 |
| 点击元素 | `browser_use action="click" ref="xxx"` | 点击页面元素 |
| 输入文本 | `browser_use action="type" text="xxx"` | 输入文字 |
| 截图 | `browser_use action="screenshot" path="xxx.png"` | 保存截图 |

---

## ⚠️ 注意事项

- 连接后浏览器保持运行，不会关闭
- 可以复用已有的登录态和书签
- 断开连接用 `browser_use action="stop"`，不会关闭浏览器
