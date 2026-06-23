# 04-create — 创建标准化真题文件

## 文件清单

| 文件 | 必需 | 说明 |
|:-----|:------|:------|
| `{prefix}-真题.md` | ✅ | Markdown 格式试卷 |
| `{prefix}-真题-答案.md` | ✅ | 答案表 |
| `{prefix}-真题.json` | ✅ | JSON 结构化试题 |
| `{prefix}-解析.md` | ❌ | 答案解析（可选） |

其中 `{prefix} = GESP{level}{year}{month}`

## 格式参考

### 真题.md 格式

参照同级别最近一期试卷的 .md 格式。例如三级参照 `GESP三级202512-真题.md`：

```markdown
---
title: "【GESP】C++等级考试{level}级 {year}年{month}月 真题"
description: "GESP {year}{month} C++{level}级 真题"
---

<uyk class="water">

---

# 📐 C++{level}级 真题 — {year}年{month}月

**试卷总分：100分　|　选择题 30分　|　判断题 20分　|　编程题 50分**
```

### 格式规范

- 选择题：`## 第 N 题【知识点】(2分)` + 题目文字 + 四个选项（A/B/C/D）
- 代码用 ````cpp` 围栏
- 判断题：`## 第 N 题` + 题目文字 + 括号加粗问号
- 编程题：按试题名称、时间限制、内存限制、题面描述、输入格式、输出格式、样例、数据范围分段

### 真题-答案.md 格式

```
1. A
2. B
...
15. C
16. T
17. F
...
25. F
26. cpp
27. cpp
```

前15题选择题答案（A/B/C/D），16-25判断题（T/F），26-27编程题占位（cpp）。

### 真题.json 格式

参照同级别现有 .json 文件。结构：

```json
{
  "title": "【GESP】C++等级考试{level}级 {year}年{month}月 真题",
  "description": "GESP C++{level}级真题",
  "time_limit": 40,
  "pass_score": 60,
  "questions": [
    {
      "title": "第 N 题",
      "content": "题目文字",
      "question_type": "single|true_false|programming",
      "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
      "correct_answer": "A|B|C|D|T|F",
      "score": 2,
      "explanation": "解析文字（每题必填，不可留空）"
    }
  ]
}
```

## 答案来源

| 题型 | 来源 |
|:-----|:------|
| 选择题 | PDF 第一页答案表（必须核对） |
| 判断题 | 自行分析（PDF 不提供官方答案） |
| 编程题 | 无标准答案，填 `"参考代码见解析"` |

## JSON 解析要求

每题 `explanation` 字段必填，中文，1-3 句：
- **选择题**：解释为什么正确选项对、错误选项错。涉及代码的简要分析运行逻辑。
- **判断题**：T 说明成立理由；F 说明错在何处、正确说法是什么。
- **编程题**：简述解题思路与核心算法。留空则写 `"待补充"`。

## 编程题超链接

.md 和 .json 的编程题必须附带 OJ 超链接。

**URL 不可自行编造，须询问用户获得。** 用户会提供 OJ 平台地址与格式。

典型格式参考（以用户告知为准）：
```
https://fslong.iok.la/problem/GESP{year}{month}-{level}-T{序号}
```

例如：`GESP202409-4-T1`、`GESP202506-3-T2`

.md 中写作：
```markdown
## 第 26 题 <a href="用户给的URL" target="_blank">26、题目名（25 分）</a>
```

.json 中填写 `"url"` 字段。

## 验证

- [ ] .md 中选择题答案与 PDF 答案表一致
- [ ] .json 是合法 JSON（可用 `python3 -c "import json; json.load(open(...))"` 验证）
- [ ] .json 每题的 `explanation` 非空（不可留 `""`）
- [ ] -答案.md 格式为 `序号. 答案` 每行
- [ ] 三级流程图图片已正确嵌入 .md（`![流程图](xxxx.jpg)`）
