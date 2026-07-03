#include <iostream>
#include <algorithm>
#include <cstring>
using namespace std;

const int MAXW = 105;
const int MAXV = 105;

// dp[j][k] = 重量不超过j、体积不超过k时的最大价值
int dp[MAXW][MAXV];
int w[105], v[105], val[105];

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int W, V, N;
    cin >> W >> V >> N;
    for (int i = 1; i <= N; ++i)
        cin >> w[i] >> v[i] >> val[i];

    // 挨个物品试，看能不能塞进背包
    for (int i = 1; i <= N; ++i)
        // 重量和体积都倒序遍历——保证每件物品只拿一次（01背包）
        for (int j = W; j >= w[i]; --j)
            for (int k = V; k >= v[i]; --k)
                // 不拿 vs 拿了这件
                dp[j][k] = max(dp[j][k], dp[j - w[i]][k - v[i]] + val[i]);

    cout << dp[W][V] << '\n';
    return 0;
}
