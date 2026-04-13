---
name: 备课

description: |
  为信息学奥赛培训（NOI/CSP/GESP）准备讲义材料的智能备课系统。
  基于 ADDIE 教学设计模型（Analysis-Design-Development-Implementation-Evaluation），
  专门针对14岁高中生设计，创建C++编程和算法竞赛培训的教案、教学材料和例题。
  采用模块化架构，SKILL.md 仅负责调度，详细流程参见 modules/ 目录。

allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion

metadata:
  trigger: 信息学奥赛备课、C++编程教学、算法竞赛培训、教学材料生成、备课
  source: 基于 ADDIE 教学设计模型、信息学竞赛教学大纲和青少年认知发展理论
  version: 2.0 (模块化重构)
---

# 备课技能

基于 **ADDIE 教学设计模型** 的信息学奥赛备课系统。

```
触发：用户要求备课/生成讲义/准备教学材料
流程：ADDIE 五阶段，按需进入对应模块文档
```

---

## 快速导航

### ADDIE 五阶段

| 阶段 | 模块文档 | 做什么 |
|------|---------|--------|
| **1. Analysis 分析** | [modules/01-Analysis分析.md](./modules/01-Analysis分析.md) | 搞清楚"教谁、教什么" |
| **2. Design 设计** | [modules/02-Design设计.md](./modules/02-Design设计.md) | 规划"怎么教" |
| **3. Development 开发** | [modules/03-Development开发.md](./modules/03-Development开发.md) | 制作"教学材料" |
| **4. Implementation 实施** | [modules/04-Implementation实施.md](./modules/04-Implementation实施.md) | 课堂执行 |
| **5. Evaluation 评价** | [modules/05-Evaluation评价.md](./modules/05-Evaluation评价.md) | 效果评估与迭代 |

### 核心工具文档

| 文档 | 用途 | 所属阶段 |
|------|------|---------|
| [modules/叙事设计.md](./modules/叙事设计.md) | 情绪曲线、植入-揭示、赌注阶梯 | Design |
| [modules/去AI味指南.md](./modules/去AI味指南.md) | 10 条去 AI 味原则 | Development |

### 资源文档

| 文档 | 用途 |
|------|------|
| [references/备课规则.md](./references/备课规则.md) | 完整课程结构、级别对照、教学标准 |
| [references/例题模板规则.md](./references/例题模板规则.md) | 例题精确格式要求 |
| [assets/讲义ppt模板.md](./assets/讲义ppt模板.md) | Marp 讲义模板 |

---

## 备课工作流

接到备课任务后，按以下流程执行：

```
用户提出备课需求
    ↓
读取对应模块文档（按需）
    ↓
按 ADDIE 阶段逐步执行
    ↓
输出：讲义/PPT + 例题 + 作业 + 代码
```

### 阶段跳转规则

- **备课场景**（最常见）：执行 Analysis → Design → Development，产出讲义
- **完整场景**：五阶段全走，含实施记录和评价报告
- **快速场景**：用户已有分析结论，直接从 Design 开始

**每个阶段完成后，进入下一阶段前先自检。**

---

## 级别对照（速查）

| 级别 | 难度 | 目标 |
|------|------|------|
| 入门级 | 1-5 | CSP-J、GESP 1-4 级 |
| 提高级 | 5-8 | CSP-S、GESP 5-6 级 |
| NOI 级 | 7-10 | NOI、省选 |

完整课程结构参见 → [references/备课规则.md](./references/备课规则.md)

---

## 技术偏好

### CDN 源

| 优先级 | 源 |
|--------|-----|
| 首选 | unpkg.com |
| 备选 | fastly.jsdelivr.net、cdnjs.cloudflare.com |
| 避免 | cdn.jsdelivr.net（国内访问不了）、bootcdn（太慢） |

### 讲义文件处理

- HTML 优先（同时有 .html 和 .md 时只添加 HTML）
- .md 文件必须以 `_ppt` 结尾才会被添加到数据库
- 支持：.pdf、.html、.md

---

## 迭代优化

技能支持自我迭代。根据使用反馈优化文档，让技能越来越好用。

优化触发：用户反馈、使用数据、错误发现、新需求。
优化执行：记录 → 分析 → 修改 → 验证。

详见各模块文档末尾的"输出物"和"检查清单"，每次使用后可对照评估效果。
