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
// 辅助函数：生成随机整数
// ═══════════════════════════════════════════════════════════════

int rnd(int a, int b) {
    return a + rand() % (b - a + 1);
}

void writeln(ofstream& fout) {}

template<typename T, typename... Args>
void writeln(ofstream& fout, const T& first, const Args&... args) {
    fout << first;
    ((fout << ' ' << args), ...);
    fout << '\n';
}

// ═══════════════════════════════════════════════════════════════
// ⚠️ 只看这里：改 mkin.h，别动 mkdata.cpp！
// ═══════════════════════════════════════════════════════════════

void test(int case_num, ofstream& fout)
{
    // ============================================================
    // Subtask 0: 样例数据（直接复制题目样例） — case 1-2
    // ============================================================
    if (case_num == 1)
    {
        // 样例 — 取自题面
        writeln(fout, 8, 8, 3);
        writeln(fout, 2);
        writeln(fout, 3, 4, 10);
        writeln(fout, 2, 3, 7);
        writeln(fout, 3);
        writeln(fout, 4, 3, 12);
        writeln(fout, 3, 2, 8);
        writeln(fout, 2, 4, 9);
        writeln(fout, 2);
        writeln(fout, 5, 5, 15);
        writeln(fout, 3, 3, 10);
    }
    else if (case_num == 2)
    {
        // 简易样例 — 2 家供应商，手动算
        // 甲: (2,2,5), (1,3,4); 乙: (3,1,6), (2,2,7)
        // 最优: (2,2,5)+(2,2,7)=(4,4,12) 或 (1,3,4)+(2,2,7)=(3,5,11)
        // 取 12
        writeln(fout, 5, 5, 2);
        writeln(fout, 2);
        writeln(fout, 2, 2, 5);
        writeln(fout, 1, 3, 4);
        writeln(fout, 2);
        writeln(fout, 3, 1, 6);
        writeln(fout, 2, 2, 7);
    }

    // ============================================================
    // Subtask 1: 小规模随机数据（最小 N，验证基本功能）— case 3-5
    // ============================================================
    else if (case_num >= 3 && case_num <= 5)
    {
        int W, V, G;
        if (case_num == 3) {
            W = 5; V = 5; G = 2;
        } else if (case_num == 4) {
            W = 8; V = 8; G = 3;
        } else {
            W = 10; V = 10; G = 5;
        }
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(1, 3);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = rnd(1, 20);
                writeln(fout, w, v, val);
            }
        }
    }

    // ============================================================
    // Subtask 1(续): 特殊性质数据 — case 6-8
    // ============================================================
    else if (case_num == 6)
    {
        // 特殊性质1：重量与体积相等（对角线约束 → 退化为 1D 背包）
        // 检验 DP 在 w=v 时结果是否合理（仅用对角线状态）
        int W = 15, V = 15, G = 6;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(2, 4);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int s = rnd(1, W);  // w == v
                int val = rnd(1, 30);
                writeln(fout, s, s, val);
            }
        }
    }
    else if (case_num == 7)
    {
        // 特殊性质2：每家只有 1 个方案 → 退化为 0/1 二维费用背包
        // 检验分组背包正确回退到普通 01 背包
        int W = 12, V = 12, G = 8;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            writeln(fout, 1);
            int w = rnd(1, W);
            int v = rnd(1, V);
            int val = rnd(1, 50);
            writeln(fout, w, v, val);
        }
    }
    else if (case_num == 8)
    {
        // 特殊性质3：所有方案的价值与其重量×体积成正比
        // 验证 DP 在"正比"场景下是否能自然选出高价值组合
        int W = 10, V = 10, G = 5;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(2, 4);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = w * v + rnd(0, 5);  // 价值与 w*v 线性相关
                writeln(fout, w, v, val);
            }
        }
    }

    // ============================================================
    // Subtask 2: Hack 数据（针对常见错误写法）— case 9-11
    // ============================================================
    else if (case_num == 9)
    {
        // Hack 1: 所有方案价值为零 → 答案必为 0
        // 针对：dp 初始化错误（如用 -1 标记不可达导致 max 无正解）
        int W = 8, V = 8, G = 4;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(2, 3);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                writeln(fout, w, v, 0);
            }
        }
    }
    else if (case_num == 10)
    {
        // Hack 2: 贪心陷阱 — 按价值/重量或价值/体积贪心会选错
        // 甲：(1,1,1)     — 单位价值很高但绝对价值低
        // 乙：(5,5,20)    — 单位价值低但绝对价值高
        // 若贪心选甲（逐个塞小的），得 4*1=4；正确选乙得 20
        int W = 5, V = 5, G = 2;
        writeln(fout, W, V, G);
        writeln(fout, 1);
        writeln(fout, 1, 1, 1);
        writeln(fout, 1);
        writeln(fout, 5, 5, 20);
    }
    else if (case_num == 11)
    {
        // Hack 3: 多维贪心陷阱 — 按价值/重量/体积三者权衡仍会错
        // 甲：(4,4,9)     — 每单位重或容价值为 2.25
        // 乙：(3,3,8)     — 每单位重或容价值 ≈ 2.67
        // 丙：(2,2,5)     — 每单位重或容价值 = 2.5
        // 贪心按"价值/kg+价值/L"排序会选乙+丙 = (5,5,13)
        // 正确答案：甲+丙 = (6,6,14) 权重虽低但总值更高
        // W=6,V=6: 甲+(4,4,9)+丙(2,2,5)=(6,6,14)
        // 乙+(3,3,8)+丙(2,2,5)=(5,5,13). 14 > 13.
        int W = 6, V = 6, G = 3;
        writeln(fout, W, V, G);
        writeln(fout, 1);
        writeln(fout, 4, 4, 9);
        writeln(fout, 1);
        writeln(fout, 3, 3, 8);
        writeln(fout, 1);
        writeln(fout, 2, 2, 5);
    }

    // ============================================================
    // Subtask 3: 中等规模数据（验证效率）— case 12-15
    // ============================================================
    else if (case_num >= 12 && case_num <= 15)
    {
        int W, V, G;
        if (case_num == 12) {
            W = 20; V = 20; G = 8;
        } else if (case_num == 13) {
            W = 25; V = 20; G = 10;
        } else if (case_num == 14) {
            W = 30; V = 25; G = 10;
        } else {
            W = 30; V = 30; G = 12;
        }
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(2, 5);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = rnd(1, 50);
                writeln(fout, w, v, val);
            }
        }
    }

    // ============================================================
    // Subtask 3(续): 大规模数据（压力测试）— case 16-20
    // ============================================================
    else if (case_num == 16)
    {
        // 80% 上限
        int W = 40, V = 40, G = 15;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(3, 7);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = rnd(1, 80);
                writeln(fout, w, v, val);
            }
        }
    }
    else if (case_num == 17)
    {
        // 80% 上限 — 不对称约束（重量大范围、体积小范围）
        int W = 50, V = 20, G = 15;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(3, 7);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = rnd(1, 80);
                writeln(fout, w, v, val);
            }
        }
    }
    else if (case_num == 18)
    {
        // 100% 上限
        int W = 50, V = 50, G = 20;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(4, 8);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = rnd(1, 100);
                writeln(fout, w, v, val);
            }
        }
    }
    else if (case_num == 19)
    {
        // 100% 上限 + 每组最大方案数（cnt=10）— 最大压力
        int W = 50, V = 50, G = 20;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            writeln(fout, 10);
            for (int i = 0; i < 10; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = rnd(1, 100);
                writeln(fout, w, v, val);
            }
        }
    }
    else if (case_num == 20)
    {
        // 上限 + 退化（所有方案重量=体积=20，价值递增）
        // 每组价值递增的方案，每个方案都需要 20×20 空间
        // 极限：最多选 2 个方案（50/20=2），测试 DP 在限制下的正确性
        int W = 50, V = 50, G = 20;
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            writeln(fout, 3);
            writeln(fout, 20, 20, 10 + g);
            writeln(fout, 30, 30, 30 + g);
            writeln(fout, 40, 40, 60 + g);
        }
    }

    // ============================================================
    // Subtask 4: 随机回归测试 — case 21-25
    // ============================================================
    else
    {
        // 全面随机，覆盖各种规模
        int W, V, G;
        if (case_num == 21) {
            W = 15; V = 10; G = 6;
        } else if (case_num == 22) {
            W = 10; V = 15; G = 6;
        } else if (case_num == 23) {
            W = 35; V = 35; G = 14;
        } else if (case_num == 24) {
            W = 45; V = 30; G = 18;
        } else {
            W = 50; V = 50; G = 20;
        }
        writeln(fout, W, V, G);
        for (int g = 0; g < G; g++) {
            int cnt = rnd(1, 8);
            writeln(fout, cnt);
            for (int i = 0; i < cnt; i++) {
                int w = rnd(1, W);
                int v = rnd(1, V);
                int val = rnd(1, 100);
                writeln(fout, w, v, val);
            }
        }
    }
}

#endif
