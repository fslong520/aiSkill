#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void test(int case_num, ofstream& fout)
{
    if (case_num == 1) {
        fout << "10\n";
    }
    else if (case_num == 2) {
        fout << "69\n";
    }
    else if (case_num == 3) {
        fout << "1\n";
    }
    else if (case_num == 4) {
        fout << "2\n";
    }
    else if (case_num == 5) {
        fout << "5\n";
    }
    else if (case_num == 6) {
        fout << "20\n";
    }
    else if (case_num == 7) {
        fout << "50\n";
    }
    else if (case_num == 8) {
        fout << "100\n";
    }
    else if (case_num == 9) {
        fout << "200\n";
    }
    else if (case_num == 10) {
        fout << "500\n";
    }
    else if (case_num == 11) {
        fout << "1000\n";
    }
    else if (case_num == 12) {
        fout << "2000\n";
    }
    else if (case_num == 13) {
        fout << "5000\n";
    }
    else if (case_num == 14) {
        fout << "10000\n";
    }
    else if (case_num == 15) {
        fout << "20000\n";
    }
    else {
        fout << case_num * 100 << "\n";
    }
}

#endif