# 输出格式说明

---

## 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `<股票代码>` | - | 6位代码如 000001，或带前缀 sz.000001 | - |
| `--period` | `-p` | 技术分析周期：daily/weekly/monthly/daily_weekly_monthly | daily |
| `--format` | `-f` | 输出格式：text/json/csv | text |
| `--no-cache` | - | 禁用缓存 | 默认启用 |
| `--cache-ttl` | - | 缓存时间（小时） | 24 |
| `--verbose` | `-v` | 详细日志 | 关闭 |
| `--peers` | - | 同业对比指定公司（逗号分隔） | 自动选择 |
| `--flow-type` | - | 资金流类型：main/north/south/all | all |

---

## 输出格式选择

### text（默认）
适合直接阅读，Markdown 格式输出。

### json
适合程序处理，结构化数据输出。
```bash
python3 run_skill.py 000001 --format json
```

### csv
适合导入表格，数据列表输出。
```bash
python3 run_skill.py 000001 --format csv
```

---

## 缓存机制

### 默认行为
- 启用智能缓存
- 缓存 TTL 24 小时
- 相同请求复用缓存数据

### 禁用缓存
```bash
python3 run_skill.py 000001 --no-cache
```

### 自定义 TTL
```bash
python3 run_skill.py 000001 --cache-ttl 1  # 1小时
```

---

## 报告保存

### 文件命名
```
{股票名称}_分析报告_{YYYYMMDD_HHMMSS}.md
```

### 保存目录
```
reports/
```

### 示例
```
reports/平安银行_分析报告_20260330_093000.md
```

---

## 股票代码格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 6位数字 | 000001 | 默认格式 |
| 带交易所前缀 | sz.000001 | baostock 格式 |
| 指数代码 | hs300 | 沪深300成分股 |