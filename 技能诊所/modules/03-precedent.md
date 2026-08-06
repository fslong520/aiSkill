# 模块三：先例研究

## 触发时机

创建技能前自动执行，或用户显式要求"查重"、"有没有类似技能"。

## 流程

1. 从需求中提取关键词（功能域、输入输出、触发场景）
2. 本地搜索：`Glob + Grep` 扫描 `~/.codebuddy/skills/*/SKILL.md`
3. 远程搜索：`npx skills find <query>` 查 skills.sh
4. ClawHub 搜索：`clawhub search <query>`
5. 汇总结果，按相似度排序
6. 输出建议：可复用 / 可合并 / 需新建

## 输出格式

```
先例研究结果：
| 来源 | 技能名 | 相似度 | 可复用部分 |
|------|--------|--------|-----------|
| 本地 | 搬题姬 | 80% | URL抓取、文件结构 |
| skills.sh | xxx-skill | 60% | 数据验证逻辑 |
| 结论 | 建议合并搬题姬的URL模块，新建独立技能 |
```

## 相似度评估标准

| 相似度 | 标准 |
|--------|------|
| >80% | 高度相似，建议复用或合并 |
| 60-80% | 中度相似，可借鉴部分模块 |
| 40-60% | 低度相似，仅参考设计思路 |
| <40% | 无关，需新建 |

## 数据源接入

### 本地搜索

```bash
# 搜索所有技能的SKILL.md
Glob pattern="~/.codebuddy/skills/*/SKILL.md"

# 搜索关键词
Grep pattern="关键词" path="~/.codebuddy/skills/"
```

### 远程搜索

```bash
# skills.sh
npx skills find <query>

# ClawHub
clawhub search <query>
clawhub inspect <slug>
```

## AVOID

- AVOID 不搜就建，重复造轮子
- AVOID 只搜本地不搜远程
- AVOID 搜到类似技能却不告知用户
- AVOID 相似度评估过于宽松或严格
- AVOID 忽略用户选择权（复用/合并/新建）
