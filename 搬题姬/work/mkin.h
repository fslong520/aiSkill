#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout) {
    // 第1-2组: 样例
    if (case_num == 1) {
        fout << "7\n";
        fout << "ooparts\n";
    } else if (case_num == 2) {
        fout << "6\n";
        fout << "abcooo\n";
    }
    
    // 第3-5组: 小规模
    else if (case_num == 3) {
        fout << "5\n";
        fout << "ooooo\n";
    } else if (case_num == 4) {
        fout << "1\n";
        fout << "o\n";
    } else if (case_num == 5) {
        fout << "1\n";
        fout << "a\n";
    }
    
    // 第6-10组: 中等规模
    else if (case_num == 6) {
        fout << "10\n";
        fout << "ooabcdefgh\n";
    } else if (case_num == 7) {
        fout << "15\n";
        fout << "abcdefghijklmno\n";
    } else if (case_num == 8) {
        fout << "20\n";
        fout << "oooooxxxxxooooooooo\n";
    } else if (case_num == 9) {
        fout << "25\n";
        fout << "xoooooooooooooooooooooo\n";
    } else if (case_num == 10) {
        fout << "30\n";
        fout << "oooooooooooooooooooooooxxx\n";
    }
    
    // 第11-15组: 大规模
    else if (case_num == 11) {
        fout << "35\n";
        fout << "ooooooooooabcdefghijklmnopqrstuvwxyz\n";
    } else if (case_num == 12) {
        fout << "40\n";
        fout << "abcdefghijklmnopqrstuvwxyzabcdefghij\n";
    } else if (case_num == 13) {
        fout << "45\n";
        fout << "ooooooooooooooooooooooooooooooooooooox\n";
    } else if (case_num == 14) {
        fout << "50\n";
        fout << "oooooooooooooooooooooooooooooooooooooooooo\n";
    } else if (case_num == 15) {
        fout << "50\n";
        fout << "xooooooooooooooooooooooooooooooooooooooooo\n";
    }
    
    // 第16-20组: 边界情况
    else if (case_num == 16) {
        fout << "2\n";
        fout << "oa\n";
    } else if (case_num == 17) {
        fout << "2\n";
        fout << "ao\n";
    } else if (case_num == 18) {
        fout << "3\n";
        fout << "oox\n";
    } else if (case_num == 19) {
        fout << "3\n";
        fout << "oxo\n";
    } else if (case_num == 20) {
        fout << "3\n";
        fout << "xoo\n";
    }
    
    // 第21-25组: 随机压力
    else {
        int len = rand() % 50 + 1;
        int leading_o = rand() % (len + 1);
        string s;
        for (int j = 0; j < leading_o; j++) {
            s += 'o';
        }
        for (int j = leading_o; j < len; j++) {
            if (j == leading_o && leading_o < len) {
                s += 'a' + (rand() % 14); // 保证第一个非o不是o
            } else {
                s += 'a' + (rand() % 26);
            }
        }
        fout << len << "\n";
        fout << s << "\n";
    }
}

#endif
