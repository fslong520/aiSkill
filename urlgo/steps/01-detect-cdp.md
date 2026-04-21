# Step 1: 检测 CDP 端口

## 🎯 目标

检测 9022 端口是否已有浏览器在监听。

## 🔧 命令

```bash
curl -s http://localhost:9022/json/version 2>/dev/null | head -5
```

## 📊 判断结果与下一步

### ✅ 端口已开启（CDP 已运行）

**输出示例**：
```json
{
   "Browser": "Edg/147.0.3912.60",
   "Protocol-Version": "1.3",
   ...
}
```

**👉 下一步**：直接执行任务（打开网页、查看页面等）

---

### ❌ 端口未开启

**输出示例**：
```
(无输出)
```

**👉 下一步**：读取 `steps/02-detect-os.md` 检测操作系统并启动浏览器

---

## ⚡ 快速判断

```bash
# 一行判断
curl -s http://localhost:9022/json/version >/dev/null 2>&1 && echo "✅ CDP已开启" || echo "❌ CDP未开启"
```

---

## 🚀 CDP 已开启后可直接执行的操作

```bash
# 打开新网页
curl -s -X PUT "http://localhost:9022/json/new?https://example.com"

# 查看所有页面
curl -s http://localhost:9022/json/list | jq -r '.[] | select(.type=="page") | "\(.title)\n   \(.url)"'

# 激活页面
curl -s "http://localhost:9022/json/activate/<PAGE_ID>"

# 关闭页面
curl -s -X PUT "http://localhost:9022/json/close/<PAGE_ID>"
```
