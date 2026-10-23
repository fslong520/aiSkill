import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SKILL_DIR = Path(__file__).resolve().parents[1]
PREPARE = SKILL_DIR / "scripts" / "prepare_pet_run.py"
STANDARD_STATES = [
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
]


class PreparePetRunTest(unittest.TestCase):
    def test_uploaded_reference_grounds_every_generated_row(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            reference = root / "my-character.png"
            Image.new("RGBA", (96, 96), (20, 40, 80, 255)).save(reference)
            run_dir = root / "run"

            subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--pet-name",
                    "Upload Buddy",
                    "--reference",
                    str(reference),
                    "--output-dir",
                    str(run_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            request = json.loads((run_dir / "pet_request.json").read_text())
            jobs = json.loads((run_dir / "imagegen-jobs.json").read_text())["jobs"]

        self.assertEqual(request["format"], "dim-sprite-v2")
        self.assertNotIn("sprite_version_number", request)
        self.assertEqual(
            [row["state"] for row in request["rows"][:9]],
            STANDARD_STATES,
        )
        self.assertNotIn("fps", request)
        self.assertEqual(len(request["references"]), 1)

        base = next(job for job in jobs if job["id"] == "base")
        self.assertTrue(base["requires_grounded_generation"])
        self.assertFalse(base["allow_prompt_only_generation"])
        self.assertEqual(base["input_images"][0]["path"], "references/reference-01.png")

        for job in jobs:
            if job["id"] == "base":
                continue
            self.assertTrue(job["requires_grounded_generation"], job["id"])
            self.assertFalse(job["allow_prompt_only_generation"], job["id"])
            paths = {image["path"] for image in job["input_images"]}
            self.assertIn("references/reference-01.png", paths, job["id"])
            self.assertIn("references/canonical-base.png", paths, job["id"])

        running_left = next(job for job in jobs if job["id"] == "running-left")
        self.assertIn("running-right", running_left["depends_on"])
        self.assertEqual(
            running_left["mirror_policy"]["may_derive_from"],
            "running-right",
        )

    def test_reserved_custom_pet_id_fails_before_creating_a_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            run_dir = Path(temporary_directory) / "run"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--pet-id",
                    "bundled-user-pet",
                    "--output-dir",
                    str(run_dir),
                ],
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn('must not use the reserved "bundled-" prefix', completed.stderr)
        self.assertFalse(run_dir.exists())

    def test_long_description_fails_before_creating_a_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            run_dir = Path(temporary_directory) / "run"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--description",
                    "😀" * 161,
                    "--output-dir",
                    str(run_dir),
                ],
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("at most 160 Unicode code points", completed.stderr)
        self.assertFalse(run_dir.exists())

    def test_missing_uploaded_reference_fails_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--reference",
                    str(root / "missing.png"),
                    "--output-dir",
                    str(root / "run"),
                ],
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("reference not found", completed.stderr)

    def test_force_replaces_the_entire_prior_run_and_assigns_a_new_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first_reference = root / "first.png"
            second_reference = root / "second.png"
            Image.new("RGBA", (32, 32), (10, 20, 30, 255)).save(first_reference)
            Image.new("RGBA", (32, 32), (40, 50, 60, 255)).save(second_reference)
            run_dir = root / "run"

            subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--pet-name",
                    "First Pet",
                    "--reference",
                    str(first_reference),
                    "--output-dir",
                    str(run_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            first_request = json.loads((run_dir / "pet_request.json").read_text())
            stale_artifact = run_dir / "final" / "stale.webp"
            stale_artifact.parent.mkdir()
            stale_artifact.write_bytes(b"stale")

            subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--pet-name",
                    "Second Pet",
                    "--reference",
                    str(second_reference),
                    "--output-dir",
                    str(run_dir),
                    "--force",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            second_request = json.loads((run_dir / "pet_request.json").read_text())

            self.assertNotEqual(first_request["run_id"], second_request["run_id"])
            self.assertEqual(second_request["display_name"], "Second Pet")
            self.assertFalse(stale_artifact.exists())
            self.assertEqual(
                Path(second_request["references"][0]["source_path"]),
                second_reference.resolve(),
            )

    def test_force_rejects_an_input_inside_the_run_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = root / "run"
            run_dir.mkdir()
            reference = run_dir / "input.png"
            Image.new("RGBA", (32, 32), (10, 20, 30, 255)).save(reference)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARE),
                    "--reference",
                    str(reference),
                    "--output-dir",
                    str(run_dir),
                    "--force",
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("input is inside the run directory", completed.stderr)
            self.assertTrue(reference.exists())


if __name__ == "__main__":
    unittest.main()
