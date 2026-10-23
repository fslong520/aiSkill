import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSEMBLER_PATH = SKILL_DIR / "scripts" / "assemble_extended_atlas.py"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_atlas.py"
sys.path.insert(0, str(ASSEMBLER_PATH.parent))
SPEC = importlib.util.spec_from_file_location("assemble_extended_atlas", ASSEMBLER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {ASSEMBLER_PATH}")
ASSEMBLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSEMBLER)


class DimCodeAtlasContractTest(unittest.TestCase):
    def run_validator(self, atlas: Image.Image) -> tuple[subprocess.CompletedProcess[str], dict]:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        atlas_path = root / "atlas.png"
        report_path = root / "validation.json"
        atlas.save(atlas_path)
        completed = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR_PATH),
                str(atlas_path),
                "--json-out",
                str(report_path),
                "--chroma-key",
                "#FF00FF",
                "--require-v2",
            ],
            capture_output=True,
            text=True,
        )
        return completed, json.loads(report_path.read_text())

    def test_v2_assembly_does_not_fill_unused_idle_column_six(self) -> None:
        atlas = Image.new("RGBA", (1536, 2288), (0, 0, 0, 0))
        look_cell = Image.new("RGBA", (192, 208), (0, 0, 0, 0))
        ImageDraw.Draw(look_cell).rectangle((30, 30, 80, 100), fill="white")

        ASSEMBLER.paste_look_cells(atlas, [look_cell] * 16)

        unused_idle = atlas.crop((6 * 192, 0, 7 * 192, 208))
        self.assertIsNone(unused_idle.getbbox())
        self.assertIsNotNone(atlas.crop((0, 9 * 208, 192, 10 * 208)).getbbox())

    def test_v2_validator_rejects_a_nontransparent_unused_idle_cell(self) -> None:
        atlas = Image.new("RGBA", (1536, 2288), (0, 0, 0, 0))
        draw = ImageDraw.Draw(atlas)
        frame_counts = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
        for row, frame_count in enumerate(frame_counts):
            for column in range(frame_count):
                left = column * 192 + 60
                top = row * 208 + 60
                draw.rectangle((left, top, left + 40, top + 60), fill="black")
        draw.rectangle((6 * 192 + 60, 60, 6 * 192 + 100, 120), fill="black")

        completed, report = self.run_validator(atlas)

        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(report["ok"])
        self.assertTrue(
            any("unused column 6 is not transparent" in error for error in report["errors"])
        )

    def test_v2_validator_rejects_a_nine_row_atlas(self) -> None:
        atlas = Image.new("RGBA", (1536, 1872), (0, 0, 0, 0))

        completed, report = self.run_validator(atlas)

        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(report["ok"])
        self.assertTrue(any("for a v2 pet" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
