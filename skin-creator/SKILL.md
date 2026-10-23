---
name: skin-creator
description: Create, modify, apply, inspect, or switch Desktop skins through the Desktop session-scoped dim skin command.
---

# Skin Creator

Use when the user asks to create, modify, apply, inspect, list, or switch a DimAgent Desktop skin or theme.

## Availability

Desktop sessions only. Every skin operation uses `dim skin ... --json`. If the result reports `DESKTOP_HOST_UNAVAILABLE`, explain that this capability requires DimAgent Desktop and stop. Do not write `{DIMCODE_HOME}/skins`, edit Desktop config, or call renderer APIs.

Skin operations may run from a subagent or a workflow `api.agent()` child session: the host automatically elevates them to the main (top-level parent) session, which is where skin state and user-uploaded images live. If you are a subagent generating a background image, you can run `dim image generate` yourself and then either run `dim skin create` (it will apply in the main session) or return the generated image path to the main session for it to finish. `PERMISSION_DENIED` on a skin call means the main session could not be resolved — hand the intermediate result back to the main session and re-run there.

## Format Boundary

Skins support PNG, JPEG, WebP, and GIF only, at most 10 MiB. Video files (MP4/WebM) are not supported: never pass a video file to `dim skin`. Tell the user about this limitation.

If the user insists on a video background, guide them to provide a GIF, or convert the video to a supported format yourself when the environment allows (e.g. a system `ffmpeg`) before calling `dim skin create` — the result must still pass the 10 MiB and format validation.

## Required Image Source

Creating a skin requires exactly one source:

1. **User-uploaded image** — call `dim skin images --json` and read its `imageId` from CLI JSON `content`.
2. **Agent-generated image** — load `dim-modality`, run `dim modality list --json`, then:

```bash
dim image generate --prompt "<prompt derived from the request>" --out-dir ./artifacts --json
```

Require `ok: true`, a non-empty `outputs` array, and an existing image file. Pass the exact absolute `outputs[].path` to `--generated-image-path`.

Never pass both `imageId` and `generatedImagePath`. Never create a blank, placeholder, solid-color, or image-free skin.

## Actions

| Intent | Command |
|---|---|
| List user images | `dim skin images --json` |
| List available skins | `dim skin list --json` |
| Get installed skin details | `dim skin get --target-skin-id <id> --json` |
| Create new skin | `dim skin create --name "<name>" (--image-id <id> \| --generated-image-path <path>) [options] --activate --json` |
| Update installed skin | `dim skin update --target-skin-id <id> [patch options] --json` |
| Activate installed skin | `dim skin activate --target-skin-id <id> --json` |
| Restore Default | `dim skin activate-default --json` |

A normal request to make a theme means create. Update only when the user explicitly asks to modify an existing skin. `targetSkinId` must come from trusted CLI JSON `content`, never from a display name.

## Default And Installed

- `dim skin list --json` includes `kind=default`; Default has no `skinId` and uses `dim skin activate-default --json` directly.
- `kind=installed` entries contain the real `skinId` used by get, update, and activate.
- Never use an unrelated update to imitate activation.

## Result Confirmation

Only report success when `ok: true` and CLI JSON `content` confirms the operation:

- create: target `skinId` and `active=true` before saying created and applied;
- update: target `skinId`; only call it active when `active=true` is present;
- activate: `kind=installed`, exact `skinId`, and `active=true`;
- activate-default: `kind=default; active=true`.

For `ok: false`, report `error.code` and `error.message`. Do not silently recover. Handles and state needed in later turns must be read from CLI JSON `content`; `result` is only the machine-readable mirror.

## Visual Guidance

Explicit user preferences override these suggestions:

| Image characteristic | Suggested flag |
|---|---|
| Subject on right | `--background-position "right center"` |
| Subject on left | `--background-position "left center"` |
| Centered or no clear subject | `--background-position center` |
| Mostly dark | `--foreground light` |
| Mostly bright | `--foreground dark` |
| Mixed brightness with opaque surfaces | `--foreground auto` |
| Full uncropped image requested | `--background-size contain` |
| Otherwise | `--background-size cover` |

Use `--background-attachment scroll` by default. Use `fixed` only for an explicit parallax request.
