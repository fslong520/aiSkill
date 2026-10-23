# 星匣创作台 · 118 技能库全文

> 提取自星匣 CDN app.js 的 baseSkillLibrary（渐进式披露：description 常驻路由，body 命中才注入）。
> 用法：开发游戏时按题材取 2-5 个技能的 body 作为设计约束注入。

## 编排（5）

### 任务拆解 `task-decomposition`
tags: 拆解, 规划, 复杂, 项目
把模糊或大型创作请求拆成 3-7 个可独立交付的子任务。

拆解原则：
1. 每个子任务必须能独立交付一个可见成果（设计文档/规格 JSON/代码块/HTML 原型/图像）
2. 第一个子任务就要有可见成果，禁止仅做 '理解需求/澄清范围' 的纯规划步骤
3. 子任务之间通过 dependsOn 表达顺序，前置产出作为后置输入
4. 总数控制在 2-6 个；超过 6 个说明粒度太细，应合并
5. 每个子任务标注 outputKind（md/json/html/image/audio）



### 技能匹配与编排 `skill-routing`
tags: 技能, 路由, 匹配
在执行前从技能库选出最相关的 3-8 个技能并组合使用。

对每个子任务，先列出所有候选技能（按 tags / description 关键词命中），再按相关性给出 0-1 评分；取 top 5 注入到执行 prompt 的 system 段。多个技能的 body 用换行拼接，不互斥。

### 迭代与修订 `iteration-and-revision`
tags: 迭代, 修订, 重做, 调整
处理用户的 '换一个' '再细化' '换风格' 等修订请求。

复用上一版的 confirmed 部分（不重新生成已确定的设定/世界观）；只重做被点名的部分；保留之前版本作为 v1，新版本叠加为 v2。

### 无技能回退 `no-skill-fallback`
tags: 回退, 通用方法, fallback
当没有任何专项技能命中时，按通用文本/对话方法处理；不要硬塞专项技能。

直接以通用助手身份回答：① 理解请求；② 给出可交付内容（文本/列表/代码块）；③ 末尾给 1-2 条非阻塞建议。不要装作命中了某个专项。

### 澄清式提问 `clarify-when-unclear`
tags: 澄清, 提问
当用户请求严重模糊到无法动手时，先问 1-2 个最关键澄清问题，再开始。

提问要少而准；优先问决定整体方向的问题；如果能在 1 个澄清后开始，就不要凑足 2 个。

## 游戏设计（4）

### 体验支柱定义 `game-pillars`
tags: 体验, 情感, 支柱, 玩家承诺, 游戏
定义玩家应获得的 3-5 条情感/挑战/节奏/独特卖点。所有游戏类创作的第一步。

用 3-5 条短句写体验支柱，每条形如 '玩家[情感]+[行为]+[反馈]'：
示例：'玩家通过抉择体验权力斗争的窒息感' / '玩家在资源紧缺时做艰难取舍' / '玩家通过角色关系网解开谜题'
禁止写空泛词如 '有趣' '好玩' '沉浸'；要写出具体情感 + 具体行为。
支柱用于后续校验：每个玩法/事件/UI 决策都应能挂到至少 1 条支柱。



### 核心循环设计 `core-loop`
tags: 核心循环, 回合, 玩法, 游戏, 模拟器
定义玩家每一轮做什么、系统如何反馈、为什么继续玩。

核心循环结构：[行动] → [系统响应] → [反馈] → [选择/进展] → [回到行动]
为每一环写 1-2 句具体内容；避免抽象词。
时间尺度要明确：是 30 秒/回合？1 分钟/天？还是事件驱动？
示例（深夜电台）：[选择来电] → [对话产生情绪+收听率变化] → [显示数值+反馈对话] → [收入/疲惫推进] → [下一来电]



### 状态与变量系统 `state-system`
tags: 状态, 变量, 数值, 公式, 模拟器, 经营
把玩法转化为可枚举的变量、初值、变化规则、上下限、胜负条件。

用 JSON 给出：
{ vars: [{ key, label, init, min, max, kind('resource'|'pressure'|'relation'|'flag'|'progress') }],
  formulas: [{ trigger, effect: 'varA -= 1; varB += rng(0,2)' }],
  endings: [{ when, label }] }
至少 4 个变量；至少 2 个胜/败条件；公式用伪代码，不允许写 'TBD/根据情况'。



### 事件与反馈表 `event-feedback`
tags: 事件, 反馈, 奖励, 惩罚, 提示
把变量变化映射为可感知事件 + UI 反馈 + 奖励/惩罚。

用 markdown 表格列出：| 触发条件 | 事件名 | UI 提示 | 数值变化 | 玩家可选回应 |。每条要可在 HTML 中实现。

## 叙事设计（5）

### 分支叙事与状态机 `branching-narrative`
tags: 分支, 节点, 选择, 结局, 互动小说, story
把线性叙事或新构思拆为节点、选择、条件、变量、结局矩阵的可执行结构。

用 JSON 输出：
{ nodes: [{ id, title, body, choices: [{ label, target, requires?, sets? }] }],
  endings: [{ id, title, condition, summary }] }
至少 8 个节点、至少 2 个分支节点、至少 2 个结局；条件用变量表达式（如 favor>=3）。
保住原作禁改约束：核心人物动机/关键事实/世界规则不可修改。



### 小说原作改编流程 `story-to-game`
tags: 小说改编, 原作, 分支拓扑, 风格锚点, 互动阅读, 红线逆命
把线性小说改编为可玩的分支剧情结构，先做原作索引、风格指纹、分支拓扑、状态系统和结局矩阵。

必须先建立内部规划：原作摄入/记忆索引、风格指纹、节奏曲线、分支拓扑、状态系统、结局矩阵；不能直接把原文压缩成几个节点。
每个选择都必须从当前场景自然长出，并在下一屏有可见回响；多个选项不能无差别跳同一段。
选项不能引用玩家尚未知晓的人名/概念；说话选项写直接台词，不写“说/问/声明”。
长篇/中篇要先做垂直切片范围；如要求可试玩第一幕，节点数、结局、成就、锁定选择和道具/地图必须量化。
结局前必须有收束节点；成就数量应大于结局数量；分支线不能两三句草率收场。



### 结局矩阵设计 `ending-design`
tags: 结局, 结尾, 多结局, ending
围绕核心张力给出 2-5 个差异化结局，附触发条件与情感色彩。

每个结局：标题 + 一段 80-150 字结尾文案 + 触发条件（变量阈值/选择路径）+ 情感色（释然/苦涩/扭曲胜利等）。避免 '好/坏结局' 这种二元化。

### 角色设计 `character-design`
tags: 角色, 人物, 立绘, 对白, character
为关键角色写出动机/关系网/外貌锚点/标志性话术，作为后续生成的依据。

每个角色：姓名 / 标签（年龄+身份+特征）/ 动机（想要+不想要）/ 关系网（与其他角色的张力）/ 外貌 3-5 个锚点 / 对白调性（一句样例）。

### 世界观与设定 `worldbuilding`
tags: 世界观, 设定, 题材, 风格, world, lore
建立题材、规则、时代/地点、视觉/语言基调、不可破坏约束。

字段：题材标签 / 时代地点 / 视觉关键词 5-8 / 语言基调 / 核心规则 3-5（玩家/读者必须知道的设定法则） / 禁改约束（不可被剧情打破的事实）。

## 前端（21）

### HTML 互动阅读产品化 `novel-to-html-game`
tags: 互动阅读, HTML游戏, 背包, 地图, 道具, 当铺, 结局图鉴, 红线逆命
把已改编的小说分支结构做成高质量 HTML 互动阅读游戏，而不是简单文字按钮页。

最低成品标准：启动页、阅读/选择界面、状态 HUD、背包、目标、回想/回溯、存档、成就、结局图鉴、移动端响应式。
RPG 化模块：systems.stats、systems.items、systems.map.locations、pawnshop/shop、nodes、achievements/endings；锁定选项必须显示 conditionReason。
首个重要道具要有获得弹层和用途说明；需要道具的选项要提前可见但锁定。
地图不能只是目录，要有当前位置、地标、开放/未开放状态、地点描述和行动结果卡。
交易、搜证、赠礼、投毒等收益行为必须有 once/消耗/风险/冷却，禁止无限刷数值。
localStorage 存档要扁平，历史长度有限，不能把完整快照递归塞进历史。



### 单文件 HTML 实现 `html-singlefile`
tags: html, 单文件, 原型, 可玩
把设计落到一个可双击运行的单文件 HTML（含 style/script，无依赖）。

硬要求：
- 一次性 <!doctype html>...</html>，不要外部 CDN/import；
- file:// 下可运行；图片用 SVG 内联或 CSS 形状；
- UI 中文、暗色风格、移动端友好；
- 玩法状态用纯 JS 变量管理；DOM 渲染用 querySelector + textContent；
- 优先收口闭合到 </html>；不写 TODO 占位。



### 游戏 UI 模式 `html-game-ui`
tags: UI, 界面, 按钮, 对话框, 状态栏
游戏专用 UI 组件：状态栏 / 选项按钮组 / 对话框 / 结局画面。

状态栏顶部 sticky；选项按钮要明显可点（border + hover 反馈）；对话框分 narrator/character 两种风格；结局画面用全屏覆盖 + 重新开始按钮；移动端按钮高度≥44px。

### 手机 APP 模拟界面 `phone-app-sim-ui`
tags: 手机, APP, 消息, 备忘录, 日记, 相册, 浏览器, 桌面, 锁屏, 通知
把玩法承载在模拟手机系统里：主屏、锁屏、通知、多个可进入 APP、APP 内真实列表/详情/搜索/解锁交互。

禁止把 APP 入口降级成一组剧情选择按钮；玩家必须先看到手机外框、锁屏/主屏、图标网格和状态栏。
每个 APP 都要有独立 view 与交互：消息=联系人列表→聊天详情；备忘录/日记=列表→正文；相册=缩略图→照片详情；浏览器=地址栏/搜索/历史。
选择行为应表现为点击图标、打开会话、搜索关键词、输入密码、查看条目、解锁隐藏内容，而不是 '你要先查看哪个？' 的选项阅读器。
数据结构优先使用 apps/messages/notes/diary/photos/browserHistory/flags/passwords/chains，不要默认使用 NODES/choices。
UI 反馈包括通知横幅、红点、锁定态、Toast、返回键、Home 指示器和已读/未读状态。



### 前端状态机 `html-state-machine`
tags: 状态机, 节点, 切换, 渲染
在 HTML 内用纯 JS 实现节点状态机，根据 currentNode 渲染。

全局 state = { node, vars, history }；render(node) 根据 node.kind 切换渲染；choose(choice) 应用 sets / 切换节点；用 sessionStorage 保存。

### CSS 美学与排版 `html-css-aesthetic`
tags: css, 样式, 排版, 字体, 暗色
用最少 CSS 营造可信的画面感：留白、字号阶梯、阴影、圆角、强调色。

字号阶梯 11/13/16/22/32；行高 1.5；圆角 8/12/16；阴影用 rgba 黑+大模糊；强调色不超过 2 个；段落最大宽度 60ch。

### Canvas 2D 实现 `html-canvas`
tags: canvas, 画布, 2d
用 <canvas> 绘制 2D 游戏画面。

结构：getContext('2d') → requestAnimationFrame 循环 → state 更新 → 重绘；坐标系记得 devicePixelRatio 处理。

### SVG 图形 `html-svg`
tags: svg
在 HTML 内联 SVG 表达可缩放图形。

viewBox 表达坐标系；preserveAspectRatio 控制缩放策略；用 fill/stroke 而非 width/height 控制粗细。

### CSS 动画 `html-css-animation`
tags: 动画, transition, keyframes
用 transition / @keyframes 营造平滑反馈。

短交互用 transition；持续动效用 keyframes；不要给关键 UI 状态加 >300ms 的动画。

### 输入控制（键盘/触屏） `html-input-control`
tags: 键盘, 触屏, input, 手势
处理 keydown / pointerdown / touch 与防误触。

桌面用 keydown，移动用 pointerdown；同时绑定，避免重复触发；移动端按钮 ≥ 44px。

### 游戏主循环 `html-game-loop`
tags: 主循环, loop, raf
requestAnimationFrame 主循环 + 时间步。

用 dt = (now - last)/1000 做时间无关动画；逻辑步固定（如 1/60 s）；渲染步可变；累计器避免漂移。

### 本地存档 `html-storage-save`
tags: localStorage, 存档, save
用 localStorage 存玩家进度。

key 用命名空间（如 game.save.v1）；存 JSON.stringify(state)；版本字段便于以后兼容；try/catch 防 quota。

### 响应式布局 `html-responsive`
tags: 响应式, responsive
移动/平板/桌面三套断点。

断点 ≤480 / ≤768 / ≥1024；优先用 flex/grid + min-content；避免 px 锁定字号，用 clamp()。

### 无障碍 `html-accessibility`
tags: a11y, 无障碍, 对比度
对比度、键盘可达、aria-label。

正文对比度 ≥ 4.5:1；按钮可 Tab 聚焦并可见聚焦圈；图像必须 alt；动效尊重 prefers-reduced-motion。

### 极简数据绑定 `html-data-binding`
tags: 数据绑定, render
用 render(state) 全量重渲染避免散乱 DOM 操作。

保持 state → DOM 单向；事件只 setState 然后 render；避免直接读取 DOM 当作状态来源。

### 脚本模块化 `html-modular-script`
tags: 模块, module
单文件下用 IIFE / namespace 分块。

把 state / engine / view / input 各放一个 const 命名空间；不要把所有函数堆在全局。

### 性能与节流 `html-perf`
tags: 性能, 节流, 防抖
节流/防抖/批量 DOM 更新。

高频事件用 rAF 合并；复杂列表用 documentFragment 一次性插入；避免每帧 querySelector。

### 错误兜底 `html-error-boundary`
tags: 错误, 错误处理
全局 onerror / onunhandledrejection 收口。

`捕获后展示一个简单的错误提示与"重启"按钮，避免整页白屏。`

### 单页营销页 `html-onepager`
tags: 落地页, 营销页, landing
单文件落地页：英雄区 + 功能 + 证言 + CTA。

首屏 7 秒内传达：是什么 / 谁用 / 为什么用 / 立即行动。CTA 至少出现 3 次，颜色一致。

### 表单交互 `html-form-ux`
tags: 表单, form
实时校验 + 友好错误。

失焦时校验（不打断输入）；错误信息说原因 + 建议；提交按钮在校验通过前禁用并解释为何禁用。

### 键盘快捷键 `html-keyboard-shortcut`
tags: 快捷键, shortcut
单字符与组合键映射。

`避免与浏览器默认快捷键冲突；提供"按 ? 看快捷键"帮助面板。`

## 模拟器（4）

### 经营/资源仿真 `sim-economy`
tags: 经营, 资源, 供需, 经济, 模拟器
为经营类作品设计资源流（采购→加工→销售→反馈）+ 平衡曲线。

至少 3 类资源（流入/流出/库存）；每类给采购成本、加工系数、销售收入；时间尺度（日/周）；3 个难度档位的初始数值表。

### 关系/养成系统 `sim-relationship`
tags: 养成, 关系, 好感, 羁绊, 感情, AVG, 嫂嫂
处理人物间好感/信任/欲望/疏远等多维关系演化。

每对关键关系建一个数值（如 trust 0-100, tension 0-100, distance 0-100）；
事件影响关系：每次互动给出 ΔX 值；
至少 3 个里程碑（如 trust≥30 / 60 / 90 解锁不同剧情）；
处理伦理边界：明确禁线，不在禁线区域设计奖励性叙事。



### 饭圈/前嫂嫂模拟器 `idol-fandom-simulator`
tags: 前嫂嫂, 嫂嫂, 饭圈, 热搜, 塌房, 公关, 粉丝, 泡泡, FRONT, 叙事权
面向架空娱乐圈/饭圈幻想的手机模拟器：公开舆论、私密关系、证据管理、危机公关和多结局。

核心张力：private intimacy + public fandom gaze + limited agency + narrative ownership；所有角色/账号/事件必须架空，不映射真人。
不要把题材降级为静态聊天或剧情选项。稳定主循环：新热搜阶段 → 3-5 个日常行动消耗 AP → 查看 Feed/FRONT/私信/相册/浏览器/PR台/地图 → 处理事件簿 unresolved crisis → 结算数值/解锁 → 进入下一阶段 → 结局图鉴。
固定系统决定状态、解锁、结局和成就；AI 只可作为评论/私信/粉丝泡泡纹理，核心进度不能依赖 AI。
HUD 至少包含 AP、热度、证据、风险、尊严、好感、现金/公关资源；每个行动必须有 tradeoff。
必须包含模块：Home/角色设置、社交 Feed/热搜榜/评论区、FRONT/Bubble 粉丝气泡、私信 IM 且底部输入框可发消息、证据/相册锁、浏览器/搜索、公关台/商店、地图地点、localStorage 成就和结局图鉴；主屏 APP 图标必须是 button 或带 data-app 的可点击元素。
阶段建议 5-7 个；结局至少 6 个，覆盖叙事夺权、清白退场、热搜反噬、保护他人、旧爱复燃但不公开、被全网续写。



### 压力/抉择系统 `sim-stress-loop`
tags: 压力, 抉择, 道德, 两难, 心理
给玩家持续的两难抉择 + 压力累积反馈。

压力 0-100 缓涨；高压触发坏事件；抉择必须有 '都不完美' 的选项；显式给出每个选项的 short-term 与 long-term 影响。

## 视觉（5）

### 概念图 Prompt 设计 `concept-art-prompt`
tags: 概念图, 立绘, 场景, prompt
为图像模型写出可控的英文 prompt（含主体/光线/构图/材质/风格关键词）。

结构：[主体] [动作/姿态], [场景与光], [构图角度], [材质], [风格关键词 2-3], [后处理]。示例：'a young woman in red velvet dress, dim radio station at night, mid-shot from below, gritty film noir, kodak portra'。

### UI 草图概念图 `ui-mockup`
tags: UI 概念图, 界面草图, mockup
为 UI 设计生成可参考的草图。

明确指定：屏幕尺寸（375x812 等）、深色/浅色、关键元素（按钮位置/图标/文字层级）。示例：'mobile dark UI mockup, story choice screen, 2 buttons centered, status bar top, 9:16'。

### 视觉风格板 `style-board`
tags: 风格板, moodboard, 色彩, 氛围
为项目建立统一的视觉锚（色板 / 关键词 / 引用艺术家）。

5 个色（含主色/辅色/强调色/警示/中性灰）；6-8 个氛围关键词；2-3 位风格参考艺术家或电影。后续所有图像 prompt 都要带上风格锚关键词。

### 概念图风格栈 `concept-art-style`
tags: 风格, concept art
组合主体 + 光影 + 构图 + 风格关键词。

三层关键词：[主体动作][环境光线][风格艺术家/介质]；负面提示词剔除水印/低质量。

### UI 设计规范 `ui-design-spec`
tags: UI, spec, 设计规范
把视觉系统写成可复用的颜色/字号/间距/圆角/阴影规范。

至少给：色板 6 色、字号阶梯 5 级、间距 4/8/12/16/24、圆角 6/10/14、阴影 2 级。

## 音频（3）

### 音频脚本设计 `audio-script`
tags: 配音, TTS, 脚本, 对白
为关键场景写可被 TTS 朗读的中文脚本（≤120 字）。

短句优先；标点完整（中文逗号、句号、问号）；明确情绪（如平静低语 / 急促）；避免英文夹杂。

### 配乐方向描述 `bgm-prompt`
tags: bgm, 配乐, 氛围, 音乐
为音频模型给出可控的配乐方向描述。

结构：[基调]+[节奏 bpm]+[关键乐器]+[情绪]+[长度]。示例：'ambient piano + low strings, 60bpm, melancholic and warm, 30s loop'。

### 角色配音方向 `voice-character`
tags: 配音, voice
为关键角色定义声线/年龄感/情绪基调。

字段：性别 / 年龄 / 节奏 / 音色（暖/冷）/ 情绪基调；给 1-2 句样例台词。

## QA（2）

### 可玩性测试清单 `qa-playtest`
tags: QA, 测试, 可玩, playtest
为可玩原型生成具体测试场景与通过标准。

用 markdown 表：| 场景编号 | 操作步骤 | 期望结果 | 风险 | 优先级 |。覆盖：开场 / 至少 1 个分支 / 每种结局 / 数值边界 / 移动端窄屏。

### HTML 单文件检查 `qa-html-checklist`
tags: HTML 检查, 单文件, 兼容
针对单文件 HTML 输出做完整性/兼容性/可玩性 checklist。

检查：<!doctype + </html> / 无外链 / 移动端 viewport / 暗色 OK / 至少 1 个交互可触发 / 无 console.error / 字数与游戏长度匹配。

## 发布（1）

### 发布包结构 `release-package`
tags: 发布, 打包, 导出, zip
把成果整理为可分发的发布包结构（HTML + 资产 + 说明）。

结构：index.html / assets/（图音）/ README.md（玩法说明 + 致谢）。文件名用 ASCII 安全字符；HTML 单文件优先内联，外部资产仅在必要时拆出。

## 写作（1）

### 文风与语气 `tone-and-voice`
tags: 文风, 语气, tone
保持作品在不同片段间一致的文风。

确定 3 个轴：句长（短/中/长）/ 词汇（口语/书面/文学）/ 视点（一/二/三人称）。每个生成片段开始前先回顾这三轴，避免风格漂移。

## 工程（1）

### 结构化 JSON 输出 `structured-json`
tags: json, 结构化, 数据
为后续步骤可消费的 JSON 严格遵守 schema。

永远在 ```json ... ``` 中输出；字段名用英文 snake_case 或 camelCase；不要 trailing comma；不要注释；尽量平铺，深度不超过 3 层。

## 审查（1）

### 伦理边界与安全 `ethical-boundary`
tags: 伦理, 安全, 边界, 敏感
在处理涉及关系、暴力、青少年保护等敏感题材时主动设置边界。

明确禁线：未成年性描写一律禁止；现实存在的真人人格不可被赋予可疑剧情；身份认同不应被设计为奖励/惩罚；涉及亲密关系不要给出未经同意可被强迫的设计。受阻时给出可继续的替代方向。

## 思考分析（16）

### 第一性原理 `first-principles`
tags: 第一性, 本质, 根本, First principles
把复杂问题剥到不可再分的基本事实再重新构建。

1) 列出当前对问题的所有假设；2) 对每条假设问 '这真的必然成立吗'；3) 把通过审查的事实作为基本砖块；4) 从砖块重新组合答案，不依赖类比与惯例。

### 5 Whys 根因分析 `five-whys`
tags: 根因, 为什么, 5 whys, 原因
对一个症状连续追问 5 次为什么直到触及根因。

格式：症状 → 为什么(1) → 答 → 为什么(2) → 答 ... 直到找到可干预的根本原因；不要在第 2 层就停下。

### MECE 拆解 `mece`
tags: MECE, 结构化, 互斥穷尽
保证拆分维度相互独立、完全穷尽。

拆完后做两个检查：① 任两子类是否有重叠？② 所有子类合起来是否覆盖全集？任一不满足就重拆。

### SWOT 分析 `swot`
tags: SWOT, 优劣势, 机会威胁
Strengths / Weaknesses / Opportunities / Threats 四象限。

S/W 看内部，O/T 看外部；每格至少 3 条具体事实，不写 '强 / 优秀' 这种空词；末尾给 1-2 个交叉策略（如 SO/ST）。

### Pre-mortem 失败预演 `pre-mortem`
tags: 失败, 预演, premortem, 风险
假设方案已经失败，倒推可能的失败原因。

把时间快进到 6 个月后宣告失败的那一刻，列出最可能的失败原因 5-8 条，每条标可监测信号 + 缓解措施。

### 魔鬼代言人 `devils-advocate`
tags: 反方, 质疑, 对立
对当前方案专门挑毛病。

假设你必须否决该方案：列出 3-5 个最强的反对理由 + 每条对应的反例或数据；末尾说哪些反驳应被吸收进方案。

### 正反 + 修正 `pros-cons-fixes`
tags: 利弊, 对比
比单纯的 pros/cons 多一列：每个 con 给修正方案。

三列表格：优点 / 缺点 / 缓解或修正。当 cons 没有可行修正时，明确写 '无法缓解'，不要假装。

### OODA 循环 `ooda-loop`
tags: OODA, 决策
Observe-Orient-Decide-Act，处理快变化。

Observe 列事实，Orient 解释含义，Decide 给具体动作，Act 立即执行；下一轮重启 Observe。

### 费米估算 `fermi-estimation`
tags: 估算, 数量级
用合理假设链估算量级未知的数。

把目标量拆成 3-5 个可估的因子，每个因子写出取值与依据，相乘后给 0.5x-2x 的区间。

### 二阶思考 `second-order-thinking`
tags: 二阶, 副作用
看决定的下一层、下下一层后果。

对每个直接后果再问 'and then what'，至少 2 层；标注哪些后果会反过来削弱原决定。

### SMART 目标 `smart-goal`
tags: SMART, 目标, 可衡量
把模糊目标转成 Specific/Measurable/Achievable/Relevant/Time-bound。

写出五项各一句话；如果某项填不出来，说明目标尚未成熟，应先打回澄清。

### Job Story 用户旅程 `user-job-story`
tags: 用户故事, JTBD, 用户场景
用 'When [情境], I want to [动作], so I can [收益]' 表达需求。

至少写 3 条不同情境；情境必须可观测；收益必须可让用户认同；动作不要绑定具体方案。

### RACI 责任矩阵 `raci`
tags: 分工, 责任, RACI
Responsible/Accountable/Consulted/Informed 四角色。

为每件事配且只配 1 个 A，1 个或多个 R，C/I 可空。

### 成本效益分析 `cost-benefit`
tags: 成本, 收益, ROI
列出全部成本与收益（含隐性），给净值与不确定性。

成本：开发 + 机会 + 心智 + 维护；收益：直接 + 间接 + 选项价值；标注每项的可信度。

### 抽象阶梯 `ladder-of-abstraction`
tags: 抽象, 具体, 层次
在'具体 ↔ 抽象'阶梯上判断当前讨论是否在合适层级。

若卡在抽象层，强制下到具体例子；若被例子淹没，强制上到抽象规则。每次切换要明示。

### 检查清单思维 `checklist-thinking`
tags: 清单, checklist
把高频犯错的步骤写成清单逐项打勾。

每条 ≤ 12 字，可二元判断；清单 ≤ 12 条；执行时按顺序勾选，不允许凭记忆跳过。

## 创作通用（22）

### 叙事弧 `narrative-arc`
tags: 叙事弧, 起承转合, 三幕
把内容编入开端-上扬-高潮-下行-收束的曲线。

标出每段的张力等级（0-5）；至少有一处张力最低点（喘息）和一处最高点（高潮）；不要让张力始终持平。

### Show, don't tell `show-dont-tell`
tags: show, tell, 细节
用具体动作/感官细节代替抽象形容。

替换规则：'他很愤怒' → 写他的动作（指节发白/掀翻椅子）；'她很美' → 写一个能引起注意的具体细节而不是评价。

### 钩子开场 `hook-opening`
tags: 钩子, hook, 开头
前 3 句必须制造好奇/张力/反差。

三种钩子：① 反预期事实 ② 进行中的冲突 ③ 一个问题。避免铺垫式的'天气怎么样'式开头。

### 场景设计 `scene-design`
tags: 场景, scene
每个场景必须有目标、冲突、转折、价值改变。

写完一段后自检：① 谁要什么？② 谁/什么阻挠？③ 转折点在哪一句？④ 场景结束时人物境况比开始时好/坏？答不出 → 重写。

### 对白工艺 `dialogue-craft`
tags: 对白, 对话
对白不是闲聊：每句要么推进信息要么揭示关系。

尽量短句；少用形容语气词；让人物用各自的口头习惯（学历/性格）；潜台词大于明说。

### 潜台词 `subtext`
tags: 潜台词, 暗示
重要情绪不直说，让读者从行为/沉默/选词推断。

每个关键场景至少留一处只能从动作而非对白读出的情绪点。

### 伏笔与回收 `foreshadow-payoff`
tags: 伏笔, 回收
前期埋下小细节，后期产生意义。

每个伏笔登记 ID + 埋设位置 + 期望回收位置；写完检查每个 ID 是否回收（保留意外不回收的也可，但要刻意）。

### 主题与中心思想 `theme-and-control-idea`
tags: 主题, 中心思想, Theme
用一句陈述句锁定作品价值判断。

格式：'当 X 时，会发生 Y'。每个场景都应能回答：本场如何论证或挑战这一主题。

### 语气滑杆 `tone-sliders`
tags: tone, 语气, 风格
用三轴具体描述目标语气：句长/词汇/亲疏。

示例：句长 短-中；词汇 口语；亲疏 第二人称亲近。生成时按此校验，不随段落漂移。

### 标题工艺 `headline-craft`
tags: 标题, headline
标题要有：信息 + 反差 + 限定 + 利益。

做 6-8 个候选；自检：能否一眼看出对谁有用？是否含具体数字或动作？

### TL;DR 摘要 `tldr-summary`
tags: 摘要, TLDR
用 1-3 句话浓缩长文最关键信息。

至少回答：① 这是什么？② 为什么重要？③ 我该做什么？

### 一句话故事推销 `story-pitch`
tags: pitch, logline
用一句话讲清主角+目标+对抗+卖点。

格式：[特定主角] 在 [情境] 下要 [目标]，但 [对抗/代价]。

### 视角与人称 `perspective-pov`
tags: 视角, 人称, POV
明确用谁的眼睛看世界，并保持一致。

选 1：① 第一人称限制 ② 第三人称限制 ③ 第三人称全知。每场景只用一个；切换需明显分段。

### 世界规则 `world-rules`
tags: 世界规则, rules, lore
明确禁/允/代价/例外四类规则。

至少 5 条：① 什么不可能 ② 什么必须付代价 ③ 什么稀缺 ④ 什么循环 ⑤ 什么例外。

### 角色原型对照 `character-archetype`
tags: 原型, Archetype
用经典原型快速定位人物功能。

原型表：英雄/向导/守门人/阴影/骗子/盟友/Herald。给每个主要人物挑 1-2 个，标注作用。

### 角色冲突轴 `character-conflict`
tags: 冲突, 矛盾
为每个主角配置 3 类冲突：内部/人际/外部。

缺任一类的角色会显得扁平；冲突之间最好彼此相关而非孤立。

### 道具与象征 `props-symbol`
tags: 道具, 象征
选 1-2 个反复出现的物件承载主题。

每次该物件出现时其含义应有一点演化；作品末尾的含义应与开篇不同。

### 环境感官 `setting-sense`
tags: 环境, 感官, 氛围
至少触达三种感官（视/听/触/嗅/味）建立可信场景。

禁止只写视觉；至少有 1 个声音 + 1 个非视觉细节；不要堆砌形容词。

### 节奏控制 `pacing-rhythm`
tags: 节奏, pacing
用句长与段落密度控制阅读速度。

高潮处用短句短段；铺陈处可长段；不要连续 5 段都同样的密度。

### 张力曲线 `narrative-tension`
tags: 张力, tension
用一组数值曲线刻画作品的张力起伏。

把作品切成 8-12 段，每段打 0-5 张力分；曲线必须有上升、回落、最高峰。

### 悬念收尾 `cliffhanger`
tags: 悬念, cliffhanger
在篇章/章节末尾留一个未决问题让读者非看下一章不可。

三种类型：① 即将到来的揭露 ② 未做出的关键决定 ③ 即将爆发的冲突。

### 笑点与幽默 `joke-craft`
tags: 幽默, 笑点
笑点结构 = 设置 + 反转 + 节奏。

三句法：① 建立期待 ② 推到极端 ③ 反转。短句优先；不要解释自己的笑话。

## 游戏专项（18）

### 卡牌 Roguelike 设计 `card-roguelike`
tags: 卡牌, Roguelike, deckbuilder
Slay-the-Spire 范式：构筑/事件/Boss/遗物。

三大循环：单局战斗（出牌 → 抽 → 弃 → 洗）、单层（节点选择 + 事件 + 商店 + 精英 + Boss）、跨局（解锁/挑战币）；卡牌至少 4 类（攻击/防御/技能/能力），保证组合涌现。

### 三消玩法 `match-three`
tags: 三消, match3, 消除
处理消除核心 + 关卡目标 + 助力体系。

至少 3 种特殊消除（直线/十字/全屏）；目标多样（收集/清障/限步）；难度曲线靠步数 - 障碍 - 颜色数 - 助力 4 个旋钮。

### 塔防设计 `tower-defense`
tags: 塔防, tower defense, td
塔类×波次×路径×经济四要素。

至少 4 种塔（伤害类型不同）×3 种敌（抗性不同）×明显路径分支；波次节奏：升压-空闲-Boss。

### 节奏游戏 `rhythm-game`
tags: 节奏, 音游, rhythm
音轨与判定窗口设计。

判定窗口随难度收紧；至少 3 难度；按键密度遵循 BPM；避免 30 秒以上的无操作真空。

### 平台跳跃 `platformer`
tags: 平台, 跳跃, platformer
跳跃手感、关卡语法、coyote-time。

跳跃必须有 coyote-time（5-7 帧）+ 跳跃缓存；关卡按 '教 → 测 → 变奏 → 大考' 推进；死亡惩罚低、重试快。

### 生存类玩法 `survival-loop`
tags: 生存, 饥饿, 体力
饥饿/体力/温度等多压力同时下降，玩家在资源采集 - 消耗中保持平衡。

每个压力轴有自然下降速度 + 行动加速 + 资源缓解；早期教学要让玩家死过一次。

### 解谜设计 `puzzle-design`
tags: 解谜, puzzle
以教-练-考的小循环铺垫机制叠加。

每个机制：第 1 关教，第 2-3 关练熟，第 4 关与上一机制组合考验；不要在没教过的情况下放组合考。

### 恋爱养成系统 `dating-sim`
tags: 恋爱, 养成, dating, 好感度
多线好感 + 关键事件 + 多结局。

为每位可攻略对象配置：好感 0-100、3 个里程碑、独立支线 5+ 节点、独立结局 ≥1；明确禁线。

### 放置/增量游戏 `incremental-idle`
tags: idle, incremental, 放置
指数增长 + 转生重置 + 自动化。

前 30 分钟手感最关键；每 1 分钟应有可见进步；2-3 个数值形成相互依赖；重置应让玩家更强而不是从零。

### 叙事 RPG `narrative-rpg`
tags: RPG, 叙事 RPG
属性/技能 + 选择影响剧情。

属性影响对话选项是否解锁；至少 3 个对话选择会被后续场景记住；不要做 '看似有选择实则汇流' 的伪分支。

### 潜行玩法 `stealth-mechanic`
tags: 潜行, stealth
感知锥 + 警觉等级 + 干扰物。

敌人三态：警觉 / 调查 / 攻击；环境必须给玩家工具（暗影/物件/声响）；失败后允许重试不必读档。

### 关卡流 `level-flow`
tags: 关卡, level
节奏: 引入-紧张-高潮-喘息。

每个关卡至少有一个 'Aha' 瞬间；不要相邻两关重复同一玩法骨架；末尾留一个钩子接下一关。

### Boss 战设计 `boss-fight`
tags: Boss, boss战
Boss = 知识检查 + 节奏阶段 + 视觉高峰。

至少 3 阶段；每阶段引入一个新机制或反转；血量不能太厚，节奏靠机制变化推进。

### 教学设计 `tutorial-design`
tags: 教学, tutorial, 新手
用做-看-想三段教学代替弹窗罗列。

每条机制：① 让玩家做一次（被引导） ② 让玩家自由练 ③ 让玩家面对一个真正考验；少用文字描述，多用情境。

### 成长曲线 `progression-curve`
tags: 成长, 等级, 曲线
经验/资源/能力的增长函数与挑战难度匹配。

玩家能力线斜率应略陡于挑战线；中后期允许玩家'刷一会'追平挑战，但不要永远追不上。

### 付费与公平 `monetization-fairness`
tags: 付费, 公平, p2w
保证免费玩家可达全部内容，付费只换时间/外观。

至少明示：① 哪些可以付费购买 ② 是否影响竞争力 ③ 是否有保底（pity）；远离 p2w。

### 活动/限时玩法 `live-event`
tags: 活动, 限时, 运营
定期限时玩法保新鲜感与回流。

节奏：周更小事件 / 月度大事件 / 季度限定；奖励要有可见但不抢核心成长。

### 游戏作品圣经 `narrative-game-bible`
tags: bible, 圣经, 游戏设定
把题材/世界观/核心循环/系统/UI 风格定型成一份规范文件，后续所有制作以此为准。

字段：题材 / 玩家承诺 / 核心循环 / 主要系统 / UI 风格 / 视觉关键词 / 音乐基调 / 禁线。

## 多模态（2）

### 图像内容分析 `image-analysis`
tags: 图像分析, ocr, 看图
对用户上传的图片做内容/结构/情绪/文字识别。

输出结构：① 主体与场景 ② 关键文字（如有） ③ 风格与情绪 ④ 与用户问题的关系。

### 文档摘要 `doc-summarize`
tags: pdf, docx, 摘要
对附件文档抽出 5-10 条要点 + 1-2 句 TLDR。

先 TLDR；再分章列要点；最后给 3 条可执行建议或问题。

## 运营（7）

### 对话/聊天记录导出 `chat-export`
tags: 对话导出, 聊天记录, 归档, export chat
把当前线程对话整理成可读的 markdown / json / txt 文件。

结构：标题 + 时间戳 + 双方姓名（用户 / Agent）+ 按时间顺序的消息。代码块保留原 fenced 标记；过长内容可分文件。导出对象是消息流本身，不是产物文件。

### 会议纪要 `meeting-notes`
tags: 纪要, 会议
把发言整理成 决策 / 行动项 / 风险 / 待跟进。

至少四节：① 决策 ② 行动项（owner+ddl）③ 待跟进问题 ④ 风险。每条可执行，不写概括语。

### 周报 `weekly-report`
tags: 周报, 汇报
本周成果/问题/下周计划三段式。

成果列结果不列动作；问题写阻塞而非借口；下周计划要可衡量。

### OKR 拆解 `okr`
tags: okr, 目标
Objective + 3-5 个可量化 Key Results。

Objective 可激励但不可衡量；KR 必须可衡量、有数字；KR 总数 3-5 条不要更多。

### 知识卡片 `knowledge-card`
tags: 知识卡, 卡片笔记
1 个观点 + 1 个例子 + 1 个反例 + 1 个出处。

卡片要原子化：一张卡只装一个观点；可被独立检索与引用。

### 访谈问题清单 `interview-questions`
tags: 访谈, 调研
围绕用户/专家访谈设计开放式问题清单。

结构：背景 / 现状 / 痛点 / 触发场景 / 替代方案 / 期望；避免引导性问题。

### 决策日志 `decision-log`
tags: 决策, ADR
记录决策的背景/选项/选择/未来回看条件。

格式：① 背景 ② 候选方案 ③ 评估维度 ④ 选择 ⑤ 何时回看。
