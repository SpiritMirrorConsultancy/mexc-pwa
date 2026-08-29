#!/usr/bin/env python3
"""Generate the PWA home-screen icons (icon-192.png and icon-512.png).

Pure-Python (Pillow). Run from the folder where you want the PNGs:

    python make_icons.py

Creates a dark rounded-square icon with a MEXC-blue "%" mark (risk/calculator
theme) at 192x192 and 512x512. iOS home-screen icons should be 180x180 or
192x192 PNG; the manifest uses 192 and 512.

Requires Pillow:  pip install Pillow
"""
import os

from PIL import Image, ImageDraw

ACCENT = (27, 118, 255, 255)     # MEXC blue #1B76FF
BG = (15, 15, 26, 255)           # dark navy #0f0f1a


def make_icon(size, path):
    S = size
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background: rounded square (iOS masks the corners anyway, but keep them soft)
    radius = int(S * 0.18)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=radius, fill=BG)

    # MEXC-blue "%" mark
    w = max(3, int(S * 0.052))                    # line / dot thickness
    r = int(S * 0.095)                            # dot radius

    # slash (thick diagonal)
    d.line(
        [(S * 0.27, S * 0.31), (S * 0.73, S * 0.69)],
        fill=ACCENT, width=w,
    )

    # top-right dot
    d.ellipse(
        [S * 0.70 - r, S * 0.28 - r, S * 0.70 + r, S * 0.28 + r],
        fill=ACCENT,
    )
    # bottom-left dot
    d.ellipse(
        [S * 0.30 - r, S * 0.72 - r, S * 0.30 + r, S * 0.72 + r],
        fill=ACCENT,
    )

    img.save(path, "PNG")
    print(f"wrote {path} ({size}x{size})")


def main():
    # Render at 512 and downscale to 192 for crisp small-size rendering.
    big = os.path.abspath("icon-512.png")
    make_icon(512, big)
    img = Image.open(big).resize((192, 192), Image.LANCZOS)
    img.save(os.path.abspath("icon-192.png"), "PNG")
    print("wrote icon-192.png (192x192)")


if __name__ == "__main__":
    main()
