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
# ✅ 正确：打包整个 work 目录
zip -r abc451_a_xxx.zip work

# ❌ 错误：进入 work 打包
cd work && zip -r ../xxx.zip .
```

## 常见错误

### config.yaml 格式

```yaml
# ✅ 正确
type: default
time: 1s
memory: 128MB

# ❌ 错误：缺少顶层配置
subtasks:
  - score: 100
```

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
