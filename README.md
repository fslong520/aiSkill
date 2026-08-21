# 智能体技能库 —— AI 技能合集

> 这里存放了我做的各种 AI 智能体技能，方便 DSH / Claude 等智能体加载使用。
>
> 技能同步发布至 [ClawHub 技能市场](https://clawhub.com)，`clawhub install <slug>` 即可安装。

## 使用方式

### DSH 用户

将技能目录链接或复制到 `~/.dsh/.agent-presets/fslong/skills/` 下，加载对应技能即可使用。

### ClawHub 用户

```bash
clawhub install <slug>
```

### 其他平台

每个技能目录下的 `SKILL.md` 包含完整指令与触发条件，可手动阅读或导入兼容的智能体系统。

---

## 技能清单

### 📚 竞赛与教育

| 目录 | Slug | 版本 | 简介 |
|------|------|------|------|
| 析题 | `xiti` | 1.5.0 | 启发式题解生成，教人思考而非给答案。HTML 产物含题面原文/样例演示/动态可视化动画 |
| 搬题姬 | `ojimport` | — | 从 OJ 平台（AtCoder/Codeforces）搬运题目，生成标准化题包 |
| 命题工坊 | `questlab` | — | 为信息学奥赛生成高质量编程题，注重思维深度与巧妙解法 |
| GESP 作业 | `gesphw` | — | 为 GESP 等级考试生成作业卷子，选择/判断/编程题全覆盖 |
| 备课 | `prepkit` | — | 信息学奥赛培训备课引导框架，基于 ADDIE 教学设计模型 |
| 课后反馈 | `class-feedback` | 2.0.0 | 操作 OJ 网页查看学生提交，分析轨迹生成反馈报告 |
| mdgesp | `mdgesp` | — | GESP 试卷处理：PDF 下载→全文提取→标准化文件 |
| 智国学堂 | `teachzero` | — | 开发和维护智国学堂（TeachZero）Django 教学平台 |
| AI 读书 | `ai-reader` | — | 整本书提炼结构化精华，知识图谱串联，多角色答辩校验 |
| oi 风格 | `oistyle` | — | C++ 代码转信奥竞赛风格（短变量/全局/大括号新行） |
| math-analysis | `math-analysis` | — | 中学数学错题生成交互式康奈尔笔记 HTML 页 |

### ✍️ 内容创作

| 目录 | Slug | 版本 | 简介 |
|------|------|------|------|
| 公众号写手 | `mpwriter` | — | 公众号文章真人写作引擎：挖真实材料，立明确判断，去 AI 腔 |
| 撸树人 | `lupen` | — | 鲁迅式文风公众号推文，批判性与思辨性 |
| 风咏 | `windchant` | — | 古诗词扩写，歌词叙事，可投喂 AI 音乐工具 |
| 风语绘 | `musecard` | — | 自媒体情绪金句插画卡片创作 |
| 笔痕 | `brush-trace` | — | 小说章节配图生成器，角色一致风格统一 |
| 漫语 | `comictale` | — | 长篇小说转哲理四格漫画 |
| 墨染天工 | `inktale` | — | 架空历史小说创作，东方科技体系 |
| 格语 | `gridtale` | — | 宫格手绘故事图生成（4/6/9 宫格） |
| 格知 | `gridknow` | — | 宫格排版科普长图生成 |
| 像素绘 | `pixel-art` | — | 像素艺术 + 彩色 Emoji 合成插图 |
| 图片姬 | `imgmuse` | — | 通用型图像 Prompt 生成器 |
| 雀影 | `queshadow` | — | AI 视频创意伙伴，分镜脚本 + Seedance 提示词 |
| 雀漫 | `vomicgen` | — | 长篇小说转动态漫画分镜脚本（Seedance 2.0） |
| cosprompt | `cosprompt` | — | 结构化 AI 绘图提示词，17 维度双格式输出 |
| 笔记手账 | `note-journal` | — | 手账风格教育知识卡片 Prompt，9 套主题 |
| Agnes 画影 | `agnespaint` | — | 调用 Agnes AI 免费 API 生成图片/视频 |
| 破晓 | `dawn` | 3.0 | 全时段股市资讯生成器，早报/午评/收盘 |
| 盯盘助手 | `stocktourch` | — | A 股智能分析系统，实时行情/技术/财务分析 |
| 炽风 | `blazefan` | — | 通用 EC 风扇调速方法论（不认品牌，只认接口） |

### 🎨 设计与出版

| 目录 | Slug | 版本 | 简介 |
|------|------|------|------|
| pptx | `pptx` | 1.1 | PPTX 文件创建、编辑、转换、提取 |
| docx | `docx` | 1.1 | Word 文档创建、编辑、格式化 |
| pdf | `pdf` | 1.1 | PDF 读取/合并/拆分/水印/OCR/表单 |
| xlsx | `xlsx` | 1.1 | 电子表格处理（创建/编辑/公式/图表） |
| textlogo | `textlogo` | — | 文字 LOGO 设计，AI 生图生成文字图形 |
| tldraw-offline | `tldraw-offline` | — | 学神风格板书——外框围栏、分区清晰、笔记感 |
| qiaomu-ai-prd | `qiaomu-ai-prd` | — | AI 可执行产品需求文档生成 |
| qiaomu-design | `qiaomu-design` | — | 偏执型设计顾问（Jobs 直觉 + Rams 纯粹主义） |

### 🛠 系统与工具

| 目录 | Slug | 版本 | 简介 |
|------|------|------|------|
| urlgo | `urlgo` | — | 连 CDP 浏览器，开网页/截图/执行 JS |
| 系统控制 | `system-ctl` | — | openKylin 3.0 UKUI 桌面系统控制统一入口 |
| 忆时 | `memocap` | 2.3.3 | 记忆胶囊系统——模拟人类记忆检索与联想 |
| 技能诊所 | `skillclinic` | 3.0.0 | 技能诊断优化 + 创建技能 + 评估门禁 |
| clawhub 发布 | `clawhubpub` | — | 一键发布技能到 ClawHub 技能市场 |
| 定时任务 | `cron` | 1.2 | 定时/周期性任务管理 |
| file_reader | `file-reader` | 1.2 | 文本文件读取与摘要 |
| make_plan | `make-plan` | 1.3 | 外部计划请求场景，引导 Agent 获取可执行计划 |
| 穷尽调试 | `pua` | — | 强制穷尽式问题解决（PUA 话术 + 结构化调试） |
| 见自己 | `seeself` | — | 自我探索梳理，生成"AI 眼中的你"分析 |
| AI 剧本杀 | `iseikelife` | — | 回合制异世界人生模拟游戏引擎 |
| EduVid | `eduvid` | — | AI 驱动的教学视频生成器（Manim） |
| news | `news` | 1.2 | 新闻资讯查询与摘要 |

> **注**：`stocktourch`（A 股分析）与 `盯盘助手` 为同一技能，slug 均为 `stocktourch`。

---

## 技能结构

每个技能目录包含：

```
技能名/
├── SKILL.md          # 技能描述文件（含触发词、指令、规范）
├── steps/            # （可选）执行步骤文档
├── templates/        # （可选）产出模板
├── assets/           # （可选）资源文件
├── agents/           # （可选）自定义 Agent 配置
└── references/       # （可选）参考文档
```

---

## 版本与更新

- 技能版本见各目录 `SKILL.md` 的 `metadata.version` 字段
- ClawHub 发布版本与本地版本同步
- 如需更新，修改后执行 `clawhub publish` 发布到 ClawHub，并同步本仓库

---

## 许可证

部分技能采用 MIT-0 许可证（Free to use, modify, and redistribute. No attribution required.），具体以各技能 `SKILL.md` 为准。

---

*维护者: [fslong520](https://github.com/fslong520)*
*更新于: 2026-08-21*