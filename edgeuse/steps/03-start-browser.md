# Step 4: 定位并启动浏览器

## 🎯 目标

根据操作系统找到浏览器并启动 CDP 模式。

**优先级**：Edge（首选）→ Chrome（备选）

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

**Edge**：
```bash
pkill -9 -f msedge 2>/dev/null
sleep 2
nohup /opt/microsoft/msedge/msedge \
  --remote-debugging-port=9022 \
  --user-data-dir="$HOME/.config/msedge" \
  --disable-gpu --no-sandbox \
  > /tmp/edge-cdp.log 2>&1 &
```

**Chrome**：
```bash
pkill -9 -f chrome 2>/dev/null
sleep 2
nohup google-chrome \
  --remote-debugging-port=9022 \
  --user-data-dir="$HOME/.config/chrome" \
  --disable-gpu --no-sandbox \
  > /tmp/chrome-cdp.log 2>&1 &
```

### 3. 验证启动

```bash
sleep 3
curl -s http://localhost:9022/json/version | head -5
```

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

**Edge**：
```powershell
Start-Process "C:\Program Files\Microsoft\Edge\Application\msedge.exe" -ArgumentList "--remote-debugging-port=9022"
```

**Chrome**：
```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9022"
```

### 3. 验证启动

等待 5 秒后访问 `http://localhost:9022/json/version`

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

**Edge**：
```bash
pkill -9 -f "Microsoft Edge" 2>/dev/null
sleep 2
nohup "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  --remote-debugging-port=9022 \
  --user-data-dir="$HOME/Library/Application Support/Microsoft Edge" \
  > /tmp/edge-cdp.log 2>&1 &
```

**Chrome**：
```bash
pkill -9 -f "Google Chrome" 2>/dev/null
sleep 2
nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9022 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome" \
  > /tmp/chrome-cdp.log 2>&1 &
```

### 3. 验证启动

```bash
sleep 3
curl -s http://localhost:9022/json/version | head -5
```

---

## ✅ 完成标志

启动成功后，继续 **Step 5** 建立 CDP 连接。
