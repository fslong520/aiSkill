#include <iostream>
#include <algorithm>
#include <cstring>
using namespace std;

const int MAXM = 1005;
const int MAXC = 15;

// dp[j] = 预算j元能拿到的最大满意度
int dp[MAXM];
int w[MAXC], v[MAXC];

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, G;
    cin >> M >> G;

    // 一个一个社团来看
    for (int g = 0; g < G; ++g) {
        int cnt;
        cin >> cnt;
        // 读入这个社团的所有方案
        for (int i = 0; i < cnt; ++i)
            cin >> w[i] >> v[i];

        // 预算从高往低试——保证每个社团最多选一个方案
        for (int j = M; j >= 0; --j) {
            int best = dp[j];  // 不选这个社团的任何方案
            for (int i = 0; i < cnt; ++i)
                if (j >= w[i])
                    // 如果选了方案i，剩下的钱 j-w[i] 从之前社团的结果里取
                    best = max(best, dp[j - w[i]] + v[i]);
            dp[j] = best;
        }
    }

    cout << dp[M] << "\n";
    return 0;
}
