# Step 1: 环境初始化

## 目标

自模板目录复文件至带题目标识之工作目录。

## 工作目录命名

**格式：** `work_{PID}_{标题简写}`

| 阶段 | 目录名 | 说明 |
|------|--------|------|
| 初始化时 | `work` 或 `work_{PID}` | PID已知则径用，未知暂用 `work` |
| 得PID后（step 2） | `work_{PID}` | 自URL取PID后更名 |
| 定标题后（step 4） | `work_{PID}_{标题简写}` | 生题面后加标题简写 |

**标题简写规则：**
- 英文标题：取完整标题，空格易下划线，转小写（如 `Trimo` → `trimo`）
- 中文标题：取前 4~8 字（如 `移除前导o` → `移除前导o`）
- 标题过长则截取前 20 字符

> **工作目录变量**：后诸步骤中，以 `{WORK_DIR}` 指当前工作目录名。
> AI 当于上下文中记 `{WORK_DIR}` 之值，所有文件操作皆基于此目录。

## 命令

### 其一：PID 已知（自 URL 或上下文可定）

```bash
rm -rf work_{PID} 2>/dev/null
cp -r question work_{PID}
# {WORK_DIR} = work_{PID}
```

### 其二：PID 未知（首初始化）

```bash
rm -rf work 2>/dev/null
cp -r question work
# {WORK_DIR} = work（后得信息后更名）
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

## 后续路径

后诸步骤引文件时用 `{WORK_DIR}/xxx` 而非 `work/xxx`。
AI 当记 `{WORK_DIR}` 之值，下步一致。

## 下一步

成 → `02-get-info.md`

败 → 查模板目录存否
