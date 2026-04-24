# Stock Research Skill v2.0

> A股智能分析系统 - 企业级配置

## 🚀 特性概览

### 核心功能
- ⚡ **实时行情**: 获取A股实时股价、涨跌幅、成交量等
- 🧠 **智能缓存**: 自动缓存减少重复请求
- 📊 **技术分析**: MA、RSI、MACD、KDJ等技术指标
- 💰 **财务分析**: 资产负债表、现金流量表、利润表分析
- 📈 **量化评分**: 多维度评分模型，提供操作建议
- 🌐 **行业分类**: 获取股票行业分类及指数成分股

### 数据源
| 数据源 | 说明 |
|--------|------|
| Baostock | A股历史与实时数据 |
| 证监会行业分类 | 行业归属分析 |
| 沪深300 | 指数成分股 |
| 上证50 | 指数成分股 |
| 中证500 | 指数成分股 |

---

## 📦 安装

### 基础安装
```bash
# 仅核心功能
pip install baostock pandas numpy matplotlib seaborn
```

### 完整安装（推荐）
```bash
# 安装所有依赖
pip install -r requirements.txt

# 或单独安装可选依赖
pip install baostock pandas numpy matplotlib seaborn peewee requests
```

---

## 🎯 快速开始

### 基础用法
```bash
# 分析单只股票
python3 run_skill.py 000001

# 获取股票技术分析
python3 run_skill.py 000001 technical

# 获取股票基本面分析
python3 run_skill.py 000001 fundamental

# 获取沪深300成分股
python3 run_skill.py hs300
```

### 输出格式
```bash
# JSON 格式
python3 run_skill.py 000001 --format json

# CSV 格式
python3 run_skill.py hs300 --format csv

# 文本格式（默认）
python3 run_skill.py 000001 --format text
```

---

## 🔧 高级功能

### 1. 缓存控制
```bash
# 禁用缓存
python3 run_skill.py 000001 --no-cache

# 设置缓存TTL为12小时
python3 run_skill.py 000001 --cache-ttl 12
```

### 2. 分析类型
```bash
# 行业分类分析
python3 run_skill.py 000001 industry

# 财务数据分析
python3 run_skill.py 000001 finance

# 现金流量分析
python3 run_skill.py 000001 cashflow

# 利润表分析
python3 run_skill.py 000001 income
```

### 3. 性能选项
```bash
# 详细日志
python3 run_skill.py 000001 --verbose
```

---

## 📊 分析能力

### 技术指标
- **移动平均线**: MA5, MA10, MA20, MA30
- **动量指标**: RSI, MACD, KDJ
- **支撑压力**: 自动识别支撑位和压力位
- **趋势分析**: 均线排列趋势判断

### 评分模型
- **基本面评分** (40%): ROE、PE、PB、增长率
- **技术面评分** (35%): RSI、MACD、均线趋势
- **情绪面评分** (25%): 资金流向、市场热度
- **综合评分**: 加权计算总分

### 操作建议
- **买入建议**: 技术面强势+基本面良好+市场情绪积极
- **卖出建议**: 技术面破位+基本面恶化+市场情绪转差
- **持有建议**: 震荡行情或不确定性强时建议持有

---

## 📋 指数成分股

### 支持的指数
- `hs300` - 沪深300成分股
- `sz50` - 上证50成分股  
- `zz500` - 中证500成分股

```bash
# 获取沪深300成分股
python3 run_skill.py hs300

# 获取上证50成分股
python3 run_skill.py sz50

# 获取中证500成分股
python3 run_skill.py zz500
```

---

## 📊 输出示例

### JSON 输出
```json
{
  "code": "sz.000001",
  "industry": "J66货币金融服务",
  "industry_code": "平安银行",
  "classification": "证监会行业分类",
  "update_date": "2026-01-26"
}
```

### 文本输出
```
【000001 行业分类】
股票代码: sz.000001
行业名称: J66货币金融服务
行业代码: 平安银行
分类标准: 证监会行业分类
更新日期: 2026-01-26
```

---

## 🔧 配置

### 环境变量
```bash
# 设置日志级别
export STOCK_LOG_LEVEL=DEBUG
```

---

## 📁 项目结构

```
stock-research-skill/
├── stock_analyzer.py     # 核心分析逻辑
├── financial_analyzer.py # 财务数据分析
├── skill_executor.py     # 命令执行器
├── cache_manager.py      # 智能缓存
├── output_formatter.py   # 输出格式化
├── utils.py              # 工具函数
├── run_skill.py          # 主执行脚本
├── requirements.txt      # 依赖
├── SKILL.md             # 技能文档
└── README.md            # 说明文档
```

---

## 🐛 故障排除

### 常见问题

**Q: baostock连接失败**
```bash
pip install baostock
```

**Q: 数据获取缓慢**
```bash
# 使用缓存功能
python3 run_skill.py 000001 --cache-ttl 24
```

**Q: 缓存导致数据过旧**
```bash
# 禁用缓存
python3 run_skill.py 000001 --no-cache
```

---

## 🤝 贡献

欢迎提交问题和改进建议！

---

## 📄 许可

MIT License