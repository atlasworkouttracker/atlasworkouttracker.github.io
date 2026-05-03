#!/usr/bin/env python3
"""Generate the Atlas Workout Tracker Marketplace card banner.

Output: banner-220x140.png — the small store-tile banner Google Workspace
Marketplace shows in browse/search previews. Layout: barbell icon on left,
product name on right.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path(__file__).parent
W, H = 220, 140
BG = (37, 99, 235, 255)        # #2563eb (matches addon accent + icon)
FG = (255, 255, 255, 255)      # white
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def draw_barbell(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float):
    """Draw a centered barbell at (cx, cy). `scale` is the icon's effective
    width (the bar length). Mirrors the proportions in _make_icon.py."""
    bar_thick = max(2, round(scale * 0.10))
    plate_w_outer = max(2, round(scale * 0.14))
    plate_h_outer = round(scale * 0.92)
    plate_w_inner = max(2, round(scale * 0.10))
    plate_h_inner = round(scale * 0.62)

    bar_left = cx - scale // 2
    bar_right = cx + scale // 2

    # Bar
    draw.rounded_rectangle(
        (bar_left, cy - bar_thick // 2, bar_right, cy + bar_thick // 2),
        radius=bar_thick // 2, fill=FG,
    )
    # Outer plates
    draw.rounded_rectangle(
        (bar_left, cy - plate_h_outer // 2,
         bar_left + plate_w_outer, cy + plate_h_outer // 2),
        radius=2, fill=FG,
    )
    draw.rounded_rectangle(
        (bar_right - plate_w_outer, cy - plate_h_outer // 2,
         bar_right, cy + plate_h_outer // 2),
        radius=2, fill=FG,
    )
    # Inner plates
    inner_gap = max(2, round(scale * 0.045))
    draw.rounded_rectangle(
        (bar_left + plate_w_outer + inner_gap,
         cy - plate_h_inner // 2,
         bar_left + plate_w_outer + inner_gap + plate_w_inner,
         cy + plate_h_inner // 2),
        radius=2, fill=FG,
    )
    draw.rounded_rectangle(
        (bar_right - plate_w_outer - inner_gap - plate_w_inner,
         cy - plate_h_inner // 2,
         bar_right - plate_w_outer - inner_gap,
         cy + plate_h_inner // 2),
        radius=2, fill=FG,
    )


def main():
    # Render at 4x then downscale for smoother edges.
    SCALE_FACTOR = 4
    big_w, big_h = W * SCALE_FACTOR, H * SCALE_FACTOR

    img = Image.new("RGBA", (big_w, big_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded background
    draw.rounded_rectangle(
        (0, 0, big_w, big_h), radius=12 * SCALE_FACTOR, fill=BG,
    )

    # Barbell on left
    barbell_cx = round(big_w * 0.20)
    barbell_cy = big_h // 2
    barbell_scale = round(big_h * 0.55)
    draw_barbell(draw, barbell_cx, barbell_cy, barbell_scale)

    # Text on right: "ATLAS" / "WORKOUT" / "TRACKER" stacked
    title_size = round(big_h * 0.18)
    sub_size = round(big_h * 0.14)
    font_title = ImageFont.truetype(FONT_BOLD, title_size)
    font_sub = ImageFont.truetype(FONT_BOLD, sub_size)

    text_x = round(big_w * 0.40)
    text_cy = big_h // 2

    # Three lines: ATLAS / WORKOUT / TRACKER
    line_gap = round(big_h * 0.025)
    lines = [
        ("ATLAS", font_title),
        ("WORKOUT", font_sub),
        ("TRACKER", font_sub),
    ]
    # Compute total height
    heights = []
    for text, font in lines:
        bbox = font.getbbox(text)
        heights.append(bbox[3] - bbox[1])
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    y = text_cy - total_h // 2

    for (text, font), h in zip(lines, heights):
        draw.text((text_x, y - font.getbbox(text)[1]), text, font=font, fill=FG)
        y += h + line_gap

    # Downscale
    final = img.resize((W, H), Image.LANCZOS)
    out = OUT_DIR / "banner-220x140.png"
    final.save(out, optimize=True)
    print(f"wrote {out.name} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
