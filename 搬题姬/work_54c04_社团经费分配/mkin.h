#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

// ═══════════════════════════════════════════════════════════════════
// 总测试点数量 & Subtask 分组配置
// ═══════════════════════════════════════════════════════════════════
// 修改 test() 时同步更新下方 SUBTASK 数组，
// 以及 testdata/config.yaml 中的 cases 列表。
//
// 默认分组策略（5 个子任务，总分 100）：
//   Subtask 0: 样例        (case 1-2)   10分
//   Subtask 1: 小规模+特殊  (case 3-8)   20分
//   Subtask 2: Hack        (case 9-11)  15分
//   Subtask 3: 中大规模     (case 12-20) 30分
//   Subtask 4: 随机回归     (case 21-25) 25分
// ═══════════════════════════════════════════════════════════════════

const int TEST_CASES = 25;

// Subtask 分组：{subtask_id, start_case, end_case}
// 修改 test() 中 case 分组时同步更新此数组
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

// ═══════════════════════════════════════════════════════════════
// ⚠️ 只看这里：改 mkin.h，别动 mkdata.cpp！
// ═══════════════════════════════════════════════════════════════
// 
// ✅ 改这个文件（mkin.h）里的 test() 函数
// ❌ 别动 mkdata.cpp（框架代码，不需要改）
//
// 测试数据分组（25组）：请同步修改 SUBTASKS[] 和 config.yaml
// ═══════════════════════════════════════════════════════════════

// 随机工具
mt19937 rng(114514);

int rand_int(int l, int r) {
    return uniform_int_distribution<int>(l, r)(rng);
}

void gen_random(int M, int G, int max_cnt, ofstream &fout) {
    fout << M << " " << G << "\n";
    for (int i = 0; i < G; ++i) {
        int cnt = rand_int(1, max_cnt);
        fout << cnt << "\n";
        for (int j = 0; j < cnt; ++j) {
            int w = rand_int(1, M);
            int v = rand_int(1, 100);
            fout << w << " " << v << "\n";
        }
    }
}

/**
 * 测试数据生成函数
 * 
 * 参数：
 *   case_num: 测试点编号（1-25）
 *   fout: 输出文件流（写入 .in 文件）
 */

void test(int case_num, ofstream& fout)
{
    // ============================================================
    // Subtask 0: 样例数据（直接复制题目样例） — case 1-2
    // ============================================================
    if (case_num == 1)
    {
        // 样例1：3 组，选 (20,10)+(15,11)+(15,7)=50 总满意 28
        fout << "50 3\n";
        fout << "2\n20 10\n15 7\n";
        fout << "2\n15 11\n10 5\n";
        fout << "2\n15 7\n10 3\n";
    }
    else if (case_num == 2)
    {
        // 样例2：2 组，选 (10,8)+(12,6)=22 总满意 14
        fout << "25 2\n";
        fout << "3\n10 8\n15 5\n8 4\n";
        fout << "2\n12 6\n9 3\n";
    }
    
    // ============================================================
    // Subtask 1: 小规模随机数据（最小 N，验证基本功能）— case 3-5
    // ============================================================
    else if (case_num == 3)
    {
        // 最小规模：M=5, G=2, 每组 1-2 个物品
        fout << "5 2\n";
        fout << "1\n3 5\n";
        fout << "2\n2 4\n4 6\n";
    }
    else if (case_num == 4)
    {
        // M=10, G=3, 少量物品
        fout << "10 3\n";
        fout << "1\n5 8\n";
        fout << "2\n3 4\n6 7\n";
        fout << "1\n4 5\n";
    }
    else if (case_num == 5)
    {
        // M=20, G=5, 小规模
        fout << "20 5\n";
        fout << "2\n7 9\n3 4\n";
        fout << "1\n10 12\n";
        fout << "2\n5 6\n8 10\n";
        fout << "1\n6 7\n";
        fout << "2\n4 5\n9 11\n";
    }
    
    // ============================================================
    // Subtask 1(续): 特殊性质数据 — case 6-8
    // ============================================================
    else if (case_num == 6)
    {
        // 特殊性质1：所有物品性价比相同（w=v），仅规模不同
        fout << "30 4\n";
        for (int g = 0; g < 4; ++g) {
            fout << "2\n";
            fout << (g + 1) * 3 << " " << (g + 1) * 3 << "\n";
            fout << (g + 1) * 5 << " " << (g + 1) * 5 << "\n";
        }
    }
    else if (case_num == 7)
    {
        // 特殊性质2：每组只有一个物品（退化为 0/1 背包）
        fout << "50 6\n";
        for (int i = 0; i < 6; ++i) {
            fout << "1\n";
            fout << (i + 1) * 7 << " " << (i + 1) * 12 << "\n";
        }
    }
    else if (case_num == 8)
    {
        // 特殊性质3：G=1 大组，10 个物品（退化单向选择）
        fout << "100 1\n";
        fout << "10\n";
        int ws[] = {10, 20, 30, 40, 50, 15, 25, 35, 45, 55};
        int vs[] = {5, 15, 20, 25, 30, 8, 18, 22, 28, 35};
        for (int i = 0; i < 10; ++i) {
            fout << ws[i] << " " << vs[i] << "\n";
        }
    }
    
    // ============================================================
    // Subtask 2: Hack 数据（针对常见错误写法）— case 9-11
    // ============================================================
    else if (case_num == 9)
    {
        // Hack 1: M=1（最小预算），仅 w=1 的物品可选
        fout << "1 5\n";
        for (int g = 0; g < 5; ++g) {
            fout << "2\n";
            fout << "1 " << rand_int(1, 100) << "\n";
            fout << "2 " << rand_int(1, 100) << "\n";
        }
    }
    else if (case_num == 10)
    {
        // Hack 2: 所有物品 w > M → 答案 = 0
        fout << "10 3\n";
        fout << "2\n15 10\n20 5\n";
        fout << "2\n12 8\n18 6\n";
        fout << "1\n25 15\n";
    }
    else if (case_num == 11)
    {
        // Hack 3: 恰有一个物品正好花费全部预算
        fout << "100 2\n";
        fout << "2\n50 30\n100 60\n";
        fout << "3\n40 25\n30 20\n20 15\n";
    }
    
    // ============================================================
    // Subtask 3: 中等规模数据（验证效率）— case 12-15
    // ============================================================
    else if (case_num == 12)
    {
        // 中等：M=200, G=10
        gen_random(200, 10, 5, fout);
    }
    else if (case_num == 13)
    {
        // 中等：M=300, G=15
        gen_random(300, 15, 6, fout);
    }
    else if (case_num == 14)
    {
        // 中等：M=500, G=20
        gen_random(500, 20, 8, fout);
    }
    else if (case_num == 15)
    {
        // 中等：M=800, G=30
        gen_random(800, 30, 8, fout);
    }
    
    // ============================================================
    // Subtask 3(续): 大规模数据（压力测试）— case 16-20
    // ============================================================
    else if (case_num == 16)
    {
        // 大规模：M=1000, G=50
        gen_random(1000, 50, 10, fout);
    }
    else if (case_num == 17)
    {
        // 大规模：M=1000, G=80
        gen_random(1000, 80, 10, fout);
    }
    else if (case_num == 18)
    {
        // 大规模：M=1000, G=100（max），每组 10 个物品（max）
        fout << "1000 100\n";
        for (int g = 0; g < 100; ++g) {
            fout << "10\n";
            for (int j = 0; j < 10; ++j) {
                int w = rand_int(1, 1000);
                int v = rand_int(1, 100);
                fout << w << " " << v << "\n";
            }
        }
    }
    else if (case_num == 19)
    {
        // 大规模 + 特殊：所有物品 w=1（退化，每组 max(v) 即该组最优）
        fout << "1000 100\n";
        for (int g = 0; g < 100; ++g) {
            fout << "5\n";
            for (int j = 0; j < 5; ++j) {
                int v = rand_int(1, 100);
                fout << "1 " << v << "\n";
            }
        }
    }
    else if (case_num == 20)
    {
        // 大规模 + 特殊：v=w（性价比恒定），每组 3-6 个物品
        fout << "1000 80\n";
        for (int g = 0; g < 80; ++g) {
            int cnt = rand_int(3, 6);
            fout << cnt << "\n";
            for (int j = 0; j < cnt; ++j) {
                int w = rand_int(1, 1000);
                int v = w;
                fout << w << " " << v << "\n";
            }
        }
    }
    
    // ============================================================
    // Subtask 4: 随机回归测试 — case 21-25
    // ============================================================
    else if (case_num == 21)
    {
        gen_random(100, 10, 5, fout);
    }
    else if (case_num == 22)
    {
        gen_random(300, 25, 7, fout);
    }
    else if (case_num == 23)
    {
        gen_random(600, 40, 8, fout);
    }
    else if (case_num == 24)
    {
        gen_random(800, 60, 10, fout);
    }
    else // case_num == 25
    {
        gen_random(1000, 80, 10, fout);
    }
}

#endif
