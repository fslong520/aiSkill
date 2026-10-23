---
priority: 700
name: 星匣引擎
description: "{🎮} 从零开发 HTML 游戏：星匣创作台方法论（9形态识别+4阶段构建+118技能库） | 触发：做游戏、开发游戏、HTML游戏、小游戏、游戏原型、试玩版"
metadata:
  version: "1.0.0"
  trigger: "做游戏,开发游戏,HTML游戏,小游戏,游戏原型,试玩,roguelike,解谜,塔防,养成,模拟器,文字冒险,互动小说,平台跳跃"
---

# 星匣引擎

## Keywords

游戏开发、HTML5、单文件、形态识别、构建流水线、技能库、游戏设计、核心循环、状态机

## Summary

以星匣创作台（网易星匣平台同类工具）的方法论从零手写 HTML 游戏：先识别游戏形态，再按 4 阶段流水线构建（骨架→内容 JSON→扩写→整合美化），全程用 reference/skills-library.md 的 118 条技能细则作设计约束。

## Strategy

1. **识别形态**（见下表）：从用户需求提取关键词判定 9 种形态之一，形态决定数据容器与禁则
2. **设计**：从 @reference/skills-library.md 按题材取 2-5 条技能 body 作设计约束（grep id 取细则）
3. **构建**（4 阶段流水线，每阶段独立产出）：
   - 阶段1 骨架：完整 `<!doctype html>` 单文件，state/render/save/load/win-loss 就位，不写具体内容
   - 阶段2 内容数据：玩法内容 JSON（nodes/endings/items 等，按下表数量硬指标）
   - 阶段3 扩写：内容量不足则扩写节点/事件/文案
   - 阶段4 整合美化：数据接入骨架，CSS 打磨，自查修补
4. **验收**：过 QA 清单（qa-html-checklist：单文件无外部依赖/存档扁平/无 TODO 占位/选项皆有后果）+ 浏览器实测截图
5. **交付**：单 HTML 文件，浏览器直接打开即玩

## 九形态路由表

| 形态 | 识别关键词 | 数据容器 | 铁则 |
|---|---|---|---|
| phone-app-sim | 手机/APP/消息/相册/锁屏 | state/apps/messages/photos/flags/endings | 禁 NODES/choices 主结构，禁终端 PIN 壳 |
| interactive-reading-rpg | 小说改编/RPG阅读/背包地图 | systems{stats,items,map,pawnshop}/nodes≥80/endings≥8/achievements≥10 | 锁定选项须 conditionReason，存档扁平 |
| idol-fandom-sim | 饭圈/娱乐圈/热搜/偶像 | phases5-7/crisisEvents/feedPosts≥18 | 角色全架空，禁映射真人 |
| phone-shell-puzzle | 手机壳解谜/密码锁/拨号盘 | screens/puzzles/inventory/clues/timers | 手机仅为容器，单屏，禁多 APP 导航 |
| mechanic-game | 平台跳跃/射击/塔防/卡牌/三消/节奏 | entities/levels/rules/winLoss | 必须可操作系统+实时反馈+胜负条件，禁退化为阅读器 |
| systems-sim | 模拟经营/养成/资源/日程 | resources/schedule/events/actors | 必须资源/事件/时间推进闭环 |
| choice-narrative | 互动小说/分支剧情/多结局（仅明确要求时） | initialState/nodes/endings | 唯一允许 NODES/choices 主结构的形态 |
| freeform-game | 题材不明 | state/screens/systems/events | 禁默认生成阅读器，先选最适玩法结构 |
| visual/audio | 只要图/只要音乐 | 资产提示词 | 不进 HTML 构建 |

## 通用设计铁则

- 每个 choice 必须有 changes 后果，禁无差别跳转同一段
- 收益行为必须 once/消耗/风险 三选一
- 禁 TODO/占位符/"此处略"；节点正文禁元叙事词（玩家/节点/分支）
- 存档扁平，history 限长，禁递归快照
- 单文件无外部依赖（CDN 库可内联或按需引）

## 模型线路（供网页版创作台注入用，非本技能必需）

- b.ai：https://api.b.ai/v1，glm-5.3-flash（推理）+ qwen3.8-flash（文本），key 见 opencode.json provider.b-ai

## AVOID

- AVOID 把所有游戏默认做成"读文字→点选项"阅读器（仅 choice-narrative 形态可用）
- AVOID 跳过形态识别直接开写
- AVOID 骨架阶段就写大段具体内容（内容归阶段2）
- AVOID 一次生成完整游戏不分级（超长必截断，须按阶段推进）
- AVOID 交付前不实测（至少浏览器打开截图验证渲染）
