#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    string names[] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"};
    if (case_num == 1)
    {
        // 样例1
        fout << "5" << endl;
        fout << "A 100 1000" << endl;
        fout << "B 90 1000" << endl;
        fout << "C 100 1000" << endl;
        fout << "D 80 500" << endl;
        fout << "E 100 800" << endl;
    }
    else if (case_num == 2)
    {
        // 样例2：1个人
        fout << "1" << endl;
        fout << "Boss 1 100" << endl;
    }
    else if (case_num == 3)
    {
        // 样例3：帮贡相同，按等级
        fout << "3" << endl;
        fout << "X 10 100" << endl;
        fout << "Y 20 100" << endl;
        fout << "Z 5 100" << endl;
    }
    else if (case_num == 4)
    {
        // 样例4：帮贡等级都相同，按顺序
        fout << "3" << endl;
        fout << "P1 10 100" << endl;
        fout << "P2 10 100" << endl;
        fout << "P3 10 100" << endl;
    }
    else if (case_num == 5)
    {
        // 样例5：刚好分完职位
        fout << "7" << endl;
        for(int i=0; i<7; i++) fout << names[i] << " " << (100-i) << " " << (1000-i) << endl;
    }
    else if (case_num >= 6 && case_num <= 10)
    {
        // 中等规模：N=10~50
        int n = 10 + (case_num - 6) * 10;
        fout << n << endl;
        for(int i=0; i<n; i++) fout << names[i%15] << i << " " << (rand()%100) << " " << (rand()%2000) << endl;
    }
    else if (case_num >= 11 && case_num <= 15)
    {
        // 中等规模：N=80
        int n = 80;
        fout << n << endl;
        for(int i=0; i<n; i++) fout << "M" << i << " " << (rand()%100) << " " << (rand()%5000) << endl;
    }
    else if (case_num >= 16 && case_num <= 20)
    {
        // 大规模边界：N=100
        int n = 100;
        fout << n << endl;
        for(int i=0; i<n; i++) fout << "Mem" << i << " " << (rand()%100) << " " << (rand()%10000) << endl;
    }
    else if (case_num >= 21 && case_num <= 25)
    {
        // 随机测试：N=1~100
        int n = rand()%100 + 1;
        fout << n << endl;
        for(int i=0; i<n; i++) fout << "R" << i << " " << (rand()%100) << " " << (rand()%10000) << endl;
    }
}

#endif
