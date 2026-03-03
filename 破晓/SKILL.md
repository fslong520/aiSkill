---
name: 破晓
description: 聚合全球资讯，智能评分筛选，生成结构化日报。支持个性化定制、机会嗅探、股票标的联动分析。适合学习者、从业者、投资人每日跟踪行业动态。
---

# 破晓 - 智能资讯日报生成器

## 执行流程

### 🎯 第一步：询问用户偏好

**使用 ask_user_question 工具询问用户：**

```json
{
  "questions": [
    {
      "question": "你想生成哪个领域的日报？（可多选）",
      "header": "领域选择",
      "multiSelect": true,
      "options": [
        {"label": "AI科技", "description": "大模型、算法、芯片、机器人"},
        {"label": "新能源汽车", "description": "电动车、电池、自动驾驶"},
        {"label": "半导体", "description": "芯片、晶圆、光刻机"},
        {"label": "医药生物", "description": "创新药、医疗器械、CXO"},
        {"label": "互联网", "description": "平台、电商、社交、游戏"},
        {"label": "新能源", "description": "光伏、风电、储能"},
        {"label": "金融科技", "description": "支付、区块链、保险"},
        {"label": "消费", "description": "食品饮料、零售、美妆"}
      ]
    }
  ]
}
```

### 🔍 第二步：抓取新闻资讯

**使用 search_web 工具查询用户选择领域的新闻：**

```python
from datetime import datetime

# 获取今天日期
today = datetime.now()
date_str = today.strftime("%Y年%m月%d日")  # 例如：2026 年 03 月 04 日

# 根据用户选择的领域构造搜索词（包含今天日期确保时效性）
keywords = {
    "AI 科技": f"AI 人工智能 大模型 {date_str}",
    "新能源汽车": f"新能源车 电动车 自动驾驶 {date_str}",
    "半导体": f"芯片 半导体 晶圆 {date_str}",
    "医药生物": f"医药 生物 创新药 {date_str}",
    "互联网": f"互联网 科技 平台 {date_str}",
    "新能源": f"光伏 风电 储能 {date_str}",
    "金融科技": f"金融科技 数字货币 支付 {date_str}",
    "消费": f"消费 零售 食品饮料 {date_str}"
    "地产": f"地产 房地产 住房 {date_str}"
}

# 使用 search_web 工具（带时间限制确保时效性）
search_web(
    query=f"{keywords[user_choice]}",
    timeRange="OneDay"  # 最近 24 小时
)
```

**时间范围参数：**
- `OneDay`：最近24小时
- `OneWeek`：最近一周

### 📊 第三步：分析标的与影响

**对每条新闻进行分析：**

1. **提取关键信息**：新闻核心内容是什么？
2. **判断影响方向**：利好还是利空？
3. **识别关联标的**：涉及哪些公司/行业？
4. **分析影响逻辑**：为什么会有影响？

**股票标的映射：**

| 领域 | A股标的 | 美股标的 |
|-----|---------|---------|
| AI科技 | 寒武纪、海光信息、浪潮信息 | NVDA、AMD、MSFT |
| 新能源汽车 | 比亚迪、宁德时代、小鹏 | TSLA |
| 半导体 | 中芯国际、中际旭创 | AMAT、LAM |
| 医药生物 | 恒瑞医药、药明康德 | PFE、MRNA |
| 互联网 | 阿里巴巴、腾讯 | GOOGL、META |
| 新能源 | 隆基绿能、阳光电源 | ENPH、SEDG |
| 金融科技 | 恒生电子、东方财富 | SQ、PYPL |
| 消费 | 贵州茅台、五粮液 | KO、PG |

### 🎯 第四步：机会嗅探

**分析A股相关标的：**

```markdown
### 📈 利好信号
- **新闻要点**：[提取关键信息]
- **受益板块**：[相关行业/概念]
- **利好标的**：
  - A股：[股票代码+名称]
- **逻辑链**：[为什么利好]

### 📉 利空信号
- **新闻要点**：[提取关键信息]
- **受损板块**：[相关行业/概念]
- **利空标的**：
  - A股：[股票代码+名称]
- **逻辑链**：[为什么利空]
```

**利好信号关键词**：突破、首发、领先、创新、融资、增长、超预期、获批、订单

**利空信号关键词**：监管、处罚、下架、亏损、裁员、竞争、替代、预警

### 🚀 第五步：生成炫酷AI日报

**生成现代化HTML日报：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【破晓日报】{{date}}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --accent-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            --dark-bg: #0f172a;
            --card-bg: rgba(255, 255, 255, 0.08);
        }
        
        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--dark-bg);
            color: #f1f5f9;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(102, 126, 234, 0.15) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(245, 87, 108, 0.15) 0%, transparent 20%);
        }
        
        .header {
            text-align: center;
            padding: 3rem 2rem;
            background: var(--primary-gradient);
        }
        
        .news-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 1.5rem;
        }
        
        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        }
        
        .news-link {
            color: #f1f5f9;
            text-decoration: none;
            font-weight: 600;
        }
        
        .news-link:hover {
            color: #667eea;
        }
        
        .stock-tag {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }
        
        .stock-tag.bullish {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: #0f172a;
        }
        
        .stock-tag.bearish {
            background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
            color: #fff;
        }
        
        @media (max-width: 768px) {
            .header { padding: 2rem 1rem; }
            .news-card { padding: 1.5rem; }
        }
    </style>
</head>
<body>
    <!-- 炫酷新闻卡片区域 -->
</body>
</html>
```

**日报核心结构：**

```markdown
# 【破晓日报】YYYY-MM-DD

## 🔥 今日焦点 TOP3
[三列卡片布局，每卡包含：标题、标签、摘要、阅读更多链接]

## 📰 热门资讯
[3x3 网格布局，按领域分类展示]
- AI 科技（3 条新闻）
- 新能源汽车（3 条新闻）
- 半导体（3 条新闻）
- 医药生物（3 条新闻）
- 互联网（3 条新闻）
- 新能源（3 条新闻）
- 金融科技（3 条新闻）
- 消费（3 条新闻）
- 地产（3 条新闻）

## 🎯 机会嗅探

### 📈 利好标的
| 新闻 | 受益板块 | A 股标的 | 逻辑 |
|-----|---------|--------|-----|
| xxx | xxx | 代码 + 名称 | xxx |

### 📉 利空标的
| 新闻 | 受损板块 | A 股标的 | 逻辑 |
|-----|---------|--------|-----|
| xxx | xxx | 代码 + 名称 | xxx |

## 📊 股票速查
| 代码 | 名称 | 信号 | 相关新闻 |
|-----|-----|-----|---------|
```

---

**✨ 核心特性：**
- 🎯 个性化定制，按需抓取
- 🌐 可点击链接直达原文
- 🎨 炫酷HTML设计，现代化渐变风格
- 📱 移动端适配
- 🔍 机会嗅探，精准A股标的
