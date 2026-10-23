---
name: dim-workflow
description: Use when the user asks to create, modify, or save a reusable Dim workflow script. Do not use it for running, stopping, opening, revealing, or checking workflow runs.
---

# Dim Workflow

这个 skill 只用于编写可复用的 Dim 工作流文件。

## 什么时候使用

用户要求这些事时使用：

- 创建一个可复用工作流。
- 修改一个已保存工作流。
- 把对话里生成的工作流保存起来以后复用。

用户只是要运行、停止、打开、查看进度时不要使用：

- `/workflow <name>`
- 给工作流命令加参数。
- 停止、打开、定位、检查某次工作流运行。

## 保存位置

已保存工作流放在：

```text
<workflowDataDir>/workflows/saved/
```

Desktop 默认路径：

```text
DIMCODE_HOME=~/.dimcode/v2
workflowDataDir=<DIMCODE_HOME>/data
saved workflows=~/.dimcode/v2/data/workflows/saved/
```

如果已知配置里的 `workflowDataDir`，使用那个绝对路径。

如果不知道 `workflowDataDir`，先询问用户。不要猜项目目录，也不要把可复用工作流保存到当前仓库里。

## 文件要求

一个工作流一个文件：

```text
<workflowDataDir>/workflows/saved/<workflowName>.mjs
```

文件必须导出 `meta`，并默认导出一个 async function：

```js
export const meta = {
  name: "example-workflow",
  description: "Short user-facing description",
}

export default async function workflow(api) {
  api.phase("Prepare")
  await api.agent("Read the relevant docs", { label: "Read docs" })

  api.phase("Implement")
  await api.agent("Make the requested code change", { label: "Edit code" })

  api.phase("Verify")
  await api.tool("exec", { command: "pnpm test" }, { label: "Run tests" })

  return { ok: true }
}
```

规则：

- `meta.name` 必须是非空且唯一的工作流名字。
- `meta.description` 必须非空。
- 需要 import 本地 helper 时使用 `.mjs`。
- `.js` 和 `.ts` 只用于没有 import 的自包含脚本。
- 用 `api.tool()` 调当前 session 的 tool。
- 用 `api.agent()` 创建 child agent。
- 工作流文件是 trusted code，必须把输入和路径写清楚。

## 右侧面板显示要求

右侧面板的阶段图来自工作流源码。想让用户看到清楚的阶段和步骤，就按下面写：

- 主要阶段用 `api.phase("Prepare")`、`api.phase("Implement")`、`api.phase("Verify")` 这类调用表达。
- 用户应该看到的步骤，用 `api.agent(prompt, { label })` 或 `api.tool(name, input, { label })` 表达。
- 尽量使用静态的 `label`、`title`、`name` 和 tool name。也就是说，传给 API 的关键参数尽量直接写成字符串，不要依赖运行时拼接。
- `label` 写短一点，表示这一步在做什么。
- 主要阶段和主要步骤放在默认导出的 `workflow(api)` 函数里。
- 可以用 helper function 处理细节，但不要把主要阶段和主要步骤全藏进 helper function。
- `api.parallel([...])` 和 `api.mapLimit(...)` 可以表达并行和批量步骤。
- 复杂编排优先考虑 `api.phase()`、`api.agent()`、`api.tool()`、`api.parallel()`、`api.mapLimit()` 的组合。组合不够用时，再写自定义脚本逻辑。
- 打 log 时写清楚当前步骤和结果，内容要让用户一眼能懂。
- 需要指定 child agent 的 provider/model 时，先查询或确认当前可用列表，再写 `providerId` 和 `modelId`。

写法示意：

```text
Prepare
  Read docs
Implement
  Edit code
Verify
  Run tests
```

对应源码里要能直接看到：

```js
api.phase("Prepare")
await api.agent("Read the relevant docs", { label: "Read docs" })

api.phase("Implement")
await api.agent("Make the requested code change", { label: "Edit code" })

api.phase("Verify")
await api.tool("exec", { command: "pnpm test" }, { label: "Run tests" })
```

## 完成后告诉用户

写入或修改已保存工作流后，告诉用户刷新 Desktop 的 workflow 列表，让 runtime 重新读取 `workflows/saved/`。
