# ChromaDB API 参考 (忆时用)

## 版本

- chromadb 1.5.4
- Python 3.13+

## 客户端初始化

```python
import chromadb
client = chromadb.PersistentClient(path="/path/to/data")
```

## 集合操作

```python
# 创建或获取集合
collection = client.get_or_create_collection(
    name="memories",
    metadata={"hnsw:space": "cosine"}
)

# 添加文档
collection.add(
    documents=["记忆内容"],
    metadatas=[{"type": "context", "emotion": "medium"}],
    ids=["uuid"]
)

# 查询 (语义搜索)
results = collection.query(
    query_texts=["查询关键词"],
    n_results=10
)

# 获取特定文档
doc = collection.get(ids=["uuid"])

# 更新
collection.update(
    ids=["uuid"],
    documents=["新内容"],
    metadatas=[{"type": "new_type"}]
)

# 删除
collection.delete(ids=["uuid"])

# 统计数量
count = collection.count()
```

## 查询结果结构

```python
{
    "ids": [["id1", "id2", ...]],
    "documents": [["doc1", "doc2", ...]],
    "metadatas": [[metadata1, metadata2, ...]],
    "distances": [[0.1, 0.2, ...]],  # cosine distance, 越小越相似
}
```

语义相似度 = 1.0 - distance

## 注意事项

- ChromaDB 自动向量化文本 (text-embedding)
- cosine 距离范围: 0 (完全相同) 到 2 (完全相反)
- metadatas 中的值必须是字符串或数字
- PersistentClient 自动持久化到磁盘
