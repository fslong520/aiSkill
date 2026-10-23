#!/usr/bin/env python3
"""Freeze hashes and dimensions for the exact artifacts sent to final visual QA."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image

EXPECTED_JOBS = {
    "base",
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
    "look-cardinals",
    "look-row-9",
    "look-row-10",
}
EXPECTED_JOB_OUTPUTS = {
    job_id: f"decoded/{job_id}.png" for job_id in EXPECTED_JOBS
}
PREVIEW_FRAMES = {
    "idle": 6,
    "running-right": 8,
    "running-left": 8,
    "waving": 4,
    "jumping": 5,
    "failed": 8,
    "waiting": 6,
    "running": 6,
    "review": 6,
}
IMAGE_DIMENSIONS = {
    "qa/contact-sheet.png": (768, 1134),
    "qa/contact-sheet-extended.png": (768, 1386),
    "qa/look-directions.png": (1536, 1170),
    "qa/direction-blind-pairs.png": (384, 3304),
}
JSON_ARTIFACTS = [
    "final/validation-extended.json",
    "qa/chroma-despill-extended.json",
    "qa/review.json",
    "qa/direction-blind-answer-key.json",
    "qa/direction-blind-verdicts-1.json",
    "qa/direction-blind-verdicts-2.json",
    "qa/direction-blind-verdicts-3.json",
    "qa/direction-blind-verdicts.json",
    "qa/direction-blind-validation.json",
    "qa/look-continuity.json",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def read_object(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        fail(f"{label} is missing or is not a regular file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not valid UTF-8 JSON: {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(run_dir: Path, relative_path: str) -> dict[str, object]:
    path = run_dir / relative_path
    if not path.is_file() or path.is_symlink():
        fail(f"QA artifact is missing or is not a regular file: {path}")
    return {
        "path": relative_path,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def validate_jobs(run_dir: Path, run_id: str) -> dict[str, dict[str, object]]:
    manifest = read_object(run_dir / "imagegen-jobs.json", "image generation manifest")
    if manifest.get("run_id") != run_id:
        fail("pet_request.json and imagegen-jobs.json run_id values must match")
    jobs = manifest.get("jobs")
    if not isinstance(jobs, list):
        fail("image generation manifest jobs must be an array")
    if len(jobs) != len(EXPECTED_JOBS) or any(not isinstance(job, dict) for job in jobs):
        fail("image generation manifest must contain exactly 13 job objects")
    by_id = {
        job.get("id"): job
        for job in jobs
        if isinstance(job, dict) and isinstance(job.get("id"), str)
    }
    if len(by_id) != len(jobs) or set(by_id) != EXPECTED_JOBS:
        fail("image generation manifest must contain exactly the 13 hatch-pet jobs")

    result: dict[str, dict[str, object]] = {}
    for job_id in sorted(EXPECTED_JOBS):
        job = by_id[job_id]
        if job.get("status") != "complete":
            fail(f"image generation job is not complete: {job_id}")
        output_path = job.get("output_path")
        if output_path != EXPECTED_JOB_OUTPUTS[job_id]:
            fail(f"image generation job has an invalid output_path: {job_id}")
        completed_at = job.get("completed_at")
        if not isinstance(completed_at, str) or not completed_at:
            fail(f"image generation job has no completed_at provenance: {job_id}")
        source_path = job.get("source_path")
        if not isinstance(source_path, str) or not source_path:
            fail(f"image generation job has no source_path provenance: {job_id}")
        result[job_id] = artifact(run_dir, output_path)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = read_object(run_dir / "pet_request.json", "pet request")
    run_id = request.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        fail("pet_request.run_id must be a non-empty string")

    atlas_relative = "final/spritesheet-extended.webp"
    atlas = run_dir / atlas_relative
    atlas_artifact = artifact(run_dir, atlas_relative)
    with Image.open(atlas) as opened:
        if opened.size != (1536, 2288):
            fail(f"final atlas must be 1536x2288; got {opened.width}x{opened.height}")

    artifacts: dict[str, object] = {"atlas": atlas_artifact}
    for relative_path, expected_size in IMAGE_DIMENSIONS.items():
        path = run_dir / relative_path
        with Image.open(path) as opened:
            if opened.size != expected_size:
                fail(
                    f"{relative_path} must be {expected_size[0]}x{expected_size[1]}; "
                    f"got {opened.width}x{opened.height}"
                )
        artifacts[relative_path] = artifact(run_dir, relative_path)

    for relative_path in JSON_ARTIFACTS:
        read_object(run_dir / relative_path, relative_path)
        artifacts[relative_path] = artifact(run_dir, relative_path)

    preview_artifacts: dict[str, object] = {}
    for state, expected_frames in PREVIEW_FRAMES.items():
        relative_path = f"qa/previews/{state}.gif"
        path = run_dir / relative_path
        with Image.open(path) as opened:
            if opened.size != (192, 208):
                fail(f"{relative_path} must be 192x208")
            if getattr(opened, "n_frames", 1) != expected_frames:
                fail(f"{relative_path} must contain {expected_frames} frames")
        preview_artifacts[state] = artifact(run_dir, relative_path)
    artifacts["previews"] = preview_artifacts

    canonical_base = artifact(run_dir, "references/canonical-base.png")
    references: dict[str, object] = {}
    raw_references = request.get("references")
    if not isinstance(raw_references, list):
        fail("pet_request.references must be an array")
    for index, entry in enumerate(raw_references):
        if not isinstance(entry, dict):
            fail(f"pet_request.references[{index}] must be an object")
        copied_path = entry.get("copied_path")
        if not isinstance(copied_path, str):
            fail(f"pet_request.references[{index}].copied_path must be a string")
        path = Path(copied_path).resolve()
        try:
            relative_path = str(path.relative_to(run_dir))
        except ValueError:
            fail(f"copied reference escapes the run directory: {path}")
        references[relative_path] = artifact(run_dir, relative_path)

    output = (
        Path(args.output).expanduser().resolve()
        if args.output
        else run_dir / "qa" / "final-visual-qa-input.json"
    )
    payload = {
        "schema_version": 1,
        "run_id": run_id,
        "atlas_sha256": atlas_artifact["sha256"],
        "artifacts": artifacts,
        "job_outputs": validate_jobs(run_dir, run_id),
        "canonical_base": canonical_base,
        "uploaded_references": references,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "run_id": run_id,
                "atlas_sha256": atlas_artifact["sha256"],
                "qa_input": str(output),
                "qa_input_sha256": sha256(output),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
