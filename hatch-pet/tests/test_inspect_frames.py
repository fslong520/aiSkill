import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

SKILL_DIR = Path(__file__).resolve().parents[1]
INSPECT_PATH = SKILL_DIR / "scripts" / "inspect_frames.py"


def _cell(secondary: tuple[int, int, int, int] | None = None) -> Image.Image:
    """A 192x208 cell: one rectangular body (100x130 = 13000 px), optionally a
    detached secondary blob well to its left."""
    cell = Image.new("RGBA", (192, 208), (0, 0, 0, 0))
    draw = ImageDraw.Draw(cell)
    draw.rectangle((50, 40, 150, 170), fill=(200, 150, 120, 255))  # main body
    if secondary is not None:
        draw.rectangle(secondary, fill=(200, 150, 120, 255))
    return cell


class InspectFramesSecondaryComponentTest(unittest.TestCase):
    """A frame with a second pose-sized component fails the row (crammed pose / stray)."""

    def _run(self, cells: list[Image.Image]) -> tuple[int, dict]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        state_dir = root / "running-left"
        state_dir.mkdir(parents=True)
        for index, cell in enumerate(cells):
            cell.save(state_dir / f"{index:02d}.png")
        (root / "frames-manifest.json").write_text(
            json.dumps(
                {
                    "chroma_key": {"rgb": [255, 0, 255]},
                    "rows": [{"state": "running-left", "method": "components"}],
                }
            )
        )
        report_path = root / "report.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(INSPECT_PATH),
                "--frames-root",
                str(root),
                "--json-out",
                str(report_path),
                "--states",
                "running-left",
                "--require-components",
            ],
            capture_output=True,
            text=True,
        )
        return completed.returncode, json.loads(report_path.read_text())

    def test_clean_row_passes(self) -> None:
        code, report = self._run([_cell() for _ in range(8)])
        self.assertEqual(code, 0)
        self.assertTrue(report["ok"])

    def test_second_pose_sized_component_fails_the_row(self) -> None:
        cells = [_cell() for _ in range(8)]
        # Frame 3 gains a detached 31x71 ~= 2200 px second blob (>128 and >15% of body).
        cells[3] = _cell(secondary=(5, 70, 35, 140))
        code, report = self._run(cells)
        self.assertNotEqual(code, 0)
        self.assertFalse(report["ok"])
        self.assertTrue(
            any("second pose-sized component" in error for error in report["errors"]),
            report["errors"],
        )

    def test_tiny_second_component_is_ignored(self) -> None:
        cells = [_cell() for _ in range(8)]
        # A sub-floor speck (6x6 = 36 px < 128) must NOT fail the row.
        cells[3] = _cell(secondary=(10, 90, 16, 96))
        code, report = self._run(cells)
        self.assertEqual(code, 0, report["errors"])
        self.assertTrue(report["ok"])


if __name__ == "__main__":
    unittest.main()
