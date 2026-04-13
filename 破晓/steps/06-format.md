# Step 5: 格式输出（微信友好）

## 🎯 目标

将报告内容格式化为适合微信转发的精美排版。

---

## 📱 微信排版原则

1. **段落要短**：每段不超过 3 行，手机阅读舒适
2. **标题清晰**：用 emoji 和符号区分层级
3. **数据表格**：用 Markdown 表格，微信可正常显示
4. **颜色限制**：微信不支持 HTML 颜色，用 emoji 代替
5. **链接处理**：微信内链接需可点击

---

## 🔧 输出格式

### 方案 A：Markdown（推荐）

**优点**：
- 微信直接支持
- 格式清晰
- 易于复制转发

**模板**：
```markdown
# 🌅 破晓早报 · 2026 年 3 月 13 日 · 星期五

---

## 📈 隔夜外盘

| 指数 | 收盘 | 涨跌幅 |
|------|------|--------|
| 道琼斯 | 45,230.50 | +0.85% |
| 纳斯达克 | 18,920.30 | +1.23% |

> 美股科技股领涨，AI 概念延续强势。

---

## 🔥 今日热点前瞻

### 1. AI 算力板块 ⭐⭐⭐⭐⭐
- **逻辑**：英伟达 GTC 大会今日开幕
- **关注**：中际旭创、工业富联

---

⚠️ **免责声明**：本早报仅供参考，不构成投资建议。
```

---

### 方案 B：HTML（备选）

**优点**：
- 样式更精美
- 可保存为文件
- 适合邮件转发

**模板**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>破晓早报 · 2026 年 3 月 13 日</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 680px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .header .date {
            margin-top: 10px;
            opacity: 0.9;
            font-size: 14px;
        }
        .section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .section h2 {
            margin: 0 0 15px 0;
            font-size: 18px;
            color: #333;
            border-left: 4px solid #667eea;
            padding-left: 12px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
        }
        .up { color: #e74c3c; }
        .down { color: #27ae60; }
        .disclaimer {
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            font-size: 12px;
            color: #856404;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌅 破晓早报</h1>
        <div class="date">2026 年 3 月 13 日 · 星期五</div>
    </div>
    
    <div class="section">
        <h2>📈 隔夜外盘</h2>
        <table>
            <tr><th>指数</th><th>收盘</th><th>涨跌幅</th></tr>
            <tr><td>道琼斯</td><td>45,230.50</td><td class="up">+0.85%</td></tr>
        </table>
    </div>
    
    <div class="disclaimer">
        ⚠️ 本早报仅供参考，不构成投资建议。股市有风险，投资需谨慎。
    </div>
</body>
</html>
```

---

##  视觉设计规范

### 配色方案

| 用途 | 颜色 | 说明 |
|------|------|------|
| 主色 | `#667eea` | 渐变紫色，用于标题 |
| 涨 | `#e74c3c` | 红色，A 股涨用红 |
| 跌 | `#27ae60` | 绿色，A 股跌用绿 |
| 背景 | `#f5f5f5` | 浅灰背景 |
| 卡片 | `#ffffff` | 白色卡片 |
| 文字 | `#333333` | 深灰文字 |
| 提示 | `#fff3cd` | 黄色警告背景 |

### 间距规则

- 段落间距：16px
- 卡片间距：15px
- 标题间距：20px
- 表格行高：40px

---

## 📄 文件保存

**保存路径**：
```
/home/fslong/桌面/破晓_{类型}_{日期}.{格式}

示例：
- /home/fslong/桌面/破晓_早报_20260313.md
- /home/fslong/桌面/破晓_午评_20260313.html
- /home/fslong/桌面/破晓_收盘_20260313.pdf
```

**类型映射**：
- `morning` → `早报`
- `midday` → `午评`
- `closing` → `收盘`

**PDF 导出建议**：
- 使用 `browser_use` 打开 HTML 文件，然后使用 `action="pdf"` 导出，以保证排版完美。
- 或使用命令行工具如 `wkhtmltopdf` 将 HTML 转为 PDF。

---

## ✅ 输出检查清单

- [ ] 日期正确（今日）
- [ ] 格式适合手机阅读（段落短）
- [ ] 表格对齐
- [ ] 涨跌幅颜色正确（A 股红涨绿跌）
- [ ] 免责声明包含
- [ ] 文件已保存
- [ ] 向用户展示核心要点

---

## 📤 展示给用户

```
✅ {报告类型} 已生成！

📅 今日：{日期} {星期}

📊 核心要点：
- {要点 1}
- {要点 2}
- {要点 3}

⚠️ 免责声明：本报告仅供参考，不构成投资建议

📄 文件：{文件路径}
```
