# Step 9: 打包发布

## 目标

题包经审计（Step 8）通过后，打包题文件为 zip。

## 前置

⚠️ **审计必先行！本步骤假定 Step 8（审计）已全过。未经审计径打包者，后果自负。**

## 基路径

**所有工作目录在桌面。打包时 `{WORK_DIR}` 已含 `detect_desktop()` 检测出的完整路径。**

## 打包前查

```bash
rm -f {WORK_DIR}/std {WORK_DIR}/mkdata {WORK_DIR}/*.exe
```

## 打包命令

文件名：`{pid}_{title}.zip`

```bash
# ✅ 正：打包整个 {WORK_DIR} 目录（解压后有 {WORK_DIR}/ 外壳）
zip -r {pid}_{title}.zip {WORK_DIR}

# ❌ 误：进 {WORK_DIR} 打包（文件散根目录）
cd {WORK_DIR} && zip -r ../{pid}_{title}.zip .
```

## 验打包构

```bash
unzip -l {pid}_{title}.zip | head -6
# 必出：
#   {WORK_DIR}/
#   {WORK_DIR}/std.cpp
#   {WORK_DIR}/problem_zh.md
#   {WORK_DIR}/mkin.h
#   {WORK_DIR}/testdata/
```

## 常见错

### config.yaml 格式（HydroOJ）

荐用 subtask 分组格式：

```yaml
# ✅ 正：顶层 time/memory 为全局默认（可被子任务覆盖）
type: default
time: 1s
memory: 512m
subtasks:
  - score: 10
    id: 0
    cases:
      - input: 1.in
        output: 1.out
  - score: 90
    id: 1
    cases:
      - input: 2.in
        output: 2.out
      - input: 3.in
        output: 3.out
```

**注：**
- 用 subtask 时必显列所有 `cases`
- `subtasks[].id` 议从 0 始编
- 总分持 100
- **必设顶层 `time` 与 `memory`**（缺省会显异常值如 65535MB）
- `type` 缺为 `default`，`time`/`memory` 可在子任务层覆

### 打包构

```
❌ 误：文件径放根目录
{pid}_{title}.zip
├── std.cpp

✅ 正：有 {WORK_DIR} 目录
{pid}_{title}.zip
└── {WORK_DIR}/
    ├── std.cpp
```

### 大样例

| 大小 | 措 |
|------|------|
| < 500 字节 | `read_file` |
| ≥ 500 字节 | 禁 `read_file`，用 shell |

## 原创题

`pid: null` 时：

```bash
zip -r 原创_{title}.zip {WORK_DIR}
```

## 完成

发 zip 文件予用户。
