#!/bin/bash
# 使用哥哥的现有 Edge 配置启动调试模式浏览器
# 这样就能复用 cookies 和浏览历史，不会被 Cloudflare 判定为机器人！

echo "🚀 使用现有配置启动 Edge 调试模式..."

# 先关闭所有 Edge 进程
echo "📌 关闭现有 Edge 进程..."
pkill -9 -f msedge 2>/dev/null
pkill -9 -f microsoft-edge 2>/dev/null
sleep 3

# 使用哥哥的现有配置目录
PROFILE_DIR="$HOME/.config/microsoft-edge"

echo "📁 使用配置目录：$PROFILE_DIR"
echo ""

# 启动调试模式 - 使用现有配置！
microsoft-edge \
  --remote-debugging-port=9222 \
  --user-data-dir="$PROFILE_DIR" \
  --disable-gpu \
  --no-sandbox \
  &

echo "⏳ 等待浏览器启动..."
sleep 8

# 检查
if pgrep -f "msedge.*9222" > /dev/null; then
  echo ""
  echo "✅ Edge 调试模式已启动！"
  echo ""
  echo "📍 调试端口：http://127.0.0.1:9222"
  echo "💡 现在可以用 Selenium 控制这个浏览器了！"
  echo ""
  echo "📋 Python 连接代码:"
  echo "   from selenium import webdriver"
  echo "   from selenium.webdriver.edge.options import Options"
  echo "   options = Options()"
  echo "   options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')"
  echo "   driver = webdriver.Edge(options=options)"
else
  echo "❌ 启动失败，请检查是否有 Edge 进程在运行"
  pgrep -af edge | head -3
fi
