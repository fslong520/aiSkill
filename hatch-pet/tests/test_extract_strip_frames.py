import importlib.util
import sys
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

SKILL_DIR = Path(__file__).resolve().parents[1]
EXTRACT_PATH = SKILL_DIR / "scripts" / "extract_strip_frames.py"
sys.path.insert(0, str(EXTRACT_PATH.parent))
SPEC = importlib.util.spec_from_file_location("extract_strip_frames", EXTRACT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {EXTRACT_PATH}")
EXTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXTRACT)


def _filled(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rectangle(box, fill=(0, 0, 0, 255))


class ExtractStripFramesFrameBleedTest(unittest.TestCase):
    """A detached fragment must stay in the column that owns it.

    The strip has two poses. Frame 0 owns a detached "arm" that sits inside its
    own column slot but whose ``center_x`` is nearer frame 1's body center. The
    old nearest-``center_x`` assignment pulled the arm across the boundary into
    frame 1 (frame 0 lost it, frame 1 gained a stray). Slot-based assignment
    keeps it in frame 0.
    """

    def _strip(self) -> Image.Image:
        # width 400, 2 frames -> slot_width 200; boundary at x=200.
        strip = Image.new("RGBA", (400, 208), (0, 0, 0, 0))
        draw = ImageDraw.Draw(strip)
        _filled(draw, (20, 40, 100, 180))    # frame 0 body, center_x 60, slot 0
        _filled(draw, (210, 40, 290, 180))   # frame 1 body, center_x 250, slot 1
        # frame 0's detached arm: center_x 165 (slot 0) but nearer seed 1 (250)
        # than seed 0 (60); separated from both bodies by a transparent gap.
        _filled(draw, (150, 90, 180, 130))
        return strip

    def test_detached_fragment_stays_in_its_own_column(self) -> None:
        strip = self._strip()

        groups = EXTRACT.component_frame_groups(strip, 2)
        self.assertIsNotNone(groups)
        assert groups is not None

        def has_arm(group: list[dict[str, object]]) -> bool:
            return any(150 <= component["center_x"] <= 180 for component in group)

        # Groups are ordered left-to-right by seed center_x.
        self.assertTrue(has_arm(groups[0]), "frame 0 should keep its own arm")
        self.assertFalse(has_arm(groups[1]), "frame 1 must not receive the stray arm")

    def test_neither_frame_keeps_a_detached_fragment(self) -> None:
        strip = self._strip()

        frames = EXTRACT.extract_component_frames(strip, 2)
        self.assertIsNotNone(frames)
        assert frames is not None

        # The arm is grouped into its own slot (frame 0, not frame 1) — proven by
        # test_detached_fragment_stays_in_its_own_column — and then cleaned as a
        # detached fragment, so neither frame carries a stray blob.
        self.assertEqual(len(EXTRACT.connected_components(frames[0])), 1)
        self.assertEqual(len(EXTRACT.connected_components(frames[1])), 1)


class ExtractStripFramesDebrisTest(unittest.TestCase):
    """A small free-floating island inside a frame's slot must be dropped.

    Chroma/despill specks and detached fur wisps land in the strip beyond the
    poses. When one sits in a frame's column it survives grouping (it is above
    the noise floor and owns that slot) and would bake in as a stray pixel blob.
    The finished cell must keep only the pose body.
    """

    def _strip_with_speck(self) -> Image.Image:
        strip = Image.new("RGBA", (400, 208), (0, 0, 0, 0))
        draw = ImageDraw.Draw(strip)
        _filled(draw, (20, 40, 100, 180))    # frame 0 body (slot 0)
        _filled(draw, (210, 40, 290, 180))   # frame 1 body (slot 1)
        # frame 0 debris: 10x10 = 100 px, above the noise floor but below the
        # 128 px detached floor, separated from the body by a transparent gap.
        _filled(draw, (150, 95, 160, 105))
        return strip

    def test_small_detached_island_is_removed(self) -> None:
        frames = EXTRACT.extract_component_frames(self._strip_with_speck(), 2)
        self.assertIsNotNone(frames)
        assert frames is not None
        # Both cells are body-only; the speck is gone.
        self.assertEqual(len(EXTRACT.connected_components(frames[0])), 1)
        self.assertEqual(len(EXTRACT.connected_components(frames[1])), 1)

    @staticmethod
    def _fitted(rects: list[tuple[int, int, int, int]]) -> Image.Image:
        cell = Image.new("RGBA", (192, 208), (0, 0, 0, 0))
        draw = ImageDraw.Draw(cell)
        for rect in rects:
            _filled(draw, rect)
        return EXTRACT.fit_to_cell(cell)

    def test_detached_medium_fragment_is_dropped(self) -> None:
        # ~650 px fragment (well above 128) sitting ~29 px off a ~11k body, only
        # ~6% of it — the baobao-style echo the 128 floor and 15% ratio both miss.
        result = self._fitted([(40, 40, 120, 180), (150, 90, 170, 120)])
        self.assertEqual(len(EXTRACT.connected_components(result)), 1)

    def test_attached_part_is_kept(self) -> None:
        # A >=128 px part with a 2 px gap to the body is a real attached detail.
        result = self._fitted([(40, 40, 120, 180), (123, 90, 153, 130)])
        self.assertEqual(len(EXTRACT.connected_components(result)), 2)

    def test_large_second_mass_is_kept(self) -> None:
        # A detached component that is >=15% of the main body is a genuine second
        # mass; extraction keeps it and the row inspector flags the row instead.
        result = self._fitted([(40, 40, 110, 170), (140, 40, 180, 120)])
        self.assertEqual(len(EXTRACT.connected_components(result)), 2)


if __name__ == "__main__":
    unittest.main()
