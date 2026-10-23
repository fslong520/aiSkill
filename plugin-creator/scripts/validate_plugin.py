#!/usr/bin/env python3
"""Validate a generated Dim plugin against the contracts Dim actually enforces.

Dim recognizes a plugin by ``.codex-plugin/plugin.json`` (probed first) or
``.claude-plugin/plugin.json``, and parses a small set of manifest fields: ``name`` (required),
``version``, ``description``, ``interface.{displayName,shortDescription,logo}``, and the
component paths ``skills`` / ``hooks`` / ``mcpServers``. Unknown fields are ignored by Dim and
are not rejected here — real plugins legitimately carry store/other-host metadata.

Beyond the manifest this checks the component files, because their failures are silent at
runtime: a hooks file with one unrecognized event registers *no* hooks, a malformed `.mcp.json`
server is dropped without an error, and a `bin/` entry without an executable bit is not
callable. It also rejects leftover ``[TODO: ...]`` placeholders.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any


TODO_MARKER = "[TODO:"
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MANIFEST_DIRS = (".codex-plugin", ".claude-plugin")
MANIFEST_REL = "/".join((MANIFEST_DIRS[0], "plugin.json"))
SUPPORTED_HOOK_EVENTS = frozenset({
    "SessionStart",
    "SubagentStart",
    "PreToolUse",
    "PermissionRequest",
    "PostToolUse",
    "PreCompact",
    "PostCompact",
    "UserPromptSubmit",
    "SubagentStop",
    "Stop",
})
SUPPORTED_MCP_TRANSPORTS = frozenset({"stdio", "http", "sse"})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a local Dim plugin.")
    parser.add_argument("plugin_path", help="Path to the plugin root directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plugin_root = Path(args.plugin_path).expanduser().resolve()
    errors = validate_plugin(plugin_root)
    if errors:
        print("Plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Plugin validation passed: {plugin_root}")


def validate_plugin(plugin_root: Path) -> list[str]:
    errors: list[str] = []
    present = [d for d in MANIFEST_DIRS if (plugin_root / d / "plugin.json").is_file()]
    if not present:
        errors.append(f"missing `{MANIFEST_REL}` (or `.claude-plugin/plugin.json`)")
        return errors
    if len(present) > 1:
        # Dim reads the first match only; the second copy is dead weight that drifts.
        errors.append("plugin declares both `.codex-plugin/plugin.json` and "
                      "`.claude-plugin/plugin.json` — ship exactly one")
    manifest_rel = f"{present[0]}/plugin.json"
    manifest = load_json_object(plugin_root / present[0] / "plugin.json", manifest_rel, errors)
    if manifest is None:
        return errors

    reject_todo_markers(manifest, "$", errors)
    validate_manifest(plugin_root, manifest, errors)
    validate_bin_entries(plugin_root, errors)
    return errors


def load_json_object(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing `{label}`")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError:
        errors.append(f"unable to read `{label}`")
        return None
    except json.JSONDecodeError:
        errors.append(f"`{label}` must be valid JSON")
        return None
    if not isinstance(payload, dict):
        errors.append(f"`{label}` must contain a JSON object")
        return None
    return payload


def reject_todo_markers(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, str):
        if TODO_MARKER in value:
            errors.append(f"{path} still contains a `[TODO: ...]` placeholder")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            reject_todo_markers(item, f"{path}[{index}]", errors)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            reject_todo_markers(item, f"{path}.{key}", errors)


def validate_manifest(plugin_root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    require_non_empty_string(manifest, "name", errors)

    version = manifest.get("version")
    if version is not None:
        if not isinstance(version, str) or SEMVER_RE.fullmatch(version) is None:
            errors.append("plugin.json field `version` must be strict semver")

    validate_optional_non_empty_string(manifest, "description", errors)

    interface = manifest.get("interface")
    if interface is not None:
        if not isinstance(interface, dict):
            errors.append("plugin.json field `interface` must be an object")
        else:
            validate_optional_non_empty_string(interface, "displayName", errors, prefix="interface")
            validate_optional_non_empty_string(interface, "shortDescription", errors, prefix="interface")
            validate_optional_asset_path(plugin_root, interface, "logo", errors)

    validate_component_path(plugin_root, manifest, "skills", errors)
    validate_component_path(plugin_root, manifest, "hooks", errors)
    validate_mcp_servers(plugin_root, manifest, errors)
    validate_skill_manifests(plugin_root, errors)


def require_non_empty_string(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    *,
    prefix: str | None = None,
) -> None:
    value = payload.get(key)
    field = f"{prefix}.{key}" if prefix is not None else key
    if not isinstance(value, str) or not value.strip():
        errors.append(f"plugin.json field `{field}` must be a non-empty string")


def validate_optional_non_empty_string(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    *,
    prefix: str | None = None,
) -> None:
    value = payload.get(key)
    if value is None:
        return
    field = f"{prefix}.{key}" if prefix is not None else key
    if not isinstance(value, str) or not value.strip():
        errors.append(f"plugin.json field `{field}` must be a non-empty string")


def validate_component_path(
    plugin_root: Path,
    manifest: dict[str, Any],
    key: str,
    errors: list[str],
) -> None:
    """`skills` resolves to a directory; `hooks` resolves to a file. Both must exist."""
    value = manifest.get(key)
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        errors.append(f"plugin.json field `{key}` must be a non-empty relative path")
        return
    resolved = resolve_inside(plugin_root, value, key, errors)
    if resolved is None:
        return
    if key == "skills" and not resolved.is_dir():
        errors.append(f"plugin.json field `skills` points to a missing directory")
    if key == "hooks":
        if not resolved.is_file():
            errors.append("plugin.json field `hooks` points to a missing file")
        else:
            validate_hooks_file(resolved, value, errors)


def validate_mcp_servers(plugin_root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    value = manifest.get("mcpServers")
    if value is None:
        return
    # Runtime only loads `mcpServers` as a path to an `.mcp.json` file; an inline
    # object is silently ignored by the loader, so reject it here too.
    if isinstance(value, str) and value.strip():
        resolved = resolve_inside(plugin_root, value, "mcpServers", errors)
        if resolved is None:
            return
        if not resolved.is_file():
            errors.append("plugin.json field `mcpServers` points to a missing file")
            return
        validate_mcp_file(resolved, value, errors)
        return
    errors.append("plugin.json field `mcpServers` must be a relative path string to an `.mcp.json` file")


def validate_hooks_file(path: Path, label: str, errors: list[str]) -> None:
    """One bad event name drops every hook in the file, so a partial check is not enough."""
    payload = load_json_object(path, label, errors)
    if payload is None:
        return
    hooks = payload.get("hooks")
    if not isinstance(hooks, dict):
        errors.append(f"`{label}` must contain a `hooks` object")
        return
    if not hooks:
        errors.append(f"`{label}` declares no hooks — drop the manifest `hooks` field instead")
        return
    for event, groups in hooks.items():
        if event not in SUPPORTED_HOOK_EVENTS:
            errors.append(
                f"`{label}` uses unrecognized hook event `{event}` — Dim then registers NONE of "
                f"the hooks in this file. Supported: {', '.join(sorted(SUPPORTED_HOOK_EVENTS))}"
            )
            continue
        if not isinstance(groups, list) or not groups:
            errors.append(f"`{label}` event `{event}` must be a non-empty array")
            continue
        for index, group in enumerate(groups):
            where = f"`{label}` {event}[{index}]"
            if not isinstance(group, dict):
                errors.append(f"{where} must be an object")
                continue
            matcher = group.get("matcher")
            if matcher is not None and not isinstance(matcher, str):
                errors.append(f"{where} `matcher` must be a string")
            entries = group.get("hooks")
            if not isinstance(entries, list) or not entries:
                errors.append(f"{where} must contain a non-empty `hooks` array")
                continue
            for entry_index, entry in enumerate(entries):
                spot = f"{where}.hooks[{entry_index}]"
                if not isinstance(entry, dict):
                    errors.append(f"{spot} must be an object")
                    continue
                if entry.get("type") != "command":
                    errors.append(f"{spot} `type` must be the literal string \"command\"")
                command = entry.get("command")
                if not isinstance(command, str) or not command.strip():
                    errors.append(f"{spot} `command` must be a non-empty string")


def validate_mcp_file(path: Path, label: str, errors: list[str]) -> None:
    """Malformed servers are dropped silently at runtime, so catch them here."""
    payload = load_json_object(path, label, errors)
    if payload is None:
        return
    servers = payload.get("mcpServers")
    if not isinstance(servers, dict):
        errors.append(f"`{label}` must contain an `mcpServers` object")
        return
    if not servers:
        errors.append(f"`{label}` declares no servers — drop the manifest `mcpServers` field instead")
        return
    for server_id, config in servers.items():
        where = f"`{label}` server `{server_id}`"
        if not isinstance(server_id, str) or not server_id.strip():
            errors.append(f"`{label}` has an empty server id")
            continue
        if not isinstance(config, dict):
            errors.append(f"{where} must be an object")
            continue
        validate_mcp_server(config, where, errors)


def validate_mcp_server(config: dict[str, Any], where: str, errors: list[str]) -> None:
    transport = config.get("type")
    if transport is not None and transport not in SUPPORTED_MCP_TRANSPORTS:
        errors.append(
            f"{where} `type` must be one of {', '.join(sorted(SUPPORTED_MCP_TRANSPORTS))}"
        )
        return
    has_url = isinstance(config.get("url"), str) and config["url"].strip() != ""
    remote = transport in {"http", "sse"} or (transport is None and has_url
                                              and config.get("command") is None)

    if remote:
        if not has_url:
            errors.append(f"{where} is a remote server and needs a non-empty `url`")
        headers = config.get("headers")
        http_headers = config.get("http_headers")
        if headers is not None and http_headers is not None:
            errors.append(
                f"{where} declares both `headers` and `http_headers` — the server is dropped at "
                "load time. Keep one (plugins conventionally use `http_headers`)."
            )
        for key, value in (("headers", headers), ("http_headers", http_headers)):
            if value is None:
                continue
            if not isinstance(value, dict) or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in value.items()
            ):
                errors.append(f"{where} `{key}` must be a string-to-string object")
        oauth_resource = config.get("oauth_resource")
        if oauth_resource is not None and not is_absolute_url(oauth_resource):
            errors.append(f"{where} `oauth_resource` must be an absolute URL")
        return

    command = config.get("command")
    if not isinstance(command, str) or not command.strip():
        errors.append(f"{where} is a stdio server and needs a non-empty `command`")
    args = config.get("args")
    if args is not None and not (
        isinstance(args, list) and all(isinstance(item, str) for item in args)
    ):
        errors.append(f"{where} `args` must be an array of strings")
    for key in ("env",):
        value = config.get(key)
        if value is not None and not (
            isinstance(value, dict)
            and all(isinstance(k, str) and isinstance(v, str) for k, v in value.items())
        ):
            errors.append(f"{where} `{key}` must be a string-to-string object")
    cwd = config.get("cwd")
    if cwd is not None and (not isinstance(cwd, str) or not cwd.strip()):
        errors.append(f"{where} `cwd` must be a non-empty string")


def is_absolute_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    match = re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value.strip())
    return bool(match)


def validate_bin_entries(plugin_root: Path, errors: list[str]) -> None:
    """`bin/` goes on the agent's exec PATH; a non-executable entry is not callable."""
    bin_root = plugin_root / "bin"
    if not bin_root.is_dir():
        return
    entries = [p for p in sorted(bin_root.rglob("*")) if p.is_file()]
    if not entries:
        errors.append("`bin/` exists but is empty — remove it or add the command entry point")
        return
    if os.name == "nt":
        return
    for entry in entries:
        if not os.access(entry, os.X_OK):
            rel = entry.relative_to(plugin_root).as_posix()
            errors.append(f"`{rel}` is not executable (chmod +x)")


def validate_optional_asset_path(
    plugin_root: Path,
    payload: dict[str, Any],
    key: str,
    errors: list[str],
) -> None:
    value = payload.get(key)
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        errors.append(f"plugin.json field `interface.{key}` must be a non-empty relative path")
        return
    resolved = resolve_inside(plugin_root, value, f"interface.{key}", errors)
    if resolved is not None and not resolved.is_file():
        errors.append(f"plugin.json field `interface.{key}` points to a missing file")


def resolve_inside(
    plugin_root: Path,
    raw_path: str,
    field: str,
    errors: list[str],
) -> Path | None:
    """Resolve a relative path and confirm it stays inside the plugin root."""
    candidate = PurePosixPath(raw_path.replace("\\", "/"))
    if candidate.is_absolute() or ".." in candidate.parts:
        errors.append(f"plugin.json field `{field}` must stay inside the plugin directory")
        return None
    resolved = (plugin_root / candidate.as_posix()).resolve()
    if not resolved.is_relative_to(plugin_root.resolve()):
        errors.append(f"plugin.json field `{field}` must stay inside the plugin directory")
        return None
    return resolved


def validate_skill_manifests(plugin_root: Path, errors: list[str]) -> None:
    skills_root = plugin_root / "skills"
    if not skills_root.is_dir():
        return
    for skill_root in sorted(skills_root.iterdir(), key=lambda path: path.name):
        if skill_root.name.startswith(".") or not skill_root.is_dir():
            continue
        validate_skill_manifest(skill_root, errors)


def validate_skill_manifest(skill_root: Path, errors: list[str]) -> None:
    skill_md_path = skill_root / "SKILL.md"
    if not skill_md_path.is_file():
        errors.append(f"skill `{skill_root.name}` is missing `SKILL.md`")
        return
    try:
        contents = skill_md_path.read_text(encoding="utf-8")
    except OSError:
        errors.append(f"unable to read skill `{skill_root.name}`")
        return
    frontmatter = parse_frontmatter(contents)
    if frontmatter is None:
        errors.append(f"skill `{skill_root.name}` must start with closed YAML frontmatter")
        return
    if not frontmatter_field(frontmatter, "name"):
        errors.append(f"skill `{skill_root.name}` frontmatter field `name` must be non-empty")
    if not frontmatter_field(frontmatter, "description"):
        errors.append(f"skill `{skill_root.name}` frontmatter field `description` must be non-empty")
    # A frontmatter-only SKILL.md is silently dropped at load time, never an error.
    body_start = contents.find("\n---", 4)
    if body_start != -1 and not contents[body_start + 4:].strip():
        errors.append(f"skill `{skill_root.name}` has an empty body — it would never load")


def parse_frontmatter(contents: str) -> str | None:
    """Return the raw frontmatter block, or None when it is missing/unclosed.

    Parsed by hand (no yaml dependency) — only the closed `---` fenced block is needed.
    """
    if not contents.startswith("---\n"):
        return None
    end = contents.find("\n---", 4)
    if end == -1:
        return None
    return contents[4:end]


def frontmatter_field(frontmatter: str, key: str) -> bool:
    """True when `key:` appears with a non-empty value on its own line."""
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.+?)\s*$", re.MULTILINE)
    match = pattern.search(frontmatter)
    return bool(match and match.group(1).strip())


if __name__ == "__main__":
    main()
