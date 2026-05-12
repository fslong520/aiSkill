# Step 11: 仅生成测试点

## 目标

用户已提供题目，**只需要测试数据（.in / .out）**，不要题面文件、不要 problem.yaml、不要打包。

## ⚠️ 核心原则

```
标程 + mkin.h = 测试数据（.in + .out）
缺标程 → .out 出不来
缺 mkin.h → .in 出不来
两样都写 → 编译 → 运行 → testdata/ 到手
```

## 流程

### 1. 分析题目

从用户提供的材料中提取以下信息（**必须找全，缺一不可**），记录到 `{WORK_DIR}/problem_zh.md`（仅自己参考，不作为交付物）：

| 信息 | 说明 |
|------|------|
| 输入格式 | 每行代表什么、变量名及类型、空格/换行分隔 |
| 输出格式 | 输出什么、每行几个数、精度要求 |
| 数据范围 | N/值的上下限、极限值 |
| 时间/内存限制 | 决定数据规模上限 |
| 算法类型 | 决定 Hack 数据方向 |

如果用户提供的信息不足以确定以上任一项，**必须询问用户补充**。

### 2. 编写标程 `{WORK_DIR}/std.cpp`

标程是生成 .out 的唯一手段，必须保证：

- 算法**正确**（能通过所有 25 组测试数据）
- 用 `std.cpp` 作为文件名，放在 `{WORK_DIR}/` 目录
- OI 风格：简短变量名、全局变量、`ios::sync_with_stdio(false)`
- 时间复杂度对标题目限制（不要写出比正解更慢的版本）
- 注意：Hack 数据是给**选手代码**挖坑的，标程必须能正确跑过所有 Hack 数据

### 3. 设计测试数据

编辑 `{WORK_DIR}/mkin.h` 的 `test()` 函数，覆盖 25 组测试数据。

**分组方案（5 个子任务，总分 100）：**

| Subtask | 用例编号 | 类型 | 分值 |
|---------|---------|------|------|
| 0 | 1-2 | 样例数据 | 10 |
| 1 | 3-8 | 小规模 + 特殊性质 | 20 |
| 2 | 9-11 | Hack 数据 | 15 |
| 3 | 12-20 | 中大规模 | 30 |
| 4 | 21-25 | 随机回归 | 25 |

**⚠️ 修改 `test()` 分组时同步更新三处：**
1. `mkin.h` 顶部的 `SUBTASKS[]` 数组
2. `{WORK_DIR}/testdata/config.yaml` 中的 `subtasks[].cases` 列表
3. 总分保持 100

#### 3a. 样例数据（case 1-2）

直接复制用户提供的样例输入/输出。用户没给样例时，自行构造**最简可验证数据**。

```cpp
if (case_num == 1) {
    // 样例1：从用户提供的题面复制，逐字符一致
    fout << "5 3" << endl;
    fout << "1 2 3 4 5" << endl;
}
else if (case_num == 2) {
    // 样例2
}
```

#### 3b. 小规模随机数据（case 3-5）

N 取题目范围的**最小规模**（如 1~10），验证基本功能正确。

```cpp
else if (case_num >= 3 && case_num <= 5) {
    int N = rand() % 5 + 1;
    int M = rand() % 5 + 1;
    fout << N << " " << M << endl;
    // 根据题目差异生成随机数据
}
```

#### 3c. 特殊性质数据（case 6-8）

针对题目的数据特性设计：

| 性质 | 说明 | 针对的错误 |
|------|------|-----------|
| 单调性 | 输入有序（递增/递减） | 排序/二分实现错误 |
| 全相同 | 所有值相等 | 重复值处理遗漏 |
| 极值集中 | 大量极值（如全是 0/1） | 特殊分支没覆盖 |
| 素数密集 | 大量素数 | 筛法写错 |
| 特定图结构 | 链/菊花/完全图 | 图算法边界 |

每个特殊性质一道用例。

```cpp
else if (case_num == 6) {
    // 特殊性质1：单调递增
    int N = 100;
    fout << N << endl;
    for (int i = 1; i <= N; i++) fout << i << " \n"[i==N];
}
else if (case_num == 7) {
    // 特殊性质2：所有值相同
    int N = 1000;
    fout << N << endl;
    for (int i = 1; i <= N; i++) fout << 5 << " \n"[i==N];
}
else if (case_num == 8) {
    // 特殊性质3：根据题目自定义
}
```

#### 3d. Hack 数据（case 9-11）

针对常见错误写法精准下毒：

| 常见错误 | Hack 数据特征 |
|---------|--------------|
| int 溢出 | 使用接近 `2^31-1` 或 `2^63-1` 的大数 |
| 边界漏判 | N=1, N=max, a[i]=0 等极端边界 |
| 精度错误 | 需要 `double` 而非 `float` 的小数，或浮点比较 |
| 超时炸弹 | 迫使错误复杂度（O(n²)）超时 |
| 错误贪心 | 构造使贪心策略得到非最优解的数据 |
| 模数陷阱 | 负数取模、未取模导致溢出 |

```cpp
else if (case_num == 9) {
    // Hack 1: int 溢出（两个接近 2^31-1 的大数相加）
    fout << 2 << endl;
    fout << "2147483647 2147483647" << endl;
}
else if (case_num == 10) {
    // Hack 2: 最小边界
    fout << 1 << endl;
    fout << 0 << endl;
}
else if (case_num == 11) {
    // Hack 3: 最大边界 / 让错误算法超时
    int N = 200000;
    fout << N << endl;
    for (int i = N; i >= 1; i--) fout << i << " \n"[i==1];
}
```

#### 3e. 中大规模数据（case 12-20）

| 用例 | 规模 | 目的 |
|------|------|------|
| 12-15 | N = 100 ~ 10000 | 中等规模，验证效率 |
| 16-18 | N 接近上限的 80% | 大压力测试 |
| 19-20 | N = 上限值 | 极限压力测试 |

```cpp
else if (case_num >= 12 && case_num <= 15) {
    int N = rand() % 1000 + 100;
    // 随机数据
}
else if (case_num >= 16 && case_num <= 20) {
    int N = 200000;  // 或题目上限
    // 接近极限的数据
}
```

#### 3f. 随机回归测试（case 21-25）

各类数据混搭，覆盖不重复的场景：

```cpp
else {
    int N = rand() % 100000 + 1;
    // 自由随机
}
```

### 4. 配置 {WORK_DIR}/testdata/config.yaml

写入 HydroOJ 格式的 subtask 配置。**用例列表必须与 mkin.h 的 SUBTASKS[] 一一对应。**

```yaml
type: default
time: 1s
memory: 512m

subtasks:
  - score: 10
    id: 0
    cases:
      - input: 1.in
        output: 1.out
      - input: 2.in
        output: 2.out

  - score: 20
    id: 1
    cases:
      - input: 3.in
        output: 3.out
      # ... 直到 8

  - score: 15
    id: 2
    cases:
      - input: 9.in
        output: 9.out
      - input: 10.in
        output: 10.out
      - input: 11.in
        output: 11.out

  - score: 30
    id: 3
    cases:
      - input: 12.in
        output: 12.out
      # ... 直到 20

  - score: 25
    id: 4
    cases:
      - input: 21.in
        output: 21.out
      # ... 直到 25
```

**时间/内存限制**从用户提供的题目信息中提取。如果用户没给，主动询问。

### 5. 编译运行

```bash
cd {WORK_DIR}
g++ std.cpp -o std -std=c++17    # 编译标程（被 mkdata 调用）
g++ mkdata.cpp -o mkdata -std=c++17
./mkdata
```

预期输出：
```
编译标准程序成功
开始生成输入数据...
生成【01.in】数据成功
...
输入数据生成完成
开始生成输出数据...
处理测试用例 【01】... 完成
...
输出数据生成完成
```

### 6. 验证

必须验证以下全部项：

- [ ] {WORK_DIR}/testdata/ 目录下 25 个 .in 和 25 个 .out 成对存在
- [ ] 前 2 组数据与题目样例完全一致（用 `diff` 或 `read_file` 对比）
- [ ] 每组 .in 格式符合题目的输入格式描述
- [ ] {WORK_DIR}/testdata/config.yaml 的 subtask cases 列表与实际生成的文件一致
- [ ] `lsp_diagnostics` 检查 mkin.h 无误

### 7. 打包

将测试数据和标程打包成 zip，放在 testdata 目录下：

```bash
cd {WORK_DIR}
zip testdata/testdata.zip testdata/*.in testdata/*.out testdata/config.yaml std.cpp
```

生成的文件：`{WORK_DIR}/testdata/testdata.zip`（含 .in/.out/config.yaml/std.cpp）

### 8. 交付

告诉用户测试数据已生成：
- `{WORK_DIR}/testdata/` 目录：25 组 `.in` + 25 组 `.out` + `config.yaml`
- `{WORK_DIR}/testdata/testdata.zip`：上述文件的打包

## 与正常流程的区别

| 项目 | 正常搬题 | 仅生成测试点 |
|------|---------|-------------|
| 题面 problem_zh.md | 生成 | **跳过**（或仅内部参考） |
| problem.yaml | 写入 | **跳过** |
| std.cpp | 编写 | **编写**（生成 .out 必需） |
| mkin.h | 编辑 | **编辑** |
| mkdata + 运行 | 执行 | **执行** |
| 打包 zip | 打包整个 {WORK_DIR}/ | **只打包 testdata/ 为 testdata.zip** |
| {WORK_DIR}/testdata/config.yaml | 写入 | **写入** |
