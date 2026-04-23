# 信奥赛代码转换详细规范

## 完整转换映射表

### 常见变量名转换
| 原变量名 | 转换后 | 用途说明 |
|---------|--------|----------|
| numberOfStudents | n | 学生数量 |
| studentScores | a[] | 学生成绩数组 |
| temp/ temporary | t | 临时变量 |
| index/counter | i,j,k | 循环变量 |
| result/answer | ans | 答案变量 |
| sum/total | sum | 求和变量 |
| max/min | mx/mn | 最大最小值 |
| length/size | len | 长度变量 |
| flag/isValid | flg | 标志变量 |

### 数据结构转换
| 原结构 | 转换后 | 说明 |
|--------|--------|------|
| vector<int> arr | int a[1005] | 固定大小数组 |
| vector<vector<int>> matrix | int a[105][105] | 二维数组 |
| queue<int> q | queue<int> q | STL容器保持不变 |
| stack<int> st | stack<int> st | STL容器保持不变 |
| priority_queue<int> pq | priority_queue<int> pq | STL容器保持不变 |

### 常用函数转换
| 原函数 | 转换后 | 说明 |
|--------|--------|------|
| arr.size() | n | 数组长度用变量表示 |
| arr.push_back(x) | a[n++] = x | 数组赋值并递增 |
| sort(arr.begin(), arr.end()) | sort(a, a + n) | 数组排序 |
| reverse(arr.begin(), arr.end()) | reverse(a, a + n) | 数组反转 |

## 特殊情况处理

### 1. 复杂算法保持原逻辑
对于复杂的算法实现（如DFS、BFS、DP等），只调整变量命名和格式，保持核心算法逻辑不变。

### 2. 输入输出处理
```cpp
// 原始写法
cin >> numberOfStudents >> numberOfQuestions;
for(int i = 0; i < numberOfStudents; i++) {
    for(int j = 0; j < numberOfQuestions; j++) {
        cin >> scores[i][j];
    }
}

// 转换后
cin >> n >> m;
for(int i = 0; i < n; i++) {
    for(int j = 0; j < m; j++) {
        cin >> a[i][j];
    }
}
```

### 3. 条件判断优化
```cpp
// 原始写法
if(studentScore >= passingScore) {
    passedCount++;
}

// 转换后
if(a[i] >= x) {
    ans++;
}
```

### 4. 循环优化
```cpp
// 原始写法
for(int currentIndex = 0; currentIndex < arraySize; currentIndex++) {
    sum += arrayOfNumbers[currentIndex];
}

// 转换后
for(int i = 0; i < n; i++) {
    sum += a[i];
}
```

## 头文件映射

### 基础头文件
```cpp
// 替换万能头
#include <bits/stdc++.h>  // 删除

// 添加具体头文件
#include <iostream>       // 必须
#include <algorithm>      // sort, reverse等
#include <vector>         // 如果使用vector
#include <queue>          // 如果使用队列
#include <stack>          // 如果使用栈
#include <map>            // 如果使用map
#include <set>            // 如果使用set
```

## 代码结构调整

### 1. 函数声明转换
```cpp
// 原始写法
void processStudentData(vector<int>& scores, int threshold) {
    // 函数体
}

// 转换后
void solve()
{
    // 函数体
}
```

### 2. 主函数格式
```cpp
// 标准竞赛格式
int main()
{
    // 输入部分
    
    // 处理部分
    
    // 输出部分
    cout << ans << endl;
    return 0;
}
```

### 3. 全局变量声明
所有需要在多个函数间共享的变量都应该声明为全局变量：
```cpp
int n, m, k;           // 基本变量
int a[1005];           // 一维数组
int b[105][105];       // 二维数组
bool vis[1005];        // 访问标记数组
int ans, cnt, mx, mn;  // 结果变量
```

## 常见模式转换

### 1. 计数问题
```cpp
// 原始
int count = 0;
for(int i = 0; i < students.size(); i++) {
    if(students[i] > averageScore) {
        count++;
    }
}

// 转换后
ans = 0;
for(int i = 0; i < n; i++) {
    if(a[i] > x) {
        ans++;
    }
}
```

### 2. 查找最值
```cpp
// 原始
int maxValue = INT_MIN;
for(int i = 0; i < numbers.size(); i++) {
    if(numbers[i] > maxValue) {
        maxValue = numbers[i];
    }
}

// 转换后
mx = -1e9;
for(int i = 0; i < n; i++) {
    if(a[i] > mx) {
        mx = a[i];
    }
}
```

### 3. 累加求和
```cpp
// 原始
int totalSum = 0;
for(int i = 0; i < values.size(); i++) {
    totalSum += values[i];
}

// 转换后
sum = 0;
for(int i = 0; i < n; i++) {
    sum += a[i];
}
```

## 错误处理和边界情况

### 1. 数组越界防护
```cpp
// 添加适当注释
// 注意数组边界：0 <= i < n
for(int i = 0; i < n; i++) {
    // 处理逻辑
}
```

### 2. 特殊输入处理
```cpp
// 处理特殊情况
if(n == 0) {
    cout << 0 << endl;
    return 0;
}
```

## 性能优化建议

### 1. 避免重复计算
```cpp
// 提前计算常量
int half = n / 2;
for(int i = 0; i < half; i++) {
    // 使用half而不是每次计算n/2
}
```

### 2. 合理使用全局变量
```cpp
// 对于频繁访问的数据使用全局变量
int prefix[1005];  // 前缀和数组
```

这个参考文档提供了详细的转换规则，在实际转换过程中可以根据具体情况灵活应用这些规则。