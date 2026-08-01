---
name: tldraw 板书工坊
description: "📝 用 tldraw 画板制作学神风格板书——外框围栏、分区清晰、笔记感。适合高校/竞赛风格。"
metadata:
  trigger: 板书、笔记、学神笔记、讲课、知识整理、tldraw画板
---

# 学神风格板书工坊

## Keywords
板书、学神笔记、知识整理、tldraw、笔记风

## Summary
用 tldraw 离线画板做整洁、清晰、有框架感的板书。外框围栏、分区排版、笔记感——像学霸亲手整理的笔记。

## ⚠ 关键提醒

**手动启动 tldraw。** 双击 AppImage 启动后，再使用本技能。

确认 server 就绪：`curl http://localhost:7236/readme` 有返回即 OK。

## Strategy

### 动手之前
1. 定主题：讲什么？分几块？
2. 谋框架：先画外框，再定内部分区
3. 搜图：需要插图的主题提前找图

### 制作流程

| 步 | 做啥 | 参考 |
|----|------|------|
| 1 | 建文档 | modules/02-api.md |
| 2 | 画整体外框 | modules/01-board-design.md |
| 3 | 画标题区 | modules/01-board-design.md |
| 4 | 画内容分区 | modules/01-board-design.md |
| 5 | 填文字+公式 | modules/01-board-design.md |
| 6 | 嵌插图 | modules/02-api.md |
| 7 | 画标注/箭头 | modules/02-api.md |
| 8 | 截屏验收 | modules/02-api.md |

### 板书要诀
- **外框套全部**——整体感，像一页笔记纸
- **标题在顶栏**——类似论文标题区
- **分区用细线**——不用大色块，用细边框或浅底色
- **配色克制**——主色1种 + 灰/黑 + 1种强调色
- **文字工整**——左对齐居多，行距一致
- **留白工整**——边距一致，有呼吸感

## AVOID
- AVOID 用脚本启动 tldraw（手动起）
- AVOID 颜色过多杂乱（克制配色）
- AVOID 没有外框（像散落的卡片）
- AVOID 大色块填充（用细边框更清爽）
- AVOID 花哨装饰（学神笔记不需要星星花边）
- AVOID 直接编辑 .tldraw archive
- AVOID 不留裁量、每步写死

## 模块索引

| 模块 | 内容 |
|------|------|
| modules/01-board-design.md | 📐 学神笔记设计——外框/分区/排版 |
| modules/02-content-templates.md | 📖 各科板书模板 |
| modules/02-api.md | 🔧 tldraw API 参考——建文档/画形状/嵌图 |
| modules/03-workflow.md | ⚙ 工作流与异常恢复 |
| modules/01-server.md | 🚀 服务配置与 tq 助手 |
| modules/04-install.md | ⬇ 安装指南 |
| modules/05-fonts.md | 🅰 字体美化 |
