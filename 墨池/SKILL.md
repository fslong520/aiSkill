---
name: 墨池
description: |
  知识管理技能，自动识别学习行为，智能管理知识库。【始终在线模式】每次对话开始时自动加载，
  全程监听用户输入，从任意对话中提取知识点、记录学习行为、更新用户画像。
  
  **全局生效配置**：已在 MEMORY.md 中记录，每次对话自动加载，无需手动触发。
  
  采用模块化架构，SKILL.md 仅负责调度，详细流程参见 modules/ 目录。

allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion

user-invocable: false

metadata:
  trigger: 始终在线、全程监听、自动触发、什么、怎么、为什么、如何、哪、几、谁、何时、何地、何处、多少、怎样、是不是、对不对、好不好、能不能、可不可以、为啥、干嘛、？、?、解释、讲一下、说一下、介绍一下、帮我理解、墨池
  source: 基于知识管理理论和艾宾浩斯遗忘曲线
  auto-load: true
  global: true
  trigger_rule: 暴力模式 - 所有疑问句触发！包含疑问词(什么/怎么/为什么/如何/哪/几/谁/何时/何地/多少/怎样/为啥/干嘛)或问号(？/?)或疑问句式(是不是/对不对/好不好/能不能)就立即触发知识提取
  version: 2.0 (模块化重构，AI 原生实现)
---

# InkPot - 墨池

> 砚田勤耕，墨香留痕。让AI陪你沉淀每一份知识。

**核心理念**：**不用 Python 脚本！** AI 直接用 `read_file`、`edit_file` 操作文件，自己判断、自己计算。

---

## 快速导航

### 核心模块

| 模块 | 文档 | 做什么 |
|------|------|--------|
| **知识点记录** | [modules/01-knowledge_record.md](./modules/01-knowledge_record.md) | 从对话中提取知识点，记录到知识库 |
| **过期机制** | [modules/02-expiry_check.md](./modules/02-expiry_check.md) | 检查知识是否过期，验证/存档处理 |
| **用户画像** | [modules/03-user_profile.md](./modules/03-user_profile.md) | 分析用户行为，推断身份和擅长领域 |
| **命令处理** | [modules/commands.md](./modules/commands.md) | 处理 `/墨池 xxx` 命令 |

### 格式规范

| 文档 | 用途 |
|------|------|
| [references/knowledge_format.md](./references/knowledge_format.md) | 知识点 KV 格式规范 |
| [references/profile_format.md](./references/profile_format.md) | 用户画像 KV 格式规范 |
| [references/log_format.md](./references/log_format.md) | 学习日志格式规范 |
| [references/expiry_rules.md](./references/expiry_rules.md) | 过期周期规则 |

---

## 触发规则

**暴力模式**：所有疑问句触发！

| 触发词 | 示例 |
|--------|------|
| 疑问代词 | 什么、怎么、为什么、如何、哪、几、谁、何时、何地、多少、怎样 |
| 口语疑问词 | 为啥、干嘛、咋 |
| 疑问句式 | 是不是、对不对、好不好、能不能、可不可以 |
| 问号 | ？、? |
| 请求解释 | 解释、讲一下、说一下、介绍一下、帮我理解 |

触发后 → 进入 [modules/01-knowledge_record.md](./modules/01-knowledge_record.md) 执行记录流程。

---

## 命令列表

| 命令 | 功能 | 模块文档 |
|------|------|---------|
| `/墨池 画像` | 查看用户画像 | [03-user_profile.md](./modules/03-user_profile.md) |
| `/墨池 过期报告` | 查看知识过期状态 | [02-expiry_check.md](./modules/02-expiry_check.md) |
| `/墨池 验证 <知识点>` | 验证过期知识 | [02-expiry_check.md](./modules/02-expiry_check.md) |
| `/墨池 永不过期 <知识点>` | 标记为基础理论 | [02-expiry_check.md](./modules/02-expiry_check.md) |
| `/墨池 清理存档` | 删除存档知识 | [02-expiry_check.md](./modules/02-expiry_check.md) |
| `/墨池 索引` | 查看知识库索引 | [commands.md](./modules/commands.md) |
| `/墨池 搜索 <关键词>` | 搜索知识点 | [commands.md](./modules/commands.md) |
| `/墨池 统计` | 学习统计报告 | [commands.md](./modules/commands.md) |
| `/墨池 复习` | 智能复习推荐 | [commands.md](./modules/commands.md) |
| `/墨池 推荐` | 个性化学习推荐 | [commands.md](./modules/commands.md) |
| `/墨池 导出` | 导出知识库 | [commands.md](./modules/commands.md) |

---

## 工作流

```
用户提问（触发墨池）
    ↓
进入 modules/01-knowledge_record.md
    ↓
提取知识点 → 用 edit_file 更新知识库
    ↓
继续对话（不打断）
```

**命令触发**：

```
用户输入：/墨池 xxx
    ↓
进入 modules/commands.md 或对应模块
    ↓
read_file → AI 处理 → 输出报告/更新知识库
```

---

## AI 原生原则

**铁律：不用 Python 脚本！**

| 操作 | AI 原生方式 |
|------|------------|
| 读取知识库 | `read_file` |
| 更新知识点 | `edit_file` |
| 记录日志 | `edit_file` append |
| 判断过期 | AI 自己计算日期差 |
| 搜索知识 | AI 自己解析文本 |

详见 MEMORY.md 中的「AI 原生优先原则」。

---

## 数据库结构

```
墨池/
├── SKILL.md                    # 调度入口（本文档）
├── modules/                    # 流程模块
│   ├── 01-knowledge_record.md
│   ├── 02-expiry_check.md
│   ├── 03-user_profile.md
│   └── commands.md
├── references/                 # 格式规范
│   ├── knowledge_format.md
│   ├── profile_format.md
│   ├── log_format.md
│   └── expiry_rules.md
├── db/                         # 数据文件
│   ├── knowledge_index.txt
│   ├── user_profile.txt
│   └── learning_log.txt
├── knowledge/                  # 知识点详情
│   ├── 算法数据结构/
│   ├── 工具使用/
│   └── ...
└── profile/                    # 用户画像详情
```

---

**作者**: fslong

**更新日期**: 2026-04-14

**更新说明**: 
- 模块化重构（SKILL.md 仅做调度入口）
- AI 原生实现（删除所有 Python 脚本）
- 新增知识过期机制
- 新增用户画像模块