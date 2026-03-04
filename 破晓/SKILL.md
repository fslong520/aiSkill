---
name: 破晓
description: 聚合全球资讯，智能评分筛选，生成结构化日报。包含娱乐吃瓜、投资分析、机会嗅探三大板块，适合投资人、从业者、吃瓜群众每日跟踪行业动态。
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
        {"label": "消费", "description": "食品饮料、零售、美妆"},
        {"label": "地产", "description": "房地产、住房"},
        {"label": "娱乐八卦", "description": "热搜、瓜田、丑闻、争议"}
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
    "消费": f"消费 零售 食品饮料 {date_str}",
    "地产": f"地产 房地产 住房 {date_str}",
    "娱乐八卦": f"热搜 瓜田 丑闻 争议 {date_str}"
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

**股票标的动态搜索：**

不要使用写死的标的映射表！AI 应该根据新闻内容自动搜索相关股票标的：

```python
# 错误示例 - 不要这样做：
fixed_mapping = {
    "AI 科技": "寒武纪、海光信息、浪潮信息",
    "新能源汽车": "比亚迪、宁德时代、小鹏"
}

# 正确做法 - AI 应该：
# 1. 从新闻中提取公司名称（如"英伟达发布新芯片"）
# 2. 使用 search_web 搜索该公司对应的 A 股/美股标的
#    搜索词示例："英伟达 对应 A股 概念股 2026"
#               "特斯拉 供应链 A 股 上市公司"
#               "AI 芯片 龙头股 A 股 2026"
# 3. 从搜索结果中提取股票代码和名称
# 4. 验证标的是否仍在交易（排除退市股票）
```

**搜索策略：**
- **直接关联**：新闻中提到的公司 → 搜索其股票代码
- **产业链关联**：新闻中的行业/概念 → 搜索相关龙头股
- **时效性验证**：搜索时加上年份确保获取最新标的信息
- **市场区分**：明确标注 A股（6 位数字代码）vs 美股（字母代码）

**示例搜索流程：**
```
新闻："特斯拉 FSD V13 发布"
→ 搜索 1："特斯拉 股票代码 A股 供应链 2026"
→ 搜索 2："自动驾驶 概念股 A股 龙头 2026"
→ 提取结果：300750·宁德时代、002594·比亚迪等
→ 验证：确认股票仍在交易中
```

### 🎯 第四步：投资分析与建议

**深度分析框架：**

```markdown
## 💰 投资建议

### 🔥 核心观点
[一句话说清今天最值得关注的投资机会/风险]

### 📊 数据支撑
- 行业数据：[关键指标]
- 资金流向：[主力资金净流入/出]
- 估值水平：[PE/PB历史分位]

### 🎯 操作建议
| 标的 | 方向 | 仓位建议 | 风险提示 |
|-----|-----|---------|---------|
| xxx | 买入/卖出 | 10%-20% | 止损线xxx |

### ⚠️ 风险提示
[明确标注风险因素]
```

**分析要点**：
- 利好信号关键词：突破、首发、领先、创新、融资、增长、超预期、获批、订单
- 利空信号关键词：监管、处罚、下架、亏损、裁员、竞争、替代、预警
- 必须给出具体操作建议，不能只是罗列新闻

### 🍉 第五步：娱乐吃瓜现场

**搜索策略：**
```python
# 搜索今日科技圈/商业圈大瓜
搜索词示例：
- "科技公司 裁员 2026年3月"
- "创始人 争议 热搜 2026"
- "融资 诈骗 跑路 2026"
- "明星 投资 踩坑 2026"
- "公司 内幕 曝光 2026"
```

**吃瓜板块结构：**
```markdown
## 🍉 今日吃瓜

### 热搜大瓜
| 事件 | 热度 | 点评 |
|-----|-----|-----|
| xxx | 🔥🔥🔥 | [一句话锐评] |

### 行业丑闻/争议
- **事件**：[标题]
- **主角**：[公司/人]
- **瓜情回顾**：[100字内]
- **点评**：[毒舌犀利评价]

### 今日神评
[收集网友精彩评论]
```

**吃瓜原则：**
- 真实可信，拒绝谣言
- 角度刁钻，点评犀利
- 把握分寸，不人身攻击

### 🚀 第六步：生成浅色日报

**生成时必须替换的占位符：**
- `{{date}}` → 实际日期（如 2026年3月4日）
- 新闻卡片中的 `href="#"` → 替换为实际新闻链接
- `href="https://example.com"` → 替换为搜索到的原始信源URL

**HTML模板使用说明：**
- 所有 `href="#"` 的链接在生成时必须替换为真实URL
- 投资观点板块的标的和逻辑根据新闻分析动态生成
- 吃瓜板块的热点根据搜索结果填充

**生成浅色主题HTML日报：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【破晓日报】{{date}}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-light: #818cf8;
            --accent: #f59e0b;
            --danger: #ef4444;
            --success: #10b981;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-secondary: #64748b;
            --border: #e2e8f0;
            --shadow: 0 4px 20px rgba(0,0,0,0.08);
            --shadow-hover: 0 12px 40px rgba(79, 70, 229, 0.15);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(79, 70, 229, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(245, 158, 11, 0.05) 0%, transparent 40%);
        }
        
        .container { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem; }
        
        /* 顶部导航 */
        .navbar {
            background: var(--card-bg);
            border-bottom: 1px solid var(--border);
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }
        
        .navbar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-tags {
            display: flex;
            gap: 0.75rem;
        }
        
        .nav-tag {
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .nav-tag:hover { transform: translateY(-2px); }
        .nav-tag.ai { background: #e0e7ff; color: #4338ca; }
        .nav-tag.invest { background: #fef3c7; color: #b45309; }
        .nav-tag.melon { background: #fce7f3; color: #be185d; }
                
        /* 平滑滚动 */
        html { scroll-behavior: smooth; }
        
        /* 投资观点 - 核心板块 */
        .invest-opinion {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
            color: #fff;
            padding: 2.5rem;
            border-radius: 24px;
            margin: 2rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .invest-opinion::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(245, 158, 11, 0.3) 0%, transparent 70%);
        }
        
        .invest-opinion h2 {
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 1rem;
            opacity: 0.9;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .invest-opinion .opinion {
            font-size: 1.85rem;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 1.5rem;
        }
        
        .invest-opinion .opinion strong {
            color: #fbbf24;
        }
        
        .invest-opinion .opinion.bull strong { color: #34d399; }
        .invest-opinion .opinion.bear strong { color: #f87171; }
        
        .action-table {
            width: 100%;
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .action-table table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .action-table th {
            text-align: left;
            padding: 0.75rem 1rem;
            font-size: 0.75rem;
            font-weight: 500;
            opacity: 0.7;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .action-table td {
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .action-table tr:last-child td { border: none; }
        
        .action-table .tag {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
        }
        
        .action-table .tag.buy { background: #34d399; color: #064e3b; }
        .action-table .tag.sell { background: #f87171; color: #7f1d1d; }
        .action-table .tag.watch { background: #60a5fa; color: #1e3a8a; }
        
        /* 板块标题 */
        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin: 2.5rem 0 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--border);
        }
        
        .section-header h2 {
            font-size: 1.35rem;
            font-weight: 700;
        }
        
        .section-header .icon {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }
        
        .section-header .icon.news { background: #e0e7ff; color: #4338ca; }
        .section-header .icon.melon { background: #fce7f3; color: #be185d; }
                
        /* 板块锚点 */
        #ai-section, #auto-section, #finance-section, #pharma-section, #internet-section, #energy-section, #fintech-section, #retail-section, #estate-section, #melon-section {
            scroll-margin-top: 80px;
        }
        
        /* 新闻卡片 */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.25rem;
        }
        
        .news-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .news-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-hover);
            border-color: var(--primary-light);
        }
        
        .news-card .tag {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        
        .news-card .tag.tech { background: #e0e7ff; color: #4338ca; }
        .news-card .tag.auto { background: #d1fae5; color: #065f46; }
        .news-card .tag.finance { background: #fef3c7; color: #92400e; }
        
        .news-card h3 {
            font-size: 1.05rem;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 0.5rem;
            color: var(--text);
        }
        
        .news-card p {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .news-card .meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: #94a3b8;
        }
        
        .news-card .meta a {
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .news-card .meta a:hover {
            color: var(--primary-light);
            text-decoration: underline;
        }
        
        /* 吃瓜板块 */
        .melon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
        }
        
        .melon-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem;
            border-left: 4px solid #f472b6;
        }
        
        .melon-card .hot {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            font-size: 0.75rem;
            color: #f472b6;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .melon-card h4 {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text);
        }
        
        .melon-card .review {
            font-size: 0.85rem;
            color: var(--text-secondary);
            padding: 0.5rem;
            background: #f8fafc;
            border-radius: 8px;
            margin-top: 0.75rem;
            font-style: italic;
        }
        
        /* 风险提示 */
        .risk-notice {
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin: 2rem 0;
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }
        
        .risk-notice i {
            color: #ef4444;
            margin-top: 0.2rem;
        }
        
        .risk-notice p {
            font-size: 0.85rem;
            color: #991b1b;
        }
        
        /* 底部 */
        .footer {
            text-align: center;
            padding: 2rem;
            color: #94a3b8;
            font-size: 0.8rem;
            border-top: 1px solid var(--border);
            margin-top: 3rem;
        }
        
        /* 动画 */
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .news-card, .melon-card { animation: slideIn 0.5s ease-out backwards; }
        .news-card:nth-child(1) { animation-delay: 0.05s; }
        .news-card:nth-child(2) { animation-delay: 0.1s; }
        .news-card:nth-child(3) { animation-delay: 0.15s; }
        
        /* 移动端 */
        @media (max-width: 768px) {
            .navbar .container { flex-direction: column; gap: 0.75rem; }
            .invest-opinion { padding: 1.5rem; }
            .invest-opinion .opinion { font-size: 1.35rem; }
            .news-grid, .melon-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- 顶部导航 -->
    <nav class="navbar">
        <div class="container">
            <div class="logo">破晓日报</div>
            <div class="nav-tags">
                <a href="#invest-opinion" class="nav-tag invest">💰 投资</a>
                <a href="#news-section" class="nav-tag ai">📰 资讯</a>
                <a href="#melon-section" class="nav-tag melon">🍉 吃瓜</a>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <!-- 投资观点 -->
        <section class="invest-opinion">
            <h2><i class="fas fa-bullseye"></i> 今日核心观点</h2>
            <p class="opinion bull">
                <strong>做多</strong> AI算力产业链，关注<strong>国产替代</strong>机会
            </p>
            <div class="action-table">
                <table>
                    <thead>
                        <tr>
                            <th>标的</th>
                            <th>方向</th>
                            <th>仓位</th>
                            <th>逻辑</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>688256·寒武纪</td>
                            <td><span class="tag buy">买入</span></td>
                            <td>15-20%</td>
                            <td>国产AI芯片龙头，订单有望爆发</td>
                        </tr>
                        <tr>
                            <td>002371·北方华创</td>
                            <td><span class="tag buy">买入</span></td>
                            <td>10-15%</td>
                            <td>半导体设备国产替代加速</td>
                        </tr>
                        <tr>
                            <td>688399·季报</td>
                            <td><span class="tag watch">观望</span></td>
                            <td>-</td>
                            <td>业绩承压，等待拐点</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
        
        <!-- 风险提示 -->
        <div class="risk-notice">
            <i class="fas fa-exclamation-triangle"></i>
            <p><strong>风险提示：</strong>本日报仅供娱乐参考，不构成任何投资建议。投资有风险，入市需谨慎。股市专治各种不服，亏钱别来找小妹。</p>
        </div>
        
        <!-- 今日焦点 -->
        <div id="news-section" class="section-header">
            <div class="icon news"><i class="fas fa-fire"></i></div>
            <h2>今日焦点</h2>
        </div>
        
        <div class="news-grid">
            <article class="news-card">
                <span class="tag tech">AI</span>
                <h3>OpenAI GPT-5 真的要来了？内部人士透露下周公布</h3>
                <p>知情人士称新模型在推理能力上有重大突破，可能会改变大模型竞争格局...</p>
                <div class="meta">
                    <span>2 小时前 · The Verge</span>
                    <a href="https://www.theverge.com/ai-models/gpt-5-rumors" target="_blank" rel="noopener noreferrer">阅读全文 →</a>
                </div>
            </article>
            
            <article class="news-card">
                <span class="tag auto">汽车</span>
                <h3>特斯拉FSD V13发布：无图模式表现超越人类司机</h3>
                <p>特斯拉声称最新自动驾驶系统安全性提升40%，但监管机构表示仍需审查...</p>
                <div class="meta">
                    <span>4 小时前 · TechCrunch</span>
                    <a href="https://techcrunch.com/2026/03/04/tesla-fsd-v13" target="_blank" rel="noopener noreferrer">阅读全文 →</a>
                </div>
            </article>
            
            <article class="news-card">
                <span class="tag finance">芯片</span>
                <h3>英伟达H200量产：HBM3e显存提升1.8倍</h3>
                <p>显存带宽达4.8TB/s，大模型推理效率显著提升，利好算力板块...</p>
                <div class="meta">
                    <span>6 小时前 · AnandTech</span>
                    <a href="https://www.anandtech.com/show/nvidia-h200" target="_blank" rel="noopener noreferrer">阅读全文 →</a>
                </div>
            </article>
        </div>
        
        <!-- 吃瓜现场 -->
        <div id="melon-section" class="section-header">
            <div class="icon melon"><i class="fas fa-watermelon"></i></div>
            <h2>吃瓜现场</h2>
        </div>
        
        <div class="melon-grid">
            <article class="melon-card">
                <span class="hot">🔥🔥🔥 热搜第一</span>
                <h4>某AI公司创始人被爆学历造假</h4>
                <div class="review">
                    "PPT做得不错，简历也写得挺好，就是做的事嘛...懂的都懂。建议查查他的LinkedIn，可能比他的产品还精彩。"
                </div>
            </article>
            
            <article class="melon-card">
                <span class="hot">🔥🔥 热议</span>
                <h4>大厂裁员的N+1到底给不给？</h4>
                <div class="review">
                    "赔偿？那得看公司良心。良心这玩意儿吧...跟工资一样，都是数字游戏。唯有劳动仲裁，才是打工人最后的体面。"
                </div>
            </article>
            
            <article class="melon-card">
                <span class="hot">🔥 新瓜</span>
                <h4>投资人diss创业者：你的BP是我看过最烂的</h4>
                <div class="review">
                    "VC这行吧，钱多人精说话直。不服？憋着。毕竟人家真金白银砸钱，错了算你的，对了你得分他一半。这波不亏。"
                </div>
            </article>
        </div>
    </div>
    
    <footer class="footer">
        <p>破晓日报 · 仅供参考 · 娱乐为主 · 投资需谨慎</p>
    </footer>
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
- 💰 **投资建议**：具体操作方向+仓位+逻辑，不只是罗列新闻
- 🍉 **吃瓜现场**：热搜锐评+行业丑闻+神回复，娱乐性拉满
- 📰 **资讯精选**：按领域分类，卡片式展示
- 🎨 **浅色主题**：清新护眼，区分度高
- 📱 移动端适配
