---
name: news
description: "Look up the latest news for the user from specified news sites. Provides authoritative URLs for politics, finance, society, world, tech, sports, and entertainment. Use browser_use to open each URL and snapshot to get content, then summarize for the user."
metadata:
  builtin_skill_version: "1.1"
  trigger: 新闻、最新新闻、今日新闻、news、时政、财经、科技新闻
  copaw:
    emoji: "📰"
    requires: {}
---

# News Reference

## Summary

获取最新新闻：根据类别选择权威新闻源URL，用browser_use打开并snapshot获取内容，摘要给用户。

## Keywords

新闻、最新新闻、今日新闻、news、时政、财经、科技

## Strategy

1. **确认类别**：确定用户需要的新闻类别（时政/财经/社会/国际/科技/体育/娱乐）
2. **选择URL**：从新闻源表中选择对应URL
3. **打开页面**：`browser_use` action=open
4. **获取内容**：`browser_use` action=snapshot
5. **摘要输出**：提取标题+摘要+来源，按时间或重要性排序

## AVOID

- AVOID 访问多个类别时混用页面，每个URL单独open+snapshot
- AVOID 页面结构变化时不告知用户，应说明并提供原链接
- AVOID 不处理超时情况，应说明并建议其他来源

## 新闻源

| 类别 | 来源 | URL |
|------|------|-----|
| 时政 | 人民日报 | https://cpc.people.com.cn/ |
| 财经 | 中国经济网 | http://www.ce.cn/ |
| 社会 | 中国新闻网 | https://www.chinanews.com/society/ |
| 国际 | CGTN | https://www.cgtn.com/ |
| 科技 | 科技日报 | https://www.stdaily.com/ |
| 体育 | CCTV体育 | https://sports.cctv.com/ |
| 娱乐 | 新浪娱乐 | https://ent.sina.com.cn/ |

## 使用browser_use

```json
{"action": "open", "url": "https://www.chinanews.com/society/"}
{"action": "snapshot"}
```

从snapshot内容中提取标题、日期、摘要，组织成简短列表回复用户。
