#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a newspaper front page summing up
Wednesday 18 November 2026 in six stories. Output: entry.png (1024x1024).

Six stories, each verified from news reports of 18 November 2026:
  1. Ukraine strikes the Crimean (Kerch) Bridge a second day running.
  2. Trump arrives in Manila for the ASEAN / Quad summit.
  3. Iran drones hit a US radar site in Bahrain; the Gulf exchange widens.
  4. Nvidia shares cheer as Jensen Huang is open to returning.
  5. Britain sanctions eight firms over West Bank settlements.
  6. Cyclone Akvan strengthens over the Bay of Bengal.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 58, 46)
PANEL = (255, 253, 246)
GREY = (90, 84, 72)
BLUE = (31, 78, 121)
ORANGE = (232, 126, 32)
GOLD = (232, 190, 40)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(d, cx, y, lines, font, fill, lead=6):
    """Draw lines centred on cx, starting at y; return y after last line."""
    for line in lines:
        w = d.textlength(line, font=font)
        d.text((cx - w / 2, y), line, font=font, fill=fill)
        y += font.size + lead
    return y


# ---------------- pictograms ----------------

def icon_bridge(d, cx, cy):
    # Two towers, deck broken in the middle, fallen span tilted down.
    for tx in (cx - 68, cx + 68):
        d.line([(tx, cy - 58), (tx, cy + 32)], fill=INK, width=7)
        d.line([(tx - 13, cy - 66), (tx + 13, cy - 66)], fill=INK, width=7)
    d.line([(cx - 92, cy + 32), (cx - 16, cy + 32)], fill=INK, width=8)
    d.line([(cx + 16, cy + 32), (cx + 92, cy + 32)], fill=INK, width=8)
    d.line([(cx - 14, cy + 32), (cx + 6, cy + 54)], fill=RED, width=7)
    d.arc([cx - 92, cy - 48, cx + 92, cy + 48], start=180, end=360,
          fill=BLUE, width=6)
    d.line([(cx - 92, cy + 56), (cx + 92, cy + 56)], fill=BLUE, width=5)


def icon_plane(d, cx, cy):
    # Airliner nose-right, with red wings and motion lines.
    d.ellipse([cx - 85, cy - 14, cx + 85, cy + 14], fill=INK)
    d.polygon([(cx + 55, cy - 8), (cx + 96, cy - 38), (cx + 78, cy - 4)],
              fill=INK)
    d.polygon([(cx - 8, cy - 6), (cx + 26, cy - 58), (cx + 46, cy - 58),
               (cx + 30, cy - 4)], fill=RED)
    d.polygon([(cx - 14, cy + 6), (cx + 6, cy + 48), (cx + 22, cy + 48),
               (cx + 18, cy + 6)], fill=RED)
    d.polygon([(cx - 78, cy - 8), (cx - 62, cy - 48), (cx - 48, cy - 48),
               (cx - 55, cy - 8)], fill=INK)
    for i in range(5):
        x = cx - 45 + i * 16
        d.ellipse([x, cy - 6, x + 8, cy + 2], fill=PAPER)
    for i, y in enumerate((cy - 52, cy - 38)):
        d.line([(cx - 96, y), (cx - 56 - i * 8, y)], fill=BLUE, width=4)


def icon_drone(d, cx, cy):
    # Quadcopter: central body, four arms, spinning rotors, camera eye.
    d.ellipse([cx - 26, cy - 20, cx + 26, cy + 20], fill=INK)
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=RED)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ax, ay = cx + sx * 52, cy + sy * 38
        d.line([(cx + sx * 20, cy + sy * 14), (ax, ay)], fill=INK, width=6)
        d.ellipse([ax - 26, ay - 7, ax + 26, ay + 7], fill=BLUE)
        d.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=INK)
    # signal rings below the drone
    d.arc([cx - 42, cy + 46, cx + 42, cy + 78], start=0, end=180,
          fill=GREY, width=4)
    d.arc([cx - 22, cy + 54, cx + 22, cy + 74], start=0, end=180,
          fill=GREY, width=4)


def icon_chip(d, cx, cy):
    # Processor with pins and a red core marked N.
    for i in range(4):
        x = cx - 45 + i * 30
        d.line([(x, cy - 80), (x, cy - 58)], fill=INK, width=6)
        d.line([(x, cy + 58), (x, cy + 80)], fill=INK, width=6)
        y = cy - 45 + i * 30
        d.line([(cx - 80, y), (cx - 58, y)], fill=INK, width=6)
        d.line([(cx + 58, y), (cx + 80, y)], fill=INK, width=6)
    d.rectangle([cx - 58, cy - 58, cx + 58, cy + 58], fill=INK)
    d.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], fill=RED)
    d.text((cx - 9, cy - 13), "N", font=fnt(BOLD, 26), fill=PAPER)
    # rising arrow beside the chip
    d.line([(cx + 88, cy + 60), (cx + 88, cy - 40)], fill=BLUE, width=6)
    d.polygon([(cx + 76, cy - 28), (cx + 88, cy - 52), (cx + 100, cy - 28)],
              fill=BLUE)


def icon_document(d, cx, cy):
    # Sanctions paper: sheet with folded corner, text lines, red seal.
    d.polygon([(cx - 62, cy - 70), (cx + 42, cy - 70), (cx + 62, cy - 50),
               (cx + 62, cy + 70), (cx - 62, cy + 70)], fill=PANEL,
              outline=INK)
    d.polygon([(cx + 42, cy - 70), (cx + 62, cy - 50), (cx + 42, cy - 50)],
              fill=GREY)
    for i, y in enumerate((-42, -22, -2, 18)):
        d.line([(cx - 46, cy + y), (cx + 46 - (16 if i == 3 else 0), cy + y)],
               fill=INK, width=5)
    # red round seal overlapping the lower right
    d.ellipse([cx + 8, cy + 22, cx + 66, cy + 80], outline=RED, width=6)
    d.ellipse([cx + 16, cy + 30, cx + 58, cy + 72], outline=RED, width=3)
    d.line([(cx + 16, cy + 66), (cx + 58, cy + 36)], fill=RED, width=5)


def icon_cyclone(d, cx, cy):
    # Spiral storm over waves, with rain streaks.
    for r, start in ((78, 200), (60, 20), (42, 200), (24, 20)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=start,
              end=start + 300, fill=BLUE, width=7)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    for i, x in enumerate((-78, -44, -10, 24, 58)):
        y = cy + 62 + (i % 2) * 8
        d.line([(cx + x, y), (cx + x - 6, y + 22)], fill=BLUE, width=4)
    d.arc([cx - 92, cy + 52, cx - 32, cy + 78], start=0, end=180,
          fill=BLUE, width=5)
    d.arc([cx + 32, cy + 52, cx + 92, cy + 78], start=0, end=180,
          fill=BLUE, width=5)


# ---------------- stories ----------------

STORIES = [
    ("EUROPE  ·  WAR", icon_bridge,
     "Ukraine hits Crimean Bridge a second day",
     "Russia pounds Kyiv bridges in reply."),
    ("ASIA  ·  DIPLOMACY", icon_plane,
     "Trump in Manila for Quad talks",
     "ASEAN summit opens ahead of China visit."),
    ("MIDDLE EAST  ·  CONFLICT", icon_drone,
     "Iran drones hit US radar in Bahrain",
     "US\u2013Iran exchange widens across the Gulf."),
    ("TECH  ·  MARKETS", icon_chip,
     "Nvidia cheers as Huang open to return",
     "Shares rise after Tuesday\u2019s earnings."),
    ("EUROPE  ·  DIPLOMACY", icon_document,
     "Britain sanctions settlement firms",
     "Eight firms hit over West Bank settlements."),
    ("ASIA  ·  WEATHER", icon_cyclone,
     "Cyclone Akvan strengthens in Bay of Bengal",
     "Andhra Pradesh and Odisha on high alert."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 208], fill=INK)
    title = "THE WORLD IN ONE DAY"
    tf = fnt(BOLD, 44)
    d.text(((W - d.textlength(title, font=tf)) / 2, 22), title,
           font=tf, fill=PAPER)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    df = fnt(BOLD, 62)
    while d.textlength(date, font=df) > W - 48 and df.size > 40:
        df = fnt(BOLD, df.size - 2)
    d.text(((W - d.textlength(date, font=df)) / 2, 82), date,
           font=df, fill=(232, 90, 70))
    sub = "Six stories from around the globe \u2014 one day"
    sf = fnt(REG, 22)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 162), sub,
           font=sf, fill=(200, 192, 172))
    d.line([(24, 208), (W - 24, 208)], fill=RED, width=6)

    # ---- grid: 2 rows x 3 columns ----
    x0, y0, gap = 24, 224, 16
    pw = (W - 2 * x0 - 2 * gap) // 3          # 314
    ph = (H - y0 - 24 - gap) // 2             # 380
    tag_f = fnt(BOLD, 17)
    head_f = fnt(BOLD, 29)
    sub_f = fnt(REG, 20)

    for i, (tag, icon, headline, sublabel) in enumerate(STORIES):
        r, c = divmod(i, 3)
        x = x0 + c * (pw + gap)
        y = y0 + r * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=PANEL, outline=INK, width=2)
        tw = d.textlength(tag, font=tag_f)
        d.text((x + (pw - tw) / 2, y + 16), tag, font=tag_f, fill=RED)
        d.line([(x + 30, y + 46), (x + pw - 30, y + 46)],
               fill=(200, 190, 165), width=2)
        icon(d, x + pw // 2, y + 125)
        lines = wrap(d, headline, head_f, pw - 36)
        hy = y + 212
        end_y = centred(d, x + pw // 2, hy, lines, head_f, INK, lead=4)
        sub_lines = wrap(d, sublabel, sub_f, pw - 36)
        centred(d, x + pw // 2, end_y + 8, sub_lines, sub_f, GREY, lead=4)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
