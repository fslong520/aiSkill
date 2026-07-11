# Step 7: 生测试数据

## 目标

**生 25 组测试数据（.in + .out）+ config.yaml + 测试点分布表。**

## 模式选择

| 模式 | 触发场景 | 前置条件 | 后续 |
|------|---------|---------|------|
| **全流程** | 完整搬题（题面+标程+数据） | `problem_zh.md` 已存在（来自 Step 4） | → `08-audit.md` |
| **仅测点** | 用户已有题面，只需测试数据 | 需自用户材料析取题面信息（入/出格式、数据范围、时限） | → 直接交付 |

两模式走同一流程，区别仅在第 4 步（打包方式）和末步（审计/交付）。

## ⚠️ 核心原则

```
生测试点 = 编 {WORK_DIR}/mkin.h 中 test() 函数
勿碰 {WORK_DIR}/mkdata.cpp（乃框架，毋须改）
标程 + mkin.h = 测试数据（.in + .out）
缺标程 → .out 不出
```

---

### 流程

#### 1. 析题（仅测点模式必做；全流程模式跳到第 2 步）

自用户材料取以下信息，记至 `{WORK_DIR}/problem_zh.md`（仅测点模式下仅内参，不作交付）：

| 信息 | 说明 |
|------|------|
| 输入格式 | 每行表示什么、变量名及类型、空格/换行分隔 |
| 输出格式 | 输出什么、每行几个数、精度要求 |
| 数据范围 | N/值的上下限、极值 |
| 时间/内存限制 | 决定数据规模上限 |
| 算法类型 | 决定 Hack 数据方向 |

若用户所供不足以定以上任一项，**必问用户补充**。

#### 2. 写标程 `{WORK_DIR}/std.cpp`

标程是生成 .out 的唯一方法，必须确保：

- 算法**正确**（能通过所有 25 组测试数据）
- 文件名为 `std.cpp`，置于 `{WORK_DIR}/` 目录
- OI 风格：简短变量名、全局变量、`ios::sync_with_stdio(false)`
- 时间复杂度对标题目限制（勿写出比正解更慢的版本）
- Hack 数据是为**选手代码**挖坑，标程必须能正确跑过所有 Hack

#### 3. 设计测试数据：编 `{WORK_DIR}/mkin.h` 之 `test()` 函数

生 25 组，分布方案详见 **`references/testdata-design.md` → 一、数据分布框架**。

边界清单与 Hack 设计详见 **`references/testdata-design.md`**：

| 章节 | 内容 |
|------|------|
| 二、题型感知边界清单 | 按数组/图论/树/字符串/DP/数学分类的边界列表 |
| 三、Hack 数据设计 | 各类常见错误的 Hack 数据模式 |
| 四、各规模数据生成建议 | case 3-20 的规模与构造建议 |

**设计步骤：**
1. 辨题目类型（数组/图论/树/字符串/DP/数学/构造）
2. 自 `references/testdata-design.md` 对应章节挑拣边界
3. 将边界写入 `mkin.h` 的 `test()` 函数

##### test() 模板

```cpp
void test(int case_num, ofstream& fout) {
    // ============================================================
    // Subtask 0: 样例数据（直接复制题目样例）— case 1-2
    // ============================================================
    if (case_num == 1) {
        // 样例1 - 从题面逐字复制
    }
    else if (case_num == 2) {
        // 样例2 - 从题面逐字复制
    }

    // ============================================================
    // Subtask 1: 小规模随机数据 — case 3-5
    // ============================================================
    else if (case_num >= 3 && case_num <= 5) {
        // N 取题目范围最小规模（如 1~10），验基本功能
    }

    // ============================================================
    // Subtask 1(续): 特殊性质数据 — case 6-8
    // ============================================================
    else if (case_num == 6) {
        // 据 references/testdata-design.md 选性质1
    }
    else if (case_num == 7) {
        // 据 references/testdata-design.md 选性质2
    }
    else if (case_num == 8) {
        // 据 references/testdata-design.md 选性质3
    }

    // ============================================================
    // Subtask 2: Hack 数据（针对常见错误写法）— case 9-11
    // ============================================================
    else if (case_num == 9) {
        // 见 references/testdata-design.md → 三、Hack 数据设计
    }
    else if (case_num == 10) {
        // 见 references/testdata-design.md → 三、Hack 数据设计
    }
    else if (case_num == 11) {
        // 见 references/testdata-design.md → 三、Hack 数据设计
    }

    // ============================================================
    // Subtask 3: 中等规模数据 — case 12-15
    // ============================================================
    else if (case_num >= 12 && case_num <= 15) {
        // N 在 [100, 10000] 范围内
    }

    // ============================================================
    // Subtask 3(续): 大规模数据（压力测试）— case 16-20
    // ============================================================
    else if (case_num >= 16 && case_num <= 20) {
        // N 接近题目限制上限
    }

    // ============================================================
    // Subtask 4: 随机回归测试 — case 21-25
    // ============================================================
    else {
        // 随机生成，覆盖各种情况
    }
}
```

#### 3b. 改 test() 后必同更

1. `mkin.h` 顶 `SUBTASKS[]` 数组（仅作注释标记用）
2. `{WORK_DIR}/testdata/config.yaml` 格式见 **`references/testdata-design.md` → 五、config.yaml 格式**
3. 25 组测点总分保持 100

#### 4. 配 `{WORK_DIR}/testdata/config.yaml`

格式见 **`references/testdata-design.md` → 五、config.yaml 格式**。

- **全流程模式**：时间/内存限制沿用 Step 5 写入的值
- **仅测点模式**：时间/内存限制从用户供题信息取；用户未供则主动问

#### 5. ⚠️ 追加测试点分布表

写完 config.yaml 后，**必**于 `{WORK_DIR}/problem_zh.md` 的 `</div>` 前追加测试点分布表。

格式、各列规则、说明列规范、约束详见 **`references/testdata-design.md` → 六、测试点分布表格式**。

**此步不可跳过，否则题包不全。**

> 模板 `question/problem_zh.md` 中已有占位表，记得按实际 subtask 分组更新说明列。

#### 6. 编译运行

```bash
cd {WORK_DIR}
g++ std.cpp -o std -std=c++17    # 编译标程（为 mkdata 所调用）
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

#### 7. 验证

必须验证以下各项：

- [ ] `{WORK_DIR}/testdata/` 目录下 25 个 `.in` 与 25 个 `.out` 成对存在
- [ ] 前 2 组数据与题目样例完全一致（用 `diff` 或逐行比较）
- [ ] 每组 `.in` 格式符合题目输入格式描述
- [ ] `{WORK_DIR}/testdata/config.yaml` 的 subtask cases 列表与实际生成的文件一致
- [ ] `{WORK_DIR}/problem_zh.md` 末尾含测试点分布表
- [ ] `lsp_diagnostics` 检查 mkin.h 无误

## 打包

### 全流程模式

```bash
# 打包整个工作目录（含题面、标程、配置、测试数据）
rm -f {WORK_DIR}/std {WORK_DIR}/mkdata {WORK_DIR}/*.exe
zip -r {pid}_{title}.zip {WORK_DIR}
```

### 仅测点模式

```bash
# 只打包测试数据，不包含源码
cd {WORK_DIR}/testdata
zip testdata.zip *.in *.out config.yaml
```

⚠️ **关键**：
- `.in`、`.out`、`config.yaml` 须在 zip **根目录**，不可有子目录前缀
- **不**打包 `std.cpp`、`mkin.h`、`mkdata.cpp` 等源码文件
- HydroOJ 只认根目录下的 `1.in` / `1.out` / … / `config.yaml`

生成文件：`{WORK_DIR}/testdata/testdata.zip`

## 大样例处理

| 大小 | 处理 |
|------|------|
| < 500 字节 | `read_file` 读取 |
| ≥ 500 字节 | 禁止 `read_file`，用 shell 验证 |

## 下一步

| 模式 | 下一步 |
|------|--------|
| **全流程** | → `08-audit.md` |
| **仅测点** | → 交付用户（告知 `testdata/testdata.zip` 已生成） |
