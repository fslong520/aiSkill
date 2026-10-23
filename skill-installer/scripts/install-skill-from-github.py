#!/usr/bin/env python3
"""Install a skill from a GitHub repo path into $AGENTS_HOME/skills."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import zipfile

from github_utils import github_request
from skill_roots import (
    installed_by_name,
    installed_plugin_dirs,
    private_plugins_root,
    private_skills_root,
    read_skill_name,
    shared_skills_root,
)

DEFAULT_REF = "main"


@dataclass
class Args:
    url: str | None = None
    repo: str | None = None
    path: list[str] | None = None
    ref: str = DEFAULT_REF
    dest: str | None = None
    name: str | None = None
    method: str = "auto"
    as_plugin: bool = False
    plugin_name: str | None = None
    shared: bool = False
    overwrite: bool = False
    list_candidates: bool = False
    format: str = "text"


@dataclass
class Source:
    owner: str
    repo: str
    ref: str
    paths: list[str]
    repo_url: str | None = None


class InstallError(Exception):
    pass


def _tmp_root() -> str:
    base = os.path.join(tempfile.gettempdir(), "agents")
    os.makedirs(base, exist_ok=True)
    return base


def _request(url: str) -> bytes:
    return github_request(url, "agents-skill-install")


def _parse_github_url(url: str, default_ref: str) -> tuple[str, str, str, str | None]:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "github.com":
        raise InstallError("Only GitHub URLs are supported for download mode.")
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise InstallError("Invalid GitHub URL.")
    owner, repo = parts[0], parts[1]
    ref = default_ref
    subpath = ""
    if len(parts) > 2:
        if parts[2] in ("tree", "blob"):
            if len(parts) < 4:
                raise InstallError("GitHub URL missing ref or path.")
            ref = parts[3]
            subpath = "/".join(parts[4:])
        else:
            subpath = "/".join(parts[2:])
    return owner, repo, ref, subpath or None


def _download_repo_zip(owner: str, repo: str, ref: str, dest_dir: str) -> str:
    zip_url = f"https://codeload.github.com/{owner}/{repo}/zip/{ref}"
    zip_path = os.path.join(dest_dir, "repo.zip")
    try:
        payload = _request(zip_url)
    except urllib.error.HTTPError as exc:
        raise InstallError(f"Download failed: HTTP {exc.code}") from exc
    with open(zip_path, "wb") as file_handle:
        file_handle.write(payload)
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        _safe_extract_zip(zip_file, dest_dir)
        top_levels = {name.split("/")[0] for name in zip_file.namelist() if name}
    if not top_levels:
        raise InstallError("Downloaded archive was empty.")
    if len(top_levels) != 1:
        raise InstallError("Unexpected archive layout.")
    return os.path.join(dest_dir, next(iter(top_levels)))


def _run_git(args: list[str]) -> None:
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise InstallError(result.stderr.strip() or "Git command failed.")


def _safe_extract_zip(zip_file: zipfile.ZipFile, dest_dir: str) -> None:
    dest_root = os.path.realpath(dest_dir)
    for info in zip_file.infolist():
        extracted_path = os.path.realpath(os.path.join(dest_dir, info.filename))
        if extracted_path == dest_root or extracted_path.startswith(dest_root + os.sep):
            continue
        raise InstallError("Archive contains files outside the destination.")
    zip_file.extractall(dest_dir)


def _validate_relative_path(path: str) -> None:
    if os.path.isabs(path) or os.path.normpath(path).startswith(".."):
        raise InstallError("Skill path must be a relative path inside the repo.")


def _validate_skill_name(name: str) -> None:
    altsep = os.path.altsep
    if not name or os.path.sep in name or (altsep and altsep in name):
        raise InstallError("Skill name must be a single path segment.")
    if name in (".", ".."):
        raise InstallError("Invalid skill name.")


def _git_sparse_checkout(repo_url: str, ref: str, paths: list[str], dest_dir: str) -> str:
    repo_dir = os.path.join(dest_dir, "repo")
    clone_cmd = [
        "git",
        "clone",
        "--filter=blob:none",
        "--depth",
        "1",
        "--sparse",
        "--single-branch",
        "--branch",
        ref,
        repo_url,
        repo_dir,
    ]
    try:
        _run_git(clone_cmd)
    except InstallError:
        _run_git(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--depth",
                "1",
                "--sparse",
                "--single-branch",
                repo_url,
                repo_dir,
            ]
        )
    _run_git(["git", "-C", repo_dir, "sparse-checkout", "set", *paths])
    _run_git(["git", "-C", repo_dir, "checkout", ref])
    return repo_dir


def _validate_skill(path: str) -> None:
    if not os.path.isdir(path):
        raise InstallError(f"Skill path not found: {path}")
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        raise InstallError("SKILL.md not found in selected skill directory.")


def _copy_skill(src: str, dest_dir: str) -> None:
    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
    if os.path.exists(dest_dir):
        raise InstallError(f"Destination already exists: {dest_dir}")
    shutil.copytree(src, dest_dir)


def _build_repo_url(owner: str, repo: str) -> str:
    return f"https://github.com/{owner}/{repo}.git"


def _build_repo_ssh(owner: str, repo: str) -> str:
    return f"git@github.com:{owner}/{repo}.git"


def _prepare_repo(source: Source, method: str, tmp_dir: str) -> str:
    if method in ("download", "auto"):
        try:
            return _download_repo_zip(source.owner, source.repo, source.ref, tmp_dir)
        except InstallError as exc:
            if method == "download":
                raise
            err_msg = str(exc)
            if "HTTP 401" in err_msg or "HTTP 403" in err_msg or "HTTP 404" in err_msg:
                pass
            else:
                raise
    if method in ("git", "auto"):
        repo_url = source.repo_url or _build_repo_url(source.owner, source.repo)
        try:
            return _git_sparse_checkout(repo_url, source.ref, source.paths, tmp_dir)
        except InstallError:
            repo_url = _build_repo_ssh(source.owner, source.repo)
            return _git_sparse_checkout(repo_url, source.ref, source.paths, tmp_dir)
    raise InstallError("Unsupported method.")


def _resolve_source(args: Args) -> Source:
    if args.url:
        owner, repo, ref, url_path = _parse_github_url(args.url, args.ref)
        if args.path is not None:
            paths = list(args.path)
        elif url_path:
            paths = [url_path]
        else:
            paths = []
        if not paths:
            raise InstallError("Missing --path for GitHub URL.")
        return Source(owner=owner, repo=repo, ref=ref, paths=paths)

    if not args.repo:
        raise InstallError("Provide --repo or --url.")
    if "://" in args.repo:
        return _resolve_source(
            Args(url=args.repo, repo=None, path=args.path, ref=args.ref)
        )

    repo_parts = [p for p in args.repo.split("/") if p]
    if len(repo_parts) != 2:
        raise InstallError("--repo must be in owner/repo format.")
    if not args.path:
        raise InstallError("Missing --path for --repo.")
    paths = list(args.path)
    return Source(
        owner=repo_parts[0],
        repo=repo_parts[1],
        ref=args.ref,
        paths=paths,
    )


def _default_bundle_name(source: Source) -> str:
    """Name the bundle after the directory the skills came from.

    A collection lives under a category path (`.../web`), which reads better as
    a plugin name than the repo alone; a repo-root install falls back to the
    repo name.
    """
    if len(source.paths) == 1:
        base = os.path.basename(source.paths[0].rstrip("/"))
        if base:
            return f"{source.repo}-{base}"
    common = os.path.commonpath([p.rstrip("/") for p in source.paths]) if source.paths else ""
    base = os.path.basename(common)
    return f"{source.repo}-{base}" if base else source.repo


def _default_dest(shared: bool) -> str:
    """Dimcode's own skills root, unless the caller explicitly asked to share.

    Installing into `~/.agents/skills` makes the skill visible to other agents
    but takes it out of dimcode's update path, so it is never the default —
    only an explicit `--shared`.
    """
    return shared_skills_root() if shared else private_skills_root()


def _find_candidates(path: str) -> list[dict[str, str]]:
    """Skills one level under `path`, for a directory that is not itself a skill.

    A collection repo points at a category directory, not at a skill, so the
    caller needs the list before it can ask the user how to import them.
    """
    if not os.path.isdir(path):
        raise InstallError(f"Path not found: {path}")
    found = []
    for entry in sorted(os.listdir(path)):
        child = os.path.join(path, entry)
        if not os.path.isdir(child):
            continue
        name = read_skill_name(child)
        if name:
            found.append({"dir": entry, "name": name})
    return found


def _assert_no_name_conflict(names: list[str]) -> None:
    """Refuse to install a skill whose name is already taken.

    Skills are resolved by name and deduped across roots, so a second skill
    under an existing name is never the one that loads — installing it would
    report success and leave the user with a skill that silently does nothing.
    The user has to resolve it (remove, rename, or skip) before we write.
    """
    existing = installed_by_name()
    clashes = []
    for name in names:
        for owner in existing.get(name, []):
            clashes.append(f"  {name}: already installed as {owner.describe()}")
    if clashes:
        raise InstallError(
            "These skills are already installed under the same name:\n"
            + "\n".join(clashes)
            + "\nRemove or rename the existing one, or drop it from this install, then retry."
        )


def _synthesize_bundle(
    staged: list[tuple[str, str]],
    bundle_name: str,
    tmp_dir: str,
) -> str:
    """Package skills into a plugin bundle laid out for the plugin installer.

    Producing a real bundle — rather than writing into the plugins directory
    directly — is what lets the shared installer do the manifest validation,
    conflict check, provenance and atomic swap exactly once.
    """
    bundle_root = os.path.join(tmp_dir, "bundle", bundle_name)
    manifest_dir = os.path.join(bundle_root, ".codex-plugin")
    os.makedirs(manifest_dir, exist_ok=True)
    manifest = {
        "name": bundle_name,
        "version": "0.0.0",
        # Required by the manifest summary; a synthesized bundle has no
        # upstream description to carry, so it is explicitly empty.
        "description": "",
        "skills": "./skills",
        "interface": {"displayName": bundle_name},
    }
    with open(os.path.join(manifest_dir, "plugin.json"), "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    for skill_name, skill_src in staged:
        _validate_skill_name(skill_name)
        shutil.copytree(skill_src, os.path.join(bundle_root, "skills", skill_name))
    return bundle_root


def _dim_binary() -> str:
    return os.environ.get("DIMCODE_CLI_BIN", "dim")


def _install_bundle(
    bundle_root: str,
    bundle_name: str,
    provenance_source: str,
    ref: str,
    overwrite: bool,
    source_paths: list[str] | None = None,
) -> str:
    """Hand the staged bundle to the shared plugin installer."""
    installed_plugins = installed_plugin_dirs()
    if not overwrite and bundle_name in installed_plugins:
        raise InstallError(
            f'A plugin named "{bundle_name}" is already installed at '
            f"{installed_plugins[bundle_name]}.\n"
            "Pass --plugin-name to install under another name, or --overwrite to replace it."
        )
    cmd = [
        _dim_binary(), "plugin", "install", bundle_root,
        "--provenance-source", provenance_source,
        "--ref", ref,
        "--generated",
        "--generated-plugin-name", bundle_name,
        "--json",
    ]
    for source_path in source_paths or []:
        cmd.extend(["--generated-path", source_path])
    if overwrite:
        cmd.append("--overwrite")
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
    except OSError as exc:
        raise InstallError(
            f"Cannot run '{_dim_binary()} plugin install': {exc}. "
            "Set DIMCODE_CLI_BIN if the CLI is not on PATH."
        ) from exc
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise InstallError(f"Plugin install failed: {message or 'unknown error'}")
    fallback = os.path.join(private_plugins_root(), bundle_name)
    try:
        installed = json.loads(result.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return fallback
    return str(installed.get("path") or fallback)


def _parse_args(argv: list[str]) -> Args:
    parser = argparse.ArgumentParser(description="Install a skill from GitHub.")
    parser.add_argument("--repo", help="owner/repo")
    parser.add_argument("--url", help="https://github.com/owner/repo[/tree/ref/path]")
    parser.add_argument(
        "--path",
        nargs="+",
        help="Path(s) to skill(s) inside repo",
    )
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--dest", help="Destination skills directory")
    parser.add_argument(
        "--name", help="Destination skill name (defaults to basename of path)"
    )
    parser.add_argument(
        "--method",
        choices=["auto", "download", "git"],
        default="auto",
    )
    parser.add_argument(
        "--as-plugin",
        action="store_true",
        help="Package the selected skills into one plugin instead of installing them loose",
    )
    parser.add_argument(
        "--plugin-name",
        help="Plugin name for --as-plugin (defaults to the path or repo name)",
    )
    parser.add_argument(
        "--shared",
        action="store_true",
        help="Install into ~/.agents/skills so other agents see it (dimcode stops managing updates)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing plugin of the same name (--as-plugin only)",
    )
    parser.add_argument(
        "--list-candidates",
        action="store_true",
        help="List the skills under --path instead of installing, for a collection directory",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--generated-path", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--generated-plugin-name", help=argparse.SUPPRESS)
    return parser.parse_args(argv, namespace=Args())


def _report_candidates(paths: list[str], repo_root: str, fmt: str) -> int:
    """Print what lives under a directory that is not itself a skill."""
    payload = []
    for path in paths:
        target = os.path.join(repo_root, path)
        payload.append({"path": path, "skills": _find_candidates(target)})
    if fmt == "json":
        print(json.dumps(payload))
        return 0
    for entry in payload:
        skills = entry["skills"]
        if not skills:
            print(f"{entry['path']}: no skills found")
            continue
        print(f"{entry['path']}: {len(skills)} skills")
        for skill in skills:
            print(f"  {skill['name']}")
    return 0


def _stage_skills(source: Source, repo_root: str, args: Args) -> list[tuple[str, str]]:
    """Resolve each requested path to (skill name, source directory)."""
    staged: list[tuple[str, str]] = []
    for path in source.paths:
        skill_src = os.path.join(repo_root, path)
        _validate_skill(skill_src)
        override = args.name if len(source.paths) == 1 else None
        skill_name = override or read_skill_name(skill_src) or os.path.basename(path.rstrip("/"))
        _validate_skill_name(skill_name)
        staged.append((skill_name, skill_src))
    return staged


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    try:
        if args.as_plugin and args.dest:
            raise InstallError("--dest cannot be combined with --as-plugin.")
        if args.as_plugin and args.shared:
            raise InstallError(
                "--shared cannot be combined with --as-plugin; a bundle installs as a plugin."
            )
        source = _resolve_source(args)
        source.ref = source.ref or args.ref
        if not source.paths:
            raise InstallError("No skill paths provided.")
        for path in source.paths:
            _validate_relative_path(path)
        tmp_dir = tempfile.mkdtemp(prefix="skill-install-", dir=_tmp_root())
        try:
            repo_root = _prepare_repo(source, args.method, tmp_dir)

            if args.list_candidates:
                return _report_candidates(source.paths, repo_root, args.format)

            staged = _stage_skills(source, repo_root, args)
            # Names are how the runtime resolves skills, so a clash makes the
            # new copy unreachable. Check before writing anything, whichever
            # mode we are in.
            _assert_no_name_conflict([name for name, _ in staged])

            if args.as_plugin:
                bundle_name = args.plugin_name or _default_bundle_name(source)
                _validate_skill_name(bundle_name)
                bundle_root = _synthesize_bundle(staged, bundle_name, tmp_dir)
                path = _install_bundle(
                    bundle_root,
                    bundle_name,
                    f"{source.owner}/{source.repo}",
                    source.ref,
                    args.overwrite,
                    source.paths,
                )
                print(f"Installed plugin {bundle_name} ({len(staged)} skills) to {path}")
                return 0

            dest_root = args.dest or _default_dest(args.shared)
            installed = []
            for skill_name, skill_src in staged:
                dest_dir = os.path.join(dest_root, skill_name)
                if os.path.exists(dest_dir):
                    raise InstallError(f"Destination already exists: {dest_dir}")
                _copy_skill(skill_src, dest_dir)
                installed.append((skill_name, dest_dir))
        finally:
            if os.path.isdir(tmp_dir):
                shutil.rmtree(tmp_dir, ignore_errors=True)
        for skill_name, dest_dir in installed:
            print(f"Installed {skill_name} to {dest_dir}")
        return 0
    except InstallError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
