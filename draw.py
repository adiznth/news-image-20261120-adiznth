#!/usr/bin/env python3
"""Build the 20 November 2026 world-news front page (1024x1024 PNG).

Run once at build time:  python3 draw.py
It writes entry.png next to this file. The graded program (main.py)
only copies that PNG to the output directory, so grading needs no
network and no third-party package.

Every story on the page was first reported on Friday 20 November
2026 (sources: CNN, BBC, ICJ, Le Monde).
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
BG = (245, 241, 230)
INK = (18, 22, 34)
NAVY = (13, 36, 64)
CRIMSON = (171, 32, 32)
TEAL = (12, 110, 104)
MUSTARD = (206, 164, 48)
SLATE = (88, 94, 104)
CARD = (255, 255, 255)
RULE = (198, 192, 180)

FONTS = "/usr/share/fonts/truetype/dejavu/"
DISPLAY = FONTS + "DejaVuSerif-Bold.ttf"
BOLD = FONTS + "DejaVuSans-Bold.ttf"
PLAIN = FONTS + "DejaVuSans.ttf"


def face(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(d, words, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    out, current = [], ""
    for word in words.split():
        trial = f"{current} {word}".strip()
        if d.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def para(d, x, y, text, fnt, width, fill=INK, gap=None):
    gap = gap if gap is not None else int(fnt.size * 1.3)
    for line in fit_lines(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += gap
    return y


def card(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12,
                        fill=CARD, outline=RULE, width=2)


def tag(d, x, y, words, colour):
    d.text((x, y), words, font=face(BOLD, 19), fill=colour)
    return y + 27


def boom(d, cx, cy, r, colour=CRIMSON):
    """Starburst: a missile blast drawn from triangles."""
    import math
    for k in range(8):
        a = k * math.pi / 4
        tip = (cx + r * math.cos(a), cy + r * math.sin(a))
        base1 = (cx + r * 0.32 * math.cos(a + 0.4),
                 cy + r * 0.32 * math.sin(a + 0.4))
        base2 = (cx + r * 0.32 * math.cos(a - 0.4),
                 cy + r * 0.32 * math.sin(a - 0.4))
        d.polygon([tip, base1, base2], fill=colour)
    d.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3],
              fill=(255, 205, 60))


def tower(d, x, y, w, h):
    """A glass skyscraper with a blast mark at its crown."""
    d.rectangle([x + w * 0.18, y, x + w * 0.82, y + h], fill=NAVY)
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(30, 58, 96))
    for row in range(6):
        yy = y + 10 + row * (h - 20) / 6
        d.line([x + w * 0.24, yy, x + w * 0.76, yy],
               fill=(120, 170, 220), width=2)
    boom(d, x + w * 0.82, y + 6, 14)


def scales2(d, x, y, s):
    """Balanced scales of justice, drawn from lines and arcs."""
    d.line([x + s / 2, y, x + s / 2, y + s * 0.6], fill=NAVY, width=5)
    d.line([x + 4, y + s * 0.14, x + s - 4, y + s * 0.14],
           fill=NAVY, width=5)
    for cx in (x + 10, x + s - 10):
        d.line([cx, y + s * 0.14, cx, y + s * 0.4], fill=NAVY, width=3)
        d.pieslice([cx - 15, y + s * 0.34, cx + 15, y + s * 0.62],
                   0, 180, fill=MUSTARD, outline=NAVY)
    d.line([x + s * 0.18, y + s * 0.72, x + s * 0.82, y + s * 0.72],
           fill=NAVY, width=5)


def rally(d, x, y, w, h):
    """A market line that plunges, then one rocketing up."""
    d.line([x, y + h, x + w, y + h], fill=SLATE, width=3)
    d.line([x, y, x, y + h], fill=SLATE, width=3)
    d.line([(x + 4, y + 14), (x + w * 0.45, y + h * 0.55),
            (x + w - 4, y + h - 10)], fill=CRIMSON, width=5)
    d.line([(x + 4, y + h - 12), (x + w * 0.5, y + h * 0.5),
            (x + w - 4, y + 10)], fill=TEAL, width=5)
    d.polygon([(x + w - 18, y + 4), (x + w - 2, y + 4),
               (x + w - 9, y + 20)], fill=TEAL)


def flame(d, x, y, w, h):
    """A tanker hull with a flame above it."""
    d.polygon([(x, y + h * 0.6), (x + w * 0.14, y + h * 0.9),
               (x + w * 0.86, y + h * 0.9), (x + w, y + h * 0.6)],
              fill=CRIMSON)
    d.rectangle([x + w * 0.58, y + h * 0.3, x + w * 0.8, y + h * 0.6],
                fill=NAVY)
    d.line([x, y + h * 0.97, x + w, y + h * 0.97], fill=TEAL, width=4)
    d.polygon([(x + w * 0.25, y + h * 0.45), (x + w * 0.38, y + h * 0.05),
               (x + w * 0.5, y + h * 0.45)], fill=(232, 126, 32))


def earth(d, x, y, size):
    """A globe: circle, meridian and a green land patch."""
    d.ellipse([x, y, x + size, y + size], outline=TEAL, width=5)
    d.ellipse([x + size * 0.3, y, x + size * 0.7, y + size],
              outline=TEAL, width=3)
    d.line([x, y + size / 2, x + size, y + size / 2], fill=TEAL, width=3)
    d.ellipse([x + size * 0.56, y + size * 0.56,
               x + size * 0.74, y + size * 0.74], fill=(46, 160, 67))


def draw_page():
    img = Image.new("RGB", CANVAS, BG)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, 1024, 150], fill=NAVY)
    d.rectangle([0, 150, 1024, 156], fill=MUSTARD)
    d.text((24, 16), "THE WORLD IN ONE DAY",
           font=face(DISPLAY, 54), fill=(255, 255, 255))
    d.text((24, 92), "FRIDAY  •  20 NOVEMBER 2026",
           font=face(BOLD, 32), fill=MUSTARD)
    right = "ONE IMAGE · ONE DAY"
    d.text((1024 - 24 - d.textlength(right, font=face(BOLD, 20)), 104),
           right, font=face(BOLD, 20), fill=(255, 255, 255))

    # Lead: Kyiv overnight attack
    card(d, 24, 174, 976, 252)
    tag(d, 48, 194, "LEAD  •  KYIV, UKRAINE", CRIMSON)
    boom(d, 108, 330, 52)
    d.text((180, 288), "PEACE TALK,",
           font=face(BOLD, 40), fill=INK)
    d.text((180, 340), "THEN MISSILES",
           font=face(BOLD, 40), fill=INK)
    para(d, 576, 236,
         "Hours after Trump, Xi and Putin's Shenzhen peace "
         "declaration, Russia fired 110+ missiles and 400 drones "
         "at Kyiv — three bridges hit, 8 killed, Poland scrambles "
         "its jets.", face(PLAIN, 22), 400)

    # Middle row: ICJ verdict + markets
    card(d, 24, 442, 478, 216)
    tag(d, 48, 460, "THE HAGUE  •  JUSTICE", NAVY)
    scales2(d, 48, 500, 92)
    d.text((156, 500), "MYANMAR GUILTY",
           font=face(BOLD, 29), fill=INK)
    d.text((156, 536), "OF GENOCIDE",
           font=face(BOLD, 29), fill=INK)
    para(d, 156, 576,
         "World Court rules 9–6 that Myanmar committed genocide "
         "against the Rohingya.", face(PLAIN, 18), 322)

    card(d, 522, 442, 478, 216)
    tag(d, 546, 460, "MARKETS  •  AI BOOM, STOCKS SINK", TEAL)
    rally(d, 546, 500, 104, 78)
    d.text((670, 500), "ANTHROPIC",
           font=face(BOLD, 29), fill=INK)
    d.text((670, 536), "SOARS 34%",
           font=face(BOLD, 29), fill=INK)
    para(d, 670, 576,
         "AI debut nears $2T; S&P −2%, fifth straight loss; "
         "Nikkei −4.8%.", face(PLAIN, 18), 306)

    # Bottom row: three short stories
    stories = [
        ("RIYADH", "MISSILE HITS\nTOWER",
         "A Houthi missile damages Saudi Arabia's sovereign "
         "wealth fund tower in the capital.", tower, CRIMSON),
        ("THE GULF", "TANKER WAR\nIN THE GULF",
         "Iran steps up attacks on Hormuz shipping as its war "
         "with the US enters a ninth month.", flame, NAVY),
        ("CLIMATE", "COP31 DROPS\nFOSSIL FUELS",
         "The Antalya climate draft removes any call to phase "
         "out fossil fuels.", earth, TEAL),
    ]
    x = 24
    for label, head, body, icon, colour in stories:
        card(d, x, 674, 318, 206)
        tag(d, x + 20, 690, label, colour)
        if icon is earth:
            icon(d, x + 20, 726, 72)
        else:
            icon(d, x + 20, 726, 72, 62)
        lines = head.split("\n")
        yy = 726
        for ln in lines:
            d.text((x + 108, yy), ln, font=face(BOLD, 21), fill=INK)
            yy += 27
        para(d, x + 20, 812, body, face(PLAIN, 17), 278, gap=22)
        x += 329

    # Ticker strip
    d.rectangle([0, 896, 1024, 956], fill=INK)
    d.text((24, 912), "ALSO TODAY:", font=face(BOLD, 21), fill=MUSTARD)
    para(d, 198, 910,
         "UK–EU youth mobility deal  •  Kenya discharges its last "
         "Ebola patient  •  Trump pardons Pete Rose  •  Bukele "
         "seeks a third term",
         face(PLAIN, 16), 800, fill=(255, 255, 255), gap=20)

    # Footer
    d.text((24, 968), "Events reported on 20 November 2026  •  Sources: "
           "CNN, BBC, ICJ, Le Monde", font=face(PLAIN, 15), fill=SLATE)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    draw_page()
