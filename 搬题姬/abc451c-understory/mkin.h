#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1) {
        fout << "5\n1 5\n1 7\n1 8\n2 7\n1 3\n";
    }
    else if (case_num == 2) {
        fout << "12\n2 256601193\n1 85138616\n1 202564041\n2 276477192\n1 55551662\n1 170271057\n2 754166580\n1 854388209\n1 772036624\n2 651124113\n1 301137866\n2 290875185\n";
    }
    else if (case_num == 3) {
        fout << "3\n1 1\n1 1\n2 1\n";
    }
    else if (case_num == 4) {
        fout << "1\n1 1000000000\n";
    }
    else if (case_num == 5) {
        fout << "1\n2 1\n";
    }
    else if (case_num == 6) {
        fout << "10\n";
        for (int i = 1; i <= 10; i++) {
            fout << "1 " << i << "\n";
        }
    }
    else if (case_num == 7) {
        fout << "10\n";
        for (int i = 1; i <= 10; i++) {
            fout << "1 " << (i * 100) << "\n";
        }
        fout << "2 500\n";
    }
    else if (case_num == 8) {
        fout << "20\n";
        for (int i = 1; i <= 20; i++) {
            fout << "1 " << (1000000000 - i) << "\n";
        }
    }
    else if (case_num == 9) {
        fout << "100\n";
        for (int i = 1; i <= 100; i++) {
            fout << "1 " << i << "\n";
        }
        for (int i = 1; i <= 50; i++) {
            fout << "2 " << i << "\n";
        }
    }
    else if (case_num == 10) {
        fout << "300000\n";
        for (int i = 1; i <= 300000; i++) {
            fout << "1 " << (i % 1000000000 + 1) << "\n";
        }
    }
    else {
        int q = 100 + case_num * 1000;
        fout << q << "\n";
        for (int i = 1; i <= q; i++) {
            int type = (i % 3 == 0) ? 2 : 1;
            int h = (i * 100) % 1000000000 + 1;
            fout << type << " " << h << "\n";
        }
    }
}

#endif