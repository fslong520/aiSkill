# Step 6: 实现标程

## 目标

写标准解题程序 `{WORK_DIR}/std.cpp`。

## 模板

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 解题代码

    return 0;
}
```

## 要点

1. 据题定算法
2. OI 风格：简变量名、全局变量
3. 时复杂度满足时限

## ⚠️ 铁律：写后即验（生数据前）

写完 std.cpp **必即**用题面样例验之，不跳：

```bash
cd {WORK_DIR}
g++ std.cpp -o std -std=c++17

# 逐样例输入验输出，一一对照题面
echo "【样例输入1】" | ./std
# 核出与题面样例输出1一致否

echo "【样例输入2】" | ./std
# 核出与题面样例输出2一致否

# ... 诸样例逐一验
```

**禁**：
- ❌ 写 std 不验样例即写 mkin.h / 生数据
- ❌ 只验一样例即谓全对
- ❌ 样例未过仍续生数据

**必**：
- ✅ 诸题面样例全过方可入下步
- ✅ 样例不过则改 std.cpp，重验，至全过

## 下一步

诸样例过 → `07-testdata.md`
