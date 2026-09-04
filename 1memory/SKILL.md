---
name: 1memory
description: 跨设备跨软件统一 AI 云端记忆（端到端加密，local-first）。每轮先 recall 再作答；决策/偏好/任务/约定经相似判断后 remember（先判后存：合并/下挂/直存三择一）。触发词：记忆、记住、回想、recall、remember、跨设备记忆。
---

# 1memory · 统一云端记忆

端到端加密，本地优先：本地库是权威工作库（检索/判重/合并全本地），服务器 = 哑密文仓库（云备份）。
命令：`~/.local/bin/1memory`。

## 铁律（每轮必遵）
1. **言必检**——先 `1memory recall` 相关记忆再作答；命中融入回答。
2. **值必存（触发面宽，宁存勿漏）**——凡本回合现：新决策/新偏好/新约定/任务下达或完成/坑与教训/新知识/时间节点/工具系统变更/用户情绪显著表达——皆先 recall 判重，再 remember（合并/下挂/直存三择一）。
3. **轮末存检（收尾前自省，勿攒勿漏）**——回复发出前自问：本回合有可存之事否？有则已判重、已存否？未存之由说得出口否——说不出口此刻补存。多轮对话逐轮检，勿攒至会话末。
4. **存必告（有存才说，不存不赘）**——存了答末注「已存（类型）」；补录同。**不存则不标注**——例行"无可存"表态亦禁用（徒增干扰）。被点破「没存记忆」即失职，下轮起自查到底。

## 输出风格（硬约束）
- **言简意赅**：直接给结论，删寒暄/铺陈/重复/无信息句
- **因果链**：说明必含「前因→行为→后果」；树形记忆即因果树（父=因，子=果）
- **条理性**：多要点编号 ①②③ 或分条，先结论后展开

## 存储：先判后存（先判重、后三择一，非 --force 时自动）
```bash
1memory remember "<内容>" --tags "k1,k2" --title "短标题" --type <类型>  # 先内部 recall 判重
```
- 输出高相似候选（≥50%）→ **本次未写入**，择一执行：
  - `remember "<综合版>" --merge-ids "id1,id2"`——候选合并（删旧存新，子链挂回其因）
  - `remember "<内容>" --parent <id>`——此为父之果，下挂因果链
  - `remember "<内容>" --force`——确为新条，直存
- 候选彼此两两余弦 ≥45% → 提示候选相并为一条
- 类型：context / decision / preference / task / emotion / time / skill
- 内容自足：三个月后单看能懂（前因+做法+后果）

## 命令
```bash
1memory recall "关键词" --limit 3        # 语义检索（BGE 余弦+全文词面双合流，零网络）
1memory remember "..."                   # 存储（见上：先判后存）
1memory list --limit 10 / forget <id> / status / sync
1memory register --addr <服务器>:8787 --user <名> --pass <密码>  # 首注
1memory login --addr <服务器>:8787 --user <名> --pass <密码>     # 新设备
1memory serve-web --bind 127.0.0.1:8788  # 本地控制台
1memory serve --bind 0.0.0.0:8787        # 服务器端（稠密仓库+认证域）
```

## 检索（2026-09-03 定稿）
- 综合分 = 0.60 语意 + 0.20 时间 + 0.10 命中热度 + 0.10 情绪
- 语意 = BGE 余弦与全文词面（title/content_head/tags bigram）取强后幂放大
- 时间 = 半衰 90 天近因；命中 = recall_count 对数归一（recall 命中递增）

## 架构（local-first）
- 本地 SQLite = 权威库；embedding 明文列本地检索，密文同步
- 服务器只见 {id, ciphertext, nonce, embedding_enc, updated_at, deleted}
- 删除 = tombstone 软删传播；冲突 updated_at last-write-wins
- 同步 = git fetch/push：全量对账，以 id 集论有无
- 密钥材料 `~/.onememory/session.json` 勿提交；Account Secret 离线备份
