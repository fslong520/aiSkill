# 模块 07 - 技能即记忆（Gene 结构）

**何时读**：用户描述一工作流（教AI流程）、recall 命中 `type=skill` 记忆、需修正/遗忘技能时。日常无此场景不读。

## 概念

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
