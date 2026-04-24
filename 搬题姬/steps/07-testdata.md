# Step 7: 生成测试数据

## 目标

编写测试数据生成逻辑，生成 25 组测试数据。

## 修改文件

⚠️ 修改 `mkin.h`，不要改 `mkdata.cpp`！

```cpp
void test() {
    // 第1-2组: 样例
    // 第3-5组: 小规模
    // 第6-10组: 中等规模
    // 第11-15组: 大规模
    // 第16-20组: 边界情况
    // 第21-25组: 随机压力
}
```

## 编译运行

```bash
cd work
g++ -o mkdata mkdata.cpp -std=c++17
./mkdata
```

## 配置文件

`work/testdata/config.yaml`:

```yaml
type: default
time: 1s
memory: 128m
```

不需要写 subtasks。

## 大样例处理

| 大小 | 处理 |
|------|------|
| < 500 字节 | `read_file` 读取 |
| ≥ 500 字节 | 禁止 `read_file`，用 shell 验证 |

## 下一步

完成 → `08-package.md`
