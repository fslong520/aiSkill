# 笔记手账 - OI代码风格规范（oi-code-style.md）

> 本文件为 SKILL.md 之附属，定义含代码知识卡的 C++ 代码格式规范。当知识卡包含 C++ 代码时，必须按以下 OI 竞赛风格格式化。适用于所有风格主题。

## 1. 代码格式规范

| 规范           | 要求                                    | 示例                                  |
| :------------- | :-------------------------------------- | :------------------------------------ |
| **头文件**     | 使用具体头文件，禁用 `bits/stdc++.h`    | `#include <iostream>`                 |
| **命名空间**   | 写 `using namespace std;`               |                                       |
| **变量作用域** | **全局变量**优先（竞赛标配）            | `int n, a[105], sum;`                 |
| **变量命名**   | 5字符以内短名                           | `n, m, x, sum, mx, mn, ans, pos, cnt` |
| **数据结构**   | 固定数组替代 vector                     | `a[105]` 而非 `vector<int>`           |
| **左大括号**   | **另起一行**（竞赛标准）                | `for(...)\n{` 而非 `for(...){`        |
| **缩进**       | 4空格                                   |                                       |
| **主函数**     | 完整 `int main()` + `return 0;`         |                                       |
| **输入输出**   | `cin`/`cout`，必要时用 `scanf`/`printf` |                                       |
| **代码注释**   | 关键步骤加中文注释                      | `// ✨ 累加求和`                       |

## 2. OI风格代码模板

```
#include <iostream>
using namespace std;

int n, a[105], ans;

int main()
{
    // ✨ 输入
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    
    // ✨ 核心逻辑
    for (int i = 1; i <= n; i++)
    {
        // 处理
    }
    
    // ✨ 输出
    cout << ans;
    return 0;
}
```

## 3. 代码在Prompt中的描述

生成含代码的知识卡Prompt时，按以下方式描述：

```
Card "💻 代码" with computer icon, [风格对应配色] header. Code in SMALL FONT (OI style):
「#include <iostream>
 using namespace std;

 int n, a[105], ans;

 int main()
 {
     cin >> n;
     for (int i = 1; i <= n; i++)
     {
         // ✨ 核心代码
     }
     cout << ans;
     return 0;
 }」
```

## 4. 高频易错点提示

OI风格常见错误，在知识卡底部"高频易错点"中提醒：
- 全局变量自动初始化为0，局部变量不会
- `return 0;` 用于提前结束程序（查找场景）
- 数组下标从1开始还是从0开始需明确

---

**文档版本**: 3.2
**最后更新**: 2026-08-02
