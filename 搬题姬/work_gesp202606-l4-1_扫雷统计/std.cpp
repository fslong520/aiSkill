#include <bits/stdc++.h>
using namespace std;

const int N = 505;
int n, m, q;
bool boom[N][N];
int cnt[N][N];
int dx[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
int dy[8] = {-1, 0, 1, -1, 1, -1, 0, 1};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m >> q;
    for(int i = 0; i < q; i++){
        int x, y;
        cin >> x >> y;
        boom[x][y] = true;
        for(int k = 0; k < 8; k++){
            int nx = x + dx[k];
            int ny = y + dy[k];
            if(nx >= 1 && nx <= n && ny >= 1 && ny <= m){
                cnt[nx][ny]++;
            }
        }
    }
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= m; j++){
            if(j > 1) cout << ' ';
            if(boom[i][j]) cout << '*';
            else cout << cnt[i][j];
        }
        cout << '\n';
    }
    return 0;
}
