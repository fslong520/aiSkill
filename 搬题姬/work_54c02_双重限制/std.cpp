#include <iostream>
#include <algorithm>
#include <cstring>
using namespace std;

const int MAXN = 305;

// dp[j][k] = 载重j、容积k以内的最大价值
int dp[MAXN][MAXN];

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int W, V, N;
    cin >> W >> V >> N;

    // 每件家具试试能不能装
    for (int i = 0; i < N; i++) {
        int w, v, p;
        cin >> w >> v >> p;
        // 倒序：保证每件最多选一次
        for (int j = W; j >= w; j--)
            for (int k = V; k >= v; k--)
                // 不装 vs 装进去
                dp[j][k] = max(dp[j][k], dp[j - w][k - v] + p);
    }

    cout << dp[W][V] << endl;
    return 0;
}
