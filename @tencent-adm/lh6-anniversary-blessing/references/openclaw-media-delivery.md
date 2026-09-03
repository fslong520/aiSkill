# OpenClaw 本地 PNG 交付

仅在 OpenClaw 中生成和发送“AI 祝福海报”时读取。

1. 不要把“工具清单没有 ImageGen/DALL·E”判定为无法生成海报。先实际运行：

   ```bash
   python3 scripts/render_blessing_poster.py --check
   ```

2. `ok=true` 后生成 PNG。输出位置使用 OpenClaw 可读取的 Agent 工作区、临时根目录或 OpenClaw 生成目录。
3. 读取脚本 JSON 返回的 `mediaUrl` / `filePath`，通过消息工具或最终 assistant 回复载荷的同名**结构化媒体字段**发送图片；图片发送成功后直接创建活动流水并展示活动页入口，不增加账号授权步骤。
4. 不要把 JSON 作为普通文本输出，不要仅输出本地路径，也不要依赖 Markdown `![...](...)`；OpenClaw 的普通文本、工具输出和流式块不会被通用解析为附件命令。
5. 只有结构化媒体发送明确失败时，才说明当前通道不能交付图片并请用户换一种祝福方式。生成成功但发送失败时，不得把路径冒充交付。

OpenClaw 支持 PNG/JPG/WebP 等本地媒体；本地路径仍受其文件读取与 `tools.fs.workspaceOnly` 策略约束。
