#include <bits/stdc++.h>
using namespace std;

struct Member {
    string name;
    int level;
    int gong;
    int id; // 输入顺序
};

// 比较函数
bool cmp(Member a, Member b) {
    if (a.gong != b.gong) return a.gong > b.gong;
    if (a.level != b.level) return a.level > b.level;
    return a.id < b.id;
}

string get_position(int rank) {
    if (rank == 1) return "BangZhu";
    if (rank == 2) return "FuBangZhu";
    if (rank <= 4) return "HuFa";
    if (rank <= 7) return "ZhangLao";
    if (rank <= 12) return "TangZhu";
    if (rank <= 42) return "JingYing";
    return "BangZhong";
}

// 映射中文职位（实际输出可能要求中文，按原题习惯）
string get_position_zh(int rank) {
    if (rank == 1) return "帮主";
    if (rank == 2) return "副帮主";
    if (rank <= 4) return "护法";
    if (rank <= 7) return "长老";
    if (rank <= 12) return "堂主";
    if (rank <= 42) return "精英";
    return "帮众";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    if (!(cin >> n)) return 0;
    
    vector<Member> members(n);
    for (int i = 0; i < n; ++i) {
        cin >> members[i].name >> members[i].level >> members[i].gong;
        members[i].id = i;
    }
    
    sort(members.begin(), members.end(), cmp);
    
    for (int i = 0; i < n; ++i) {
        cout << members[i].name << " " << get_position_zh(i + 1) << " " << members[i].level << endl;
    }
    
    return 0;
}
