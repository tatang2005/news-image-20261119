#!/usr/bin/env python3
"""Draw the entry image for make.fun competition news-image-20261119.

A one-page newspaper front page summing up the world news of
Thursday 19 November 2026, drawn entirely with PIL shapes and type.
Output: entry.png (1024x1024) next to this script.

Layout, palette and type are the same family as the 18 November entry:
dated masthead, six labelled panels in a 3x2 grid, footer ticker strip.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)      # #f7f3ea
INK = (26, 26, 26)           # #1a1a1a
RED = (179, 32, 42)          # #b3202a
FAINT = (120, 112, 96)       # muted warm grey for hairlines / waves
GOLD = (176, 141, 46)        # sparing third tone for one icon

W = H = 1024
MARGIN = 40
CONTENT_W = W - 2 * MARGIN

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "liberation", "LiberationSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start_size, max_width, min_size=14):
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, min_size)


def wrap(draw, text, fnt, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def spaced(draw, cx, y, text, fnt, fill=INK, tracking=6):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


# ------------------------------------------------------------------- icons
def icon_summit(d, box):
    """Three overlapping circles: three leaders at one table."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 30
    d.ellipse([cx - r - 26, cy - r + 6, cx + r - 26, cy + r + 6],
              outline=INK, width=5)
    d.ellipse([cx - r + 26, cy - r + 6, cx + r + 26, cy + r + 6],
              outline=RED, width=5)
    d.ellipse([cx - r, cy - r - 12, cx + r, cy + r - 12],
              outline=GOLD, width=5)


def _sag(d, xa, ya, xb, yb, sag, fill, width=4):
    pts = []
    for i in range(25):
        f = i / 24
        px = xa + (xb - xa) * f
        py = ya + (yb - ya) * f + sag * 4 * f * (1 - f)
        pts.append((px, py))
    d.line(pts, fill=fill, width=width)


def icon_bridge(d, box):
    """A suspension bridge over water, one span broken (the strike)."""
    x0, y0, x1, y1 = box
    deck_y = y1 - 32
    mid = (x0 + x1) // 2
    top_y = y0 + 10
    for tx in (x0 + 28, x1 - 28):
        d.line([(tx, top_y), (tx, deck_y)], fill=INK, width=5)
    _sag(d, x0 + 4, deck_y - 6, x0 + 28, top_y, 4, INK)
    _sag(d, x0 + 28, top_y, x1 - 28, top_y, 26, INK)
    _sag(d, x1 - 28, top_y, x1 - 4, deck_y - 6, 4, INK)
    for f in (0.18, 0.34, 0.5, 0.66, 0.82):
        hx = (x0 + 28) + (x1 - 28 - x0 - 28) * f
        hy = top_y + 26 * 4 * f * (1 - f)
        d.line([(hx, hy), (hx, deck_y)], fill=FAINT, width=3)
    d.line([(x0 + 4, deck_y), (mid - 15, deck_y)], fill=INK, width=6)
    d.line([(mid + 15, deck_y), (x1 - 4, deck_y)], fill=INK, width=6)
    d.line([(mid - 13, deck_y + 3), (mid + 9, deck_y + 17)], fill=RED, width=6)
    for wx in range(x0 + 8, x1 - 26, 36):
        d.arc([wx, deck_y + 10, wx + 24, deck_y + 24], 180, 360,
              fill=FAINT, width=3)


def icon_gaza(d, box):
    """A tank silhouette over a dashed ceasefire line."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    # dashed ceasefire line
    for dx in range(x0 + 4, x1 - 18, 26):
        d.line([(dx, y1 - 14), (dx + 14, y1 - 14)], fill=RED, width=4)
    # tracks
    d.rounded_rectangle([cx - 52, y1 - 38, cx + 52, y1 - 20],
                        radius=9, outline=INK, width=5)
    for wx in (-36, -12, 12, 36):
        d.ellipse([cx + wx - 7, y1 - 36, cx + wx + 7, y1 - 22],
                  outline=INK, width=3)
    # hull + turret + barrel
    d.polygon([(cx - 44, y1 - 38), (cx + 44, y1 - 38),
               (cx + 30, y1 - 52), (cx - 30, y1 - 52)], fill=INK)
    d.rectangle([cx - 20, y1 - 66, cx + 16, y1 - 52], fill=INK)
    d.line([(cx + 16, y1 - 60), (cx + 54, y1 - 60)], fill=INK, width=6)


def icon_climate(d, box):
    """A leaf inside a circle: the planet and the talks."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=5)
    ax, ay = cx - 19, cy + 19
    bx, by = cx + 19, cy - 19
    dx, dy = bx - ax, by - ay
    px, py = -dy, dx
    norm = math.hypot(px, py)
    px, py = px / norm, py / norm
    side_a, side_b = [], []
    for i in range(21):
        f = i / 20
        off = math.sin(f * math.pi) * 13
        side_a.append((ax + dx * f + px * off, ay + dy * f + py * off))
        side_b.append((ax + dx * f - px * off, ay + dy * f - py * off))
    d.line(side_a, fill=RED, width=4)
    d.line(side_b, fill=RED, width=4)
    d.line([(ax, ay), (bx, by)], fill=RED, width=3)


def icon_ipo(d, box):
    """A rising chart arrow breaking through a ceiling line."""
    x0, y0, x1, y1 = box
    # axes
    d.line([(x0 + 10, y0 + 8), (x0 + 10, y1 - 12)], fill=INK, width=4)
    d.line([(x0 + 10, y1 - 12), (x1 - 6, y1 - 12)], fill=INK, width=4)
    # bars
    for i, hgt in enumerate((18, 28, 40)):
        bx = x0 + 26 + i * 26
        d.rectangle([bx, y1 - 12 - hgt, bx + 16, y1 - 12], fill=FAINT)
    # rising line + arrowhead
    pts = [(x0 + 24, y1 - 28), (x0 + 52, y1 - 44),
           (x0 + 76, y1 - 40), (x1 - 16, y1 - 68)]
    d.line(pts, fill=RED, width=6, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey + 2), (ex - 4, ey + 14)], fill=RED)


def icon_court(d, box):
    """Scales of justice: beam, two pans, central pillar."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    top = y0 + 12
    d.line([(cx - 46, top), (cx + 46, top)], fill=INK, width=5)
    d.line([(cx, top - 8), (cx, y1 - 16)], fill=INK, width=5)
    d.ellipse([cx - 6, top - 14, cx + 6, top - 2], fill=RED)
    d.rectangle([cx - 20, y1 - 16, cx + 20, y1 - 10], fill=INK)
    for sx in (cx - 46, cx + 46):
        d.line([(sx, top), (sx - 14, y1 - 34)], fill=INK, width=3)
        d.line([(sx, top), (sx + 14, y1 - 34)], fill=INK, width=3)
        d.arc([sx - 18, y1 - 40, sx + 18, y1 - 20], 0, 180, fill=INK, width=4)


# ------------------------------------------------------------------ stories
STORIES = [
    ("SHENZHEN TRILATERAL", icon_summit,
     "Trump, Xi and Putin meet for first-ever three-way APEC "
     "summit; peace declaration, no breakthrough."),
    ("UKRAINE HITS BRIDGE AGAIN", icon_bridge,
     "Ukraine strikes the Crimean Bridge a third time this week; "
     "rail traffic halted."),
    ("GAZA RAID AMID CEASEFIRE", icon_gaza,
     "Israeli tanks enter central Gaza; US Senate rejects Iran "
     "war-powers limit 51-48."),
    ("COP31 DROPS FOSSIL FUELS", icon_climate,
     "Antalya draft strips out fossil-fuel phase-out and $120B "
     "adaptation fund before Friday deadline."),
    ("ANTHROPIC RECORD IPO", icon_ipo,
     "Claude maker raises $81.3B in largest IPO ever, passing "
     "SpaceX; shares jump on Nasdaq debut."),
    ("MYANMAR GENOCIDE RULING", icon_court,
     "World Court finds Myanmar committed genocide against the "
     "Rohingya - a first for a state."),
]

FOOTER_LINES = [
    "Denmark approves Greenland Arctic deal with US, 109-0",
    "Bangladesh: four killed, Yunus ancestral home torched",
    "IAEA: North Korea expands uranium enrichment at Yongbyon",
]


# -------------------------------------------------------------------- draw
def draw_panel(d, x, y, w, headline, icon_fn, sub):
    icon_fn(d, (x + w // 2 - 55, y + 0, x + w // 2 + 55, y + 80))
    size = 38
    while size > 22:
        head_font = font(SERIF_BOLD, size)
        head_lines = wrap(d, headline, head_font, w - 16)
        if len(head_lines) <= 2:
            break
        size -= 2
    hy = y + 88
    for line in head_lines:
        centered(d, x + w // 2, hy, line, head_font, INK)
        hy += head_font.size + 4
    sub_font = font(SANS, 22)
    sub_lines = wrap(d, sub, sub_font, w - 20)
    sy = hy + 4
    for line in sub_lines:
        centered(d, x + w // 2, sy, line, sub_font, INK)
        sy += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cx = W // 2

    # ---- masthead
    d.line([(MARGIN, 34), (W - MARGIN, 34)], fill=INK, width=3)
    spaced(d, cx, 46, "THE WORLD IN ONE DAY", font(SANS_BOLD, 27), INK, 8)
    d.line([(MARGIN, 88), (W - MARGIN, 88)], fill=INK, width=1)

    day_font = fit_font(d, "THURSDAY", SERIF_BOLD, 64, CONTENT_W)
    centered(d, cx, 100, "THURSDAY", day_font, RED)
    date_font = fit_font(d, "19 NOVEMBER 2026", SERIF_BOLD, 118, CONTENT_W)
    centered(d, cx, 168, "19 NOVEMBER 2026", date_font, INK)

    d.line([(MARGIN, 292), (W - MARGIN, 292)], fill=INK, width=5)
    d.line([(MARGIN, 302), (W - MARGIN, 302)], fill=INK, width=1)

    # ---- story grid: 3 columns x 2 rows
    grid_top = 310
    grid_bottom = 892
    gutter = 18
    col_w = (CONTENT_W - 2 * gutter) // 3
    row_h = (grid_bottom - grid_top - gutter) // 2

    for i, (headline, icon_fn, sub) in enumerate(STORIES):
        col, row = i % 3, i // 3
        px = MARGIN + col * (col_w + gutter)
        py = grid_top + row * (row_h + gutter)
        draw_panel(d, px, py, col_w, headline, icon_fn, sub)

    for col in (1, 2):
        sx = MARGIN + col * col_w + (col - 1) * gutter + gutter // 2
        d.line([(sx, grid_top + 4), (sx, grid_bottom - 4)], fill=FAINT, width=1)
    mid_y = grid_top + row_h + gutter // 2
    d.line([(MARGIN, mid_y), (W - MARGIN, mid_y)], fill=FAINT, width=1)

    # ---- footer strip
    d.line([(MARGIN, 906), (W - MARGIN, 906)], fill=RED, width=4)
    foot_font = font(SANS_BOLD, 25)
    fy = 918
    for line in FOOTER_LINES:
        centered(d, cx, fy, line, foot_font, INK)
        fy += 31

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
