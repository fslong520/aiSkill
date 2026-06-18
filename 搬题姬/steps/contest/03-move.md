# Contest Step 3: 逐题全搬

## 目标

逐题生完整题包（题面、标程、测数、配）。

## 最高铁律：必自文件读题面

⚠️ 每搬一题前，必以 grep + read_file 自题面汇总文件读该题信息！

**禁**：
- ❌ 自对话上下文记取题面
- ❌ 自前译内容忆
- ❌ 伪记题内容径写

**必**：
- ✅ 用 `grep` 于题面文件中定位当前题
- ✅ 用 `read_file` 读该题全内
- ✅ 确读成后方始搬

## 步骤（对每题）

### Step 3-1 读题面

```bash
grep -n "## A -" abc453.md  # 定位题
read_file abc453.md         # 读内容
```

### Step 3-2 环境初始化

工作目录名：`work_{PID}`
PID 可自题明确（如 `abc453` 赛中 A 题 → `abc453a`）。

```bash
rm -rf work_{PID}
cp -r question work_{PID}
# {WORK_DIR} = work_{PID}
```

### Step 3-3 生题面

据读得信息生。生后更名目录加标题：

```bash
mv {WORK_DIR} {WORK_DIR}_{标题简写}
# {WORK_DIR} = work_{PID}_{标题简写}
```

写入 `{WORK_DIR}/problem_zh.md`。

### Step 3-4 写配

```yaml
pid: abc453a
title: "中(英)"
score:  # AI 按 03-gesp.md「第六步：定分」规则估算，已知比赛分数直接采用
tag:
  - "知识点标签1"
  - "知识点标签2"
  - "GESP X级"
```

⚠️ **tag 含 1~3 个知识点标签 + 1 个等级标签，禁只写 GESP 等级**
⚠️ **score 按 03-gesp.md「第六步：定分」规则估算，已知比赛分数直接采用，禁写死默认值**

写入 `{WORK_DIR}/problem.yaml`。

### Step 3-5 实现标程

据题面编解法，写入 `{WORK_DIR}/std.cpp`。

### ⚠️ Step 3-6 验标程（铁律：生数前必行）

写完 std.cpp **必即**用全样例验，不跳：

```bash
cd {WORK_DIR}
g++ std.cpp -o std -std=c++17

# 逐样例入验出，一一对照题面
echo "【样例输入1】" | ./std
# 核出与题面否

echo "【样例输入2】" | ./std
# 核出与题面否
# ... 诸样例逐一验
```

**禁**：样例未全过便写 mkin.h / 生数
**必**：诸样例全过，方入下步

### Step 3-7 编测试数据

改 `{WORK_DIR}/mkin.h` 之 `test()` 函。

### Step 3-8 生测试数据

```bash
cd {WORK_DIR}
g++ -o mkdata mkdata.cpp -std=c++17
./mkdata
```

### Step 3-9 打包发布

⚠️ **打包铁律：必自 {WORK_DIR} 之父目录打包全 {WORK_DIR} 目录。**

```bash
# ✅ 正：打包全 {WORK_DIR}/ 目录（解压后有 {WORK_DIR}/ 壳）
rm -f {WORK_DIR}/std {WORK_DIR}/mkdata {WORK_DIR}/*.exe
zip -r {pid}_{title}.zip {WORK_DIR}

# ❌ 误：cd 进 {WORK_DIR} 再打包（文件散根目录）
# cd {WORK_DIR} && zip -r ../{pid}_{title}.zip .
# ❌ 误：于 {WORK_DIR} 目录内打包当前目录
# cd {WORK_DIR} && zip -r {pid}_{title}.zip *
```

**验打包构：**
```bash
unzip -l {pid}_{title}.zip | head -6
# 望出：
#   {WORK_DIR}/
#   {WORK_DIR}/std.cpp
#   {WORK_DIR}/problem_zh.md
#   {WORK_DIR}/testdata/
```

## 成后

清思，备下题！

- ❌ 禁留上题上下文
- ✅ 每题独读题面信息

## 完成

N 个 zip 文件已生，务成！
