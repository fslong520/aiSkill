#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a real PNG fallback for the "AI 祝福海报" playbook.

This renderer is used only when the current Agent has no native image model
but can execute Python and attach a local raster image to the conversation.
It never creates HTML or SVG.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


WIDTH = 1080
HEIGHT = 1440


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False))


def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        return None


def find_cjk_font():
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    fc_match = shutil.which("fc-match")
    if fc_match:
        try:
            result = subprocess.run(
                [fc_match, "-f", "%{file}", "Noto Sans CJK SC"],
                capture_output=True, text=True, timeout=3, check=False,
            )
            candidate = (result.stdout or "").strip()
            if candidate and os.path.isfile(candidate):
                return candidate
        except (OSError, subprocess.TimeoutExpired):
            pass
    return None


def capability():
    pillow = load_pillow()
    font_path = find_cjk_font()
    if not pillow:
        return {"ok": False, "error": "pillow_missing", "install_package": "Pillow"}
    if not font_path:
        return {"ok": False, "error": "cjk_font_missing"}
    return {"ok": True, "format": "PNG", "font": font_path,
            "width": WIDTH, "height": HEIGHT}


def color_lerp(start, end, ratio):
    return tuple(round(start[i] + (end[i] - start[i]) * ratio) for i in range(3))


def wrap_text(draw, text, font, max_width, max_lines):
    text = " ".join((text or "").replace("\r", "").split())
    if not text:
        return []
    lines = []
    line = ""
    for char in text:
        candidate = line + char
        if draw.textlength(candidate, font=font) <= max_width:
            line = candidate
            continue
        if line:
            lines.append(line.rstrip())
        line = char.lstrip()
        if len(lines) == max_lines:
            break
    if line and len(lines) < max_lines:
        lines.append(line.rstrip())
    consumed = "".join(lines)
    if len(consumed) < len(text) and lines:
        while lines[-1] and draw.textlength(lines[-1] + "…", font=font) > max_width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"
    return lines


def draw_centered_lines(draw, lines, font, fill, center_x, top, spacing):
    y = top
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        width = box[2] - box[0]
        draw.text((center_x - width / 2, y), line, font=font, fill=fill)
        y += spacing
    return y


def render(args):
    cap = capability()
    if not cap["ok"]:
        emit(cap)
        return 1
    Image, ImageDraw, ImageFont = load_pillow()
    font_path = cap["font"]
    image = Image.new("RGB", (WIDTH, HEIGHT), "#071a40")
    draw = ImageDraw.Draw(image, "RGBA")

    top_color = (7, 27, 68)
    bottom_color = (19, 116, 220)
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        draw.line((0, y, WIDTH, y), fill=color_lerp(top_color, bottom_color, ratio) + (255,))

    # Cloud/server atmosphere without any external visual assets.
    for x, y, radius, alpha in [
        (930, 130, 210, 28), (85, 390, 145, 22), (890, 1120, 250, 20),
        (175, 1325, 210, 18),
    ]:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius),
                     fill=(255, 255, 255, alpha))
    for x, y, width in [(92, 215, 170), (808, 345, 178), (110, 1155, 160)]:
        draw.rounded_rectangle((x, y, x + width, y + 52), radius=18,
                               outline=(124, 211, 255, 90), width=3)
        draw.ellipse((x + 18, y + 20, x + 28, y + 30), fill=(255, 173, 73, 220))
        draw.line((x + 44, y + 26, x + width - 20, y + 26),
                  fill=(173, 228, 255, 100), width=3)

    regular = lambda size: ImageFont.truetype(font_path, size)
    title_font = regular(58)
    big_font = regular(250)
    label_font = regular(34)
    blessing_font = regular(52)
    story_font = regular(31)
    footer_font = regular(27)

    draw.text((70, 72), "LIGHTHOUSE · 6TH ANNIVERSARY",
              font=regular(25), fill=(201, 237, 255, 225))
    draw.text((810, 30), "6", font=big_font, fill=(255, 255, 255, 24))
    draw.text((70, 132), args.title or "轻量 6 周年 · 云上祝福",
              font=title_font, fill=(255, 255, 255, 255))
    draw.rounded_rectangle((70, 225, 350, 281), radius=28,
                           fill=(255, 165, 70, 235))
    label = "AI 祝福海报"
    label_box = draw.textbbox((0, 0), label, font=label_font)
    draw.text((210 - (label_box[2] - label_box[0]) / 2, 233), label,
              font=label_font, fill=(255, 255, 255, 255))

    card = (70, 360, 1010, 1120)
    draw.rounded_rectangle((82, 376, 1022, 1136), radius=42,
                           fill=(2, 14, 44, 42))
    draw.rounded_rectangle(card, radius=42, fill=(255, 255, 255, 242),
                           outline=(218, 239, 255, 245), width=3)
    draw.ellipse((112, 414, 168, 470), fill=(25, 118, 231, 255))
    draw.ellipse((131, 428, 179, 470), fill=(81, 190, 255, 255))
    draw.line((196, 443, 893, 443), fill=(213, 228, 245, 255), width=3)

    blessing = (args.blessing or "愿每一次部署都顺利上线，每一盏云端灯塔都长明。").strip()
    blessing_lines = wrap_text(draw, blessing, blessing_font, 760, 7)
    content_height = max(1, len(blessing_lines)) * 84
    content_top = 500 + max(0, (430 - content_height) // 2)
    draw_centered_lines(draw, blessing_lines, blessing_font,
                        (20, 50, 92, 255), WIDTH / 2, content_top, 84)

    if args.story:
        story_lines = wrap_text(draw, "我的故事：" + args.story, story_font, 760, 3)
        story_top = 970 - len(story_lines) * 44
        draw.rounded_rectangle((130, story_top - 18, 950, 1038), radius=20,
                               fill=(237, 247, 255, 255))
        draw_centered_lines(draw, story_lines, story_font,
                            (68, 103, 145, 255), WIDTH / 2, story_top, 44)

    draw.text((70, 1205), "Lighthouse 6 周年，感谢一路同行。",
              font=regular(34), fill=(255, 255, 255, 245))
    draw.line((70, 1273, 1010, 1273), fill=(181, 227, 255, 100), width=2)
    footer = args.signature or "腾讯云轻量应用服务器 · 6 周年"
    draw.text((70, 1315), footer, font=footer_font,
              fill=(207, 239, 255, 225))

    out = Path(args.out).expanduser().resolve()
    if out.suffix.lower() != ".png":
        emit({"ok": False, "error": "output_must_be_png"})
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(out), format="PNG", optimize=True)
    emit({"ok": True, "path": str(out), "filePath": str(out),
          "mediaUrl": str(out), "mime_type": "image/png",
          "width": WIDTH, "height": HEIGHT, "bytes": out.stat().st_size})
    return 0


def main():
    parser = argparse.ArgumentParser(description="LH6 AI 祝福海报 PNG 渲染器")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--title", default="轻量 6 周年 · 云上祝福")
    parser.add_argument("--story", default="")
    parser.add_argument("--blessing", default="")
    parser.add_argument("--signature", default="")
    parser.add_argument("--out", default="lh6_blessing_poster.png")
    args = parser.parse_args()
    if args.check:
        emit(capability())
        return 0 if capability()["ok"] else 1
    return render(args)


if __name__ == "__main__":
    sys.exit(main())
