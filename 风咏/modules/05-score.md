# 模块五：文字描曲

## 宗旨

以文字描曲——不用五线谱/简谱，用文字与标记让编曲人与 AI 音乐工具可还原旋律、节奏、力度、唱法。

## 总纲五件

| 项 | 例 |
|----|-----|
| 拍号 | 4/4 |
| BPM | 76（中速偏慢——夜泊之缓）——BPM 后注情绪理由 |
| 调式 | 五声羽调（la-do-re-mi-sol），主音 la——古风骨相 |
| 音域 | a → e²（约十一度）——不宜过宽（夜泊低吟） |
| 结构 | 前奏4 → 主歌1×4 → 主歌2×4 → 预副歌×4 → 副歌×4 → 间奏2 → 桥段×4 → 副歌再现×4 → 尾声×4 → 尾奏4 |

## 逐段描曲六维

每段每句按六维描述：

| 维 | 说什么 | 例 |
|----|--------|-----|
| 音区 | 高/中/低音区 | 中低音区起（la-do） |
| 走向 | 上行↗/下行↘/平行→/波浪〜 | "乌啼"上行（re-mi，如啼） |
| 进行 | 级进/跳进/重复音/回旋 | "撞"字跳进上行（la-do-mi）——钟声动机 |
| 音型 | 长音/短音/附点/切分/拖腔 | "拨着算盘"短促附点（do.do-do，如算盘声） |
| 力度 | pp/p/mp/mf/f/ff、渐强<、渐弱> | "敲醒"强音，句尾长音渐弱 |
| 唱法 | 气声/胸腔/念白/耳语/滑音/叹息 | "沉"字滑音下行（沉没） |

## 动机设计

选一个意象作旋律动机贯穿全曲（听者识之）：
- 钟声动机：《楓橋夜泊》——凡钟声处旋律相近（跳进上行→下行落长音）：撞响/钟声/敲醒/钟声远了——四次出现，听者识钟
- 其他可选：水声动机、霜落动机（下行滑音）、灯火动机（上行暖音）

## 唱法总则（成表）

| 段 | 唱法 | 咬字 | 呼吸 |
|----|------|------|------|
| 主歌 | 气声低吟（自语感） | 字字清晰（叙事） | 句末换气留白 |
| 预副歌 | 气声渐实（愁渐浓） | 滑音处软 | 副歌前深吸（爆发预备） |
| 副歌 | 胸腔放开（苍凉） | 字头硬（重音字） | 句句换气，末句拖腔 |
| 桥段 | 念白（冷峻/锋芒） | 顿挫（咬牙） | 短促呼吸 |
| 尾声 | 耳语（最轻——最深处） | 软（吞字——梦呓） | 浅吸，终句屏息 |

## 特殊处理

- 滑音：沉/落/远——下行滑音（沉郁）
- 拖腔：句尾长音（余韵）——副歌末句最重
- 停顿：间奏/留白——钟声后静
- 情绪线：每段一词（倦→温→愁→叩→醒→放→释）

## 检查

- [ ] 总纲五件齐
- [ ] 每段每句六维皆述（至少音区/走向/力度/唱法）
- [ ] 动机贯穿（至少两现）
- [ ] 唱法总则成表
- [ ] AI 工具提示可直接粘贴

## AI 曲调提示（文字描曲 → AI 可执行提示）

文字描曲是人读的；AI 提示须把曲调限制翻译给 Suno/ACE，否则 AI 自由发挥。

**结构**：
1. **风格行**（第一行——总纲）：genre + instruments + BPM + 拍号 + 调式 + 人声 + 整体氛围 + 结构动态
   - 例：`chinese folk ballad, xiao flute, guzheng, piano, temple bell, sparse, 76 BPM, 4/4, A minor pentatonic, male vocal, intimate restrained, cinematic crescendo`
2. **段落括号**（每段歌词前）：曲调指令——音区/力度/唱法/旋律特征/特殊效果
   - 例：`[Chorus] (full chest voice, powerful, temple bell tolls, sustained long notes, stronger on 敲醒)`
3. **歌词内嵌**：段落标签 + 原文歌词

**翻译对照表**：

| 文字描曲 | AI 提示词 |
|----------|-----------|
| 五声羽调 | A minor pentatonic scale |
| BPM/拍号 | 76 BPM, 4/4 time |
| 气声低吟 | breathy low register |
| 胸腔放开 | full chest voice, powerful |
| 念白顿挫 | almost spoken, staccato, bitter |
| 耳语渐无 | whispered, fading into silence |
| 渐强渐弱 | crescendo / fading dynamics |
| 钟声动机 | bell-toll motif / faint distant bell |
| 算盘附点 | abacus-like staccato |
| 留白 | sparse arrangement, silence |
| 滑音 | descending slides |
| 拖腔 | sustained long notes |

**要点**：
- 段落括号是 AI 可读的曲调指令——每段必写（音区/力度/唱法至少三样）
- 动机首现处标注（"first bell-toll motif on 撞响"）——AI 后续识别
- 情绪顶点句标注（"stronger on 敲醒""highest note"）——AI 有重音落点
- 终段必写 "into silence"（余韵收束）
