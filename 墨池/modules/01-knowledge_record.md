# 知识点记录模块

> 核心功能：从对话中提取知识点，记录到知识库

## 触发条件

用户输入包含以下任一条件时触发：

| 触发词 | 示例 |
|--------|------|
| 疑问代词 | 什么、怎么、为什么、如何、哪、几、谁、何时、何地、多少、怎样 |
| 口语疑问词 | 为啥、干嘛、咋 |
| 疑问句式 | 是不是、对不对、好不好、能不能、可不可以 |
| 问号 | ？、? |
| 请求解释 | 解释、讲一下、说一下、介绍一下、帮我理解 |

## 执行流程

```
用户提问（触发墨池）
    ↓
1. 提取核心概念
   - 识别问题主题
   - 确定知识分类
   - 提取关键词作为标签
    ↓
2. 生成摘要
   - AI 根据回答内容生成一句话摘要（不超过 50 字）
    ↓
3. 检查是否已存在
   - read_file knowledge_index.txt
   - AI 搜索是否已有同名知识点
    ↓
4. 更新或创建
   - 已存在 → 更新 learning_count +1、last_learned、status
   - 不存在 → 创建新知识点块
    ↓
5. 计算过期日期
   - 根据分类查过期周期（见 expiry_rules.md）
   - expires_at = today + 周期天数
   - status = fresh
    ↓
6. 写入知识库
   - edit_file 更新 knowledge_index.txt
   - edit_file append learning_log.txt
    ↓
7. 继续对话（不等待，不打断）
```

## AI 原生操作示例

### 创建新知识点

```
AI 判断：
- 用户问"Hermes Agent 是什么"
- 核心概念：Hermes Agent
- 分类：AI架构
- 标签：Agent架构,记忆管理,上下文压缩
- 摘要：NousResearch开源的Agent记忆管理架构，解决长时间运行时的上下文压缩问题

AI 执行 edit_file：
在 knowledge_index.txt 末尾添加：

=== Hermes Agent ===
id: AI架构_001
category: AI架构
tags: Agent架构,记忆管理,上下文压缩
summary: NousResearch开源的Agent记忆管理架构，解决长时间运行时的上下文压缩问题
file: knowledge/AI架构/Hermes Agent.md
learning_count: 1
mastery: 了解
first_learned: 2026-04-14
last_learned: 2026-04-14
expires_at: 2026-07-14
status: fresh
source: 对话学习

AI 执行 edit_file：
在 learning_log.txt 末尾添加：

2026-04-14 22:50 | Hermes Agent | 新增 | 对话学习
```

### 更新已有知识点

```
AI 判断：
- 用户再次问"差分"
- 已存在知识点"差分"，learning_count=3

AI 执行 edit_file：
替换"差分"块，更新：
- learning_count: 4
- last_learned: 2026-04-14
- expires_at: 2027-04-14（重新计算）
- status: fresh

AI 执行 edit_file：
在 learning_log.txt 末尾添加：

2026-04-14 22:50 | 差分 | 复习 | 用户提问
```

## 不打断对话的原则

**铁律**：墨池记录是后台任务，不能打断正常对话！

```
错误做法：
用户：什么是差分？
AI：让我帮你记录这个知识点...（等待记录完成）...差分是...

正确做法：
用户：什么是差分？
AI：差分是前缀和的逆运算...（正常回答）
（后台异步执行 edit_file 更新知识库，不等待）
```

## 输出物

- `db/knowledge_index.txt` - 知识点块（新增或更新）
- `db/learning_log.txt` - 学习日志行（append）
- `knowledge/<分类>/<知识点>.md` - 详情文件（可选，复杂知识才创建）

## 检查清单

执行后自检：

- ✅ 知识点块格式正确（KV 格式）
- ✅ expires_at 已计算并填入
- ✅ status 已设置（fresh）
- ✅ learning_log.txt 已 append
- ✅ 对话未被打断