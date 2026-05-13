# Step 11: 仅生测试点

## 目标

用户已供题，**仅需测试数据（.in / .out）**，不要题面文件、不要 problem.yaml、不要打包。

## ⚠️ 核心原则

```
标程 + mkin.h = 测试数据（.in + .out）
缺标程 → .out 不出
缺 mkin.h → .in 不出
两样皆写 → 编译 → 运行 → testdata/ 到手
```

## 流程

### 1. 析题

自用户材取以下信息（**必遍查，缺一不可**），记至 `{WORK_DIR}/problem_zh.md`（仅自参，不作交付）：

| 信息 | 说明 |
|------|------|
| 入格式 | 每行表何、量名及型、空格/换行分隔 |
| 出格式 | 出何、每行几数、精度求 |
| 数据范围 | N/值之上下限、极值 |
| 时/内存限 | 决数据规上限 |
| 算法类 | 决 Hack 数据向 |

若用户所供不足以定上任一，**必问用户补**。

### 2. 写标程 `{WORK_DIR}/std.cpp`

标程乃生 .out 之独法，必保：

- 算法**正**（能过诸 25 组测试数据）
- 用 `std.cpp` 为文件名，置 `{WORK_DIR}/` 目录
- OI 风格：简变量名、全局变量、`ios::sync_with_stdio(false)`
- 时复杂度对标题限（勿写出比正解更慢版）
- 注：Hack 数据乃为**选手码**掘坑，标程必能正跑过诸 Hack

### 3. 设计测试数据

编 `{WORK_DIR}/mkin.h` 之 `test()` 函，覆 25 组。

**分组方案（5 子任，总 100）：**

| Subtask | 用例编号 | 类 | 分值 |
|---------|---------|------|------|
| 0 | 1-2 | 样例 | 10 |
| 1 | 3-8 | 小规模 + 特性 | 20 |
| 2 | 9-11 | Hack 数据 | 15 |
| 3 | 12-20 | 中大规模 | 30 |
| 4 | 21-25 | 随机复测 | 25 |

**⚠️ 改 `test()` 分组时同更三处：**
1. `mkin.h` 顶 `SUBTASKS[]` 数组
2. `{WORK_DIR}/testdata/config.yaml` 中 `subtasks[].cases` 列表
3. 总分持 100

#### 3a. 样例数据（case 1-2）

径复用户供样例入/出。用户未供样例时，自构**最简可验数据**。

```cpp
if (case_num == 1) {
    // 样例1：自用户供题面复，逐字一致
    fout << "5 3" << endl;
    fout << "1 2 3 4 5" << endl;
}
else if (case_num == 2) {
    // 样例2
}
```

#### 3b. 小规模随机（case 3-5）

N 取题范围**最小规模**（如 1~10），验基本功正。

```cpp
else if (case_num >= 3 && case_num <= 5) {
    int N = rand() % 5 + 1;
    int M = rand() % 5 + 1;
    fout << N << " " << M << endl;
    // 据题异生随机数据
}
```

#### 3c. 特性质数据（case 6-8）

针题数据特性设计：

| 性质 | 说明 | 针之错 |
|------|------|-----------|
| 单调性 | 入有序（递增/递减） | 排序/二分实现误 |
| 全同 | 诸值等 | 重复值理遗 |
| 极值集 | 大量极值（如全 0/1） | 特殊支未覆 |
| 素数密 | 大量素数 | 筛法写误 |
| 特定图构 | 链/菊/全图 | 图法边界 |

每特性一用例。

```cpp
else if (case_num == 6) {
    // 特性1：单调递
    int N = 100;
    fout << N << endl;
    for (int i = 1; i <= N; i++) fout << i << " \n"[i==N];
}
else if (case_num == 7) {
    // 特性2：诸值同
    int N = 1000;
    fout << N << endl;
    for (int i = 1; i <= N; i++) fout << 5 << " \n"[i==N];
}
else if (case_num == 8) {
    // 特性3：据题自定义
}
```

#### 3d. Hack 数据（case 9-11）

针常见错法精准下毒：

| 常见错 | Hack 数据征 |
|---------|--------------|
| int 溢出 | 用近 `2^31-1` 或 `2^63-1` 大数 |
| 边界漏判 | N=1, N=max, a[i]=0 等极边 |
| 精度误 | 需 `double` 非 `float` 小数，或浮点比较 |
| 超时炸 | 迫错复杂度（O(n²)）超时 |
| 错贪心 | 构使贪心策得非优解数据 |
| 模数阱 | 负取模、未取模致溢 |

```cpp
else if (case_num == 9) {
    // Hack 1: int 溢出（两近 2^31-1 大数相加）
    fout << 2 << endl;
    fout << "2147483647 2147483647" << endl;
}
else if (case_num == 10) {
    // Hack 2: 最小边界
    fout << 1 << endl;
    fout << 0 << endl;
}
else if (case_num == 11) {
    // Hack 3: 最大边界 / 使错法超时
    int N = 200000;
    fout << N << endl;
    for (int i = N; i >= 1; i--) fout << i << " \n"[i==1];
}
```

#### 3e. 中大规数据（case 12-20）

| 用例 | 规模 | 的 |
|------|------|------|
| 12-15 | N = 100 ~ 10000 | 中规，验效 |
| 16-18 | N 近上限 80% | 大压测 |
| 19-20 | N = 上限值 | 极压测 |

```cpp
else if (case_num >= 12 && case_num <= 15) {
    int N = rand() % 1000 + 100;
    // 随机数据
}
else if (case_num >= 16 && case_num <= 20) {
    int N = 200000;  // 或题上限
    // 近极数据
}
```

#### 3f. 随机复测（case 21-25）

诸类数混搭，覆不复景：

```cpp
else {
    int N = rand() % 100000 + 1;
    // 自由随机
}
```

### 4. 配 {WORK_DIR}/testdata/config.yaml

写入 HydroOJ 格 subtask 配。**用例表必与 mkin.h 之 SUBTASKS[] 一一应。**

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
      # ... 至 8

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
      # ... 至 20

  - score: 25
    id: 4
    cases:
      - input: 21.in
        output: 21.out
      # ... 至 25
```

**时/内存限**自用户供题信息取。若用户未供，主动问。

### 5. 编译运行

```bash
cd {WORK_DIR}
g++ std.cpp -o std -std=c++17    # 编译标程（为 mkdata 所调）
g++ mkdata.cpp -o mkdata -std=c++17
./mkdata
```

预期出：
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

必验下诸项：

- [ ] {WORK_DIR}/testdata/ 目录下 25 .in 与 25 .out 成对存
- [ ] 前 2 组数与样例题完全一致（用 `diff` 或 `read_file` 较）
- [ ] 每组 .in 格合同题入格式述
- [ ] {WORK_DIR}/testdata/config.yaml 之 subtask cases 表与实生文件一致
- [ ] `lsp_diagnostics` 查 mkin.h 无误

### 7. 打包

将测数与标程打为 zip，置 testdata 目录：

```bash
cd {WORK_DIR}
zip testdata/testdata.zip testdata/*.in testdata/*.out testdata/config.yaml std.cpp
```

生文件：`{WORK_DIR}/testdata/testdata.zip`（含 .in/.out/config.yaml/std.cpp）

### 8. 交付

告用户测数已生：
- `{WORK_DIR}/testdata/` 目录：25 组 `.in` + 25 组 `.out` + `config.yaml`
- `{WORK_DIR}/testdata/testdata.zip`：前诸文件打

## 与常流之别

| 项 | 常搬题 | 仅生测试点 |
|------|---------|-------------|
| 题面 problem_zh.md | 生 | **跳**（或仅内参） |
| problem.yaml | 写 | **跳** |
| std.cpp | 写 | **写**（生 .out 必需） |
| mkin.h | 编 | **编** |
| mkdata + 运 | 行 | **行** |
| 打包 zip | 打全 {WORK_DIR}/ | **只打 testdata/ 为 testdata.zip** |
| {WORK_DIR}/testdata/config.yaml | 写 | **写** |
