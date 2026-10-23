# Plugin MCP servers (`.mcp.json`)

The manifest `mcpServers` field is a **relative path string** to a JSON file, never an inline
object. An inline `mcpServers` object in `plugin.json` is silently ignored (no error, no
server). The file's shape:

```json
{
  "mcpServers": {
    "<serverId>": { /* transport config */ }
  }
}
```

Server ids are namespaced at load time as `plugin:<plugin-name>/<serverId>`, so a plugin's
server id only has to be unique inside its own file.

## stdio servers

```json
{
  "mcpServers": {
    "example": {
      "command": "node",
      "args": ["./scripts/start-mcp.mjs"],
      "cwd": ".",
      "env": { "EXAMPLE_TOKEN": "${EXAMPLE_TOKEN}" }
    }
  }
}
```

- `command` is required and must be non-empty. `type: "stdio"` is the default and may be
  omitted.
- **A plugin stdio server runs from the plugin root when `cwd` is absent, and a relative `cwd`
  resolves against the plugin root.** Relative `args` paths therefore work without any
  `${CLAUDE_PLUGIN_ROOT}` prefix — `["./scripts/start-mcp.mjs"]` is a correct and common form.
- `${CLAUDE_PLUGIN_ROOT}` is also available in `command`, `args`, `cwd`, and `env`, and resolves
  to the plugin's absolute root. Use it when a value must be absolute (for example a path handed
  to a child process that changes directory). Prefer relative paths otherwise — they are shorter
  and survive being copied between plugins.
- Any other `${VAR}` in these fields resolves against the host environment. A missing variable
  produces a `missing_env` warning, not a hard failure.

## HTTP and SSE servers

```json
{
  "mcpServers": {
    "example": {
      "type": "http",
      "url": "https://example.com/mcp/",
      "http_headers": { "APP": "dim-agent" }
    }
  }
}
```

- `type` accepts `"stdio"`, `"http"`, and `"sse"`. When `type` is absent but `url` is present
  and `command` is not, the loader infers `"http"`.
- `url` is required and must be non-empty for `http` / `sse`.
- **Headers use either `headers` or `http_headers`, never both.** Plugins conventionally write
  `http_headers` (the Codex spelling); the loader rewrites it to `headers`. Declaring both keys
  on one server is an `invalid_server` warning and **that server is dropped** — the rest of the
  file still loads.
- `http_headers` must be a string→string object. A non-string value drops the server the same
  way.
- `oauth_resource` (plugin-only key) declares the OAuth protected-resource URL. It must be an
  **absolute URL**; anything else drops the server.

## Per-server extras

- `enabled: false` keeps a server declared but inactive. Absent means enabled.
- `title` and `description` are accepted as presentation metadata.

## Failure model

Failures here are **per server and mostly silent** — the plugin still installs, the file still
loads, the server just never appears. Symptoms are "the plugin's tools are missing", not an
error dialog. Before handing a plugin back, confirm the server actually connected rather than
assuming a valid-looking `.mcp.json` worked.

The one exception is a bad file: unparseable JSON or a missing `mcpServers` object produces a
single warning and contributes no servers at all.

## MCP Apps (widget UI)

A server that renders a UI widget in Dim has additional, **fail-fast** requirements that break
the *whole server connection* when violated. See `mcp-apps.md` before adding `_meta.ui` to any
tool.
