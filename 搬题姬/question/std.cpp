#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <set>
#include <queue>
#include <stack>
#include <list>
#include <tuple>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <tuple>
#define endl '\n'
#define int long long
#define pii pair<int, int>
using namespace std;
const int inf = 0x3f3f3f3f3f3f3f3f;
const int mod = 998244353;
const int mxn = 3e6 + 5;

int n,a[114514];
int c=0;
signed main()
{
    cin>>n;
    for(int i=0;i<n;++i) cin>>a[i];
    for(int i=0;i<n-2;++i)
    {
        c+=(a[i]<a[i+1] and a[i+1]>a[i+2]);
    }
    cout<<c<<endl;
    return 0;
}
