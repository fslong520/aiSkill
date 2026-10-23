#!/usr/bin/env python3
"""Validate and atomically install a completed Codex v2 Pet run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

PET_ID_PATTERN = re.compile(r"^[a-z0-9._-]+$")
FORMAT = "dim-sprite-v2"
MANIFEST_FILENAME = "pet.json"
SPRITESHEET_FILENAME = "spritesheet.webp"
EXPECTED_DIRECTIONS = [
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
MAX_MANIFEST_BYTES = 64 * 1024
MAX_SPRITESHEET_BYTES = 20 * 1024 * 1024
MAX_DESCRIPTION_CODE_POINTS = 160


def fail(message: str) -> None:
    raise SystemExit(message)


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        fail(f"{label} is missing or is not a regular file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not valid UTF-8 JSON: {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object: {path}")
    return value


def require_non_empty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def require_ok_report(path: Path, label: str) -> dict[str, Any]:
    report = read_json_object(path, label)
    if report.get("ok") is not True:
        fail(f"{label} must contain ok=true: {path}")
    return report


def validate_request(request: dict[str, Any]) -> dict[str, Any]:
    pet_id = require_non_empty_string(request.get("pet_id"), "pet_request.pet_id")
    if PET_ID_PATTERN.fullmatch(pet_id) is None:
        fail("pet_request.pet_id must match [a-z0-9._-]+")
    if pet_id.startswith("bundled-"):
        fail('pet_request.pet_id must not use the reserved "bundled-" prefix')

    name = require_non_empty_string(request.get("display_name"), "pet_request.display_name")
    description = require_non_empty_string(
        request.get("description"),
        "pet_request.description",
    )
    if len(description.strip()) > MAX_DESCRIPTION_CODE_POINTS:
        fail(
            "pet_request.description must be at most "
            f"{MAX_DESCRIPTION_CODE_POINTS} Unicode code points"
        )
    if request.get("format") != FORMAT:
        fail(f'pet_request.format must equal "{FORMAT}"')

    return {
        "id": pet_id,
        "displayName": name,
        "description": description,
        "spriteVersionNumber": 2,
        "spritesheetPath": SPRITESHEET_FILENAME,
    }


def validate_direction_semantics(
    path: Path,
    *,
    run_id: str,
    atlas_sha256: str,
) -> None:
    report = read_json_object(path, "direction semantics report")
    if report.get("run_id") != run_id or report.get("atlas_sha256") != atlas_sha256:
        fail("direction semantics report does not match the current run and atlas")
    directions = report.get("directions")
    if not isinstance(directions, list):
        fail("direction semantics report must contain a directions array")

    labels: list[str] = []
    for index, entry in enumerate(directions):
        if not isinstance(entry, dict):
            fail(f"direction semantics directions[{index}] must be an object")
        label = require_non_empty_string(
            entry.get("direction"),
            f"direction semantics directions[{index}].direction",
        )
        verdict = entry.get("verdict")
        if verdict not in {"pass", "warning", "fail"}:
            fail(
                f"direction semantics directions[{index}].verdict "
                "must be pass, warning, or fail"
            )
        if verdict == "fail":
            fail(f"direction semantics contains a failed direction: {label}")
        require_non_empty_string(
            entry.get("expected"),
            f"direction semantics directions[{index}].expected",
        )
        require_non_empty_string(
            entry.get("observed"),
            f"direction semantics directions[{index}].observed",
        )
        require_non_empty_string(
            entry.get("reason"),
            f"direction semantics directions[{index}].reason",
        )
        labels.append(label)
    if labels != EXPECTED_DIRECTIONS:
        fail("direction semantics must contain all 16 directions in fixed clockwise order")


def validate_blind_review(
    run_dir: Path,
    *,
    run_id: str,
    atlas_sha256: str,
) -> None:
    qa_dir = run_dir / "qa"
    answer_key_path = qa_dir / "direction-blind-answer-key.json"
    consensus_path = qa_dir / "direction-blind-verdicts.json"
    answer_key = read_json_object(answer_key_path, "blind direction answer key")
    consensus = read_json_object(consensus_path, "blind direction consensus")
    validation = read_json_object(
        qa_dir / "direction-blind-validation.json",
        "blind direction validation",
    )
    verdict_paths = [
        qa_dir / f"direction-blind-verdicts-{index}.json" for index in range(1, 4)
    ]
    for index, path in enumerate(verdict_paths, start=1):
        verdict = read_json_object(path, f"blind direction verdict {index}")
        if not isinstance(verdict.get("pairs"), list) or len(verdict["pairs"]) != 14:
            fail(f"blind direction verdict {index} must contain all 14 pairs")
    if answer_key.get("atlas_sha256") != atlas_sha256:
        fail("blind direction answer key does not match the current atlas")
    if not isinstance(answer_key.get("pairs"), list) or len(answer_key["pairs"]) != 14:
        fail("blind direction answer key must contain all 14 pairs")
    if consensus.get("review_count") != 3:
        fail("blind direction consensus must combine exactly three isolated reviews")
    expected_input_hashes = [sha256(path) for path in verdict_paths]
    if consensus.get("input_sha256") != expected_input_hashes:
        fail("blind direction consensus input hashes do not match the isolated reviews")
    if not isinstance(consensus.get("pairs"), list) or len(consensus["pairs"]) != 14:
        fail("blind direction consensus must contain all 14 pairs")
    if (
        validation.get("atlas_sha256") != atlas_sha256
        or validation.get("answer_key_sha256") != sha256(answer_key_path)
        or validation.get("verdicts_sha256") != sha256(consensus_path)
    ):
        fail("blind direction validation is stale or does not match its inputs")
    if not isinstance(validation.get("pairs"), list) or len(validation["pairs"]) != 14:
        fail("blind direction validation must contain all 14 pair results")
    if validation.get("ok") is True:
        return

    resolution = read_json_object(
        qa_dir / "blind-review-resolution.json",
        "blind review resolution",
    )
    if resolution.get("decision") != "accept" or resolution.get("severity") != "minor":
        fail("failed blind direction validation requires an accepted minor resolution")
    if resolution.get("run_id") != run_id or resolution.get("atlas_sha256") != atlas_sha256:
        fail("blind review resolution does not match the current run and atlas")
    require_non_empty_string(resolution.get("reviewed_by"), "blind review resolution.reviewed_by")


def require_file(path: Path, label: str) -> None:
    if not path.is_file() or path.is_symlink():
        fail(f"{label} is missing or is not a regular file: {path}")


def prepare_final_visual_input(run_dir: Path) -> dict[str, Any]:
    descriptor, output_name = tempfile.mkstemp(
        prefix=".final-visual-qa-input.recheck-",
        suffix=".json",
        dir=run_dir / "qa",
    )
    os.close(descriptor)
    output = Path(output_name)
    completed = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve().parent / "prepare_final_visual_qa.py"),
            "--run-dir",
            str(run_dir),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"final visual QA inputs are incomplete or invalid: {detail}")
    try:
        return read_json_object(output, "recomputed final visual QA input")
    finally:
        output.unlink(missing_ok=True)


def validate_qa(
    run_dir: Path,
    *,
    run_id: str,
    atlas_sha256: str,
) -> None:
    qa_dir = run_dir / "qa"
    require_ok_report(qa_dir / "chroma-despill-extended.json", "chroma despill report")
    require_ok_report(qa_dir / "look-continuity.json", "look continuity report")

    review = read_json_object(qa_dir / "review.json", "standard-row review")
    errors = review.get("errors")
    if not isinstance(errors, list) or errors:
        fail("standard-row review must contain an empty errors array")

    validate_direction_semantics(
        qa_dir / "direction-semantics.json",
        run_id=run_id,
        atlas_sha256=atlas_sha256,
    )
    validate_blind_review(run_dir, run_id=run_id, atlas_sha256=atlas_sha256)

    recorded_input_path = qa_dir / "final-visual-qa-input.json"
    recorded_input = read_json_object(recorded_input_path, "final visual QA input")
    recomputed_input = prepare_final_visual_input(run_dir)
    if recorded_input != recomputed_input:
        fail("final visual QA input is stale or does not match the current artifacts")
    if (
        recorded_input.get("run_id") != run_id
        or recorded_input.get("atlas_sha256") != atlas_sha256
    ):
        fail("final visual QA input does not match the current run and atlas")

    final_review = read_json_object(
        qa_dir / "final-visual-qa.json",
        "final independent visual QA report",
    )
    if final_review.get("ok") is not True or final_review.get("verdict") != "pass":
        fail("final independent visual QA report must pass")
    if (
        final_review.get("run_id") != run_id
        or final_review.get("atlas_sha256") != atlas_sha256
        or final_review.get("qa_input_sha256") != sha256(recorded_input_path)
        or final_review.get("direction_semantics_sha256")
        != sha256(qa_dir / "direction-semantics.json")
    ):
        fail("final independent visual QA report is stale or mismatched")
    if final_review.get("reviewed_by") != "independent-visual-worker":
        fail("final visual QA must be recorded by an independent visual worker")
    require_non_empty_string(final_review.get("qa_note"), "final visual QA report.qa_note")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_atlas_validation(
    skill_dir: Path,
    atlas: Path,
    chroma_key: str,
    report_path: Path,
) -> dict[str, Any]:
    command = [
        sys.executable,
        str(skill_dir / "scripts" / "validate_atlas.py"),
        str(atlas),
        "--json-out",
        str(report_path),
        "--chroma-key",
        chroma_key,
        "--require-v2",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"packaged spritesheet failed v2 atlas validation: {detail}")
    return require_ok_report(report_path, "package atlas validation")


def write_json(path: Path, value: dict[str, Any]) -> None:
    encoded = (json.dumps(value, indent=2) + "\n").encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def default_pets_root() -> Path:
    dimcode_home = os.environ.get("DIMCODE_HOME")
    root = Path(dimcode_home).expanduser() if dimcode_home else Path.home() / ".dimcode" / "v2"
    return root / "pets"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--pets-root", default="")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    if not run_dir.is_dir():
        fail(f"run directory not found: {run_dir}")
    pets_root = (
        Path(args.pets_root).expanduser().resolve()
        if args.pets_root
        else default_pets_root().resolve()
    )
    skill_dir = Path(__file__).resolve().parents[1]

    request = read_json_object(run_dir / "pet_request.json", "pet request")
    manifest = validate_request(request)
    run_id = require_non_empty_string(request.get("run_id"), "pet_request.run_id")

    prior_validation = require_ok_report(
        run_dir / "final" / "validation-extended.json",
        "final atlas validation",
    )
    if prior_validation.get("rows") != 11:
        fail("final atlas validation must report exactly 11 rows")

    spritesheet = run_dir / "final" / "spritesheet-extended.webp"
    require_file(spritesheet, "final spritesheet")
    if spritesheet.stat().st_size > MAX_SPRITESHEET_BYTES:
        fail(f"final spritesheet exceeds {MAX_SPRITESHEET_BYTES} bytes")
    atlas_sha256 = sha256(spritesheet)
    validate_qa(run_dir, run_id=run_id, atlas_sha256=atlas_sha256)

    chroma_key = request.get("chroma_key")
    if not isinstance(chroma_key, dict):
        fail("pet_request.chroma_key must be an object")
    chroma_hex = require_non_empty_string(chroma_key.get("hex"), "pet_request.chroma_key.hex")

    encoded_manifest = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    if len(encoded_manifest) > MAX_MANIFEST_BYTES:
        fail(f"generated pet.json exceeds {MAX_MANIFEST_BYTES} bytes")

    pets_root.mkdir(parents=True, exist_ok=True)
    target_dir = pets_root / manifest["id"]
    if target_dir.exists():
        fail(f'Pet id "{manifest["id"]}" is already installed: {target_dir}')

    staged_dir = Path(
        tempfile.mkdtemp(prefix=f'.pet-install-{manifest["id"]}-', dir=pets_root)
    )
    package_validation_path = run_dir / "qa" / "package-validation.json"
    run_summary_path = run_dir / "qa" / "run-summary.json"
    pending_validation_path: Path | None = None
    try:
        pending_descriptor, pending_validation_name = tempfile.mkstemp(
            prefix=".package-validation.pending-",
            suffix=".json",
            dir=run_dir / "qa",
        )
        os.close(pending_descriptor)
        pending_validation_path = Path(pending_validation_name)

        staged_manifest = staged_dir / MANIFEST_FILENAME
        staged_spritesheet = staged_dir / SPRITESHEET_FILENAME
        staged_manifest.write_bytes(encoded_manifest)
        shutil.copyfile(spritesheet, staged_spritesheet)

        if sha256(staged_spritesheet) != atlas_sha256:
            fail("staged spritesheet bytes do not match the validated source")
        validation = run_atlas_validation(
            skill_dir,
            staged_spritesheet,
            chroma_hex,
            pending_validation_path,
        )

        if target_dir.exists():
            fail(f'Pet id "{manifest["id"]}" was installed concurrently: {target_dir}')

        validation["file"] = str(target_dir / SPRITESHEET_FILENAME)
        validation["validated_sha256"] = atlas_sha256
        write_json(package_validation_path, validation)
        write_json(
            run_summary_path,
            {
                "ok": True,
                "spriteVersionNumber": 2,
                "run_id": run_id,
                "atlas_sha256": atlas_sha256,
                "run_dir": str(run_dir),
                "spritesheet": str(run_dir / "final" / "spritesheet-extended.webp"),
                "validation": str(package_validation_path),
                "chroma_despill": str(run_dir / "qa" / "chroma-despill-extended.json"),
                "contact_sheet": str(run_dir / "qa" / "contact-sheet-extended.png"),
                "direction_sheet": str(run_dir / "qa" / "look-directions.png"),
                "direction_semantics": str(run_dir / "qa" / "direction-semantics.json"),
                "blind_direction_validation": str(
                    run_dir / "qa" / "direction-blind-validation.json"
                ),
                "continuity": str(run_dir / "qa" / "look-continuity.json"),
                "review": str(run_dir / "qa" / "review.json"),
                "final_visual_qa_input": str(
                    run_dir / "qa" / "final-visual-qa-input.json"
                ),
                "final_visual_qa": str(run_dir / "qa" / "final-visual-qa.json"),
                "package": str(target_dir),
            },
        )
        pending_validation_path.unlink(missing_ok=True)

        success_output = json.dumps(
            {
                "ok": True,
                "pet_id": manifest["id"],
                "package": str(target_dir),
                "manifest": str(target_dir / MANIFEST_FILENAME),
                "spritesheet": str(target_dir / SPRITESHEET_FILENAME),
                "qa_summary": str(run_summary_path),
            },
            indent=2,
        ) + "\n"
        os.replace(staged_dir, target_dir)
    except BaseException:
        if staged_dir.exists():
            shutil.rmtree(staged_dir, ignore_errors=True)
        if pending_validation_path is not None:
            pending_validation_path.unlink(missing_ok=True)
        package_validation_path.unlink(missing_ok=True)
        run_summary_path.unlink(missing_ok=True)
        raise

    try:
        sys.stdout.write(success_output)
        sys.stdout.flush()
    except OSError:
        pass


if __name__ == "__main__":
    main()
