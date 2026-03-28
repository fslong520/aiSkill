#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<int> cntA(m + 1, 0), cntB(m + 1, 0);

    for (int i = 0; i < n; i++) {
        int a, b;
        cin >> a >> b;
        cntA[a]++;
        cntB[b]++;
    }

    for (int j = 1; j <= m; j++) {
        cout << cntB[j] - cntA[j] << '\n';
    }

    return 0;
}