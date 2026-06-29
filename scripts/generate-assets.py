from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def font(size, bold=False):
    candidates = [
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


INK = (17, 19, 23)
MUTED = (95, 104, 115)
RED = (216, 25, 50)
BLUE = (24, 58, 102)
TEAL = (15, 124, 120)
GREEN = (79, 127, 82)
LINE = (220, 226, 232)
PAPER = (247, 248, 250)
WHITE = (255, 255, 255)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, fill=INK, bold=False, anchor=None):
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def dashboard_image(width=1220, height=780):
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)

    rounded(draw, (34, 34, width - 34, height - 34), 18, WHITE, LINE, 2)
    rounded(draw, (58, 64, width - 58, 132), 8, (250, 251, 252), LINE, 1)
    text(draw, (82, 84), "Hive Terminal", 28, INK, True)
    text(draw, (82, 116), "Weekly replenishment workspace - illustrative sample data", 15, MUTED)
    rounded(draw, (width - 320, 78, width - 82, 118), 6, (254, 236, 239), (246, 190, 199), 1)
    text(draw, (width - 300, 90), "Sample data: 18 SKUs", 15, RED, True)

    cards = [
        ("Forecast accuracy", "91.4%", BLUE),
        ("Cash freed", "$42.8K", TEAL),
        ("Stockout risk", "-23%", GREEN),
        ("Reorder value", "$18.2K", RED),
    ]
    x = 58
    for label, value, color in cards:
        rounded(draw, (x, 158, x + 260, 280), 8, WHITE, LINE, 1)
        text(draw, (x + 22, 180), label, 16, MUTED)
        text(draw, (x + 22, 222), value, 36, color, True)
        x += 280

    rounded(draw, (58, 316, 646, 704), 8, WHITE, LINE, 1)
    text(draw, (84, 344), "Demand forecast vs. actual", 20, INK, True)
    axis_y = 642
    draw.line((94, axis_y, 604, axis_y), fill=LINE, width=2)
    draw.line((94, 390, 94, axis_y), fill=LINE, width=2)
    points_actual = [(100, 604), (160, 580), (220, 592), (280, 536), (340, 510), (400, 458), (460, 476), (520, 430), (590, 392)]
    points_forecast = [(100, 622), (160, 594), (220, 566), (280, 548), (340, 498), (400, 478), (460, 448), (520, 420), (590, 376)]
    draw.line(points_actual, fill=BLUE, width=5, joint="curve")
    draw.line(points_forecast, fill=RED, width=5, joint="curve")
    for point in points_actual:
        draw.ellipse((point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4), fill=BLUE)
    for point in points_forecast:
        draw.ellipse((point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4), fill=RED)
    text(draw, (436, 352), "Actual", 14, BLUE, True)
    text(draw, (514, 352), "Forecast", 14, RED, True)

    rounded(draw, (676, 316, width - 58, 704), 8, WHITE, LINE, 1)
    text(draw, (704, 344), "Reorder recommendations", 20, INK, True)
    columns = [704, 850, 970, 1080]
    headers = ["SKU", "Action", "Qty", "Why"]
    for x, h in zip(columns, headers):
        text(draw, (x, 392), h, 13, MUTED, True)
    rows = [
        ("HNY-204", "Reorder", "420", "Stockout risk"),
        ("BEE-118", "Hold", "0", "Overstock"),
        ("BOX-045", "Reorder", "160", "Lead time"),
        ("KIT-722", "Reduce", "90", "Slow demand"),
        ("JAR-310", "Reorder", "240", "Margin risk"),
    ]
    y = 430
    for i, row in enumerate(rows):
        if i % 2 == 0:
            rounded(draw, (698, y - 12, width - 86, y + 35), 6, (247, 250, 252), None)
        for x, cell in zip(columns, row):
            fill = RED if cell == "Reorder" else TEAL if cell == "Hold" else INK
            text(draw, (x, y), cell, 15, fill, cell in {"Reorder", "Hold", "Reduce"})
        y += 54

    return image


def audit_snapshot_image(width=1220, height=780):
    image = Image.new("RGB", (width, height), (237, 244, 243))
    draw = ImageDraw.Draw(image)

    rounded(draw, (34, 34, width - 34, height - 34), 18, WHITE, LINE, 2)
    rounded(draw, (58, 62, width - 58, 126), 8, (250, 251, 252), LINE, 1)
    text(draw, (82, 82), "Inventory Audit Snapshot", 28, INK, True)
    text(draw, (82, 114), "Illustrative sample data - cash, stockout, and reorder-policy examples", 15, MUTED)
    rounded(draw, (width - 252, 78, width - 82, 116), 6, (236, 247, 246), (171, 216, 212), 1)
    text(draw, (width - 226, 89), "Sample data", 15, TEAL, True)

    summary = [
        ("Cash unlocked", "$42.8K", TEAL, 0.78),
        ("Lost-sales risk", "-23%", RED, 0.58),
        ("Policy changes", "31 SKUs", BLUE, 0.66),
    ]
    y = 164
    for label, value, color, bar in summary:
        rounded(draw, (58, y, 530, y + 104), 8, WHITE, LINE, 1)
        text(draw, (84, y + 22), label, 16, MUTED, True)
        text(draw, (84, y + 52), value, 34, color, True)
        draw.rounded_rectangle((280, y + 61, 490, y + 75), radius=7, fill=(232, 237, 242))
        draw.rounded_rectangle((280, y + 61, int(280 + 210 * bar), y + 75), radius=7, fill=color)
        y += 128

    rounded(draw, (568, 164, width - 58, 500), 8, WHITE, LINE, 1)
    text(draw, (596, 194), "SKU priority matrix", 22, INK, True)
    text(draw, (596, 224), "Higher-risk products move first", 15, MUTED)
    matrix = (628, 260, width - 102, 454)
    draw.rectangle(matrix, outline=LINE, width=2)
    mx0, my0, mx1, my1 = matrix
    draw.line((mx0, (my0 + my1) // 2, mx1, (my0 + my1) // 2), fill=LINE, width=1)
    draw.line(((mx0 + mx1) // 2, my0, (mx0 + mx1) // 2, my1), fill=LINE, width=1)
    text(draw, (mx0, my1 + 18), "Holding cost", 13, MUTED)
    text(draw, (mx1 - 120, my1 + 18), "Stockout risk", 13, MUTED)
    points = [
        (704, 404, TEAL),
        (772, 348, BLUE),
        (842, 386, TEAL),
        (902, 296, RED),
        (980, 326, RED),
        (1046, 286, RED),
    ]
    for x, py, color in points:
        draw.ellipse((x - 11, py - 11, x + 11, py + 11), fill=color, outline=WHITE, width=3)
    text(draw, (904, 254), "Act now", 14, RED, True)

    rounded(draw, (568, 520, width - 58, 736), 8, WHITE, LINE, 1)
    text(draw, (596, 550), "Next-best policies", 20, INK, True)
    rows = [
        ("HNY-204", "Stockout exposure", "Reorder now"),
        ("BEE-118", "Overstock", "Pause buying"),
        ("KIT-722", "Slow demand", "Reduce target"),
    ]
    columns = [596, 758, 976]
    headers = ["SKU", "Finding", "Action"]
    for x, h in zip(columns, headers):
        text(draw, (x, 594), h, 13, MUTED, True)
    row_y = 628
    for i, row in enumerate(rows):
        if i % 2 == 0:
            rounded(draw, (588, row_y - 11, width - 84, row_y + 31), 6, (247, 250, 252), None)
        for x, cell in zip(columns, row):
            fill = RED if cell == "Reorder now" else TEAL if cell == "Pause buying" else INK
            text(draw, (x, row_y), cell, 15, fill, cell in {"Reorder now", "Pause buying"})
        row_y += 38

    return image


def create_assets():
    dashboard = dashboard_image()
    dashboard.save(PUBLIC / "dashboard-preview.png")
    audit_snapshot = audit_snapshot_image()
    audit_snapshot.save(PUBLIC / "audit-snapshot.png")

    hero = Image.new("RGB", (1800, 1040), (250, 251, 252))
    draw = ImageDraw.Draw(hero)
    # Quiet left area for overlay text.
    for x in range(0, 1800, 48):
        color = (237, 241, 245) if (x // 48) % 2 == 0 else (245, 247, 249)
        draw.rectangle((x, 0, x + 24, 1040), fill=color)
    dash = dashboard.resize((1030, 660), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", dash.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((0, 0, dash.width - 1, dash.height - 1), radius=20, fill=(0, 0, 0, 44))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    hero.paste(shadow.convert("RGB"), (980, 214))
    hero.paste(dash, (950, 190))
    draw.rectangle((0, 0, 870, 1040), fill=(255, 255, 255))
    for i, color in enumerate([RED, (232, 65, 82), (177, 18, 35)]):
        cx = 112 + i * 70
        cy = 940 - (i % 2) * 58
        draw.regular_polygon((cx, cy, 42), 6, rotation=30, fill=color)
    hero.save(PUBLIC / "hero-dashboard.png", quality=95)

    og = Image.new("RGB", (1200, 630), (247, 248, 250))
    draw = ImageDraw.Draw(og)
    mark = Image.open(PUBLIC / "logo-mark.png").convert("RGBA")
    mark.thumbnail((230, 230), Image.Resampling.LANCZOS)
    og.paste(mark, (74, 92), mark)
    text(draw, (74, 360), "Just Hive Data", 66, INK, True)
    text(draw, (74, 438), "Inventory optimization for SMB operators", 32, MUTED)
    rounded(draw, (860, 90, 1126, 540), 16, WHITE, LINE, 2)
    text(draw, (896, 134), "Hive Terminal", 24, INK, True)
    text(draw, (896, 166), "Illustrative sample data", 15, MUTED)
    for idx, (label, value, color) in enumerate([
        ("Cash freed", "$42.8K", TEAL),
        ("Stockout risk", "-23%", RED),
        ("Forecast", "91.4%", BLUE),
    ]):
        y = 216 + idx * 96
        rounded(draw, (896, y, 1090, y + 72), 8, (247, 250, 252), LINE, 1)
        text(draw, (914, y + 14), label, 16, MUTED)
        text(draw, (914, y + 38), value, 25, color, True)
    og.save(PUBLIC / "og-image.png", quality=95)


if __name__ == "__main__":
    create_assets()
