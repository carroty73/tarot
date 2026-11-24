#!/usr/bin/env python3
"""오늘의 타로의 앱 아이콘(1024x1024)과 OG 이미지(1200x630)를 그린다. 실행: python3 tarot/make_og_images.py
- 결과: assets/img/icon/icon-1.png, assets/img/og/og-1.png (이미지 규칙: 시안은 번호를 붙여 남기고 icon.png, og.png는 채택한 것을 가리키는 링크).
  이미 있는 번호는 덮어쓰지 않는다(다음 번호로 저장하려면 N을 바꿔서 실행: python3 make_og_images.py 2).
- 이 그림은 화면과 같은 어두운 보랏빛, 금색 별 무늬, 마법진 선, 카드 뒷면으로 그린다."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
N = sys.argv[1] if len(sys.argv) > 1 else "1"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
GOLD = (228, 194, 122)
S = 2   # 2배로 그린 뒤 줄여서 선을 부드럽게


def radial(w, h, cx, cy, r, inner, outer):
    im = Image.new("RGB", (w, h), outer)
    px = im.load()
    for y in range(h):
        for x in range(w):
            d = min(1.0, math.hypot(x - cx, y - cy) / r)
            px[x, y] = tuple(int(inner[i] + (outer[i] - inner[i]) * d) for i in range(3))
    return im


def star(d, cx, cy, r, fill, width=0):
    pts = []
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.32
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def magic(d, cx, cy, R, color, w):
    for rad, lw in ((1.0, w), (0.94, max(1, w // 2)), (0.78, w), (0.62, max(1, w // 2))):
        d.ellipse((cx - R * rad, cy - R * rad, cx + R * rad, cy + R * rad), outline=color, width=int(lw))
    for i in range(72):
        a = i * math.pi / 36
        r1, r2 = R * 0.82, R * (0.86 if i % 6 else 0.89)
        d.line((cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a)), fill=color, width=max(1, w // 2))
    pts = [(cx + R * 0.62 * math.cos(math.radians(-90 + k * 144)), cy + R * 0.62 * math.sin(math.radians(-90 + k * 144))) for k in range(5)]
    d.polygon(pts, outline=color)
    for m in range(12):
        a = m * math.pi / 6
        x, y, rr = cx + R * 0.97 * math.cos(a), cy + R * 0.97 * math.sin(a), R * 0.018
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=color, width=max(1, w // 2))


def icon():
    W = 1024 * S
    im = radial(W, W, W / 2, W / 2.1, W * 0.75, (122, 52, 104), (28, 10, 40))
    ov = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    magic(d, W / 2, W / 2, W * 0.40, GOLD + (150,), 5 * S)
    star(d, W / 2, W / 2, W * 0.27, GOLD + (255,))
    d.ellipse((W / 2 - W * 0.05, W / 2 - W * 0.05, W / 2 + W * 0.05, W / 2 + W * 0.05), fill=(122, 52, 104, 255), outline=GOLD + (255,), width=4 * S)
    glow = ov.filter(ImageFilter.GaussianBlur(14 * S))
    im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), glow), ov)
    return im.convert("RGB").resize((1024, 1024), Image.LANCZOS)


def card_back(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bg = radial(w, h, w / 2, h / 2, w * 0.75, (138, 58, 107), (61, 21, 48)).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(w * 0.07), fill=255)
    im.paste(bg, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(w * 0.07), outline=GOLD + (255,), width=max(2, w // 40))
    d.rounded_rectangle((w * 0.07, w * 0.07, w - w * 0.07, h - w * 0.07), radius=int(w * 0.04), outline=GOLD + (200,), width=max(1, w // 90))
    c = w / 2
    d.ellipse((c - w * 0.27, h / 2 - w * 0.27, c + w * 0.27, h / 2 + w * 0.27), outline=GOLD + (255,), width=max(2, w // 60))
    star(d, c, h / 2, w * 0.34, GOLD + (255,))
    d.ellipse((c - w * 0.04, h / 2 - w * 0.04, c + w * 0.04, h / 2 + w * 0.04), fill=(122, 52, 104, 255), outline=GOLD + (255,), width=max(1, w // 110))
    return im


def og():
    W, H = 1200 * S, 630 * S
    im = radial(W, H, W * 0.70, H * 0.5, W * 0.6, (96, 40, 90), (14, 6, 24)).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    magic(d, W * 0.72, H * 0.5, H * 0.78, GOLD + (95,), 3 * S)
    glow = ov.filter(ImageFilter.GaussianBlur(8 * S))
    im = Image.alpha_composite(Image.alpha_composite(im, glow), ov)
    # 카드 두 장(뒷면과 바보 앞면)을 비스듬히 겹쳐 놓는다
    cw, ch = int(250 * S), int(432 * S)
    front = Image.open(os.path.join(HERE, "images/png_330x570/1_메이저_아르카나(22)/00_the_fool(바보).png")).convert("RGBA").resize((cw, ch), Image.LANCZOS)
    fm = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(fm).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=int(cw * 0.05), fill=255)
    front.putalpha(fm)
    back = card_back(cw, ch)
    for card, cx, cy, ang in ((back, W * 0.71, H * 0.54, 10), (front, W * 0.855, H * 0.47, -9)):
        sh = Image.new("RGBA", (cw + 120 * S, ch + 120 * S), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((60 * S, 70 * S, 60 * S + cw, 70 * S + ch), radius=int(cw * 0.05), fill=(0, 0, 0, 170))
        sh = sh.filter(ImageFilter.GaussianBlur(18 * S)).rotate(ang, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(sh, (int(cx - sh.width / 2), int(cy - sh.height / 2)))
        r = card.rotate(ang, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(FONT, 118 * S, index=0)
    f2 = ImageFont.truetype(FONT, 38 * S, index=0)
    f3 = ImageFont.truetype(FONT, 28 * S, index=0)
    d.text((78 * S, 205 * S), "오늘의 타로", font=f1, fill=(255, 255, 255, 255))
    d.line((82 * S, 360 * S, 330 * S, 360 * S), fill=GOLD + (255,), width=4 * S)
    d.text((80 * S, 392 * S), "카드를 눌러 한 장 뽑아 보세요", font=f2, fill=(240, 226, 196, 255))
    d.text((80 * S, 452 * S), "타로 카드 78장의 뜻과 키워드", font=f3, fill=(190, 178, 208, 255))
    d.text((80 * S, 560 * S), "tarot.carroty.com", font=f3, fill=GOLD + (255,))
    return im.convert("RGB").resize((1200, 630), Image.LANCZOS)


def fool(w, h):
    f = Image.open(os.path.join(HERE, "images/png_330x570/1_메이저_아르카나(22)/00_the_fool(바보).png")).convert("RGBA").resize((w, h), Image.LANCZOS)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(w * 0.05), fill=255)
    f.putalpha(m)
    return f


def put(im, card, cx, cy, ang, shadow=True):
    if shadow:
        pad = 80 * S
        sh = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 14 * S, pad + card.width, pad + card.height + 14 * S), radius=int(card.width * 0.05), fill=(0, 0, 0, 190))
        sh = sh.filter(ImageFilter.GaussianBlur(16 * S)).rotate(ang, resample=Image.BICUBIC, expand=True)
        im.alpha_composite(sh, (int(cx - sh.width / 2), int(cy - sh.height / 2)))
    r = card.rotate(ang, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))


def icon_base(ring_alpha=70):
    W = 1024 * S
    im = radial(W, W, W / 2, W / 2.1, W * 0.75, (122, 52, 104), (24, 8, 36)).convert("RGBA")
    ov = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    magic(ImageDraw.Draw(ov), W / 2, W / 2, W * 0.45, GOLD + (ring_alpha,), 4 * S)
    return Image.alpha_composite(im, ov), W


def icon_a():   # 카드 뒷면 한 장을 세워 놓은 모양
    im, W = icon_base(60)
    h = int(W * 0.66); w = int(h * 330 / 570)
    put(im, card_back(w, h), W / 2, W / 2, 0)
    return im.convert("RGB").resize((1024, 1024), Image.LANCZOS)


def icon_b():   # 카드 뒷면과 바보 앞면을 비스듬히 겹친 모양
    im, W = icon_base(55)
    h = int(W * 0.60); w = int(h * 330 / 570)
    put(im, card_back(w, h), W * 0.43, W * 0.52, -11)
    put(im, fool(w, h), W * 0.58, W * 0.49, 9)
    return im.convert("RGB").resize((1024, 1024), Image.LANCZOS)


def icon_c():   # 바보 카드를 가운데에 놓고 뒤에 금빛 후광
    im, W = icon_base(110)
    aura = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(aura).ellipse((W * 0.18, W * 0.18, W * 0.82, W * 0.82), fill=(255, 214, 140, 120))
    im = Image.alpha_composite(im, aura.filter(ImageFilter.GaussianBlur(70 * S)))
    h = int(W * 0.68); w = int(h * 330 / 570)
    put(im, fool(w, h), W / 2, W / 2, 0)
    return im.convert("RGB").resize((1024, 1024), Image.LANCZOS)


def _finish(im, gold_layer, W):
    glow = gold_layer.filter(ImageFilter.GaussianBlur(26 * S))
    im = Image.alpha_composite(Image.alpha_composite(im, glow), gold_layer)
    return im.convert("RGB").resize((1024, 1024), Image.LANCZOS)


def icon_moon():   # 단순한 굵은 초승달 + 작은 별 (카드 그림 없이 도형만)
    im, W = icon_base(0)
    m = Image.new("L", (W, W), 0)
    d = ImageDraw.Draw(m)
    R = W * 0.30
    d.ellipse((W * 0.46 - R, W * 0.5 - R, W * 0.46 + R, W * 0.5 + R), fill=255)
    d.ellipse((W * 0.46 - R * 0.80 + W * 0.15, W * 0.5 - R * 0.86, W * 0.46 + R * 0.80 + W * 0.15, W * 0.5 + R * 0.86), fill=0)
    g = Image.new("RGBA", (W, W), GOLD + (255,)); g.putalpha(m)
    star(ImageDraw.Draw(g), W * 0.70, W * 0.34, W * 0.075, GOLD + (255,))
    return _finish(im, g, W)


def icon_star():   # 단순한 굵은 8각 별 하나
    im, W = icon_base(0)
    g = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    star(d, W / 2, W / 2, W * 0.36, GOLD + (255,))
    d.ellipse((W / 2 - W * 0.05, W / 2 - W * 0.05, W / 2 + W * 0.05, W / 2 + W * 0.05), fill=(122, 52, 104, 255))
    return _finish(im, g, W)


def icon_lovers():   # 겹친 두 고리(연인) + 가운데 작은 별
    im, W = icon_base(0)
    g = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    R, w = W * 0.20, int(W * 0.026)
    for cx in (W * 0.5 - R * 0.62, W * 0.5 + R * 0.62):
        d.ellipse((cx - R, W / 2 - R, cx + R, W / 2 + R), outline=GOLD + (255,), width=w)
    star(d, W / 2, W / 2, W * 0.085, GOLD + (255,))
    return _finish(im, g, W)


if len(sys.argv) > 1 and sys.argv[1] == "simple":   # python3 make_og_images.py simple : 도형만 쓴 단순 아이콘 시안(icon-5 달, 6 별, 7 연인)
    for n, fn in ((5, icon_moon), (6, icon_star), (7, icon_lovers)):
        p = os.path.join(HERE, "assets/img/icon", f"icon-{n}.png")
        if os.path.exists(p):
            print("이미 있어 건너뜀:", p); continue
        fn().save(p); print("만듦:", p)
    sys.exit(0)

if len(sys.argv) > 1 and sys.argv[1] == "icons":   # python3 make_og_images.py icons : 카드가 들어간 아이콘 시안 3개(icon-2, 3, 4)
    for n, fn in ((2, icon_a), (3, icon_b), (4, icon_c)):
        p = os.path.join(HERE, "assets/img/icon", f"icon-{n}.png")
        if os.path.exists(p):
            print("이미 있어 건너뜀:", p); continue
        fn().save(p); print("만듦:", p)
    sys.exit(0)

for kind, im, name in (("icon", icon(), f"icon-{N}.png"), ("og", og(), f"og-{N}.png")):
    p = os.path.join(HERE, "assets/img", kind, name)
    if os.path.exists(p):
        print("이미 있어 건너뜀:", p); continue
    im.save(p)
    link = os.path.join(HERE, "assets/img", kind, f"{kind}.png")
    if os.path.islink(link) or not os.path.exists(link):
        if os.path.islink(link): os.remove(link)
        os.symlink(name, link)
    print("만듦:", p)
