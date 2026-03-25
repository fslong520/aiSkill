#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1) {
        fout << "3\n";
    }
    else if (case_num == 2) {
        fout << "4\n";
    }
    else if (case_num == 3) {
        fout << "5\n";
    }
    else if (case_num == 4) {
        fout << "10\n";
    }
    else if (case_num == 5) {
        fout << "100\n";
    }
    else if (case_num == 6) {
        fout << "1000\n";
    }
    else if (case_num == 7) {
        fout << "10000\n";
    }
    else if (case_num == 8) {
        fout << "100000\n";
    }
    else if (case_num == 9) {
        fout << "1000000\n";
    }
    else if (case_num == 10) {
        fout << "1940500\n";
    }
    else if (case_num <= 15) {
        fout << case_num * 100 << "\n";
    }
    else {
        fout << case_num * 10000 << "\n";
    }
}

#endif