# 模块 06 - 导入导出管理

## 导入功能

将外部记忆文件导入到 ChromaDB 向量化存储中。

### 支持的格式

| 格式 | 说明 | 解析方式 |
|------|------|----------|
| Markdown (.md) | 按标题分段解析 | 标题→日期, 引用块→情绪/关键字 |
| 纯文本 (.txt) | 按空行分段 | 首行→日期(如 YYYY-MM-DD) |
| JSON (.json) | 结构化数据 | 按字段映射元数据 |

### 导入命令

```bash
# 从 Markdown 导入
python3 scripts/memory_core.py import-file memories.md --format markdown

# 从纯文本导入
python3 scripts/memory_core.py import-file notes.txt --format text

# 从 JSON 导入 (结构化,保留 ID 和元数据)
python3 scripts/memory_core.py import-file memories.json --format json
```

### Markdown 格式示例

```markdown
## 2025-03-15
> 情绪: high

今天和AI讨论了一个关于未来的想法，感觉很兴奋。
我们决定尝试一个新的架构方案。
```

导入后自动解析:
- 日期: 2025-03-15
- 情绪: high
- 内容: "## 2025-03-15\n今天和AI讨论……"

### JSON 格式示例

```json
{
  "memories": [
    {
      "id": "optional-uuid",
      "content": "记忆内容",
      "type": "emotion",
      "emotion": "high",
      "keywords": "关键词",
      "created_at": "2025-03-15T10:00:00",
      "created_date": "2025-03-15"
    }
  ]
}
```

## 导出功能

### 支持的格式

| 格式 | 说明 | 用途 |
|------|------|------|
| markdown | 标准排版 | 阅读、归档、打印 |
| timeline | 按时间线组织 | 年度回顾、记忆叙事 |
| json | 结构化向量数据 | 备份、迁移、跨系统 |

### 导出命令

```bash
# 导出为可读 Markdown
python3 scripts/memory_core.py export --format markdown --output memories.md

# 导出为时间线回忆录 (按日期分组)
python3 scripts/memory_core.py export --format timeline --output "2026回顾.md"

# 导出为 JSON (可重新导入)
python3 scripts/memory_core.py export --format json --output memories.json
```

### 时间线格式示例

导出的 Markdown 按日期分节:

```markdown
# 忆时 ・ 记忆时间线
导出日期: 2026-05-01
总记忆数: 42

## 2025-03-15

### 🟠 [EMOTION]
- 关键字: 未来, 想法, 兴奋
- 情绪: high
- 今天和AI讨论了一个关于未来的想法，感觉很兴奋

## 2025-03-20

### 🟡 [DECISION]
- 关键字: 架构, Python
- 情绪: medium
- 决定采用新的架构方案
```

## 完整备份/迁移流程

### 备份

```bash
# 1. 导出 JSON (包含所有向量数据)
python3 scripts/memory_core.py export --format json --output backup.json

# 2. 导出时间线 (人类可读)
python3 scripts/memory_core.py export --format timeline --output memories-timeline.md

# 3. 导出可读 Markdown
python3 scripts/memory_core.py export --format markdown --output memories.md
```

### 迁移到新设备

```bash
# 新设备上初始化
python3 scripts/memory_core.py init

# 导入
python3 scripts/memory_core.py import-file backup.json --format json
```

## 注意事项

- 导入时如果 ID 冲突会自动生成新 UUID
- 导出 JSON 可用于完整迁移，导出 Markdown 适合阅读
- 时间线导出时胶囊记忆会标记 🔒 锁图标
