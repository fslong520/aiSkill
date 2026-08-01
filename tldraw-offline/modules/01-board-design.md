# 学神笔记风格板书设计

## 核心原则

- **外框用细线**——`size:"s"`，不要 `size:"m"`。粗线显得笨
- **四色卡片布局**——每区独立色（橙/蓝/绿/紫），2×2 网格
- **深色标题无底色**——蓝/黑大字，不染背景
- **浅色内盒**——每区两个浅色底 box 装内容
- **装饰点到为止**——四角星、卡角圆点、标题线端圆点
- **框线粗细统一**——所有边框 `size:"s"`，一致才显精致

## 基础工具函数

```javascript
const { createShapeId, toRichText } = await import("tldraw");
const T=(x,y,l,c,s)=>editor.createShape({id:createShapeId(),type:"text",x,y,props:{color:c,richText:toRichText(l),size:s||"m",font:"draw"}});
const B=(x,y,w,h,c)=>editor.createShape({id:createShapeId(),type:"geo",x,y,props:{geo:"rectangle",w,h,color:c,fill:"solid",richText:toRichText(""),size:"s",font:"draw"}});
const F=(x,y,w,h,c)=>editor.createShape({id:createShapeId(),type:"geo",x,y,props:{geo:"rectangle",w,h,color:c,fill:"none",size:"s",font:"draw"}});
const S=(x,y,sz,c)=>editor.createShape({id:createShapeId(),type:"geo",x,y,props:{geo:"star",w:sz,h:sz,color:c,fill:"solid",size:"s"}});
const O=(x,y,sz,c)=>editor.createShape({id:createShapeId(),type:"geo",x,y,props:{geo:"ellipse",w:sz,h:sz,color:c,fill:"solid",size:"s"}});
```

## 四色卡片模板

```
  ⭐                      ⭐           ← 四角星
┌────────────────────────────────────────────┐
│  主标题（蓝字）                             │
│  副标题（灰字）                             │
│  ───────────── ● ────────────              │  ← 细线+圆点
│                                             │
│  ┌─ 橙边 ──────────┐  ┌─ 蓝边 ───────────┐ │
│  │ ● 区标题 (橙)    │  │ ● 区标题 (蓝)    │ │
│  │ ┌─浅蓝box──┐    │  │ ┌─浅蓝box──┐   │ │
│  │ │正文内容   │    │  │ │ ① ② ③ ④ │   │ │
│  │ └──────────┘    │  │ └──────────┘   │ │
│  │ ┌─黄box──┐     │  │ ┌─紫 box──┐   │ │
│  │ │ 💡提示  │     │  │ │步骤内容  │   │ │
│  │ └────────┘     │  │ └──────────┘   │ │
│  │ ●              ●│  │ ●             ●│ │
│  └─────────────────┘  └────────────────┘ │
│                                             │
│  ┌─ 绿边 ──────────┐  ┌─ 紫边 ───────────┐ │
│  │ ...              │  │ ...              │ │
│  │       ☆         │  │       ☆         │ │
│  └─────────────────┘  └────────────────┘ │
  ⭐                      ⭐
```

## 装饰元素清单

| 装饰 | 函数 | 位置 |
|------|------|------|
| 角星 | S(x,y,12,"orange"/"violet") | 画板四角 |
| 卡角点 | O(x,y,8,color) | 每区上下角 |
| 标题线 | line + O(端) | 标题下方 |
| 内容星 | S(x,y,15,"yellow") | 区内亮点 |

## 字号建议

| 元素 | size | 色 |
|------|------|----|
| 总标题 | "l" | blue |
| 副标题 | "s" | grey |
| 区标题 | "m" | 区色 |
| 正文 | "s" | black |
| 强调 | "s" | red |

## 配色规则

- 每区边框色 = 区标题色 = 卡角点色
- 内盒底色用浅色（light-blue / yellow / light-green / light-violet）
- 全局装饰色：yellow（星）、grey（线）
