# 模块 01 - 初始化与 Chroma 管理

## 目标

初始化 ChromaDB 向量数据库，建立必要的集合。

## 执行步骤

1. 检查 Python 3.13 是否可用
2. 检查 chromadb 是否已安装
3. 运行初始化命令:

```bash
python3 /home/fslong/.config/opencode/skills/忆时/scripts/memory_core.py init
```

4. 确认输出包含"忆时记忆系统初始化完成"

## 集合结构

ChromaDB 内会创建以下集合:

| 集合名 | 用途 | 距离度量 |
|--------|------|----------|
| memories | 长期记忆向量存储 | cosine |
| relationships | 记忆间关联关系 | cosine |
| meta | 系统状态元数据 | cosine |

## 记忆元数据结构

每条记忆包含以下元数据:

```json
{
  "type": "context",
  "emotion": "medium",
  "emotion_weight": 0.5,
  "created_at": "2025-01-15T10:30:00",
  "created_date": "2025-01-15",
  "updated_at": "2025-01-15T10:30:00",
  "keywords": "Python,学习,装饰器",
  "source": "manual",
  "source_session": "",
  "frequency": "1",
  "recall_count": "0",
  "is_capsule": "false",
  "capsule_unlock_at": ""
}
```

## 模型安装

本技能使用 all-MiniLM-L6-v2 embedding 模型。
首次初始化时会自动安装：有离线包则解压 `models/onnx.tar.gz`，否则从 Chroma S3 下载。
安装后模型文件位于 `models/all-MiniLM-L6-v2/onnx/` 目录。

> ⚠️ 模型不会写入 `~/.cache/chroma/`，清缓存不会被删除。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| YISHI_DATA_DIR | ~/.config/opencode/skills/忆时/data | ChromaDB 存储路径 |
