"""Importing skills: where they land, and when the install must refuse.

Everything after the fetch is exercised here — classifying what the path holds,
refusing a name that is already taken, packaging a collection into one plugin —
by pointing the script at a local fixture instead of GitHub. The transport
itself (zip download, git sparse checkout) is untouched by these tests.
"""

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"


def write_skill(directory: Path, name: str, description: str = "does things") -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\nbody\n", encoding="utf-8"
    )
    return directory


# Runs the script's main() with the fetch stubbed out to a local directory, and
# with `dim` replaced by a stub that behaves like the real plugin installer:
# it copies the staged bundle into the plugins root and prints the JSON record.
DRIVER = textwrap.dedent(
    """
    import json, os, shutil, sys
    sys.path.insert(0, os.environ["SCRIPTS_DIR"])
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "installer", os.path.join(os.environ["SCRIPTS_DIR"], "install-skill-from-github.py")
    )
    installer = importlib.util.module_from_spec(spec)
    sys.modules["installer"] = installer
    spec.loader.exec_module(installer)

    installer._prepare_repo = lambda source, method, tmp_dir: os.environ["REPO_ROOT"]

    def fake_install_bundle(bundle_root, bundle_name, provenance_source, ref, overwrite, source_paths=None):
        import skill_roots
        dest = os.path.join(skill_roots.private_plugins_root(), bundle_name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(dest):
            if not overwrite:
                raise installer.InstallError("already installed")
            shutil.rmtree(dest)
        shutil.copytree(bundle_root, dest)
        with open(os.path.join(dest, "dim-install.json"), "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "source": provenance_source,
                    "ref": ref,
                    "generated": True,
                    "generatedPaths": source_paths or [],
                    "generatedPluginName": bundle_name,
                }, fh
            )
        return dest

    installer._install_bundle = fake_install_bundle
    raise SystemExit(installer.main(json.loads(os.environ["ARGV"])))
    """
)


class InstallSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.home = root / "home"
        self.dimcode_home = self.home / ".dimcode" / "v2"
        self.repo = root / "repo"
        (self.home / ".agents" / "skills").mkdir(parents=True)
        (self.dimcode_home / "skills").mkdir(parents=True)
        self.addCleanup(self._tmp.cleanup)

    def run_installer(self, argv: list[str]) -> subprocess.CompletedProcess:
        env = {
            **os.environ,
            "HOME": str(self.home),
            "AGENTS_HOME": str(self.home / ".agents"),
            "DIMCODE_HOME": str(self.dimcode_home),
            "SCRIPTS_DIR": str(SCRIPTS_DIR),
            "REPO_ROOT": str(self.repo),
            "ARGV": json.dumps(argv),
        }
        env.pop("XDG_CONFIG_HOME", None)
        return subprocess.run(
            [sys.executable, "-c", DRIVER],
            capture_output=True,
            text=True,
            env=env,
        )

    def test_installs_into_dimcode_own_root_by_default(self) -> None:
        write_skill(self.repo / "pdf", "pdf")

        result = self.run_installer(["--repo", "acme/skills", "--path", "pdf"])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.dimcode_home / "skills" / "pdf" / "SKILL.md").is_file())
        self.assertFalse((self.home / ".agents" / "skills" / "pdf").exists())

    def test_shared_flag_installs_into_the_cross_agent_directory(self) -> None:
        write_skill(self.repo / "pdf", "pdf")

        result = self.run_installer(["--repo", "acme/skills", "--path", "pdf", "--shared"])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / ".agents" / "skills" / "pdf" / "SKILL.md").is_file())
        self.assertFalse((self.dimcode_home / "skills" / "pdf").exists())

    def test_directory_name_is_not_the_skill_identity(self) -> None:
        # The runtime resolves the frontmatter name, so that is what the install
        # is named after — not the folder it happened to sit in upstream.
        write_skill(self.repo / "folder-name", "actual-name")

        result = self.run_installer(["--repo", "acme/skills", "--path", "folder-name"])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.dimcode_home / "skills" / "actual-name").is_dir())

    def test_lists_candidates_for_a_collection_directory(self) -> None:
        write_skill(self.repo / "web" / "better-ui", "better-ui")
        write_skill(self.repo / "web" / "better-colors", "better-colors")

        result = self.run_installer(
            ["--repo", "acme/skills", "--path", "web", "--list-candidates", "--format", "json"]
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        names = sorted(skill["name"] for skill in payload[0]["skills"])
        self.assertEqual(names, ["better-colors", "better-ui"])

    def test_refuses_a_name_already_taken_by_a_loose_skill(self) -> None:
        write_skill(self.repo / "pdf", "pdf")
        write_skill(self.home / ".agents" / "skills" / "pdf", "pdf")

        result = self.run_installer(["--repo", "acme/skills", "--path", "pdf"])

        self.assertEqual(result.returncode, 1)
        self.assertIn("already installed under the same name", result.stderr)
        self.assertFalse((self.dimcode_home / "skills" / "pdf").exists())

    def test_refuses_a_name_already_taken_by_a_plugin_bundled_skill(self) -> None:
        # A bundled skill occupies the name just as a loose one does; scanning
        # only the skills directories would miss it and install a dead copy.
        write_skill(self.repo / "better-ui", "better-ui")
        write_skill(self.dimcode_home / "plugins" / "web-pack" / "skills" / "better-ui", "better-ui")

        result = self.run_installer(["--repo", "acme/skills", "--path", "better-ui"])

        self.assertEqual(result.returncode, 1)
        self.assertIn("from plugin web-pack", result.stderr)

    def test_packages_a_collection_into_one_plugin(self) -> None:
        write_skill(self.repo / "web" / "better-ui", "better-ui")
        write_skill(self.repo / "web" / "better-colors", "better-colors")

        result = self.run_installer(
            [
                "--repo", "acme/skills",
                "--path", "web/better-ui", "web/better-colors",
                "--as-plugin", "--plugin-name", "web-pack",
            ]
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        bundle = self.dimcode_home / "plugins" / "web-pack"
        manifest = json.loads((bundle / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "web-pack")
        self.assertEqual(manifest["description"], "")
        self.assertEqual(manifest["skills"], "./skills")
        self.assertTrue((bundle / "skills" / "better-ui" / "SKILL.md").is_file())
        self.assertTrue((bundle / "skills" / "better-colors" / "SKILL.md").is_file())
        # Provenance records the origin so a later reinstall can rebuild it.
        provenance = json.loads((bundle / "dim-install.json").read_text())
        self.assertEqual(provenance["source"], "acme/skills")
        self.assertTrue(provenance["generated"])
        # Nothing leaks into the loose skills directories.
        self.assertFalse((self.dimcode_home / "skills" / "better-ui").exists())

    def test_rejects_dest_combined_with_as_plugin(self) -> None:
        write_skill(self.repo / "pdf", "pdf")

        result = self.run_installer(
            ["--repo", "acme/skills", "--path", "pdf", "--as-plugin", "--dest", "/tmp/x"]
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("--dest cannot be combined with --as-plugin", result.stderr)


if __name__ == "__main__":
    unittest.main()
