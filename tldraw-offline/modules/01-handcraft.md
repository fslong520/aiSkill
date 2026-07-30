# 手抄报设计

## 花边（手抄报的灵魂）

花边是手抄报的标志。四边走一圈，立刻有手抄报的感觉。

### 四角装饰

用 `type:"geo"` + `geo:"star"` 或小圆点放四个角：

```javascript
// 四角星星
editor.createShape({id:createShapeId(),type:"geo",
  props:{geo:"star",w:30,h:30,color:"red"}});  // 放在四个角
```

### 四边花边线

用 `type:"line"` + `dash:"dotted"` 或 `dash:"dashed"` 画四边：

```javascript
const L=(x,y,w,h)=>{
  editor.createShape({id:createShapeId(),type:"line",
    props:{color:"orange",dash:"dotted",size:"m",spline:"line",
      points:[{id:"a",index:"a1",x:0,y:0},{id:"b",index:"a2",x:w,y:0}]}});
};
// 上边、下边、左边、右边
L(20,10,850,0); L(20,530,850,0);  // 横线
// 竖线用两个点
```

也可以用多条短花边线拼出波浪效果。

## 标题

手抄报的标题要大、要花哨：

```
⭐  ╔══════════════════╗  ⭐
   ║   主题大标题      ║
   ╚══════════════════╝
```

**做法：**
1. `geo:"rectangle"` + `fill:"solid"` 做标题底色（红/蓝/橙）
2. 大字 `size:"l"` 写标题文字
3. 标题两侧各加一个 `geo:"star"` 小星星装饰
4. 标题下方加一条波浪线 `dash:"dotted"`

## 分区

不要用直角矩形。用这些形状做分区：

| 形状 | geo 类型 | 适合 |
|------|---------|------|
| 椭圆 | `ellipse` | 中心主题/标题 |
| 云朵 | `cloud` | 温馨内容/故事 |
| 菱形 | `diamond` | 注意事项/重点 |
| 六边形 | `hexagon` | 知识点 |
| 圆角感 | `rectangle` + 浅底色 | 正文区 |

### 分区示例

```javascript
// 椭圆主题框
editor.createShape({id:createShapeId(),type:"geo",
  props:{geo:"ellipse",w:200,h:100,color:"red",fill:"none"}});

// 云朵内容框
editor.createShape({id:createShapeId(),type:"geo",
  props:{geo:"cloud",w:250,h:120,color:"blue",fill:"solid"}});

// 五角星装饰
editor.createShape({id:createShapeId(),type:"geo",
  props:{geo:"star",w:25,h:25,color:"yellow",fill:"solid"}});
```

## 配色方案（手抄报风格）

| 风格 | 主色 | 搭配 | 底色 |
|------|------|------|------|
| 可爱风 | pink, red | yellow, violet | light-red, light-violet |
| 清新风 | blue, green | light-blue, light-green | yellow |
| 国庆风 | red, yellow | orange | light-red |
| 科幻风 | violet, blue | light-blue | light-violet |
| 自然风 | green, light-green | yellow, light-blue | light-green |

**每个分区用不同底色**，颜色越丰富越像手抄报。

## 装饰元素

### 小星星（各区点缀）

```javascript
for(let i=0;i<5;i++){
  editor.createShape({id:createShapeId(),type:"geo",
    props:{geo:"star",w:15,h:15,color:"yellow",fill:"solid"}});
}
```

散落放在分区角落、标题旁、空白处。

### 装饰点

```javascript
// 用小的椭圆点做装饰
editor.createShape({id:createShapeId(),type:"geo",
  props:{geo:"ellipse",w:8,h:8,color:"red",fill:"solid"}});
```

### 分隔线

```javascript
editor.createShape({id:createShapeId(),type:"line",
  props:{color:"orange",dash:"dotted",size:"m",spline:"line",
    points:[{id:"a",index:"a1",x:0,y:0},{id:"b",index:"a2",x:300,y:0}]}});
```

### 插图配对话气泡

插图旁加一个小箭头或气泡标注：

```javascript
// 小气泡用 geo:"cloud"
editor.createShape({id:createShapeId(),type:"geo",
  props:{geo:"cloud",w:80,h:40,color:"light-blue",fill:"solid",
    richText:{type:"doc",content:[{type:"paragraph",content:[{type:"text",text:"看这里！"}]}]},
    align:"middle",verticalAlign:"middle",size:"s"}});
```

## 布局参考

```
    ⭐    ════════════════    ⭐          ← 花边上线+星
  ┌──────────────────────────────────┐
  │  🎯  ☆ 大标题 ☆                 │  ← 标题带星
  │  ═══════════════════════════════  │    下划线
  │                                   │
  │  ╭── 椭圆 ──╮  ┌── 云朵 ──┐      │
  │  │ 内容…   │  │ 内容…   │      │
  │  ╰─────────╯  └─────────┘      │
  │              ☆                    │
  │  ◆ 菱形重点框 ◆                   │
  │                                   │
  │  ═══════ 分隔线 ═══════          │
  │  ✏️ 小练习                       │
  │  ⭐                          ⭐   │
  └──────────────────────────────────┘
    ⭐    ════════════════    ⭐          ← 花边下线+星
```

## 制作步骤

1. **花边**：四角放星，四边画花边线
2. **标题**：底色方块 + 大字 + 两侧星
3. **分区**：椭圆/云朵/菱形做区域，各填内容
4. **插图**：每区至少一张图（下载后 base64 嵌入）
5. **装饰**：星、点、线散落点缀
6. **连线**：用箭头连接相关区域
7. **练习**：底部留一块小练习区
