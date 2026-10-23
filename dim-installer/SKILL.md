---
name: dim-installer
description: Translate third-party install instructions written for Codex, Claude Code, or other agents into the Dim equivalents, then install into Dim. Use when a user asks to install a plugin, skill, MCP server, or extension from a repo/URL whose README documents installation for another agent (e.g. `codex plugin add`, `claude mcp add`, `~/.codex/config.toml`), or says "install this into Dim".
metadata:
  short-description: Install third-party plugins/skills/MCP servers into Dim
---

# Dim Installer

Third-party projects usually document installation for Codex or Claude Code. Their
README steps (`codex ...`, `claude ...`, `~/.codex/...`, `~/.claude/...`) do NOT apply
to Dim directly. This skill maps those instructions onto Dim's own mechanisms and
installs into Dim.

**Never run `codex` or `claude` commands, and never write into `~/.codex/` or
`~/.claude/`, even when the project's README says to.** Those install for a different
agent. Translate every step using the tables below.

## Step 1: Classify what the project actually is

Read the project's README / repo layout and decide which mechanism it uses. A project
may combine several (e.g. a plugin that also ships an MCP server — the plugin manifest
handles it; install the plugin only).

| Evidence in the project | Mechanism | Go to |
| --- | --- | --- |
| `codex plugin marketplace add` / `codex plugin add`, or a `.codex-plugin/plugin.json` / `.claude-plugin/plugin.json` manifest, or a `marketplace.json` catalog | Plugin | Step 2A |
| A directory containing `SKILL.md` (openai/skills style, Claude skills) | Skill | Step 2B |
| `claude mcp add ...`, `[mcp_servers.x]` blocks in `config.toml`, an `.mcp.json` snippet, or "add this to your MCP config" | MCP server | Step 2C |
| "Add this to your CLAUDE.md / AGENTS.md / system prompt" | Instructions file | Step 2D |
| VS Code / Cursor extension, IDE-specific hooks, or anything with no Dim equivalent | Unsupported | Say so plainly; do not improvise a partial install |

## Step 2A: Install a plugin

Dim reads the same plugin manifests as Codex and Claude Code (`.codex-plugin/plugin.json`
first, then `.claude-plugin/plugin.json`), so third-party plugins install as-is — only
the commands differ:

| README says (Codex) | Run for Dim |
| --- | --- |
| `codex plugin marketplace add <source> [--ref <ref>]` | `dim plugin marketplace add <source> [--ref <ref>]` |
| `codex plugin add <item>@<marketplace>` | `dim plugin install <item>@<marketplace>` |
| `codex plugin list` | `dim plugin marketplace list`, or inspect `~/.dimcode/v2/plugins/` and `~/.agents/plugins/` |
| `codex plugin marketplace remove <name>` | `dim plugin marketplace remove <name>` |

`<source>` accepts a Git URL or a local absolute path, same as Codex. Worked example
(Canvasight — its README documents the Codex commands on the left):

```bash
dim plugin marketplace add https://github.com/Niall-Young/Canvasight.git --ref stable
dim plugin install canvasight@canvasight-local
```

### Local plugins / "personal marketplace" READMEs (e.g. Cowart)

Some READMEs document a local flow: clone the repo somewhere, hand-write
`~/.agents/plugins/marketplace.json`, then `codex plugin marketplace add ~` +
`codex plugin add <name>@personal`. Do NOT translate that literally:

- **Never run `dim plugin marketplace add ~`.** Dim copies the whole local source
  directory into its cache; pointing it at the home directory copies everything.
- **Check `~/.agents/plugins/<name>` first.** Dim and Codex share this discovery root.
  If the plugin is already installed there (e.g. previously installed for Codex), Dim
  already loads it — nothing to install; just start a new session.
- **Preferred install: clone straight into the shared discovery root**, skipping the
  marketplace entirely:

  ```bash
  git clone <repo-url> ~/.agents/plugins/<name>
  cd ~/.agents/plugins/<name> && npm install && npm run build   # only if the README says so
  ```

  Dim discovers `~/.agents/plugins/<name>/` (self-describing via its plugin manifest)
  at the next session start.
- If the marketplace flow is genuinely needed, use a small dedicated directory as the
  source (containing `.agents/plugins/marketplace.json` plus the plugin folders its
  relative `path` entries point to), never `~`:

  ```bash
  dim plugin marketplace add /path/to/personal-marketplace-dir
  dim plugin install <name>@personal
  ```

## Step 2B: Install a skill

Dim loads `SKILL.md` skills from `~/.agents/skills/<name>/` (user-level) and
`<project>/.agents/skills/<name>/` (project-level). Prefer the `skill-installer` skill
when it is available — it handles GitHub download/sparse-checkout. Otherwise copy the
skill directory (the folder containing `SKILL.md`) into `~/.agents/skills/<name>/`.

README paths to translate: `~/.claude/skills/...` or `~/.codex/skills/...` →
`~/.agents/skills/...`.

## Step 2C: Register an MCP server

Dim's MCP config lives at:

- User-level: `~/.dimcode/v2/mcp.json`
- Project-level: `<project>/.mcp.json`

Both use the `{ "mcpServers": { ... } }` shape. Translate the README's config into it:

```json
{
  "mcpServers": {
    "<server-id>": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "some-mcp-server"],
      "env": { "API_KEY": "..." }
    },
    "<remote-id>": {
      "type": "http",
      "url": "https://example.com/mcp",
      "headers": { "Authorization": "Bearer ..." }
    }
  }
}
```

Merge into the existing file — read it first, add the new key, write back. Do not
overwrite other entries. `claude mcp add <name> -- <command> <args...>` translates to a
stdio entry; `[mcp_servers.<name>]` TOML blocks from `~/.codex/config.toml` translate
field-by-field (`command`/`args`/`env` map directly).

## Step 2D: Instructions files

Dim reads `AGENTS.md` (searched upward from the project directory) and `~/AGENTS.md`
(global). "Add this to your CLAUDE.md" → add it to the project's `AGENTS.md`.

## Step 3: After installing

Plugins, skills, and MCP servers load at session start. Tell the user: **start a new
session (or restart Dim) to pick up the newly installed component**, then verify it
appears (skills via the skill list, plugins/MCP via their tools being available).

## Path reference

| Other agent | Dim |
| --- | --- |
| `~/.codex/` or `~/.claude/` (config home) | `~/.dimcode/v2/` (override: `$DIMCODE_HOME`) |
| `~/.codex/config.toml` MCP blocks, `claude mcp add` | `~/.dimcode/v2/mcp.json` (user) / `<project>/.mcp.json` (project) |
| `~/.claude/skills/`, `~/.codex/skills/` | `~/.agents/skills/` (user) / `<project>/.agents/skills/` (project) |
| Codex/Claude plugin dirs | `~/.dimcode/v2/plugins/` (marketplace installs) / `~/.agents/plugins/` (local dev) |
| `CLAUDE.md` | `AGENTS.md` |
