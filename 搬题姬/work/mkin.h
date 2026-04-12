#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

void gen_grid(int H, int W, char S_start, char S_end, ofstream& fout) {
    vector<string> grid(H, string(W, '.'));
    int sr, sc, gr, gc;
    // Random S
    sr = rand() % H; sc = rand() % W;
    grid[sr][sc] = S_start;
    // Random G (different from S)
    do {
        gr = rand() % H; gc = rand() % W;
    } while (gr == sr && gc == sc);
    grid[gr][gc] = S_end;

    for(int i=0; i<H; ++i) {
        for(int j=0; j<W; ++j) {
            if(grid[i][j] == '.') {
                int r = rand() % 100;
                if(r < 20) grid[i][j] = '#';
                else if(r < 30) grid[i][j] = 'o';
                else if(r < 40) grid[i][j] = 'x';
            }
        }
    }
    fout << H << " " << W << endl;
    for(int i=0; i<H; ++i) fout << grid[i] << endl;
}

void test(int case_num, ofstream& fout)
{
    if (case_num == 1)
    {
        // 样例1
        fout << "4 6" << endl;
        fout << "S....G" << endl;
        fout << "##.###" << endl;
        fout << "#o#o#x" << endl;
        fout << "..#x.." << endl;
    }
    else if (case_num == 2)
    {
        // 样例2
        fout << "4 7" << endl;
        fout << "...#..." << endl;
        fout << ".#.#.#." << endl;
        fout << ".SoGxG." << endl;
        fout << ".#.#.#." << endl;
    }
    else if (case_num >= 3 && case_num <= 5)
    {
        // 小规模测试
        int H = rand() % 5 + 2;
        int W = rand() % 5 + 2;
        gen_grid(H, W, 'S', 'G', fout);
    }
    else if (case_num >= 6 && case_num <= 10)
    {
        // 中等规模
        int H = rand() % 20 + 10;
        int W = rand() % 20 + 10;
        gen_grid(H, W, 'S', 'G', fout);
    }
    else if (case_num >= 11 && case_num <= 15)
    {
        // 大规模
        int H = rand() % 50 + 50;
        int W = rand() % 50 + 50;
        gen_grid(H, W, 'S', 'G', fout);
    }
    else if (case_num >= 16 && case_num <= 20)
    {
        // 特大规模 (up to 1000)
        int H = rand() % 500 + 200;
        int W = rand() % 500 + 200;
        gen_grid(H, W, 'S', 'G', fout);
    }
    else if (case_num >= 21 && case_num <= 25)
    {
        // 压力测试 (up to 1000x1000)
        int H = rand() % 500 + 500;
        int W = rand() % 500 + 500;
        gen_grid(H, W, 'S', 'G', fout);
    }
}

#endif // MKIN_H
