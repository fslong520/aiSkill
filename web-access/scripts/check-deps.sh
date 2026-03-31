#!/usr/bin/env bash
# 环境检查 + 确保 CDP Proxy 就绪
# 支持 Chrome 和 Edge 浏览器的 CDP 模式

# Node.js
if command -v node &>/dev/null; then
  NODE_VER=$(node --version 2>/dev/null)
  NODE_MAJOR=$(echo "$NODE_VER" | sed 's/v//' | cut -d. -f1)
  if [ "$NODE_MAJOR" -ge 22 ] 2>/dev/null; then
    echo "node: ok ($NODE_VER)"
  else
    echo "node: warn ($NODE_VER, 建议升级到 22+)"
  fi
else
  echo "node: missing — 请安装 Node.js 22+"
  exit 1
fi

# 浏览器调试端口 — 检测 Chrome 和 Edge 的 DevToolsActivePort
BROWSER_RESULT=$(node -e "
const fs = require('fs');
const path = require('path');
const os = require('os');
const net = require('net');

function checkPort(port) {
  return new Promise((resolve) => {
    const socket = net.createConnection(port, '127.0.0.1');
    const timer = setTimeout(() => { socket.destroy(); resolve(false); }, 2000);
    socket.once('connect', () => { clearTimeout(timer); socket.destroy(); resolve(true); });
    socket.once('error', () => { clearTimeout(timer); resolve(false); });
  });
}

// 返回浏览器名称和路径的映射
function browserPortFiles() {
  const home = os.homedir();
  const localAppData = process.env.LOCALAPPDATA || '';
  const result = [];
  
  switch (process.platform) {
    case 'darwin':
      // Chrome
      result.push({ name: 'chrome', path: path.join(home, 'Library/Application Support/Google/Chrome/DevToolsActivePort') });
      result.push({ name: 'chrome', path: path.join(home, 'Library/Application Support/Google/Chrome Canary/DevToolsActivePort') });
      result.push({ name: 'chrome', path: path.join(home, 'Library/Application Support/Chromium/DevToolsActivePort') });
      // Edge
      result.push({ name: 'edge', path: path.join(home, 'Library/Application Support/Microsoft Edge/DevToolsActivePort') });
      result.push({ name: 'edge', path: path.join(home, 'Library/Application Support/Microsoft Edge Beta/DevToolsActivePort') });
      result.push({ name: 'edge', path: path.join(home, 'Library/Application Support/Microsoft Edge Dev/DevToolsActivePort') });
      break;
    case 'linux':
      // Chrome
      result.push({ name: 'chrome', path: path.join(home, '.config/google-chrome/DevToolsActivePort') });
      result.push({ name: 'chrome', path: path.join(home, '.config/google-chrome-beta/DevToolsActivePort') });
      result.push({ name: 'chrome', path: path.join(home, '.config/google-chrome-unstable/DevToolsActivePort') });
      result.push({ name: 'chrome', path: path.join(home, '.config/chromium/DevToolsActivePort') });
      // Edge
      result.push({ name: 'edge', path: path.join(home, '.config/microsoft-edge/DevToolsActivePort') });
      result.push({ name: 'edge', path: path.join(home, '.config/microsoft-edge-beta/DevToolsActivePort') });
      result.push({ name: 'edge', path: path.join(home, '.config/microsoft-edge-dev/DevToolsActivePort') });
      break;
    case 'win32':
      // Chrome
      result.push({ name: 'chrome', path: path.join(localAppData, 'Google/Chrome/User Data/DevToolsActivePort') });
      result.push({ name: 'chrome', path: path.join(localAppData, 'Google/Chrome SxS/User Data/DevToolsActivePort') });
      result.push({ name: 'chrome', path: path.join(localAppData, 'Chromium/User Data/DevToolsActivePort') });
      // Edge
      result.push({ name: 'edge', path: path.join(localAppData, 'Microsoft/Edge/User Data/DevToolsActivePort') });
      result.push({ name: 'edge', path: path.join(localAppData, 'Microsoft/Edge Beta/User Data/DevToolsActivePort') });
      result.push({ name: 'edge', path: path.join(localAppData, 'Microsoft/Edge Dev/User Data/DevToolsActivePort') });
      break;
    default:
      break;
  }
  return result;
}

(async () => {
  // 检测 DevToolsActivePort 文件
  for (const item of browserPortFiles()) {
    try {
      const lines = fs.readFileSync(item.path, 'utf8').trim().split(/\\r?\\n/).filter(Boolean);
      const port = parseInt(lines[0], 10);
      if (port > 0 && port < 65536 && await checkPort(port)) {
        console.log(JSON.stringify({ browser: item.name, port: port }));
        process.exit(0);
      }
    } catch (_) {}
  }

  // 回退：检测常见调试端口
  for (const port of [9222, 9229, 9333]) {
    if (await checkPort(port)) {
      console.log(JSON.stringify({ browser: 'unknown', port: port }));
      process.exit(0);
    }
  }

  process.exit(1);
})();
" 2>/dev/null)

if [ -z "$BROWSER_RESULT" ] || [ "$?" -ne 0 ]; then
  echo "browser: not connected"
  echo ""
  echo "请开启浏览器的远程调试模式："
  echo "  Chrome: 访问 chrome://inspect/#remote-debugging 勾选 Allow remote debugging"
  echo "  Edge:   访问 edge://inspect/#remote-debugging 勾选 Allow remote debugging"
  echo ""
  echo "或者使用命令行启动："
  echo "  Chrome: google-chrome --remote-debugging-port=9222"
  echo "  Edge:   microsoft-edge --remote-debugging-port=9222"
  exit 1
fi

# 解析结果
BROWSER_NAME=$(echo "$BROWSER_RESULT" | node -e "console.log(JSON.parse(require('fs').readFileSync(0,'utf8')).browser)")
BROWSER_PORT=$(echo "$BROWSER_RESULT" | node -e "console.log(JSON.parse(require('fs').readFileSync(0,'utf8')).port)")

echo "browser: $BROWSER_NAME (port $BROWSER_PORT)"

# CDP Proxy — 已运行则跳过，未运行则启动并等待连接
HEALTH=$(curl -s --connect-timeout 2 "http://127.0.0.1:3456/health" 2>/dev/null)
if echo "$HEALTH" | grep -q '"connected":true'; then
  echo "proxy: ready"
else
  if ! echo "$HEALTH" | grep -q '"ok"'; then
    echo "proxy: starting..."
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    node "$SCRIPT_DIR/cdp-proxy.mjs" > /tmp/cdp-proxy.log 2>&1 &
  fi
  for i in $(seq 1 15); do
    sleep 1
    curl -s http://localhost:3456/health | grep -q '"connected":true' && echo "proxy: ready" && exit 0
    [ $i -eq 3 ] && echo "⚠️  浏览器可能有授权弹窗，请点击「允许」后等待连接..."
  done
  echo "❌ 连接超时，请检查浏览器调试设置"
  exit 1
fi