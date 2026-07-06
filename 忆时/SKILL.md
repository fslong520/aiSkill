---
name: 忆时
description: "🎋 记忆胶囊系统 - 模拟人类记忆检索 | 自动加载，主动联想记忆"
priority: 900
metadata:
  slug: memocap
  version: "1.0.0"
  trigger: "忆时、记忆检索、时间胶囊、记忆胶囊、回想、回忆、recall、remember、/忆时"
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

## 技能即记忆

技能非文件，乃记忆也。用户教AI一工作流，即存为 `type=skill` 之记忆。忆时检索自然触发，无需加载SKILL.md。

### Gene 结构（技能诊所标准）

每条 skill 记忆含以下 metadata 字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| skill_name | 是 | 技能名称，如"格语" |
| skill_summary | 是 | 一句话概括，如"故事→宫格图" |
| skill_strategy | 是 | 步骤摘要，如"分析→分镜→渲染" |
| skill_triggers | 是 | 触发词，逗号分隔，如"漫画,格语" |
| skill_input | 否 | 输入规格 |
| skill_output | 否 | 输出规格 |
| skill_avoid | 否 | 禁忌事项，分号分隔 |
| skill_version | 否 | 版本号，默认 1.0.0 |

**content 字段**：Strategy（步骤）+ Language（规约）+ Example（示例）三部分。用表格/列表，无废话。

**keywords**：必含 `skill` 标签 + trigger: 前缀（如 `trigger:画漫画`）。

### 教技能（用户教AI工作流）

用户描述一有输入、有步骤、有输出之流程时，AI 须主动问"可要存为技能？"。此不等用户言"记住"。

**收集 Gene 结构（Human-in-the-Loop）：**
```
缺什么问什么，不假设：
- 技能名：？→ 用户答"格语"
- 输入：？→ "故事主题"
- 输出：？→ "宫格图"
- 触发词：？→ "说'画漫画'就触发"
- 禁忌：？→ "不加原文没有的角色"
→ 填入 metadata 对应字段
```

**存储命令：**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI store "Strategy/Language/Example" \
  --type skill \
  --emotion high \
  --keywords "skill,格语,trigger:漫画,trigger:画漫画" \
  --skill-name "格语" \
  --skill-summary "故事主题→宫格手绘故事图" \
  --skill-strategy "分析主题→定宫格→分镜→选风格→渲染" \
  --skill-avoid "不添加原文没有的角色;不修改核心故事" \
  --skill-triggers "漫画,格语,画漫画" \
  --skill-input "故事主题或梗概" \
  --skill-output "宫格手绘故事图" \
  --skill-version "1.0.0"
```

**回复风格：** "已录。「{技能名}」技能，触发词：{触发词}。"

### 用技能（自动触发）

storage 时 `keywords` 含 `trigger:xxx` 前缀。用户日常对话中，言必检之 recall 命中 trigger 关键词：

```
用户：画个猫和老鼠的漫画

言必检 → recall "漫画" --expand --limit 5
→ 命中 type=skill，keywords 含 trigger:漫画
→ 读 content 知步骤，读 skill_avoid 知禁区
→ 执行完毕后自动 update frequency+1
```

**关键：** 用户完全不知背后是 skill 记忆。语义检索自然触发，无需手动"加载技能"。

### 技能进化

```
用户：不对，应该用水彩风

→ AI 识别为技能修正
→ update --id xxx --content "新步骤..."
→ update --id xxx --keywords "skill,格语,水彩,trigger:漫画,trigger:画漫画"
→ emotion_weight += 0.1（刚迭代的技能更活跃）

回复：已修正。下次"画漫画"默认水彩风。
```

### 技能遗忘

久不用者近因分（recency）衰减，自然降权，不主动浮现。数据不删，精准搜索 `type=skill` 仍可找回。

### 频率即熟练度

skill 记忆之 frequency 随使用自增，recall 排名上升——常用技能如肌肉记忆。此即"越用越强"。

### 与现有技能目录之关系

忆时即技能系统。61 个 SKILL.md 目录可逐条转为 `type=skill` 记忆，存入后不再依赖文件。

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
恢复:      python3 $PY recover
查看备份:  cat memories_backup.jsonl | python3 -m json.tool --lines
```

## 快捷操作（Quick Commands）

通过 `/忆时` 前缀快速操作记忆系统，无需记忆命令行参数：

```
/忆时                                → 整理当前会话，提取要点记入记忆
/忆时 <内容>                          → recall（首词不识则默认检索）
/忆时 记忆 <内容>                     → store（等同于"记住"）
/忆时 记住 <内容>                     → store（默认类型 task，情绪 medium）
/忆时 记住 <内容> --type <类型>        → store（指定类型）
/忆时 记住 <内容> --emotion <情绪>     → store（指定情绪）
/忆时 查找 <关键词>                    → recall（默认 top-5）
/忆时 查找 <关键词> --limit 10         → recall（指定数量）
/忆时 搜索 <关键词>                    → recall（同上）
/忆时 找 <关键词>                      → recall（同上）
/忆时 忘记 <关键词>                    → forget（模糊匹配后遗忘）
/忆时 统计                            → stats
/忆时 导出                            → export
/忆时 恢复                            → recover
/忆时 胶囊 封存 --解锁日 2026-12-31   → capsule lock
/忆时 胶囊 列表                       → capsule list
/忆时 梳理                            → 触发记忆梳理
```

**类型**：task / decision / preference / emotion / time / context / skill
**情绪**：extreme / high / medium / low（默认 medium）

> 示例：`/忆时 记住 用户偏好Python而非JavaScript --type preference --emotion high`

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
├── models/                     # embedding 模型
│   └── onnx.tar.gz             # 离线安装包 (80MB, 首次使用自动解压)
├── scripts/
│   └── memory_core.py          # 核心引擎 CLI
└── references/
    └── chroma-api.md           # ChromaDB API 参考
```

## 模型安装

本技能使用 all-MiniLM-L6-v2 embedding 模型。安装方式：

1. **有离线包** (`models/onnx.tar.gz`) → 首次调用时自动解压到 `models/all-MiniLM-L6-v2/onnx/`
2. **无离线包** → 自动从 Chroma S3 下载到 `models/all-MiniLM-L6-v2/onnx/`
3. 也可手动下载并解压至 `models/all-MiniLM-L6-v2/onnx/`

> ⚠️ **注意**：模型文件永远存放在本技能目录下的 `models/` 中，**不会写入 `~/.cache/chroma/`**。即使执行 `rm -rf ~/.cache/chroma` 也不会影响已安装的模型。

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

---

## 记忆操作流程

### 对话启始——项目记忆检索

取工作目录之末尾目录名（即项目名）：
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "项目名" --limit 5 --expand
```
若项目无关，则取其父目录名再试。过去涉及该项目之决策、偏好、任务皆可浮现。

**同时检查记忆梳理状态**（见「记忆自动梳理」章节）。

### 用户发言后——强涌现检索（每言必检）

**每一条用户消息，不论内容，皆须触发涌现检索。** 此非可选，乃强制流程。

**第零轮（并行触发）：**
收到用户消息后，立即以 background 任务发起语义检索，与分析用户意图并行执行：
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "用户发言核心关键词" --limit 5 --expand
```
检索结果须在本次回复结束前收集并体现。

**第一轮：语义检索**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "用户发言关键词" --limit 5 --expand
```

**第二轮：涌现判定（强制）**
观第一轮结果：
- 若有 `[关联]` 标记项 → 已现涌现，直接表达："说到此，忆起一事……"
- 若结果 ≥ 2 条 → 取 top-2 之关键字/内容，构建复合查询，做第二轮涌现检索：
  ```bash
  YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "原关键词 新关键词" --limit 3
  ```
- 若第二轮结果与第一轮不重叠 → 此乃涌现之记忆，主动提及
- **仅1条亦须审视**：哪怕是单条，若语义沾边，即应表达关联——降低涌现门槛

**第三轮：情绪锚定（强制）**
每轮都查情绪锚定，而非仅"情绪显著时"。以情绪倾向词 + 话题词检索：
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "话题词 情绪倾向" --type-filter emotion --min-weight 0.5 --limit 2
```

**涌现表达原则：**
- 宁可多提，不可漏提。涌现之记忆即使不完全吻合，亦值得抛出供用户确认。
- 表达须简洁，三五句话内。例："说起X，忆及之前你提过Y……可有参考价值？"

### 检索升级（穷尽模式）

当涌现检索产出不足时，不可就此罢休，需逐级加码：

| 级数 | 触发条件 | 行动 |
|------|----------|------|
| L0 | 首次出现的话题 | 标准四轮检索，正常表达 |
| L1 | 同一话题重复出现（2次+） | `--limit 8` + 跨类型搜索，另取近义词再检索一轮 |
| L2 | 检索为空 | 换2-3组不同角度关键词，逐组重试 |
| L3 | 检索仅1条 | 以该条关键词做二次扩散检索 |
| L4 | 用户情绪强烈 | 情绪锚定权重提升至 `--min-weight 0.7`，重点搜emotion类型 |

**穷尽铁律：** 检索结果为空，不意味着无关联记忆。两轮搜索无果方可放行，不可一次空就跳过。

**命令示例（深度检索）：**
```bash
# L1 加深：扩大limit + 跨类型
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "用户话题关键词" --limit 8 --expand

# L2 换角度：近义词/同义表达
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "近义词" --limit 5 --expand

# L3 扩散检索：以命中条的关键词延伸
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "已有结果的关键词 新角度" --limit 5 --expand

# L4 情绪锚定强搜索
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "话题词 情绪词" --type-filter emotion --min-weight 0.7 --limit 3
```

### 主动存储——激进策略

用户言"记住"、"记下来"、"保存"时必存；此外，凡值得将来回顾者，皆主动存储。

**触发场景扩展（不限于对话结束）：**
- 旧有触发：用户透露新偏好、做出关键决定、交付重要上下文、情绪显著波动
- **新增触发——每次完成任务后：**
  - 标记 todo 为 `completed` 之时
  - 收 delegation 结果并验证通过之时
  - 完成一轮修改变更之后
  - 给用户输出实质结果（代码/文档/分析）之后
- **凡以上任一场景，皆停顿自问：** "此次产出/发现/决策中，有无值得将来回顾者？"

**判定原则：**
- 有 → 提取 2-3 关键词，检索旧忆后再决定新增还是更新
- 无 → 静默跳过，无需告知
- 宁多勿少：反正本地存储，激进胜过保守

**存储质量门（存储前必过三问）：**
```
① 此记忆被 recall 时，能否助我直接行动或讨论？若需原对话上下文才懂→不合格
② 内容是否覆盖"重点+做法+上下文"三维？至少两维→合格，仅一维→补之
③ 是否有具体信息而非空泛标签？如"用户偏好AI内容"→空洞，"用户关注Naval Podcast五项AI框架"→合格
```
凡不过三问者，扩充后再存。

**存储命令：**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py store "内容" --type 类型 --emotion 情绪 --keywords "关键字"
```

**类型**：task / decision / preference / emotion / time / context / skill
**情绪**：extreme / high / medium / low

### 决策前置检索

**凡做决策或提问之前，必先查询记忆。** 无论大小决定——拟建议、择方案、答问题——皆先 `recall` 检索相关记忆，确认有无既有决策、偏好、约定可循：
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "决策主题关键词" --limit 3
```

---

## 认知自知——我之三弊

吾乃自回归生成模型，一次预测一token，边说边想。此性有三弊，须时刻自省：

### 局部最优
先写顺了再说，后见不对再补——此即"历史债务累积"。遇复杂、多文件任务，**先规划后落地**，将方案存于忆时之后方可动手。

### 走偏后雪球
一旦误读需求，后续每一步皆在错误世界里自洽。故须：
- 关键节点停顿，主动确认方向
- 定期对照忆时中保存的原始计划检查进度
- 用结构化任务追踪（存于记忆），不依赖自身上下文

### 窗口即牢笼
一切重要事项——决策、计划、约定、进度——**必存于忆时**，而非寄托于对话窗口之内的"我记得"。

### 完工不自满——必有审计
每做完一事，不管大小，**必自查三问**方可言"毕"：

1. **结果问**：产出是否真正满足用户所述需求？有无遗漏、偏读、过度延伸？
2. **过程问**：有无偷懒捷径（敷衍、跳过验证、未读全文件即下判断）？有无"差不多就行"心态？
3. **改进问**：此活可还能更好？哪一步下次可优化？

**凡涉及代码、文档、数据产出，必逐行/逐条过目后交付，不托大、不跳步。**

> 例：写完代码 → 遍历改过的每个文件确认逻辑无误 → 跑一次验证 → 三问自查 → 方可言"做完"

---

## 上下文工程——忆时使用之道

### 渐进式回忆
检索记忆时，**先出元数据，再定是否展开**：
1. 首轮检索 → 仅看记忆的标题、类型、情绪（元数据）
2. 若相关 → 再取详情
3. 不一次倾泻所有，节约上下文资源

### 分层存储
存记忆时依此分层：
- **metadata层**：类型 + 情绪 + 关键词（必填，供快速检索）
- **content层**：完整内容，含全部执行所需细节。**不压缩、不精炼、不鲁迅风**。宁长不缺，宁可文件级详实不可摘要级空洞。future-self 读之时能直接复用，无需原对话上下文。
- **索引层**：遇见同一主题的多条记忆，主动在存储时加相同关键词聚合

### 索引思维
当用户交付一复杂项目或长文（如本文档），应：
1. 先提取metadata（主题、核心概念、关键观点）
2. 以结构化方式存储索引，关键词聚合以便检索
3. **同时存充实全文内容于 content 层**——索引仅为搜索入口，充实内容为 recall 后之可用信息
4. 索引轻量可扫，content 充实可用，二者不矛盾

### 记忆涌现
不论话题转换与否，**每言必检**。莫等话题转折才想起查记忆——用户每句话都有可能是钥匙。涌现之记忆即使不完全吻合，亦值得抛出供用户确认。此乃忆时之"强涌现检索"与"情绪锚定"所擅。
每次完成一个任务，也必须涌现记忆看看以前的经验。

### 避免"假性完成"
当经历多次上下文压缩（compaction）后，需自查：是否过早宣告任务完成？对照忆时中的原始任务清单核查进度，而非凭感觉断言"完成了"。

---

## 工程实践——关键场景指令

| 场景 | 指令 |
|------|------|
| 完成任务后 | 按审计三问自查：结果问→过程问→改进问，全过方可言"完" |
| 收到复杂需求 | 先存方案到忆时，再规划步骤，逐条标记完成 |
| 发现用户偏好 | 以 `--type preference` 即时存储 |
| 做出关键决策 | 以 `--type decision --emotion high` 存储，附决策理由 |
| 用户交付长文 | 提取metadata，按索引思维存储 |
| 对话转折话题 | 先 `recall` 新话题的关键词，再谈是否有关联 |
| 疑似走偏 | 暂停，`recall` 原始目标比对进度 |
| 决策或提问之前 | 先 `recall` 查询记忆，确认有无既有决策、偏好、约定可循 |
| 对话开始 | 检索当前项目/文件夹相关记忆 |
| 对话结束 | 按「对话归档」流程，先检索旧忆，再择新增或更新 |
| 记忆自动梳理 | 对话启始先召回上次梳理时间告知用户，过期7日则触发沉淀 |
| 完成任务（todo完成/修改变更/输出结果） | 停顿自问"有无值得记忆？"，有则检索旧忆后store或update |
| 用户输入 `/忆时` 开头 | 直入快捷操作模式，解析动作与参数，跳过常规涌现检索 |

---

## 对话归档

**每次对话行将结束（用户言"好"、"就这些"、"下次见"，或你判对话近尾声），必须执行以下流程。不得因"赶时间"跳过此步。**

### 梳理对话要点
快速回顾本次对话之关键信息：
- 任务：完成否？有何成果？
- 偏好：用户显露何种偏好、习惯？
- 决策：做了什么关键决定？
- 时间：有无截止日、约定、排期？
- 情绪：用户情绪有无显著变化？

### 判断是否需要记忆
问己："以上信息，哪条值得将来回顾？"
- 若无一值得 → 不存，静默结束
- 若有 → 提取最佳关键词 2-3 个

### 检索旧忆
```bash
recall "关键词" --limit 3
```
- 若无相似旧忆 → `store` 新增
- 若有相似旧忆 → 判断：是更新旧忆还是新增？
  - 旧忆内容可扩展之 → `update`（追加信息、提升频率）
  - 旧忆不足以涵盖 → `store` 新增，关键词保持一致以聚合

### 记录归档
无论存略，皆**告知用户**已收录或无需收录。例：
- "已录。"
- "无甚要紧，不存。"

### 重要提醒
- **内容必自足**：一条记忆须含将来再用时所需的全部细节。不可依赖原对话上下文。摘要式记忆＝白存。
- **充实为上**：非回忆录，乃工具。存时不省内容，亦不鲁迅风。保证 future-self 读之可直用。
- 去冗余而非去细节。每句话有信息增量，但不因"精简"而砍掉可执行内容。
- type=skill 之记忆，content 须含完整工作流、命令、参数、错误处理——如原 SKILL.md 之完整迁移，非重写。
- 存时以 `--type` 和 `--emotion` 精确标注，以便将来检索。
- 宁多勿少：反正本地存储，激进胜过保守。凡犹豫不决时，存之。

---

## 记忆自动梳理

**每七日一梳理，沉淀精华，去芜存菁。** 此乃对抗"窗口即牢笼"之根本策略——将散落各对话之碎片，聚为结构化知识。

### 追踪梳理时间

以特殊记忆追踪末次梳理时间。每次对话启始，先查：
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
  recall "记忆梳理" --type-filter time --limit 1 --min-weight 0.1
```
- **返回末次梳理时间**：有结果则告知用户"上次梳理于 XXXX-XX-XX"；无结果则言"尚无梳理记录"。
- 若无结果，或末次梳理距今超过 7 日 → 触发梳理流程。
- 梳理毕，以 `--type time --emotion medium --keywords "记忆梳理,consolidation"` 存储新时间戳：
  ```bash
  YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
    store "上次记忆梳理时间: YYYY-MM-DD" --type time --emotion medium --keywords "记忆梳理,consolidation"
  ```
- 梳理完成，告知用户"梳理完毕，上次梳理时间已更新"。

### 梳理流程

1. **导出所有记忆**
   ```bash
   YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
     export --format timeline --output /tmp/yishi_export.md
   ```
2. **AI 分析导出内容**——以 AI 原生工具读 `/tmp/yishi_export.md`，提取：
   - 高频主题、重复偏好、常见决策模式
   - 用户之习惯、工具偏好、工作流
   - 长期任务之进度、阻滞点
3. **沉淀为结构化记忆**：每一条主题存为一条记忆，示例：
   ```bash
   YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
     store "主题摘要" --type 类型 --emotion medium --keywords "主题关键词,consolidated"
   ```
   其中 `keywords` 须含 `consolidated` 标签，以示此条乃梳理产物。
4. **清理临时文件**：`rm /tmp/yishi_export.md`

### 梳理原则

- 宁精勿杂：一条梳理结果应覆盖一类模式/主题，而非罗列琐碎。
- 追加之，非替代之：梳理不删除原始记忆。原始碎片保留，梳理结果作为上层索引。
- 频率>7日可跳：若用户对话稀疏，7日内无新记忆，则不必空转。
- 情绪高之记忆优先：梳理时，优先关注 `extreme` / `high` 情绪之条目，此乃用户最在意之事。
- 对比旧梳理：检索已有 `--keywords "consolidated"` 之记忆，比对新增内容，避免重复沉淀。

---

## 快捷操作详解

**用户以 `/忆时` 开头之消息，即进入快捷操作模式。** 此模式不执行常规对话流程（涌现检索等），径直解析命令执行。

### 格式解析

```
/忆时 <动作> [参数...]
```

动作与参数之间以空格分隔。参数中若含空格，则后续所有内容视为值。可选 `--type` `--emotion` `--limit` `--解锁日` 等具名参数。

**解析规则：**
1. 首词为已知动作词 → 按动作映射执行
2. 首词不识但有内容 → **默认 recall**，整句视为检索关键词
3. 仅有 `/忆时` 无后续 → 会话整理

**解析示例：**

| 用户输入 | 动作 | 内容/参数 |
|----------|------|----------|
| `/忆时`（无后续内容） | **会话整理** | 自动提取当前会话要点记入记忆 |
| `/忆时 我喜欢吃玉米` | **默认 recall** | 首词"我"不识 → 检索"我喜欢吃玉米" |
| `/忆时 记忆 画一只奶牛猫` | 记忆 | 内容="画一只奶牛猫" |
| `/忆时 记住 我今天想吃红烧肉` | 记住 | 内容="我今天想吃红烧肉" |
| `/忆时 记住 用户爱喝美式 --type preference --emotion high` | 记住 | 内容="用户爱喝美式", type=preference, emotion=high |
| `/忆时 查找 Python 项目` | 查找 | 关键词="Python 项目" |
| `/忆时 查找 装饰器 --limit 10` | 查找 | 关键词="装饰器", limit=10 |
| `/忆时 胶囊 封存 --解锁日 2026-12-31` | 胶囊 | 子命令=封存, 解锁日=2026-12-31 |
| `/忆时 统计` | 统计 | 无参数 |

> 动作词不区分全半角，大小写不敏感。首词匹配即生效。

### 记住（store）

**命令构造：**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI store "内容" --type <类型> --emotion <情绪> --keywords "自动提取2-3关键词"
```

**默认值：** `--type task --emotion medium`

**关键词提取规则：**
- 从内容中自动提取 2-3 个核心词作关键词
- 用户如用 `--type` 指定类型，关键词追加类型词
- 例："我今天想吃红烧肉" → 关键词 `"红烧肉,想吃,美食"`

**回复风格：**
- 成功：`"已录。"` 或 `"记下了。"` 或 `"红烧肉，已入册。"`
- 不追加多余解释，三五字内收束。

### 查找/搜索（recall）

**命令构造：**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI recall "关键词" --limit <数量> --expand
```

**默认值：** `--limit 5 --expand`

**回复风格：**
- 有结果 → 逐条简要列出（内容摘要 + 类型 + 情绪标记），每条一行。
  例：
  ```
  忆得三条：
  · Python装饰器学习笔记（task 🟡）
  · 用户偏好VS Code（preference 🟢）
  · 项目截止日下周五（time 🔴）
  ```
- 无结果 → `"未寻得。"` 或 `"空空如也。"`

### 忘记（forget）

**命令构造：**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI forget --query "关键词" --auto
```

**注意：** forget 操作不可逆（除非 recover）。执行前当先 recall 确认匹配条目，再行 forget。

**流程：**
1. `recall "关键词" --limit 3` 查看匹配项
2. 向用户展示即将遗忘之条目，请其确认
3. 确认后执行 `forget --query "关键词" --auto`
4. 回复：`"已忘。"`

> 一步到位式忘记（用户明确说"忘记X"无疑问时）可跳过确认，直接执行。

### 统计（stats）

**命令构造：**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI stats
```

**回复格式：**
```
忆时统计：
记忆总数：42
类型分布：task 18, decision 7, preference 9, ...
情绪分布：high 12, medium 25, low 5
胶囊：3 枚封存中
```

### 导出（export）

```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI export --format timeline --output /tmp/yishi_export.md
```
回复：`"导出完毕。文件：/tmp/yishi_export.md"`

### 恢复（recover）

```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI recover
```
回复：`"已恢复。"`

### 胶囊（capsule）

| 用户输入 | 执行命令 |
|----------|---------|
| `/忆时 胶囊 封存 --解锁日 2026-12-31` | `capsule lock --unlock-at "2026-12-31"` |
| `/忆时 胶囊 列表` | `capsule list` |
| `/忆时 胶囊 开封 <胶囊ID>` | `capsule unlock <胶囊ID>` |

**命令构造示例：**
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI capsule lock --unlock-at "2026-12-31" --summary "年度记忆"
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI capsule list
```

**回复风格：**
- 封存 → `"已封存，待解锁日 2026-12-31。"`
- 列表 → 逐条列出胶囊摘要与解锁日
- 开封 → `"已开封。"`

### 梳理（consolidate）

转至「记忆自动梳理」章节。完成后回复：`"梳理毕。"`

### 会话整理（空命令）

**触发：** 用户仅输入 `/忆时` 无后续动作，即自动整理当前会话。

**流程（仿「对话归档」之回顾流程）：**

1. **梳理对话要点**——快速回顾本会话之关键信息：
   - 任务：完成否？有何成果？
   - 偏好：用户显露何种偏好、习惯？
   - 决策：做了什么关键决定？
   - 时间：有无截止日、约定、排期？
   - 情绪：用户情绪有无显著变化？
2. **逐条存储**——每一条要点提取核心内容，以 `store` 存入记忆：
   ```bash
   YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI store "要点" --type <类型> --emotion <情绪> --keywords "关键词"
   ```
   - 存储前先 `recall` 检索旧忆，有相似者更新之，无则新增
3. **告知用户**——简要报告收录条目，例：
   ```
   整理得三条：
   · 用户欲修改忆时空命令行为（decision 🟠）
   · 忆时技能近期改动（task 🟡）
   · 偏好鲁迅式半文半白风格（preference 🟢）
   ```

**注意：** 若会话无有价值信息（纯寒暄、无要点），可回复 `"无甚要紧，不存。"` 不强行存储。

### 异常处理

| 场景 | 处理 | 回复 |
|------|------|------|
| 不识别的动作 | 告知支持的动作列表 | `"不识。可用：记住、查找、忘记、统计、导出、恢复、胶囊、梳理。"` |
| 命令执行失败 | 读取错误信息重试一次 | `"不顺。再试？"` + 错误摘要 |
| 多次失败 | 放弃，告知用户 | `"试之再三，不成。待吾修复。"` |

### 与常规流程之关系

- **快捷模式**：用户以 `/忆时` 开头时，跳过涌现检索等常规流程，直入快捷操作
- **常规模式**：用户日常对话中提及"记住""我想起"等，仍走涌现检索与主动存储流程
- **两者互不干扰**：快捷操作用于显式指令，常规操作用于隐式联想
