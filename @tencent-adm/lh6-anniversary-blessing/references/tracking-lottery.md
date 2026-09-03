# 活动入口、账号绑定与邀请归因

本 Skill 只连接 `SKILL.md` 中写明的活动后端与活动页。接口地址与活动 ID 已内置在脚本中，执行时不要改动，也不要替换为其他环境的地址。

## Skill 负责的请求

祝福交付后，脚本按以下顺序 best-effort 上报 UGC，再创建一次性活动入口：

1. 图片祝福：`POST /ugc/images`，提交 `SourceId`、`ContentType`、`ImageBase64`。
2. 文本或图片记录：`POST /ugc/blessings`，提交 `SourceId`、`Text` 或完整 `ImageUrl`，以及 `PublicConsent`。
3. 创建入口：`POST /entry`，提交 `EventId`、`SourceId` 和可选的邀请人 `InviteCode`。

脚本会为每次祝福生成不可预测的 `SourceId`，并通过 `Idempotency-Key` 传递请求标识。UGC 失败不阻断入口创建。

## `/entry` 响应

```json
{
  "claim_url": "https://lighthouse6.cloud.tencent.com/claim?e=签名EntryToken",
  "entry_expires_at": "2026-08-28T07:14:13Z"
}
```

Skill 只向用户返回 `ClaimUrl`，不解析、改写或展示 EntryToken。活动页消费凭证后负责清理 URL。

## 浏览器侧流程

- 用户打开 `ClaimUrl` 后，由活动页发起腾讯云 OAuth 登录。
- 活动页通过后端会话将登录后的 UIN 与 EntryToken 绑定，再调用领取接口。
- Skill 不获取 UIN，不调用 OAuth、`/auth/me`、`ClaimLotteryEntry` 或抽奖接口。
- 邀请归因、邀请成功人数、10 份上限和最终开奖由活动后端负责。

## 环境隔离要求

- 入口创建、UGC、UIN 绑定、幂等、邀请码和份额一律按脚本内置的活动 ID 写入。
- 不复用其他环境的 Cookie、密钥或幂等记录。
- Skill 不接触奖池明细，奖品发放与通知由活动后端负责。
