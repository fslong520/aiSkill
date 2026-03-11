#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1)
    {
        // 样例1：N=1，输出0
        fout << "1" << endl;
    }
    else if (case_num == 2)
    {
        // 样例2：N=2，输出0
        fout << "2" << endl;
    }
    else if (case_num == 3)
    {
        // 样例3：N=11，输出2026
        fout << "11" << endl;
    }
    else if (case_num == 4)
    {
        // 边界测试：N=1（最小值）
        fout << "1" << endl;
    }
    else if (case_num == 5)
    {
        // 边界测试：N=11（最大值）
        fout << "11" << endl;
    }
    else if (case_num >= 6 && case_num <= 13)
    {
        // 中间值测试：N=3到10
        fout << (case_num - 3) << endl;
    }
    else
    {
        // 随机测试：生成1到11之间的随机数
        fout << (rand() % 11 + 1) << endl;
    }
}

#endif