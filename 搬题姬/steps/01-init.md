# Step 1: 环境初始化

## 目标

自模板目录复文件至带题目标识之工作目录。

## 基路径

### 桌面路径检测（跨平台）

先检测用户桌面路径，后续所有工作目录创建于桌面。

```bash
# 自动检测桌面路径（支持 Linux / macOS / Windows）
# 检测到路径后确保目录存在，不存在则创建
detect_desktop() {
    local d=""
    # Linux: ~/.config/user-dirs.dirs 中有 XDG_DESKTOP_DIR
    if [ -f "$HOME/.config/user-dirs.dirs" ]; then
        . "$HOME/.config/user-dirs.dirs"
        if [ -n "$XDG_DESKTOP_DIR" ] && [ -d "$XDG_DESKTOP_DIR" ]; then
            echo "$XDG_DESKTOP_DIR"
            return
        fi
    fi
    # macOS: ~/Desktop
    d="$HOME/Desktop"; [ -d "$d" ] && echo "$d" && return
    # Linux 中文: ~/桌面
    d="$HOME/桌面";   [ -d "$d" ] && echo "$d" && return
    # Linux 西班牙语: ~/Escritorio
    d="$HOME/Escritorio"; [ -d "$d" ] && echo "$d" && return
    # Windows Git Bash / WSL: ~/Desktop (再试一次)
    d="$HOME/Desktop"; [ -d "$d" ] && echo "$d" && return
    # 兜底：使用 ~/Desktop，不存在则创建
    mkdir -p "$HOME/Desktop"
    echo "$HOME/Desktop"
}
```

## 工作目录命名

**格式：** `{BASE_DIR}/work_{PID}_{标题简写}`

| 阶段 | 目录名 | 说明 |
|------|--------|------|
| 初始化时 | `{BASE_DIR}/work` 或 `{BASE_DIR}/work_{PID}` | PID已知则径用，未知暂用 `work` |
| 得PID后（step 2） | `{BASE_DIR}/work_{PID}` | 自URL取PID后更名 |
| 定标题后（step 4） | `{BASE_DIR}/work_{PID}_{标题简写}` | 生题面后加标题简写 |

**标题简写规则：**
- 英文标题：取完整标题，空格易下划线，转小写（如 `Trimo` → `trimo`）
- 中文标题：取前 4~8 字（如 `移除前导o` → `移除前导o`）
- 标题过长则截取前 20 字符

> **工作目录变量**：后诸步骤中，以 `{WORK_DIR}` 指 `{BASE_DIR}/work_{PID}_{标题简写}`。
> AI 当于上下文中记 `{WORK_DIR}` 之值，所有文件操作皆基于此目录。

## 命令

### 其一：PID 已知（自 URL 或上下文可定）

```bash
BASE_DIR=$(detect_desktop)
rm -rf $BASE_DIR/work_{PID} 2>/dev/null
cp -r question $BASE_DIR/work_{PID}
# {WORK_DIR} = $BASE_DIR/work_{PID}
```

### 其二：PID 未知（首初始化）

```bash
BASE_DIR=$(detect_desktop)
rm -rf $BASE_DIR/work 2>/dev/null
cp -r question $BASE_DIR/work
# {WORK_DIR} = $BASE_DIR/work（后得信息后更名）
```

## 模板位置

1. `$BASE_DIR/question/` — 若用户预置模板于桌面
2. `SKILL.md 所在目录/question/` — 技能自带模板
3. `当前工作目录/question/` — 兜底

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
