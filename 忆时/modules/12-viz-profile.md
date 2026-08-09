# 模块 12 - 可视化与人物画像

**何时读**：用户想看记忆全貌（"看看记了啥""可视化"`/忆时 可视化`）、问"我是怎样的人""人物画像"（`/忆时 画像`）时。日常无此场景不读。

## 可视化（viz）

**命令构造：**
```bash
MEMO_DIR=~/.local/share/opencode/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/viz/viz.py
```

**参数：**
| 参数 | 说明 |
|------|------|
| `-o /path/out.html` | 指定输出路径（默认 `~/Desktop/忆时记忆全景.html`） |
| `--no-open` | 生成后不自动打开浏览器 |
| `--data x.json` | 复用已有导出 JSON，跳过重新导出 |

**产出**：单文件自包含 HTML（孟菲斯 Modern 风格——暖灰底/品牌橙/chunky shadow/黑粗边），**书页式**布局（A4 比例，3D 翻页动画）：封面（孟菲斯装饰+统计徽章）→ 藏卷统计（类型/情绪条形）→ 时序与热度（月度柱状+高频 Top3）→ 目录（10 主题卷目，点击跳转）→ 主题卷页（每页 4 条记忆卡一条一条，含关键词 chips；每条限高 3 行，超长悬停显全文——无提示文字，用户自然发现）→ 封底。翻页交互：按钮/点击页缘/键盘 ←→ Space PageDown/Home/End；窗口自适应（fitBook 保 A4 比例）。

**主题聚类**：脚本内 TOPICS 规则按关键词顺序匹配（纸焰小说→教学学生→GESP考级→灵逸OJ→数学讲义→技能开发→系统运维→工程配置→忆时系统→其他），首中即归。

**依赖**：同目录 template.html（孟菲斯模板，含 `/*__DATA__*/` 占位符）；上一级 memory_core.py（内部调用 `export --format json` 取数）。须设 `MEMO_DIR`。

**回复风格：**
```
✅ 记忆全景已生成: /home/fslong/Desktop/忆时记忆全景.html
   共 377 条记忆 · 主题 10 类
   纸焰小说 68 · 教学学生 62 · ...
```
已生成并打开 → `"全景已成，浏览器见。"`

## 画像（profile）

**两步流程：**

```bash
# ① 取素材（AI 消费）
MEMO_DIR=~/.local/share/opencode/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/viz/profile.py
# ② 注入画像正文，生成页面
MEMO_DIR=~/.local/share/opencode/忆时/data python3 ~/.config/opencode/skills/忆时/scripts/viz/profile.py \
  --content 画像正文.html --out ~/Desktop/哥哥人物画像.html --open
```

**素材报告含**：总数/跨度、类型/情绪/主题分布、高频检索 Top10、extreme 条目、最活跃日期、事件候选（每日高情绪条目，供时间线）。

**画像正文撰写**（AI 职责，按「见自己」Step 2 结构，**两页设定集**——像小说世界观设定集之两页纸）：

```html
<div class="sheet">
  <div class="seal">忆时绘像</div>
  <div class="s-head"><span class="s-no">设定 一</span><h2>人物总览</h2></div>
  <div class="s-body">
    <div class="pname">哥哥<span class="dot">·</span>人物总览</div>
    <div class="psub">MEMORY SETTINGS · 第一页</div>
    <div class="pdata"><div><!--TOTAL--><small>条记忆</small></div>…</div>
    <div class="impression"><div class="q">总体印象</div><p>一句有画面感的话</p></div>
    <div class="sec">六界身份</div>
    <div class="ids"><div class="id"><div class="ico">🧑‍🏫</div><div><div class="nm">信奥教练</div><div class="ds">说明</div></div></div>…</div>
    <div class="sec">九十日轨迹</div>
    <div class="tl"><div class="tl-item"><div class="d">日期</div><div class="e">事件</div></div>…</div>
  </div>
  <div class="s-foot"><span>忆时 · 人物设定集</span><span>PAGE 1 / 2</span></div>
</div>
<div class="sheet"><!-- 设定 二：s-body 内分三组 s-group（space-between 自动分散填满）：
  <div class="s-group"><div class="sec">性格特质</div><div class="traits">…3条…</div></div>
  <div class="s-group"><div class="sec">价值观底色</div><div class="vals">…4卡…</div></div>
  <div class="s-group"><div class="glow">…独特亮点…</div></div>
--></div>
```

纸张 min-height 860px（矮屏 78vh），内容超高则纸随长、不裁切；内容未满则 s-body `justify-content:space-between` 将各组均匀分散填满。内容宜精炼（特质 3 条为度）。可用组件类：sheet/s-head/s-no/seal/s-body/s-group/s-foot/pname/psub/pdata/impression/sec/ids/id/ico/nm/ds/traits/trait/tt/tag/td/ev/vals/val/vn/tl/tl-item/d/e/glow/gq。`<!--TOTAL-->` 在正文中亦会被替换为记忆总数。数据图表若需可于页内写 `<div class="row"><!--DATA--></div>`（两页放不下则省略）。

**产出后**：画像结果按「值必存」存入记忆（type context），并告知哥哥。

**署名规范**：记忆之书封底与画像页眉/页脚均须署名。默认署 `fslong`（哥哥之署名），生成画像前**必先问署名**（"署谁之名？"），用户另告则从其言。书页封底已内置 fslong；画像正文之 `.s-foot` 由 AI 撰写时写入署名。

**自动封存**：画像生成后自动封存为时间胶囊（解锁日 = 生成日 + 3 个月），胶囊内容含画像文件路径与摘要——三月后启封，可览当日之我。`--no-capsule` 可关闭此行为。解封用 `/忆时 胶囊 开封 <ID>`。

**回复风格：** `"画像已成，已封存，三月后开封。浏览器见。"`
