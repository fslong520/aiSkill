# Plugin manifest spec (`plugin.json`)

## Manifest location and format

Dim recognizes a plugin by a manifest at the plugin root, probing in this order:

1. `.codex-plugin/plugin.json`
2. `.claude-plugin/plugin.json`

Both are read with identical rules; the first one found wins. Which to write:

- **`.codex-plugin/`** — the ecosystem default. Every plugin distributed through the Dim plugin
  store uses it, Dim's own generated plugins write it, and market ingestion probes it first.
  This skill's default.
- **`.claude-plugin/`** — write this instead (`--manifest-format claude`) when the same
  directory must also load in Claude Code, which reads only this path.

Do not ship both. Two manifests means the `.claude-plugin` copy is dead weight that silently
drifts out of sync.

## Fields Dim reads

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Brief plugin description",
  "interface": {
    "displayName": "My Plugin",
    "shortDescription": "Short subtitle shown in the plugin list",
    "logo": "./assets/logo.png"
  },
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

- `name` (`string`, required): Plugin identifier. Sanitized to `[A-Za-z0-9._-]`, max 128 chars;
  this skill normalizes to lower-case hyphen-case ≤ 64 chars. Matches the plugin folder name.
- `version` (`string`, optional): Strict semver by convention. The runtime accepts any non-empty
  string and does not validate it.
- `description` (`string`, optional): Falls back to `interface.shortDescription` in the UI.
- `interface` (`object`, optional): Presentation metadata (below).
- `skills` (`string`, optional): Relative path to the skills directory, normally `./skills/`.
- `hooks` (`string`, optional): Relative path to the hooks config file. **Any path works** —
  `./hooks.json` and `./hooks/hooks.json` are both common. Pick one and keep the file there.
- `mcpServers` (`string`, optional): Relative path to an `.mcp.json` file. An inline object is
  not supported — the runtime loads only a path string. See `mcp-servers.md`.

### `interface` fields Dim reads

- `displayName` (`string`): User-facing title. Defaults to `name`.
- `shortDescription` (`string`): Brief subtitle for compact views.
- `logo` (`string`): Relative path to a logo asset inside the plugin.

### Fields Dim ignores but plugins carry anyway

Real plugins routinely include a larger metadata block: top-level `author`, `homepage`,
`repository`, `license`, `keywords`, and under `interface`: `longDescription`, `developerName`,
`category`, `capabilities`, `websiteURL`, `privacyPolicyURL`, `termsOfServiceURL`,
`defaultPrompt` (string or array), `brandColor`, `composerIcon`, `logoDark`, `screenshots`.
A sibling `apps` path (`./.app.json`) also appears on plugins ported from other hosts.

Dim's runtime parses **none** of these. They are harmless, and they matter for store listings
and for the same directory loading in other hosts — so **do not delete them from an existing
plugin**. Do not invent them for a new plugin either; add them only when a listing or another
host actually needs them.

### Path conventions

- Component path values are relative to the plugin root and begin with `./`.
- Declare a component path only when its file/directory exists.

## Components

### Skills

Skills live under `skills/<skill-name>/SKILL.md`, each starting with YAML frontmatter:

```markdown
---
name: my-skill
description: What it does and when to use it.
---

# My Skill

Instructions for the assistant.
```

Dim discovers plugin skills automatically from each plugin's `skills/` directory and loads them
into the system prompt.

### Hooks

`hooks` points to a JSON file mapping lifecycle events to commands. Use `${CLAUDE_PLUGIN_ROOT}`
in command paths — Dim substitutes the plugin's absolute root at runtime (the PowerShell
`$env:CLAUDE_PLUGIN_ROOT` and cmd `%CLAUDE_PLUGIN_ROOT%` spellings are substituted too):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          { "type": "command", "command": "node \"${CLAUDE_PLUGIN_ROOT}/hooks/on-start.js\"" }
        ]
      }
    ]
  }
}
```

Only these event names are recognized: `SessionStart`, `SubagentStart`, `PreToolUse`,
`PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`,
`SubagentStop`, `Stop`. An unrecognized event name is not a partial failure — Dim drops every
hook in that file (logs a warning, registers nothing). Do not invent event names; when unsure
which event fits, ask rather than guess.

What `matcher` is tested against depends on the event: the tool name for `PreToolUse` /
`PostToolUse`, the requested tool for `PermissionRequest`, the compaction trigger for
`PreCompact` / `PostCompact`, the session-start source for `SessionStart`, the subagent profile
for `SubagentStart` / `SubagentStop`. `UserPromptSubmit` and `Stop` have no subject — their
matcher is ignored and the hook always runs.

`type` must be the literal string `"command"` and `command` must be a non-empty string; that is
the only spec shape Dim parses. Plugin hooks run with the same full host environment as the
user's own hooks (not a restricted subset), so a plugin hook can read provider keys/tokens from
the process env — call this out to the user if the plugin's hook touches secrets.

### MCP servers

See `mcp-servers.md` for the `.mcp.json` contract (stdio `cwd` resolution, `http_headers`,
`oauth_resource`, `sse`, and the per-server failure model), and `mcp-apps.md` before adding a
widget UI.

### Executables (`bin/`)

Anything the agent should be able to run as a shell command goes in `<plugin-root>/bin/`. The
host collects every installed plugin's `bin/` directory and prepends it to the agent's exec
`PATH`, and on POSIX it repairs missing executable bits at install and PATH-refresh time
(Windows gets no chmod — ship `.exe`, `.cmd`, or `.bat` there, not a bare `.ps1`).

Rules:

- `bin/<command>` may be a real binary or a wrapper script. Support files live elsewhere in the
  plugin; only `bin/` is the public surface.
- Never install executables outside the plugin directory, and never declare PATH yourself.
- Prefix command names with the plugin (`example-send`), never generic names (`send`, `node`,
  `git`) that would collide with system commands or another plugin.
- Different platforms ship as different zips with the same internal layout — do not put multiple
  platform directories in one package.

`bin/` is only needed when something outside the plugin's own MCP/hook wiring must invoke a
command. A plugin whose MCP server is launched from `.mcp.json` (`command: "node"`,
`args: ["./scripts/start-mcp.mjs"]`) does not need `bin/` at all.

## Validation notes

- `name` must be a non-empty string; the folder name must match it. Dim does not verify this
  invariant — for a locally-placed plugin, a mismatch silently uses the folder name for
  skills/hooks/mcp resolution while the manifest `name` becomes only a display label. Keep the
  two in lockstep.
- `interface.logo` and any declared component path must point to real files/directories inside
  the plugin.
- The manifest `skills` field only toggles a UI "has skills" indicator; skill discovery always
  scans `<plugin-root>/skills` regardless of this field's value or presence. Keep skills at
  `./skills/` — pointing `skills` elsewhere does not relocate discovery.
- Sub-skill `SKILL.md` files must have non-empty `name` and `description` frontmatter, and a
  non-empty body after the closing `---`. A frontmatter-only file with no body is silently
  dropped (not an error) — the skill just never appears.
- The manifest must not contain `[TODO: ...]` placeholders.

Run `scripts/validate_plugin.py <plugin-path>` before handing back a generated plugin.
