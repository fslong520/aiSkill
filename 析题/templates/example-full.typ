// ═══════════════════════════════════════════════════════════
// ABC472 题解（A–G）· typst 学术风完整版
// 编译：typst compile <本文件> 题解.pdf
// ═══════════════════════════════════════════════════════════
#import "theme-academic.typ": *

#show: theme.with(
  title: "ABC472 题解（A–G）",
  subtitle: "AtCoder Beginner Contest 472 · 启发式题解 · 学术风",
  author: "析题",
)
#show: code-init

// ═══════════════════════════════════════════════════════════
// A — 非 A 字符替换为点
// ═══════════════════════════════════════════════════════════
#heading[#text(fill: rgb("#111"))[A — 非 A 字符替换为点]]

#problem-statement[
  #heading(level: 3)[题面]
  给定一个由大写英文字母组成的字符串 $S$。将 $S$ 中除 A 之外的所有字符替换为 `.`，输出所得字符串。

  #heading(level: 3)[题目一句话]
  扫一遍字符串：是 A 就原样输出，不是就吐一个点。
]

#align(center, image("illu/illu_a_color.png", width: 55%))

#heading(level: 2)[怎么想]
这题要是想复杂了就亏了——有人先建个数组，把每个字符判断完存起来，最后再统一输出。绕这么大一圈图啥？#strong[判断是逐字符的，输出也是逐字符的]，边读边出，一个循环搞定。
三目运算符 `c=='A'?'A':'.'` 一行顶五行的 if-else，简洁利落。

#heading(level: 2)[关键点]
#key-point[一句点透：流式处理——字符到，字符出，不需要中间存储。]

#align(center, image("figs/fig_a.svg", width: 100%))

#heading(level: 2)[样例演示]
#booktabs(
  ("字符", "判断", "输出"),
  (
    ("A", "是 A", "A"),
    ("T", "非 A", "."),
    ("C", "非 A", "."),
    ("O", "非 A", "."),
    ("D", "非 A", "."),
    ("E", "非 A", "."),
    ("R", "非 A", "."),
  ),
)
拼接得 `A......` ✓

#heading(level: 2)[复杂度]
时间 $O(|S|)$，空间 $O(1)$。

#heading(level: 2)[参考代码]
```cpp
string s;
signed main()
{
    cin >> s;
    for (auto c : s) cout << (c == 'A' ? 'A' : '.');
    return 0;
}
```
#review[点评：三目运算符一行搞定，判断与输出合二为一，干净利落。流式输出不用攒数组，思路清爽。]

#heading(level: 2)[易错点]
#warn[
- 把「非 A 换点」看成「A 换点」——条件写反，样例全灭。先想清楚：保留的是 A，改掉的是其余。
- 题目没说要求换行，输出末尾不换行也能 AC，但养成补 `endl` 的习惯更稳。
]

// ═══════════════════════════════════════════════════════════
// B — 折木棍
// ═══════════════════════════════════════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[B — 折木棍]]

#problem-statement[
  #heading(level: 3)[题面]
  有一根木棍，上面有 $N-1$ 个刻痕，将其分成 $N$ 段，各段长度从一端起依次为 $L_1, L_2, ..., L_N$。选择一处刻痕折断木棍得到两根木棍时，求两根木棍长度之差的绝对值的最小可能值。

  #heading(level: 3)[题目一句话]
  在 $N-1$ 个刻痕里挑一个折，让两段长度差最小。
]

#align(center, image("illu/illu_b.png", width: 55%))

#heading(level: 2)[怎么想]
#strong[第一反应：]暴力！对每个刻痕，把左边加起来、右边加起来，算差，取最小——$O(N^2)$。$N <= 100$ 也就 10000 次，这题还真跑得动……但 $O(N^2)$ 的毛病是「每次都要重新求和」，重复劳动。

#strong[转折观察：]仔细看「左边之和」——第 $k$ 个刻痕的左边，就是前 $k$ 段之和，即#strong[前缀和]。设总长 $S$，在第 $k$ 个刻痕折，两段长就是前缀 $P_k$ 和 $S - P_k$，差值 $|P_k - (S - P_k)| = |S - 2P_k|$。

#strong[修正后：]一趟求总长 $S$，再一趟扫前缀 $P_k$，顺手取 $min |S - 2P_k|$。$O(N)$ 搞定。

#strong[因果收束：]因为差值化简后只依赖前缀 $P_k$，所以扫描时只需维护一个累加变量 $x$，每步算 $|S-2x|$ 取最小——这就是代码里 `x+=a[i]` 与 `mn=min(mn,abs(s-2*x))` 两行的由来。

验证样例：$L = [5, 2, 3, 8]$，$S = 18$。
- 第 1 个刻痕：$P=5$，$|18-2*5|=8$
- 第 2 个刻痕：$P=7$，$|18-2*7|=4$
- 第 3 个刻痕：$P=10$，$|18-2*10|=2$ ✓ 最小

#heading(level: 2)[关键点]
#key-point[「左边之和」就是前缀和，差值变形为 $|S - 2P_k|$，一趟扫描取最小。]

#align(center, image("figs/fig_b.svg", width: 95%))

#heading(level: 2)[样例演示]
#booktabs(
  ("刻痕", "前缀 P", "两段长", "差值", "mn"),
  (
    ("1", "5", "5 / 13", [$|18-10|=8$], "8"),
    ("2", "7", "7 / 11", [$|18-14|=4$], "4"),
    ("3", "10", "10 / 8", [$|18-20|=2$], strong[2]),
  ),
)
输出 2 ✓

#heading(level: 2)[复杂度]
时间 $O(N)$，空间 $O(N)$。

#heading(level: 2)[参考代码]
```cpp
int n, x = 0, s = 0, mn = inf, a[mxn];
signed main()
{
    cin >> n;
    for (int i = 0; i < n; ++i) cin >> a[i], s += a[i];
    for (int i = 0; i < n - 1; ++i)
    {
        x += a[i];
        mn = min(mn, abs(s - 2 * x));
    }
    cout << mn << endl;
    return 0;
}
```
#review[点评：先把总和 $s$ 求出来，扫描时只维护前缀 $x$，差值写成 $|s-2x|$——不用每次算「右边之和」，省一趟。循环到 `n-1` 而非 `n` 也正确：第 $n$ 个「刻痕」不存在，折了就是空棍，没意义。]

#heading(level: 2)[易错点]
#warn[
- 循环写成 `i<n`——把「不折」也算进去了，那差值就是 $S$ 本身，会污染答案。
- $N=2$ 时只有 1 个刻痕，循环只走一遍。
- $S$ 最大 $10^7$，int 够，但写成 long long 更保险。
]

// ═══════════════════════════════════════════════════════════
// C — 节食
// ═══════════════════════════════════════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[C — 节食]]

#problem-statement[
  #heading(level: 3)[题面]
  高桥在父母家进行为期 $N$ 天的探亲。第 $i$ 天零食热量为 $A_i$。他重复如下行为：当且仅当最近 $M$ 天内所吃零食的总热量不超过 $K$ 时，才吃当天的零食。按 $i=1,...,N$ 的顺序依次决定，对每一天输出 Yes/No。

  #heading(level: 3)[题目一句话]
  每天想不想吃，取决于「最近 $M$ 天已吃掉的热量 + 今天」超没超 $K$。
]

#align(center, image("illu/illu_c.png", width: 55%))

#heading(level: 2)[怎么想]
#strong[第一反应：]每天把最近 $M$ 天重新扫一遍求和？$O(N M)$，$N=2*10^5$、$M$ 也接近时，$4*10^10$ 次加法，等到高桥探亲结束都算不完。

#strong[卡点：]窗口每次只动一格——滑出去一天，滑进来一天。绝大多数热量是重复计算的。

#strong[转折观察：]这是教科书级的#strong[滑动窗口]。维护一个「当前窗口内吃过的热量和」$s$：每天先#strong[滑出]第 $i-M$ 天（如果那天吃了，就把它的热量减掉），再#strong[尝试加]今天 $A_i$。加完如果 $<= K$，吃！否则不吃，把刚加的减回去。

#strong[细节——「如果那天吃了」：]窗口里滑出的元素，有些天是吃了的（贡献过热量），有些是没吃的（没贡献）。所以得记一个标记数组 $f$：$f[i]=1$ 表示第 $i$ 天吃了。滑出时查标记，吃了才减——不然把没吃过的热量也减掉，窗口和就错了。

#strong[因果收束：]因为窗口每次只滑出一天、滑进一天，窗口和只需"减滑出、加滑进"两步维护——所以代码里用 `s += a[i] - a[i-m]*f[i-m]` 一行同时完成两件事，判断超限后 `s -= a[i]` 撤销今天的贡献。整个算法 $O(N)$。

验证样例1：$N=5, M=3, K=83$，$A=[48,73,59,90,21]$。
- 第 1 天：窗口和 0，加 48 → 48 ≤ 83 ✓ 吃（$s=48$）
- 第 2 天：加 73 → 121 > 83 ✗ 不吃（$s=48$）
- 第 3 天：加 59 → 107 > 83 ✗ 不吃（$s=48$）
- 第 4 天：滑出第 1 天（吃了，减 48 → $s=0$），加 90 → 90 > 83 ✗ 不吃（$s=0$）
- 第 5 天：滑出第 2 天（没吃，不减），加 21 → 21 ≤ 83 ✓ 吃

输出 Yes No No No Yes ✓

#heading(level: 2)[关键点]
#key-point[滑动窗口 + 吃否标记——滑出时按标记减，才能维护「窗口内吃过的热量和」。]

#align(center, image("figs/fig_c.svg", width: 100%))

#heading(level: 2)[样例演示]
#booktabs(
  ("天", "窗口内容", [$s + A_i$], [$<= 83$?], "结果"),
  (
    ("1", "[48]", "0+48=48", "✓", "Yes (s=48)"),
    ("2", "[48,73]", "48+73=121", "✗", "No (s=48)"),
    ("3", "[48,73,59]", "48+59=107", "✗", "No (s=48)"),
    ("4", "[73,59,90]", "(48−48)+90=90", "✗", "No (s=0)"),
    ("5", "[59,90,21]", "0+21=21", "✓", "Yes (s=21)"),
  ),
)

#heading(level: 2)[复杂度]
时间 $O(N)$，空间 $O(N)$。

#heading(level: 2)[参考代码]
```cpp
int n, m, k, s, a[mxn], f[mxn];
signed main()
{
    cin >> n >> m >> k;
    for (int i = 0; i < m; ++i)
    {
        cin >> a[i];
        s += a[i];
        if (s <= k) cout << "Yes" << endl, f[i] = 1;
        else cout << "No" << endl, s -= a[i];
    }
    for (int i = m; i < n; ++i)
    {
        cin >> a[i];
        s += a[i] - a[i - m] * f[i - m];   // 滑出 i-m 天（吃了才减）
        if (s <= k) cout << "Yes" << endl, f[i] = 1;
        else cout << "No" << endl, s -= a[i];
    }
    return 0;
}
```
#review[点评：妙处全在 `s += a[i] - a[i-m]*f[i-m]` 这一行——把「滑出 + 尝试加今天」合并成一次更新。$f$ 数组当「吃否」标记，滑出时乘上标记：吃了减、没吃不减，一次乘法搞定条件判断。]

#heading(level: 2)[易错点]
#warn[
- 忘了滑出——窗口和越滚越大，前 $M$ 天的热量永远不消失，后面全判 No。
- 滑出时不查标记——没吃的天也减，窗口和变负，样例就崩。
- $K$ 达 $10^15$，必须 long long。
]

// ═══════════════════════════════════════════════════════════
// D — 轰炸狂乱
// ═══════════════════════════════════════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[D — 轰炸狂乱]]

#problem-statement[
  #heading(level: 3)[题面]
  $H$ 行 $W$ 列网格，每格是空地 `.` 或炸弹 `#`。空地 $(i,j)$ 若第 $i$ 行与第 $j$ 列均无炸弹，称为安全空地。一次移动可移到上/下/左/右的相邻空地。求满足「从 $(i,j)$ 出发至多 $K$ 次移动即可到达某个安全空地」的空地个数。

  #heading(level: 3)[题目一句话]
  从每个空地出发，$K$ 步内能不能走到一个「整行整列都没炸弹」的空地。
]

#align(center, image("illu/illu_d.png", width: 55%))

#heading(level: 2)[怎么想]
#strong[第一反应：]对每个空地做 BFS，看 $K$ 步内有没有安全空地？$H*W$ 个格子每个 BFS 一次——$O((H W)^2)$，$5*10^5$ 个格子平方一下，那是 $2.5*10^11$，直接梦碎。

#strong[关键观察一：怎么找安全空地？]「第 $i$ 行无炸弹 #strong[且] 第 $j$ 列无炸弹」——扫一遍网格，记下每行每列有没有炸弹（`xx[i]`、`yy[j]`），再扫一遍，行列都干净的 `.` 格就是安全空地。$O(H W)$ 搞定。

#strong[关键观察二：多源 BFS（换视角）：]与其「每个点出发找安全地」，不如#strong[反过来]——把所有安全空地#strong[同时]作为 BFS 起点，向外扩散。这样每个格子第一次被访问时的距离，就是它到最近安全空地的步数。一次 BFS，全部格子距离到手。

#strong[因果收束：]因为所有安全空地同时入队（距离 0），BFS 按层扩散，每个格子首次被访问时一定来自最近的源——所以一次扩散就能得到全图每个格子到最近安全空地的距离。这就是代码里先把安全空地全部 `q.push`、再统一 while 扩散的设计。

#strong[为什么多源可行？]每个格子第一次被访问，一定来自「最近的那个源」——这正是我们要的最短距离。安全空地之间互相走，距离只会更短，不影响「≤K」判定。

验证样例1：安全空地只有 $(2,2)$（第 2 行、第 2 列都无炸弹）。以它为源扩散，距离 1 的有 $(1,2),(2,1),(2,3),(3,2)$。$K=1$，统计距离 ≤1 的：源 + 四个邻居 = 5 ✓。

#heading(level: 2)[关键点]
#key-point[多源 BFS——所有安全空地一起入队，一次扩散得到每个格子到最近安全空地的距离。]

#align(center, image("figs/fig_d.svg", width: 70%))

#heading(level: 2)[样例演示]
#booktabs(
  ("格子", "行炸弹?", "列炸弹?", [$距(2,2)$], [$<= 1$?]),
  (
    ("(2,2)", "无", "无", "0", "✓"),
    ("(1,2)", "有(第1行)", "无", "1", "✓"),
    ("(2,1)", "无", "有(第1列)", "1", "✓"),
    ("(2,3)", "无", "有(第3列)", "1", "✓"),
    ("(3,2)", "有(第3行)", "无", "1", "✓"),
    ("其余空地", "—", "—", [$>= 2$], "✗"),
  ),
)
合计 5 ✓（安全空地自己距离 0，也算满足 ≤K）

#heading(level: 2)[复杂度]
时间 $O(H * W)$，空间 $O(H * W)$。

#heading(level: 2)[参考代码]
```cpp
int h, w, k, ans = 0;
string s[mxn];
int xx[mxn], yy[mxn], dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};
vector<vector<int>> dis;
queue<pii> q;

signed main()
{
    cin >> h >> w >> k;
    dis.resize(h, vector<int>(w, -1));
    for (int i = 0; i < h; ++i) cin >> s[i];
    for (int i = 0; i < h; ++i)
        for (int j = 0; j < w; ++j)
            if (s[i][j] == '#') xx[i] = 1, yy[j] = 1; // i行j列有炸弹
    for (int i = 0; i < h; ++i)
        for (int j = 0; j < w; ++j)
        {
            if (s[i][j] == '#') continue;
            if (xx[i] or yy[j] or dis[i][j] != -1) continue;
            dis[i][j] = 0;
            q.push({i, j});
        }
    while (q.size())
    {
        auto [x, y] = q.front();
        q.pop();
        for (int i = 0; i < 4; ++i)
        {
            int nx = x + dx[i], ny = y + dy[i];
            if (nx < 0 or nx >= h or ny < 0 or ny >= w) continue;
            if (s[nx][ny] == '#') continue;
            if (dis[nx][ny] != -1) continue;
            dis[nx][ny] = dis[x][y] + 1;
            q.push({nx, ny});
        }
    }
    for (int i = 0; i < h; ++i)
        for (int j = 0; j < w; ++j)
            if (s[i][j] != '#' and dis[i][j] != -1 and dis[i][j] <= k) ans++;
    cout << ans << endl;
    return 0;
}
```
#review[点评：思路一气呵成：两遍扫描找安全空地 → 全部入队 → 一次 BFS 扩散 → 统计。用 `dis[i][j]!=-1` 兼当「访问过」标记，省一张 visited 表，老练。]

#heading(level: 2)[易错点]
#warn[
- 「行无炸弹 #strong[且] 列无炸弹」——条件写成 `or` 就变成「行或列干净」，安全空地暴增，答案全错。
- $K=0$ 时只数安全空地本身，别忘了距离 0 也 ≤K。
- `#` 格既不能当源也不能被走到——所有判断先排除 `#`。
- $H$、$W$ 都能到 $5*10^5$，但乘积不超过 $5*10^5$，按 $H*W$ 量级开数组、BFS 才不会爆。
]

// ═══════════════════════════════════════════════════════════
// E — 奇环
// ═══════════════════════════════════════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[E — 奇环]]

#problem-statement[
  #heading(level: 3)[题面]
  给定简单连通无向图，顶点 $1$ 至 $N$，$M$ 条边。判断是否存在由奇数个顶点组成的环（长度 ≥ 3，顶点两两不同，首尾相接），若存在则输出任意一个。共 $T$ 个测试用例。

  #heading(level: 3)[题目一句话]
  图里有没有奇数长度的环？有就把它找出来。
]

#align(center, image("illu/illu_e.png", width: 55%))

#heading(level: 2)[怎么想]
#strong[第一反应：]枚举环？那可是 $O(2^N)$ 级别的快乐，$N=2*10^5$ 想都别想。

#strong[关键知识：]「图里有没有奇环」=「图是不是二分图」——#strong[二分图就是没有奇环的图]，这是图论的看家定理。所以问题变成：染色判二分图；发现不是二分图的那一刻，把奇环揪出来。

#strong[转折观察——怎么把环「揪」出来：]BFS/DFS 染色时，如果遇到一条边连接两个#strong[同色]顶点（且非父子边），冲突了，图非二分图。这时候：沿着 BFS 树从这两个点往祖先走，走到它们的公共祖先 `lca`，拼出一条路径，再加上冲突边本身，就构成一个环。

#strong[为什么这个环一定是奇数长？]设两冲突点 $u, v$ 同色。BFS 树中深度奇偶 = 颜色（`color = depth mod 2`）。同色 ⟹ `depth_u` 与 `depth_v` 同奇偶 ⟹ $d_u + d_v$ 为偶数。环长 $= d_u + d_v - 2 d_l + 1$。偶数 − 偶数 + 1 = #strong[奇数] ✓。数学保证了这条路永远正确。

#strong[因果收束：]因为构造环需要"沿父链上跳"，所以 BFS 时必须记录每个点的父节点 `par` 与深度 `depth`；因为要拼出路径，所以两冲突点先对齐深度、再一起上跳到 LCA，最后"上段 + LCA + 下段"拼接——这就是代码里 `while (depth[a] > depth[b]) a = par[a]` 与 `seg + back` 两段的由来。

举个例：三角形 $1-2-3$。BFS 从 1 出发：1 染 0（深度 0），2 染 1（深度 1），3 染 0（深度 2）。检查 3 的邻居时发现 1 也是颜色 0——冲突！沿父链：$d_3=2 > d_1=0$，3 上跳到父 2（深度 1），再跳到 1（深度 0），`lca`=1。路径 = 3→2→1，加上冲突边 (1,3)，环为 $3,2,1$，长度 3（奇数）✓。

#heading(level: 2)[关键点]
#key-point[奇环 ⟺ 非二分图；同色冲突边 + 树上路径经 LCA 拼环，深度同奇偶保证环长必奇。]

#align(center, image("figs/fig_e.svg", width: 85%))

#heading(level: 2)[样例演示]
#booktabs(
  ("用例", "图", "有奇环?", "输出"),
  (
    ("1", "三角形 1-2-3", "✓（3 环）", "3 / 2 1 3"),
    ("2", "7点7边(偶环+尾巴)", "✗ 二分图", "-1"),
    ("3", "五边形 1-2-3-4-5-1", "✓（5 环）", "5 / 3 2 1 5 4"),
    ("4", "两五边形+桥接", "✓（5 环）", "5 / 3 2 1 5 4"),
  ),
)

#heading(level: 2)[复杂度]
时间 $O(N + M)$，空间 $O(N + M)$。

#heading(level: 2)[参考代码]
```cpp
int T;
vector<int> g[200005];
int color[200005], depth[200005], par[200005];

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> T;
    while (T--)
    {
        int n, m;
        cin >> n >> m;
        for (int i = 1; i <= n; i++)
        {
            g[i].clear();
            color[i] = -1;
            depth[i] = 0;
            par[i] = 0;
        }
        for (int i = 0; i < m; i++)
        {
            int a, b;
            cin >> a >> b;
            g[a].push_back(b);
            g[b].push_back(a);
        }
        // BFS 染色判二分图；遇同色非父边 → 构造奇环
        queue<int> q;
        q.push(1);
        color[1] = 0;
        vector<int> cyc;
        while (!q.empty() && cyc.empty())
        {
            int u = q.front();
            q.pop();
            for (int v : g[u])
            {
                if (color[v] == -1)
                {
                    color[v] = color[u] ^ 1;   // 异色入队
                    depth[v] = depth[u] + 1;
                    par[v] = u;
                    q.push(v);
                }
                else if (par[u] != v && color[v] == color[u])
                {
                    // 同色冲突 → 奇环：u..lca..v + 边(v,u)
                    int a = u, b = v;
                    while (depth[a] > depth[b]) a = par[a];  // 先对齐深度
                    while (depth[b] > depth[a]) b = par[b];
                    while (a != b)                            // 再一起上跳到 lca
                    {
                        a = par[a];
                        b = par[b];
                    }
                    int lca = a;
                    vector<int> seg;
                    for (int x = u; x != lca; x = par[x]) seg.push_back(x);
                    seg.push_back(lca);
                    vector<int> back;
                    for (int x = v; x != lca; x = par[x]) back.push_back(x);
                    reverse(back.begin(), back.end());
                    seg.insert(seg.end(), back.begin(), back.end());
                    cyc = seg;
                    break;
                }
            }
        }
        if (cyc.empty()) cout << -1 << "\n";
        else
        {
            cout << cyc.size() << "\n";
            for (size_t i = 0; i < cyc.size(); i++)
            {
                if (i) cout << " ";
                cout << cyc[i];
            }
            cout << "\n";
        }
    }
    return 0;
}
```
#review[点评：选 BFS 而非 DFS 是明智的——$N$ 到 $2*10^5$ 时递归 DFS 会爆栈，BFS 用显式队列天然安全。冲突处理也很严谨：先对齐深度、再一起上跳求 LCA，最后「上段 + lca + 下段」拼环。]

#heading(level: 2)[易错点]
#warn[
- 只判「是/否二分图」不输出环——题目要的是环本身，输出 Yes 一分不得。
- 同色边的判定要排除父边 `par[u] != v`，否则把树边当冲突，输出假环。
- DFS 递归在 $N=2*10^5$ 的链上直接栈溢出——务必 BFS 或手写栈。
- 多个测试用例要清空全局数组，忘了清就会串数据。
]

// ═══════════════════════════════════════════════════════════
// F — 切片重心
// ═══════════════════════════════════════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[F — 切片重心]]

#problem-statement[
  #heading(level: 3)[题面]
  xy 平面上有凸 $N$ 边形 $P$，顶点逆时针编号 $1..N$。$Q$ 个询问，每个询问给两个不相邻顶点 $u, v$。连线 $u-v$ 将 $P$ 分成两个多边形，取位于从 $u$ 到 $v$ 有向直线右侧的那个 $P'$，求其几何中心（密度均匀薄板的重心）。误差容差 $10^(-6)$。

  #heading(level: 3)[题目一句话]
  凸多边形被一条对角线切成两半，取右边那块，求它的重心，$Q$ 次询问要快。
]

#align(center, image("illu/illu_f.png", width: 55%))

#heading(level: 2)[怎么想]
#strong[第一反应：]每次询问把 $P'$ 的顶点全列出来，套多边形重心公式算一遍？$P'$ 平均有 $N/2$ 个顶点，$Q$ 次就是 $O(Q N)$——$2*10^5 * 3*10^4$，直接爆炸。

#strong[卡点：]重心公式是「对每条边累加」——每次重算，重复劳动。

#strong[转折观察一：右侧那块是哪块？]凸多边形逆时针编号，内部在每条有向边的"左侧"。连线 $u -> v$ 的"右侧"就是内部的反侧——即从 $u$ 逆时针走到 $v$ 的那段弧。所以 $P'$ 的顶点序列就是 $u, u+1, ..., v$（若 $u < v$）或 $u, ..., N, 1, ..., v$（若 $u > v$）——环上连续的一段。

#strong[转折观察二：多边形重心公式（面积加权）：]顶点 $p_0..p_(k-1)$ 逆时针，设 $c_i = p_i times p_(i+1) = x_i y_(i+1) - x_(i+1) y_i$（注意最后一条边 $p_(k-1) arrow.r p_0$ 也要算！）：
$ S = 1/2 sum c_i, quad C_x = (sum (x_i+x_(i+1)) c_i)/(6S) = (sum (x_i+x_(i+1)) c_i)/(3 sum c_i) $

举个例（样例1 询问 $u=2, v=4$）：$P'$ 顶点 $2:(1,3), 3:(-3,2), 4:(-1,-2)$。
- 边 $2->3$：$c = 1*2 - 3*(-3) = 11$，分子项 $(1-3)*11 = -22$
- 边 $3->4$：$c = (-3)*(-2) - 2*(-1) = 8$，分子项 $(-3-1)*8 = -32$
- 边 $4->2$（#strong[闭合边，易漏！]）：$c = (-1)*3 - (-2)*1 = -1$，分子项 $(-1+1)*(-1) = 0$
- $sum c = 11+8-1 = 18$，$sum M = -54$，$C_x = -54/(3*18) = -1$ ✓；$C_y = 54/54 = 1$ ✓

看看——如果把闭合边 $4->2$ 漏掉，$sum c = 19$，重心就变成 $-54/57 approx -0.947$，错得离谱。闭合边是重心公式的命根子。

#strong[转折观察三：前缀和提速：]$P'$ 的边集是「顶点序列里相邻的边」+「闭合边」。顶点序列是环上的连续一段 ⟹ 边集是「环上的连续一段边」+ 一条闭合边。

#strong[因果收束：]因为"环上连续一段"的求和是区间求和，而区间求和可以 $O(1)$ 完成——所以预处理每条边 $i -> i+1$ 的 `c`、分子 $X$、$Y$ 三个前缀和，询问时区间求和，再单独补上闭合边 $v -> u$ 的贡献即可。总复杂度 $O(N + Q)$。

#heading(level: 2)[关键点]
#key-point[多边形重心 = 面积加权求和，边集是环上连续段 + 闭合边（$v -> u$ 的贡献必加），前缀和把每次询问压到 $O(1)$。]

#align(center, image("figs/fig_f.svg", width: 90%))

#heading(level: 2)[样例演示]
#booktabs(
  ("边", [$c_i$], [分子项 X], [$sum c_i$], [$sum X$]),
  (
    ("2→3", "11", "(1−3)×11 = −22", "11", "−22"),
    ("3→4", "8", "(−3−1)×8 = −32", "19", "−54"),
    ("4→2 闭合", "−1", "(−1+1)×(−1) = 0", "18", "−54"),
  ),
)
$C_x = -54/(3*18) = -1$，$C_y = 54/54 = 1$ → 输出 `-1.000000000000000 1.000000000000000` ✓

#heading(level: 2)[复杂度]
时间 $O(N + Q)$，空间 $O(N)$。

#heading(level: 2)[参考代码]
```cpp
int n, q;
long long x[30005], y[30005];
long double preC[30005], preX[30005], preY[30005];

// 边 i (1≤i≤N) 从顶点 i 到 i+1（i=N 时到 1）
long long c(int i, int j)
{
    return x[i] * y[j] - y[i] * x[j];
}

long double sum(const long double a[], int l, int r)
{
    if (l > r) return 0;
    return a[r] - (l == 1 ? 0 : a[l - 1]);
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout << fixed << setprecision(15);
    cin >> n >> q;
    for (int i = 1; i <= n; i++) cin >> x[i] >> y[i];
    for (int i = 1; i <= n; i++)
    {
        int j = (i == n) ? 1 : i + 1;
        long long c = c(i, j);
        preC[i] = preC[i - 1] + c;
        preX[i] = preX[i - 1] + (long double)(x[i] + x[j]) * c;
        preY[i] = preY[i - 1] + (long double)(y[i] + y[j]) * c;
    }
    auto range = [&](int l, int r, const long double a[]) -> long double {
        if (l <= r) return sum(a, l, r);
        return sum(a, l, n) + sum(a, 1, r);
    };
    for (int qi = 0; qi < q; qi++)
    {
        int u, v;
        cin >> u >> v;
        int lo = u, hi = (v - 1 + n - 1) % n + 1;  // v-1 循环
        long double sc = range(lo, hi, preC);
        long double mx = range(lo, hi, preX);
        long double my = range(lo, hi, preY);
        long long cvu = c(v, u);   // 闭合边 v→u
        sc += cvu;
        mx += (long double)(x[v] + x[u]) * cvu;
        my += (long double)(y[v] + y[u]) * cvu;
        long double cx = mx / (3.0L * sc);
        long double cy = my / (3.0L * sc);
        cout << cx << " " << cy << "\n";
    }
    return 0;
}
```
#review[点评：三个前缀和（c / 分子 X / 分子 Y）一维并行，询问时 `range` 函数统一处理「跨环」区间，干净。用 `long double` 累加是细心之举——分子量级可达 $10^22$，double 的有效位数会吃紧。闭合边单独补，注释点明「必加」。]

#heading(level: 2)[易错点]
#warn[
- #strong[闭合边 $v -> u$ 的贡献漏加]——这是本公式最容易丢的一环，丢了 $sum c$ 就错，重心跟着歪。
- 顶点序列方向搞反——右侧那块是「$u$ 到 $v$」的哪一半要想清楚。
- 浮点：分子巨大，用 long double；输出位数至少 15 位。
- $u > v$ 时区间跨过顶点 1，前缀和要拆成两段。
]

// ═══════════════════════════════════════════════════════════
// G — 级联网格
// ═══════════════════════════════════════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[G — 级联网格]]

#problem-statement[
  #heading(level: 3)[题面]
  $H$ 行 $W$ 列网格，每格是 +、-、\# 之一。操作：选一个非 \# 格，将「只通过左、右、下方向移动、不经过 \# 即可从所选格到达」的所有格子改为 \#（所选格本身包含在内）。可操作零次或多次，求操作后「+ 个数减 - 个数」的最大值。

  #heading(level: 3)[题目一句话]
  每次选一个格，把它「向下 + 左右」能到的整片都涂黑，问最多能留下多少个「+ 减 -」。
]

#align(center, image("illu/illu_g.png", width: 55%))

#heading(level: 2)[怎么想]
#strong[第一反应：]暴力枚举操作组合？操作次数不限、每格都能当源点——指数级状态，想都别想。

#strong[卡点：]涂黑只能向下 + 左右传播，#strong[不能向上]——这是单向传播。

#strong[转折观察一：涂黑只会「传染」到下一行。]因为向上回不去，左右只在同一行内——所以最终状态可以#strong[逐行描述]：某行被涂黑的部分，只由「本行的操作」和「上一行传染下来的」决定，跟更上面的行无关。

#strong[转折观察二：把每行按 `#` 切成「段」。]一行里被墙隔开的连续块是独立单元——向左/右传播只会吞掉同一段内的格子；向下的传染看「列区间是否相交」。每行段数很少（`#` 分隔），所以「本行涂黑哪些段」可以压成一个二进制 mask。

#strong[转折观察三：行间转移规则。]上一行涂黑的段，会传染到下一行「列区间与它相交」的段——这些段#strong[必须]涂黑；其余段自由选择。这就是唯一的行间约束。

#strong[因果收束：]因为每行段数少（$2^c$ 可枚举），又因为行间传染只依赖「上一行的 mask」——所以是典型的#strong[逐行状压 DP]：`dp[i][mask]` = 前 $i$ 行、第 $i$ 行涂黑 mask 段时的最大保留值。转移两步：①上行 mask 中涂黑的段，把本行相交段全部强制涂黑，得到 nm；②行内从「全保留」出发逐个把段涂黑（涂黑一段收益减 $w$）。这就是代码里两段循环的由来。

验证样例1：$2*3$ 网格 `+-+ / --+`，两行各 1 段，段值 $+1$（第 1 行）与 $-1$（第 2 行）。
- dp 递推：`dp[1][0] = 1`（行1 保留）、`dp[1][1] = 0`（行1 涂黑）；行2 若上行涂黑则必涂：`dp[2][1] = dp[1][1] + 0 = 0`；上行保留则行2 自由：`dp[2][1] = 1 + 0 = 1`（行2 涂黑）、`dp[2][0] = 1 + (-1) = 0`（行2 也保留）
- 答案 = `max(dp[2])` = max{-1, 1} = 1 ✓——对应「第 1 行全保留、第 2 行全涂黑」

全保留 = $+1 + (-1) = 0$；第 1 行也涂黑则第 2 行被传染必涂，剩 $0$。最大就是 1 ✓。

#heading(level: 2)[关键点]
#key-point[涂黑只会向下传染 ⟹ 按行切段、逐行状压 DP。每行段数少（`#` 分隔）是本题能压的关键。]

#align(center, image("figs/fig_g.svg", width: 70%))

#heading(level: 2)[样例演示]
#booktabs(
  ("方案", "涂黑", "保留", "值"),
  (
    ("不操作", "—", "全部 6 格", "2−4 = −2"),
    ("选 (2,1)", "第2行 3 格", "第1行 + - +", strong["2−1 = 1 ✓"]),
    ("选 (1,1)", "全部 6 格", "—", "0"),
  ),
)

#heading(level: 2)[复杂度]
时间 $O(H * 2^c * c^2)$，空间 $O(2^c)$。
$c$ = 每行最大段数（`#` 分隔，远小于 $W$）。

#heading(level: 2)[参考代码]
```cpp
#include <iostream>
#include <vector>
using namespace std;
const int inf = 0x3f3f3f3f3f3f3f3f;
const int mxn = 3e6 + 5;

int n, m;
string a[mxn];           // 网格，1~n 行
vector<pii> seg[mxn];    // 每行连续段的 [l, r]
vector<int> w[mxn];      // 每段的值（+1/-1 累加）
int cnt[mxn];            // 每行段数
vector<vector<int>> dp;  // dp[i][mask]：前 i 行、第 i 行涂黑 mask 段的最大保留值

int gv(char c) { return c == '+' ? 1 : -1; }

bool jiao(pii x, pii y)  // 两段列区间是否相交
{
    int l = max(x.first, y.first);
    int r = min(x.second, y.second);
    return l <= r;
}

signed main()
{
    cin >> n >> m;
    for (int i = 1; i <= n; ++i)
    {
        cin >> a[i];
        for (int j = 0; j < m; ++j) if (a[i][j] != '#')
        {
            int l = j, s = gv(a[i][j]);          // 段起点 + 段值
            while (j + 1 < m && a[i][j + 1] != '#')
            {
                ++j;
                s += gv(a[i][j]);                // 同一段内连吃
            }
            seg[i].push_back({l, j});
            w[i].push_back(s);
        }
        cnt[i] = seg[i].size();                  // 每行段数
    }

    dp.assign(n + 1, {});
    dp[0] = {0};                                 // 空行，mask 只有 0
    for (int i = 1; i <= n; ++i)
    {
        dp[i].assign(1 << cnt[i], -inf);
        // 行间传染：上行涂黑的段，本行列区间相交的段必须涂黑
        for (int mask = 0; mask < (1 << cnt[i - 1]); ++mask)
        {
            int nm = 0;
            for (int j = 0; j < cnt[i - 1]; ++j) if (mask >> j & 1)
                for (int k = 0; k < cnt[i]; ++k) if (jiao(seg[i - 1][j], seg[i][k]))
                    nm |= 1 << k;               // 被传染的段强制涂黑
            dp[i][nm] = max(dp[i][nm], dp[i - 1][mask]);
        }
        // 行内：先默认全保留——把所有段的值都加上
        for (int mask = 0; mask < (1 << cnt[i]); ++mask)
            for (int j = 0; j < cnt[i]; ++j) if (!(mask >> j & 1))
                dp[i][mask] += w[i][j];
        // 行内：逐个把段涂黑——涂黑 j 收益减 w[j]
        for (int mask = 0; mask < (1 << cnt[i]); ++mask)
            for (int j = 0; j < cnt[i]; ++j) if (!(mask >> j & 1))
                dp[i][mask | (1 << j)] = max(dp[i][mask | (1 << j)], dp[i][mask] - w[i][j]);
    }
    int ans = -inf;
    for (auto v : dp[n]) ans = max(ans, v);
    cout << ans << endl;
    return 0;
}
```
#review[点评：核心是把「单向传播」翻译成「逐行传染」：不能向上 ⟹ 每行的状态只看上一行压过来的 mask。按 `\#` 切段后状态量骤减，$2^c$ 枚举 + 行间 `jiao` 相交转移，干净利落。行内「先全加再逐个减」是从全保留出发做子集转移的小技巧。]

#heading(level: 2)[易错点]
#warn[
- mask 表示「涂黑」的段——行间传染时，上行 mask 中为 1 的段才向下传染，别取反。
- 段区间是闭区间 [l, r]，相交判断 $max(l) <= min(r)$——列相邻（恰好相接）也算相交，会传染。
- 行内两步顺序不能乱：先「加未涂黑段的值」再「减段值转移」。
- 每行段数决定 $2^c$——`#` 分隔是本题能压的关键；段数多的行会爆状态。
]

// ═══════════════════════════════════════════════════════════
// 串讲
// ═══════════════════════════════════════════════════════════
#pagebreak()
#heading[#text(fill: rgb("#111"))[串讲]]

这七题恰好铺开了一条「算法视野」之路——A 题流式处理，入门姿势；B 题前缀和，把重复求和变成一趟扫描；C 题滑动窗口，前缀和的亲兄弟，窗口只动一格所以只更新两端；D 题多源 BFS，把「每个点找目标」翻转为「目标们一起扩散」，一次遍历全图；E 题二分图染色，用「深度奇偶 = 颜色」的数学性质保证构造正确；F 题前缀和 + 面积加权公式，把几何题翻译成区间求和，闭合边的细节是成败关键；G 题最抽象，把「单向向下传播」翻译成「逐行传染」，按 `\#` 切段后逐行状压 DP。

七题七种翻译，共同点只有一个——#strong[把新问题翻译成你已会的老工具]。

#booktabs(
  ("题", "核心技巧", "一句话"),
  (
    ("A", "字符串扫描", [原地替换，$O(n)$]),
    ("B", "折木棍", [前缀和 $|S-2P_k|$ 一趟扫描]),
    ("C", "节食", [滑动窗口，滑出按标记减]),
    ("D", "轰炸狂乱", [多源 BFS，一次扩散全图]),
    ("E", "奇环", [BFS 染色，同色冲突拼环]),
    ("F", "切片重心", [面积加权，前缀和 $O(1)$ 查询]),
    ("G", "级联网格", [按行切段状压 DP，段相交传染]),
  ),
)
