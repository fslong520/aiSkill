# 字体美化

## 字体

| 用途 | 字体 | PostScript |
|------|------|------------|
| 全部文字 | 霞鹜漫黑（LXGW Marker Gothic） | `LXGWMarkerGothic-Regular` |
| 英文数字 | Cascadia Mono（fallback） | `CascadiaMono-Regular` |

## 注入代码

在 exec 中运行一次，整个文档生效：

```javascript
const s = document.createElement("style");
s.setAttribute("data-board-font", "1");
s.textContent = `
@font-face {
  font-family: "BoardFont";
  src: local("LXGWMarkerGothic-Regular"), local("LXGW Marker Gothic"), local("霞鹜漫黑");
}
.tl-rich-text, .tl-text-measure, .tl-text-shape__text {
  font-family: "BoardFont", "LXGW Marker Gothic", "Cascadia Mono", sans-serif !important;
}
/* 霞鹜漫黑渲染偏大且行距偏宽，统一修正 */
.tl-rich-text { font-size: 0.75em !important; line-height: 1.0 !important; }
.tl-text-measure { font-size: 0.75em !important; line-height: 1.0 !important; }`;
document.head.appendChild(s);
```

## 验证

```javascript
const f = [];
document.fonts.forEach(ff => f.push(ff.family + "(" + ff.status + ")"));
return f.filter(x => x.includes("Board"));
// 期望：["BoardFont(loaded)"]
```

## 字体文件

系统已装：`/usr/share/fonts/TTF/LXGWMarkerGothic-Regular.ttf`
