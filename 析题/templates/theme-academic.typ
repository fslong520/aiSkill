// ═══════════════════════════════════════════════════════════
// 析题 · 学术主题（typst 0.15+）
// 用途：多题题解 / 无需动图的单题题解 → 编译 PDF，微信/打印/上传
// 风格：LaTeX / typst 学术刊风 —— 衬线正文、命题框、三线表、行号代码
// 用法：见 example-multi.typ（多题）与 example-single.typ（单题）
// ═══════════════════════════════════════════════════════════
#import "@preview/cetz:0.3.4"
#import "@preview/fletcher:0.5.4"
#import "@preview/codly:1.3.0": *

#let academic-theme(
  title: none,          // 题解总标题
  subtitle: none,       // 副标题（如比赛名/日期）
  author: "析题",
  date: none,           // 默认编译日期
  lang: "zh",
  doc,
) = {
  // ── 页面：A4，学术版心 ──
  set page(
    paper: "a4",
    margin: (x: 2.2cm, y: 2.4cm, top: 2.6cm),
    numbering: "1",
    number-align: center + bottom,
  )
  set text(
    lang: lang,
    size: 10.5pt,
    font: ("Libertinus Serif", "Noto Serif CJK SC"),
  )
  set par(justify: true, leading: 0.72em)
  set heading(numbering: "1.1")

  // ── 图题（caption）：小字灰、禁斜体（中文无斜体，强求会回退隶书）──
  show figure.caption: set text(size: 8.5pt, fill: rgb("#555555"), style: "normal", font: ("Libertinus Serif", "Noto Serif CJK SC"))
  show figure.caption: it => block(above: 0.35em, below: 0.6em, it)

  show heading.where(level: 1): it => block(
    above: 1.6em, below: 0.7em,
    it,
  ) + v(0.35em) + line(length: 100%) + v(0.4em)

  // ── 标题区 ──
  if title != none {
    text(size: 19pt, weight: "bold", title)
    v(0.2em)
  }
  if subtitle != none {
    text(size: 10.5pt, fill: rgb("#555555"), subtitle)
    v(0.6em)
  }
  // 作者/日期行
  let d = if date == none { datetime.today() } else { date }
  text(size: 9pt, fill: rgb("#777777"), [#author · #d.display("[year]-[month]-[day]")])
  v(1.2em)

  doc
}

// ── 题解小节环境 ──
// 题目一句话
#let problem-statement(body) = block(
  fill: rgb("#f7f8fa"),
  inset: (x: 1em, y: 0.6em),
  radius: 0pt,
  stroke: (left: 2.5pt + rgb("#2b6cb0"), rest: 0.5pt + rgb("#d5dbe0")),
  body,
)

// 怎么想（含因果链）
#let thinking(body) = block(
  fill: none,
  inset: (x: 0.2em, y: 0.2em),
  radius: 0pt,
  stroke: (left: 2.5pt + rgb("#2b6cb0"), rest: 0.5pt + rgb("#d5dbe0")),
  body,
)

// 关键点（命题）
#let key-point(body) = block(
  fill: rgb("#f6f8fa"),
  inset: (x: 1em, y: 0.6em),
  radius: 0pt,
  stroke: (left: 3pt + rgb("#234"), rest: 0.5pt + rgb("#c8ccd0")),
  body,
)

// 易错点
#let warn(body) = block(
  fill: rgb("#fffdf8"),
  inset: (x: 1em, y: 0.6em),
  radius: 0pt,
  stroke: (left: 3pt + rgb("#9c7c4f"), rest: 0.5pt + rgb("#d9cfb8")),
  body,
)

// 点评
#let review(body) = block(
  fill: rgb("#fafafa"),
  inset: (x: 1em, y: 0.6em),
  radius: 0pt,
  stroke: 0.5pt + rgb("#dddddd"),
  body,
)

// 图下说明（小字灰、禁斜体——中文无斜体，强求回退隶书）
#let captionless(body) = block(
  above: 0.35em,
  below: 0.6em,
  text(size: 8.5pt, fill: rgb("#555555"), style: "normal", font: ("Libertinus Serif", "Noto Serif CJK SC"), body),
)

// ── 三线表（Booktabs）──
#let booktabs(head, rows, cell-align: center) = {
  let n = head.len()
  let hdr = head.map(h => table.cell(stroke: (top: 1.2pt, bottom: 0.6pt))[#h])
  // 每行展开为多个 cell；末行底边加粗
  let body = rows.enumerate().map(((i, row)) =>
    row.map(c =>
      table.cell(stroke: (bottom: if i == rows.len() - 1 { 1.2pt } else { 0.4pt }))[#c]
    )
  ).flatten()
  align(center, table(
    columns: (auto,) * n,
    align: cell-align,
    inset: (x: 0.8em, y: 0.3em),
    stroke: none,
    table.header(..hdr),
    ..body,
  ))
}

// ── 代码块：codly 主题（文档内 #show: code-init 启用）──
#let code-init = codly-init.with()

// ── 静态组图（多题用：真画图表示状态变化）──
// array-steps: 数组类算法状态组图。arr=数组内容, steps=每步 {cur, done, msg}
//   cur: 当前高亮下标（金）| done: 已处理下标列表（绿）| 其余灰
#let array-step-fig(arr, cur: none, done: (), marks: ()) = {
  let n = arr.len()
  let cell-w = 1.15
  cetz.canvas({
    import cetz.draw: *
    for i in range(n) {
      let fc = if cur == i { rgb("#ffd54f") } else if i in done { rgb("#c8e6c9") } else if i in marks.map(x => x.at(0)) { rgb("#ffcdd2") } else { rgb("#edeae2") }
      rect((i * cell-w, 0), (1, 1), fill: fc, stroke: 0.5pt + gray)
      content((i * cell-w + 0.5, 0.5), text(size: 15pt, arr.at(i)))
      content((i * cell-w + 0.5, -0.35), text(size: 8.5pt, fill: rgb("#888888"), str(i)))
    }
  })
}

// 组图：每步一行（数组图 + 说明），纵向堆叠
#let array-steps(arr, steps, msg-col: 6cm) = {
  set text(size: 10pt)
  let rows = steps.map(s =>
    grid(
      columns: (auto, msg-col),
      column-gutter: 0.6cm,
      align: (left + horizon, left + horizon),
      array-step-fig(arr, cur: s.cur, done: s.done, marks: s.at("marks", default: ())),
      text(size: 9.5pt)[#s.msg],
    )
  )
  grid(columns: 1, row-gutter: 0.55cm, ..rows)
}

// 通用组图（网格/格子面板）：cells = 二维数组内容，step 里标 {r,c} 状态
#let grid-steps(cells, steps, cell-w: 0.9, cell-h: 0.9) = {
  let nrow = cells.len()
  let ncol = cells.at(0).len()
  let rows = steps.map(s =>
    grid(
      columns: (auto, auto),
      column-gutter: 0.6cm,
      align: (left + horizon, left + horizon),
      cetz.canvas({
        import cetz.draw: *
        for r in range(nrow) {
          for c in range(ncol) {
            let fc = rgb("#edeae2")
            for st in s.states {
              if st.at(0) == r and st.at(1) == c { fc = st.at(2) }
            }
            rect((c * (cell-w + 0.15), -r * (cell-h + 0.15)), (cell-w, cell-h), fill: fc, stroke: 0.4pt + gray)
            content((c * (cell-w + 0.15) + cell-w / 2, -r * (cell-h + 0.15) + cell-h / 2), text(size: 10pt, cells.at(r).at(c)))
          }
        }
      }),
      text(size: 9.5pt)[#s.msg],
    )
  )
  grid(columns: 1, row-gutter: 0.5cm, ..rows)
}

// ═══════════ 各题针对性组图（真画图，勿套通用格子） ═══════════

// A 题：输入串 → 输出串 双行对应
#let a-diagram(input, out, done: (), cur: none) = {
  let n = input.len()
  let w = 1.1
  cetz.canvas({
    import cetz.draw: *
    for i in range(n) {
      let fc = if cur == i { rgb("#ffd54f") } else if i in done { rgb("#c8e6c9") } else { rgb("#edeae2") }
      rect((i * w, 0.9), (1, 1), fill: fc, stroke: 0.5pt + gray)
      content((i * w + 0.5, 1.4), text(size: 13pt, input.at(i)))
    }
    content((-0.6, 1.4), text(size: 10pt, fill: gray, "输入"))
    for i in range(n) {
      let fc = if i in done { if out.at(i) == "A" { rgb("#c8e6c9") } else { rgb("#ffcdd2") } } else { rgb("#f5f4f0") }
      rect((i * w, -0.9), (1, 1), fill: fc, stroke: 0.5pt + gray)
      content((i * w + 0.5, -0.4), text(size: 13pt, if i in done { out.at(i) } else { "·" }))
    }
    content((-0.6, -0.4), text(size: 10pt, fill: gray, "输出"))
    for i in range(n) {
      line((i * w + 0.5, 0.9), (i * w + 0.5, -0.1), mark: (end: ">", size: 4pt), stroke: 0.4pt + gray)
    }
  })
}

// B 题：数组 + 前缀累积条（S/2 中分线 + 累积标签）
#let b-diagram(arr, total, cur: none, done: (), label: "") = {
  let n = arr.len()
  let w = 1.2
  let sum = 0
  for i in range(n) { if i in done { sum += int(arr.at(i)) } }
  let bw = n * w + 0.5
  cetz.canvas({
    import cetz.draw: *
    for i in range(n) {
      let fc = if cur == i { rgb("#ffd54f") } else if i in done { rgb("#bbdefb") } else { rgb("#edeae2") }
      rect((i * w, 0), (1, 1), fill: fc, stroke: 0.5pt + gray)
      content((i * w + 0.5, 0.5), text(size: 13pt, arr.at(i)))
    }
    rect((0, -1.0), (bw, 0.45), fill: rgb("#f0efe9"), stroke: 0.4pt + gray)
    if sum > 0 {
      rect((0, -1.0), (bw * sum / total, 0.45), fill: rgb("#90caf9"), stroke: 0.3pt + rgb("#1565c0"))
    }
    line((bw / 2, -1.5), (bw / 2, -0.5), stroke: 0.4pt + rgb("#1565c0"))
    content((bw / 2 + 0.08, -1.75), text(size: 9pt, fill: rgb("#1565c0"), "S/2"))
    content((0.05, -1.75), text(size: 9pt, fill: gray, label))
  })
}

// C 题：滑动窗口——格子 + 窗口框（随 cur 移动，宽 = M 格）
#let c-diagram(arr, cur: none, eaten: (), window: ()) = {
  let n = arr.len()
  let w = 1.1
  cetz.canvas({
    import cetz.draw: *
    for i in range(n) {
      let fc = if i in eaten { rgb("#c8e6c9") } else { rgb("#edeae2") }
      rect((i * w, 0), (1, 1), fill: fc, stroke: 0.5pt + gray)
      content((i * w + 0.5, 0.5), text(size: 13pt, arr.at(i)))
    }
    if window.len() == 2 {
      let l = window.at(0); let r = window.at(1)
      rect((l * w - 0.12, -0.12), ((r - l + 1) * w + 0.24, 1.24), fill: none, stroke: 1.2pt + rgb("#1565c0"))
    }
    if cur != none { rect((cur * w + 0.08, 0.08), (0.84, 0.84), fill: none, stroke: 1pt + rgb("#ff8f00")) }
    for i in range(n) { content((i * w + 0.5, -0.45), text(size: 8.5pt, fill: gray, str(i))) }
  })
}

// D 题：网格 + 距离层着色（多源 BFS）
#let d-diagram(cells, dists, step: none) = {
  let nr = cells.len()
  let nc = cells.at(0).len()
  let w = 0.85
  cetz.canvas({
    import cetz.draw: *
    for r in range(nr) {
      for c in range(nc) {
        let ch = cells.at(r).at(c)
        let d = dists.at(r).at(c)
        let fc = if ch == "#" { rgb("#424242") } else if step != none and d == step { rgb("#ffd54f") } else if d == 0 { rgb("#a5d6a7") } else if d <= step { rgb("#90caf9") } else { rgb("#edeae2") }
        rect((c * w, -r * w), (w - 0.08, w - 0.08), fill: fc, stroke: 0.3pt + gray)
        if ch != "#" and d != 99 { content((c * w + (w - 0.08) / 2, -r * w + (w - 0.08) / 2), text(size: 8.5pt, str(d))) }
      }
    }
  })
}

// E 题：三角节点图（染色 + 冲突 + 环）
#let e-diagram(nodes, edges, colors: (), highlight: (), conflict: (), cycle: ()) = {
  cetz.canvas({
    import cetz.draw: *
    let pos = ((0, 0.9), (-1.0, -0.7), (1.0, -0.7))
    let col-map = ("0": rgb("#a5d6a7"), "1": rgb("#90caf9"))
    for i in range(nodes.len()) {
      let c = if i < colors.len() { col-map.at(str(colors.at(i))) } else { rgb("#edeae2") }
      let stroke = if i in conflict { 1.4pt + rgb("#c62828") } else if i in highlight { 1.4pt + rgb("#ff8f00") } else { 0.5pt + gray }
      circle(pos.at(i), radius: 0.42, fill: c, stroke: stroke)
      content((pos.at(i).at(0), pos.at(i).at(1)), text(size: 12pt, nodes.at(i)))
    }
    for e in edges {
      let col = if e in cycle { rgb("#ff8f00") } else if e in conflict { rgb("#c62828") } else { gray }
      line(pos.at(e.at(0)), pos.at(e.at(1)), stroke: (if e in cycle or e in conflict { 1pt } else { 0.5pt }) + col)
    }
  })
}

// F 题：多边形切片（顶点 + 切割线 + 重心）
#let f-diagram(pts, cut: (), filled: (), g: ()) = {
  cetz.canvas({
    import cetz.draw: *
    let n = pts.len()
    for i in range(n) {
      line(pts.at(i), pts.at(calc.rem(i + 1, n)), stroke: 0.7pt + rgb("#333333"))
    }
    for i in range(n) {
      let fc = if i in filled { rgb("#90caf9") } else { rgb("#edeae2") }
      circle(pts.at(i), radius: 0.12, fill: fc, stroke: 0.5pt + gray)
      content((pts.at(i).at(0) + 0.15, pts.at(i).at(1) + 0.12), text(size: 9pt, str(i)))
    }
    if cut.len() == 2 {
      line(pts.at(cut.at(0)), pts.at(cut.at(1)), stroke: 1pt + rgb("#c62828"))
    }
    if g.len() == 2 {
      circle(g, radius: 0.1, fill: rgb("#c62828"), stroke: none)
      content((g.at(0) + 0.15, g.at(1) - 0.15), text(size: 9pt, fill: rgb("#c62828"), "G"))
    }
  })
}

// G 题：网格涂黑（# 墙 + 传染扩散）
#let g-diagram(cells, black: (), src: ()) = {
  let nr = cells.len()
  let nc = cells.at(0).len()
  let w = 0.85
  cetz.canvas({
    import cetz.draw: *
    for r in range(nr) {
      for c in range(nc) {
        let ch = cells.at(r).at(c)
        let fc = if ch == "#" { rgb("#424242") } else if (r, c) in black { rgb("#333333") } else if (r, c) == src { rgb("#ffd54f") } else { rgb("#edeae2") }
        rect((c * w, -r * w), (w - 0.08, w - 0.08), fill: fc, stroke: 0.3pt + gray)
        if ch != "#" {
          content((c * w + (w - 0.08) / 2, -r * w + (w - 0.08) / 2), text(size: 9pt, fill: (if (r, c) in black { rgb("#cccccc") } else { rgb("#222222") }), ch))
        }
      }
    }
  })
}

// 导出
#let theme = academic-theme
