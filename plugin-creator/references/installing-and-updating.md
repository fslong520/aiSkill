# Installing and updating Dim plugins

A Dim plugin is a self-describing directory. Disk is the single source of truth: Dim scans its
plugin roots, reads each plugin's manifest, and loads the plugin's components. Installing means
placing the folder in a root; removing the folder removes the plugin.

## Plugin roots

Dim scans two roots, in priority order (a name present in both resolves to the first):

1. **`<DIMCODE_HOME>/plugins/`** — the install root, default `~/.dimcode/v2/plugins`
   (`DIMCODE_HOME` → `$XDG_CONFIG_HOME/.dimcode/v2` → `~/.dimcode/v2`). **Everything Dim installs
   lands here**, whether from git or from the plugin store, along with a provenance file
   (`dim-install.json` for git, `.dimcode-market.json` for the store).
2. **`~/.agents/plugins/`** — the shared, cross-agent root. Still scanned so plugins placed there
   by hand or by another agent keep working, but Dim never writes to it — it does not own what
   other agents put there.

Hand-placing a plugin in either root works. This skill scaffolds into `~/.agents/plugins` by
default because it is the stable, agent-neutral path and cannot collide with a store install.

## Local development

1. Scaffold the plugin (default parent `~/.agents/plugins`):

```bash
python3 scripts/create_basic_plugin.py my-plugin --with-skills
```

2. Edit the manifest and component files.

3. Start a **new session**. Dim re-scans the plugin roots, and the plugin's skills, hooks, and
   MCP servers load. A new session is the boundary at which changes are picked up.

To iterate, edit files in place and start another session. Removing the plugin directory removes
the plugin.

## Activation by component

- **Skills** — discovered from each plugin's `skills/` directory and loaded into the system
  prompt automatically. They also appear in the desktop Skills list.
- **Hooks** — read from the file named by the manifest `hooks` field and registered on session
  start. Command paths use `${CLAUDE_PLUGIN_ROOT}`, which Dim replaces with the plugin's absolute
  root.
- **MCP servers** — read from the file named by the manifest `mcpServers` field and merged into
  the MCP runtime, with ids namespaced `plugin:<plugin-name>/<serverId>`. An inline `mcpServers`
  object in the manifest itself is not supported — Dim silently ignores it (no error), so the
  component never loads. A malformed *server entry* is dropped on its own, also silently; see
  `mcp-servers.md`.
- **Executables** — every installed plugin's `bin/` directory is prepended to the agent's exec
  `PATH`, with executable bits repaired on POSIX at install and PATH-refresh time.

## Toggling components

In the Dim desktop app, open Plugins → select the plugin to see its detail page. Each skill,
hook, and MCP server has its own on/off switch, plus a master switch for all components.

## Sharing via git

1. Build the plugin in a directory you will push to git (use `--path`):

```bash
python3 scripts/create_basic_plugin.py my-plugin --path ./plugins --with-skills
```

2. Commit and push the plugin directory (including its `.codex-plugin/plugin.json`) to a git
   repo.

3. In the Dim desktop app, open Plugins → Add plugin and paste the git source — either
   `owner/repo` or a full git URL, with an optional ref. Dim clones the repo, reads the manifest,
   and installs into `<DIMCODE_HOME>/plugins/<name>/` with a `dim-install.json` provenance file.

Updating a git-installed plugin is done from the same Add-plugin flow (reinstall from source), or
by editing the installed copy in place for local tweaks.

The desktop app also has a Plugin Store tab that installs from a hosted marketplace (a zip
archive, not a git clone). That path matters for *distributing* a finished plugin, not for
creating one. Two constraints it imposes on the package are worth knowing while authoring:

- The client never runs a build or a dependency install. Build output and runtime dependencies
  must already be inside the package.
- The zip root is the plugin root — the manifest directory sits directly under it, not under an
  extra folder level.
