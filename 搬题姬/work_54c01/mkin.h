#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

// ═══════════════════════════════════════════════════════════════════
// 总测试点数量 & Subtask 分组配置
// ═══════════════════════════════════════════════════════════════════

const int TEST_CASES = 25;

struct SubtaskDef {
    int id, start, end;
};
const SubtaskDef SUBTASKS[] = {
    {0, 1, 2},    // 样例
    {1, 3, 8},    // 小规模 + 特殊性质
    {2, 9, 11},   // Hack 数据
    {3, 12, 20},  // 中大规模
    {4, 21, 25},  // 随机回归
};
const int SUBTASK_COUNT = sizeof(SUBTASKS) / sizeof(SUBTASKS[0]);

// 工具函数：生成随机数据
int rng(int l, int r) {
    static mt19937 gen(114514);
    return uniform_int_distribution<int>(l, r)(gen);
}

void test(int case_num, ofstream& fout)
{
    // ============================================================
    // Subtask 0: 样例数据 — case 1-2 (10分)
    // ============================================================
    if (case_num == 1)
    {
        // 样例 - 从题面逐字复制
        fout << "10 10 4\n";
        fout << "4 3 8\n";
        fout << "3 5 7\n";
        fout << "2 2 5\n";
        fout << "5 4 9\n";
    }
    else if (case_num == 2)
    {
        // 自制样例2：W=5,V=5,N=3
        // 物品1: (3,2,6); 物品2: (2,3,5); 物品3: (1,1,4)
        // 最优: 全选 w=6>5 不行
        // 选1+3: w=4,v=3,val=10; 选2+3: w=3,v=4,val=9
        // 最佳: 1+3 = val=10
        fout << "5 5 3\n";
        fout << "3 2 6\n";
        fout << "2 3 5\n";
        fout << "1 1 4\n";
    }

    // ============================================================
    // Subtask 1: 小规模 + 特殊性质 — case 3-8 (20分)
    // ============================================================
    else if (case_num == 3)
    {
        // 最小规模 N=1，单物品恰好可放
        fout << "10 10 1\n";
        fout << "5 5 10\n";
    }
    else if (case_num == 4)
    {
        // N=2，验证两物品选其一
        // 物品1: w=8,v=8,val=20
        // 物品2: w=3,v=3,val=8
        // 容量W=10,V=10: 两个都能放(11>10不行),只能放一个
        // 选物品1: w=8,v=8,val=20; 选物品2: w=3,v=3,val=8
        // 最佳: 物品1=20
        fout << "10 10 2\n";
        fout << "8 8 20\n";
        fout << "3 3 8\n";
    }
    else if (case_num == 5)
    {
        // N=8，中等小规模随机
        fout << "15 15 8\n";
        fout << "5 4 12\n";
        fout << "3 6 8\n";
        fout << "7 2 15\n";
        fout << "2 8 6\n";
        fout << "4 5 10\n";
        fout << "6 3 14\n";
        fout << "3 3 7\n";
        fout << "8 7 11\n";
    }
    else if (case_num == 6)
    {
        // 特殊性质1：所有物品重量=1,体积=1,价值递增
        // 验证容量绑定下的选择
        int W = 10, V = 10, N = 15;
        fout << W << " " << V << " " << N << "\n";
        for (int i = 1; i <= N; ++i)
            fout << "1 1 " << i << "\n";
    }
    else if (case_num == 7)
    {
        // 特殊性质2：所有物品价值相同，重量体积各不相同
        // 应优先选体积小重量轻的
        int W = 20, V = 20, N = 10;
        fout << W << " " << V << " " << N << "\n";
        vector<tuple<int,int,int>> items = {
            {5, 5, 10}, {7, 3, 10}, {3, 7, 10},
            {6, 4, 10}, {4, 6, 10}, {2, 8, 10},
            {8, 2, 10}, {1, 9, 10}, {9, 1, 10},
            {10, 10, 10}
        };
        for (auto [x, y, z] : items)
            fout << x << " " << y << " " << z << "\n";
    }
    else if (case_num == 8)
    {
        // 特殊性质3：物品可恰好填满背包（边界条件）
        // W=10,V=10，物品组合可恰好装满
        int W = 10, V = 10, N = 6;
        fout << W << " " << V << " " << N << "\n";
        // (4,4,7) + (3,3,5) + (3,3,6) = w=10,v=10,val=18
        // (2,2,4) + (5,5,9) + (3,3,6) = w=10,v=10,val=19
        // 最佳为后者
        fout << "4 4 7\n";
        fout << "3 3 5\n";
        fout << "3 3 6\n";
        fout << "2 2 4\n";
        fout << "5 5 9\n";
        fout << "1 1 2\n";
    }

    // ============================================================
    // Subtask 2: Hack 数据 — case 9-11 (15分)
    // ============================================================
    else if (case_num == 9)
    {
        // Hack 1: N=100，所有物品重量体积均为1，价值=1
        // 测试 O(W*V*N)=100^3=1e6 压力下的正确性
        int W = 50, V = 50, N = 100;
        fout << W << " " << V << " " << N << "\n";
        for (int i = 0; i < N; ++i)
            fout << "1 1 1\n";
    }
    else if (case_num == 10)
    {
        // Hack 2: 单物品恰好等于背包容量（边界漏判测试）
        // dp[W][V] 应等于此物品价值
        int W = 100, V = 100, N = 1;
        fout << W << " " << V << " " << N << "\n";
        fout << "100 100 50\n";
    }
    else if (case_num == 11)
    {
        // Hack 3: 所有物品都放不下，答案应为0
        // 针对：未处理无边初始化（dp数组全0则正确）
        int W = 5, V = 5, N = 3;
        fout << W << " " << V << " " << N << "\n";
        fout << "6 6 100\n";  // w>W, v>V
        fout << "5 6 200\n";  // v>V
        fout << "6 5 300\n";  // w>W
    }

    // ============================================================
    // Subtask 3: 中大规模数据 — case 12-20 (30分)
    // ============================================================
    else if (case_num >= 12 && case_num <= 15)
    {
        // 中等规模：N=30-80, W,V=30-80
        int W, V, N;
        if (case_num == 12) { W = 30; V = 30; N = 30; }
        else if (case_num == 13) { W = 50; V = 50; N = 50; }
        else if (case_num == 14) { W = 80; V = 60; N = 70; }
        else { W = 60; V = 80; N = 40; }
        fout << W << " " << V << " " << N << "\n";
        for (int i = 0; i < N; ++i) {
            int w = rng(1, W);
            int v = rng(1, V);
            int val = rng(1, 100);
            fout << w << " " << v << " " << val << "\n";
        }
    }
    else if (case_num >= 16 && case_num <= 20)
    {
        // 大规模压力测试：N接近100, W,V接近100
        int W, V, N;
        if (case_num == 16) { W = 80; V = 80; N = 80; }
        else if (case_num == 17) { W = 100; V = 100; N = 90; }
        else if (case_num == 18) { W = 100; V = 100; N = 100; }
        else if (case_num == 19) { W = 100; V = 90; N = 100; }
        else { W = 90; V = 100; N = 100; }
        fout << W << " " << V << " " << N << "\n";
        for (int i = 0; i < N; ++i) {
            int w = rng(1, W);
            int v = rng(1, V);
            int val = rng(1, 100);
            fout << w << " " << v << " " << val << "\n";
        }
    }

    // ============================================================
    // Subtask 4: 随机回归测试 — case 21-25 (25分)
    // ============================================================
    else
    {
        // 混合随机：覆盖各种 N,W,V 组合
        int W, V, N;
        if (case_num == 21) { W = 1; V = 100; N = 50; }    // 极端：重量为1
        else if (case_num == 22) { W = 100; V = 1; N = 50; } // 极端：体积为1
        else if (case_num == 23) { W = 100; V = 100; N = 1; } // 极端：单物品
        else if (case_num == 24) { W = 100; V = 100; N = 100; } // 全满
        else { W = 50; V = 50; N = 100; } // 物品多但容量小

        fout << W << " " << V << " " << N << "\n";
        for (int i = 0; i < N; ++i) {
            int w = rng(1, max(1, W));
            int v = rng(1, max(1, V));
            int val = rng(1, 100);
            fout << w << " " << v << " " << val << "\n";
        }
    }
}

#endif
