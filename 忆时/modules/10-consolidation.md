# 模块 10 - 记忆自动梳理

**何时读**：对话启始检查梳理状态，末次梳理距今超过 7 日时；用户输入 `/忆时 梳理` 时。

**每七日一梳理，沉淀精华，去芜存菁。** 此乃对抗"窗口即牢笼"之根本策略——将散落各对话之碎片，聚为结构化知识。

## 追踪梳理时间

以特殊记忆追踪末次梳理时间。每次对话启始，先查：
```bash
MEMO_DIR=~/.local/share/opencode/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
  recall "记忆梳理" --type-filter time --limit 1 --min-weight 0.1
```
- **返回末次梳理时间**：有结果则告知用户"上次梳理于 XXXX-XX-XX"；无结果则言"尚无梳理记录"。
- 若无结果，或末次梳理距今超过 7 日 → 触发梳理流程。
- 梳理毕，以 `--type time --emotion 0.5 --keywords "记忆梳理,consolidation"` 存储新时间戳：
  ```bash
  MEMO_DIR=~/.local/share/opencode/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
    store "上次记忆梳理时间: YYYY-MM-DD" --type time --emotion 0.5 --keywords "记忆梳理,consolidation"
  ```
- 梳理完成，告知用户"梳理完毕，上次梳理时间已更新"。

## 梳理流程

1. **导出所有记忆**
   ```bash
   MEMO_DIR=~/.local/share/opencode/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
     export --format timeline --output /tmp/yishi_export.md
   ```
2. **AI 分析导出内容**——以 AI 原生工具读 `/tmp/yishi_export.md`，提取：
   - 高频主题、重复偏好、常见决策模式
   - 用户之习惯、工具偏好、工作流
   - 长期任务之进度、阻滞点
3. **沉淀为结构化记忆**：每一条主题存为一条记忆，示例：
   ```bash
   MEMO_DIR=~/.local/share/opencode/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/memory_core.py \
     store "主题摘要" --type 类型 --emotion 0.5 --keywords "主题关键词,consolidated"
   ```
   其中 `keywords` 须含 `consolidated` 标签，以示此条乃梳理产物。
4. **清理临时文件**：`rm /tmp/yishi_export.md`

## 梳理原则

- 宁精勿杂：一条梳理结果应覆盖一类模式/主题，而非罗列琐碎。
- 追加之，非替代之：梳理不删除原始记忆。原始碎片保留，梳理结果作为上层索引。
- 频率>7日可跳：若用户对话稀疏，7日内无新记忆，则不必空转。
- 情绪高之记忆优先：梳理时，优先关注情绪值 ≥0.7 之条目，此乃用户最在意之事。
- 对比旧梳理：检索已有 `--keywords "consolidated"` 之记忆，比对新增内容，避免重复沉淀。

完成后回复：`"梳理毕。"`
