#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    cin >> n;

    // 预处理所有2的幂次及其字符串长度
    vector<pair<long long, int>> powers;
    for (long long p = 1; p <= 1000000000LL; p *= 2) {
        powers.push_back({p, (int)to_string(p).length()});
    }

    // 计算拼接后的数值
    auto concat = [](long long a, long long b, int b_len) -> long long {
        long long factor = 1;
        for (int i = 0; i < b_len; i++) factor *= 10;
        return a * factor + b;
    };

    set<long long> visited;
    priority_queue<long long, vector<long long>, greater<long long>> pq;

    // 初始化：所有单个2的幂次
    for (auto& [p, len] : powers) {
        pq.push(p);
        visited.insert(p);
    }

    long long ans = 0;
    for (long long i = 0; i < n; i++) {
        ans = pq.top();
        pq.pop();

        // 生成所有可能的扩展
        for (auto& [p, len] : powers) {
            long long next = concat(ans, p, len);
            if (next <= 1000000000LL && visited.find(next) == visited.end()) {
                visited.insert(next);
                pq.push(next);
            }
        }
    }

    cout << ans << '\n';

    return 0;
}