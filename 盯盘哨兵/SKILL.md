---
name: WatchTower
description: 实时盯盘工具，帮助上班族工作时间查询股票、贵金属价格走势并推送到指定频道
tags: [股票, 盯盘, 财经, 推送, 实时]
icon: 📈
author: 小妹
version: "1.2.0"

metadata:
  trigger: 查股票、盯盘、股价、黄金、白银、期货、指数、实时行情、盯盘哨兵
---

Domain keywords: 查股票, 盯盘, 股价, 黄金, 白银, 期货, 指数, 实时行情

Summary: 查股票/贵金属/期货/指数实时行情，推送到微信。

Strategy:
1. 解析品种 → 名称转代码（黄金→AU，茅台→600519）
2. `urlgo open` 打开东方财富页面
3. `urlgo snapshot` 获取价格数据
4. 生成简报 → `copaw channels send` 推送微信

AVOID:
- AVOID 用 WebFetch 读网页，应该用 urlgo snapshot
- AVOID 不检查 CDP 就操作，先 `urlgo status` 确认
- AVOID 频繁访问同一网站，间隔 1 分钟以上
- AVOID 非交易时间期待实时数据，显示的是收盘价

---

## 品种代码速查

| 品种 | 代码 | URL |
|------|------|-----|
| 沪金主连 | AU | http://quote.eastmoney.com/unify/r/113.aum |
| 沪银主连 | AG | http://quote.eastmoney.com/unify/r/113.agm |
| 螺纹钢 | RB | http://quote.eastmoney.com/unify/r/110.rb1 |
| 铁矿石 | I | http://quote.eastmoney.com/unify/r/110.i1 |
| 原油 | SC | http://quote.eastmoney.com/unify/r/110.sc1 |
| 上证指数 | 000001 | https://quote.eastmoney.com/sh000001.html |
| 创业板指 | 399006 | https://quote.eastmoney.com/sz399006.html |

**股票搜索**: `https://so.eastmoney.com/web/s?keyword={名称或代码}`

## 输出模板

**股票/贵金属**:
```
📊 【{名称}】实时行情
💰 当前：{价格} | 📈 {涨跌幅}% ({涨跌额})
📅 区间：{最低} - {最高}
💡 {简要分析}
⏰ {时间}
```

## 推送配置

```bash
copaw channels send \
  --agent-id default \
  --channel wechat \
  --target-user "o9cq8012x7_zwZtDYePv8bo7qxLM@im.wechat" \
  --target-session "weixin:o9cq8012x7_zwZtDYePv8bo7qxLM@im.wechat" \
  --text "{简报内容}"
```

## 数据源优先级

1. 东方财富网（首选）- 数据全、更新快
2. 新浪财经（备用）
3. Bing搜索（不用百度）
