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
//   case 1:    样例数据（Hello）
//   case 2-3:  边界单字符（'a', 'A'）
//   case 4-5:  大小写混合边界（aA, zZ）
//   case 6:    全小写字母表
//   case 7:    全大写字母表
//   case 8:    大小写交替
//   case 9:    长全小写（长度1000）
//   case 10-15:随机大小写（短串）
//   case 16-20:随机大小写（长串）
//   case 21-25:随机长短
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

void test(int case_num, ofstream& fout)
{
    if (case_num == 1) { fout << "Hello" << endl; }
    else if (case_num == 2) { fout << "a" << endl; }
    else if (case_num == 3) { fout << "A" << endl; }
    else if (case_num == 4) { fout << "aA" << endl; }
    else if (case_num == 5) { fout << "zZ" << endl; }
    else if (case_num == 6) { fout << "abcdefghijklmnopqrstuvwxyz" << endl; }
    else if (case_num == 7) { fout << "ABCDEFGHIJKLMNOPQRSTUVWXYZ" << endl; }
    else if (case_num == 8) { fout << "AbCdEf" << endl; }
    else if (case_num == 9) {
        string s; for (int i = 0; i < 1000; i++) s += 'a' + rand() % 26;
        fout << s << endl;
    }
    else if (case_num >= 10 && case_num <= 15) {
        int len = 10 + rand() % 50;
        string s;
        for (int i = 0; i < len; i++)
            s += (rand() % 2) ? ('a' + rand() % 26) : ('A' + rand() % 26);
        fout << s << endl;
    }
    else if (case_num >= 16 && case_num <= 20) {
        int len = 500 + rand() % 501;
        string s;
        for (int i = 0; i < len; i++)
            s += (rand() % 2) ? ('a' + rand() % 26) : ('A' + rand() % 26);
        fout << s << endl;
    }
    else {
        int len = 1 + rand() % 100;
        string s;
        for (int i = 0; i < len; i++)
            s += (rand() % 2) ? ('a' + rand() % 26) : ('A' + rand() % 26);
        fout << s << endl;
    }
}

#endif
