#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;

    multiset<int> trees;

    while (q--) {
        int type, h;
        cin >> type >> h;

        if (type == 1) {
            // 添加一棵高度为 h 的树
            trees.insert(h);
        } else {
            // 删除所有高度 <= h 的树
            auto it = trees.upper_bound(h);
            trees.erase(trees.begin(), it);
        }

        cout << trees.size() << '\n';
    }

    return 0;
}