#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long a;
    cin >> a;

    // 数学推导：1~k-1 的和 = k+1~n 的和
    // (k-1)*k/2 = n*(n+1)/2 - k*(k+1)/2
    // 化简得：2k² = n(n+1)
    // 即：n² + n - 2k² = 0
    // 求根公式：n = (-1 + √(1+8k²)) / 2

    for (long long k = a; ; k++) {
        long long d = 1 + 8 * k * k;
        long long sqrt_d = sqrt(d);
        if (sqrt_d * sqrt_d == d) {
            // 验证 n 是正整数
            if ((sqrt_d - 1) % 2 == 0) {
                long long n = (sqrt_d - 1) / 2;
                if (n > k) {
                    cout << k << " " << n << endl;
                    return 0;
                }
            }
        }
    }

    return 0;
}