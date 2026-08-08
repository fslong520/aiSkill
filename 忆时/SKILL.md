---
name: 忆时
description: "🎋 记忆胶囊系统 - 模拟人类记忆检索 | 自动加载，主动联想记忆"
priority: 900
metadata:
  slug: memocap
  version: "2.0.0"
  trigger: "忆时、记忆检索、时间胶囊、记忆胶囊、回想、回忆、recall、remember、/忆时"
  copaw:
    emoji: "🎋"
    requires: {}
    auto_load: true
---

# 忆时 - 记忆胶囊系统

> 模拟人类的记忆机制，让 AI 拥有会遗忘、会联想、会涌现、会封存的记忆系统。
> **渐进式披露**：本文件为入口总纲。细节皆在 modules/——按「按需读取」表，遇场景才读对应模块，勿一次全读。

## 触发条件

- **自动加载**：每次对话自动激活，AI 主动联想和检索记忆
- **关键字**：忆时、记忆检索、时间胶囊、记忆胶囊、回想、回忆、我说过、我记得
- **命令**：用户输入以 `/忆时` 开头时，自动触发快捷操作模式
- **场景**：用户询问过去的事情、要求回忆、需要上下文关联、触发闪回
- **主动**：定时模式运行时主动扫描到期胶囊和记忆关联

## 核心概念

| 概念 | 说明 |
|------|------|
| **类人检索** | 语义40% + 近因20% + 情绪15% + 频率25%，不像数据库那样精确 |
| **渐进式回忆** | 先抛最相关的1-2条，用户追问再深入，非一次性倒出 |
| **遗忘曲线** | 记忆随时间指数衰减，低频率的记忆会变得"模糊" |
| **情绪锚定** | 高情绪（🔴高/🟠中高）记忆权重更高，不易遗忘 |
| **记忆涌现** | 话题转换时发现隐藏关联，主动说出"说到这个我突然想到…" |
| **时间胶囊** | 封存某段记忆，设定解锁日期，到期后自动/手动解封翻阅 |

## 记忆类型

| 类型 | 说明 | 情绪权重倾向 |
|------|------|-------------|
| emotion | 情绪事件（开心、愤怒、悲伤） | |
| decision | 用户做出的决策 | 🟠 |
| task | 任务/待办 | 🟡 |
| time | 时间敏感信息（截止日期） | 🔴 |
| preference | 用户偏好/习惯 | 🟢 |
| context | 上下文/背景信息 | 🟡 |
| skill | 技能——用户教AI的工作流，Gene结构化存储 | 🟠 |

## 按需读取（渐进式披露核心）

**规则：未遇对应场景，不读模块。每模块读一次即可，勿重复加载。**

| 场景 | 读模块 |
|------|--------|
| 对话启始、每言必检、主动存储、检索升级、决策前置 | modules/13-retrieval-store.md |
| 用户描述工作流（教AI流程）、skill记忆检索命中 | modules/07-skill-memory.md |
| 对话结束归档、仅输入 `/忆时` 会话整理 | modules/09-archiving.md |
| 用户输入 `/忆时 ...`（命令构造/回复风格） | modules/11-quick-commands.md |
| 可视化（"看看记了啥"）、人物画像 | modules/12-viz-profile.md |
| 记忆自动梳理（上次梳理过期7日） | modules/10-consolidation.md |
| 模型安装/切换、opencode.json 配置 | modules/08-setup.md |
| 复杂任务规划、上下文压缩后自查、长文索引 | modules/14-behavior.md |
| 首次初始化、Chroma 集合结构 | modules/01-initialize.md |
| 定时主动模式（胶囊检查/遗忘归档） | modules/03-active-mode.md |
| 时间胶囊管理 | modules/04-time-capsule.md |
| 检索算法原理（综合得分公式） | modules/05-retrieval.md |
| 导入导出、备份迁移 | modules/06-import-export.md |
| 被动检索触发场景与渐进式回忆 | modules/02-passive-mode.md |

## 核心命令

```bash
PY=/home/fslong/.config/opencode/skills/忆时/scripts/memory_core.py
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data    # 所有命令必设

初始化:    python3 $PY init
存储记忆:  python3 $PY store "内容" --type task --emotion high
检索记忆:  python3 $PY recall "查询" --limit 5 --expand
封胶囊:   python3 $PY capsule lock --unlock-at "2026-12-31"
查看胶囊:  python3 $PY capsule list
导入:      python3 $PY import-file file.md --format markdown
导出:      python3 $PY export --format timeline --output output.md
可视化:    python3 ~/.config/opencode/skills/忆时/scripts/viz/viz.py
统计:      python3 $PY stats
遗忘:      python3 $PY forget --before "2025-01-01" --auto
恢复:      python3 $PY recover
查看备份:  cat memories_backup.jsonl | python3 -m json.tool --lines
```

## 快捷操作一览

`/忆时` 前缀，免记命令行参数。命令构造、解析规则、回复风格见 modules/11-quick-commands.md。

| 输入 | 动作 |
|------|------|
| `/忆时`（无后续） | 会话整理 |
| `/忆时 <内容>` | 默认 recall |
| `/忆时 记住/记忆 <内容> [--type T] [--emotion E]` | store |
| `/忆时 查找/搜索/找 <关键词> [--limit N]` | recall |
| `/忆时 忘记 <关键词>` | forget |
| `/忆时 统计` | stats |
| `/忆时 导出` | export |
| `/忆时 可视化 [--out 路径]` | 记忆全景 HTML |
| `/忆时 画像` | 人物画像 |
| `/忆时 恢复` | recover |
| `/忆时 胶囊 封存/列表/开封` | capsule lock/list/unlock |
| `/忆时 梳理` | 记忆梳理 |

**类型**：task / decision / preference / emotion / time / context / skill
**情绪**：extreme / high / medium / low（默认 medium）

## 工程实践——关键场景

| 场景 | 指令 |
|------|------|
| 完成任务后 | 按审计三问自查：结果问→过程问→改进问，全过方可言"完" |
| 收到复杂需求 | 先存方案到忆时，再规划步骤，逐条标记完成 |
| 发现用户偏好 | 以 `--type preference` 即时存储 |
| 做出关键决策 | 以 `--type decision --emotion high` 存储，附决策理由 |
| 用户交付长文 | 提取metadata，按索引思维存储（见 modules/14） |
| 对话转折话题 | 先 `recall` 新话题的关键词，再谈是否有关联 |
| 疑似走偏 | 暂停，`recall` 原始目标比对进度 |
| 决策或提问之前 | 先 `recall` 查询记忆，确认有无既有决策、偏好、约定可循 |
| 对话开始 | 检索当前项目/文件夹相关记忆（见 modules/13） |
| 对话结束 | 按归档流程，先检索旧忆，再择新增或更新（见 modules/09） |
| 记忆自动梳理 | 对话启始先召回上次梳理时间告知用户，过期7日则触发沉淀（见 modules/10） |
| 完成任务（todo完成/修改变更/输出结果） | 停顿自问"有无值得记忆？"，有则检索旧忆后store或update |
| 用户输入 `/忆时` 开头 | 直入快捷操作模式，解析动作与参数，跳过常规涌现检索 |

## 项目结构

```
忆时/
├── SKILL.md                    # 技能定义 (入口总纲/识别层)
├── yishi-instructions.md       # 外挂提示词 (必须配置到 opencode.json)
├── modules/                    # 详细流程模块 (执行层，按需读取)
│   ├── 01-initialize.md        # Chroma 初始化
│   ├── 02-passive-mode.md      # 被动模式流程
│   ├── 03-active-mode.md       # 主动模式流程
│   ├── 04-time-capsule.md      # 时间胶囊操作
│   ├── 05-retrieval.md         # 类人检索策略
│   ├── 06-import-export.md     # 导入导出操作
│   ├── 07-skill-memory.md      # 技能即记忆 (Gene)
│   ├── 08-setup.md             # 模型安装与配置
│   ├── 09-archiving.md         # 对话归档与会话整理
│   ├── 10-consolidation.md     # 记忆自动梳理
│   ├── 11-quick-commands.md    # 快捷操作详解
│   ├── 12-viz-profile.md       # 可视化与人物画像
│   ├── 13-retrieval-store.md   # 记忆操作流程 (检索/存储细则)
│   └── 14-behavior.md          # 认知自知与上下文工程
├── models/                     # embedding 模型
│   └── onnx.tar.gz             # MiniLM 离线安装包 (80MB, 回退用)
├── scripts/
│   ├── memory_core.py          # 核心引擎 CLI
│   └── viz/                    # 记忆可视化
│       ├── viz.py              # 记忆全景生成器（导出→聚类→注入模板→打开）
│       ├── template.html       # 记忆全景模板（孟菲斯风，/*__DATA__*/ 占位）
│       ├── profile.py          # 人物画像助手（素材报告 + 正文注入）
│       └── profile_template.html # 画像模板（<!--DATA-->/<!--CONTENT--> 占位）
└── references/
    └── chroma-api.md           # ChromaDB API 参考
```

## 运行环境

- Python: 3.13+
- 依赖: chromadb 1.5.4
- 脚本: `scripts/memory_core.py`
- 数据: `data/` (ChromaDB PersistentClient 自动创建)
- 模型: bge-base-zh-v1.5（768维，默认），回退 MiniLM（384维）。安装/切换见 modules/08-setup.md
