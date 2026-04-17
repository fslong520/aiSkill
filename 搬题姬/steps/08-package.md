# Step 8: 打包发布

## 🎯 目标

打包题目文件为 zip 包并发送给用户。

---

## 🚨 打包前检查清单

### ✅ 必须检查

1. **清理临时文件**：
   ```bash
   rm -f work/std work/mkdata work/*.exe
   ```

2. **验证打包结构**：
   - ✅ 正确：打包整个 `work` 目录
   - ❌ 错误：进入 work 打包内容

3. **确认 config.yaml 格式**：
   ```yaml
   type: default       # 顶层必须有
   time: 1s            # 顶层时间限制
   memory: 128MB       # 顶层内存限制
   ```

---

## 🔧 打包命令

**文件名格式**：`{pid}_{title}.zip`

```bash
# ✅ 正确做法：打包整个 work 目录
zip -r abc451_a_xxx.zip work

# ❌ 错误做法：进入 work 打包内容
cd work && zip -r ../xxx.zip .   # 解压后无 work 目录！
```

---

## 🚨 常见错误（血泪教训）

### 错误1：config.yaml 格式错误

```yaml
# ❌ 错误！缺少顶层配置
subtasks:
  - score: 100
    testcases:       # ❌ 应该是 cases！
      - input: 1.in
        output: 1.out

# ✅ 正确！
type: default
time: 1s
memory: 128MB
```

**关键点**：
- 顶层必须有 `type`、`time`、`memory`
- 测试点列表是 `cases` 不是 `testcases`

### 错误2：打包结构错误

```
❌ 错误结构：
problem.zip
├── std.cpp          # 文件直接放根目录
├── problem_zh.md

✅ 正确结构：
problem.zip
└── work/            # 有 work 目录
    ├── std.cpp
    ├── problem_zh.md
```

### 错误3：大样例炸掉上下文

| 文件大小 | 处理方式 |
|---------|---------|
| < 500 字节 | `read_file` 读取 |
| ≥ 500 字节 | **禁止 read_file**，用 shell 命令 |

**大样例验证**：
```bash
wc -c testdata/1.in        # 检查大小
head -5 testdata/1.in      # 查看前几行
./std < testdata/1.in > testdata/1.out  # 运行标程
```

---

## 🔧 原创题目命名

如果 `pid: null`（无题号）：
```bash
zip -r 原创_{title}.zip work
```

---

## 📊 下一步跳转

### ✅ 打包完成

**输出**：zip 文件已生成

**👉 下一步**：发送文件给用户，任务完成！