---
name: OI风格

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
  trigger: C++代码转换、信奥赛风格、代码规范化、竞赛代码优化
  source: 基于信息学奥林匹克竞赛代码规范和实践经验
---

# 信奥赛代码风格转换器

## 功能说明
自动扫描文档中的C++代码块，将其转换为符合信息学奥林匹克竞赛规范的代码风格：
- 使用简短变量名（不超过5个字符）
- 优先使用全局变量
- 采用竞赛标准格式（左大括号另起一行）
- 明确包含所需头文件
- 添加必要的中文注释

## 使用方法
直接在文档中运行此skill，它会自动找到所有C++代码块并进行转换。

## 转换规则

### 变量命名规范
- 函数名、变量名、参数名不超过5个字符
- 优先使用字母：a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
- 循环变量常用：i, j, k
- 数组名常用：a, b, c, d
- 临时变量常用：x, y, z, t

### 代码格式要求
- 左大括号必须另起一行
- 使用4个空格缩进
- 逻辑段落之间留空行
- 关键步骤添加中文注释

### 头文件规范
- 不使用万能头文件 `<bits/stdc++.h>`
- 明确包含所需的具体头文件
- 常用：`<iostream>`, `<algorithm>`, `<vector>`, `<queue>`, `<stack>` 等

## 转换示例

**转换前：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int numberOfStudents;
    vector<int> studentScores;
    
    cin >> numberOfStudents;
    for(int i = 0; i < numberOfStudents; i++) {
        int score;
        cin >> score;
        studentScores.push_back(score);
    }
    
    sort(studentScores.begin(), studentScores.end());
    
    int sum = 0;
    for(int i = 0; i < numberOfStudents; i++) {
        sum += studentScores[i];
    }
    
    cout << sum << endl;
    return 0;
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
    
    for(int i = 0; i < n; i++)
    {
        cin >> a[i];
    }
    
    sort(a, a + n);
    
    for(int i = 0; i < n; i++)
    {
        ans += a[i];
    }
    
    cout << ans << endl;
    return 0;
}
```

## 注意事项
1. 只转换标记为cpp语言的代码块
2. 保持原有逻辑不变，仅调整格式和命名
3. 数组索引从0开始（符合C++标准）
4. 保留原有的算法思路和解题方法
5. 在关键步骤添加适当的中文注释
