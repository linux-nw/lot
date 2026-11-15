#!/usr/bin/env python3
"""Erzeugt alle Android-Icons fuer Lot: Kerbstab (cremefarbener Stab, Kerben, gruene Kerbe) auf Schwarz."""
import os, sys
from PIL import Image, ImageDraw

RES = sys.argv[1] if len(sys.argv) > 1 else 'android/app/src/main/res'
BG, CREAM, GREEN = (31, 28, 23, 255), (244, 238, 223, 255), (135, 200, 150, 255)
SS = 4  # Supersampling

# Geometrie im 140er-Raster (Stab 34 breit, 112 hoch)
STICK = (53, 14, 87, 126)
CUTS = [  # (Polygon, gruen?)
    ([(87, 26), (75, 32), (87, 38)], False), ([(87, 46), (75, 52), (87, 58)], False),
    ([(87, 66), (75, 72), (87, 78)], False), ([(53, 36), (65, 42), (53, 48)], False),
    ([(53, 56), (65, 62), (53, 68)], False), ([(53, 76), (65, 82), (53, 88)], False),
]
GREEN_TRI = [(87, 90), (65, 100), (87, 110)]

def stick(size, scale, cx=None, cy=None, bg=None):
    """Zeichnet den Kerbstab; Kerben sind echte Ausschnitte (transparent bzw. Hintergrund)."""
    S = size * SS
    cx = S / 2 if cx is None else cx; cy = S / 2 if cy is None else cy
    k = S / 140.0 * scale
    def P(pt): return (cx + (pt[0] - 70) * k, cy + (pt[1] - 70) * k)
    mask = Image.new('L', (S, S), 0); d = ImageDraw.Draw(mask)
    x0, y0, x1, y1 = STICK
    d.rounded_rectangle([*P((x0, y0)), *P((x1, y1))], radius=8 * k, fill=255)
    for poly, _ in CUTS: d.polygon([P(p) for p in poly], fill=0)
    layer = Image.new('RGBA', (S, S), (0, 0, 0, 0)); layer.paste(CREAM, mask=mask)
    g = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(g).polygon([P(p) for p in GREEN_TRI], fill=GREEN)
    layer.alpha_composite(g)
    return layer

def finish(img, size): return img.resize((size, size), Image.LANCZOS)

dens = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}
for n, m in dens.items():
    d = os.path.join(RES, 'mipmap-' + n)
    os.makedirs(d, exist_ok=True)
    fg = int(108 * m)  # Adaptiv: Stab innerhalb der Sicherheitszone (66 dp)
    finish(stick(fg, 0.56), fg).save(os.path.join(d, 'ic_launcher_foreground.png'))
    L = int(48 * m)
    S = L * SS
    base = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(base).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.22, fill=BG)
    base.alpha_composite(stick(L, 0.78)); finish(base, L).save(os.path.join(d, 'ic_launcher.png'))
    rb = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ImageDraw.Draw(rb).ellipse([0, 0, S - 1, S - 1], fill=BG)
    rb.alpha_composite(stick(L, 0.74)); finish(rb, L).save(os.path.join(d, 'ic_launcher_round.png'))

with open(os.path.join(RES, 'values', 'ic_launcher_background.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#1F1C17</color>\n</resources>\n')
# Vorschau (512 px) fuer README
prev = Image.new('RGBA', (2048, 2048), (0, 0, 0, 0))
ImageDraw.Draw(prev).rounded_rectangle([0, 0, 2047, 2047], radius=450, fill=BG)
prev.alpha_composite(stick(512, 0.9).resize((2048, 2048), Image.LANCZOS))
os.makedirs('assets', exist_ok=True); prev.resize((512, 512), Image.LANCZOS).save('assets/icon.png')
print('Icons ok')
