---
name: computer-use
description: Drive the user's desktop GUI through DimAgent's built-in CUA Driver MCP tools. Use when the user asks to operate a native app, click/type/scroll in another application, inspect desktop windows, or automate a visible GUI workflow from Desktop.
---

# Computer Use

Use this skill only in DimAgent Desktop. The CUA Driver runtime and MCP server
are owned by the Desktop app; do not install, update, or launch a separate
`cua-driver` binary yourself.

## Tool Selection

Use the built-in MCP tools from the `cua-driver` server. If no CUA Driver tools
are available, tell the user to enable the Computer Use plugin from the Desktop
sidebar: Skills / Plugins > Plugins > My Plugins > Computer Use. It is not in
Settings.

## Workflow

1. Inspect state first. Use the CUA tools to list apps/windows or read the
   target window state before taking an action.
2. Act with the most specific target available. Prefer a non-empty
   `element_token` from the latest `get_window_state`, then `element_index`,
   then window-scoped coordinates.
3. Verify after every action by reading the window state again.
4. Report uncertainty when the post-action state does not prove the requested
   change happened.

## Element Tokens

- Treat `element_token` as an opaque per-snapshot handle. Never parse, construct,
  modify, or reuse it after a newer snapshot.
- When both `element_token` and `element_index` are available, use the token.
  `window_id` may be omitted when a valid token is present.
- Never send an empty `element_token`; omit it and use the latest snapshot's
  index or coordinates instead.
- If an action reports a stale token, call `get_window_state` again and retry
  once with the new token. Never fall back to an index from the stale snapshot.

## Desktop Rules

- Do not bring another app to the foreground unless the user explicitly asks.
- Do not use shell shims such as `open`, `osascript`, `cliclick`, or
  platform-specific input hacks for GUI control while CUA tools are available.
- On macOS, Accessibility and Screen Recording permission must belong to
  `com.dimagent.cua1`; the Desktop plugin settings own that authorization flow.
