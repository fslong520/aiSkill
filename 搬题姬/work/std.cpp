#include <iostream>
#include <cmath>
using namespace std;

int main()
{
    int n;
    cin >> n;
    
    // 计算 2^n - 2*n
    long long ans = (1LL << n) - 2LL * n;
    
    cout << ans << endl;
    
    return 0;
}