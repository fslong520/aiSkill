# Step 6: 实现标程

## 目标

写标准解题程序 `{WORK_DIR}/std.cpp`。

## 模板

```cpp
#include <iostream>
#include <algorithm>
#include <cstring>
using namespace std;

// 全局数组——大小按题面数据范围来定
// const int MAXN = 105;
// int dp[MAXN], w[MAXN], v[MAXN], val[MAXN];

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 读数据 + 算答案

    cout << ans << '\n';
    return 0;
}
```

## 要点

1. 据题定算法
2. OI 风格：**左大括号单独起一行**，**全局变量**，简变量名（如 `w`, `v`, `dp`, `n`, `m`）
3. `#include <bits/stdc++.h>` 尽量少用，优先逐一声明所需头文件
4. **STL 容器（vector / map / set 等）尽量少用**——优先用全局数组（`int dp[105][105]` 而非 `vector<vector<int>>`），确有必要时可用
5. ⚠️ **禁 `memcpy` / `memset`**——数组拷贝用 `vector` 赋值（`auto prev = dp`），初始化用 `fill`
5. ⚠️ **禁动态内存分配**——`new`/`malloc`/`vector.resize()` 均不可
6. 时复杂度满足时限

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
