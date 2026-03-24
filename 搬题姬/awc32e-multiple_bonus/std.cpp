#include <iostream>
#include <cmath>
#define endl '\n'
#define int long long
using namespace std;

const int MAXN = 200005;

int N, Q, B;
int lazy_add[505];
int bit[MAXN];

void bit_add(int i, int v) {
    for (; i <= N; i += i & (-i))
        bit[i] += v;
}

int bit_sum(int i) {
    int s = 0;
    for (; i > 0; i -= i & (-i))
        s += bit[i];
    return s;
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> Q;
    B = (int)sqrt(N) + 1;

    for (int i = 1; i <= N; i++) {
        int s;
        cin >> s;
        bit_add(i, s);
    }

    while (Q--) {
        int op;
        cin >> op;

        if (op == 1) {
            int k, v;
            cin >> k >> v;

            if (k <= B) {
                lazy_add[k] += v;
            } else {
                for (int j = k; j <= N; j += k) {
                    bit_add(j, v);
                }
            }
        } else {
            int x;
            cin >> x;

            int ans = bit_sum(x);

            for (int k = 1; k <= B; k++) {
                if (lazy_add[k] == 0) continue;
                ans += lazy_add[k] * (x / k);
            }

            cout << ans << '\n';
        }
    }

    return 0;
}