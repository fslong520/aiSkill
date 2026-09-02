---
name: 1memory
description: 1memory 记忆系统 - 跨设备跨软件统一 AI 记忆（local-first，端到端加密）。触发词：1memory、记忆、记住、回想、recall、remember、记忆检索、存记忆、遗忘、忘掉。
keywords: 1memory,记忆,recall,remember,remember
---

# Skill: 1memory 记忆系统

## Summary
1memory 是类人记忆系统 CLI（Rust 版，`~/.local/bin/1memory`）。本地 SQLite 权威库 + 服务器哑密文仓库，端到端加密，写后自动同步。检索=本地全量余弦（256 维 char-bigram 哈希 embedding）+ 关键词融合，零网络零泄露。store 自动判重合并。

## 命令速查
```bash
1memory recall "关键词" --limit 3          # 语义检索（先此一步，每言必检）
1memory remember "完整内容" --type decision --tags "k1,k2" --title "短标题"   # 存（自动同步）
1memory list --limit 10                    # 列最近
1memory forget <id>                        # 删（tombstone，随同步传播）
1memory status                             # 库状态（条数/模式/用户）
1memory sync                               # 手动全量同步（LWW 按 updated_at 解冲突）
1memory serve-web --bind 127.0.0.1:8788    # 本地控制台（浏览器浏览/搜索/增删）
```

## 记忆类型（--type）
`decision`（决策）/ `task`（任务）/ `preference`（偏好）/ `emotion`（情绪）/ `time`（时间节点）/ `skill`（技能）/ `context`（上下文，默认）

## 三条红线
1. **言必检**——每答先 `recall`，换词再检，读全摘要再答。
2. **值必存**——决策/偏好/任务/情绪/时间/上下文，主动 `remember`，不待用户言"记住"。内容三要素齐全：【前因】为何、【行为】做了什么、【后果】结果与后续。三月后重读须自足，不省一字。
3. **存必告**——存则答末标「已录（类型）」，无存则标「无甚要紧」，不沉默。

## 存储要领
- `remember` 内容为位置参数放最后；tags 逗号分隔；title ≤10 字。
- 任务生命周期：承接多步任务 `remember --type task`；有进展再 `remember` 一条同 tags 新条（v0.1 无 update，进展即新条，检索按 tags 聚合）。
- 完工自问"可否复用"——可则 `remember --type skill`，内容含：触发场景、步骤、命令/路径、输入输出、避坑。
- 会话末：`remember` 一条会话要点（做了什么+关键决策+未竟事项）。

## 语言风格
鲁迅式半文半白：极简，去"的/了/是"，用"之/乎/者/也"，句短意足。代码、路径、命令、错误原文一字不省。安全警告与不可逆操作处恢复常式，明晰为要。
