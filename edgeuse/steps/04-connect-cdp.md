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
2. 重新执行连接命令

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
