#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1) {
        fout << "4\n2 5 4\n3 2\n5\n";
    }
    else if (case_num == 2) {
        fout << "4\n2 5 4\n3 2\n6\n";
    }
    else if (case_num == 3) {
        fout << "10\n1039 1802 3781 231 5828 1944 392 262 1481\n763 2742 1270 4789 905 1431 1301 442\n1979 2033 5552 142 2194 2064 1205\n4012 7531 2121 4173 4043 3184\n6059 2175 161 493 1712\n5694 6220 6090 5231\n2336 2206 1347\n654 1873\n1743\n";
    }
    else if (case_num == 4) {
        fout << "2\n5\n";
    }
    else if (case_num == 5) {
        fout << "3\n1 2\n3\n";
    }
    else if (case_num == 6) {
        fout << "5\n1 2 3 4\n1 2 3\n1 2\n1\n";
    }
    else if (case_num == 7) {
        // 不满足三角不等式
        fout << "3\n1 10\n1\n";
    }
    else if (case_num == 8) {
        fout << "6\n1 2 3 4 5\n1 2 3 4\n1 2 3\n1 2\n1\n";
    }
    else if (case_num == 9) {
        fout << "10\n";
        for (int i = 0; i < 9; i++) {
            for (int j = i + 1; j < 10; j++) {
                fout << (abs(i - j) + 1) << " ";
            }
            fout << "\n";
        }
    }
    else if (case_num == 10) {
        fout << "20\n";
        for (int i = 0; i < 19; i++) {
            for (int j = i + 1; j < 20; j++) {
                fout << (abs(i - j) * 2 + 1) << " ";
            }
            fout << "\n";
        }
    }
    else {
        int n = 5 + case_num;
        fout << n << "\n";
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                fout << (abs(i - j) + 1) << " ";
            }
            fout << "\n";
        }
    }
}

#endif