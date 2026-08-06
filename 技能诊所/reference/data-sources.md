# 数据源接入指南

## 三大数据源

| 数据源 | 用途 | 接入方式 |
|--------|------|---------|
| 本地技能库 | 查重、借鉴 | `Glob + Grep` 扫描 `~/.codebuddy/skills/` |
| skills.sh | 远程技能发现 | `npx skills find <query>` |
| ClawHub | 技能市场 | `clawhub search <query>` + `clawhub inspect <slug>` |

## 接入策略

- 本地优先：快、无网络依赖
- 远程补充：本地无结果时查远程
- 缓存机制：搜索结果暂存，避免重复请求

## 本地搜索示例

```bash
# 搜索所有技能的SKILL.md
Glob pattern="~/.codebuddy/skills/*/SKILL.md"

# 搜索关键词
Grep pattern="关键词" path="~/.codebuddy/skills/"
```

## 远程搜索示例

```bash
# skills.sh
npx skills find "code review"

# ClawHub
clawhub search "code review"
clawhub inspect "code-review-skill"
```

## 缓存机制

- 搜索结果暂存到 `feedback/search-cache.json`
- 缓存有效期：24小时
- 手动清除：用户可要求"清除缓存"

## AVOID

- AVOID 只搜本地不搜远程
- AVOID 重复请求相同查询
- AVOID 忽略缓存机制
