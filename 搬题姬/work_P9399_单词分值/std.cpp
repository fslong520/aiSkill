#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    int score = 0;
    for (char c : s) {
        if (c >= 'a' && c <= 'z') score += c - 'a' + 1;
        else if (c >= 'A' && c <= 'Z') score -= (int)c;
    }
    cout << score << endl;
    return 0;
}
