#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

// ═══════════════════════════════════════════════════════════════════
// 总测试点数量 & 测试类型注释
// ═══════════════════════════════════════════════════════════════════
// 25 组测试点，无 subtask 分组，每点独立计分
// 
// 测试类型分布（仅供注释参考）：
//   case 1-2:  样例数据
//   case 3-8:  小规模 + 特殊性质
//   case 9-11: Hack 数据
//   case 12-20: 中大规模
//   case 21-25: 随机回归
// ═══════════════════════════════════════════════════════════════════

const int TEST_CASES = 25;

// ═══════════════════════════════════════════════════════════════
// ⚠️ 只看这里：改 mkin.h，别动 mkdata.cpp！
// ═══════════════════════════════════════════════════════════════
// 
// ✅ 改这个文件（mkin.h）里的 test() 函数
// ❌ 别动 mkdata.cpp（框架代码，不需要改）
//
// 测试数据说明（25组，无分组，每点独立计分）：
// ═══════════════════════════════════════════════════════════════

/**
 * 测试数据生成函数
 * 
 * 参数：
 *   case_num: 测试点编号（1-25）
 *   fout: 输出文件流（写入 .in 文件）
 * 
 * 特殊性质数据设计参考：
 *   - 单调性：递增/递减序列，测试排序、二分等算法
 *   - 所有值相同：测试重复值处理
 *   - 极值：最大/最小可能值，测试溢出
 * 
 * Hack 数据设计参考：
 *   - int 溢出：使用 > 2^31-1 的数据，使 int 错误
 *   - 边界漏判：N=1, N=max 等，测试边界处理
 *   - 超时：使 O(n²) 算法超时
 *   - 错误贪心：使贪心策略失败的数据
 */

void test(int case_num, ofstream& fout)
{
    // 1-2: 样例
    if (case_num == 1) { fout << "23 5" << endl; }
    else if (case_num == 2) { fout << "10 3" << endl; }
    // 3-8: 小规模+特殊性质
    else if (case_num == 3) { fout << "1 1" << endl; }
    else if (case_num == 4) { fout << "10000 1" << endl; }
    else if (case_num == 5) { fout << "10000 10000" << endl; }
    else if (case_num == 6) { fout << "2 2" << endl; }
    else if (case_num == 7) { fout << "9999 5000" << endl; }
    else if (case_num == 8) { fout << "10000 9999" << endl; }
    // 9-11: Hack
    else if (case_num == 9) { fout << "1 1" << endl; }
    else if (case_num == 10) { fout << "9999 1" << endl; }
    else if (case_num == 11) { fout << "10000 5000" << endl; }
    // 12-20: 中大规模
    else if (case_num >= 12 && case_num <= 15) {
        int n = rand() % 4900 + 100;
        int k = rand() % n + 1;
        fout << n << " " << k << endl;
    }
    else if (case_num >= 16 && case_num <= 20) {
        int n = rand() % 5001 + 5000;
        int k = rand() % n + 1;
        fout << n << " " << k << endl;
    }
    // 21-25: 随机回归
    else {
        int n = rand() % 10000 + 1;
        int k = rand() % n + 1;
        fout << n << " " << k << endl;
    }
}

#endif
