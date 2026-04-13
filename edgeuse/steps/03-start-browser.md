# Step 4: 定位并启动浏览器

## 🎯 目标

根据操作系统找到浏览器并启动 CDP 模式。

**优先级**：Edge（首选）→ Chrome（备选）

---

## 🚨 铁律（非常重要！）

1. **启动前必须检查旧进程！** 
   - 如果浏览器已打开但 **没有开启 9022 端口**，必须关掉旧进程再启动！
   - 因为浏览器机制：已有实例运行时，新启动命令会把 URL 传给旧实例，旧实例没 CDP 就白启动了
   - 检查方法：`curl -s http://localhost:9022/json/version`，如果失败但有浏览器进程在跑，说明是旧进程占位
2. **只加 `--remote-debugging-port=9022` 参数！** 不要加其他参数！
   - ❌ 不要加 `--headless`
   - ❌ 不要加 `--disable-gpu`
   - ❌ 不要加 `--no-sandbox`
   - ❌ 不要加 `--disable-dev-shm-uses`
   - ❌ 不要加 `--user-data-dir`（用浏览器默认配置目录）
   - 多余的参数会导致浏览器启动失败或行为异常

---

## 🐧 Linux

### 1. 查找浏览器

```bash
# 查找 Edge
EDGE_PATH=$(ls /opt/microsoft/msedge/msedge 2>/dev/null || which microsoft-edge-stable 2>/dev/null)

# 查找 Chrome（Edge 不可用时）
CHROME_PATH=$(which google-chrome 2>/dev/null || which google-chrome-stable 2>/dev/null || ls /opt/google/chrome/chrome 2>/dev/null)

# 判断使用哪个
if [ -n "$EDGE_PATH" ]; then
  BROWSER=$EDGE_PATH
  BROWSER_NAME="Edge"
elif [ -n "$CHROME_PATH" ]; then
  BROWSER=$CHROME_PATH
  BROWSER_NAME="Chrome"
else
  echo "未找到浏览器！"
  exit 1
fi
```

### 2. 启动浏览器

**⚠️ 启动前先检查：如果 Edge 已打开但没有 9022 端口，必须先关掉！**

```bash
# 检查 CDP 是否已开启
CDP_CHECK=$(curl -s --max-time 2 http://localhost:9022/json/version 2>/dev/null)

if [ -z "$CDP_CHECK" ]; then
  # CDP 未开启，检查是否有 Edge/Chrome 进程在运行
  if pgrep -f "msedge\|chrome" > /dev/null 2>&1; then
    echo "检测到浏览器已运行但未开启 CDP，正在关闭..."
    pkill -f "msedge\|chrome" 2>/dev/null
    sleep 2
  fi
fi
```

**Edge**：
```bash
nohup /opt/microsoft/msedge/msedge \
  --remote-debugging-port=9022 \
  > /tmp/edge-cdp.log 2>&1 &
```

**Chrome**：
```bash
nohup google-chrome \
  --remote-debugging-port=9022 \
  > /tmp/chrome-cdp.log 2>&1 &
```

### 3. 验证启动

```bash
sleep 5
curl -s http://localhost:9022/json/version | head -5
```

如果验证失败（返回为空或连接拒绝）：
- 检查日志：`cat /tmp/edge-cdp.log` 或 `cat /tmp/chrome-cdp.log`
- 可能原因：旧进程未完全退出，等几秒再重试

---

## 🪟 Windows

### 1. 查找浏览器（PowerShell）

```powershell
# 查找 Edge
$edgePaths = @(
  "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
  "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)

# 查找 Chrome
$chromePaths = @(
  "C:\Program Files\Google\Chrome\Application\chrome.exe",
  "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
)

foreach ($p in $edgePaths) { if (Test-Path $p) { $browser = $p; break } }
if (-not $browser) {
  foreach ($p in $chromePaths) { if (Test-Path $p) { $browser = $p; break } }
}
```

### 2. 启动浏览器

**⚠️ 启动前先检查：如果浏览器已打开但没有 9022 端口，必须先关掉！**

```powershell
# 检查 CDP 是否已开启
try {
  $response = Invoke-WebRequest -Uri "http://localhost:9022/json/version" -TimeoutSec 2 -UseBasicParsing
  $cdpOpen = $true
} catch {
  $cdpOpen = $false
}

if (-not $cdpOpen) {
  # CDP 未开启，检查是否有浏览器进程在运行
  if (Get-Process msedge, chrome -ErrorAction SilentlyContinue) {
    Write-Host "检测到浏览器已运行但未开启 CDP，正在关闭..."
    taskkill /F /IM msedge.exe 2>$null
    taskkill /F /IM chrome.exe 2>$null
    Start-Sleep -Seconds 2
  }
}
```

**Edge**：
```powershell
Start-Process "C:\Program Files\Microsoft\Edge\Application\msedge.exe" -ArgumentList "--remote-debugging-port=9022"
```

**Chrome**：
```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9022"
```

### 3. 验证启动

等待 5 秒后访问 `http://localhost:9022/json/version`。如果失败，检查是否有旧进程残留。

---

## 🍎 macOS

### 1. 查找浏览器

```bash
# 查找 Edge
EDGE_PATH="/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

# 查找 Chrome
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 判断
if [ -f "$EDGE_PATH" ]; then
  BROWSER="$EDGE_PATH"
  BROWSER_NAME="Edge"
elif [ -f "$CHROME_PATH" ]; then
  BROWSER="$CHROME_PATH"
  BROWSER_NAME="Chrome"
else
  echo "未找到浏览器！"
  exit 1
fi
```

### 2. 启动浏览器

**⚠️ 启动前先检查：如果浏览器已打开但没有 9022 端口，必须先关掉！**

```bash
# 检查 CDP 是否已开启
CDP_CHECK=$(curl -s --max-time 2 http://localhost:9022/json/version 2>/dev/null)

if [ -z "$CDP_CHECK" ]; then
  # CDP 未开启，检查是否有 Edge/Chrome 进程在运行
  if pgrep -f "Microsoft Edge\|Google Chrome" > /dev/null 2>&1; then
    echo "检测到浏览器已运行但未开启 CDP，正在关闭..."
    pkill -f "Microsoft Edge\|Google Chrome" 2>/dev/null
    sleep 2
  fi
fi
```

**Edge**：
```bash
nohup "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  --remote-debugging-port=9022 \
  > /tmp/edge-cdp.log 2>&1 &
```

**Chrome**：
```bash
nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9022 \
  > /tmp/chrome-cdp.log 2>&1 &
```

### 3. 验证启动

```bash
sleep 5
curl -s http://localhost:9022/json/version | head -5
```

如果验证失败，检查日志或等待旧进程完全退出。

---

## ✅ 完成标志

启动成功后，继续 **Step 5** 建立 CDP 连接。
