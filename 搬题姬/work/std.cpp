#include <bits/stdc++.h>
using namespace std;

const int N = 100005;
int n, a[N];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    sort(a, a + n);
    int median = a[n / 2];
    
    long long moves = 0;
    for (int i = 0; i < n; i++) {
        moves += abs(a[i] - median);
    }
    
    cout << moves << '\n';
    
    return 0;
}
