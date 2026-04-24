# 事件系统规则

## 事件结构

```json
{
  "id": "event_001",
  "type": "random",
  "stage": ["childhood", "youth"],
  "weight": 10,
  "conditions": {
    "age_min": 5,
    "age_max": 15,
    "attributes": { "intelligence": 8 },
    "race": ["human", "elf"],
    "world_tags": ["magic"]
  },
  "content": {
    "title": "神秘的老人",
    "description": "你在森林边缘遇到了一位神秘的老人...",
    "choices": [
      {
        "text": "上前搭话",
        "effects": { "wisdom": 2, "luck": 1 },
        "next_event": "event_002"
      },
      {
        "text": "绕道离开",
        "effects": { "caution": 1 }
      }
    ]
  }
}
```

## 事件类型

### 1. 随机事件 (random)

根据权重随机触发，无前置条件。

**类别**：
- 日常琐事（买菜、天气、小意外）
- 偶遇（陌生人、动物、物品）
- 发现（秘境、宝物、秘密）
- 灾难（火灾、瘟疫、袭击）
- 好运（意外收获、贵人相助）

**权重分配**：
```
日常琐事：50%
偶遇：20%
发现：10%
灾难：10%
好运：10%
```

### 2. 命运事件 (fate)

预设的人生节点，必定触发。

**人生节点**：
| 年龄 | 事件 |
|------|------|
| 0岁 | 出生（种族、家庭、天赋） |
| 5岁 | 天赋觉醒 |
| 10岁 | 教育选择 |
| 15岁 | 成人礼/志向选择 |
| 18岁 | 职业起点 |
| 25岁 | 人生抉择 |
| 35岁 | 中年危机/巅峰 |
| 50岁 | 人生回顾 |
| 60岁+ | 晚年事件 |
| 随机 | 死亡 |

### 3. 世界事件 (world)

根据世界状态触发，影响所有人。

**触发条件**：
```json
{
  "world_year": { "min": 1250, "max": 1300 },
  "world_tags": ["war", "disaster"],
  "random_probability": 0.1
}
```

**世界事件类型**：
- 战争爆发/结束
- 瘟疫流行
- 自然灾害（地震、洪水、干旱）
- 政权更迭
- 魔法潮汐变化
- 神灵显现
- 经济危机/繁荣
- 技术革命

### 4. 关系事件 (relationship)

根据人际关系触发。

**触发来源**：
- 家人（父母、兄弟姐妹、配偶、子女）
- 朋友
- 敌人
- 导师/学生
- 组织成员

**事件类型**：
- 关系建立/破裂
- 冲突/和解
- 合作/背叛
- 生离/死别
- 求助/支援

### 5. 选择事件 (choice)

玩家主动触发。

**触发方式**：
- 玩家说"我想去..."
- 玩家说"我想学..."
- 玩家说"我想找..."
- 玩家提出任何行动

**处理流程**：
1. 解析玩家意图
2. 判断可行性
3. 生成对应事件
4. 提供选项

## 事件生成算法

### 每回合事件数量

```
基础事件数 = 1
+ 丰富度调整（玩家偏好）
+ 人生阶段调整（少年期+1）
+ 幸运值调整（高幸运+1）
= 1-3个事件/回合
```

### 事件权重计算

```python
def calculate_weight(event, player, world):
    base_weight = event.base_weight
    
    # 属性加成
    attr_bonus = sum(
        player.attributes[attr] * modifier
        for attr, modifier in event.attr_modifiers.items()
    )
    
    # 阶段加成
    stage_bonus = 2 if player.stage in event.stages else 0
    
    # 世界状态加成
    world_bonus = sum(
        1.5 for tag in event.world_tags 
        if tag in world.current_tags
    )
    
    # 关系加成
    relation_bonus = sum(
        1 for rel in player.relationships 
        if rel.type in event.relation_types
    )
    
    # 前置事件检查
    if event.prerequisite and not check_prerequisite(event, player.history):
        return 0
    
    return base_weight + attr_bonus + stage_bonus + world_bonus + relation_bonus
```

### 事件结果计算

```python
def calculate_outcome(choice, player):
    # 基础效果
    effects = choice.effects.copy()
    
    # 属性修正
    for attr, value in effects.items():
        if attr in player.attributes:
            # 高属性更容易成功
            modifier = player.attributes[attr] / 10
            effects[attr] = value * (1 + modifier * 0.2)
    
    # 幸运修正
    if random() < player.attributes['luck'] / 100:
        effects = boost_positive_effects(effects)
    
    # 随机波动
    for key in effects:
        effects[key] *= random(0.8, 1.2)
    
    return effects
```

## 人生阶段事件池

### 婴儿期（0-3岁）

**事件类型**：
- 天赋觉醒征兆
- 家庭变故
- 被抱走/送人
- 意外事故
- 早慧表现

**特点**：
- 玩家选择受限
- 被动事件为主
- 奠定基础属性

### 童年期（4-12岁）

**事件类型**：
- 教育开始
- 初次冒险
- 建立友谊
- 发现兴趣
- 家庭影响
- 小型挑战

**特点**：
- 开始有主动选择
- 属性快速成长
- 建立早期关系

### 少年期（13-17岁）

**事件类型**：
- 学业选择
- 初恋
- 叛逆事件
- 天赋发展
- 社会初步接触
- 成人礼

**特点**：
- 选择影响人生方向
- 情感事件增多
- 社会角色开始形成

### 青年期（18-35岁）

**事件类型**：
- 职业选择/发展
- 婚恋
- 冒险探索
- 社会地位变化
- 重大抉择
- 成就/失败

**特点**：
- 事件影响最大
- 多线发展可能
- 人生巅峰期

### 中年期（36-55岁）

**事件类型**：
- 家庭责任
- 事业危机/转机
- 健康问题
- 子女教育
- 社会地位巩固
- 中年危机

**特点**：
- 稳定为主
- 传承事件
- 可能出现衰退

### 老年期（56岁+）

**事件类型**：
- 退休/退隐
- 回忆往事
- 传承遗产
- 健康恶化
- 人生总结
- 死亡

**特点**：
- 属性衰退
- 故事收尾
- 准备结局

## 特殊事件

### 连锁事件

```json
{
  "chain_id": "merchant_path",
  "events": [
    { "event": "meet_merchant", "age_min": 10 },
    { "event": "first_trade", "age_min": 12 },
    { "event": "merchant_guild", "age_min": 15 },
    { "event": "own_shop", "age_min": 18 }
  ],
  "rewards": {
    "complete": { "trait": "商道天才", "gold": 1000 }
  }
}
```

### 隐藏事件

```json
{
  "id": "hidden_dragon_blood",
  "hidden": true,
  "conditions": {
    "race": "human",
    "age_min": 15,
    "luck_min": 15,
    "previous_events": ["dragon_encounter_1", "dragon_encounter_2"]
  },
  "probability": 0.05
}
```

### 悲剧事件

```json
{
  "id": "family_tragedy",
  "type": "tragedy",
  "weight": 5,
  "conditions": { "family_status": "happy" },
  "content": {
    "title": "突如其来的噩耗",
    "description": "你的家中传来噩耗...",
    "choices": [
      { "text": "接受现实", "effects": { "trauma": 1, "maturity": 2 } },
      { "text": "寻求真相", "effects": { "determination": 1 }, "next_event": "investigate" }
    ]
  }
}
```

## 事件描述风格

### 叙事风格

```
第二人称："你走进..."
现在时："阳光洒在..."
感官描写："空气中弥漫着..."
情感渲染："你的心跳加速..."
```

### 选择设计原则

1. **每个选择都有意义** — 没有绝对正确答案
2. **选择有代价** — 得到意味着失去
3. **选择有后果** — 影响后续事件
4. **选择体现性格** — 塑造角色人格

### 描述模板

```markdown
## [事件标题]

[场景描述：时间、地点、氛围]

[事件正文：发生了什么]

**你的选择**：

1. [选项1] — [简短后果暗示]
2. [选项2] — [简短后果暗示]
3. [选项3] — [简短后果暗示]（可能需要特定条件）
```

## 事件数据存储

### 历史记录

```json
{
  "turn": 16,
  "year": 1263,
  "age": 16,
  "events": [
    {
      "id": "event_042",
      "title": "学院的邀请",
      "choice": "接受邀请",
      "effects": { "intelligence": 3, "gold": -50 },
      "story": "那一年，我收到了魔法学院的邀请..."
    }
  ]
}
```

### 事件统计

```json
{
  "total_events": 156,
  "by_type": {
    "random": 80,
    "fate": 25,
    "world": 15,
    "relationship": 20,
    "choice": 16
  },
  "by_outcome": {
    "positive": 60,
    "neutral": 50,
    "negative": 46
  }
}
```