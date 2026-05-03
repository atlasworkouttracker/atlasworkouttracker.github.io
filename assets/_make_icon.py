#!/usr/bin/env python3
"""Generate the Atlas Workout Tracker app icon at multiple sizes.

Master is rendered at 1024x1024 then downsampled with LANCZOS for crisp
small-size variants. Output: icon-1024.png, icon-512.png, icon-128.png,
icon-96.png, icon-32.png in this directory.

Design: rounded blue square (#2563eb) with a centered barbell silhouette
in white. Reads cleanly down to 32x32.
"""
from PIL import Image, ImageDraw
from pathlib import Path

OUT_DIR = Path(__file__).parent
MASTER_SIZE = 1024
SIZES = [1024, 512, 128, 96, 32]
BG = (37, 99, 235, 255)        # #2563eb (matches addon accent)
FG = (255, 255, 255, 255)      # white

def render(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded square background.
    draw.rounded_rectangle((0, 0, size, size), radius=size // 8, fill=BG)

    cy = size // 2
    # Bar: thin horizontal bar across the middle.
    bar_thick = round(size * 0.052)
    bar_inset = round(size * 0.18)
    draw.rounded_rectangle(
        (bar_inset, cy - bar_thick // 2,
         size - bar_inset, cy + bar_thick // 2),
        radius=bar_thick // 2,
        fill=FG,
    )

    # Outer plates (large) — rounded vertical rects.
    plate_w_outer = round(size * 0.075)
    plate_h_outer = round(size * 0.5)
    edge_margin = round(size * 0.13)
    # Left outer plate
    draw.rounded_rectangle(
        (edge_margin, cy - plate_h_outer // 2,
         edge_margin + plate_w_outer, cy + plate_h_outer // 2),
        radius=round(size * 0.018),
        fill=FG,
    )
    # Right outer plate
    draw.rounded_rectangle(
        (size - edge_margin - plate_w_outer, cy - plate_h_outer // 2,
         size - edge_margin, cy + plate_h_outer // 2),
        radius=round(size * 0.018),
        fill=FG,
    )

    # Inner plates (smaller) — sits next to outer plates.
    plate_w_inner = round(size * 0.052)
    plate_h_inner = round(size * 0.34)
    inner_gap = round(size * 0.025)
    inner_left_x = edge_margin + plate_w_outer + inner_gap
    inner_right_x = size - edge_margin - plate_w_outer - inner_gap - plate_w_inner
    draw.rounded_rectangle(
        (inner_left_x, cy - plate_h_inner // 2,
         inner_left_x + plate_w_inner, cy + plate_h_inner // 2),
        radius=round(size * 0.014),
        fill=FG,
    )
    draw.rounded_rectangle(
        (inner_right_x, cy - plate_h_inner // 2,
         inner_right_x + plate_w_inner, cy + plate_h_inner // 2),
        radius=round(size * 0.014),
        fill=FG,
    )

    return img


def main():
    master = render(MASTER_SIZE)
    for s in SIZES:
        if s == MASTER_SIZE:
            out = master
        else:
            # Render fresh at MASTER then downscale with LANCZOS for crispness.
            out = master.resize((s, s), Image.LANCZOS)
        out.save(OUT_DIR / f"icon-{s}.png", optimize=True)
        print(f"wrote icon-{s}.png ({out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    main()
