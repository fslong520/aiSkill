# Step 3: 定位并启动浏览器

## 🎯 目标

根据操作系统找到浏览器并启动 CDP 模式。

**优先级**：Edge（首选）→ Chrome（备选）

---

## 🚨 铁律（非常重要！）

1. **启动前必须检查旧进程！** 
   - 如果浏览器已打开但 **没有开启 9022 端口**，必须关掉旧进程再启动！
2. **只加 `--remote-debugging-port=9022` 参数！** 不要加其他参数！

---

## 🐧 Linux

### 查找并启动 Edge

```bash
# 先检查并关闭旧进程
curl -s http://localhost:9022/json/version >/dev/null 2>&1 || pkill -f "msedge|chrome" 2>/dev/null; sleep 2

# 启动 Edge
nohup /opt/microsoft/msedge/msedge --remote-debugging-port=9022 > /tmp/edge-cdp.log 2>&1 &
```

### 验证启动

```bash
sleep 5 && curl -s http://localhost:9022/json/version | head -5
```

---

## 🍎 macOS

### 查找并启动 Edge

```bash
# 先检查并关闭旧进程
curl -s http://localhost:9022/json/version >/dev/null 2>&1 || pkill -f "Microsoft Edge|Google Chrome" 2>/dev/null; sleep 2

# 启动 Edge
nohup "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --remote-debugging-port=9022 > /tmp/edge-cdp.log 2>&1 &
```

---

## 🪟 Windows (PowerShell)

### 查找并启动 Edge

```powershell
# 先检查并关闭旧进程
try { Invoke-WebRequest -Uri "http://localhost:9022/json/version" -TimeoutSec 2 } catch { taskkill /F /IM msedge.exe 2>$null; Start-Sleep -Seconds 2 }

# 启动 Edge
Start-Process "C:\Program Files\Microsoft\Edge\Application\msedge.exe" -ArgumentList "--remote-debugging-port=9022"
```

---

## 📊 判断结果与下一步跳转

### ✅ 启动成功

**输出示例**：
```json
{
   "Browser": "Edg/...",
   "Protocol-Version": "1.3",
   ...
}
```

**👉 下一步**：读取 `steps/04-connect-cdp.md` 建立 CDP 连接。

---

### ❌ 启动失败

**输出示例**：无输出或连接拒绝

**处理**：
1. 检查日志：`cat /tmp/edge-cdp.log`
2. 等待旧进程完全退出（多等几秒）
3. 重新执行启动命令