#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, a[105];
    cin >> n;
    for (int i = 0; i < n; i++) cin >> a[i];
    int passes = 0;
    for (int i = 0; i < n; i++) {
        bool flag = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                swap(a[j], a[j + 1]);
                flag = true;
            }
        }
        passes++;
        if (!flag) break;
    }
    cout << passes << endl;
    return 0;
}