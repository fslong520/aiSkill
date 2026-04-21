# Step 3: 启动浏览器

## 🎯 目标

启动浏览器并开启 CDP 调试端口 9022。

---

## Linux 启动命令

```bash
# Edge（推荐）
microsoft-edge --remote-debugging-port=9022 --user-data-dir=/tmp/edge-cdp &

# Chrome
google-chrome --remote-debugging-port=9022 --user-data-dir=/tmp/chrome-cdp &

# Chromium
chromium --remote-debugging-port=9022 --user-data-dir=/tmp/chromium-cdp &
```

---

## macOS 启动命令

```bash
# Edge（推荐）
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --remote-debugging-port=9022 --user-data-dir=/tmp/edge-cdp &

# Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9022 --user-data-dir=/tmp/chrome-cdp &

# Chromium
/Applications/Chromium.app/Contents/MacOS/Chromium --remote-debugging-port=9022 --user-data-dir=/tmp/chromium-cdp &
```

---

## ⚡ 启动后验证

```bash
# 等待 2 秒后检测
sleep 2 && curl -s http://localhost:9022/json/version | head -3
```

---

## 🚀 验证成功后可执行的操作

```bash
# 打开新网页
curl -s -X PUT "http://localhost:9022/json/new?https://example.com"

# 查看所有页面
curl -s http://localhost:9022/json/list | jq -r '.[] | select(.type=="page") | "\(.title)\n   \(.url)"'
```

---

## ⚠️ 注意事项

- `--user-data-dir` 指定临时目录，避免污染默认配置
- `&` 后台运行，不阻塞终端
- 首次启动可能需要几秒钟
