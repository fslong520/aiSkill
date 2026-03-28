#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1) {
        fout << "legal\n";
    }
    else if (case_num == 2) {
        fout << "atcoder\n";
    }
    else if (case_num == 3) {
        fout << "illegal\n";
    }
    else if (case_num == 4) {
        fout << "a\n";  // 长度1，不是5的倍数
    }
    else if (case_num == 5) {
        fout << "abcde\n";  // 长度5，是5的倍数
    }
    else if (case_num == 6) {
        fout << "abcdefghij\n";  // 长度10，是5的倍数
    }
    else if (case_num == 7) {
        fout << "abc\n";  // 长度3
    }
    else if (case_num == 8) {
        fout << "abcd\n";  // 长度4
    }
    else if (case_num == 9) {
        fout << "abcdefg\n";  // 长度7
    }
    else if (case_num == 10) {
        fout << "abcdefgh\n";  // 长度8
    }
    else {
        // 生成随机长度的字符串
        int len = (case_num % 10) + 1;
        for (int i = 0; i < len; i++) {
            fout << (char)('a' + (i % 26));
        }
        fout << "\n";
    }
}

#endif