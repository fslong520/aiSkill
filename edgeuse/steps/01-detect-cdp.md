# Step 1: 检测 CDP 端口

## 🎯 目标

检测 9022 端口是否已有浏览器在监听。

## 🔧 命令

```bash
curl -s http://localhost:9022/json/version 2>/dev/null | head -5
```

## 📊 判断结果

### 端口已开启（CDP 已运行）

**输出示例**：
```json
{
   "Browser": "Edg/146.0.3856.97",
   "Protocol-Version": "1.3",
   ...
}
```

**下一步**：跳到 Step 5 建立 CDP 连接。

---

### 端口未开启

**输出示例**：
```
curl: (7) Failed to connect to localhost port 9022
```

或无输出。

**下一步**：继续 Step 2 断开旧连接，然后 Step 3 检测操作系统。

---

## ⚡ 快速判断

```bash
# 返回 0 = 已开启，返回 1 = 未开启
curl -s http://localhost:9022/json/version >/dev/null 2>&1 && echo "CDP已开启" || echo "CDP未开启"
```
