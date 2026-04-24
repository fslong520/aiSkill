# 信奥赛代码转换实例

## 实例1：简单排序问题

### 转换前
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int numberOfElements;
    vector<int> elements;
    
    cin >> numberOfElements;
    for(int i = 0; i < numberOfElements; i++) {
        int elementValue;
        cin >> elementValue;
        elements.push_back(elementValue);
    }
    
    sort(elements.begin(), elements.end());
    
    for(int i = 0; i < numberOfElements; i++) {
        cout << elements[i] << " ";
    }
    cout << endl;
    
    return 0;
}
```

### 转换后
```cpp
#include <iostream>
#include <algorithm>
using namespace std;

int n, a[1005];

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
        cout << a[i] << " ";
    }
    cout << endl;
    
    return 0;
}
```

## 实例2：查找最大值

### 转换前
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int arraySize;
    vector<int> dataArray;
    
    cin >> arraySize;
    for(int currentIndex = 0; currentIndex < arraySize; currentIndex++) {
        int inputValue;
        cin >> inputValue;
        dataArray.push_back(inputValue);
    }
    
    int maximumValue = dataArray[0];
    for(int i = 1; i < arraySize; i++) {
        if(dataArray[i] > maximumValue) {
            maximumValue = dataArray[i];
        }
    }
    
    cout << "Maximum value is: " << maximumValue << endl;
    return 0;
}
```

### 转换后
```cpp
#include <iostream>
using namespace std;

int n, a[1005], mx;

int main()
{
    cin >> n;
    
    for(int i = 0; i < n; i++)
    {
        cin >> a[i];
    }
    
    mx = a[0];
    for(int i = 1; i < n; i++)
    {
        if(a[i] > mx)
        {
            mx = a[i];
        }
    }
    
    cout << mx << endl;
    return 0;
}
```

## 实例3：二维数组处理

### 转换前
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int numberOfRows, numberOfColumns;
    vector<vector<int>> matrix;
    
    cin >> numberOfRows >> numberOfColumns;
    
    // 读入矩阵
    for(int row = 0; row < numberOfRows; row++) {
        vector<int> currentRow;
        for(int col = 0; col < numberOfColumns; col++) {
            int value;
            cin >> value;
            currentRow.push_back(value);
        }
        matrix.push_back(currentRow);
    }
    
    // 计算每行的和
    vector<int> rowSums;
    for(int row = 0; row < numberOfRows; row++) {
        int rowSum = 0;
        for(int col = 0; col < numberOfColumns; col++) {
            rowSum += matrix[row][col];
        }
        rowSums.push_back(rowSum);
    }
    
    // 输出结果
    for(int i = 0; i < rowSums.size(); i++) {
        cout << "Row " << (i + 1) << " sum: " << rowSums[i] << endl;
    }
    
    return 0;
}
```

### 转换后
```cpp
#include <iostream>
using namespace std;

int n, m, a[105][105], sum[105];

int main()
{
    cin >> n >> m;
    
    // 读入矩阵
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            cin >> a[i][j];
        }
    }
    
    // 计算每行的和
    for(int i = 0; i < n; i++)
    {
        sum[i] = 0;
        for(int j = 0; j < m; j++)
        {
            sum[i] += a[i][j];
        }
    }
    
    // 输出结果
    for(int i = 0; i < n; i++)
    {
        cout << sum[i] << endl;
    }
    
    return 0;
}
```

## 实例4：搜索算法

### 转换前
```cpp
#include <bits/stdc++.h>
using namespace std;

bool linearSearch(vector<int>& arr, int target) {
    for(int i = 0; i < arr.size(); i++) {
        if(arr[i] == target) {
            return true;
        }
    }
    return false;
}

int main() {
    int arraySize, searchTarget;
    vector<int> dataArray;
    
    cin >> arraySize;
    for(int i = 0; i < arraySize; i++) {
        int value;
        cin >> value;
        dataArray.push_back(value);
    }
    
    cin >> searchTarget;
    
    if(linearSearch(dataArray, searchTarget)) {
        cout << "Found" << endl;
    } else {
        cout << "Not found" << endl;
    }
    
    return 0;
}
```

### 转换后
```cpp
#include <iostream>
using namespace std;

int n, a[1005], x;

bool find()
{
    for(int i = 0; i < n; i++)
    {
        if(a[i] == x)
        {
            return true;
        }
    }
    return false;
}

int main()
{
    cin >> n;
    
    for(int i = 0; i < n; i++)
    {
        cin >> a[i];
    }
    
    cin >> x;
    
    if(find())
    {
        cout << "Found" << endl;
    }
    else
    {
        cout << "Not found" << endl;
    }
    
    return 0;
}
```

## 实例5：统计问题

### 转换前
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int numberOfStudents;
    vector<int> studentAges;
    
    cin >> numberOfStudents;
    for(int studentIndex = 0; studentIndex < numberOfStudents; studentIndex++) {
        int age;
        cin >> age;
        studentAges.push_back(age);
    }
    
    int countOfAdults = 0;
    int countOfMinors = 0;
    
    for(int i = 0; i < numberOfStudents; i++) {
        if(studentAges[i] >= 18) {
            countOfAdults++;
        } else {
            countOfMinors++;
        }
    }
    
    cout << "Adults: " << countOfAdults << endl;
    cout << "Minors: " << countOfMinors << endl;
    
    double averageAge = 0.0;
    for(int i = 0; i < numberOfStudents; i++) {
        averageAge += studentAges[i];
    }
    averageAge /= numberOfStudents;
    
    cout << "Average age: " << averageAge << endl;
    
    return 0;
}
```

### 转换后
```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int n, a[1005], ad, ch;
double avg;

int main()
{
    cin >> n;
    
    for(int i = 0; i < n; i++)
    {
        cin >> a[i];
    }
    
    // 统计成年人和未成年人数量
    ad = 0;
    ch = 0;
    for(int i = 0; i < n; i++)
    {
        if(a[i] >= 18)
        {
            ad++;
        }
        else
        {
            ch++;
        }
    }
    
    cout << "Adults: " << ad << endl;
    cout << "Minors: " << ch << endl;
    
    // 计算平均年龄
    avg = 0.0;
    for(int i = 0; i < n; i++)
    {
        avg += a[i];
    }
    avg /= n;
    
    cout << "Average age: " << fixed << setprecision(2) << avg << endl;
    
    return 0;
}
```

## 实例6：复杂条件判断

### 转换前
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int numberOfParticipants;
    vector<int> participantScores;
    vector<string> participantNames;
    
    cin >> numberOfParticipants;
    for(int i = 0; i < numberOfParticipants; i++) {
        string name;
        int score;
        cin >> name >> score;
        participantNames.push_back(name);
        participantScores.push_back(score);
    }
    
    int winnerIndex = 0;
    int highestScore = participantScores[0];
    
    for(int i = 1; i < numberOfParticipants; i++) {
        if(participantScores[i] > highestScore) {
            highestScore = participantScores[i];
            winnerIndex = i;
        } else if(participantScores[i] == highestScore && 
                  participantNames[i] < participantNames[winnerIndex]) {
            winnerIndex = i;
        }
    }
    
    cout << "Winner: " << participantNames[winnerIndex] << endl;
    cout << "Score: " << highestScore << endl;
    
    return 0;
}
```

### 转换后
```cpp
#include <iostream>
#include <string>
using namespace std;

int n, a[1005], mx, idx;
string s[1005], ans;

int main()
{
    cin >> n;
    
    for(int i = 0; i < n; i++)
    {
        cin >> s[i] >> a[i];
    }
    
    // 找到最高分及对应的选手
    mx = a[0];
    idx = 0;
    for(int i = 1; i < n; i++)
    {
        if(a[i] > mx)
        {
            mx = a[i];
            idx = i;
        }
        else if(a[i] == mx && s[i] < s[idx])
        {
            idx = i;
        }
    }
    
    cout << "Winner: " << s[idx] << endl;
    cout << "Score: " << mx << endl;
    
    return 0;
}
```

这些实例展示了不同类型问题的转换方法，涵盖了从简单到复杂的各种场景。