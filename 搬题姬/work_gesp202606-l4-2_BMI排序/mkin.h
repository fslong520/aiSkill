#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

struct SubtaskDef {
    int id, start, end;
};
const SubtaskDef SUBTASKS[] = {
    {0, 1, 2},
    {1, 3, 8},
    {2, 9, 11},
    {3, 12, 20},
    {4, 21, 25},
};
const int SUBTASK_COUNT = sizeof(SUBTASKS) / sizeof(SUBTASKS[0]);

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

int rand_int(int l, int r) {
    return uniform_int_distribution<int>(l, r)(rng);
}

double rand_double(double l, double r) {
    return uniform_real_distribution<double>(l, r)(rng);
}

void output_case(int n, const vector<int>& w, const vector<double>& h, ofstream& fout) {
    fout << n << "\n";
    for (int i = 0; i < n; i++) {
        if (i) fout << ' ';
        fout << w[i];
    }
    fout << "\n";
    for (int i = 0; i < n; i++) {
        if (i) fout << ' ';
        fout << fixed << setprecision(2) << h[i];
    }
    fout << "\n";
}

void test(int case_num, ofstream& fout)
{
    if (case_num == 1)
    {
        vector<int> w = {60, 80, 50, 70};
        vector<double> h = {1.50, 1.60, 1.40, 1.50};
        output_case(4, w, h, fout);
    }
    else if (case_num == 2)
    {
        vector<int> w = {100, 50, 75};
        vector<double> h = {1.80, 1.60, 1.70};
        output_case(3, w, h, fout);
    }

    else if (case_num == 3)
    {
        output_case(1, {60}, {1.50}, fout);
    }
    else if (case_num == 4)
    {
        output_case(2, {70, 70}, {1.70, 1.70}, fout);
    }
    else if (case_num == 5)
    {
        output_case(5, {100, 90, 80, 70, 60}, {1.50, 1.50, 1.50, 1.50, 1.50}, fout);
    }
    else if (case_num == 6)
    {
        output_case(5, {60, 70, 80, 90, 100}, {1.50, 1.50, 1.50, 1.50, 1.50}, fout);
    }
    else if (case_num == 7)
    {
        int n = 10;
        vector<int> w(n, 60);
        vector<double> h(n, 1.50);
        output_case(n, w, h, fout);
    }
    else if (case_num == 8)
    {
        output_case(2, {200, 1}, {1.00, 2.00}, fout);
    }

    else if (case_num == 9)
    {
        int n = 1000;
        vector<int> w(n, 60);
        vector<double> h(n, 1.50);
        output_case(n, w, h, fout);
    }
    else if (case_num == 10)
    {
        int n = 1000;
        vector<int> w(n);
        vector<double> h(n, 1.50);
        for (int i = 0; i < n; i++) w[i] = n - i;
        output_case(n, w, h, fout);
    }
    else if (case_num == 11)
    {
        int n = 1000;
        vector<int> w(n);
        vector<double> h(n);
        for (int i = 0; i < n; i++) {
            w[i] = rand_int(1, 200);
            h[i] = rand_double(1.0, 2.0);
        }
        output_case(n, w, h, fout);
    }

    else if (case_num >= 12 && case_num <= 15)
    {
        int n = 50 + (case_num - 12) * 50;
        vector<int> w(n);
        vector<double> h(n);
        for (int i = 0; i < n; i++) {
            w[i] = rand_int(1, 200);
            h[i] = rand_double(1.0, 2.0);
        }
        output_case(n, w, h, fout);
    }
    else if (case_num >= 16 && case_num <= 20)
    {
        int n = 500 + (case_num - 16) * 125;
        vector<int> w(n);
        vector<double> h(n);
        for (int i = 0; i < n; i++) {
            w[i] = rand_int(1, 200);
            h[i] = rand_double(1.0, 2.0);
        }
        output_case(n, w, h, fout);
    }

    else
    {
        int n = 100 + rand_int(0, 900);
        vector<int> w(n);
        vector<double> h(n);
        for (int i = 0; i < n; i++) {
            w[i] = rand_int(1, 200);
            h[i] = rand_double(1.0, 2.0);
        }
        output_case(n, w, h, fout);
    }
}

#endif
