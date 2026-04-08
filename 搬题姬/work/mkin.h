#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

// 模拟一轮比赛，返回新的状态
void simulate(int& p1, int& p2, int& waiting, int winner) {
    if (winner == p1) {
        int loser = p2;
        p2 = waiting;
        waiting = loser;
    } else if (winner == p2) {
        int loser = p1;
        p1 = waiting;
        waiting = loser;
    }
}

void test(int case_num, ofstream& fout)
{
    if (case_num == 1)
    {
        // 样例1：合法序列
        fout << "1\n";
        fout << "3\n1\n1\n2\n";
    }
    else if (case_num == 2)
    {
        // 样例2：不合法序列
        fout << "1\n";
        fout << "2\n1\n2\n";
    }
    else if (case_num == 3)
    {
        // 简单合法序列：1赢一次
        fout << "1\n";
        fout << "1\n1\n";
    }
    else if (case_num == 4)
    {
        // 简单合法序列：2赢一次
        fout << "1\n";
        fout << "1\n2\n";
    }
    else if (case_num == 5)
    {
        // 不合法：3一开始就不在场上
        fout << "1\n";
        fout << "1\n3\n";
    }
    else if (case_num == 6)
    {
        // 不合法：连续两个不同的人赢（但第一个人赢后，第二个人已下场）
        fout << "1\n";
        fout << "2\n1\n2\n";
    }
    else if (case_num == 7)
    {
        // 合法：轮流赢
        fout << "1\n";
        fout << "4\n1\n3\n2\n1\n";
    }
    else if (case_num == 8)
    {
        // 不合法：场上没有人能赢
        fout << "1\n";
        fout << "2\n1\n3\n";
    }
    else if (case_num == 9)
    {
        // 多组测试用例：混合合法和非法
        fout << "3\n";
        fout << "1\n1\n";          // 合法
        fout << "1\n2\n";          // 合法
        fout << "1\n3\n";          // 非法
    }
    else if (case_num == 10)
    {
        // 复杂合法序列
        fout << "1\n";
        fout << "6\n1\n3\n1\n2\n3\n2\n";
    }
    else if (case_num >= 11 && case_num <= 15)
    {
        // 中等规模随机测试
        int n = 20 + rand() % 30;
        fout << "1\n" << n << "\n";
        
        int p1 = 1, p2 = 2, waiting = 3;
        for (int i = 0; i < n; i++) {
            // 随机选择场上的一个人作为胜利者
            int winner = (rand() % 2 == 0) ? p1 : p2;
            fout << winner << "\n";
            simulate(p1, p2, waiting, winner);
        }
    }
    else if (case_num == 16)
    {
        // 边界：n=1，最小规模
        fout << "1\n";
        fout << "1\n1\n";
    }
    else if (case_num == 17)
    {
        // 边界：n=100，最大规模
        fout << "1\n";
        fout << "100\n";
        
        int p1 = 1, p2 = 2, waiting = 3;
        for (int i = 0; i < 100; i++) {
            int winner = (rand() % 2 == 0) ? p1 : p2;
            fout << winner << "\n";
            simulate(p1, p2, waiting, winner);
        }
    }
    else if (case_num == 18)
    {
        // 边界：T=10，最大测试组数
        fout << "10\n";
        for (int t = 0; t < 10; t++) {
            int n = 5 + rand() % 10;
            fout << n << "\n";
            
            int p1 = 1, p2 = 2, waiting = 3;
            for (int i = 0; i < n; i++) {
                int winner = (rand() % 2 == 0) ? p1 : p2;
                fout << winner << "\n";
                simulate(p1, p2, waiting, winner);
            }
        }
    }
    else if (case_num == 19)
    {
        // 边界：n=100，故意插入非法
        fout << "1\n";
        fout << "100\n";
        
        int p1 = 1, p2 = 2, waiting = 3;
        for (int i = 0; i < 50; i++) {
            int winner = (rand() % 2 == 0) ? p1 : p2;
            fout << winner << "\n";
            simulate(p1, p2, waiting, winner);
        }
        // 第51次故意输出waiting（非法）
        fout << waiting << "\n";
        for (int i = 52; i < 100; i++) {
            fout << (rand() % 3 + 1) << "\n";  // 随机输出
        }
    }
    else if (case_num == 20)
    {
        // 边界：全是同一个人赢
        fout << "1\n";
        fout << "50\n";
        for (int i = 0; i < 50; i++) {
            fout << "1\n";
        }
    }
    else
    {
        // 随机压力测试
        int T = 1 + rand() % 5;
        fout << T << "\n";
        
        for (int t = 0; t < T; t++) {
            int n = 10 + rand() % 40;
            fout << n << "\n";
            
            int p1 = 1, p2 = 2, waiting = 3;
            bool has_error = (rand() % 3 == 0);  // 1/3概率出现非法
            
            for (int i = 0; i < n; i++) {
                if (has_error && i == n / 2) {
                    // 在中间插入非法的胜利者
                    fout << waiting << "\n";
                } else {
                    int winner = (rand() % 2 == 0) ? p1 : p2;
                    fout << winner << "\n";
                    simulate(p1, p2, waiting, winner);
                }
            }
        }
    }
}

#endif
