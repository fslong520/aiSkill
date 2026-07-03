#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int MAXC = 15;

// 读入每个供应商的方案，临时存一下
int w[MAXC], v[MAXC], val[MAXC];

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int W, V, G;
    cin >> W >> V >> G;

    // dp[iw][iv] = 重量iw、体积iv以内的最大价值
    vector<vector<int>> dp(W + 1, vector<int>(V + 1, 0));

    // 一个供应商一个供应商地处理
    for (int g = 0; g < G; g++) {
        int cnt;
        cin >> cnt;
        for (int i = 0; i < cnt; i++)
            cin >> w[i] >> v[i] >> val[i];

        // 先记下选这个供应商之前的状态
        vector<vector<int>> prev = dp;

        // 在不超过限重限容的前提下，试着从这个供应商里挑一个方案
        for (int iw = W; iw >= 0; iw--)
            for (int iv = V; iv >= 0; iv--)
                for (int i = 0; i < cnt; i++)
                    if (iw >= w[i] && iv >= v[i]) {
                        // 如果选方案i，剩下的重量和体积用之前的结果
                        int cand = prev[iw - w[i]][iv - v[i]] + val[i];
                        if (cand > dp[iw][iv])
                            dp[iw][iv] = cand;
                    }
    }

    cout << dp[W][V] << '\n';
    return 0;
}
