# 用户偏好账本 · 前端视觉风格（哥哥钦定）

> 最高优先级：凡哥哥让我写前端，默认用此风格。除非哥哥明说换风格，否则一律照此实现。
> 参考源：1memory-windows-client（哥哥朋友所作，2026-09-07 钦定）。

## 风格名：ENSO 柔和立体风（Neumorphism 变体 · 浅色为默认）

一句话：低饱和暖灰底 + 白色高光边 + 大范围柔和双向阴影（外暗内亮），浮起的面板感，克制优雅，阅读舒适。

## 核心 DNA（照抄这些值）

### 1. 色板（浅色主题）
```css
--bg: #f1f2f4;            /* 页面底：低饱和冷暖灰 */
--panel: #fff;             /* 面板：纯白 */
--text: #27292d;           /* 主文字：近黑 */
--muted: #82858d;          /* 次要文字：中灰 */
--line: #eaecef;           /* 分割线：极浅灰 */
--accent: #6856c9;         /* 强调色：低饱和紫（唯一彩度来源，克制使用） */
--soft: #f7f8fa;           /* 输入框/悬停底 */
--hover: #eeeef2;
--black: #242527;          /* 主按钮/深色块 */
--green: #4c927a;          /* 状态绿：低饱和 */
--cream: #f5eee8;          /* 奶油色块（insight 卡） */
```
分类色（mem-icon / type-badge 用，全部低饱和 pastel）：
- 紫 `#eae8f3/#9684b4` · 橙 `#f7ece2/#b28c65` · 绿 `#e7f1ed/#79a38e` · 蓝 `#e7eef5/#819ab4` · 粉 `#f6e9ec/#b88c97`

### 2. 深度系统（灵魂所在——双向柔和阴影）
```css
/* 面板级（sidebar/inspector）：四层阴影，亮部朝左上、暗部朝右下 */
--depth-panel: 10px 14px 32px rgba(62,70,89,.075),
  2px 3px 8px rgba(62,70,89,.045),
  -5px -5px 20px rgba(255,255,255,.88),
  inset 0 1px 2px rgba(255,255,255,1);
/* 卡片级 */
--depth-card: 7px 9px 23px rgba(65,73,92,.055),
  1px 2px 5px rgba(65,73,92,.025),
  -4px -4px 14px rgba(255,255,255,.75),
  inset 0 1px 1px #fff;
/* 控件级（按钮/输入框） */
--depth-control: 4px 5px 11px rgba(74,81,98,.095),
  -3px -3px 9px rgba(255,255,255,.94),
  inset 0 1px 1px rgba(255,255,255,.95);
```
面板底用微渐变增光感：`background: linear-gradient(145deg, #fff, #fdfdfe);`
边框用白高光：`border: 1px solid rgba(255,255,255,.95);`
凹陷感（搜索框/标签容器）：`box-shadow: inset 2px 2px 5px rgba(124,131,147,.045), inset -2px -2px 5px #fff;`
深色激活块：`background: linear-gradient(155deg, #292a2d, #17181b);` + 微亮内描边 `inset 0 1px 1px rgba(255,255,255,.18)`

### 3. 字体与排版
- 中文：系统栈 `-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`（Windows 加 "Segoe UI Variable Text"）
- 基准 14px；正文行高 1.9-2.1（阅读型界面给足呼吸）
- 标题：`font-weight: 550; letter-spacing: -0.6~-1.1px; font-size: clamp(23px, 2vw, 33px)`
- ~~次要信息敢用小字号：meta 8-10px + muted 色~~ **已废止（2026-09-09，见文末可读性修正：字号地板 12px）**
- ~~eyebrow 小标签：`font-size: 8-9px; letter-spacing: 1-1.4px`~~ **已废止（2026-09-09，同下）**

### 4. 形状与组件
- 大圆角：面板 20px、卡片 11-17px、按钮 10px、胶囊 30-40px、modal 22px
- 按钮按下反馈：`button:active { transform: scale(.975) }`；全局 transition .16s
- 图标按钮：32px 圆形，hover 出 soft 底
- 分段标签（side-tabs/view-tabs）：浅灰容器 + 白底凸起 active 块
- 类型徽章：pastel 底 + 低饱和同系文字，9px 圆角 5px
- 状态点：4-6px 圆点 + `box-shadow: 0 0 0 3px {color}10`（同色 6% 光环）
- 滚动条：5px 细条 + 半透明圆角
- 列表渐隐：`mask-image: linear-gradient(#000 97%, transparent)`

### 5. 布局
- 桌面：`grid-template-columns: 270px 1fr; padding: 12px; gap: 12px`，面板各自独立浮起，不通铺
- 宽屏 1650px+ 侧栏 300px；阅读列宽 max-width 790px 居中
- 动效：`appear .24s ease`（淡入）、`modal-in .22s`（上移 8px + scale .985 进入）

### 6. 深色主题（data-theme="dark"）
```css
--bg:#1e2024; --panel:#282b30; --text:#e1e3e8; --muted:#949ba8;
--line:#373b44; --soft:#30333a; --hover:#3a3c46; --black:#44414c;
```
深色下 pastel 色块降饱和：`filter: brightness(.8) saturate(.7)`

### 7. 无障碍底线（原作自带，必保留）
- `:focus-visible { outline: 2px solid #8c7ddd; outline-offset: 3px }`
- `prefers-reduced-motion: reduce` 全动画关停
- `prefers-contrast: more` 提升次要文字对比
- 触控高亮去除 `-webkit-tap-highlight-color: transparent`

## Do / Don't

**Do**：阴影宁浅勿深（透明度 ≤.12）；彩色只出现在分类徽章/图标底（pastel）与 accent；白边框 + 微渐变制造"上缘受光"；层级靠浮起深度而非描边；次要信息用灰与字重分层次，**字号不得低于 12px**（见文末可读性修正）。

**Don't**：禁高饱和大色块；禁生硬投影 `box-shadow: 0 2px 4px black`；禁通铺背景无浮层；禁 transition 缓慢 (>0.3s)；禁忽略 focus-visible；深色主题不是简单反色，需整体降饱和调对比。

## 2026-09-09 可读性修正（哥哥钦定 · 优先级高于上文所有字号规则）

> 原话：「界面还有个问题就是解释说明性文字太多了，字体太小，导致阅读困难有障碍」「最小的12就行了」

**硬规则（违反即失败）：**

1. **字号地板 12px**：任何可见文字 ≥12px。元信息 12px / 主文字 14px / 正文 14-15px；
   标题 15-25px 不缩。旧「meta 8-10px」「≥8px 可读」一律作废。
2. **说明文案 ≤25 字**：界面上的解释性段落只留结论，删过程、删"为什么"、删自我辩解；
   细节移入 `title` 提示或文档，不摊在页面上。
3. **小字字距**：原 8-9px 眉批的 1-1.5px 字距在放大后显松散，改 0.6-0.8px。
4. **验收门禁**：交付前用真实渲染量测——最小字号 ≥12px、无裁切（scroll>client）、
   可见长文（>45 字）为 0；三指标缺一不算完成。
5. **诊断先量化**：报"字号小/文案多"时必须给出统计（如"511 处声明中 374 处 <12px"），
   禁凭观感下结论。

## 实现捷径

写新前端时：把 ENSO 色板 + 三档深度阴影变量直接抄进 `:root`，面板/卡片/控件分别挂 `--depth-panel/card/control`，即可获得八成气质。完整原始代码参考：`/tmp/opencode/1m-win/1memory-windows-client/src/`（styles.css 全量 + depth.css 深度系统）；若已清理，从 1memory-windows-client-final-source.zip 重解。
