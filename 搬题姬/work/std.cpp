#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <set>
#include <queue>
#include <stack>
#include <list>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <tuple>
#define endl '\n'
#define int long long
#define pii pair<int, int>
using namespace std;
const int MOD = 998244353;
const int MXN = 3e5 + 5;

int h, w;
string s[MXN];
int sr,sc,gr,gc;
int dr[4] = {-1, 1, 0, 0};
int dc[4] = {0, 0, -1, 1};
char ch[4] = {'U', 'D', 'L', 'R'};
int pre[4000000];
int g=-1;
string ans;

bool in(int r, int c)
{
    // 判断合法
    return 0 <= r && r < h && 0 <= c && c < w;
}
int id(int r, int c, int d)
{
    // 计算编号，方便后面计算路径，把三维压缩成1维并包含方向
    return ((r * w + c) << 2) | d;
}

void push(int nd)
{
}

signed main()
{
    // 输入输出优化
    cin.tie(0)->sync_with_stdio(0);
    cout.tie(0);
    cin>>h>>w;
    for(int i=0;i<h;++i) cin>>s[i];
    for(int i=0;i<h;++i)
    {
        for(int j=0;j<w;++j)
        {
            if(s[i][j]=='S') sr=i,sc=j;
            if(s[i][j]=='G') gr=i,gc=j;
        }
    }
    fill(pre, pre + 4000000, -1);
    queue<int> q;
    for(int d=0;d<4;++d)
    {
        int nr=sr+dr[d],nc=sc+dc[d];
        if(!in(nr,nc) or s[nr][nc]=='#') continue;
        int v = id(nr, nc, d);
        pre[v] = -2;
        q.push(v);
    }
    while(!q.empty())
    {
        int v = q.front();
        q.pop();
        int d = v & 3; // 获取方向
        int x = v >> 2; // 获取编号
        int r = x / w, c = x % w; // 获取行和列
        if(r==gr and c==gc)
        {
            g = v; // 记录终点
            break;
        }
        auto push=[&](int nd)
        {
            int nr=r+dr[nd],nc=c+dc[nd];
            if(!in(nr,nc) or s[nr][nc]=='#') return;
            int nv = id(nr, nc, nd);
            if(pre[nv]!=-1) return;
            pre[nv] = v;
            q.push(nv);
        };
        if(s[r][c]=='o') push(d); // 如果是直行直接进去
        else if(s[r][c]=='x') /// 强制转弯，不能回头
        {
            for(int nd=0;nd<4;++nd)
            {
                if(nd!=d) push(nd);
            }
        }
        else
        {
            for(int nd=0;nd<4;++nd) push(nd);
        }
    }
    if(g==-1) cout<<"No"<<endl;
    else
    {
        for(int v=g;v!=-2;v=pre[v]) ans+=ch[v & 3]; // 记录路径
        reverse(ans.begin(), ans.end());
        cout<<"Yes"<<endl;
        cout<<ans<<endl;
    }
    return 0;
}
