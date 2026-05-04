# Step 8: 打包发布

## 目标

打包题目文件为 zip 包。

## 打包前检查

```bash
rm -f work/std work/mkdata work/*.exe
```

## 打包命令

文件名：`{pid}_{title}.zip`

```bash
# ✅ 正确：打包整个 work 目录（解压后有 work/ 外壳）
zip -r abc451_a_xxx.zip work

# ❌ 错误：进入 work 打包（文件散落根目录）
cd work && zip -r ../xxx.zip .
```

## 验证打包结构

```bash
unzip -l xxx.zip | head -5
# 必须输出：
#   work/
#   work/std.cpp
#   work/problem_zh.md
#   work/mkin.h
#   work/testdata/
```

## 常见错误

### config.yaml 格式（HydroOJ）

推荐使用 subtask 分组格式：

```yaml
# ✅ 正确：顶层 time/memory 作为全局默认（可被子任务覆盖）
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

**注意：**
- 使用 subtask 时必须显式列出所有 `cases`
- `subtasks[].id` 建议从 0 开始编号
- 总分保持 100
- **必须设置顶层 `time` 和 `memory`**（缺省会显示异常值如 65535MB）
- `type` 缺省为 `default`，`time`/`memory` 可在子任务级别覆盖

### 打包结构

```
❌ 错误：文件直接放根目录
problem.zip
├── std.cpp

✅ 正确：有 work 目录
problem.zip
└── work/
    ├── std.cpp
```

### 大样例

| 大小 | 处理 |
|------|------|
| < 500 字节 | `read_file` |
| ≥ 500 字节 | 禁止 `read_file`，用 shell |

## 原创题目

`pid: null` 时：

```bash
zip -r 原创_{title}.zip work
```

## 完成

发送 zip 文件给用户。
