# 过期机制模块

> 知识会过时，需要定期验证。AI 自己判断，不用 Python 脚本！

## 核心功能

1. **过期检查**：判断知识是否过期
2. **过期报告**：生成过期状态报告
3. **知识验证**：验证过期知识是否仍有效
4. **存档清理**：删除存档超过 30 天的知识

## 过期周期规则

详见 [references/expiry_rules.md](../references/expiry_rules.md)

速查表：

| 分类 | 周期 |
|------|------|
| 工具使用 | 60 天 |
| 计算机基础 | 90 天 |
| 算法数据结构 | 365 天 |
| 信竞教学 | 365 天 |
| 数学 | 永不过期 |
| 生活健康 | 365 天 |

## 命令处理

### `/墨池 过期报告`

**执行流程**：

```
1. read_file knowledge_index.txt
2. AI 遍历每个知识点，计算状态：
   - 当前日期 - last_learned = 已过天数
   - 查周期表，判断 fresh/aging/stale/permanent
3. 生成 Markdown 格式报告
4. 输出给用户
```

**报告格式**：

```markdown
# 墨池知识过期报告

生成时间：2026-04-14 22:50

## 状态概览

| 状态 | 数量 |
|------|------|
| 🟢 新鲜 | 5 |
| 🟡 老化 | 2 |
| 🔴 需验证 | 1 |
| ⭐ 永不过期 | 3 |

## 需验证的知识点

- **ClawHub技能发布** (工具使用) - 过期于 2026-05-29
- **测试知识点** (测试) - 过期于 2026-04-29
```

### `/墨池 验证 <知识点>`

**执行流程**：

```
1. read_file knowledge_index.txt，找到目标知识点
2. 向用户提问："【知识点名称】是否仍有效？内容有无变化？"
3. 用户确认：
   - "有效" → edit_file 更新 expires_at（重新计算）、status=fresh、last_verified=今天
   - "无效" → edit_file 更新 status=archived、archived_at=今天
4. edit_file append learning_log.txt 记录事件
```

### `/墨池 永不过期 <知识点>`

**执行流程**：

```
1. read_file knowledge_index.txt，找到目标知识点
2. edit_file 更新：
   - expires_at: never
   - status: permanent
3. edit_file append learning_log.txt 记录事件
```

### `/墨池 清理存档`

**执行流程**：

```
1. read_file knowledge_index.txt
2. AI 遍历 archived 状态的知识点
3. 判断：当前日期 - archived_at ≥ 30 天 → 删除
4. 对于要删除的：
   - edit_file 删除整个块
   - 删除对应的 knowledge/xxx.md 文件（如果存在）
5. edit_file append learning_log.txt 记录删除事件
6. 输出删除列表给用户
```

## AI 判断逻辑

**判断状态（伪代码，不是 Python！）**：

```
对于每个知识点：
  如果 expires_at == 'never':
    状态 = 'permanent'
  
  否则：
    已过天数 = 当前日期 - last_learned
    周期天数 = 查表(category)
    
    如果 已过天数 < 周期天数的一半:
      状态 = 'fresh'
    如果 已过天数 < 周期天数:
      状态 = 'aging'
    否则:
      状态 = 'stale'
```

## 定期检查建议

建议每月执行一次 `/墨池 过期报告`，及时验证过期知识。

## 输出物

- 过期报告（Markdown 格式输出）
- 更新后的 `knowledge_index.txt`（验证/标记后）
- 更新后的 `learning_log.txt`（记录事件）

## 检查清单

- ✅ 状态判断正确（按周期规则）
- ✅ 报告格式清晰（Markdown 表格）
- ✅ 验证后更新了 expires_at 和 status
- ✅ learning_log.txt 已记录事件