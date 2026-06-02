#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int a, b;
    cin >> a >> b;
    long long sum = 0;
    for (int i = a; i <= b; i++) {
        if (i % 2 == 0) sum += i;
    }
    cout << sum << endl;
    return 0;
}
