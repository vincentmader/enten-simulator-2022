#!/usr/bin/env python3
"""
Generates two sets of water-effect animation frames:

  ripple_N.png  — concentric expanding ellipses (entry / exit)
  wake_N.png    — single fast ellipse ring (V-wake while moving)

All images are RGBA with a transparent background.
Ellipses are foreshortened (2.5:1 width:height) to fake top-down perspective.
"""

import os
import numpy as np
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../resources/sprites/splashes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WATER_COLOR = (190, 225, 245)   # light blue-white, matches pond palette

# ── helpers ───────────────────────────────────────────────────────────────────

def draw_ellipse_ring(draw, cx, cy, rx, alpha, width):
    ry = max(1, int(rx / 2.5))
    c  = (*WATER_COLOR, max(0, min(255, alpha)))
    w  = max(1, width)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=c, width=w)


# ── ripple frames (entry / exit) ──────────────────────────────────────────────
#
# Two concentric rings with a phase offset of 0.3.
# Both expand to the same max radius and fade to transparent.

N_RIPPLE  = 10
RW, RH    = 160, 80
RCX, RCY  = RW // 2, RH // 2
MAX_RX    = 72

for i in range(N_RIPPLE):
    t   = i / (N_RIPPLE - 1)
    img = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)

    for t_start, base_alpha in [(0.0, 230), (0.3, 200)]:
        if t < t_start:
            continue
        p     = (t - t_start) / (1.0 - t_start)   # 0→1 for this ring
        rx    = int(4 + MAX_RX * p)
        alpha = int(base_alpha * (1 - p) ** 1.1)
        width = max(1, int(2.5 * (1 - p * 0.65)))
        draw_ellipse_ring(d, RCX, RCY, rx, alpha, width)

    img.save(os.path.join(OUTPUT_DIR, f"ripple_{i}.png"))

print(f"Wrote {N_RIPPLE} ripple frames")


# ── wake frames (movement) ────────────────────────────────────────────────────
#
# Single thin ring — fast expand, fast fade.
# Spawned in pairs to the sides of the duck's trail; the V-wake emerges
# naturally from the duck's movement leaving old rings behind.

N_WAKE  = 8
WW, WH  = 80, 40
WCX, WCY = WW // 2, WH // 2
MAX_WX  = 36

for i in range(N_WAKE):
    t   = i / (N_WAKE - 1)
    img = Image.new("RGBA", (WW, WH), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)

    rx    = int(3 + MAX_WX * t)
    alpha = int(210 * (1 - t) ** 0.75)
    width = max(1, int(2 * (1 - t * 0.5)))
    draw_ellipse_ring(d, WCX, WCY, rx, alpha, width)

    img.save(os.path.join(OUTPUT_DIR, f"wake_{i}.png"))

print(f"Wrote {N_WAKE} wake frames")
print(f"All frames in: {OUTPUT_DIR}")
