#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int T;
    cin >> T;
    
    while (T--) {
        int n;
        cin >> n;
        
        // 初始状态：1和2在场上，3在场下
        int player1 = 1, player2 = 2;  // 场上的两个人
        int waiting = 3;               // 场下的人
        
        bool valid = true;
        
        for (int i = 0; i < n; i++) {
            int winner;
            cin >> winner;
            
            if (!valid) continue;  // 已经不合法了，继续读但不处理
            
            // 判断胜利者是否在场上
            if (winner == player1) {
                // player1 赢了，player2 输了下场，waiting 上场
                int loser = player2;
                player2 = waiting;
                waiting = loser;
            } else if (winner == player2) {
                // player2 赢了，player1 输了下场，waiting 上场
                int loser = player1;
                player1 = waiting;
                waiting = loser;
            } else {
                // 胜利者不在场上，序列不合法
                valid = false;
            }
        }
        
        cout << (valid ? "YES" : "NO") << "\n";
    }
    
    return 0;
}
