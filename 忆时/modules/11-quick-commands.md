# 模块 11 - 快捷操作详解

**何时读**：用户消息以 `/忆时` 开头时。读此模块得命令构造、参数解析、回复风格。

**用户以 `/忆时` 开头之消息，即进入快捷操作模式。** 此模式不执行常规对话流程（涌现检索等），径直解析命令执行。

## 格式解析

```
/忆时 <动作> [参数...]
```

动作与参数之间以空格分隔。参数中若含空格，则后续所有内容视为值。可选 `--type` `--emotion` `--limit` `--解锁日` 等具名参数。

**解析规则：**
1. 首词为已知动作词 → 按动作映射执行
2. 首词不识但有内容 → **默认 recall**，整句视为检索关键词
3. 仅有 `/忆时` 无后续 → 会话整理（见 modules/09-archiving.md）

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

## 记住（store）

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

## 查找/搜索（recall）

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

## 忘记（forget）

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

## 统计（stats）

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

## 导出（export）

```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI export --format timeline --output /tmp/yishi_export.md
```
回复：`"导出完毕。文件：/tmp/yishi_export.md"`

## 可视化（viz）

```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/viz/viz.py
```
参数、产出、主题聚类、回复风格——详见 modules/12-viz-profile.md「可视化」。

## 画像（profile）

两步流程、素材报告、正文撰写结构、署名规范、自动封存——详见 modules/12-viz-profile.md「画像」。

## 恢复（recover）

```bash
YISHI_DATA_DIR=~/.config/opencode/skills/忆时/data python3 $YISHI recover
```
回复：`"已恢复。"`

## 胶囊（capsule）

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

## 梳理（consolidate）

转至 modules/10-consolidation.md「记忆自动梳理」。完成后回复：`"梳理毕。"`

## 会话整理（空命令）

见 modules/09-archiving.md「会话整理」。

## 异常处理

| 场景 | 处理 | 回复 |
|------|------|------|
| 不识别的动作 | 告知支持的动作列表 | `"不识。可用：记住、查找、忘记、统计、导出、可视化、恢复、胶囊、梳理。"` |
| 命令执行失败 | 读取错误信息重试一次 | `"不顺。再试？"` + 错误摘要 |
| 多次失败 | 放弃，告知用户 | `"试之再三，不成。待吾修复。"` |

## 与常规流程之关系

- **快捷模式**：用户以 `/忆时` 开头时，跳过涌现检索等常规流程，直入快捷操作
- **常规模式**：用户日常对话中提及"记住""我想起"等，仍走涌现检索与主动存储流程
- **两者互不干扰**：快捷操作用于显式指令，常规操作用于隐式联想
