#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1) {
        fout << "5 4\n1 2\n2 1\n3 1\n2 2\n2 4\n";
    }
    else if (case_num == 2) {
        fout << "10 5\n3 2\n3 4\n1 2\n2 2\n4 4\n3 1\n3 4\n4 2\n3 3\n3 2\n";
    }
    else if (case_num == 3) {
        fout << "1 1\n1 1\n";
    }
    else if (case_num == 4) {
        fout << "1 5\n3 4\n";
    }
    else if (case_num == 5) {
        fout << "3 3\n1 2\n2 3\n3 1\n";
    }
    else if (case_num == 6) {
        fout << "100 100\n";
        for (int i = 0; i < 100; i++) {
            fout << (i % 100 + 1) << " " << ((i + 1) % 100 + 1) << "\n";
        }
    }
    else if (case_num == 7) {
        fout << "50 10\n";
        for (int i = 0; i < 50; i++) {
            fout << (i % 10 + 1) << " " << ((i + 5) % 10 + 1) << "\n";
        }
    }
    else if (case_num == 8) {
        fout << "20 5\n";
        for (int i = 0; i < 20; i++) {
            fout << 1 << " " << 5 << "\n";
        }
    }
    else if (case_num == 9) {
        fout << "10 20\n";
        for (int i = 0; i < 10; i++) {
            fout << (i + 1) << " " << (i + 11) << "\n";
        }
    }
    else if (case_num == 10) {
        fout << "100 1\n";
        for (int i = 0; i < 100; i++) {
            fout << 1 << " " << 1 << "\n";
        }
    }
    else {
        int n = 10 + case_num;
        int m = 5 + case_num % 10;
        fout << n << " " << m << "\n";
        for (int i = 0; i < n; i++) {
            int a = (i % m) + 1;
            int b = ((i + case_num) % m) + 1;
            fout << a << " " << b << "\n";
        }
    }
}

#endif