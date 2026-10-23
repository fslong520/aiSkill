"""Where installed skills live, and what they are actually called.

A skill's identity is the `name` in its SKILL.md frontmatter, not its directory
name: that is the name the runtime loads it under, and two directories claiming
the same name means only one of them is ever reachable. Everything here reads
that name, and reads it from every root the runtime scans — including skills
that arrive inside plugin bundles, which a scan of the loose skills directories
alone would miss.
"""

from __future__ import annotations

from dataclasses import dataclass
import os


def dimcode_home() -> str:
    """`DIMCODE_HOME` -> `$XDG_CONFIG_HOME/.dimcode/v2` -> `~/.dimcode/v2`."""
    explicit = os.environ.get("DIMCODE_HOME", "").strip()
    if explicit:
        return os.path.abspath(os.path.expanduser(explicit))
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    if xdg:
        return os.path.abspath(os.path.join(os.path.expanduser(xdg), ".dimcode", "v2"))
    return os.path.abspath(os.path.expanduser("~/.dimcode/v2"))


def agents_home() -> str:
    return os.path.expanduser(os.environ.get("AGENTS_HOME", "~/.agents"))


def private_skills_root() -> str:
    """Where dimcode installs skills it manages."""
    return os.path.join(dimcode_home(), "skills")


def shared_skills_root() -> str:
    """Cross-agent skills directory; read here, written only on explicit request."""
    return os.path.join(agents_home(), "skills")


def private_plugins_root() -> str:
    return os.path.join(dimcode_home(), "plugins")


def shared_plugins_root() -> str:
    return os.path.join(agents_home(), "plugins")


def plugin_roots() -> list[str]:
    return [private_plugins_root(), shared_plugins_root()]


@dataclass
class InstalledSkill:
    """A skill already on disk, identified the way the runtime identifies it."""

    name: str
    path: str
    #: "private" | "shared" | "plugin"
    origin: str
    #: Owning plugin's directory name when origin == "plugin".
    plugin: str | None = None

    def describe(self) -> str:
        if self.origin == "plugin":
            return f"{self.name} (from plugin {self.plugin}, {self.path})"
        where = "dimcode" if self.origin == "private" else "shared agents dir"
        return f"{self.name} ({where}, {self.path})"


def read_skill_name(skill_dir: str) -> str | None:
    """The frontmatter `name`, or None when this isn't a readable skill dir.

    Falls back to the directory name only when the file exists but declares no
    name — the runtime does the same, and refusing to see such a skill would
    make it invisible to the conflict check that exists to protect it.
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None
    try:
        with open(skill_md, encoding="utf-8") as handle:
            head = handle.read(4096)
    except OSError:
        return None
    if not head.startswith("---"):
        return os.path.basename(skill_dir.rstrip("/\\"))
    end = head.find("\n---", 3)
    frontmatter = head[3:end] if end != -1 else head[3:]
    for line in frontmatter.splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "name":
            name = value.strip().strip("'\"")
            if name:
                return name
    return os.path.basename(skill_dir.rstrip("/\\"))


def _scan_loose(root: str, origin: str) -> list[InstalledSkill]:
    if not os.path.isdir(root):
        return []
    found: list[InstalledSkill] = []
    for entry in sorted(os.listdir(root)):
        path = os.path.join(root, entry)
        if not os.path.isdir(path):
            continue
        name = read_skill_name(path)
        if name:
            found.append(InstalledSkill(name=name, path=path, origin=origin))
    return found


def _scan_plugins() -> list[InstalledSkill]:
    found: list[InstalledSkill] = []
    for root in plugin_roots():
        if not os.path.isdir(root):
            continue
        for plugin in sorted(os.listdir(root)):
            skills_dir = os.path.join(root, plugin, "skills")
            if not os.path.isdir(skills_dir):
                continue
            for entry in sorted(os.listdir(skills_dir)):
                path = os.path.join(skills_dir, entry)
                if not os.path.isdir(path):
                    continue
                name = read_skill_name(path)
                if name:
                    found.append(
                        InstalledSkill(name=name, path=path, origin="plugin", plugin=plugin)
                    )
    return found


def installed_skills() -> list[InstalledSkill]:
    """Every skill the runtime can currently see, across every root."""
    return [
        *_scan_loose(private_skills_root(), "private"),
        *_scan_loose(shared_skills_root(), "shared"),
        *_scan_plugins(),
    ]


def installed_by_name() -> dict[str, list[InstalledSkill]]:
    out: dict[str, list[InstalledSkill]] = {}
    for skill in installed_skills():
        out.setdefault(skill.name, []).append(skill)
    return out


def installed_plugin_dirs() -> dict[str, str]:
    """Installed plugin directory name -> path, first root wins."""
    out: dict[str, str] = {}
    for root in plugin_roots():
        if not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            path = os.path.join(root, entry)
            if entry in out or not os.path.isdir(path):
                continue
            if ".installing-" in entry or ".backup-" in entry:
                continue
            out[entry] = path
    return out
