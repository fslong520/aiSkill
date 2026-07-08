#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int N = 1005;
struct node {
    int id;
    ll w;
    ll h;  // height in cm
} a[N];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i].w;
        a[i].id = i;
    }
    for (int i = 1; i <= n; i++) {
        double x;
        cin >> x;
        a[i].h = (ll)(x * 100 + 0.5);  // m -> cm, round
    }

    sort(a + 1, a + n + 1, [](const node &x, const node &y) {
        // BMI = w/h^2
        // compare x.w / x.h^2 > y.w / y.h^2
        // <=> x.w * y.h * y.h > y.w * x.h * x.h
        ll lhs = x.w * y.h * y.h;
        ll rhs = y.w * x.h * x.h;
        if (lhs != rhs) return lhs > rhs;
        return x.id < y.id;
    });

    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << a[i].id;
    }
    cout << '\n';

    return 0;
}
