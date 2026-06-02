#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k, cnt = 0;
    cin >> k;
    for (int i = 100; i <= 999; i++) {
        int s = i / 100 + (i / 10 % 10) + i % 10;
        if (s == k) cnt++;
    }
    cout << cnt << endl;
    return 0;
}
