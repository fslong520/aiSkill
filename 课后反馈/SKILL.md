---
name: 课后反馈
description: 使用urlgo操作OJ网页，查看学生提交代码，分析提交轨迹，生成课后反馈报告
allowed-tools:
  - bash
  - Read
  - Write
  - Edit
  - AskUserQuestion

metadata:
  slug: class-feedback
  trigger: 课后反馈、课后总结、学生表现、课堂反馈、反馈报告
  version: "2.0.0"

---

## Keywords

课后反馈, 学生表现, 代码分析, OJ提交, 课堂评价, 提交轨迹

## Summary

使用urlgo操作OJ状态页，筛选学生提交记录，点"语言"列进详情取代码，分析提交轨迹，生成课后反馈。**必须urlgo操作网页，禁止自行拼接地址**。

## Strategy

1. 询问 OJ 地址 / 学生用户名 / 课程内容
2. 启动浏览器 → 打开状态页（读 `modules/oj-urlgo.md`）
3. 页面筛选作者 → 提取提交记录表
4. 逐题点"语言"列进详情 → 取最终 AC 代码
5. 分析提交轨迹（次数/分数变化/边界条件）
6. 生成报告（读 `modules/report-format.md`）

## 核心配置

| 配置项 | 来源 |
|-------|------|
| OJ地址 | **用户必须提供** |
| 学生用户名 | **用户必须提供** |
| 课程内容 | **用户必须提供** |
| 输出目录 | 用户指定或当前目录 |

## ⚠️ 核心原则

- ❌ 禁止自行拼接 URL / 用 curl / webfetch 直访（Vue SPA 需登录态）
- ❌ 禁止不看代码就写评价
- ✅ 每一步 urlgo 操作，从页面取真实数据
- ✅ 评价必须基于实际代码 + 提交轨迹

## 页面操作要点（细节见 modules/oj-urlgo.md）

1. **浏览器**：`urlgo start` 失败（edge 占用）→ 手动 `chromium --remote-debugging-port=9022`
2. **页面 ID**：每次 `urlgo open` 返回新 ID，后续操作必须用新 ID
3. **筛选**：URL 参数 `?username=xx` 常不生效 → 必须在页面"请输入作者"输入框逐字符触发
4. **进详情**：点行的**语言列**（`td.col_9 span`）才跳 `submission-detail/{id}`；点行/其他列无效
5. **取代码**：`document.body.innerText.match(/include[\s\S]*复制/)`

## 报告生成

**格式与原则见 `modules/report-format.md`**：
- 一、重点知识：只讲知识点，不掺杂评价
- 二、上课情况：基于实际代码 + 提交轨迹评价
- 评价要具体：提交次数、分数变化、卡点（边界条件/模型识别）

---

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 用 curl/webfetch 访问 OJ | urlgo 操作，Vue SPA 需登录态 |
| 用 open 返回的旧页面 ID | 每次 open 后取新 ID |
| URL 带 username 就当筛选过 | 页面输入框逐字符触发筛选 |
| 点行/点 Run ID 进详情 | 点语言列 `td.col_9 span` |
| 不看代码就写评价 | 查看实际代码 + 提交轨迹 |
| 评价泛泛而谈 | 指出提交次数、分数变化、具体卡点 |
| 知识点放学生代码 | 知识点只讲知识点 |

## AVOID

- AVOID 杀用户正在用的 edge（改起 chromium 独立实例）
- AVOID 用 curl/webfetch 直访 OJ（Vue SPA 需登录态）
- AVOID 不看代码就写评价
- AVOID 用旧页面 ID / 相信 URL 参数已筛选
- AVOID 知识点部分掺杂学生评价

---

## 质量检查

- [ ] urlgo 打开状态页并筛选到目标学生
- [ ] 逐题点语言列查看实际代码
- [ ] 记录每题的提交轨迹（次数、分数变化）
- [ ] 重点知识只讲知识点，不掺杂评价
- [ ] 上课情况基于实际代码 + 轨迹
- [ ] 评价简洁（每生一两句）
- [ ] 未自行拼接任何 URL
