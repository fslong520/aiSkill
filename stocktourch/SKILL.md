---
name: StockLab
version: 2.0.0
description: A股智能分析系统，支持实时行情、技术分析、财务分析、行业分类和大盘分析
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion

metadata:
  trigger: 股票分析、技术指标、财务分析、大盘分析、资金流向、同业对比、A股、股票
---

## Keywords

股票分析, 技术指标, 财务分析, 大盘分析, 资金流向, 同业对比, A股, 股票, MA, RSI, MACD

## Summary

从baostock和AKShare获取A股数据，提供技术分析（MA/RSI/MACD/KDJ）、财务分析、同业对比、资金流向、大盘分析等功能，生成投资决策报告。

## Strategy
1. 识别意图：股票代码 + 分析类型（技术/财务/综合/大盘）
2. 执行脚本：`python3 <技能根目录>/run_skill.py <代码> <类型>`
3. 财务分析：调用`core/financial_analyzer.py`获取AKShare数据
4. 网络搜索：使用search_web获取最新公告、行业动态
5. 综合分析：融合技术面、基本面、财务面、新闻面
6. 生成报告：Markdown格式，文件名含时间戳

AVOID:
- AVOID 技术数据不注明时间，必须标注"截至[最新交易日]收盘"
- AVOID 财报数据不注明报告期，必须标注"基于[最新财报报告期]"
- AVOID 网络搜索用模糊时间词（最近/近期），必须用具体日期
- AVOID 跳过财务分析直接给结论，必须调用financial_analyzer

---

## 命令速查

| 分析类型 | 命令示例 | 说明 |
|---------|---------|------|
| 综合分析 | `python3 run_skill.py 000001 comprehensive` | 技术面+基本面+新闻面 |
| 技术分析 | `python3 run_skill.py 000001 technical` | MA/RSI/MACD/KDJ |
| 财务分析 | `python3 run_skill.py 600036 finance` | 三大报表深度分析 |
| 同业对比 | `python3 run_skill.py 002050 compare_peers` | 行业横向对比 |
| 资金流向 | `python3 run_skill.py 002050 capital_flow` | 主力/北向资金 |
| 大盘分析 | `python3 run_skill.py market report` | 市场走势分析 |
| 多周期 | `python3 run_skill.py 002050 technical --period daily_weekly_monthly` | 日/周/月线联合 |

**股票代码格式**：`000001`、`sh.600036`、`hs300`（指数）

## 核心流程

### 个股综合分析

1. **技术数据**：执行脚本获取基本信息、技术指标、基本面数据
2. **财务数据**：调用`get_comprehensive_financial_report()`获取三大报表
3. **财报分析**：按`report/读财报.md`方法论分析（审计意见→资产负债表→利润表→现金流→造假风险→杜邦分析）
4. **网络搜索**：search_web获取公告、行业动态、分析师观点
5. **融合分析**：技术面+基本面+财务面+新闻面综合评分
6. **生成报告**：保存到`reports/`目录，文件名`{股票名}_分析报告_YYYYMMDD.md`

### 大盘分析

1. 判断时间：开盘前/交易中/收盘后
2. 搜索行情：`{日期} A股收盘 上证指数 深证成指 创业板指`
3. 整合信息：指数表现、板块热点、资金流向、市场情绪
4. 生成报告：适合公众号发布的Markdown格式

## 评分模型

| 维度 | 权重 | 说明 |
|------|------|------|
| 基本面 | 35% | PE/PB/ROE等 |
| 技术面 | 25% | 均线/指标/形态 |
| 财务面 | 25% | 三大报表质量 |
| 资金流 | 10% | 主力/北向资金 |
| 情绪面 | 5% | 市场情绪评估 |

**风险等级**：9-10分低风险 | 7-8分中低风险 | 5-6分中高风险 | 3-4分高风险 | 1-2分极高风险

## 时效性铁律

| 数据类型 | 时效要求 | 示例 |
|---------|---------|------|
| 技术数据 | 最新交易日 | "截至2026-04-21收盘" |
| 财报数据 | 报告期 | "基于2025年三季报" |
| 网络信息 | 具体日期 | "据2026-04-22证券时报报道" |
| 搜索查询 | 计算时间范围 | "2026年4月以来"、"近5个交易日(0415-0421)" |

## 项目结构

```
stocktourch/
├── run_skill.py          # 入口脚本
├── core/
│   ├── stock_analyzer.py      # 股票分析器
│   ├── financial_analyzer.py  # 财务分析器（AKShare）
│   └── market_analyzer.py     # 大盘分析器
├── report/
│   └── 读财报.md            # 财报分析方法论
└── web/
    └── web_crawler.py       # 网页爬虫
```

## 依赖安装

```bash
python3 -m pip install baostock pandas numpy akshare --break-system-packages
```

## 详细文档

- [财报分析方法论](report/读财报.md)
- [API参数详解](docs/api.md)
