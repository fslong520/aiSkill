#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize any generated poster to a non-distorted 1080x1440 PNG."""

import argparse
import json
import sys
from pathlib import Path


WIDTH = 1080
HEIGHT = 1440


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    try:
        from PIL import Image, ImageFilter, ImageOps
    except ImportError:
        print(json.dumps({"ok": False, "error": "pillow_missing"}, ensure_ascii=False))
        return 2

    source_path = Path(args.input).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    if not source_path.is_file():
        print(json.dumps({"ok": False, "error": "input_missing"}, ensure_ascii=False))
        return 2

    try:
        with Image.open(source_path) as opened:
            source = ImageOps.exif_transpose(opened).convert("RGB")
        background = ImageOps.fit(source, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
        background = background.filter(ImageFilter.GaussianBlur(radius=32))
        foreground = ImageOps.contain(source, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
        x = (WIDTH - foreground.width) // 2
        y = (HEIGHT - foreground.height) // 2
        background.paste(foreground, (x, y))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        background.save(out_path, format="PNG", optimize=True)
    except Exception:
        print(json.dumps({"ok": False, "error": "poster_normalize_failed"}, ensure_ascii=False))
        return 2

    print(json.dumps({
        "ok": True,
        "format": "PNG",
        "width": WIDTH,
        "height": HEIGHT,
        "filePath": str(out_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
