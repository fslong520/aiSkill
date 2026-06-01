---
name: Agnes画影
version: 1.1.0
description: 调用 Agnes AI 免费 API 生成图片/视频。从 AGNES_API_KEY 环境变量读取密钥。
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
metadata:
  slug: agnespaint
  trigger: Agnes、画影、生成图片、生成视频、Agnes AI、agnes画影
---

# Agnes画影 — Agnes AI 多模态创作

## Keywords

多模态生成、图片生成、视频生成、Agnes AI、API 调用

## Summary

调用 Agnes AI 免费全模态 API，据用户描述生成图片或视频，返回结果 URL。

## Strategy

1. **意图识别** — 用户要图片还是视频（默认图片）
2. **确认 Prompt** — 向用户复述并确认描述
3. **调 API** — 按类型调用对应端点，视频需轮询
4. **返结果** — 返回 URL，询问是否继续

## AVOID

- 勿将 API Key 暴露在日志或 prompt 中
- 勿高频轮询视频接口（间隔 ≥10 秒）
- 勿一次生成多张图/多个视频而未先问用户
- 勿假设视频同步返回——必须轮询至 complete
- 勿假设用户使用 zsh——每次配置前须侦测 OS 与 shell
- 勿在 Windows 上使用 Linux 路径语法（如 ~/.zshrc）

---

## 前置条件

- `AGNES_API_KEY` 环境变量（运行时自动侦测 OS 与 shell，见下方配置步骤）
- API 基础地址：`https://apihub.agnes-ai.com/v1`

## 获取 API Key

| 步骤 | 操作 |
|------|------|
| 1 | 打开 [platform.agnes-ai.com](https://platform.agnes-ai.com/)，注册/登录 |
| 2 | 左侧导航 → **API Keys** → **Create API Key** |
| 3 | 复制生成的 `sk-` 开头密钥 |
| 4a | **侦测环境**：`uname -s` 判 OS，`echo $SHELL` 判 shell |
| 4b | **配置命令**（据上一步结果选择）：<br>• Linux/macOS + **zsh** → `echo 'export AGNES_API_KEY="sk-..."' >> ~/.zshrc && source ~/.zshrc`<br>• Linux + **bash** → `echo 'export AGNES_API_KEY="sk-..."' >> ~/.bashrc && source ~/.bashrc`<br>• macOS + **bash** → `echo 'export AGNES_API_KEY="sk-..."' >> ~/.bash_profile && source ~/.bash_profile`<br>• Windows + **PowerShell** → `Add-Content -Path $PROFILE -Value '$env:AGNES_API_KEY="sk-..."'`<br>• 其他环境 → 询问用户其 shell 配置文件名 |
| 5 | 验证：`curl -s https://apihub.agnes-ai.com/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer $AGNES_API_KEY" -d '{"model":"agnes-2.0-flash","messages":[{"role":"user","content":"hi"}]}'`，返回含 `choices` 即成功 |

---

## 工作流

### 1. 识别意图

| 用户说 | → 操作 |
|--------|--------|
| "画/生成图片/做张图……" | 图片 |
| "生成视频/短片/短视频……" | 视频 |
| 未明确 | 默认图片，可反问确认 |

### 2. 确认 Prompt（Human-in-the-Loop）

向用户展示你要发送的描述文字，确认后再调 API。

### 3. 调用 API

详细参数与 curl 示例见 `modules/01-api-reference.md`。

**快速参考**：

| 能力 | 端点 | 模型名 |
|------|------|--------|
| 图片 | `POST /v1/images/generations` | `agnes-image-2.0-flash` |
| 视频 | `POST /v1/video/generations` | `agnes-video-v2.0`（带 `v`） |

- 图片：从响应 `.data[0].url` 取 URL
- 视频：异步任务，轮询 `.data.status` 至 `completed`，从 `.data.remixed_from_video_id` 取 URL

### 4. 返回结果

展示 URL，问用户"还要再生成吗？"

---

## 使用示例

```
用户：画一只在云朵上睡觉的柴犬，治愈风
→ 确认 Prompt → 调图片 API → 返回图片 URL

用户：做一段赛博朋克城市夜景，5 秒
→ 确认 Prompt → 调视频 API → 轮询至完成 → 返回视频 URL
```
