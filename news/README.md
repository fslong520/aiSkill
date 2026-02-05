# News Aggregator Skill v2.0

> 全网热点新闻聚合器 - 企业级配置

## 🚀 特性概览

### 核心功能
- ⚡ **异步并发**: 3-5倍速度提升
- 🧠 **智能缓存**: 自动缓存减少重复请求
- 🔄 **自动重试**: 请求失败自动重试
- 📊 **健康监控**: 实时监控数据源状态
- 🔍 **关键词扩展**: 自动扩展相关术语
- 📋 **订阅模式**: 定时自动推送

### 数据源（10+）
| 数据源 | 说明 |
|--------|------|
| Hacker News | 硅谷技术热点 |
| GitHub Trending | 开源项目趋势 |
| Product Hunt | 新产品发现 |
| 36Kr | 中文科技快讯 |
| 腾讯新闻 | 科技资讯 |
| 华尔街见闻 | 金融动态 |
| V2EX | 开发者社区 |
| 微博热搜 | 社交热点 |
| Reddit | 科技讨论 |
| TechCrunch | 科技新闻 |

---

## 📦 安装

### 基础安装
```bash
# 仅核心功能
pip install -r requirements.txt
```

### 完整安装（推荐）
```bash
# 安装所有依赖
pip install -r requirements.txt

# 或单独安装可选依赖
pip install aiohttp tqdm httpx
```

---

## 🎯 快速开始

### 基础用法
```bash
# 获取所有数据源的前 10 条
python scripts/fetch_news.py

# 获取 Hacker News
python scripts/fetch_news.py --source hackernews

# 获取 AI 相关新闻
python scripts/fetch_news.py --keyword "AI"

# 深度获取文章内容
python scripts/fetch_news.py --source hackernews --deep
```

### 输出格式
```bash
# Markdown 格式
python scripts/fetch_news.py --format markdown

# HTML 格式
python scripts/fetch_news.py --format html
```

---

## 🔧 高级功能

### 1. 交互式模式
```bash
python scripts/fetch_news.py --interactive
```

### 2. 健康监控
```bash
# 查看所有数据源健康状态
python scripts/fetch_news.py --health
```

### 3. 订阅模式
```bash
# 查看订阅状态
python scripts/fetch_news.py --subscription status

# 运行到期订阅
python scripts/fetch_news.py --subscription run
```

### 4. 性能选项
```bash
# 禁用缓存
python scripts/fetch_news.py --no-cache

# 禁用关键词扩展
python scripts/fetch_news.py --no-expand

# 详细日志
python scripts/fetch_news.py --verbose
```

---

## 🧠 智能关键词扩展

系统会自动将简单关键词扩展到整个领域：

```bash
# 输入 "AI" 会自动扩展为：
# AI,LLM,GPT,Claude,Generative,Machine Learning,RAG,Agent,Copilot,LangChain,DeepSeek

python scripts/fetch_news.py --keyword "AI"
```

### 支持的领域
- `AI`, `LLM` - 人工智能
- `Android` - 安卓开发
- `Web` - 前端开发
- `Backend` - 后端开发
- `Python`, `Rust`, `Go` - 编程语言
- `Cloud` - 云计算
- `Database` - 数据库
- `Security` - 安全
- `Finance`, `Crypto` - 金融与加密货币
- `Product` - 产品管理
- `Startup` - 创业

---

## 📋 内置订阅

| 订阅名称 | 数据源 | 频率 | 说明 |
|----------|--------|------|------|
| daily_tech | HN, GitHub, 36Kr, PH | daily | 每日科技新闻 |
| finance_daily | 华尔街见闻, 腾讯 | daily | 每日金融动态 |
| global_scan | 所有源 | daily | 全网扫描 |
| ai_focus | HN, GitHub, PH | hourly | AI 专项追踪 |

---

## 📊 输出示例

### JSON 输出
```json
[
  {
    "source": "Hacker News",
    "title": "OpenAI releases GPT-5",
    "url": "https://...",
    "heat": "450 points",
    "time": "2 hours ago",
    "content": "文章内容..."
  }
]
```

### Markdown 输出
```markdown
# 新闻汇总

*生成时间: 2024-01-20 10:30:00*
*总计 50 条新闻*

## Hacker News

### 1. [OpenAI releases GPT-5](https://...)
🕒 2 hours ago | 🔥 450 points

> 文章摘要...
```

---

## 🔧 配置

### 环境变量
```bash
# 禁用缓存
export NEWS_CACHE_DISABLED=1

# 设置日志级别
export NEWS_LOG_LEVEL=DEBUG

# 禁用异步模式
export NEWS_ASYNC_DISABLED=1
```

### 配置文件
配置存储在 `~/.news-aggregator/subscriptions.json`

---

## 📁 项目结构

```
news-aggregator-skill/
├── config.py           # 配置管理
├── logger.py           # 日志系统
├── cache.py            # 智能缓存
├── retry.py            # 重试机制
├── keywords.py         # 关键词扩展
├── health.py           # 健康监控
├── ui.py               # 用户体验组件
├── subscription.py     # 订阅管理
├── async_fetcher.py    # 异步获取器
├── scripts/
│   └── fetch_news.py   # 主脚本
├── requirements.txt    # 依赖
├── SKILL.md           # 技能文档
├── templates/         # 自定义模板
└── reports/           # 报告输出
```

---

## 🐛 故障排除

### 常见问题

**Q: aiohttp 导入失败**
```bash
pip install aiohttp
```

**Q: 某个数据源总是失败**
```bash
# 查看健康状态
python scripts/fetch_news.py --health

# 系统会自动禁用连续失败的数据源
```

**Q: 缓存导致数据过旧**
```bash
# 禁用缓存
python scripts/fetch_news.py --no-cache
```

---

## 📈 性能对比

| 版本 | 10个源 | 50条新闻 | 深度获取 |
|------|--------|----------|----------|
| v1.0 | ~30s | ~60s | ~120s |
| v2.0 | ~8s | ~15s | ~30s |

**速度提升: 3-4倍**

---

## 🤝 贡献

欢迎提交问题和改进建议！

---

## 📄 许可

MIT License
