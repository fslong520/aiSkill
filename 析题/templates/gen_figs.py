# -*- coding: utf-8 -*-
"""生成七题多状态序列 SVG。每帧一步，帧间→箭头，展示动态变化。"""

FONT = 'font-family="Noto Serif CJK SC"'

def esc(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def array_frame(cells, colors, w=56, h=56, gap=6, labels=None, title=None):
    """数组格子帧。cells: 内容列表; colors: 每格背景色或None; labels: 每格下标标签"""
    n = len(cells)
    W = n*(w+gap) - gap
    y0 = 30
    parts = []
    for i,c in enumerate(cells):
        x = i*(w+gap)
        fc = colors[i] if colors else "#edeae2"
        sw = 1.5
        st = "#555"
        if fc == "#ffd54f": st = "#ff8f00"; sw = 2.5
        if fc == "#c62828" or fc == "#b71c1c": st = "#b71c1c"
        parts.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" fill="{fc}" stroke="{st}" stroke-width="{sw}"/>')
        parts.append(f'<text x="{x+w/2}" y="{y0+h/2+9}" font-size="26" text-anchor="middle" {FONT}>{esc(c)}</text>')
        if labels and i < len(labels):
            parts.append(f'<text x="{x+w/2}" y="{y0+h+16}" font-size="12" fill="#888" text-anchor="middle" {FONT}>{esc(labels[i])}</text>')
    if title:
        parts.append(f'<text x="{W/2}" y="18" font-size="15" fill="#333" text-anchor="middle" {FONT}>{esc(title)}</text>')
    return f'<g>{ "".join(parts) }</g>', W, y0+h+30

def grid_frame(rows, colors, cell=52, title=None, cell_text_color=None, bold_border=()):
    """网格帧。rows: 每行字符; colors: 与rows同形颜色; bold_border: [(r,c)]金框"""
    nr = len(rows); nc = len(rows[0])
    W = nc*(cell+4)-4; H = nr*(cell+4)-4
    parts = []
    for r in range(nr):
        for c in range(nc):
            x = c*(cell+4); y = r*(cell+4)
            fc = colors[r][c]
            st = "#444"; sw = 1.2
            if (r,c) in bold_border: st = "#ff8f00"; sw = 3
            if fc == "#424242": st = "#222"
            parts.append(f'<rect x="{x+1}" y="{y+1}" width="{cell-2}" height="{cell-2}" fill="{fc}" stroke="{st}" stroke-width="{sw}"/>')
            txt = rows[r][c]
            if txt and txt != '#' and txt != ' ':
                col = (cell_text_color[r][c] if cell_text_color else "#222")
                parts.append(f'<text x="{x+cell/2}" y="{y+cell/2+9}" font-size="22" text-anchor="middle" fill="{col}" {FONT}>{esc(txt)}</text>')
    if title:
        parts.append(f'<text x="{W/2}" y="{H+20}" font-size="15" fill="#333" text-anchor="middle" {FONT}>{esc(title)}</text>')
    return f'<g>{ "".join(parts) }</g>', W, H+40

def compose(frames, gap=46):
    """横向排列帧，帧间→箭头。返回整体svg字符串"""
    total_w = sum(f[1] for f in frames) + gap*(len(frames)-1)
    max_h = max(f[2] for f in frames)
    parts = []
    x = 0
    for idx,(body,W,H) in enumerate(frames):
        parts.append(f'<g transform="translate({x},0)">{body}</g>')
        x += W
        if idx < len(frames)-1:
            ax = x + gap/2
            parts.append(f'<g stroke="#999" stroke-width="2"><line x1="{ax-8}" y1="{max_h/2}" x2="{ax+8}" y2="{max_h/2}"/><path d="M{ax+8},{max_h/2} l-7,-4 v8 z" fill="#999"/></g>')
            x += gap
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{max_h}" viewBox="0 0 {total_w} {max_h}">{"".join(parts)}</svg>'

def save(name, svg):
    with open(f'/var/tmp/typst_test/figs2/{name}', 'w') as f:
        f.write(svg)
    print(f'{name}  {svg.split("width=")[1].split(" ")[0]}x{svg.split("height=")[1].split(" ")[0]}')

# ── A 题：字符串扫描（3 帧：初始→扫到T→完成）──
A = ("A","T","C","O","D","E","R")
f1 = array_frame(A, ["#edeae2"]*7, labels=["0","1","2","3","4","5","6"], title="初始：全部未处理")
f2 = array_frame(A, ["#c8e6c9","#ffd54f","#edeae2","#edeae2","#edeae2","#edeae2","#edeae2"], labels=["0","1","2","3","4","5","6"], title="扫到 T：非 A → 替换")
f3 = array_frame(["A",".",".",".",".",".","."], ["#c8e6c9","#ffcdd2","#ffcdd2","#ffcdd2","#ffcdd2","#ffcdd2","#ffcdd2"], labels=["0","1","2","3","4","5","6"], title="完成：A...... ✓")
save('fig_a.svg', compose([f1,f2,f3]))

# ── B 题：折木棍（3 帧：P1→P2→P3 累积条增长）──
def b_frame(done_idx, label, title):
    vals = ["5","2","3","8"]
    colors = []
    for i in range(4):
        if i <= done_idx: colors.append("#bbdefb")
        else: colors.append("#edeae2")
    body, W, H = array_frame(vals, colors, labels=["P1=5","P2=7","P3=10","P4=18"], title=title)
    # 下方累积条
    bw = 4*(56+6)-6
    sums = {0:5,1:7,2:10,3:18}
    ratio = sums[done_idx]/18
    bar = f'<g><rect x="0" y="120" width="{bw}" height="24" fill="#f0efe9" stroke="#aaa"/><rect x="0" y="120" width="{bw*ratio}" height="24" fill="#90caf9" stroke="#1565c0"/><line x1="{bw/2}" y1="110" x2="{bw/2}" y2="154" stroke="#1565c0" stroke-width="2"/><text x="{bw/2+6}" y="146" font-size="13" fill="#1565c0" {FONT}>S/2</text><text x="{bw/2}" y="178" font-size="13" fill="#888" text-anchor="middle" {FONT}>{label}</text></g>'
    return f'<g>{body}{bar}</g>', W, 190
f1 = b_frame(0, "P₁=5", "步1：折在 5 后")
f2 = b_frame(1, "P₂=7", "步2：折在 7 后")
f3 = b_frame(2, "P₃=10, |18−20|=2", "步3：折在 10 后 → 最小 ✓")
save('fig_b.svg', compose([f1,f2,f3]))

# ── C 题：节食（3 帧：窗口[0,2]→[1,3]→[2,4]）──
def c_frame(win_l, win_r, eaten, cur, title):
    vals = ["48","73","59","90","21"]
    colors = []
    for i in range(5):
        if i == cur: colors.append("#ffd54f")
        elif i in eaten: colors.append("#c8e6c9")
        else: colors.append("#edeae2")
    body, W, H = array_frame(vals, colors, labels=["0","1","2","3","4"], title=title)
    w = 56+6
    box = f'<rect x="{win_l*w-4}" y="24" width="{(win_r-win_l+1)*w+8}" height="{56+8}" fill="none" stroke="#1565c0" stroke-width="2.5"/>'
    return f'<g>{body}{box}</g>', W, H
f1 = c_frame(0,2,[0],0,"窗口[0,2]：48+73=121>83 → 不吃48")
f2 = c_frame(1,3,[0,1],1,"窗口[1,3]：73+59=132>83 → 不吃73")
f3 = c_frame(2,4,[0,4],4,"窗口[2,4]：90+21≤83 → 吃90、21 ✓")
save('fig_c.svg', compose([f1,f2,f3]))

# ── D 题：多源BFS（3 帧：距离0→1→2 层扩散）──
D_rows = [["#","+","#"],["+","+","+"],["#","+","#"]]
def d_frame(step, title):
    dist = [[99,1,99],[1,0,1],[99,1,99]]
    colors = []
    for r in range(3):
        row = []
        for c in range(3):
            if D_rows[r][c] == "#": row.append("#424242")
            elif dist[r][c] == 0: row.append("#a5d6a7")
            elif dist[r][c] <= step: row.append("#90caf9")
            else: row.append("#edeae2")
        colors.append(row)
    body, W, H = grid_frame(D_rows, colors, title=title, cell_text_color=[["#ddd","#222","#ddd"],["#222","#222","#222"],["#ddd","#222","#ddd"]])
    return body, W, H
f1 = d_frame(0, "步1：源(2,2) 距离0（绿）")
f2 = d_frame(1, "步2：扩散距离1（蓝）")
f3 = d_frame(2, "步3：距离2 层（K=1 → 统计≤1 = 5）")
save('fig_d.svg', compose([f1,f2,f3]))

# ── E 题：奇环（3 帧：染色→冲突→环）──
def e_frame(title, c1, c2, c3, conflict_nodes=(), cycle_edges=()):
    W = 330; H = 280
    pos = {"1":(165,60),"2":(55,215),"3":(275,215)}
    colors = {"1":c1,"2":c2,"3":c3}
    parts = []
    edges = [("1","2"),("2","3"),("1","3")]
    for (a,b) in edges:
        col = "#999"; sw = 2; dash = ""
        if (a,b) in cycle_edges or (b,a) in cycle_edges:
            col = "#ff8f00"; sw = 3; dash = ' stroke-dasharray="10 6"'
        if (a,b) == ("1","3") or (a,b) == ("3","1"):
            if conflict_nodes: col = "#c62828"; sw = 3; dash = ' stroke-dasharray="10 6"'
        p1 = pos[a]; p2 = pos[b]
        parts.append(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{col}" stroke-width="{sw}"{dash}/>')
    for node,(x,y) in pos.items():
        fc = colors[node]
        st = "#555"; sw = 1.5
        if node in conflict_nodes: st = "#c62828"; sw = 3
        parts.append(f'<circle cx="{x}" cy="{y}" r="42" fill="{fc}" stroke="{st}" stroke-width="{sw}"/>')
        parts.append(f'<text x="{x}" y="{y+12}" font-size="28" text-anchor="middle" {FONT}>{node}</text>')
    parts.append(f'<text x="{W/2}" y="272" font-size="14" fill="#333" text-anchor="middle" {FONT}>{esc(title)}</text>')
    return f'<g>{"".join(parts)}</g>', W, 280
f1 = e_frame("步1：BFS 染色中（1蓝 2蓝 3未定）", "#90caf9", "#90caf9", "#edeae2")
f2 = e_frame("步2：1 与 3 同色 → 冲突边（红）", "#a5d6a7", "#90caf9", "#a5d6a7", conflict_nodes=("1","3"))
f3 = e_frame("步3：冲突边+路径拼环 1-2-3（橙）长3 奇", "#a5d6a7", "#90caf9", "#a5d6a7", conflict_nodes=("1","3"), cycle_edges=(("1","2"),("2","3")))
save('fig_e.svg', compose([f1,f2,f3]))

# ── F 题：切片重心（3 帧：原多边形→切割→重心）──
F_pts = [(120,90),(200,40),(320,70),(360,190),(210,280)]
def f_frame(title, cut=False, fill_side=False, g=False):
    W = 500; H = 340
    parts = []
    # 边
    poly = " ".join(f"{x},{y}" for x,y in F_pts)
    parts.append(f'<polygon points="{poly}" fill="none" stroke="#333" stroke-width="2"/>')
    if fill_side:
        right = " ".join(f"{F_pts[i][0]},{F_pts[i][1]}" for i in (1,2,3))
        parts.append(f'<polygon points="{right}" fill="#90caf9" fill-opacity="0.45" stroke="none"/>')
    if cut:
        parts.append(f'<line x1="{F_pts[1][0]}" y1="{F_pts[1][1]}" x2="{F_pts[3][0]}" y2="{F_pts[3][1]}" stroke="#c62828" stroke-width="2.5" stroke-dasharray="8 5"/>')
    for i,(x,y) in enumerate(F_pts):
        fc = "#90caf9" if (fill_side and i in (1,2,3)) else "#edeae2"
        parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{fc}" stroke="#555"/>')
        parts.append(f'<text x="{x+10}" y="{y-8}" font-size="13" {FONT}>{i}</text>')
    if g:
        parts.append(f'<circle cx="270" cy="150" r="8" fill="#c62828"/>')
        parts.append(f'<text x="282" y="146" font-size="16" fill="#c62828" font-weight="bold" {FONT}>G</text>')
    parts.append(f'<text x="{W/2}" y="330" font-size="14" fill="#333" text-anchor="middle" {FONT}>{esc(title)}</text>')
    return f'<g>{"".join(parts)}</g>', W, 340
f1 = f_frame("步1：凸多边形（顶点 0-4）")
f2 = f_frame("步2：切 1→3 分两片，右侧 P′（蓝）", cut=True, fill_side=True)
f3 = f_frame("步3：面积加权求重心 G（红点）", cut=True, fill_side=True, g=True)
save('fig_f.svg', compose([f1,f2,f3]))

# ── G 题：涂黑（3 帧：选源→传染→保留）──
G_rows = [["+","-","+"],["-","-","+"]]
def g_frame(step, title):
    colors = []
    txtcol = []
    for r in range(2):
        row = []; tc = []
        for c in range(3):
            if r == 1 and step >= 1: row.append("#333"); tc.append("#ccc")
            elif step == 0 and r == 1 and c == 0: row.append("#ffd54f"); tc.append("#222")
            elif G_rows[r][c] == "+": row.append("#c8e6c9"); tc.append("#222")
            elif G_rows[r][c] == "-": row.append("#ffcdd2"); tc.append("#222")
            else: row.append("#edeae2"); tc.append("#222")
        colors.append(row); txtcol.append(tc)
    body, W, H = grid_frame(G_rows, colors, title=title, cell_text_color=txtcol, bold_border=(((1,0),) if step==0 else ()))
    return body, W, H
f1 = g_frame(0, "步1：选源(2,1)（金框）")
f2 = g_frame(1, "步2：向下传染 → 第2行全涂黑")
f3 = g_frame(1, "步3：保留第1行 +−+ → 值=2−1=1 ✓")
save('fig_g.svg', compose([f1,f2,f3]))

print("全部生成完毕")
