---
name: news
version: "2.0.0"
description: "Enhanced news aggregator with async fetching, smart caching, and subscription support. Fetches real-time content from 10+ sources including Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, and more. Use for daily tech briefings, AI/LLM tracking, global hot topics, or deep content analysis."
---

# News Aggregator

全网热点新闻聚合器 - 支持异步并发、智能缓存、健康监控和订阅模式。

## 目标

从多个主流数据源实时获取热点新闻，支持：
- 快速聚合（异步并发，速度提升 3-5 倍）
- 智能过滤（关键词自动扩展）
- 灵活输出（JSON/Markdown/HTML）
- 深度分析（自动获取文章全文）
- 订阅推送（支持定时任务）

## 执行流程

### 1. 识别用户意图

根据用户输入确定：
- **数据源**: 全网扫描 / 特定源 / 组合源
- **过滤条件**: 关键词 / 时间窗口 / 领域
- **输出需求**: 快速预览 / 深度分析 / 格式化报告

### 2. 构建命令

**基础命令模板**:
```bash
python scripts/fetch_news.py --source <数据源> --limit <数量> [选项]
```

**常用场景映射**:

| 用户需求 | 数据源 | 关键参数 |
|---------|--------|----------|
| 每日科技早报 | `hackernews,github,36kr,producthunt` | `--limit 15 --format markdown` |
| AI/LLM 追踪 | `hackernews,github,producthunt` | `--keyword "AI" --deep` |
| 全网热点 | `all` | `--limit 15` |
| 特定源扫描 | 单个源（如 `hackernews`） | `--limit 20` |
| 深度分析 | 任意源 | `--deep --format markdown` |

**智能关键词扩展规则**:
- 用户输入 "AI" → 自动扩展为: `AI,LLM,GPT,Claude,Generative,Machine Learning,RAG,Agent,Copilot,LangChain`
- 用户输入 "Android" → 自动扩展为: `Android,Kotlin,Jetpack Compose,Flutter,Mobile,SDK`
- 用户输入 "Finance" → 自动扩展为: `Finance,FinTech,Trading,Stock,Crypto,Blockchain,DeFi`

### 3. 执行命令

```bash
# 进入技能目录
cd .claude/skills/news

# 执行新闻聚合
python scripts/fetch_news.py [参数]
```

### 4. 处理输出

- 报告自动保存到 `scripts/reports/news_report_YYYYMMDD_HHMM.{md|json|html}`
- 向用户展示关键信息摘要
- 提供深入分析的选项

## 数据源列表

| 参数 | 名称 | 说明 |
|------|------|------|
| `hackernews` | Hacker News | 硅谷技术热点 |
| `github` | GitHub Trending | 开源项目趋势 |
| `producthunt` | Product Hunt | 新产品发现 |
| `36kr` | 36Kr | 中文科技快讯 |
| `tencent` | 腾讯新闻 | 科技资讯 |
| `wallstreetcn` | 华尔街见闻 | 金融动态 |
| `v2ex` | V2EX | 开发者社区 |
| `weibo` | 微博热搜 | 社交热点 |
| `reddit` | Reddit | 科技讨论 |
| `techcrunch` | TechCrunch | 科技新闻 |

## 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--source` | `-s` | 数据源（逗号分隔或 `all`） | `all` |
| `--limit` | `-l` | 每个数据源的条数限制 | `10` |
| `--keyword` | `-k` | 关键词过滤（逗号分隔，自动扩展） | 无 |
| `--deep` | `-d` | 深度获取文章内容 | 关闭 |
| `--format` | `-f` | 输出格式（`json`/`markdown`/`html`） | `json` |
| `--interactive` | `-i` | 交互式配置模式 | 关闭 |
| `--health` | - | 显示数据源健康状态报告 | 关闭 |
| `--subscription` | - | 订阅管理（`status`/`run`/`list`） | - |
| `--no-cache` | - | 禁用智能缓存 | 启用 |
| `--no-expand` | - | 禁用关键词智能扩展 | 启用 |
| `--verbose` | `-v` | 详细日志输出 | 关闭 |

## 示例

### 场景 1: 每日科技早报

**用户输入**: "生成今日科技早报"

**执行命令**:
```bash
python scripts/fetch_news.py --source hackernews,github,36kr,producthunt --limit 15 --format markdown
```

**输出**: Markdown 格式的科技新闻汇总，包含全球头条、开源趋势、产品发现等板块。

---

### 场景 2: AI/LLM 领域深度追踪

**用户输入**: "扫描最近 AI 相关的新闻"

**执行命令**:
```bash
python scripts/fetch_news.py --source hackernews,github,producthunt --keyword "AI" --limit 20 --deep --format markdown
```

**输出**: 深度分析报告，包含文章全文内容摘要，关键词自动扩展到 20+ AI 相关术语。

---

### 场景 3: 全网热点扫描

**用户输入**: "全网扫描最近热点"

**执行命令**:
```bash
python scripts/fetch_news.py --source all --limit 15 --format markdown
```

**输出**: 覆盖所有数据源的热点新闻汇总。

---

### 场景 4: 特定数据源

**用户输入**: "Hacker News 现在有什么热门"

**执行命令**:
```bash
python scripts/fetch_news.py --source hackernews --limit 20
```

**输出**: Hacker News 前 20 条热门内容。

---

### 场景 5: 健康检查

**用户输入**: "检查数据源状态"

**执行命令**:
```bash
python scripts/fetch_news.py --health
```

**输出**: 各数据源的可用性、成功率、平均响应时间等健康指标。

---

### 场景 6: 交互式配置

**用户输入**: "交互式获取新闻"

**执行命令**:
```bash
python scripts/fetch_news.py --interactive
```

**流程**:
1. 选择数据源
2. 输入关键词（可选）
3. 选择输出格式

---

## 订阅模式

内置订阅配置：

| 订阅名称 | 数据源 | 频率 | 说明 |
|----------|--------|------|------|
| `daily_tech` | HN, GitHub, 36Kr, PH | daily | 每日科技新闻 |
| `finance_daily` | 华尔街见闻, 腾讯 | daily | 每日金融动态 |
| `global_scan` | 所有源 | daily | 全网扫描 |
| `ai_focus` | HN, GitHub, PH | hourly | AI 专项追踪 |

**订阅管理**:
```bash
# 查看订阅状态
python scripts/fetch_news.py --subscription status

# 运行到期订阅
python scripts/fetch_news.py --subscription run

# 列出所有订阅
python scripts/fetch_news.py --subscription list
```

## 依赖安装

```bash
# 基础依赖（必需）
python -m pip install -i https://mirrors.aliyun.com/pypi/simple --break-system-packages -r beautifulsoup4
# 完整依赖（推荐）
python -m pip install -i https://mirrors.aliyun.com/pypi/simple --break-system-packages -r requirements.txt 

# 包含:
# - aiohttp >= 3.9.0 (异步支持)
# - tqdm >= 4.66.0 (进度条)
# - httpx >= 0.25.0 (HTTP/2 支持)
```

## 注意事项

1. **首次运行**: 需要先安装依赖 `pip install -r requirements.txt`
2. **缓存机制**: 默认启用 5 分钟缓存，使用 `--no-cache` 禁用
3. **关键词扩展**: 默认启用，使用 `--no-expand` 禁用
4. **报告保存**: Markdown/HTML 格式自动保存到 `scripts/reports/` 目录
5. **编码问题**: Windows 下如遇乱码，脚本已自动处理 UTF-8 编码
