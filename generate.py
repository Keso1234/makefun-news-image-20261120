"""Draw a newspaper front page summing up the world news of
Friday, 20 November 2026. Standard library plus Pillow only.
Writes entry.png (1024x1024) next to this file."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (22, 22, 22)
MUTED = (96, 93, 88)
RED = (176, 32, 24)
BLUE = (26, 64, 108)
GREEN = (24, 120, 70)
RULE = (178, 173, 164)
PANEL = (236, 232, 222)
PANEL_LINE = (205, 200, 190)
MARGIN = 36

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def load(name, size):
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_lines(draw, x, y, lines, font, fill, spacing=4):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, font):
    draw.text((x, y), text, font=font, fill=RED)
    return y + font.size + 4


# ---- small drawn illustrations (simple geometric marks) ----

def icon_scales(draw, x, y, s, color=BLUE):
    """Scales of justice inside a square of side s at (x, y)."""
    cx = x + s // 2
    top = y + int(s * 0.12)
    base = y + int(s * 0.88)
    draw.line([(cx, top), (cx, base)], fill=color, width=5)
    draw.line([(x + int(s * 0.18), top + 8), (x + int(s * 0.82), top + 8)],
              fill=color, width=5)
    for px in (x + int(s * 0.18), x + int(s * 0.82)):
        draw.line([(px, top + 8), (px - 22, top + 52)], fill=color, width=3)
        draw.line([(px, top + 8), (px + 22, top + 52)], fill=color, width=3)
        draw.arc([px - 24, top + 44, px + 24, top + 78],
                 start=0, end=180, fill=color, width=4)
    draw.line([(cx - 26, base), (cx + 26, base)], fill=color, width=5)
    draw.ellipse([cx - 7, top - 8, cx + 7, top + 6], fill=color)


def icon_globe(draw, x, y, s, color=BLUE):
    cx, cy, r = x + s // 2, y + s // 2, int(s * 0.36)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=color, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2],
             start=180, end=360, fill=color, width=3)


def icon_bridge(draw, x, y, s, color=BLUE):
    deck = y + int(s * 0.62)
    draw.rectangle([x + 8, deck, x + s - 8, deck + 8], fill=color)
    for tx in (x + int(s * 0.25), x + int(s * 0.68)):
        draw.rectangle([tx, y + int(s * 0.22), tx + 8, deck], fill=color)
    draw.line([(x + int(s * 0.25) + 4, y + int(s * 0.22)),
               (x + 12, deck)], fill=color, width=3)
    draw.line([(x + int(s * 0.25) + 4, y + int(s * 0.22)),
               (x + int(s * 0.47), deck)], fill=color, width=3)
    draw.line([(x + int(s * 0.68) + 4, y + int(s * 0.22)),
               (x + int(s * 0.47), deck)], fill=color, width=3)
    draw.line([(x + int(s * 0.68) + 4, y + int(s * 0.22)),
               (x + s - 12, deck)], fill=color, width=3)
    # blast mark above the deck
    bx, by = x + int(s * 0.47), y + int(s * 0.30)
    for dx, dy in ((-14, -10), (14, -10), (-16, 6), (16, 6), (0, -18)):
        draw.line([(bx, by), (bx + dx, by + dy)], fill=RED, width=4)


def icon_tower(draw, x, y, s, color=BLUE):
    tw = int(s * 0.30)
    tx = x + (s - tw) // 2
    ty = y + int(s * 0.14)
    th = int(s * 0.72)
    draw.rectangle([tx, ty, tx + tw, ty + th], outline=color, width=4)
    for wy in range(ty + 12, ty + th - 8, 16):
        draw.line([(tx + 8, wy), (tx + tw - 8, wy)], fill=color, width=2)
    # impact star at the top corner
    sx, sy = tx + tw - 4, ty + 6
    for dx, dy in ((-18, -14), (12, -16), (-20, 4), (16, 2), (-6, -20)):
        draw.line([(sx, sy), (sx + dx, sy + dy)], fill=RED, width=4)


def icon_chart(draw, x, y, s, color=BLUE):
    ox, oy = x + int(s * 0.14), y + int(s * 0.82)
    draw.line([(ox, y + int(s * 0.14)), (ox, oy)], fill=color, width=4)
    draw.line([(ox, oy), (x + int(s * 0.88), oy)], fill=color, width=4)
    # one line up (the IPO), one line down (the market)
    up = [(ox + 6, oy - 18), (ox + 34, oy - 34), (ox + 62, oy - 30),
          (ox + 92, oy - 66)]
    down = [(ox + 6, oy - 62), (ox + 34, oy - 44), (ox + 62, oy - 50),
            (ox + 92, oy - 16)]
    draw.line(up, fill=GREEN, width=5, joint="curve")
    draw.line(down, fill=RED, width=5, joint="curve")


def icon_controller(draw, x, y, s, color=BLUE):
    cx, cy = x + s // 2, y + s // 2
    draw.rounded_rectangle([cx - 44, cy - 26, cx + 44, cy + 26],
                           radius=18, outline=color, width=5)
    draw.ellipse([cx + 16, cy - 10, cx + 28, cy + 2], fill=color)
    draw.ellipse([cx + 30, cy + 2, cx + 42, cy + 14], fill=color)
    draw.line([(cx - 34, cy), (cx - 16, cy)], fill=color, width=5)
    draw.line([(cx - 25, cy - 9), (cx - 25, cy + 9)], fill=color, width=5)


# ---- page ----

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    mast = load(SERIF_B, 58)
    date_f = load(SANS_B, 27)
    sub_f = load(SANS, 17)
    kick_f = load(SANS_B, 18)
    lead_head = load(SERIF_B, 38)
    lead_body = load(SANS, 20)
    card_kick = load(SANS_B, 16)
    card_head = load(SERIF_B, 24)
    card_body = load(SANS, 17)
    strip_head = load(SERIF_B, 25)
    strip_body = load(SANS, 18)
    foot_f = load(SANS, 15)

    inner = W - 2 * MARGIN  # 952

    # Masthead
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=mast)
    draw.text(((W - tw) / 2, 24), title, font=mast, fill=INK)
    rule(draw, MARGIN, 100, W - MARGIN, width=3, fill=INK)

    # Date band
    date_text = "FRIDAY, 20 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_f)
    draw.text(((W - dw) / 2, 112), date_text, font=date_f, fill=INK)
    tag = "ONE DAY  \u00b7  ONE PAGE  \u00b7  THE WORLD'S NEWS"
    sw = draw.textlength(tag, font=sub_f)
    draw.text(((W - sw) / 2, 148), tag, font=sub_f, fill=MUTED)
    rule(draw, MARGIN, 176, W - MARGIN, width=2, fill=INK)

    # ---- Lead story ----
    ly = 192
    lx = MARGIN
    text_w = 600
    y = kicker(draw, lx, ly, "THE HAGUE  \u00b7  WORLD COURT", kick_f)
    head = "WORLD COURT: MYANMAR COMMITTED GENOCIDE"
    y = draw_lines(draw, lx, y, wrap(draw, head, lead_head, text_w),
                   lead_head, INK, spacing=2)
    y += 6
    deck = ("The International Court of Justice rules 9\u20136 that Myanmar's "
            "forces committed genocide against the Rohingya \u2014 the court's "
            "first such finding against a state. The ruling orders reparations "
            "and a safe return home.")
    y = draw_lines(draw, lx, y, wrap(draw, deck, lead_body, text_w),
                   lead_body, INK, spacing=3)
    # Lead illustration panel (right)
    px0 = MARGIN + text_w + 24
    py0, py1 = ly, 408
    draw.rectangle([px0, py0, W - MARGIN, py1], fill=PANEL,
                   outline=PANEL_LINE, width=2)
    icon_scales(draw, px0 + 82, py0 + 10, 148)
    cap = "The ICJ in The Hague:\ngenocide, 9\u20136"
    cy = py0 + 166
    for line in cap.split("\n"):
        lw = draw.textlength(line, font=card_body)
        draw.text((px0 + (W - MARGIN - px0 - lw) / 2, cy), line,
                  font=card_body, fill=MUTED)
        cy += card_body.size + 2
    rule(draw, MARGIN, 424, W - MARGIN, width=2)

    # ---- Secondary grid, 2 x 2 ----
    cards = [
        ("SHENZHEN  \u00b7  SUMMIT", icon_globe,
         "Trump, Xi and Putin sign peace declaration",
         "First three-way summit runs about 70 minutes and ends with a "
         "four-point declaration \u2014 but no breakthrough on Ukraine or Iran."),
        ("UKRAINE WAR", icon_bridge,
         "Russian strikes hit Kyiv bridges; 8 killed",
         "Overnight barrage on the capital's Dnipro crossings injures 28, "
         "hours after Ukraine's third strike this week on the Crimea Bridge."),
        ("MIDDLE EAST", icon_tower,
         "Houthi missiles damage Riyadh tower",
         "Strikes hit the Saudi capital's financial district, damaging the "
         "sovereign wealth fund tower. Riyadh intercepts a missile and drones."),
        ("MARKETS  \u00b7  TECH", icon_chart,
         "Anthropic jumps 17% in record IPO",
         "The $83 IPO closes at $97.17 in the largest listing ever, yet the "
         "S&P 500 falls a fifth day and Tokyo's Nikkei drops 4.8%."),
    ]
    gap = 20
    cw = (inner - gap) // 2
    ch = 172
    gy0 = 440
    for i, (kick, icon, headline, body) in enumerate(cards):
        cx0 = MARGIN + (i % 2) * (cw + gap)
        cy0 = gy0 + (i // 2) * (ch + gap)
        draw.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=PANEL,
                       outline=PANEL_LINE, width=2)
        icon(draw, cx0 + 12, cy0 + 34, 96)
        tx = cx0 + 122
        tw2 = cw - 122 - 14
        yy = kicker(draw, tx, cy0 + 10, kick, card_kick)
        yy = draw_lines(draw, tx, yy,
                        wrap(draw, headline, card_head, tw2),
                        card_head, INK, spacing=1)
        draw_lines(draw, tx, yy + 4,
                   wrap(draw, body, card_body, tw2),
                   card_body, INK, spacing=2)

    # ---- GTA 6 strip ----
    sy0 = gy0 + 2 * ch + gap + 20  # 824
    draw.rectangle([MARGIN, sy0, W - MARGIN, sy0 + 96], fill=BLUE)
    icon_controller(draw, MARGIN + 14, sy0 + 10, 76, color=(250, 247, 240))
    sx = MARGIN + 104
    draw.text((sx, sy0 + 10), "CULTURE  \u00b7  GAMES", font=card_kick,
              fill=(255, 214, 130))
    draw.text((sx, sy0 + 32), "GTA 6 opens with an estimated $2.36bn",
              font=strip_head, fill=(250, 247, 240))
    draw.text((sx, sy0 + 64),
              "About 24.6m copies on day one \u2014 the biggest entertainment "
              "launch on record.",
              font=strip_body, fill=(220, 226, 232))

    # ---- Footer ticker ----
    fy = sy0 + 112
    rule(draw, MARGIN, fy, W - MARGIN, width=2)
    foot = ("ALSO TODAY:  IMF warns global public debt is nearing 100% of "
            "world GDP  \u00b7  US Senate passes energy-permitting bill, "
            "62\u201333  \u00b7  Poland says Russian missiles and a drone "
            "violated its airspace")
    draw_lines(draw, MARGIN, fy + 10, wrap(draw, foot, foot_f, inner),
               foot_f, MUTED, spacing=2)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
