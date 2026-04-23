# Step 1: 实时行情数据抓取（⚠️ 必须先做！）

## 🎯 目标

**必须通过浏览器打开东方财富网页，实时抓取行情数据！不打开网页 = 数据无效！**

---

## 🔴 铁律

### ⚠️ 必须先调用 edgeuse 技能！

**所有网页操作必须先调用 edgeuse 技能建立 CDP 连接！禁止直接调用 browser_use 的 start/open！**

```
✅ 正确流程：
1. 先调用 edgeuse 技能（它会完成 CDP 检测、浏览器启动、CDP 连接）
2. edgeuse 完成后，再使用 browser_use action="navigate/snapshot/screenshot" 执行具体操作

❌ 错误做法：
直接 browser_use action="open" url="xxx"  ← 这会跳过 edgeuse，可能导致 CDP 未连接！
```

### 为什么必须打开网页？

1. **东方财富 API 不可靠**：`push2.eastmoney.com`、`qt.gtimg.cn` 等接口经常返回空 JSON、422 错误、或 `RemoteDisconnected`
2. **搜索结果不准确**：搜索引擎抓取的行情信息可能滞后数小时
3. **记忆数据不可信**：模型记忆中的数据是训练时的快照，不是今日实时数据
4. **用户能一眼看出**：用户每天都在看盘，数据对不对一目了然

### 执行原则

```
✅ 必须：用 edgeuse/browser_use 打开东方财富网页 → 等待页面加载 → snapshot 提取数据
❌ 禁止：调用 API 接口、搜索二手信息、凭记忆/估计写数据
```

### 🔴 铁律：数据清洗与防污染（防止胡编乱造）

**AI 解析 snapshot 时必须遵守的绝对规则：**

1.  **🚫 严禁提取链接**：
    *   如果提取到的内容包含 `http` 或 `https`，**立即丢弃**，这是链接不是数据！
    *   例如：不要把 `https://so.eastmoney.com...` 当作板块名称写入报告。
2.  **🧹 严格清洗文本**：
    *   提取板块名称时，去掉后面的“板块”、“概念”后缀（除非它是专有名词），但绝不要保留 URL 路径。
    *   提取数值时，必须带有明确的单位（如 `亿`、`万`、`%`），裸数字（如 `123062`）通常是错误解析的原始数据，**必须结合上下文确认单位**。
3.  **🔍 交叉验证**：
    *   如果在 A 页面看到成交额是 `1.23 万亿`，在 B 页面看到是 `1230 亿`（单位看错），**必须警惕**！
    *   成交额不可能只有 1000 亿（那是十几年前的数据），也不可能一天 10 万亿。如果数据偏离常识（如上证成交 < 2000 亿 或 > 1.5 万亿），**必须去个股详情页二次确认**。

---

## 🔧 执行步骤

### 💡 技巧：使用“个股详情页”获取精准汇总数据（强烈推荐！）

**之前的“行情中心列表页”数据密集且难以解析，容易出错！**
**建议优先访问以下“指数详情页”获取全市场汇总数据，数据更干净、准确：**

| 指数 | 详情 URL | 优势 |
| :--- | :--- | :--- |
| **上证指数** | `https://quote.eastmoney.com/zs000001.html` | **包含全市场成交额、涨跌家数统计**，无干扰链接 |
| **深证成指** | `https://quote.eastmoney.com/zs399001.html` | 同上，深市数据更准确 |
| **创业板指** | `https://quote.eastmoney.com/zs399006.html` | 同上 |

**操作建议**：
1. 先打开上述详情页（如 `zs000001.html`），`snapshot` 提取页面侧边栏或顶部的"行情数据"（成交额、涨跌家数）。
2. 再去列表页看板块排行（板块名称）。
3. **不要试图从列表页的几千行 HTML 里去加减算总成交额，直接去详情页抄总数！**

### 0. 先调用 edgeuse 技能（必须！）

```
调用 edgeuse 技能 → 等待 CDP 连接建立完成 → 再进行后续操作
```

### 1. 打开东方财富行情中心

```
// edgeuse 已建立连接后，使用 browser_use 执行具体操作
browser_use action="navigate" url="https://quote.eastmoney.com/center/gridlist.html#hs_a_board"
browser_use action="wait_for" wait_time=3  // 等待页面加载
browser_use action="snapshot" → 提取三大指数、涨跌家数、成交额
```

**必须提取的数据**：
- 上证指数：收盘价、涨跌幅、成交额
- 深证成指：收盘价、涨跌幅、成交额
- 创业板指：收盘价、涨跌幅、成交额
- 沪深300：收盘价、涨跌幅（如有）
- 涨跌家数：上涨/下跌/平盘各多少家
- 涨停/跌停家数

### 2. 打开板块排行页面

```
browser_use action="navigate" url="https://quote.eastmoney.com/center/boardrank.html"
browser_use action="wait_for" wait_time=3
browser_use action="snapshot" → 提取板块涨跌排行
```

**必须提取的数据**：
- 涨幅前 5 板块名称及涨跌幅
- 跌幅前 5 板块名称及涨跌幅
- 各板块领涨股及涨幅

### 3. 打开资金流向页面

```
browser_use action="navigate" url="https://data.eastmoney.com/zjlx/dpzjlx.html"
browser_use action="wait_for" wait_time=3
browser_use action="snapshot" → 提取资金流向数据
```

**必须提取的数据**：
- 北向资金（沪股通、深股通）净流入/流出
- 主力资金净流入/流出
- 港股通（沪、深）资金流向

### 4. 大盘星图（热力图）

```
browser_use action="navigate" url="https://quote.eastmoney.com/stockhotmap/"
browser_use action="wait_for" wait_time=3
browser_use action="snapshot" → 提取热力图数据
```

**注意**：
- 该页面可能有滑块验证，遇到验证时跳过，标注"热力图页面遇反爬验证"
- 如能正常加载，提取涨跌家数、涨跌停统计、热门板块聚集

### 5. 东方财富首页（补充资讯）

```
browser_use action="navigate" url="https://www.eastmoney.com/"
browser_use action="wait_for" wait_time=3
browser_use action="snapshot" → 提取热门板块标签、快讯
```

**补充提取**：
- 热门搜索板块（如"锂电池板块领涨"、"半导体板块活跃"）
- 首页快讯摘要

---

## ⚠️ 铁律：涨跌家数汇总（避免重复统计）

**东方财富统计存在包含关系，绝对禁止简单相加！**

### ❌ 错误做法
```
总数 = 上证A股 + 深证A股 + 创业板 + 科创板 + 北交所
```
**原因**：
- 创业板属于深证，科创板属于上证
- 这样叠加会把双创板块重复计算，导致总数飙升至 6500+ 家，远超 A 股实际数量！

### ✅ 正确做法（三选一）
1. **首选（总览数据）**：查看页面顶部是否有"沪深京"或"全市场"汇总栏，直接提取该数据。
2. **次选（公式法）**：`总数 = 上证A股 + 深证A股 + 北交所`
   - ⚠️ **绝对不要加**创业板和科创板数据。
3. **验证法**：A 股上市公司总数约为 5300-5400 家。如果算出 6000+ 家，说明重复统计了。

---

## 📊 数据提取模板

从 snapshot 中提取数据时，使用以下模板整理：

```json
{
  "indices": {
    "sh_index": {"value": "3988.56", "change": "+2.34", "pct": "+0.06%"},
    "sz_index": {"value": "14407.86", "change": "+98.39", "pct": "+0.69%"},
    "cyb_index": {"value": "3476.44", "change": "+27.65", "pct": "+0.80%"}
  },
  "market_breadth": {
    "up_count": 2326,
    "down_count": 1089,
    "flat_count": 200,
    "limit_up": 45,
    "limit_down": 8
  },
  "top_sectors": [
    {"name": "锂电池", "pct": "+3.2%"},
    {"name": "能源金属", "pct": "+2.8%"},
    {"name": "半导体", "pct": "+1.5%"}
  ],
  "capital_flow": {
    "northbound": "+35.2亿",
    "southbound_sh": "+41.85亿",
    "southbound_sz": "-18.4亿"
  },
  "hot_keywords": ["锂电池板块领涨", "能源金属板块领涨", "半导体板块活跃"]
}
```

---

## ⚠️ 常见问题

### Q: 页面加载很慢怎么办？

**A**: 增加 `wait_for` 等待时间到 5 秒。东方财富页面是动态渲染的，需要等 JS 执行完毕。

### Q: snapshot 抓不到数据？

**A**: 
1. 检查是否进入了正确的 URL
2. 页面可能在 iframe 中，尝试 `frame_selector="iframe"` 再 snapshot
3. 多等几秒再 snapshot
4. 如实在无法获取，在报告中标注"该数据页面暂未获取"，不要编造

### Q: 大盘星图页面有滑块验证？

**A**: 跳过该页面，在报告中说明"热力图页面遇反爬验证，以下基于行情中心数据推断"。不要编造热力图数据。

### Q: 数据和我知道的不一样？

**A**: 以网页实时数据为准！如果你记忆中的数据与网页不符，说明记忆中的数据是旧的。

### Q: 涨跌家数加起来超过 6000 家？

**A**: **重复统计了！**
- 检查是否把创业板、科创板的数据重复加到了上证、深证中
- 正确算法：上证 + 深证 + 北交所（去掉双创）
- 详见上方"铁律：涨跌家数汇总"

---

## 📌 页面 URL 汇总

| 页面 | URL | 用途 |
|------|-----|------|
| 行情中心 | `https://quote.eastmoney.com/center/gridlist.html#hs_a_board` | 三大指数、涨跌家数 |
| 板块排行 | `https://quote.eastmoney.com/center/boardrank.html` | 板块涨跌排行 |
| 资金流向 | `https://data.eastmoney.com/zjlx/dpzjlx.html` | 北向/主力资金 |
| 大盘星图 | `https://quote.eastmoney.com/stockhotmap/` | 热力图（可能遇验证） |
| 东方财富首页 | `https://www.eastmoney.com/` | 热门板块、快讯 |
| 沪深指数 | `https://quote.eastmoney.com/center/hszs.html` | 指数行情 |
