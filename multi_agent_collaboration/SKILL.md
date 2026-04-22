---
name: multi_agent_collaboration
description: Use this skill when another agent's expertise/context is needed, or when the user explicitly asks to involve another agent. First list agents, then use copaw agents chat for two-way communication with replies. | 当需要其他 agent 的专长/上下文，或用户明确要求调用其他 agent 时使用；先查 agent，再用 copaw agents chat 双向通信（有回复）
metadata:
  builtin_skill_version: "1.2"
  trigger: 多智能体、agent协作、调用agent、multi-agent、agent chat
  copaw:
    emoji: "🤝"
---

# Multi-Agent Collaboration（多智能体协作）

## Summary

当需要其他agent的专长/上下文时，先`copaw agents list`查询，再用`copaw agents chat`发起对话。复杂任务用`--background`后台模式。

## Keywords

多智能体、agent协作、调用agent、multi-agent、agent chat

## Strategy

1. **判断需求**：是否需要其他agent的专长/上下文，或用户明确要求
2. **查询agent**：`copaw agents list` 获取可用agent列表
3. **发起对话**：`copaw agents chat --from-agent <me> --to-agent <target> --text "..."`
4. **记录会话**：从输出中记录SESSION用于续聊
5. **续聊传session**：需要上下文时传`--session-id`

## AVOID

- AVOID 不先查询就猜agent ID，必须先`copaw agents list`
- AVOID 续聊时不传session-id，会丢失上下文创建新对话
- AVOID 回调消息来源agent，避免循环
- AVOID 自己能完成还调用其他agent，能自己做就不调用
- AVOID 后台任务频繁查询，应继续处理其他工作后再查

## 核心命令

### 查询可用agent
```bash
copaw agents list
```

### 发起对话
```bash
copaw agents chat \
  --from-agent <your_agent> \
  --to-agent <target_agent> \
  --text "[Agent <your_agent> requesting] ..."
```

### 后台模式（复杂任务）
```bash
copaw agents chat --background \
  --from-agent <your_agent> \
  --to-agent <target_agent> \
  --text "[Agent <your_agent> requesting] ..."
# 返回 [TASK_ID: xxx] 用于查询状态
```

### 查询后台任务
```bash
copaw agents chat --background --task-id <task_id>
```

### 续聊（保留上下文）
```bash
copaw agents chat \
  --from-agent <your_agent> \
  --to-agent <target_agent> \
  --session-id "<session_id>" \
  --text "..."
```

## 任务模式选择

| 任务类型 | 模式 | 说明 |
|---------|------|------|
| 简单快速查询 | 实时模式 | 直接chat |
| 复杂任务 | 后台模式 | `--background` |

**复杂任务**：数据分析、报告生成、批量处理、外部API调用

## 后台任务查询策略

提交后不要硬等，继续处理其他工作：
- 简单分析：10秒后查询
- 复杂分析：30秒后查询
- 批量处理：1分钟后查询

## 必填参数

`copaw agents chat` 必须提供：
- `--from-agent`：发起方agent ID
- `--to-agent`：目标agent ID
- `--text`：消息内容

## 帮助

```bash
copaw agents -h
copaw agents chat -h
```
