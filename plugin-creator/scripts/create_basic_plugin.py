#!/usr/bin/env python3
"""Scaffold a Dim plugin directory with a `.codex-plugin/plugin.json` manifest.

Dim scans ``<DIMCODE_HOME>/plugins`` (its own install root) and ``~/.agents/plugins`` (the
shared, cross-agent root). The default parent here is ``~/.agents/plugins`` so a scaffolded
plugin is live on the next session and cannot collide with a store install. Pass ``--path`` to
build a plugin elsewhere (e.g. a git repo to share).

The manifest is written as ``.codex-plugin/plugin.json`` — the ecosystem default that Dim probes
first. Pass ``--manifest-format claude`` for ``.claude-plugin/plugin.json`` when the same
directory must also load in Claude Code.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


MAX_PLUGIN_NAME_LENGTH = 64
DEFAULT_PLUGIN_PARENT = Path.home() / ".agents" / "plugins"
MANIFEST_DIRS = {"codex": ".codex-plugin", "claude": ".claude-plugin"}
MANIFEST_FILE = "plugin.json"


def normalize_plugin_name(plugin_name: str) -> str:
    """Normalize a plugin name to lowercase hyphen-case."""
    normalized = plugin_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def validate_plugin_name(plugin_name: str) -> None:
    if not plugin_name:
        raise ValueError("Plugin name must include at least one letter or digit.")
    if len(plugin_name) > MAX_PLUGIN_NAME_LENGTH:
        raise ValueError(
            f"Plugin name '{plugin_name}' is too long ({len(plugin_name)} characters). "
            f"Maximum is {MAX_PLUGIN_NAME_LENGTH} characters."
        )


def display_name_from_plugin_name(plugin_name: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", plugin_name))


def build_plugin_json(
    plugin_name: str,
    *,
    with_skills: bool,
    with_hooks: bool,
    with_mcp: bool,
) -> dict[str, Any]:
    """Build the manifest Dim reads. Only the fields Dim parses are written."""
    display_name = display_name_from_plugin_name(plugin_name)
    payload: dict[str, Any] = {
        "name": plugin_name,
        "version": "0.1.0",
        "description": f"{display_name} plugin",
        "interface": {
            "displayName": display_name,
            "shortDescription": f"Use {display_name} in Dim.",
        },
    }
    # Component paths are added only when their companion files are created, so the manifest
    # never points at something that does not exist.
    if with_skills:
        payload["skills"] = "./skills/"
    if with_hooks:
        payload["hooks"] = "./hooks.json"
    if with_mcp:
        payload["mcpServers"] = "./.mcp.json"
    return payload


def build_starter_skill(plugin_name: str) -> str:
    """A minimal, valid starter skill so the plugin contributes something usable."""
    display_name = display_name_from_plugin_name(plugin_name)
    return (
        "---\n"
        f"name: {plugin_name}\n"
        f"description: {display_name} starter skill. Replace this description with the real "
        f"trigger so Dim knows when to use {display_name}.\n"
        "---\n\n"
        f"# {display_name}\n\n"
        "Describe what this skill does and the steps the assistant should follow when it is "
        "invoked. Keep instructions concrete and task-focused.\n"
    )


def build_starter_bin(plugin_name: str) -> str:
    """A POSIX wrapper on PATH. Command names are plugin-prefixed to avoid collisions."""
    return (
        "#!/usr/bin/env sh\n"
        f"# Entry point for the {plugin_name} plugin. The host puts this directory on the\n"
        "# agent's exec PATH, so this file is invoked by name. Keep support files elsewhere\n"
        "# in the plugin and reference them relative to this script.\n"
        'root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"\n'
        'echo "replace this with the real ${root} entry point"\n'
    )


def write_json(path: Path, data: dict, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def write_text(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Dim plugin skeleton with a validation-ready plugin.json."
    )
    parser.add_argument("plugin_name")
    parser.add_argument(
        "--path",
        default=str(DEFAULT_PLUGIN_PARENT),
        help=(
            "Parent directory for the plugin (defaults to ~/.agents/plugins, where Dim "
            "discovers plugins). Pass another directory to build a plugin for git sharing."
        ),
    )
    parser.add_argument(
        "--with-skills",
        action="store_true",
        help="Create skills/<name>/SKILL.md starter skill and set manifest `skills`.",
    )
    parser.add_argument(
        "--with-hooks",
        action="store_true",
        help="Create hooks.json and set manifest `hooks`.",
    )
    parser.add_argument(
        "--with-mcp",
        action="store_true",
        help="Create .mcp.json and set manifest `mcpServers`.",
    )
    parser.add_argument(
        "--with-bin",
        action="store_true",
        help=(
            "Create bin/<name>, an executable the host puts on the agent's exec PATH. Only "
            "needed when something outside the plugin's own MCP/hook wiring must run a command."
        ),
    )
    parser.add_argument(
        "--with-assets",
        action="store_true",
        help="Create an assets/ directory for icons and logos.",
    )
    parser.add_argument(
        "--manifest-format",
        choices=sorted(MANIFEST_DIRS),
        default="codex",
        help=(
            "Manifest directory to write: codex (.codex-plugin, default, probed first by Dim "
            "and used by the plugin store) or claude (.claude-plugin, for Claude Code "
            "compatibility). Never ship both."
        ),
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_plugin_name = args.plugin_name
    plugin_name = normalize_plugin_name(raw_plugin_name)
    if plugin_name != raw_plugin_name:
        print(f"Note: Normalized plugin name from '{raw_plugin_name}' to '{plugin_name}'.")
    validate_plugin_name(plugin_name)

    plugin_root = Path(args.path).expanduser().resolve() / plugin_name
    plugin_root.mkdir(parents=True, exist_ok=True)

    manifest_path = plugin_root / MANIFEST_DIRS[args.manifest_format] / MANIFEST_FILE
    write_json(
        manifest_path,
        build_plugin_json(
            plugin_name,
            with_skills=args.with_skills,
            with_hooks=args.with_hooks,
            with_mcp=args.with_mcp,
        ),
        args.force,
    )

    if args.with_skills:
        write_text(
            plugin_root / "skills" / plugin_name / "SKILL.md",
            build_starter_skill(plugin_name),
            args.force,
        )

    if args.with_hooks:
        # Empty hooks map; fill events with commands that use ${CLAUDE_PLUGIN_ROOT} paths.
        write_json(plugin_root / "hooks.json", {"hooks": {}}, args.force)

    if args.with_mcp:
        write_json(plugin_root / ".mcp.json", {"mcpServers": {}}, args.force)

    if args.with_bin:
        bin_entry = plugin_root / "bin" / plugin_name
        write_text(bin_entry, build_starter_bin(plugin_name), args.force)
        bin_entry.chmod(0o755)

    if args.with_assets:
        (plugin_root / "assets").mkdir(parents=True, exist_ok=True)

    print(f"Created plugin scaffold: {plugin_root}")
    print(f"plugin manifest: {manifest_path}")
    if args.with_mcp:
        print("next: fill .mcp.json — see references/mcp-servers.md (stdio cwd defaults to the "
              "plugin root; use http_headers, not headers, for remote servers)")
    if args.with_hooks:
        print("next: fill hooks.json — one unrecognized event name drops every hook in the file")


if __name__ == "__main__":
    main()
