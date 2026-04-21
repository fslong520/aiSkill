# CDP HTTP API 完整参考

## 📌 基础 API

| API | 方法 | 说明 |
|-----|------|------|
| `/json/version` | GET | 获取浏览器版本信息 |
| `/json/list` | GET | 获取所有页面列表 |
| `/json/new?<URL>` | PUT | 打开新页面 |
| `/json/activate/<ID>` | GET | 激活页面 |
| `/json/close/<ID>` | PUT | 关闭页面 |

---

## 🚀 常用操作

### 检测 CDP

```bash
curl -s http://localhost:9022/json/version
```

### 打开网页

```bash
curl -s -X PUT "http://localhost:9022/json/new?https://www.baidu.com"
```

### 查看页面列表

```bash
curl -s http://localhost:9022/json/list | jq -r '.[] | select(.type=="page") | "\(.id | .[0:8]) \(.title)"'
```

### 激活页面

```bash
curl -s "http://localhost:9022/json/activate/<FULL_PAGE_ID>"
```

### 关闭页面

```bash
curl -s -X PUT "http://localhost:9022/json/close/<FULL_PAGE_ID>"
```

---

## ⚠️ 重要提示

1. **打开网页必须用 PUT 方法**
2. **页面 ID 很长**，建议用变量保存
3. **URL 中的特殊字符需要编码**
