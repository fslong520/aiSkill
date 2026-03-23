# 图片生成提示词模板

## 生成规则

### 通用规则

1. **分辨率**：1024x1024
2. **风格**：根据世界观自动调整
3. **存储路径**：`life_sim/stories/[角色名]/images/`
4. **命名规则**：`[类型]_[年龄]_[简短描述].png`

### 风格对应表

| 世界类型 | 风格关键词 | 色调 |
|----------|-----------|------|
| 奇幻中世纪 | fantasy art, medieval, detailed, painting style | 温暖、金色 |
| 东方玄幻 | Chinese art style, xianxia, ethereal, ink wash | 清雅、水墨 |
| 蒸汽朋克 | steampunk, industrial, mechanical, brass | 铜色、褐色 |
| 黑暗奇幻 | dark fantasy, gothic, atmospheric, shadowy | 阴暗、紫黑 |
| 异能都市 | anime style, modern, urban, vibrant | 霓虹、对比 |
| 原始部落 | tribal art, primal, natural, earthy | 大地色系 |
| 废土末世 | post-apocalyptic, gritty, desolate, wasteland | 灰黄、锈色 |

---

## 角色卡提示词

### 婴儿期角色卡

```
[风格关键词], character portrait, infant baby, [种族特征], 
cute, innocent, swaddled clothes, soft lighting, 
fantasy setting, detailed, 1k resolution, portrait shot

[种族特征说明]
人类：human, round face, soft skin
精灵：elf baby, pointed ears, delicate features
兽人：orc baby, small tusks, greenish skin
龙裔：dragonborn baby, small scales, reptilian eyes
```

### 童年期角色卡

```
[风格关键词], character portrait, [年龄] years old child, 
[种族] [性别], [外貌特征], wearing [服装], 
[表情], [动作/姿势], fantasy setting background, 
detailed, 1k resolution, upper body portrait

[示例]
fantasy art, character portrait, 8 years old child, 
half-elf girl, silver hair, violet eyes, pointed ears, 
wearing simple village clothes, curious expression, 
holding a small book, village background, 
detailed, 1k resolution
```

### 少年期角色卡

```
[风格关键词], character portrait, [年龄] years old teenager, 
[种族] [性别], [外貌特征], wearing [服装], 
[表情], [动作/姿势], [背景环境], 
detailed, 1k resolution, upper body portrait

[示例]
fantasy art, character portrait, 16 years old teenager, 
half-elf female, silver hair in ponytail, violet eyes, 
pointed ears, slim figure, wearing magic academy uniform, 
confident smile, holding a spell book, magic academy hall, 
detailed, 1k resolution
```

### 成年期角色卡

```
[风格关键词], character portrait, [年龄] years old adult, 
[种族] [性别], [职业/身份], [外貌特征], 
wearing [服装/装备], [表情], [动作/姿势], 
[背景环境], detailed, 1k resolution, upper body portrait

[示例]
fantasy art, character portrait, 25 years old adult, 
half-elf female, wizard, silver hair, violet eyes, 
pointed ears, elegant features, wearing elegant wizard robe 
with magical embroidery, serious expression, 
casting spell with glowing hands, ancient library, 
detailed, 1k resolution
```

### 老年期角色卡

```
[风格关键词], character portrait, [年龄] years old elder, 
[种族] [性别], [身份], [外貌特征], 
gray/white hair, aged face, wise expression, 
wearing [服装], [动作/姿势], [背景环境], 
detailed, 1k resolution, upper body portrait
```

### 角色卡通用后缀

```
, high quality, detailed, fantasy art style, 
professional character design, 1k resolution
```

---

## 场景图提示词

### 出生地场景

```
[风格关键词], [地点类型] scene, [时间], [天气], 
[建筑特征], [环境细节], [人物活动], 
atmospheric, detailed, 1k resolution, wide shot

[示例]
fantasy art, small village scene, golden hour, 
clear sky, rustic wooden houses, cobblestone streets, 
villagers going about their day, nearby forest, 
mountains in distance, peaceful atmosphere, 
detailed, 1k resolution, wide shot
```

### 学院/学校场景

```
[风格关键词], [学院类型] academy scene, [时间], 
[建筑风格], students, [活动], 
atmospheric lighting, detailed, 1k resolution

[示例]
fantasy art, magic academy scene, afternoon, 
grand stone architecture, tall towers, 
students in robes walking, magical glowing orbs floating, 
grand entrance hall, stained glass windows, 
detailed, 1k resolution
```

### 战斗场景

```
[风格关键词], battle scene, [角色描述], 
[敌人描述], [动作], [特效], 
dramatic lighting, dynamic pose, 
detailed, 1k resolution

[示例]
fantasy art, battle scene, young wizard casting fire spell, 
flame dragon enemy, intense combat, fire magic effects, 
dramatic lighting, dynamic action, 
ancient ruins battlefield, detailed, 1k resolution
```

### 自然场景

```
[风格关键词], [地形] landscape, [时间], [天气], 
[植物], [动物], [氛围], 
detailed, 1k resolution, wide shot

[示例]
fantasy art, enchanted forest landscape, twilight, 
mystical fog, ancient tall trees, glowing flowers, 
fireflies, magical atmosphere, ethereal light, 
detailed, 1k resolution, wide shot
```

### 城市/城镇场景

```
[风格关键词], [城市类型] city scene, [时间], 
[建筑风格], [街道活动], [标志性建筑], 
atmospheric, detailed, 1k resolution, wide shot

[示例]
fantasy art, medieval city scene, evening, 
stone buildings, busy market street, castle on hill, 
guards patrolling, merchants selling goods, 
warm light from windows, detailed, 1k resolution
```

### 重要事件场景

```
[风格关键词], [事件类型] scene, [关键人物], 
[事件动作], [环境], [情感氛围], 
dramatic, detailed, 1k resolution

[示例]
fantasy art, coronation scene, young queen, 
being crowned, grand throne room, 
nobles watching, golden light, majestic atmosphere, 
detailed, 1k resolution
```

### 居家/日常生活场景

```
[风格关键词], [房间类型] interior, [时间], 
[家具装饰], [人物活动], [氛围], 
cozy, detailed, 1k resolution

[示例]
fantasy art, cozy cottage interior, evening, 
wooden furniture, fireplace with warm glow, 
person reading by window, cat sleeping, 
peaceful atmosphere, detailed, 1k resolution
```

---

## 特殊场景提示词

### 出生场景

```
[风格关键词], birthing room, [时代建筑], 
soft candlelight, mother holding newborn, 
midwife assisting, warm and tender moment, 
detailed, 1k resolution
```

### 成人礼场景

```
[风格关键词], coming of age ceremony, 
[文化特征], [主角描述], ceremonial setting, 
community gathering, solemn yet joyful atmosphere, 
detailed, 1k resolution
```

### 婚礼场景

```
[风格关键词], wedding ceremony, 
[文化/宗教特征], bride and groom, 
beautiful decoration, guests, romantic atmosphere, 
detailed, 1k resolution
```

### 死亡场景

```
[风格关键词], deathbed scene, [角色描述], 
elderly/weak, surrounded by loved ones, 
peaceful expression, soft light, emotional moment, 
detailed, 1k resolution
```

### 结局场景（人生总结）

```
[风格关键词], life journey collage, 
[角色一生关键场景], multiple panels, 
chronological progression, 
artistic montage, detailed, 1k resolution
```

---

## 负面提示词

```
(通用负面提示词)
low quality, blurry, deformed, ugly, bad anatomy, 
bad proportions, extra limbs, disfigured, 
watermark, signature, text, logo, 
cropped, out of frame, worst quality, 
low resolution, jpeg artifacts
```

---

## 生成策略

### 自动生成时机

| 事件 | 触发条件 | 图片类型 |
|------|----------|----------|
| 出生 | 游戏开始 | 角色卡（婴儿） |
| 成年 | 18岁 | 角色卡（成年） |
| 成人礼 | 15-18岁 | 场景图 |
| 婚礼 | 结婚事件 | 场景图 |
| 重要战斗 | 战斗事件 | 场景图 |
| 到达新地点 | 首次到达 | 场景图 |
| 人生终点 | 死亡 | 角色卡（结局）+ 场景图 |

### 手动生成触发

玩家说：
- "生成角色卡" → 角色卡
- "生成场景" → 当前场景
- "画一张[描述]" → 自定义图片
- "我想看看[某人/某地]" → 对应图片

### 图片管理

```
stories/
└── [角色名]/
    └── images/
        ├── character_00_newborn.png
        ├── character_08_child.png
        ├── character_16_teenager.png
        ├── character_25_adult.png
        ├── scene_00_birthplace.png
        ├── scene_15_academy.png
        ├── scene_25_wedding.png
        └── ...
```