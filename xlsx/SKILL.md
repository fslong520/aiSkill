---
name: xlsx
description: 创建、读取、编辑Excel文件(.xlsx/.xlsm/.csv)，支持公式、格式化、图表等
license: Proprietary
---

Domain keywords: Excel, xlsx, 表格, 公式, 数据分析, pandas, openpyxl

Summary: pandas用于数据分析，openpyxl用于公式和格式化，必须用Excel公式而非Python计算值。

Strategy:
1. 选择工具：pandas分析数据，openpyxl处理公式/格式
2. 创建/加载文件
3. 添加数据、公式、格式
4. 保存文件
5. 重新计算公式（scripts/recalc.py）

AVOID:
- AVOID 用Python计算后硬编码值，必须用Excel公式
- AVISION 公式错误(#REF!/#DIV/0!)，必须验证引用
- AVOID 用data_only=True保存，公式会丢失
- AVOID 不运行recalc.py，公式值不会更新

---

## 快速参考

| 任务 | 工具 |
|------|------|
| 数据分析 | pandas |
| 公式/格式 | openpyxl |
| 公式重算 | scripts/recalc.py |

## 前置依赖

```bash
pip install openpyxl pandas
# LibreOffice (soffice) 用于公式重算
```

## 新建Excel文件

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# 数据
sheet['A1'] = 'Header'
sheet.append(['Row', 'of', 'data'])

# 公式（必须用公式，不要硬编码）
sheet['B10'] = '=SUM(B2:B9)'
sheet['C5'] = '=(C4-C2)/C2'  # 增长率

# 格式
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

## 编辑现有文件

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb.active

sheet['A1'] = 'New Value'
sheet.insert_rows(2)
wb.save('modified.xlsx')
```

## 数据分析（pandas）

```python
import pandas as pd

df = pd.read_excel('file.xlsx')
df.describe()
df.to_excel('output.xlsx', index=False)
```

## 公式重算（必须执行）

```bash
python scripts/recalc.py output.xlsx
```

返回JSON：
```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42
}
```

## 财务模型颜色规范

| 颜色 | 用途 |
|------|------|
| 蓝色(0,0,255) | 硬编码输入 |
| 黑色(0,0,0) | 公式计算 |
| 绿色(0,128,0) | 工作表内链接 |
| 红色(255,0,0) | 外部文件链接 |
| 黄色背景 | 关键假设 |

## 数字格式规范

| 类型 | 格式 |
|------|------|
| 年份 | 文本字符串"2024" |
| 货币 | $#,##0 |
| 百分比 | 0.0% |
| 负数 | 括号(123)而非-123 |
| 零值 | 显示为"-" |

## 公式验证清单

- [ ] 测试2-3个引用是否正确
- [ ] 列映射正确（列64=BL）
- [ ] 行偏移（DataFrame行5=Excel行6）
- [ ] 除法前检查分母
- [ ] 跨表引用用Sheet1!A1格式
- [ ] 运行recalc.py并检查错误

## 关键规则

| 规则 | 说明 |
|------|------|
| 公式优先 | 用=SUM()而非Python计算 |
| 保留公式 | 不要用data_only=True保存 |
| 重算必须 | 每次修改后运行recalc.py |
| 验证错误 | 检查#REF!/#DIV/0!等 |
