## 优秀prompt示例
```md
创建一张16:9横版科普图，主题是"C++判断素数 - 寻找数学中的特殊数字"，面向14岁学生。

整体布局分为五个区域：

1. **标题区（顶部）**：主标题使用大号蓝色字体，副标题橙色

2. **素数概念区（左上）**：
   - 白板上写着素数定义："只能被1和自身整除的大于1的自然数"
   - 可爱的机器人助教指着黑板
   - 素数举例：2,3,5,7,11,13...
   - 反例：4=2×2, 6=2×3, 9=3×3

3. **判断逻辑流程图（中部）**：
   ① 输入数字n → ② 如果n<2? → ③ 从2到√n循环检查 → ④ 如果n能被整除? → ⑤ 都不能整除，是素数

4. **C++代码示例区（右侧）**：
   完整的isPrime函数代码，带中文注释

5. **可视化示例区（底部）**：
   展示判断17是否为素数的过程：17÷2=8余1, 17÷3=5余2, 17÷4=4余1 → 是素数！

整体风格：卡通机器人角色、明亮配色、流程图用圆角矩形、适合14岁学生
```


```md
创建一张16:9横版科普图，主题是"C++ 埃拉托斯特尼筛法（埃氏筛）- 批量寻找素数"，面向14岁学生。

整体布局分为五个区域：

1. **标题区（顶部）**：
   - 主标题："C++埃拉托斯特尼筛法"，使用大号蓝色字体
   - 副标题："批量寻找素数的高效方法"，使用橙色字体
   - 可爱的机器人助教站在标题旁边

2. **原理讲解区（左上）**：
   - 一个白板/黑板，上面写着：
     "筛法原理：像筛子一样筛掉合数"
     "步骤：从2开始，标记每个素数的所有倍数为合数"
   - 机器人在旁边指着黑板
   - 画一个筛子图标，有数字掉下来

3. **算法流程图（中上）**：
   ① 创建数组2到n，全标记为素数
   ② i=2开始
   ③ 如果i是素数？→ Yes：标记i²,i²+i,i²+2i...为合数
   ④ i++，如果i≤√n？→ Yes返回③，No进入⑤
   ⑤ 未被标记的就是素数

4. **可视化示例区（中下）**：
   展示找出2-20内素数的过程，用不同颜色表示不同步骤，被划掉的数字打红叉
   结果：[2,3,5,7,11,13,17,19]用绿色星星高亮

5. **代码实现区（右侧）**：完整C++代码

6. **时间复杂度区（底部中央）**：
   "⏱️ 时间复杂度：O(n log log n)"
   "空间复杂度：O(n)"
   用黄色背景框突出显示

整体风格：卡通机器人、明亮配色（蓝色、橙色、绿色、粉红色）、适合14岁学生
```


```md
创建一张16:9横版科普图，主题是"C++ 欧拉筛（线性筛）- 最快的素数筛法"，面向14岁学生。

整体布局分为五个区域：

1. **标题区（顶部）**：
   - 主标题："C++欧拉筛（线性筛）"，使用大号蓝色字体
   - 副标题："每个合数只被筛一次！"，使用橙色字体
   - 可爱的机器人助教戴着博士帽

2. **核心思想区（左上）**：
   - 白板写着："欧拉筛的秘密："
     "✓ 每个合数只被最小质因子筛掉"
     "✓ 避免重复标记，速度最快！"
   - 对比图：埃氏筛12被2,3都筛过 ❌ / 欧拉筛12只被2筛一次 ✓

3. **算法流程图（中上）**：
   ① 创建prime数组和isPrime数组
   ② 从i=2遍历到n
   ③ 如果isPrime[i]=true → 加入prime数组
   ④ 对于每个已找到的素数p：标记i*p为合数
   ⑤ 如果i%p==0，跳出循环（关键！用红色强调）

4. **可视化示例区（中下）**：展示筛选2-15的详细过程

5. **代码实现区（右侧）**：完整C++代码，"if(i%p == 0) break;" 用红色高亮

6. **时间复杂度区（底部）**：
   "⏱️ 时间复杂度：O(n) - 线性！"
   "🏆 最快的素数筛法！"
   加小奖杯图标

7. **对比说明**："埃氏筛：O(n log log n) / 欧拉筛：O(n) / n=1000000时快约3倍！"

整体风格：蓝色、紫色、橙色、金色配色，强调"线性"和"最优"特点
```


```md
创建C++ for循环科普海报（竖版3:4），必须完全修正流程图箭头：

**标题：** "C++ for循环探秘" + 可爱机器人

**代码框：**
for (int i = 1; i <= 5; i++) {
    cout << "第" << i << "次循环" << endl;
}

**流程图（4个圆形节点，严格按以下要求绘制箭头）：**

位置排列（顺时针）：
- 左上：初始化(i=1) 蓝色圆圈
- 右上：条件判断(i<=5?) 绿色圆圈  
- 右下：执行循环体 橙色圆圈
- 左下：更新(i++) 紫色圆圈

**箭头连接（必须严格遵守）：**

1️⃣ **从"初始化"出发：**
   - 只有1条箭头：蓝色箭头从"初始化"指向"条件判断"
   
2️⃣ **从"条件判断"出发：**
   - 2条箭头：
     * 绿色箭头标注"是(True)"指向"执行循环体"
     * 红色箭头标注"否(False)"指向右侧"结束"标志
   
3️⃣ **从"执行循环体"出发：**
   - 只有1条箭头：橙色箭头指向"更新(i++)"
   
4️⃣ **从"更新(i++)"出发：**
   - 只有1条箭头：紫色箭头向上弯曲指向"条件判断"
   - ⚠️ **特别注意：这条箭头必须指向"条件判断"，绝对不能指向"初始化"！**

**❌ 禁止出现的箭头：**
- 任何指向"初始化"节点的箭头
- 从"更新"到"初始化"的箭头
- 从任何节点回到"初始化"的箭头

**✅ 正确的循环路径：**
初始化(一次) → 条件判断 → 执行 → 更新 → 回到条件判断（循环）

**右侧输出展示：**
"逐步输出展示"
- 第1次循环 ①
- 第2次循环 ②
- 第3次循环 ③
- 第4次循环 ④
- 第5次循环 ⑤

**底部组件解析：**
3个并排框：
- 初始化: int i = 1 (起点) - 设置循环的开始位置
- 条件: i <= 5 (继续还是停止?) - 判断是否继续循环
- 更新: i++ (每次+1) - 每次循环结束后改变i的值

**底部比喻：**
"就像爬楼梯 - 从1层爬到5层，每次上一层"
配图：小孩爬楼梯1-5

**视觉风格：**
- 明亮友好色彩
- 扁平化可爱图标
- 清晰中文字体
- 浅色科技背景
- 竖版3:4

**【最关键】画流程图时必须牢记：**
- 初始化是"起点"，只执行一次，不在循环内
- 循环由"条件判断-执行-更新"三部分组成
- 更新后必须回到条件判断，而不是初始化
- 初始化节点只有一条出去的箭头，没有任何进入的箭头
```

```md
为16岁学生设计一张横版科普信息图，主题是贪心算法中的最大最小类问题。

布局分为三个部分：
1. 【核心概念】- 解释什么是贪心算法，强调"局部最优→全局最优"的核心思想
2. 【经典例题】- 包含"数列极差问题"和"活动选择问题"两个典型案例，用简洁的图示说明
3. 【解题技巧】- 总结最大最小类贪心问题的解题模式和关键步骤

设计风格：
- 现代简洁，适合青少年学生
- 使用明亮、活泼的配色方案
- 图文结合，信息层次清晰
- 包含适当的图标和示意图辅助理解
- 横版16:9比例

```

```md
Educational infographic about C++ decimal and binary conversion for 14-year-old students, landscape orientation. Clean, modern, technical illustration style with soft gradient backgrounds (light blue to white).

Main content layout:
1. Title at top: "C++进制转换：十进制 ⟷ 二进制"

2. Left section - "十进制 → 二进制" (Decimal to Binary):
   - Clear heading with arrow icon
   - Algorithm explanation: "除2取余法" (Division by 2 method)
   - Step-by-step example: Convert decimal 13 to binary
   - Visual flow diagram:
     * 13 ÷ 2 = 6 ... 余数1
     * 6 ÷ 2 = 3 ... 余数0
     * 3 ÷ 2 = 1 ... 余数1
     * 1 ÷ 2 = 0 ... 余数1
   - Result: 1101₂ (reading remainders from bottom to top)
   - Simple C++ code block showing while loop implementation

3. Right section - "二进制 → 十进制" (Binary to Decimal):
   - Clear heading with arrow icon
   - Algorithm explanation: "按权展开法" (Positional notation method)
   - Step-by-step example: Convert binary 1101 to decimal
   - Visual calculation:
     * 1×2³ + 1×2² + 0×2¹ + 1×2⁰
     * 8 + 4 + 0 + 1 = 13
   - Simple C++ code block showing the calculation loop

Visual style: Soft pastel color scheme (light blues, mint greens, soft purples), clean sans-serif fonts, rounded rectangles for code blocks, subtle shadows, professional yet approachable design, mathematical symbols clearly displayed, arrows indicating process flow. Include small binary digit icons (0s and 1s) as decorative elements.
```

```md
Educational infographic about "Binary Search on Answer" for 14-year-old students. Landscape orientation, Chinese language. Four sections:

**Section 1 (Top-left, 30%)** - Real problem scenario with cute icons:
Title: "🎯 实际问题"
"老师要把100本书分给5个同学，每个同学至少分1本。怎样分配，能让拿书最多的那个同学的书尽可能少？"
Show 5 cartoon students and stacks of books, with question mark "最少需要多少本？"

**Section 2 (Top-right, 30%)** - Core concept:
Title: "💡 二分答案的思路"
"不直接算答案，而是猜一个数字k，问：'能不能让每个人都不超过k本？'"
"✓ 如果可以 → 答案可能更小，往左找"
"✗ 如果不行 → 答案需要更大，往右找"
Show a thinking process with arrows

**Section 3 (Middle, 25%)** - Visual binary search process:
Show number line 1 to 100, with binary search steps:
Step 1: left=1, right=100, mid=50 → check(50)? ✓ → right=50
Step 2: left=1, right=50, mid=25 → check(25)? ✓ → right=25  
Step 3: left=1, right=25, mid=13 → check(13)? ✗ → left=14
Final: Answer = 20
Use colored arrows and highlighting

**Section 4 (Bottom, 15%)** - Simple code:
```cpp
int left = 1, right = 100;  // 答案范围
while (left < right) {
    int mid = (left + right) / 2;
    if (check(mid)) right = mid;  // mid可行，试试更小的
    else left = mid + 1;           // mid不行，要更大
}
// left 就是答案
```


```md
Educational infographic about Fibonacci recursive solution in Chinese. Title "一图看懂斐波那契数列递归解法".

Sections:
1. "兔子问题起源" - rabbit breeding illustration
2. "数学定义" - F(n)=F(n-1)+F(n-2), F(0)=0, F(1)=1
3. "递归树结构" - PERFECTLY CORRECT tree for f(5):

EXACT STRUCTURE:
Level 1: f(5)
Level 2: f(5) splits to [f(4), f(3)]

Level 3: 
- f(4) splits to [f(3), f(2)]
- RIGHT f(3) splits to [f(2), f(1)✓LEAF]

Level 4:
- LEFT f(3) splits to [f(2), f(1)✓LEAF]  
- First f(2) splits to [f(1)✓LEAF, f(0)✓LEAF]

Level 5:
- Remaining f(2) nodes each split to [f(1)✓LEAF, f(0)✓LEAF]

VERIFICATION RULES - Every node MUST follow:
- f(5) = f(4) + f(3) ✓
- f(4) = f(3) + f(2) ✓
- f(3) = f(2) + f(1) ✓✓✓ CRITICAL!
- f(2) = f(1) + f(0) ✓
- f(1) = leaf "返回1"
- f(0) = leaf "返回0"

Color coding: green circles for f(n≥2), orange for f(1) leaves, blue for f(0) leaves

4. "C++代码" - code snippet in box
5. "性能问题" - O(2^n) warning with duplication diagram
6. "优化方向" - DP and memoization

Modern educational design, clear hierarchy, soft colors. THE TREE MUST BE MATHEMATICALLY PERFECT - every f(3) node has exactly children f(2) and f(1).
```