# Step 7: 生成测试数据

## 🎯 目标

编写测试数据生成逻辑并生成 25 组测试数据。

---

## 🔧 修改文件

**⚠️ 不要修改 `mkdata.cpp`！修改 `mkin.h`！**

在 `work/mkin.h` 中编写 `test()` 函数：

```cpp
void test() {
    // 第1-2组: 样例（直接使用原题样例）
    // 第3-5组: 小规模
    // 第6-10组: 中等规模
    // 第11-15组: 大规模
    // 第16-20组: 边界情况
    // 第21-25组: 随机压力
}
```

---

## 🔧 编译和运行

```bash
cd work
g++ -o mkdata mkdata.cpp -std=c++17
./mkdata
```

---

## 🔧 配置文件

**文件**：`work/testdata/config.yaml`

```yaml
type: default
time: 1s
memory: 128m
```

**⚠️ 注意**：不需要写 subtasks，系统会自动识别测试点！

---

## 🚨 大样例处理规则

| 文件大小 | 处理方式 |
|---------|---------|
| < 500 字节 | `read_file` 读取 |
| ≥ 500 字节 | **禁止 `read_file`**，用 shell 命令验证 |

**大样例验证**：
```bash
wc -c testdata/1.in        # 检查大小
head -5 testdata/1.in      # 查看前几行
./std < testdata/1.in > testdata/1.out  # 运行标程
```

---

## 📊 判断结果与下一步跳转

### ✅ 测试数据生成完成

**输出**：`testdata/` 目录包含 25 组 .in/.out 文件

**👉 下一步**：读取 `steps/08-package.md` 打包发布