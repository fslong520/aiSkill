---
name: OIStyle

description: |
  自动检测文档中的C++代码并将其转换为信息学奥林匹克竞赛风格的代码格式。
  专门针对信息学竞赛需求优化，自动应用OI代码规范：使用简短变量名（不超过5个字符）、
  优先使用全局变量、采用标准竞赛格式（左大括号另起一行）、明确包含必要头文件。
  支持自动添加中文注释和关键步骤说明，确保代码符合竞赛要求。
  适用于将普通C++代码转换为信奥赛风格、代码规范化处理、竞赛代码模板生成等场景。
  保持原有算法逻辑不变，仅调整命名规范和代码格式，提升代码的竞赛适用性。

allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion

metadata:
  trigger: OI风格、信奥赛风格、C++代码转换、竞赛代码、变量命名规范化
---

# 信奥赛代码风格转换器

## Summary

扫描文档中的C++代码块，转换为OI竞赛规范风格：短变量名、全局变量、左大括号另起一行、明确头文件、中文注释。

## Keywords

C++代码转换、信奥赛风格、代码规范化、竞赛代码优化、OI风格、变量命名、头文件

## Strategy

1. **扫描定位**：找到文档中所有标记为 `cpp` 的代码块
2. **分析结构**：识别变量命名、数据结构、头文件、代码格式
3. **转换执行**：
   - 变量名 → 5字符以内短名（参考 reference.md 映射表）
   - vector → 固定数组
   - 万能头 → 具体头文件
   - 左大括号 → 另起一行
4. **添加注释**：在关键步骤添加中文注释
5. **验证确认**：展示转换结果，询问用户是否满意

## AVOID

- AVOID 使用 `bits/stdc++.h` 万能头文件，应替换为具体所需头文件
- AVOID 变量名超过5个字符，应使用 a, b, c, n, m, ans, mx, mn 等短名
- AVOID 左大括号不另起一行，竞赛标准格式要求左大括号独占一行
- AVOID 保留 vector 当可用固定数组替代时，竞赛中优先使用全局数组
- AVOID 改变原有算法逻辑，只调整命名和格式，核心逻辑必须保持不变
- AVOID 缺少关键步骤的中文注释，便于阅读和理解

## 转换规则速查

### 变量命名
| 原名 | 转换后 | 用途 |
|------|--------|------|
| numberOfStudents | n | 数量 |
| result/answer | ans | 结果 |
| max/min | mx/mn | 最值 |
| temp | t | 临时 |

### 数据结构
| 原结构 | 转换后 |
|--------|--------|
| vector<int> arr | int a[1005] |
| vector<vector<int>> | int a[105][105] |

### 头文件映射
```cpp
// 删除
#include <bits/stdc++.h>

// 添加具体头文件
#include <iostream>    // cin/cout
#include <algorithm>   // sort, reverse
#include <vector>      // 如需保留vector
#include <queue>       // 队列
```

## 示例

**转换前：**
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int numberOfStudents;
    vector<int> studentScores;
    cin >> numberOfStudents;
    // ...
}
```

**转换后：**
```cpp
#include <iostream>
#include <algorithm>
using namespace std;

int n, a[1005], ans;

int main()
{
    cin >> n;
    // ...
}
```

## 详细参考

完整转换映射和更多实例见：
- [reference.md](reference.md) - 详细转换规范
- [examples.md](examples.md) - 更多转换实例
