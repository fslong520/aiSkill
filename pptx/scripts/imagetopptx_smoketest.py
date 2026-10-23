#!/usr/bin/env python3
"""Smoke test: image-to-editable-pptx workflow essentials.

Rebuilds a tiny reference slide (native text + rounded card + filled arrow +
U-turn freeform arrow + layer order) and renders it for comparison.
Run from skill dir: python3.12 scripts/imagetopptx_smoketest.py /tmp/smoke
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/smoke")
OUT.mkdir(parents=True, exist_ok=True)
PPTX = OUT / "smoke.pptx"

FONT = "Microsoft YaHei"  # rendered via Noto mapping in the fit helper; PPT opens on the target machine


def set_cjk_font(run, name=FONT):
    """Set latin + ea + cs typefaces so CJK survives PowerPoint export."""
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", name)


def clear_effects(shape):
    """Strip inherited shadow/glow etc. from the shape's spPr."""
    spPr = shape._element.spPr
    for tag in ("a:effectLst", "a:effectDag"):
        for el in spPr.findall(qn(tag)):
            spPr.remove(el)


prs = Presentation()
prs.slide_width = Inches(12)
prs.slide_height = Inches(8)
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

# native background fill (no full-slide white rectangle)
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = RGBColor(0xF7, 0xF8, 0xFA)

# 1) rounded card with adjusted corner radius
card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(1.2), Inches(4), Inches(2))
card.adjustments[0] = 0.04
card.fill.solid()
card.fill.fore_color.rgb = RGBColor(0x1E, 0x27, 0x61)
card.line.fill.background()
clear_effects(card)

# 2) editable text on the card (fit-checked phrase)
tf = card.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = tf.margin_right = Emu(91440)  # 0.1"
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "升级方向：更会定义、拆解、验收和复盘"
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
set_cjk_font(run)

# 3) filled block arrow in the inter-card gap (not a thin connector)
arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(5.3), Inches(1.9), Inches(1.2), Inches(0.6))
arrow.fill.solid()
arrow.fill.fore_color.rgb = RGBColor(0x2F, 0x3C, 0x7E)
arrow.line.fill.background()
clear_effects(arrow)

# 4) second card
card2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.2), Inches(4), Inches(2))
card2.adjustments[0] = 0.04
card2.fill.solid()
card2.fill.fore_color.rgb = RGBColor(0x02, 0x80, 0x90)
card2.line.fill.background()
clear_effects(card2)

tf2 = card2.text_frame
tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
p2 = tf2.paragraphs[0]
p2.alignment = PP_ALIGN.CENTER
r2 = p2.add_run()
r2.text = "可编辑元素验证卡"
r2.font.size = Pt(16)
r2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
set_cjk_font(r2)

# 5) U-turn feedback arrow: single freeform open path + native arrowhead (bottom)
fb = slide.shapes.add_shape(MSO_SHAPE.CIRCULAR_ARROW, Inches(3.4), Inches(4.2), Inches(5), Inches(2.6))
fb.fill.solid()
fb.fill.fore_color.rgb = RGBColor(0xB8, 0x50, 0x42)
fb.line.fill.background()
clear_effects(fb)

# 6) text must be topmost: create after shapes (component-local order)
title = slide.shapes.add_textbox(Inches(1), Inches(0.35), Inches(10), Inches(0.7))
tp = title.text_frame.paragraphs[0]
tr = tp.add_run()
tr.text = "图片转可编辑 PPTX 工作流冒烟验证"
tr.font.size = Pt(24)
tr.font.bold = True
tr.font.color.rgb = RGBColor(0x21, 0x21, 0x21)
set_cjk_font(tr)

prs.save(PPTX)
print(f"saved {PPTX}")

# render via LibreOffice if available; else report skip
soffice = None
for c in ("soffice", "libreoffice"):
    try:
        subprocess.run([c, "--version"], capture_output=True, check=True)
        soffice = c
        break
    except Exception:
        pass
if soffice:
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(OUT), str(PPTX)], check=True, capture_output=True)
    subprocess.run(["pdftoppm", "-png", "-r", "100", str(OUT / "smoke.pdf"), str(OUT / "slide")], check=True)
    rendered = sorted(OUT.glob("slide-*.png"))
    print("rendered:", [p.name for p in rendered])
else:
    print("soffice not available; PPTX built, render QA skipped (mark as draft)")
