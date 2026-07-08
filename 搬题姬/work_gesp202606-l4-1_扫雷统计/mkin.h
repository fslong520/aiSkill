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

void test(int case_num, ofstream& fout)
{
    if (case_num == 1)
    {
        fout << "3 3 2\n1 1\n3 3\n";
    }
    else if (case_num == 2)
    {
        fout << "4 5 4\n1 1\n1 5\n4 1\n4 5\n";
    }

    else if (case_num == 3)
    {
        fout << "1 1 1\n1 1\n";
    }
    else if (case_num == 4)
    {
        // 单行，无雷
        fout << "1 5 0\n";
    }
    else if (case_num == 5)
    {
        // 单列，3雷
        fout << "5 1 3\n1 1\n3 1\n5 1\n";
    }
    else if (case_num == 6)
    {
        // 全铺满
        int n = 5, m = 5;
        fout << n << " " << m << " " << n * m << "\n";
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                fout << i << " " << j << "\n";
    }
    else if (case_num == 7)
    {
        // 只有1雷在角落
        fout << "10 10 1\n10 10\n";
    }
    else if (case_num == 8)
    {
        // 棋盘格分布
        int n = 6, m = 6;
        fout << n << " " << m << " " << 18 << "\n";
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                if ((i + j) % 2 == 0)
                    fout << i << " " << j << "\n";
    }

    else if (case_num == 9)
    {
        // Hack: 500x500 全雷
        int n = 500, m = 500;
        fout << n << " " << m << " " << n * m << "\n";
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                fout << i << " " << j << "\n";
    }
    else if (case_num == 10)
    {
        // Hack: 500x500 仅1雷
        fout << "500 500 1\n250 250\n";
    }
    else if (case_num == 11)
    {
        // Hack: 500x500 边界布满
        int n = 500, m = 500;
        vector<pair<int,int>> mines;
        for (int i = 1; i <= n; i++) {
            mines.push_back({i, 1});
            mines.push_back({i, m});
        }
        for (int j = 2; j < m; j++) {
            mines.push_back({1, j});
            mines.push_back({n, j});
        }
        fout << n << " " << m << " " << mines.size() << "\n";
        for (auto &p : mines)
            fout << p.first << " " << p.second << "\n";
    }

    else if (case_num == 12)
    {
        int n = 50, m = 50, q = 100;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 13)
    {
        int n = 100, m = 100, q = 500;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 14)
    {
        int n = 100, m = 100, q = 2000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 15)
    {
        int n = 200, m = 200, q = 1000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 16)
    {
        int n = 300, m = 300, q = 5000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 17)
    {
        int n = 400, m = 400, q = 20000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 18)
    {
        int n = 500, m = 500, q = 50000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 19)
    {
        int n = 500, m = 500, q = 2000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 20)
    {
        // 500x500 半数雷
        int n = 500, m = 500;
        vector<pair<int,int>> mines;
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++)
                if ((i + j) % 2 == 0)
                    mines.push_back({i, j});
        fout << n << " " << m << " " << mines.size() << "\n";
        for (auto &p : mines)
            fout << p.first << " " << p.second << "\n";
    }

    else if (case_num == 21)
    {
        int n = 250, m = 250, q = 5000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 22)
    {
        int n = 400, m = 400, q = 10000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 23)
    {
        int n = 500, m = 500, q = 100000;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else if (case_num == 24)
    {
        // 10x500 稀疏
        int n = 10, m = 500, q = 200;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
    else
    {
        // 500x10 稀疏
        int n = 500, m = 10, q = 200;
        fout << n << " " << m << " " << q << "\n";
        set<pair<int,int>> used;
        for (int i = 0; i < q; ) {
            int x = rand_int(1, n), y = rand_int(1, m);
            if (used.insert({x, y}).second) {
                fout << x << " " << y << "\n";
                i++;
            }
        }
    }
}

#endif
