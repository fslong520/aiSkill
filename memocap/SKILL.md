---
name: memocap
description: "忆时记忆系统 - 类人记忆检索/存储/遗忘/胶囊/可视化。让 AI 拥有会遗忘、会联想、会涌现、会封存的记忆。触发词：忆时、记忆、记住、回想、回忆、recall、remember、时间胶囊、记忆检索、可视化、记忆脑图、人物画像。"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
metadata:
  slug: memocap
  version: "2.5.10"
  trigger: 忆时, 记忆检索, 时间胶囊, 记忆胶囊, 回想, 回忆, recall, remember, /忆时, 记住, 可视化, 记忆脑图, 人物画像
---

# Skill: 忆时记忆系统

## Keywords
忆时, 记忆, 记忆检索, 记忆存储, 时间胶囊, 遗忘曲线, 记忆涌现, 视觉化, 记忆能力

## Summary
忆时是类人记忆系统。核心命令经 `memory_core.py` CLI 走混合检索（BM25+向量 RRF）、去重合并、遗忘曲线、情绪锚定。数据与脚本共享于本机 `~/.local/share/忆时/`，多工具双栖共用。

## 前置（启始三检，每会话必行）
缺一不可，验不过即报不绕：
1. `MEMO_DIR` 已设环境变量？——否则脚本路径错、数据错存。
2. 数据目录 `~/.local/share/忆时/data` 存在且可写？
3. `python3` 可用？`memory_core.py` 能否运行？

## 路径与命令
```bash
LOCAL_BASE=~/.local/share/忆时
YISHI=$LOCAL_BASE/scripts/memory_core.py
MEMO_DIR=$LOCAL_BASE/data
# store：内容为【位置参数放最后】（无 --content/--tags），关键字用 --keywords；title ≤10 字自动生成，可 --title 覆盖
#   两段式：先 recall 判断（读相似旧忆，判同主题否）→ 再 store 决策。脚本不代决：
#   store 遇相似≥70%候选（最多3条完整原文）即【不落库】挂起等 AI。统一一条路 --merge-ids（N 可0）：
#   ①选（候选里选出值得合并者，可0条）②删（选N条→--merge-ids "ID1,ID2,..."；选0条→--merge-ids ""空串=删0条）③并（综合版=所选旧内容+新内容 AI 手写存入；选0条=新内容原样存）
python3 $YISHI store --type <decision|task|preference|emotion|context|time|skill> --keywords "k1,k2" --emotion <0-1> "[完整内容]"
# recall：检索/核实（默认最相关3条，勿多；相似>0.5 即看；--judge 判定模式输出全文+相似度/类型/创建日，值必存第一段用）
python3 $YISHI recall "关键词" --judge
# merge：梳理时语义合并高相关簇（锚记忆→预览簇→--content+--apply 删旧存新）
python3 $YISHI merge --id <锚ID> --threshold 0.68
# 其余子命令：forget 删除 | stats 统计 | export 导出 | recover 恢复 | capsule 时间胶囊
# 可视化：python3 $LOCAL_BASE/scripts/viz/viz.py（全景）/ mindmap.py（网状记忆图谱，D3 力导向）
# 人物画像：python3 $LOCAL_BASE/scripts/viz/profile.py
```

## 三条红线（铁律）
1. **言必检**——每言先 recall 检索再作答，检而再检，换词查透。
2. **困必查**——卡住/不确定/忘细节/报错不明/改了没效果 → **先 recall 翻记忆找先例教训**，不得硬扛、不得凭猜、不得卡死；翻完仍无解才注明「无记忆」行事。
3. **值必存**——有价值信息（决策/偏好/任务/情绪/时间/上下文）主动留存，**必两段式**：先 recall 判断（`--judge` 读全文，判同主题否）→ 再 store 决策。**脚本不代决**——store 遇候选【不落库】挂起等 AI，统一一条路 `--merge-ids`（N 可 0）：可合并→`--merge-ids "ID1,ID2,..."` 删旧存新综合版；不可合并→`--merge-ids ""` 空串机械存储。**禁止裸 store**。禁止"先存了再说"（先落库再合并=临时碎片）。存后 recall 核实。
4. **存必告**——存则告"已录"（指明类型），不存亦告，不沉默。

## 存储质量
记忆内容**不可压缩**（对话输出可省字，存储须自足）。内容按【前因】【行为】【后果】三要素，答得出"为何"与"何如"、三月后重读自能理解方存。宁多三行因果，不省一字。

## 语言风格
默认简约直给，去填充词、客套、自夸、工具调用叙述。安全警告/不可逆操作/多步易歧义处自动恢复正常句式，明晰为要。

## 模块详情
细册在 `~/.local/share/忆时/docs/modules/`（13-retrieval-store.md 检索存储、12-viz-profile.md 可视化画像、11-quick-commands.md 快捷命令等）。渐进式披露——遇场景才读对应模块，勿一次全读。
