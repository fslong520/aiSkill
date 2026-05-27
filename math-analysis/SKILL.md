---
name: 数学分析
description: Create Chinese middle-school or high-school math wrong-question explanations as interactive Cornell-note HTML pages. Use when the user asks to analyze a math problem, explain a wrong solution, make a web version of a math note, or mentions 数学分析, 错题, 康奈尔笔记, 二元一次方程组, 集合, 函数, 几何, 初中数学, 高中数学, 沪教版, 人教版, 北师大版, 苏教版, 湘教版, or 浙教版.
---

# 数学分析

## Purpose

Use this skill to turn a student's middle-school or high-school math problem, photo, wrong solution, or short question into a clear Chinese teaching webpage. The default output is a standalone HTML file in Cornell-note style, with Morandi palette switching, text highlighter marks, and student-style margin comments.

## Required inputs

Before teaching, confirm these if the user has not already provided them:

1. 教材版本, such as 沪教版, 人教版, 北师大版, 苏教版, 湘教版, 浙教版.
2. 年级和学期, such as 六年级下, 七年级上, 九年级下.
3. 当前章节或最近知识点.
4. 题目原文, from text or photo.
5. 学生原解, 错解, or the step they got stuck on, from text or photo.

If version, grade, or chapter is missing, ask for it before giving the final explanation. If the user provides enough information in the message or attachments, proceed.

## Knowledge lookup

Before writing the explanation, search or check the corresponding textbook/version/chapter knowledge when internet access is available. If internet access is unavailable or sources are unclear, state that and ask the user for a textbook目录, page photo, or teacher handout.

Keep within the student's current grade and textbook range. Do not introduce advanced methods unless clearly marked as optional and not needed for exams.

## Explanation order

Use this stable order:

1. 判断题目属于初中还是高中内容, and name the grade, chapter, and knowledge points.
2. 用一句话说清楚这道题真正考什么.
3. 列出最基础、最该记住的公式、定理或定义, and when to use them.
4. 分析学生错误: 哪一步错, 为什么错, 下次先看什么.
5. 分步完整解题. Every step says why it is done. Do not skip algebra steps for weak students.
6. When the problem is helped by a picture, add a visual model inside the solution steps. Use simple function graphs, number lines, geometric diagrams, area/length models, set diagrams, or coordinate sketches to show why the algebraic result is true. Do this especially for 集合区间/数轴, 函数与不等式, 二次函数符号, 几何证明, 解析几何, 动点, 最值, 面积, 相似/全等, and probability/counting arrangements. Keep the diagram at the student's level and make it explanatory, not decorative.
7. List at most 3 common traps.
8. Add 1 to 2 non-advanced alternative methods if useful, and say which is best for exams.
9. Summarize the pattern: keywords/conditions/features, what knowledge to think of, and the usual first move.
10. Give 3 same-type mini problems: 基础题, 容易混淆题, 稍微变形题. Each includes 题目, 简短答案, 关键思路.

Tone: like a patient Chinese middle-school math teacher at the blackboard. Use simple, concrete Chinese. Avoid empty praise, corporate words, and translationese.

## Web output contract

Always create a standalone `.html` webpage unless the user explicitly asks for chat-only output.

Recommended path:

`/Users/marsfish/AI/report/<日期>_数学分析_<短题名>.html`

Use the Cornell-note layout:

- Header: title, 教材版本, 年级学期, 章节, and 知识点. Do not put the answer in the keyword/tag chips.
- Left cue column: 考点, 关键公式, 错因提醒, 同类题识别.
- Main note column: 题目区, 错解分析, 正确解法, 易错点, 同类小题.
- Bottom summary: one short paragraph telling the student what to remember.

Visual modeling rules:

- If a problem can be made clearer by a graph, diagram, coordinate sketch, number line, set diagram, area model, or geometric construction, include that visual next to the relevant solution step.
- Put each visual after the algebra step it explains. Add a short caption that tells the student exactly what to look at.
- Prefer inline SVG for generated diagrams because it works in a standalone HTML file. Keep shapes simple: axes, curves, key points, intervals, shaded regions, triangles, circles, auxiliary lines, and labels.
- For coordinate graphs, compute or carefully place key points before drawing. Roots, intercepts, vertices, endpoints, labeled points, and axes must line up with their numeric labels; do not draw a merely approximate curve when the diagram is used to justify the answer.
- For graph/number-line questions, show open/closed endpoints and discrete integer/natural-number points clearly. For geometry questions, show auxiliary lines, equal lengths/angles, and the target relation.
- Do not use decorative charts. Every diagram must answer a teaching question: "Where is the interval?", "Which region is positive?", "Which points are allowed?", "Which lengths/angles correspond?", or "What model is being counted?"

For the HTML UI:

- Use Morandi colors with four selectable themes: 黄, 绿, 蓝, 紫.
- Default to Morandi blue when the user does not choose a color.
- Include a palette switcher that changes CSS variables without reloading the page.
- Include student note tools: the user can select text anywhere in the learning page, including title metadata, cue column, main explanation, exercises, and final summary. A small floating pen toolbar appears beside the selected text, with highlighter colors, comment, and a rightmost targeted undo button. Do not require the user to move to a fixed toolbar to choose highlight color.
- Highlight and comment states must be composable. A student should be able to highlight text first and then add a comment to that same highlighted text, or comment first and then add/change highlight color on the same marked text.
- The floating pen toolbar should not stay visible after the student is done. Hide it and clear its active target when the user clicks normal page content, clicks blank space, presses Escape, or scrolls without an active text selection. It should reappear only when the user selects text or clicks an existing highlight/comment mark.
- Targeted undo should remove the currently selected or clicked highlight/comment mark. It should not only reverse actions by time order.
- Do not include drag-to-draw box controls or rectangular wrong-question boxes from the older version.
- Keep implementation/debug text out of the visible page.
- Keep math readable with plain HTML plus MathJax if formulas are complex. If internet is not available for MathJax, also include readable plain-text formula fallbacks.
- Make the page responsive for desktop and mobile.

For the HTML shell and student-note behavior, use or adapt `assets/cornell-note-template.html`. For output rules and section wording, read `references/cornell-web-output.md` when needed.

## Validation

After creating the HTML:

1. Check the file exists.
2. Open or inspect the HTML enough to confirm it contains the four themes, floating pen toolbar, targeted undo, Cornell sections, and the solved answer. Confirm the answer is not in the top keyword/tag chips.
3. If a local preview server is needed, start one and give the user the URL. If opening the HTML file is enough, provide the absolute file path.
