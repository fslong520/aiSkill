# Step 6: 实现标程

## 目标

写标准解题程序 `{WORK_DIR}/std.cpp`。

## 模板

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <set>
#include <queue>
#include <stack>
#include <list>
#include <tuple>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <tuple>
#define endl '\n'
#define int long long
#define pii pair<int, int>
using namespace std;
const int inf = 0x3f3f3f3f3f3f3f3f;
const int mod = 998244353;
const int mxn = 3e6 + 5;

int n,a[114514];
int c=0;
signed main()
{
    cin>>n;
    for(int i=0;i<n;++i) cin>>a[i];
    for(int i=0;i<n-2;++i)
    {
        c+=(a[i]<a[i+1] and a[i+1]>a[i+2]);
    }
    cout<<c<<endl;
    return 0;
}

```

## 要点

1. 据题定算法
2. OI 风格：**左大括号单独起一行**，**全局变量**，简变量名（如 `w`, `v`, `dp`, `n`, `m`）
3. `#include <bits/stdc++.h>` 尽量少用，优先逐一声明所需头文件
4. **STL 容器（vector / map / set 等）尽量少用**——优先用全局数组（`int dp[105][105]` 而非 `vector<vector<int>>`），确有必要时可用
5. ⚠️ **禁 `memcpy` / `memset`**——数组拷贝用 `vector` 赋值（`auto prev = dp`），初始化用 `fill`
6. ⚠️ **禁动态内存分配**——`new`/`malloc`/`vector.resize()` 均不可
7. ⚠️ **字符串用 `std::string`，禁用 `char[]`**——读入用 `cin >> s` 或 `getline`，输出用 `s.c_str()`（如需）
   - ❌ `char s[105]; scanf("%s", s);`
   - ✅ `string s; cin >> s;`
8. ⚠️ **不引入 `<cstring>` / `<string.h>`**——禁 `char[]`、`memcpy`、`memset`。初始化用 `fill`，拷贝用赋值
9. ⚠️ **禁止使用 C 语言的输入输出**——`scanf`/`printf` 均不可，必须用 `cin`/`cout`（或 `getline`）。头文件用 `<iostream>` 而非 `<stdio.h>`。
   - ❌ `scanf("%d", &n); printf("%d\n", ans);`
   - ✅ `cin >> n; cout << ans << endl;`
10. **除数组外，尽量用 C++ 写法**——结构体、算法、字符串处理等优先用 C++ 标准库（`std::sort`、`std::string`、`std::vector` 等），避免 C 风格（`qsort`、`char[]`、`strcpy` 等）。
11. 时复杂度满足时限

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
