// ═══════════════════════════════════════════════════════════
// 析题 · typst 多题题解模板（PDF，学术风）
// 用法：多题合一题解 / 无需动图的单题题解 → 编译 PDF
//   编译：typst compile <本文件> 题解.pdf
// 覆盖：题目一句话 / 怎么想 / 关键点 / 逻辑链 / 复杂度 / 参考代码 / 易错点
// 组图规范：多题不用动画——用多张静态图（snapshots/表格/流程图）表示变化
// ═══════════════════════════════════════════════════════════
#import "theme-academic.typ": *

#show: theme.with(
  title: "ABC000 题解（A–G）",
  subtitle: "AtCoder Beginner Contest 000 · 多题合一",
  author: "析题",
)

// 启用代码块主题
#show: code-init

// ══════════════════════════
// 第 1 题
// ══════════════════════════
#heading[#text(fill: rgb("#111"))[A — 题目标题]]

#problem-statement[
  #heading(level: 3)[题目一句话]
  一行说清题意（给定…，求…）。
]

#heading(level: 2)[怎么想]
// 因果链：发现 → 因为 → 所以 → 代码
第一反应：#emph[暴力…]。因为 #emph[数据范围 $n <= 10^5$]，所以 #emph[不能 $O(n^2)$]。
转折观察：手推样例发现…。所以用 #strong[前缀和]：$O(n)$ 一趟。

#heading(level: 2)[关键点]
#key-point[一句点透：把重复求和变成一趟扫描。]

#heading(level: 2)[组图：状态变化]
// ⚠ 多题不用动画：用静态组图表示变化（snapshots 环境或三线表）
#snapshots((
  [*步骤1* 初始数组 $[5, 2, 3, 8]$，前缀和 $= 0$],
  [*步骤2* 加 $5$ → 前缀 $P_1 = 5$],
  [*步骤3* 加 $2$ → 前缀 $P_2 = 7$],
  [*步骤4* 加 $3$ → 前缀 $P_3 = 10$，$|18-2×10|=2$ 最小 ✓],
))

#heading(level: 2)[复杂度]
时间 $O(n)$，空间 $O(1)$。

#heading(level: 2)[参考代码]
#block(stroke: (left: 2.5pt + rgb("#2b6cb0"), rest: 0.5pt + rgb("#dddddd")), inset: 0.5em)[
```cpp
#include <iostream>
using namespace std;
int main() {
    int n; cin >> n;
    long long x = 0;
    for (int i = 0; i < n; i++) { long long v; cin >> v; x += v; }
    cout << x << endl;
    return 0;
}
```
]

#heading(level: 2)[样例演示]
#booktabs(
  ("输入", "前缀", "输出"),
  (("5 2 3 8", "$P_3=10$", "10 ✓"), ("1 1", "$P_2=2$", "2 ✓")),
)

#heading(level: 2)[易错点]
#warn[
- 前缀和用 `long long`，$n=10^5$ 时 $sum$ 可能超 `int`
- 别把 `#` 格当可操作格（若有网格）
]

// ══════════════════════════
// 第 2 题（重复第 1 题结构）
// ══════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[B — 题目标题]]

#problem-statement[
  #heading(level: 3)[题目一句话]
  题意…
]

#heading(level: 2)[怎么想]
……

// 串讲（多题末尾）
#heading[#text(fill: rgb("#111"))[串讲]]
这七题恰好铺开一条「算法视野」之路——……共同点只有一个：#strong[把新问题翻译成你已会的老工具]。
