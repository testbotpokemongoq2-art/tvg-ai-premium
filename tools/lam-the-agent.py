# -*- coding: utf-8 -*-
"""Dựng ảnh thẻ agent theo đúng khuôn 01–13 trên tvgagentai.com: logo TVG vàng phía trên,
nhân vật ở giữa, khung tiêu đề viền vàng phía dưới.
Chạy: python -I tools/lam-the-agent.py  (từ thư mục landing-13-agent)"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VP = os.path.join(os.path.dirname(HERE), "van-phong")
S = 720
FONT_B = next((f for f in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf") if os.path.exists(f)), None)
FONT_R = next((f for f in ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf") if os.path.exists(f)), None)

THE = [  # số, ảnh gốc, tiêu đề, dòng phụ
    ("14", os.path.join(VP, "ai-hang", "assets", "badger_full.jpg"), "14 · AI Hằng — Accounting", "BOOKKEEPING · CASH FLOW · TOUR P&L · REPORTS"),
    ("15", os.path.join(VP, "ai-phu", "assets", "badger_full.jpg"), "15 · AI Phú — Photo to Video", "STORYBOARD · MOTION · VOICE-OVER · REELS"),
]


def gold_text(base, xy, text, font, anchor="mm"):
    """Chữ vàng chuyển sắc (sáng ở trên, đậm ở dưới) + bóng tối, giống tiêu đề thẻ cũ."""
    d = ImageDraw.Draw(base)
    x, y = xy
    d.text((x + 2, y + 3), text, font=font, fill=(0, 0, 0), anchor=anchor)
    mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(mask).text(xy, text, font=font, fill=255, anchor=anchor)
    l, t, r, b = mask.getbbox()
    grad = Image.new("RGB", base.size)
    gd = ImageDraw.Draw(grad)
    for yy in range(t, b + 1):
        k = (yy - t) / max(b - t, 1)
        c = (int(250 - 70 * k), int(215 - 80 * k), int(130 - 80 * k))
        gd.line([(0, yy), (base.width, yy)], fill=c)
    base.paste(grad, (0, 0), mask)


def frame(d, box, inset=0):
    """Khung bát giác viền vàng đôi như thanh tiêu đề thẻ cũ."""
    l, t, r, b = box
    c = 16
    pts = [(l + c, t), (r - c, t), (r, t + c), (r, b - c), (r - c, b), (l + c, b), (l, b - c), (l, t + c)]
    d.polygon(pts, fill=(12, 10, 6))
    d.line(pts + [pts[0]], fill=(212, 166, 64), width=3)
    l, t, r, b = l + 7, t + 7, r - 7, b - 7
    pts2 = [(l + c, t), (r - c, t), (r, t + c), (r, b - c), (r - c, b), (l + c, b), (l, b - c), (l, t + c)]
    d.line(pts2 + [pts2[0]], fill=(138, 106, 42), width=1)


def make(num, src, title, sub, logo):
    art = Image.open(src).convert("RGB")
    # Nền: chính ảnh phóng to, làm mờ & tối (giữ không khí HUD đen vàng)
    bg = art.resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(18))
    bg = ImageEnhance.Brightness(bg).enhance(.45)
    # Nhân vật thu nhỏ, đặt thấp xuống để chừa chỗ cho logo
    sc = int(S * .8)
    fg = art.resize((sc, sc), Image.LANCZOS)
    m = Image.new("L", (sc, sc), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, sc, sc), 28, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(10))
    bg.paste(fg, ((S - sc) // 2, int(S * .14)), m)
    # Logo TVG trên cùng
    lg = logo.copy()
    lg.thumbnail((int(S * .26), int(S * .17)))
    bg.paste(lg, ((S - lg.width) // 2, 10), lg)
    # Khung tiêu đề dưới
    d = ImageDraw.Draw(bg)
    box = (22, int(S * .77), S - 22, S - 18)
    frame(d, box)
    f1 = ImageFont.truetype(FONT_B, 42)
    while d.textlength(title, font=f1) > box[2] - box[0] - 50:
        f1 = ImageFont.truetype(FONT_B, f1.size - 2)
    gold_text(bg, (S // 2, box[1] + 50), title, f1)
    f2 = ImageFont.truetype(FONT_R, 17)
    d.text((S // 2, box[1] + 96), "  ".join(sub), font=f2, fill=(212, 166, 64), anchor="mm") if False else \
        d.text((S // 2, box[1] + 96), sub, font=f2, fill=(212, 166, 64), anchor="mm")
    out = os.path.join(HERE, "images", f"{num}.jpg")
    bg.save(out, quality=90)
    print("Đã tạo", out)


if __name__ == "__main__":
    logo = Image.open(os.path.join(HERE, "images", "logo.png")).convert("RGBA")
    for t in THE:
        make(*t, logo)
