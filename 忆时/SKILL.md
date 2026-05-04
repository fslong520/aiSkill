---
name: 忆时
description: "🎋 记忆胶囊系统 - 模拟人类记忆检索 | 自动加载，主动联想记忆"
priority: 900
metadata:
  slug: memocap
  version: "1.0.0"
  trigger: "忆时、记忆检索、时间胶囊、记忆胶囊、回想、回忆、recall、remember"
  copaw:
    emoji: "🎋"
    requires: {}
    auto_load: true
---

# 忆时 - 记忆胶囊系统

> 模拟人类的记忆机制，让 AI 拥有会遗忘、会联想、会涌现、会封存的记忆系统。
> 详细流程参见 modules/ 目录。

## 触发条件

- **自动加载**：每次对话自动激活，AI 主动联想和检索记忆
- **关键字**：忆时、记忆检索、时间胶囊、记忆胶囊、回想、回忆、我说过、我记得
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

## 执行流程入口

1. 读取 `modules/01-initialize.md` - 初始化 Chroma
2. 读取 `modules/02-passive-mode.md` - 被动模式流程
3. 读取 `modules/03-active-mode.md` - 主动模式流程
4. 读取 `modules/04-time-capsule.md` - 时间胶囊操作
5. 读取 `modules/05-retrieval.md` - 类人检索策略
6. 读取 `modules/06-import-export.md` - 导入导出操作

## 核心命令

```bash
PY=/home/fslong/.config/opencode/skills/忆时/scripts/memory_core.py

初始化:    python3 $PY init
存储记忆:  python3 $PY store "内容" --type task --emotion high
检索记忆:  python3 $PY recall "查询" --limit 5 --expand
封胶囊:  python3 $PY capsule lock --unlock-at "2026-12-31"
查看胶囊:  python3 $PY capsule list
导入:      python3 $PY import-file file.md --format markdown
导出:      python3 $PY export --format timeline --output output.md
统计:      python3 $PY stats
遗忘:      python3 $PY forget --before "2025-01-01" --auto
```

## 项目结构

```
忆时/
├── SKILL.md                    # 技能定义 (入口)
├── yishi-instructions.md       # 外挂提示词 (必须配置到 opencode.json)
├── modules/                    # 详细流程模块
│   ├── 01-initialize.md        # Chroma 初始化
│   ├── 02-passive-mode.md      # 被动模式流程
│   ├── 03-active-mode.md       # 主动模式流程
│   ├── 04-time-capsule.md      # 时间胶囊操作
│   ├── 05-retrieval.md         # 类人检索策略
│   └── 06-import-export.md     # 导入导出操作
├── models/onnx/                # 内置 embedding 模型 (87MB)
│   ├── model.onnx
│   ├── config.json
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   ├── special_tokens_map.json
│   └── vocab.txt
├── scripts/
│   └── memory_core.py          # 核心引擎 CLI
└── references/
    └── chroma-api.md           # ChromaDB API 参考
```

## 内置模型

本技能自带 all-MiniLM-L6-v2 embedding 模型 (87MB)，位于 `models/onnx/` 目录。
首次使用无需任何下载，开箱即用。

## 使用说明

### 必须配置外挂提示词

本技能依赖 OpenCode 的 `instructions` 配置才能完整生效。
未配置时，AI 不会自动检索记忆或存储记忆。

**配置步骤：**

1. 编辑全局配置文件 `~/.config/opencode/opencode.json`
2. 添加 `instructions` 字段，指向技能目录下的提示词文件：

```json
{
  "instructions": [
    "~/.config/opencode/skills/忆时/yishi-instructions.md"
  ]
}
```

3. 重启 OpenCode 使配置生效

**配置后 AI 将自动：**
- 每次对话前检索记忆系统
- 用户说"记住"时自动存储记忆
- 话题关联时主动涌现历史记忆
- 对话结束时自动归档重点

**未配置则：**
- 技能仍可手动调用命令
- 但不会自动检索/存储记忆
- 不会主动联想和闪回

## 运行环境

- Python: 3.13+
- 依赖: chromadb 1.5.4
- 脚本: `scripts/memory_core.py`
- 数据: `data/` (ChromaDB PersistentClient 自动创建)
