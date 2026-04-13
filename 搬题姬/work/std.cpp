#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    string s;
    cin >> n >> s;
    
    int start = 0;
    while (start < n && s[start] == 'o') {
        start++;
    }
    
    cout << s.substr(start) << endl;
    
    return 0;
}
