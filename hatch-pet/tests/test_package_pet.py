import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
PACKAGE = SCRIPTS_DIR / "package_pet.py"
PREPARE_FINAL_QA = SCRIPTS_DIR / "prepare_final_visual_qa.py"
FRAME_COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
STATES = [
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
JOB_IDS = {
    "base",
    *STATES,
    "look-cardinals",
    "look-row-9",
    "look-row-10",
}
DIRECTIONS = [
    "000",
    "022.5",
    "045",
    "067.5",
    "090",
    "112.5",
    "135",
    "157.5",
    "180",
    "202.5",
    "225",
    "247.5",
    "270",
    "292.5",
    "315",
    "337.5",
]

def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_script(script_name: str, *arguments: object) -> None:
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name), *(str(value) for value in arguments)],
        check=True,
        capture_output=True,
        text=True,
    )


def save_preview(path: Path, frame_count: int) -> None:
    frames: list[Image.Image] = []
    for index in range(frame_count):
        frame = Image.new("RGBA", (192, 208), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        draw.rectangle(
            (50 + index, 55, 110 + index, 145),
            fill=(20, 40 + index, 80, 255),
        )
        frames.append(frame)
    frames[0].save(
        path,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        disposal=2,
        optimize=False,
    )


def create_valid_run(root: Path) -> Path:
    run_dir = root / "run"
    final_dir = run_dir / "final"
    qa_dir = run_dir / "qa"
    references_dir = run_dir / "references"
    decoded_dir = run_dir / "decoded"
    final_dir.mkdir(parents=True)
    (qa_dir / "previews").mkdir(parents=True)
    references_dir.mkdir(parents=True)
    decoded_dir.mkdir(parents=True)

    atlas = Image.new("RGBA", (1536, 2288), (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas)
    for row, frame_count in enumerate(FRAME_COUNTS):
        for column in range(frame_count):
            left = column * 192 + 60
            top = row * 208 + 60
            draw.rectangle(
                (left, top, left + 50, top + 70),
                fill=(20 + row, 40 + column, 80, 255),
            )
    extended_atlas = final_dir / "spritesheet-extended.webp"
    atlas.save(
        extended_atlas,
        format="WEBP",
        lossless=True,
        quality=100,
        method=6,
        exact=True,
    )
    atlas.crop((0, 0, 1536, 1872)).save(
        final_dir / "spritesheet.webp",
        format="WEBP",
        lossless=True,
        quality=100,
        method=6,
        exact=True,
    )

    run_id = "test-run-001"
    write_json(
        run_dir / "pet_request.json",
        {
            "run_id": run_id,
            "pet_id": "upload-buddy",
            "display_name": "Upload Buddy",
            "description": "A helpful uploaded companion.",
            "format": "dim-sprite-v2",
            "chroma_key": {"hex": "#FF00FF", "name": "magenta"},
            "references": [],
        },
    )

    canonical_base = references_dir / "canonical-base.png"
    Image.new("RGBA", (192, 208), (20, 40, 80, 255)).save(canonical_base)
    jobs = []
    for index, job_id in enumerate(sorted(JOB_IDS)):
        output_path = decoded_dir / f"{job_id}.png"
        Image.new("RGBA", (32, 32), (20 + index, 40, 80, 255)).save(output_path)
        jobs.append(
            {
                "id": job_id,
                "status": "complete",
                "output_path": str(output_path.relative_to(run_dir)),
                "source_path": f"/generated/{job_id}.png",
                "completed_at": "2026-07-28T00:00:00Z",
            }
        )
    write_json(run_dir / "imagegen-jobs.json", {"run_id": run_id, "jobs": jobs})

    write_json(final_dir / "validation-extended.json", {"ok": True, "rows": 11})
    write_json(qa_dir / "chroma-despill-extended.json", {"ok": True})
    write_json(qa_dir / "look-continuity.json", {"ok": True, "warnings": []})
    write_json(qa_dir / "review.json", {"errors": [], "warnings": []})

    run_script(
        "make_contact_sheet.py",
        final_dir / "spritesheet.webp",
        "--output",
        qa_dir / "contact-sheet.png",
    )
    run_script(
        "make_contact_sheet.py",
        extended_atlas,
        "--output",
        qa_dir / "contact-sheet-extended.png",
    )
    run_script(
        "make_direction_qa_sheet.py",
        extended_atlas,
        "--output",
        qa_dir / "look-directions.png",
    )
    run_script(
        "make_direction_blind_qa_sheet.py",
        extended_atlas,
        "--output",
        qa_dir / "direction-blind-pairs.png",
        "--answer-key",
        qa_dir / "direction-blind-answer-key.json",
    )

    answer_key = read_json(qa_dir / "direction-blind-answer-key.json")
    verdict_pairs = [
        {
            "pair": entry["pair"],
            "A": entry["A"]["expected_direction"],
            "B": entry["B"]["expected_direction"],
            "reason": "test landmark evidence",
        }
        for entry in answer_key["pairs"]
    ]
    verdict_paths = []
    for index in range(1, 4):
        verdict_path = qa_dir / f"direction-blind-verdicts-{index}.json"
        write_json(verdict_path, {"pairs": verdict_pairs})
        verdict_paths.append(verdict_path)
    combine_arguments: list[object] = []
    for verdict_path in verdict_paths:
        combine_arguments.extend(["--verdicts", verdict_path])
    run_script(
        "combine_direction_blind_verdicts.py",
        *combine_arguments,
        "--json-out",
        qa_dir / "direction-blind-verdicts.json",
    )
    run_script(
        "validate_direction_blind_verdicts.py",
        "--answer-key",
        qa_dir / "direction-blind-answer-key.json",
        "--verdicts",
        qa_dir / "direction-blind-verdicts.json",
        "--json-out",
        qa_dir / "direction-blind-validation.json",
    )

    for state, frame_count in zip(STATES, FRAME_COUNTS[:9], strict=True):
        save_preview(qa_dir / "previews" / f"{state}.gif", frame_count)

    run_script("prepare_final_visual_qa.py", "--run-dir", run_dir)
    atlas_sha256 = sha256(extended_atlas)
    write_json(
        qa_dir / "direction-semantics.json",
        {
            "run_id": run_id,
            "atlas_sha256": atlas_sha256,
            "directions": [
                {
                    "direction": direction,
                    "verdict": "pass",
                    "expected": "test direction",
                    "observed": "test landmark",
                    "reason": "test acceptance",
                }
                for direction in DIRECTIONS
            ],
        },
    )
    qa_input = qa_dir / "final-visual-qa-input.json"
    direction_semantics = qa_dir / "direction-semantics.json"
    write_json(
        qa_dir / "final-visual-qa.json",
        {
            "ok": True,
            "verdict": "pass",
            "run_id": run_id,
            "atlas_sha256": atlas_sha256,
            "qa_input_sha256": sha256(qa_input),
            "direction_semantics_sha256": sha256(direction_semantics),
            "reviewed_by": "independent-visual-worker",
            "qa_note": "All test visuals are acceptable.",
        },
    )
    return run_dir


def package(run_dir: Path, pets_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PACKAGE),
            "--run-dir",
            str(run_dir),
            "--pets-root",
            str(pets_root),
        ],
        capture_output=True,
        text=True,
    )


class PackagePetTest(unittest.TestCase):
    def test_installs_only_manifest_and_spritesheet_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"

            completed = package(run_dir, pets_root)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            pet_dir = pets_root / "upload-buddy"
            manifest = read_json(pet_dir / "pet.json")

            self.assertEqual(
                sorted(path.name for path in pet_dir.iterdir()),
                ["pet.json", "spritesheet.webp"],
            )
            self.assertEqual(
                manifest,
                {
                    "id": "upload-buddy",
                    "displayName": "Upload Buddy",
                    "description": "A helpful uploaded companion.",
                    "spriteVersionNumber": 2,
                    "spritesheetPath": "spritesheet.webp",
                },
            )
            self.assertEqual(Path(result["package"]), pet_dir.resolve())
            self.assertTrue((run_dir / "qa" / "package-validation.json").is_file())
            summary = read_json(run_dir / "qa" / "run-summary.json")
            self.assertEqual(summary["run_id"], "test-run-001")
            self.assertEqual(
                summary["atlas_sha256"],
                sha256(run_dir / "final" / "spritesheet-extended.webp"),
            )
            self.assertEqual(list(pets_root.glob(".pet-install-upload-buddy-*")), [])

    def test_rejects_description_longer_than_160_code_points(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"
            request_path = run_dir / "pet_request.json"
            request = read_json(request_path)
            request["description"] = "😀" * 161
            write_json(request_path, request)

            completed = package(run_dir, pets_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("at most 160 Unicode code points", completed.stderr)
            self.assertFalse((pets_root / "upload-buddy").exists())

    def test_failed_qa_leaves_no_partial_pet_or_temp_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"
            (run_dir / "qa" / "direction-semantics.json").unlink()

            completed = package(run_dir, pets_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse((pets_root / "upload-buddy").exists())
            self.assertEqual(
                list(pets_root.glob(".pet-install-upload-buddy-*"))
                if pets_root.exists()
                else [],
                [],
            )

    def test_existing_pet_id_fails_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"
            existing = pets_root / "upload-buddy"
            existing.mkdir(parents=True)
            marker = existing / "keep.txt"
            marker.write_text("keep", encoding="utf-8")

            completed = package(run_dir, pets_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(pets_root.glob(".pet-install-upload-buddy-*")), [])

    def test_stale_final_visual_report_fails_before_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"
            report_path = run_dir / "qa" / "final-visual-qa.json"
            report = read_json(report_path)
            report["atlas_sha256"] = "0" * 64
            write_json(report_path, report)

            completed = package(run_dir, pets_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("stale or mismatched", completed.stderr)
            self.assertFalse((pets_root / "upload-buddy").exists())

    def test_direction_semantics_modified_after_review_fails_before_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"
            semantics_path = run_dir / "qa" / "direction-semantics.json"
            semantics = read_json(semantics_path)
            semantics["directions"][0]["reason"] = "modified after independent review"
            write_json(semantics_path, semantics)

            completed = package(run_dir, pets_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("stale or mismatched", completed.stderr)
            self.assertFalse((pets_root / "upload-buddy").exists())

    def test_placeholder_visual_artifact_fails_before_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"
            Image.new("RGB", (16, 16), "white").save(
                run_dir / "qa" / "contact-sheet-extended.png"
            )

            completed = package(run_dir, pets_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("must be 768x1386", completed.stderr)
            self.assertFalse((pets_root / "upload-buddy").exists())

    def test_incomplete_generation_job_fails_before_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run_dir = create_valid_run(root)
            pets_root = root / "pets"
            jobs_path = run_dir / "imagegen-jobs.json"
            manifest = read_json(jobs_path)
            manifest["jobs"][0]["status"] = "pending"
            write_json(jobs_path, manifest)

            completed = package(run_dir, pets_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("job is not complete", completed.stderr)
            self.assertFalse((pets_root / "upload-buddy").exists())

    def test_success_reports_are_written_before_atomic_install(self) -> None:
        source = PACKAGE.read_text(encoding="utf-8")
        package_report = source.index("write_json(package_validation_path, validation)")
        summary_report = source.index("write_json(\n            run_summary_path")
        install = source.index("os.replace(staged_dir, target_dir)")

        self.assertLess(package_report, install)
        self.assertLess(summary_report, install)
        self.assertNotIn("write_json(", source[install:])


if __name__ == "__main__":
    unittest.main()
