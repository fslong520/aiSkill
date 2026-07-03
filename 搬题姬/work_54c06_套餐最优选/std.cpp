#include <iostream>
#include <algorithm>
#include <cstring>
using namespace std;

const int MAXM = 1005;
const int MAXC = 25;

// dp[j] = 预算j元能得到的最大满意度
int dp[MAXM];

// 每组套餐临时放这里
int w[MAXC], v[MAXC];

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, G;
    cin >> M >> G;

    // 一组一组套餐来看
    for (int g = 0; g < G; ++g) {
        int cnt;
        cin >> cnt;
        // 读入这组的所有套餐
        for (int i = 0; i < cnt; ++i)
            cin >> w[i] >> v[i];

        // 预算从高往低试，保证每组最多选一个
        for (int j = M; j >= 1; --j) {
            int best = dp[j];  // 这组啥也不选
            for (int i = 0; i < cnt; ++i)
                if (j >= w[i])
                    // 选了套餐i，剩下的钱从之前几组的结果里取
                    best = max(best, dp[j - w[i]] + v[i]);
            dp[j] = best;
        }
    }

    cout << dp[M] << '\n';
    return 0;
}
