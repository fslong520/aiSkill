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
        // 样例1
        fout << "5 3" << endl;
        fout << "1 2 3 1 2" << endl;
    }
    else if (case_num == 2)
    {
        // 样例2
        fout << "8 5" << endl;
        fout << "2 3 5 1 4 2 3 5" << endl;
    }
    else if (case_num == 3)
    {
        // 样例3：大K值
        fout << "10 1000000000" << endl;
        fout << "500000000 500000000 300000000 700000000 100000000 900000000 400000000 600000000 200000000 800000000" << endl;
    }
    else if (case_num == 4)
    {
        // 最小值：N=1, K=1
        fout << "1 1" << endl;
        fout << "1" << endl;
    }
    else if (case_num == 5)
    {
        // K=1，所有区间都满足
        fout << "5 1" << endl;
        fout << "1 2 3 4 5" << endl;
    }
    else if (case_num >= 6 && case_num <= 10)
    {
        // 小规模测试：N=10~50, K较小
        int N = 10 + (case_num - 6) * 10;
        long long K = rand() % 10 + 2;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (rand() % 100 + 1) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num >= 11 && case_num <= 15)
    {
        // 中等规模测试：N=100~1000
        int N = 100 + (case_num - 11) * 225;
        long long K = rand() % 100 + 10;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (rand() % 1000 + 1) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num >= 16 && case_num <= 20)
    {
        // 大规模测试：N=10000~100000
        int N = 10000 + (case_num - 16) * 22500;
        long long K = rand() % 10000 + 100;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (rand() % 100000 + 1) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num == 21)
    {
        // 边界情况：所有A[i]都是K的倍数
        int N = 100;
        long long K = 7;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (K * (rand() % 10 + 1)) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num == 22)
    {
        // 边界情况：所有A[i]都不是K的倍数，但某些区间和是
        int N = 100;
        long long K = 5;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (rand() % 4 + 1) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num == 23)
    {
        // 边界情况：K非常大
        int N = 1000;
        long long K = 1000000000;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (rand() % 1000000000 + 1) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
    else if (case_num == 24)
    {
        // 最大规模测试：N=200000
        int N = 200000;
        long long K = rand() % 1000000000 + 1;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (rand() % 1000000000 + 1) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
    else
    {
        // 随机压力测试
        int N = rand() % 50000 + 1;
        long long K = rand() % 1000000000 + 1;
        fout << N << " " << K << endl;
        for (int i = 0; i < N; i++) {
            fout << (rand() % 1000000000 + 1) << (i == N - 1 ? "" : " ");
        }
        fout << endl;
    }
}

#endif
