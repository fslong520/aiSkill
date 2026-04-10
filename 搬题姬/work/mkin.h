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
        fout << "5" << endl;
        fout << "1 2 3 4 5" << endl;
    }
    else if (case_num == 2)
    {
        // n=1, 不需要操作
        fout << "1" << endl;
        fout << "42" << endl;
    }
    else if (case_num == 3)
    {
        // 所有元素已经相同
        fout << "5" << endl;
        fout << "3 3 3 3 3" << endl;
    }
    else if (case_num == 4)
    {
        // 只有两个元素
        fout << "2" << endl;
        fout << "1 100" << endl;
    }
    else if (case_num == 5)
    {
        // 负数
        fout << "5" << endl;
        fout << "-5 -3 0 3 5" << endl;
    }
    else if (case_num >= 6 && case_num <= 10)
    {
        int n = 5 + (case_num - 6) * 5;
        fout << n << endl;
        for (int i = 0; i < n; i++) {
            fout << (rand() % 201 - 100) << (i == n - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num >= 11 && case_num <= 15)
    {
        int n = 100 + (case_num - 11) * 200;
        fout << n << endl;
        for (int i = 0; i < n; i++) {
            fout << (rand() % 20001 - 10000) << (i == n - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num >= 16 && case_num <= 20)
    {
        int n = 1000 + (case_num - 16) * 24750;
        fout << n << endl;
        for (int i = 0; i < n; i++) {
            fout << (rand() % 2000000001 - 1000000000) << (i == n - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num == 21)
    {
        // 全相同
        int n = 1000;
        fout << n << endl;
        for (int i = 0; i < n; i++) fout << "7" << (i == n - 1 ? "" : " ");
        fout << endl;
    }
    else if (case_num == 22)
    {
        // 等差数列
        int n = 100;
        fout << n << endl;
        for (int i = 0; i < n; i++) {
            fout << (i * 2 + 1) << (i == n - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num == 23)
    {
        // 包含极端值
        fout << "5" << endl;
        fout << "-1000000000 0 0 0 1000000000" << endl;
    }
    else if (case_num == 24)
    {
        // n=100000
        int n = 100000;
        fout << n << endl;
        for (int i = 0; i < n; i++) {
            fout << (rand() % 2000000001 - 1000000000) << (i == n - 1 ? "" : " ");
        }
        fout << endl;
    }
    else
    {
        int n = rand() % 50000 + 1;
        fout << n << endl;
        for (int i = 0; i < n; i++) {
            fout << (rand() % 2000000001 - 1000000000) << (i == n - 1 ? "" : " ");
        }
        fout << endl;
    }
}

#endif
