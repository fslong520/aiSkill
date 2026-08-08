# 模块 13 - 记忆操作流程（检索与存储细则）

**何时读**：对话启始取项目名、用户每言必检（涌现检索/情绪锚定）、主动存储、检索结果不足需升级、做决策或提问之前。此乃每言必检之详细执行档，日常对话高频场景触发。

## 对话启始——项目记忆检索

取工作目录之末尾目录名（即项目名）：
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "项目名" --limit 5 --expand
```
若项目无关，则取其父目录名再试。过去涉及该项目之决策、偏好、任务皆可浮现。

**同时检查记忆梳理状态**（见 modules/10-consolidation.md「记忆自动梳理」）。

## 用户发言后——强涌现检索（每言必检）

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

## 检索升级（穷尽模式）

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

## 主动存储——激进策略

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

## 决策前置检索

**凡做决策或提问之前，必先查询记忆。** 无论大小决定——拟建议、择方案、答问题——皆先 `recall` 检索相关记忆，确认有无既有决策、偏好、约定可循：
```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py recall "决策主题关键词" --limit 3
```
