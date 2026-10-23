# MCP Apps in a Dim plugin (widget UI)

An MCP App is a tool whose result renders as an HTML widget inside Dim (right panel by default,
or inline in the timeline). It is a normal plugin MCP server plus two things: `_meta.ui` on the
tool, and a `ui://` resource serving the HTML.

This file covers only the constraints that **fail** and are hard to diagnose. The full contract
— host architecture, widget lifecycle, JSON-RPC surface, sandbox model — lives in the repo at
`docs/architecture/mcp-apps-host.md` and is the single source of truth. Read it before building
a non-trivial app.

## Do not scaffold this blind

A real MCP App is a frontend project: HTML/JS bundle, build step, and self-contained runtime
dependencies shipped inside the plugin. There is no `--with-mcp-app` scaffold because a generated
skeleton would not be a usable starting point. Build the server first, confirm its tools work
without UI, then add `_meta.ui`.

## The failure that eats the whole server

Tool `_meta.ui` is validated during **connection discovery**. An invalid value on *one* tool
throws, the connect rolls back, the transport closes, and **none of that server's tools
register** — including the ones with no UI at all. The user sees "the plugin's tools are all
missing" with no obvious cause.

These are the throwing conditions:

| Field | Rule | Violation |
|---|---|---|
| `resourceUri` | string, parses as a URL, protocol `ui:`, literally starts with `ui://` | non-string, or any other scheme |
| `visibility` | non-empty array; every entry is `"model"` or `"app"`; no duplicates | empty array, non-array, unknown value, repeated value |
| `displayMode` | `"inline"` or `"fullscreen"` | any other string |
| `exclusivePanelKey` | string, non-empty after trim, ≤ 128 chars | non-string, blank, too long |

Every one of these is optional; omitting a field is always safe. `visibility` defaults to
`["model", "app"]`, and `_meta["ui/resourceUri"]` is read as a deprecated fallback when
`_meta.ui.resourceUri` is absent.

```json
{
  "name": "open_canvas",
  "inputSchema": { "type": "object", "properties": {} },
  "_meta": {
    "ui": {
      "resourceUri": "ui://example/canvas.html",
      "visibility": ["model", "app"],
      "displayMode": "fullscreen"
    }
  }
}
```

Visibility controls two separate gates: only tools including `"model"` are registered for the
model, and only tools including `"app"` can be called by the widget. An app may only call tools
on the **same server** that created it.

`displayMode` defaults to `fullscreen` (a right-panel tab) when absent. Only a tool that
explicitly declares `"inline"` renders in the timeline.

## The `ui://` resource

`resources/read(<resourceUri>)` must return a response that satisfies **all** of:

- exactly one entry in `contents` (not zero, not two)
- the content `uri` equals the requested URI
- `mimeType` is exactly `text/html;profile=mcp-app`
- exactly one of `text` or `blob` is present (never both, never neither); `blob` must be
  canonical base64
- decoded HTML is valid UTF-8 and ≤ 10 MiB

Any miss throws a typed error and the widget fails to open. The host never substitutes empty
HTML or a placeholder widget.

Resource-level `_meta.ui` may also carry `csp`, `permissions`, and `prefersBorder`. Content-level
`_meta.ui` wins; the `resources/list` entry's metadata is only a fallback.

## CSP and permissions

The host writes the CSP itself; a `<meta>` CSP in the HTML cannot widen it. Declare the extra
origins the widget needs under `_meta.ui.csp`:

```json
{
  "_meta": {
    "ui": {
      "csp": {
        "connectDomains": ["https://api.example.com"],
        "resourceDomains": ["https://cdn.example.com"],
        "frameDomains": [],
        "baseUriDomains": []
      },
      "prefersBorder": true
    }
  }
}
```

- Only these four keys exist. An unknown key throws.
- Each entry is a single CSP source string: no whitespace, `;`, or quotes.
- `resourceDomains` / `frameDomains` additionally accept the literals `data:` and `blob:`.
  `connectDomains` does **not** — those are already allowed in the baseline `connect-src`.
- Allowed schemes: `http`/`https` everywhere, plus `ws`/`wss` for `connectDomains`.
- No userinfo, query, fragment, or path beyond `/`. A wildcard port (`http://127.0.0.1:*`) and a
  subdomain wildcard (`https://*.example.com`) are allowed; wildcarding `localhost` is not.

`_meta.ui.permissions` only meaningfully grants `clipboardWrite`, written as an empty object
(`{"clipboardWrite": {}}`). `camera`, `microphone`, and `geolocation` are parsed but not granted.
Every permission value must be an empty object; anything else throws.

## Checklist before shipping an app plugin

- Tools without UI still register (nothing in `_meta.ui` is malformed).
- `resourceUri` starts with `ui://` and `resources/read` returns exactly one
  `text/html;profile=mcp-app` content.
- Runtime dependencies and build output (`dist/`) are inside the plugin — the host never runs a
  build or an install on the user's machine.
- The widget's outbound origins are declared in `csp.connectDomains`.
