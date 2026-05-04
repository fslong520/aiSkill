#!/usr/bin/env python3
"""像素绘 - 环境自检脚本"""

import subprocess, sys, os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SKILL_DIR, 'assets')

checks = []

def check(ok, msg, fix=""):
    checks.append((ok, msg, fix))
    print(f"{'✓' if ok else '✗'} {msg}")
    if not ok and fix:
        print(f"   修复: {fix}")

print("=" * 50)
print("  像素绘 - 环境检查")
print("=" * 50)

# Python
check(sys.version_info >= (3, 8), f"Python ≥ 3.8: {sys.version}")

# Packages
for pkg, name in [('gi', 'PyGObject'), ('cairo', 'pycairo'),
                   ('numpy', 'NumPy'), ('PIL', 'Pillow')]:
    try:
        __import__(pkg)
        check(True, f"{name}: OK")
    except ImportError:
        check(False, f"{name}: 未安装", f"pip install {name.lower()}")

# PangoCairo
try:
    import gi
    gi.require_version('Pango', '1.0')
    gi.require_version('PangoCairo', '1.0')
    from gi.repository import Pango, PangoCairo
    check(True, "PangoCairo: OK")
except Exception as e:
    check(False, f"PangoCairo: {e}", "sudo apt install python3-gi python3-gi-cairo libpango1.0-dev")

# Fonts
font_list = subprocess.run(['fc-list'], capture_output=True, text=True).stdout
check('Noto Color Emoji' in font_list, "Noto Color Emoji 系统字体",
      "sudo apt install fonts-noto-color-emoji")
check('DejaVu Sans' in font_list or 'DejaVuSans' in font_list, "DejaVu Sans 系统字体",
      "sudo apt install fonts-dejavu-core")

# Bundled fonts
for f in ['NotoColorEmoji.ttf', 'DejaVuSans.ttf', 'GB_ST_GB18030.ttf']:
    fp = os.path.join(ASSETS, f)
    check(os.path.exists(fp), f"资产文件: {f}", f"缺少 {fp}，请从系统字体目录复制")

# Pillow + fonts
try:
    from PIL import ImageFont
    fp = os.path.join(ASSETS, 'GB_ST_GB18030.ttf')
    ImageFont.truetype(fp, 16)
    check(True, "PIL 中文渲染: OK")
except Exception as e:
    check(False, f"PIL 中文渲染: {e}")

# PangoCairo emoji rendering test
try:
    import cairo, numpy as np
    from gi.repository import Pango, PangoCairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 60, 30)
    ctx = cairo.Context(surface)
    layout = PangoCairo.create_layout(ctx)
    layout.set_text("☀️🌲🍓", -1)
    fd = Pango.font_description_from_string('Noto Color Emoji 28')
    layout.set_font_description(fd)
    PangoCairo.update_layout(ctx, layout)
    PangoCairo.show_layout(ctx, layout)
    buf = surface.get_data()
    arr = np.frombuffer(buf, np.uint8).reshape(30, 60, 4)
    visible = np.sum(arr[:,:,3] > 50)
    check(visible > 100, f"Emoji 渲染测试: {visible}px 可见 (需 >100)")
except Exception as e:
    check(False, f"Emoji 渲染测试: {e}")

print("=" * 50)
oks = sum(1 for c in checks if c[0])
print(f"  {oks}/{len(checks)} 项通过")
if oks < len(checks):
    print()
    for ok, msg, fix in checks:
        if not ok and fix:
            print(f"  ● {fix}")
print("=" * 50)
