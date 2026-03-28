#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<vector<int>> A(n, vector<int>(n, 0));

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int a;
            cin >> a;
            A[i][j] = A[j][i] = a;
        }
    }

    // 验证三角不等式
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                if (A[i][j] + A[j][k] < A[i][k]) {
                    cout << "No\n";
                    return 0;
                }
            }
        }
    }

    // 以节点0为根
    // 对于每个节点i，找父节点p使得 A[0][p] + A[p][i] == A[0][i]
    // 且 A[0][p] < A[0][i]
    // 选择 A[0][p] 最大的

    // 按到根的距离排序
    vector<pair<int,int>> order;
    for (int i = 0; i < n; i++) order.push_back({A[0][i], i});
    sort(order.begin(), order.end());

    vector<int> parent(n, -1);
    parent[order[0].second] = order[0].second; // 根节点

    for (int idx = 1; idx < n; idx++) {
        int d_i = order[idx].first;
        int i = order[idx].second;

        // 找父节点
        int best_p = -1;
        int best_d = -1;

        for (int jdx = 0; jdx < idx; jdx++) {
            int d_p = order[jdx].first;
            int p = order[jdx].second;

            // 必须满足 A[0][p] + A[p][i] == A[0][i]
            if (d_p + A[p][i] == d_i) {
                // 选择 A[0][p] 最大的（距离根最远的作为父节点）
                if (d_p > best_d) {
                    best_d = d_p;
                    best_p = p;
                }
            }
        }

        if (best_p == -1) {
            cout << "No\n";
            return 0;
        }
        parent[i] = best_p;
    }

    // 计算每个节点到根的实际距离
    vector<int> dist(n, 0);
    for (int idx = 1; idx < n; idx++) {
        int i = order[idx].second;
        int p = parent[i];
        dist[i] = dist[p] + A[p][i];
    }

    // 验证所有距离
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            // 计算LCA的距离
            int a = i, b = j;
            while (a != b) {
                if (A[0][a] > A[0][b]) a = parent[a];
                else b = parent[b];
            }
            int lca = a;
            int calc = dist[i] + dist[j] - 2 * dist[lca];
            if (calc != A[i][j]) {
                cout << "No\n";
                return 0;
            }
        }
    }

    cout << "Yes\n";
    return 0;
}