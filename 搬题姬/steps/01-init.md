# Step 1: 环境初始化

## 目标

从模板目录复制文件到带题目标识的工作目录。

## 工作目录命名规范

**格式：** `work_{PID}_{标题简写}`

| 阶段 | 目录名 | 说明 |
|------|--------|------|
| 初始化时 | `work` 或 `work_{PID}` | PID已知则直接用，未知先用 `work` |
| 获取PID后（step 2） | `work_{PID}` | 从URL提取PID后重命名 |
| 确定标题后（step 4） | `work_{PID}_{标题简写}` | 生成题面后加上标题简写 |

**标题简写规则：**
- 英文标题：取完整标题，空格替换为下划线，转小写（如 `Trimo` → `trimo`）
- 中文标题：取前 4~8 个字（如 `移除前导o` → `移除前导o`）
- 标题过长时截取前 20 个字符

> **工作目录变量**：后续所有步骤中，用 `{WORK_DIR}` 表示当前工作目录名。
> AI 需在上下文中记住 `{WORK_DIR}` 的值，所有文件操作都基于此目录。

## 命令

### 情况一：PID 已知（从 URL 或上下文可确定）

```bash
rm -rf work_{PID} 2>/dev/null
cp -r question work_{PID}
# {WORK_DIR} = work_{PID}
```

### 情况二：PID 未知（首次初始化）

```bash
rm -rf work 2>/dev/null
cp -r question work
# {WORK_DIR} = work（后续获取信息后重命名）
```

## 模板位置

1. `SKILL.md 所在目录/question/`
2. `当前工作目录/question/`

## 模板文件

| 文件 | 用途 |
|------|------|
| `std.cpp` | 标程模板 |
| `mkdata.cpp` | 数据生成器模板 |
| `mkin.h` | 测试数据逻辑模板 |
| `problem.yaml` | 配置文件模板 |

## 重要：后续步骤的路径

所有后续步骤中，引用文件时使用 `{WORK_DIR}/xxx` 而非 `work/xxx`。
AI 需记住 `{WORK_DIR}` 的值，并在以下步骤中保持一致。

## 下一步

成功 → `02-get-info.md`

失败 → 检查模板目录是否存在
