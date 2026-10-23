---
name: plugin-creator
description: Create and scaffold Dim plugin directories with a required `.codex-plugin/plugin.json` manifest, optional skills/hooks/MCP components, MCP App widgets, and `bin/` executables. Use when the user wants to create a new Dim plugin, add skills/hooks/MCP servers to a plugin, validate a plugin before sharing, or set up a plugin for local development.
metadata:
  short-description: Create or scaffold a Dim plugin
---

# Plugin Creator

Scaffold a Dim plugin: a directory with a `.codex-plugin/plugin.json` manifest plus optional
`skills/`, a hooks file, an `.mcp.json`, and a `bin/` directory. Dim scans its plugin roots at
session start; each plugin folder is self-describing, so placing one in a root makes its skills,
hooks, MCP servers, and executables load on the next session.

## Quick Start

1. Scaffold the plugin. By default it is created live under `~/.agents/plugins/<name>/` — a root
   Dim scans, so a new session picks it up immediately.

```bash
# Names are normalized to lower-case hyphen-case (<= 64 chars). The folder name and the
# manifest `name` are always identical. Run from the skill root (the directory holding
# this SKILL.md).
python3 scripts/create_basic_plugin.py <plugin-name>
```

2. Edit `<plugin-path>/.codex-plugin/plugin.json` when the request gives specific metadata
   (description, display name, version). The scaffold starts with valid defaults and must not
   contain `[TODO: ...]` placeholders.

3. Add the components the plugin needs:

```bash
python3 scripts/create_basic_plugin.py <plugin-name> \
  --with-skills --with-hooks --with-mcp --with-bin --with-assets
```

   - `--with-skills` creates `skills/<plugin-name>/SKILL.md`, a working starter skill, and sets
     manifest `"skills": "./skills/"`.
   - `--with-hooks` creates `hooks.json` and sets manifest `"hooks": "./hooks.json"`.
   - `--with-mcp` creates `.mcp.json` and sets manifest `"mcpServers": "./.mcp.json"`.
   - `--with-bin` creates `bin/<plugin-name>`, an executable placed on the agent's exec PATH.
   - `--with-assets` creates an `assets/` folder for icons/logos.
   - `--manifest-format claude` writes `.claude-plugin/` instead, for a directory that must also
     load in Claude Code. Never ship both manifests.

   `--with-hooks` and `--with-mcp` create **empty** component files. Fill them in before handing
   the plugin back — validation fails on an empty hooks/MCP file, because declaring a component
   that contributes nothing is a broken plugin, not a neutral one.

4. Build a plugin for git distribution instead of local dev with `--path`:

```bash
# Create under a repo or scratch directory you will push to git.
python3 scripts/create_basic_plugin.py <plugin-name> --path <parent-directory>
```

5. Validate before handing back or sharing:

```bash
python3 scripts/validate_plugin.py <plugin-path>
```

6. **Tell the user to start a new session/thread.** Dim loads a plugin's components when a
   session starts, so a plugin created or changed in the *current* session only becomes usable in
   the *next* one. If you scaffolded the plugin mid-conversation, the skill will not be callable
   here yet.

## What this skill creates

- Plugin root at `<parent-directory>/<plugin-name>/` (default parent `~/.agents/plugins`).
- Always `<plugin-root>/.codex-plugin/plugin.json` with the manifest shape Dim reads.
- `<plugin-name>` is normalized: `My Plugin` → `my-plugin`, `My--Plugin` → `my-plugin`;
  underscores, spaces, and punctuation become `-`; consecutive hyphens collapse; result is
  lower-case.
- Optional, created only when requested: `skills/<plugin-name>/SKILL.md`, `hooks.json`,
  `.mcp.json`, `bin/<plugin-name>`, `assets/`.

## Manifest

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "My Plugin plugin",
  "interface": {
    "displayName": "My Plugin",
    "shortDescription": "Use My Plugin in Dim."
  },
  "skills": "./skills/",
  "hooks": "./hooks.json",
  "mcpServers": "./.mcp.json"
}
```

Component paths (`skills`, `hooks`, `mcpServers`) appear only when their files exist. See
`references/plugin-json-spec.md` for the full field guide, the manifest-format choice, and the
larger metadata block real plugins carry (which Dim ignores but **must not be deleted** from an
existing plugin).

## Components

- **Skills** — directories under `skills/<name>/` each containing a `SKILL.md` with valid
  frontmatter (`name`, `description`) and a non-empty body. Dim discovers them automatically.
- **Hooks** — a JSON file (manifest `hooks` field) mapping lifecycle events to commands. Any path
  works: `./hooks.json` and `./hooks/hooks.json` are both common. Use `${CLAUDE_PLUGIN_ROOT}` in
  command paths. **One unrecognized event name drops every hook in the file** — see the event
  list in `references/plugin-json-spec.md` and never invent event names.
- **MCP** — an `.mcp.json` with an `mcpServers` object; server ids are namespaced
  `plugin:<plugin-name>/<serverId>`. Read `references/mcp-servers.md` before writing it: a stdio
  server already runs from the plugin root (so relative `args` work), remote servers use
  `http_headers` rather than `headers`, and a malformed server is dropped **silently**.
- **MCP Apps (widget UI)** — a tool whose result renders as HTML in Dim. Read
  `references/mcp-apps.md` before adding any `_meta.ui` to a tool: an invalid value there fails
  the whole server connection, so *every* tool from that server disappears. There is no scaffold
  for this — a real app is a frontend project with its own build.
- **Executables** — anything the agent should run as a shell command goes in `bin/`, which the
  host puts on the agent's exec PATH. Only needed when something outside the plugin's own
  MCP/hook wiring must invoke a command; a plugin whose MCP server is launched from `.mcp.json`
  does not need it.

## Required behavior

- The outer folder name and `plugin.json` `"name"` are always the same normalized name.
- Keep the manifest present; ship exactly one of `.codex-plugin` / `.claude-plugin`.
- Do not leave `[TODO: ...]` placeholders in the manifest.
- Add a component path to the manifest only when its file actually exists **and has content**.
- When editing an existing plugin, preserve manifest fields Dim does not read (store and
  cross-host metadata). Removing them breaks listings elsewhere and gains nothing.
- Use `--force` only when overwriting an existing plugin path is intentional.
- After creating or modifying a plugin, end by telling the user to start a new session/thread.

## Install and update

See `references/installing-and-updating.md` for plugin roots, the local-development loop, the git
sharing path, and component toggling. In short:

- **Local dev** — scaffold into `~/.agents/plugins/<name>/`, then start a new session.
- **Share** — push the plugin directory to a git repo, then in the Dim desktop app open
  Plugins → Add plugin and paste the git URL. Dim installs it under `<DIMCODE_HOME>/plugins/`.

## Validation

After editing this `SKILL.md`, run:

```bash
python3 ../skill-creator/scripts/quick_validate.py .
```

Before handing back a generated plugin, run:

```bash
python3 scripts/validate_plugin.py <plugin-path>
```

It checks the manifest, the hooks file's event names and command shape, every `.mcp.json` server,
`bin/` executable bits, and each skill's frontmatter and body — the failures that are silent at
runtime.
