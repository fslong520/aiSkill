# 模块二：创建技能

## 核心理念

```
技能 = 预定义上下文 + 执行规则 + 验证标准
```

## 流程

1. 收集需求（名称、描述、触发场景、输入输出）
2. 判断是否值得沉淀
3. 选择模板
4. 创建文件
5. 验证质量

## 判断标准

```
✅ 值得沉淀：
- 经常遇到
- 流程明确
- 可标准化

❌ 不值得：
- 一次性任务
- 流程不明确
```

## 简单技能模板

```markdown
---
priority: 500
name: {技能名}
description: "{emoji} {描述} | 触发：xxx"
metadata:
  version: "1.0.0"
  trigger: "触发关键字"
---

# {技能名}

## Keywords
关键词1、关键词2、关键词3

## Summary
一句话概括。

## Strategy
1. 步骤一
2. 步骤二

## Language
- 极致简练
- 用表格/列表代替段落
- 每句话有信息增量

## AVOID
- AVOID 错误行为1
- AVOID 错误行为2
```

## 复杂技能模板

```markdown
---
priority: 800
name: {技能名}
description: "{emoji} {描述} | 触发：xxx"
allowed-tools:
  - Read
  - Write

metadata:
  version: "1.0.0"
  trigger: "触发关键字"
---

# {技能名}

## Keywords
关键词1、关键词2、关键词3

## Summary
一句话概括。

## Strategy
1. 读取 modules/01-xxx.md
2. 执行步骤
3. 输出结果

## Language
- 极致简练
- 用表格/列表代替段落
- 每句话有信息增量

## AVOID
- AVOID 错误行为1
- AVOID 错误行为2
```

## 命名原则

| 好 | 差 |
|------|------|
| 搬题姬、墨池、雀影 | XXX工具、XXX助手 |
| 破晓、格知 | 超长名字、英文混杂 |

## 最佳实践

1. Spec-Driven：先定义规格
2. Context Compression：SKILL.md < 200行
3. Tool Selection：明确 allowed-tools
4. Verification-First：先定义验收标准

## AVOID

- AVOID 创建一次性任务为技能
- AVOID 命名功能性、无辨识度
- AVOID SKILL.md 过长不拆分
- AVOID 无 metadata.trigger
- AVOID 无示例
- AVOID 冗余描述
