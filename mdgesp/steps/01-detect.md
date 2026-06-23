# 01-detect — 解析用户输入

## 输入格式

用户说"处理2024年9月GESP四级真题"、"下载2025年6月三级"、"真题202506三级"等。

## 解析规则

| 信息 | 提取方式 |
|:-----|:---------|
| year | 四位年号：2024/2025/2026… |
| month | 两位月份：03/06/09/12 |
| level | "一级"、"1级"、"1" → 1，类推 |
| subject | 默认为 C++（GESP 仅 C++/Python） |

## 路径生成

```
dir_name = "GESP{level}级真题"
file_prefix = "GESP{level}{year}{month}"
pdf_path  = "{dir_name}/{file_prefix}.pdf"
txt_path  = "{dir_name}/{file_prefix}.txt"
md_path   = "{dir_name}/{file_prefix}-真题.md"
json_path = "{dir_name}/{file_prefix}-真题.json"
ans_path  = "{dir_name}/{file_prefix}-真题-答案.md"
```

## 参考目录

当前工程根目录下已有：
- `GESP四级真题/`
- `GESP三级真题/`
- `GESP五级真题/`
- `GESP六级真题/`

## 验证

- [ ] year/month/level 均非空
- [ ] 目录 `GESP{level}级真题/` 存在，否则 mkdir
