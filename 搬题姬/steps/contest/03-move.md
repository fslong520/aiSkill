# Contest Step 3: 逐题完整搬运

## 目标

逐题生成完整题包（题面、标程、测试数据、配置）。

## 最高铁律：必须从文件读取题面

⚠️ 每搬运一道题前，必须用 grep + read_file 从题面汇总文件读取该题信息！

**禁止**：
- ❌ 从对话上下文记忆中提取题面
- ❌ 从之前翻译的内容回忆
- ❌ 假装记得题目内容直接写

**必须**：
- ✅ 用 `grep` 在题面文件中定位当前题目
- ✅ 用 `read_file` 读取该题目完整内容
- ✅ 确认读取成功后才开始搬运

## 步骤（对每道题目）

### Step 3-1 读取题面

```bash
grep -n "## A -" abc453.md  # 定位题目
read_file abc453.md         # 读取内容
```

### Step 3-2 环境初始化

工作目录命名：`work_{PID}`
PID 可从题号确定（如 `abc453` 比赛中的 A 题 → `abc453a`）。

```bash
rm -rf work_{PID}
cp -r question work_{PID}
# {WORK_DIR} = work_{PID}
```

### Step 3-3 生成题面

基于读取的信息生成。生成后重命名目录加入标题：

```bash
mv {WORK_DIR} {WORK_DIR}_{标题简写}
# {WORK_DIR} = work_{PID}_{标题简写}
```

写入 `{WORK_DIR}/problem_zh.md`。

### Step 3-4 写入配置

```yaml
pid: abc453a
title: "中文(英文)"
tag:
  - "GESP X级"
```

写入 `{WORK_DIR}/problem.yaml`。

### Step 3-5 实现标程

根据题面编写解法，写入 `{WORK_DIR}/std.cpp`。

### Step 3-6 编写测试数据

修改 `{WORK_DIR}/mkin.h` 的 `test()` 函数。

### Step 3-7 生成测试数据

```bash
cd {WORK_DIR}
g++ -o mkdata mkdata.cpp -std=c++17
./mkdata
```

### Step 3-8 验证标程

编译并验证样例通过。

### Step 3-9 打包发布

⚠️ **打包铁律：必须从 {WORK_DIR} 的父目录打包整个 {WORK_DIR} 目录。**

```bash
# ✅ 正确：打包整个 {WORK_DIR}/ 目录（解压后有 {WORK_DIR}/ 外壳）
rm -f {WORK_DIR}/std {WORK_DIR}/mkdata {WORK_DIR}/*.exe
zip -r {pid}_{title}.zip {WORK_DIR}

# ❌ 错误：cd 进 {WORK_DIR} 再打包（文件会散落在根目录）
# cd {WORK_DIR} && zip -r ../{pid}_{title}.zip .
# ❌ 错误：在 {WORK_DIR} 目录内打包当前目录
# cd {WORK_DIR} && zip -r {pid}_{title}.zip *
```

**验证打包结构：**
```bash
unzip -l {pid}_{title}.zip | head -6
# 期望输出：
#   {WORK_DIR}/
#   {WORK_DIR}/std.cpp
#   {WORK_DIR}/problem_zh.md
#   {WORK_DIR}/testdata/
```

## 完成当前题目后

清空思路，准备下一题！

- ❌ 禁止保留上一题的上下文
- ✅ 每题独立读取题面信息

## 完成

N 个 zip 文件已生成，任务完成！
