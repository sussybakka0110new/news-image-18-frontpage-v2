"""Draw a dense one-day world-news front page as a 1024x1024 PNG.

Standard library only: the PNG is assembled with struct and zlib, and all text is
painted from a small 5x7 bitmap font. No network, no randomness: identical bytes
on every run.
"""

import struct
import zlib

W = H = 1024

BG = (9, 14, 30)
PANEL = (16, 24, 46)
NAVY = (9, 14, 30)
GOLD = (232, 184, 59)
GOLD_DIM = (150, 112, 36)
CREAM = (245, 238, 215)
PALE = (196, 208, 230)
RED = (226, 78, 62)
LAND = (46, 66, 96)
COAST = (94, 124, 164)

DATE = "18 NOVEMBER 2026"

# 5x7 glyphs, one row per line. Only the characters the page uses are defined.
FONT = {
    "A": "01110/10001/10001/11111/10001/10001/10001",
    "B": "11110/10001/10001/11110/10001/10001/11110",
    "C": "01111/10000/10000/10000/10000/10000/01111",
    "D": "11110/10001/10001/10001/10001/10001/11110",
    "E": "11111/10000/10000/11110/10000/10000/11111",
    "F": "11111/10000/10000/11110/10000/10000/10000",
    "G": "01111/10000/10000/10111/10001/10001/01111",
    "H": "10001/10001/10001/11111/10001/10001/10001",
    "I": "11111/00100/00100/00100/00100/00100/11111",
    "J": "00111/00010/00010/00010/00010/10010/01100",
    "K": "10001/10010/10100/11000/10100/10010/10001",
    "L": "10000/10000/10000/10000/10000/10000/11111",
    "M": "10001/11011/10101/10101/10001/10001/10001",
    "N": "10001/11001/10101/10011/10001/10001/10001",
    "O": "01110/10001/10001/10001/10001/10001/01110",
    "P": "11110/10001/10001/11110/10000/10000/10000",
    "Q": "01110/10001/10001/10001/10101/10010/01101",
    "R": "11110/10001/10001/11110/10100/10010/10001",
    "S": "01111/10000/10000/01110/00001/00001/11110",
    "T": "11111/00100/00100/00100/00100/00100/00100",
    "U": "10001/10001/10001/10001/10001/10001/01110",
    "V": "10001/10001/10001/10001/10001/01010/00100",
    "W": "10001/10001/10001/10101/10101/11011/10001",
    "X": "10001/10001/01010/00100/01010/10001/10001",
    "Y": "10001/10001/01010/00100/00100/00100/00100",
    "Z": "11111/00001/00010/00100/01000/10000/11111",
    "0": "01110/10001/10011/10101/11001/10001/01110",
    "1": "00100/01100/00100/00100/00100/00100/01110",
    "2": "01110/10001/00001/00010/00100/01000/11111",
    "3": "11111/00010/00100/00010/00001/10001/01110",
    "4": "00010/00110/01010/10010/11111/00010/00010",
    "5": "11111/10000/11110/00001/00001/10001/01110",
    "6": "00110/01000/10000/11110/10001/10001/01110",
    "7": "11111/00001/00010/00100/01000/01000/01000",
    "8": "01110/10001/10001/01110/10001/10001/01110",
    "9": "01110/10001/10001/01111/00001/00010/01100",
    " ": "00000/00000/00000/00000/00000/00000/00000",
    ".": "00000/00000/00000/00000/00000/01100/01100",
    ",": "00000/00000/00000/00000/01100/01100/00110",
    "-": "00000/00000/00000/11111/00000/00000/00000",
    "/": "00001/00010/00010/00100/01000/01000/10000",
    ":": "00000/01100/01100/00000/01100/01100/00000",
    "&": "01100/10010/10100/01000/10101/10010/01101",
    "'": "00100/00100/00000/00000/00000/00000/00000",
    "(": "00010/00100/01000/01000/01000/00100/00010",
    ")": "01000/00100/00010/00010/00010/00100/01000",
    "?": "01110/10001/00001/00010/00100/00000/00100",
    "!": "00100/00100/00100/00100/00100/00000/00100",
    "+": "00000/00100/00100/11111/00100/00100/00000",
    "%": "11001/11010/00010/00100/01000/01011/10011",
    "|": "00100/00100/00100/00100/00100/00100/00100",
}

SECTIONS = [
    ("WORLD / CONFLICT", [
        "Ukraine strike partly collapses Kerch Bridge",
        "Zelensky hails 'unprecedented' strike",
        "Russia 'double-tap' on Kyiv kills 72",
        "Rescue operation targeted after Kyiv strike",
        "Russian military plane crashes; all 19 dead",
        "Iran launches third strikes on Bahrain",
        "Bahrain hosts US Navy's 5th Fleet",
        "Iran strikes on Bahrain continue",
        "Trump: US takes Iran plot 'very seriously'",
        "Palestinian woman, 72, shot in West Bank",
        "Five EU states unveil Rwanda return hubs",
        "EU accused of sugarcoating Egypt funds",
        "Costa Rican journalist shot dead",
        "First such killing in 25 years",
        "Isolated Brazilian tribe emerges",
    ]),
    ("POLITICS / TECH", [
        "Nvidia doubles revenue in results",
        "Nvidia board: no plan to reinstate Huang",
        "Trump backs Huang reinstatement",
        "Megaspeed probed over chip exports",
        "Huang to testify before Congress",
        "Trump, Xi meet at APEC in Shenzhen",
        "China AI faces Nvidia spy scandal",
        "Xi sends 'Chinamaxxing' message",
        "Xi and Putin start talks",
        "Rubio: no systemic attack after outages",
        "Trump serious on meeting Kim Jong-un",
        "Democrats win Alaska Senate race",
        "Count ends two weeks after midterms",
        "US loses measles elimination status",
        "Measles-free status ended after 26 years",
    ]),
    ("REGIONS / CULTURE", [
        "US soldier arrested in UK on spying",
        "Philippines seeks Thomas Markle charges",
        "Hundreds arrested at Philippine protests",
        "Protests over Iran war and AI pact",
        "Oil supply back in surplus, says IEA",
        "IEA: first surplus since Iran war",
        "Australian wages fastest since 2023",
        "Prices climb faster than wages",
        "William and Kate fete Earthshot in Mumbai",
        "Royals begin India visit",
        "US player held with 75lb marijuana",
        "Nigerian airport arrest stuns NBA",
        "NY teen reunites with lost cat",
        "Pope Leo hit by flying rosary in Peru",
        "Nissan cuts petrol output as China EV booms",
    ]),
]

CANVAS = bytearray(BG * (W * H))


def rect(x, y, w, h, color):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x0 >= x1 or y0 >= y1:
        return
    row = bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        start = (yy * W + x0) * 3
        CANVAS[start:start + len(row)] = row


def outline(x, y, w, h, color, t=1):
    rect(x, y, w, t, color)
    rect(x, y + h - t, w, t, color)
    rect(x, y, t, h, color)
    rect(x + w - t, y, t, h, color)


def text_width(s, scale, gap=1):
    return (len(s) * (5 + gap) - gap) * scale if s else 0


def put_text(s, x, y, scale, color, gap=1):
    s = s.upper()
    for i, ch in enumerate(s):
        glyph = FONT.get(ch, FONT["?"])
        gx = x + i * (5 + gap) * scale
        for ry, rowstr in enumerate(glyph.split("/")):
            for rx, bit in enumerate(rowstr):
                if bit == "1":
                    rect(gx + rx * scale, y + ry * scale, scale, scale, color)


def put_centered(s, x0, x1, y, scale, color, gap=1):
    put_text(s, x0 + (x1 - x0 - text_width(s, scale, gap)) // 2, y, scale, color, gap)


def wrap(s, limit):
    words, lines, line = s.split(), [], ""
    for word in words:
        candidate = word if not line else line + " " + word
        if len(candidate) <= limit:
            line = candidate
        else:
            if line:
                lines.append(line)
            while len(word) > limit:
                lines.append(word[:limit])
                word = word[limit:]
            line = word
    if line:
        lines.append(line)
    return lines[:2]


def marker(local_x, local_y, color, label, label_dx=0, label_dy=9):
    x, y = 28 + local_x, 736 + local_y
    rect(x - 2, y - 2, 9, 9, NAVY)
    rect(x, y, 5, 5, color)
    put_text(label, x + label_dx, y + label_dy, 1, PALE)


def compose():
    # Deep navy field and a warm-gold masthead banner.
    rect(0, 0, W, 108, GOLD)
    rect(0, 104, W, 4, GOLD_DIM)
    put_centered("WORLD NEWS / THE DAILY FRONT PAGE", 0, W, 12, 2, NAVY)
    put_centered(DATE, 0, W, 30, 8, NAVY)

    # Three themed columns of short, verified headlines.
    col_x = (16, 348, 680)
    for col, (label, stories) in enumerate(SECTIONS):
        put_centered(label, col_x[col], col_x[col] + 324, 116, 2, GOLD)
        rect(col_x[col], 137, 324, 1, GOLD_DIM)
        for row, story in enumerate(stories):
            y = 146 + row * 36
            x = col_x[col]
            rect(x, y + 34, 324, 1, (28, 40, 66))
            rect(x + 1, y + 3, 4, 4, RED)
            for line_no, line in enumerate(wrap(story, 26)):
                put_text(line, x + 10, y + 1 + line_no * 16, 2,
                         CREAM if line_no == 0 else PALE)

    # Simplified world map with ten flashpoint markers.
    rect(16, 700, 992, 280, PANEL)
    outline(16, 700, 992, 280, GOLD_DIM, 2)
    put_text("WORLD MAP / 10 FLASHPOINTS", 26, 708, 2, GOLD)
    put_centered("6 CONTINENTS / 45 STORIES", 690, 1008, 708, 2, GOLD)

    def land(x, y, w, h):
        rect(28 + x, 736 + y, w, h, LAND)
        outline(28 + x, 736 + y, w, h, COAST, 1)

    land(30, 18, 150, 60)
    land(60, 78, 50, 18)
    land(105, 100, 55, 70)
    land(190, 8, 40, 22)
    land(420, 22, 70, 38)
    land(415, 70, 85, 75)
    land(500, 10, 260, 70)
    land(560, 80, 50, 35)
    land(640, 80, 70, 20)
    land(740, 125, 80, 40)
    land(840, 150, 12, 18)

    marker(95, 45, GOLD, "WASHINGTON", -20, -12)
    marker(135, 140, GOLD, "PERU", -8, 10)
    marker(455, 40, RED, "KYIV", -14, -12)
    marker(490, 28, GOLD, "RUSSIA", -8, -12)
    marker(555, 95, RED, "BAHRAIN", -18, 10)
    marker(440, 110, GOLD, "NIGERIA", -14, 10)
    marker(475, 138, RED, "RWANDA", -12, 10)
    marker(690, 45, GOLD, "BEIJING", -14, -12)
    marker(585, 100, GOLD, "MUMBAI", 4, 16)
    marker(780, 150, GOLD, "CANBERRA", -18, 10)

    put_centered("N.AMERICA   S.AMERICA   EUROPE   AFRICA   ASIA   OCEANIA",
                 16, 1008, 958, 2, GOLD_DIM)
    rect(0, 990, W, 1, GOLD)
    put_centered("WORLD NEWS | " + DATE + " | SOURCES: BBC, GUARDIAN",
                 0, W, 998, 2, GOLD)


def save_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(CANVAS[y * W * 3:(y + 1) * W * 3])
    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


if __name__ == "__main__":
    compose()
    save_png("entry.png")
