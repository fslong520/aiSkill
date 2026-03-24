#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1)
    {
        fout << "5 6" << endl;
        fout << "1 2 3 4 5" << endl;
        fout << "2 3" << endl;
        fout << "1 2 10" << endl;
        fout << "2 5" << endl;
        fout << "1 1 1" << endl;
        fout << "2 1" << endl;
        fout << "2 4" << endl;
    }
    else if (case_num == 2)
    {
        fout << "4 7" << endl;
        fout << "5 1 4 2" << endl;
        fout << "1 4 7" << endl;
        fout << "2 4" << endl;
        fout << "1 3 2" << endl;
        fout << "2 2" << endl;
        fout << "1 1 5" << endl;
        fout << "2 3" << endl;
        fout << "2 1" << endl;
    }
    else if (case_num == 3)
    {
        fout << "12 10" << endl;
        fout << "3 1 4 1 5 9 2 6 5 3 5 8" << endl;
        fout << "2 6" << endl;
        fout << "1 3 4" << endl;
        fout << "2 12" << endl;
        fout << "1 5 7" << endl;
        fout << "2 10" << endl;
        fout << "1 2 1" << endl;
        fout << "1 12 100" << endl;
        fout << "2 12" << endl;
        fout << "2 1" << endl;
        fout << "2 11" << endl;
    }
    else if (case_num == 4)
    {
        fout << "20 14" << endl;
        fout << "10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200" << endl;
        fout << "2 20" << endl;
        fout << "1 4 25" << endl;
        fout << "1 6 10" << endl;
        fout << "2 12" << endl;
        fout << "1 1 3" << endl;
        fout << "2 5" << endl;
        fout << "1 10 100" << endl;
        fout << "2 20" << endl;
        fout << "1 7 8" << endl;
        fout << "1 20 50" << endl;
        fout << "2 19" << endl;
        fout << "2 20" << endl;
        fout << "1 3 6" << endl;
        fout << "2 18" << endl;
    }
    else if (case_num == 5)
    {
        fout << "1 4" << endl;
        fout << "1000000000" << endl;
        fout << "2 1" << endl;
        fout << "1 1 1000000000" << endl;
        fout << "2 1" << endl;
        fout << "2 1" << endl;
    }
    else if (case_num >= 6 && case_num <= 15)
    {
        int n = 10 + (case_num - 6) * 10;
        int q = 5 + (case_num - 6);
        fout << n << " " << q << endl;
        for (int i = 1; i <= n; i++) fout << i << " ";
        fout << endl;
        for (int i = 0; i < q; i++) {
            if (i % 2 == 0) {
                fout << "2 " << (1 + i * n / q) << endl;
            } else {
                fout << "1 " << (1 + i % n) << " " << (i + 1) * 10 << endl;
            }
        }
    }
    else
    {
        int n = 50 + (case_num - 16) * 10;
        int q = 10 + (case_num - 16);
        fout << n << " " << q << endl;
        for (int i = 1; i <= n; i++) fout << (i % 100 + 1) << " ";
        fout << endl;
        for (int i = 0; i < q; i++) {
            if (i % 3 == 0) {
                fout << "2 " << (1 + i * n / q) << endl;
            } else {
                fout << "1 " << (1 + i % (n/2)) << " " << (i + 1) * 5 << endl;
            }
        }
    }
}

#endif