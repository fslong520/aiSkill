---
name: neural-shelf

description: |
  基于神经网络的智能文件整理系统，具备四阶段AI整理流程、神经感知分析、智能决策分类、
  安全执行和一键撤销恢复功能。采用深度学习算法分析文件内容、类型和关联关系，
  自动识别重复文件并提供智能分类建议。支持多种文件类型识别、自定义分类规则、
  批量处理和安全备份机制。适用于智能文件夹整理、重复文件处理、文档分类管理、
  存储空间优化等场景。提供详细的整理报告和操作日志，确保文件整理过程的可追溯性和安全性。

allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion

metadata:
  trigger: 智能文件整理、重复文件检测、文档分类管理、存储空间优化
  source: 基于深度学习的文件分析算法，参考现代文件管理系统设计理念
---

# NeuralShelf - 神经网络文件整理系统 v2.0

基于神经网络的智能化文件整理解决方案，采用内容相关性分组、项目结构保护、本地备份策略和准确去重判定机制。

## 核心改进 - v2.0版本变更

### 整理策略转变

#### 1. 内容导向整理（替代类型分类）
- **旧逻辑**：按文件类型（文档、图片、视频等）机械分类
- **新逻辑**：按内容相关性和语义主题智能分组，将相关文件聚合到一起
- **优势**：项目相关文件自动集中，相关资料不再分散

#### 2. 智能去重机制
- **MD5哈希检测**：快速识别完全相同的文件
- **去重统计**：原始文件数 → 去重后文件数，实时追踪
- **保留原始**：原文件保持不动，不删除任何文件

#### 3. 项目结构保护
- **识别标记**：检测 .git、.idea、package.json、pom.xml 等工程标记
- **优先保护**：项目文件单独分组，不被打乱
- **完整性保证**：工程结构保持原样

#### 4. 移动-复制备份策略
- **先移动后复制**：首先使用 mv 命令将原始文件移动到备份位置，再将整理后的文件复制到目标位置
- **两阶段执行**：阶段1移动原始文件到备份，阶段2从备份复制到新位置
- **本地备份路径**：各文件目录下的 backup/ 子目录
- **去重统计对比**：整理成功判定基于文件数量守恒

#### 5. 成功判定机制
- **数量守恒验证**：原始N个 → 去重M个 → 整理M个 = 成功
- **备份完整性**：确保所有去重后的文件都被整理
- **项目保护验证**：项目文件0被移动

#### 阶段一：神经感知分析阶段
- 深度扫描指定目录获取完整文件列表
- AI神经网络智能分析文件内容、类型和关联关系
- 识别文件间的逻辑联系和上下文关系
- 生成详细的文件特征分析报告

#### 阶段二：神经决策分类阶段
- AI神经网络基于文件内容、命名模式、文件类型和关联性进行综合分析
- 智能判断最合适的分类逻辑和归类标准
- 为每个文件确定最优目标位置
- 生成详细的文件移动整理方案
- 支持用户预览和确认整理方案

#### 阶段三：神经执行整理阶段
- **阶段3.1**：移动原始文件到备份位置（使用 mv 命令）
- **阶段3.2**：从备份位置复制文件到新的目标位置（使用 copy2）
- 支持批量操作提高效率
- 执行过程中实时记录操作日志
- 生成移动前后对比报告
- 确保操作的准确性和一致性

#### 阶段四：神经恢复保障阶段
- 完整记录所有操作的原始位置信息和备份路径
- 移动前自动创建备份确保数据安全
- 支持一键撤销功能完全恢复原始状态
- 提供操作历史查询和选择性撤销
- 确保整理过程的可逆性和安全性

### 2. 安全保护机制
- 所有文件移动前自动创建备份
- 完整的操作记录和审计日志
- 支持批量操作的原子性保证
- 权限检查和安全验证
- 磁盘空间充足性检查

### 3. 智能重复文件处理
- 基于内容哈希的精确重复检测
- 基于相似度的模糊重复识别
- 智能保留策略（最新/最大/最优质量）
- 重复文件隔离到专门文件夹
- 支持用户自定义重复处理规则

### 4. 详细报告系统
- 实时操作日志记录
- 移动前后文件状态对比
- 详细的统计信息和分析
- 时间戳和性能数据追踪
- 支持多种格式报告输出（Markdown/JSON/HTML）

## 快速开始

### 命令行使用

```bash
# 四阶段神经网络整理（推荐）
bash skill/NeuralShelf/scripts/run.sh smart-organize /path/to/target_directory

# 仅神经感知分析阶段 - 查看文件分析结果
bash skill/NeuralShelf/scripts/run.sh analyze-only /path/to/target_directory

# 仅神经决策阶段 - 生成整理方案供预览
bash skill/NeuralShelf/scripts/run.sh plan-only /path/to/target_directory

# 神经执行阶段 - 按方案执行整理
bash skill/NeuralShelf/scripts/run.sh execute-plan /path/to/target_directory --plan plan_file.json

# 神经恢复操作 - 恢复到整理前状态
bash skill/NeuralShelf/scripts/run.sh undo-last /path/to/target_directory

# 基础神经整理（兼容旧版本）
bash skill/NeuralShelf/scripts/run.sh organize /path/to/target_directory

# 仅神经检测重复文件
bash skill/NeuralShelf/scripts/run.sh scan-duplicates /path/to/target_directory

# 生成神经整理报告
bash skill/NeuralShelf/scripts/run.sh generate-report /path/to/target_directory

# 使用神经网络自定义配置
bash skill/NeuralShelf/scripts/run.sh smart-organize /path/to/target_directory --config custom.conf
```

### 自然语言使用

```
"智能整理我的下载文件夹"
"分析并制定文件分类方案"
"按AI建议整理我的文档"
"查看文件移动整理方案"
"执行文件整理计划"
"撤销刚才的文件整理"
"检测并处理重复的照片"
"生成详细的整理对比报告"
"预览整理前后的文件状态"
```

## 配置选项

### 基础配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `target_directory` | 整理目标目录 | 当前目录 |
| `exclude_patterns` | 排除文件模式列表 | `['*.tmp', '*.log']` |
| `duplicate_strategy` | 重复文件处理策略 | `keep_newest` |
| `backup_enabled` | 是否启用备份 | `true` |

### 文件类型映射

```yaml
file_types:
  documents:
    extensions: ['.pdf', '.doc', '.docx', '.txt', '.md']
    target_folder: 'Documents'
  images:
    extensions: ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    target_folder: 'Images'
  videos:
    extensions: ['.mp4', '.avi', '.mkv', '.mov']
    target_folder: 'Videos'
  code:
    extensions: ['.py', '.js', '.java', '.cpp', '.html', '.css']
    target_folder: 'Code'
```

### 命名规范模板

```yaml
naming_conventions:
  documents: '{year}/{month}/{filename}'
  images: '{year}/{month}/{day}/{filename}'
  default: '{category}/{filename}'
```

## 工作流程

### 阶段一：神经感知分析阶段
1. **目录深度扫描**
   - 递归扫描目标目录获取完整文件列表
   - 记录文件的基本属性（大小、修改时间、权限等）
   - 识别目录结构和嵌套关系

2. **AI神经网络内容分析**
   - 分析文件内容特征和文本信息
   - 识别文件类型和格式
   - 检测文件间的关联关系
   - 提取命名模式和时间信息

3. **特征提取报告**
   - 生成详细的文件特征分析报告
   - 识别潜在的分类标准
   - 标记需要注意的特殊情况

### 阶段二：神经决策分类阶段
1. **AI神经网络归类决策**
   - 基于内容、命名、类型等多维度分析
   - 智能判断最优分类逻辑
   - 为每个文件确定目标位置
   - 考虑文件间的关联性

2. **方案生成与预览**
   - 生成详细的移动整理方案
   - 支持用户预览和确认
   - 提供多种整理策略选择
   - 标记潜在风险操作

3. **安全检查**
   - 验证目标路径的可写性
   - 检查磁盘空间是否充足
   - 确认权限是否足够
   - 评估操作风险等级

### 阶段三：神经执行整理阶段
1. **备份创建**
   - 为所有涉及的文件创建备份
   - 记录原始位置和状态信息
   - 生成操作前快照

2. **批量移动执行**
   - 按照整理方案逐个执行移动
   - 实时记录操作日志
   - 监控执行状态和进度
   - 处理异常情况

3. **状态验证**
   - 验证移动结果的正确性
   - 检查文件完整性
   - 更新操作记录

### 阶段四：神经报告生成阶段
1. **前后状态对比**
   - 生成整理前后的目录结构对比
   - 统计各类文件的数量变化
   - 展示移动路径和结果

2. **详细报告生成**
   - 操作日志和时间线
   - 成功/失败统计信息
   - 性能数据和耗时分析
   - 问题和建议总结

3. **操作记录保存**
   - 完整的操作历史记录
   - 支持后续撤销操作
   - 便于审计和追溯

## 安全机制

### 四重安全保障

#### 1. 操作前安全检查
- **权限验证**: 严格检查目录读写权限
- **空间检查**: 验证目标磁盘空间是否充足
- **锁定检测**: 检查文件是否被其他进程占用
- **只读保护**: 识别并妥善处理只读文件

#### 2. 执行期数据保护
- **双重备份**: 移动前创建时间戳备份
- **原子操作**: 支持批量操作的事务性保证
- **状态快照**: 记录操作前的完整文件状态
- **实时监控**: 执行过程中的状态跟踪

#### 3. 操作后验证机制
- **完整性校验**: 验证移动后文件的完整性
- **路径验证**: 确认文件确实到达目标位置
- **权限确认**: 验证新位置的访问权限
- **大小对比**: 核对文件大小确保传输完整

#### 4. 撤销恢复保障
- **完整记录**: 详细记录每次操作的原始信息
- **一键撤销**: 支持快速恢复到操作前状态
- **选择性恢复**: 可选择性撤销特定操作
- **历史追溯**: 完整的操作历史查询功能

## 输出示例

### 四阶段流程控制台输出
```
🎯 开始四阶段神经网络整理: /home/user/Downloads

📋 阶段一：神经感知分析完成
📊 扫描到 156 个文件
🔍 识别出 23 个文档、67 张图片、8 个视频
⏱️ 分析耗时: 1.2 秒

🧠 阶段二：神经决策完成
💡 神经网络生成 4 类整理方案
📄 方案已保存至: plans/smart_plan_20240115_1430.json
✅ 用户确认执行方案

🛡️ 阶段三：神经执行中
🔒 创建备份: 156 个文件已备份
🔄 执行移动: 89 个文件移动成功
⚠️ 警告: 3 个文件因权限问题跳过
✅ 执行完成，耗时 2.1 秒

📈 阶段四：神经报告生成
📊 移动统计: 文档(+15) 图片(+42) 视频(+5)
📄 详细报告: reports/smart_report_20240115_1430.md
🔍 操作日志: logs/operations_20240115_1430.log
✅ 智能整理全部完成！
```

### 四阶段详细报告内容
```markdown
# NeuralShelf 神经网络整理报告 - 2024-01-15 14:30:25

## 📋 阶段一：神经感知分析报告

### 基础扫描结果
- **目标目录**: `/home/user/Downloads`
- **扫描文件数**: 156 个
- **目录层级**: 4 层深度
- **分析耗时**: 1.2 秒

### 文件类型分布
| 类型 | 数量 | 占比 | 平均大小 |
|------|------|------|----------|
| 文档文件 | 23 | 14.7% | 2.3 MB |
| 图片文件 | 67 | 42.9% | 1.8 MB |
| 视频文件 | 8 | 5.1% | 45.2 MB |
| 代码文件 | 15 | 9.6% | 3.1 KB |
| 其他文件 | 43 | 27.7% | 0.8 MB |

### 关联关系分析
- **命名相关文件组**: 12 组
- **时间连续文件**: 23 个
- **项目相关文件**: 8 组

## 🧠 阶段二：神经决策方案

### 神经网络分类策略
1. **按内容类型分类** (权重: 40%)
   - 文档 → Documents/{年}/{月}/
   - 图片 → Images/{年}/{月}/{日}/
   - 视频 → Videos/{年}/{月}/

2. **按项目关联分类** (权重: 30%)
   - 项目A文件 → Projects/A/
   - 项目B文件 → Projects/B/

3. **按时间顺序分类** (权重: 20%)
   - 按年月日层级组织

4. **按重要性分类** (权重: 10%)
   - 重要文件 → Important/

### 整理方案详情
```json
{
  "total_files": 156,
  "move_operations": 89,
  "skip_operations": 67,
  "backup_required": 89,
  "estimated_time": "2.1 seconds",
  "risk_level": "low"
}
```

## 🛡️ 阶段三：神经执行与备份

### 备份详情
| 文件 | 备份路径 | 备份时间 | 状态 |
|------|----------|----------|------|
| report.pdf | Backups/20240115_143025/report.pdf | 14:30:25 | ✅ |
| photo.jpg | Backups/20240115_143025/photo.jpg | 14:30:25 | ✅ |

### 移动执行记录
| 源路径 | 目标路径 | 文件大小 | 执行时间 | 状态 |
|--------|----------|----------|----------|------|
| Downloads/report.pdf | Documents/2024/01/report.pdf | 2.1 MB | 14:30:26 | ✅ |
| Downloads/photo.jpg | Images/2024/01/15/photo.jpg | 1.8 MB | 14:30:26 | ✅ |
| Downloads/video.mp4 | Videos/2024/01/video.mp4 | 45.2 MB | 14:30:27 | ✅ |

### 异常处理
- **跳过文件**: 3 个（权限不足）
- **警告文件**: 2 个（只读属性）
- **失败操作**: 0 个

## 📈 阶段四：神经前后对比分析

### 整理效果统计
| 指标 | 整理前 | 整理后 | 变化 |
|------|--------|--------|------|
| 文档文件 | 8 个 | 23 个 | +15 (+187%) |
| 图片文件 | 25 个 | 67 个 | +42 (+168%) |
| 视频文件 | 3 个 | 8 个 | +5 (+167%) |
| 代码文件 | 5 个 | 15 个 | +10 (+200%) |
| 其他文件 | 115 个 | 43 个 | -72 (-63%) |

### 目录结构改善
**整理前**: 杂乱无章的单一目录
**整理后**: 清晰的多级分类结构
- 按类型分离：不同类型文件归类存放
- 按时间组织：便于查找历史文件
- 按项目分组：相关文件集中管理

### 存储优化
- **空间释放**: 释放了 15% 的目录空间
- **查找效率**: 文件查找时间减少 70%
- **管理便利**: 目录浏览更加直观清晰

## 🔄 撤销信息

### 操作记录标识
- **会话ID**: SESSION_20240115_143025
- **备份位置**: `/home/user/.file-organizer/backups/SESSION_20240115_143025/`
- **可撤销操作**: 89 个移动操作
- **撤销时效**: 支持7天内完全撤销

### 撤销命令
```bash
# 撤销本次神经网络整理
bash skill/NeuralShelf/scripts/run.sh undo-session SESSION_20240115_143025

# 查看可撤销神经网络操作
bash skill/NeuralShelf/scripts/run.sh list-sessions
```
```

## 故障排除

### 常见问题

**Q: 权限被拒绝错误**
A: 确保对目标目录有读写权限，或者使用 `sudo` 运行

**Q: 磁盘空间不足**
A: 清理不必要的文件或调整重复文件处理策略

**Q: 部分文件无法移动**
A: 检查文件是否被其他程序占用，或是否为只读文件

**Q: 配置文件加载失败**
A: 检查配置文件格式是否正确，参考默认配置模板

**Q: 如何撤销整理操作**
A: 使用 `undo-session` 命令撤销指定会话的操作

**Q: 备份文件丢失怎么办**
A: 检查 `.file-organizer/backups/` 目录，或使用 `list-backups` 查看可用备份

**Q: 整理方案不满意如何调整**
A: 使用 `plan-only` 模式生成方案后手动编辑，再用 `execute-plan` 执行

### 日志查看
```bash
# 查看详细操作日志
cat /home/fslong/.qoder/skills/NeuralShelf/logs/organizer.log

# 查看错误日志
cat /home/fslong/.qoder/skills/file-organizer/logs/error.log

# 查看特定会话日志
cat /home/fslong/.qoder/skills/file-organizer/logs/session_20240115_143025.log

# 查看备份记录
cat /home/fslong/.qoder/skills/file-organizer/logs/backups.log
```

## 依赖要求

```bash
# Python 3.8+
python -m pip install -r requirements.txt
```

主要依赖包：
- `pathlib` - 路径操作
- `hashlib` - 文件哈希计算
- `yaml` - 配置文件解析
- `datetime` - 时间处理
- `logging` - 日志系统

## 高级用法

### 四阶段流程控制
```bash
# 完整四阶段神经网络整理（推荐）
bash skill/NeuralShelf/scripts/run.sh smart-organize /home/user/Downloads

# 分步执行：先神经感知分析再决策
bash skill/NeuralShelf/scripts/run.sh analyze-only /home/user/Downloads
bash skill/NeuralShelf/scripts/run.sh plan-only /home/user/Downloads

# 手动审核神经网络方案后执行
bash skill/NeuralShelf/scripts/run.sh execute-plan /home/user/Downloads --plan my_plan.json
```

### 撤销和恢复操作
```bash
# 查看可撤销的神经网络操作会话
bash skill/NeuralShelf/scripts/run.sh list-sessions

# 撤销特定神经网络会话的所有操作
bash skill/NeuralShelf/scripts/run.sh undo-session SESSION_20240115_143025

# 选择性撤销特定神经网络文件
bash skill/NeuralShelf/scripts/run.sh undo-file /path/to/file
```

### 自定义规则
创建 `custom_rules.py` 文件定义特殊处理逻辑：

```python
def custom_classification(file_path, file_content):
    """自定义文件分类规则"""
    if 'urgent' in file_path.name.lower():
        return 'Urgent'
    return None

def custom_backup_strategy(file_path):
    """自定义备份策略"""
    # 对重要文件创建额外备份
    if file_path.suffix in ['.pdf', '.docx']:
        return True
    return False
```

### 批量处理
```bash
# 并行处理多个目录
for dir in dir1 dir2 dir3; do
    bash skill/NeuralShelf/scripts/run.sh smart-organize "$dir" &
done
wait

# 按优先级顺序处理
dirs=("work" "downloads" "documents")
for dir in "${dirs[@]}"; do
    bash skill/NeuralShelf/scripts/run.sh smart-organize "/home/user/$dir"
done
```

### 定时智能整理
```bash
# 添加到 crontab 每周日凌晨3点执行智能整理
0 3 * * 0 bash /path/to/skill/NeuralShelf/scripts/run.sh smart-organize /home/user/Downloads

# 每日备份检查和清理
0 2 * * * bash /path/to/skill/NeuralShelf/scripts/run.sh cleanup-backups --days 7
```