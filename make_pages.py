#!/usr/bin/env python3
"""카드별 페이지(78장)와 78장 목록 페이지, 사이트맵을 만든다. 실행: python3 tarot/make_pages.py
- 입력: tarot/cards.json(make_cards.py가 만듦). 해석을 고쳤으면 make_cards.py를 먼저 실행한다.
- 출력: tarot/cards/index.html(목록), tarot/cards/<영어-이름>/index.html(카드별), tarot/cards/thumbs/<영어-이름>.jpg(작은 그림), tarot/cards/img/<영어-이름>.jpg(가벼운 큰 그림),
  tarot/cards/cards.css, tarot/sitemap.xml, tarot/robots.txt
- 주소: https://tarot.carroty.com/cards/the-fool/ 처럼 영어 이름(소문자, 공백은 -)을 쓴다.
- 카드 페이지에는 해석, 연애운, 재물운 세 칸이 있다(연애운과 재물운은 topics_data.py). 일/조언 같은 글을 더할 때는 아래 card_page()에 칸을 추가한다."""
import html, json, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://tarot.carroty.com"
SITE = "오늘의 타로"
GROUP_ID = {"메이저 아르카나": "major", "완드": "wands", "컵": "cups", "소드": "swords", "펜타클": "pentacles"}
GROUP_LABEL = {"major": "메이저 아르카나", "wands": "완드", "cups": "컵", "swords": "소드", "pentacles": "펜타클"}
e = html.escape


def slug(en):
    return re.sub(r"[^a-z0-9]+", "-", en.lower()).strip("-")


cards = json.load(open(os.path.join(HERE, "cards.json"), encoding="utf-8"))
for i, c in enumerate(cards):
    c["slug"] = slug(c["en"])
    c["gid"] = GROUP_ID[c["group"]]
    c["idx"] = i
by_group = {}
for c in cards:
    by_group.setdefault(c["gid"], []).append(c)
for g in by_group.values():
    for n, c in enumerate(g):
        c["n"] = n   # 메이저는 0~21번
assert len({c["slug"] for c in cards}) == 78

OUT = os.path.join(HERE, "cards")
os.makedirs(os.path.join(OUT, "thumbs"), exist_ok=True)

# 작은 그림(목록과 같은 분류 칸에 쓴다)
for c in cards:
    t = os.path.join(OUT, "thumbs", c["slug"] + ".jpg")
    if not os.path.exists(t):
        Image.open(os.path.join(HERE, c["src"])).convert("RGB").resize((110, 190), Image.LANCZOS).save(t, "JPEG", quality=78)

# 가벼운 큰 그림(330x570 JPEG, 원본 PNG의 5분의 1 정도). 첫 화면 뽑기와 카드 페이지가 쓴다(폰에서 빨리 뜨게). OG 이미지는 원본 PNG를 그대로 쓴다.
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
for c in cards:
    t = os.path.join(OUT, "img", c["slug"] + ".jpg")
    if not os.path.exists(t):
        Image.open(os.path.join(HERE, c["src"])).convert("RGB").resize((330, 570), Image.LANCZOS).save(t, "JPEG", quality=84, optimize=True)

CSS = """/* 카드 페이지와 목록 페이지가 같이 쓰는 스타일. 어두운 보랏빛과 금색(오늘의 타로 화면과 같은 색) */
:root { --bg: #08050f; --ink: #e8ece9; --mut: #b4adc0; --gold: #e4c27a; --pl: #3a2d4a; --chip: #3a2433; --chip-fg: #f0d3e4; --accent: #c0689a; color-scheme: dark; }
* { box-sizing: border-box; }
html { overflow-x: clip; }
body { margin: 0; background: radial-gradient(100% 60% at 50% 8%, #3b1840 0%, #190c26 55%, var(--bg) 100%) fixed, var(--bg); color: var(--ink); font: 16px/1.65 -apple-system, "Malgun Gothic", "Noto Sans KR", system-ui, sans-serif; word-break: keep-all; overflow-wrap: break-word; }
main { max-width: 640px; margin: 0 auto; padding: 16px max(16px, env(safe-area-inset-right, 0px)) 48px max(16px, env(safe-area-inset-left, 0px)); }
a { color: var(--gold); text-decoration: none; }
a:hover, a:focus-visible { text-decoration: underline; }
.top { display: flex; justify-content: space-between; align-items: center; gap: 12px; font-size: 13px; color: var(--mut); }
.crumb { margin: 0; }
.crumb i { font-style: normal; opacity: .6; margin: 0 5px; }
h1 { margin: 14px 0 0; font-size: 28px; line-height: 1.25; text-wrap: balance; text-shadow: 0 2px 14px rgba(0, 0, 0, .6); }
h1 small { display: block; margin-top: 2px; font-size: 16px; font-weight: 400; color: var(--mut); }
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 12px 0 0; padding: 0; list-style: none; }
.chips li { padding: 1px 11px; border-radius: 999px; background: var(--chip); color: var(--chip-fg); font-size: 13px; }
.chips li.g { background: transparent; border: 1px solid var(--pl); color: var(--mut); }
.hero { position: relative; display: flex; justify-content: center; margin: 22px 0 18px; }
.hero::before { content: ""; position: absolute; left: 50%; top: 50%; width: min(90vw, 420px); aspect-ratio: 1; transform: translate(-50%, -50%); background: radial-gradient(circle, rgba(228, 194, 122, .28), transparent 65%); pointer-events: none; }
.hero img { position: relative; width: min(58vw, 240px); height: auto; border-radius: 10px; box-shadow: 0 10px 34px rgba(0, 0, 0, .6); }
section { margin: 22px 0 0; }
h2 { margin: 0 0 6px; font-size: 18px; color: var(--gold); }
section p { margin: 0; }
.cta { display: block; margin: 22px 0 0; padding: 13px 16px; text-align: center; border-radius: 999px; background: var(--accent); color: #1a0f16; font-weight: 700; }
.cta:hover { text-decoration: none; filter: brightness(1.08); }
.pn { display: flex; justify-content: space-between; gap: 12px; margin: 26px 0 0; padding-top: 14px; border-top: 1px solid var(--pl); font-size: 14px; }
.pn div { min-width: 0; }
.pn small { display: block; color: var(--mut); font-size: 12px; }
.pn .nx { text-align: right; }
.row { display: grid; grid-template-columns: repeat(auto-fill, minmax(76px, 1fr)); gap: 12px 10px; margin: 10px 0 0; padding: 0; list-style: none; }
.row a { display: block; text-align: center; font-size: 13px; color: var(--ink); }
.row img { display: block; width: 100%; max-width: 84px; height: auto; margin: 0 auto 4px; border-radius: 6px; box-shadow: 0 4px 14px rgba(0, 0, 0, .5); }
.tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 0; padding: 0; list-style: none; }
.tabs a { display: inline-block; padding: 3px 13px; border-radius: 999px; border: 1px solid var(--pl); font-size: 14px; color: var(--ink); }
.lead { margin: 10px 0 0; color: var(--mut); }
.note { margin: 28px 0 0; font-size: 13px; color: var(--mut); }
footer { margin: 28px 0 0; font-size: 12px; color: var(--mut); text-align: center; }
"""
open(os.path.join(OUT, "cards.css"), "w", encoding="utf-8").write(CSS)


def head(title, desc, canon, image=None, extra=""):
    t = ""
    if image:
        t = f'<meta property="og:image" content="{e(image)}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{e(image)}">\n'
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canon)}">
{t}<meta name="theme-color" content="#190c26">
<link rel="stylesheet" href="/cards/cards.css?v=1">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/icon/app-icon-180.png">
{extra}</head>
<body>
<main>
"""


FOOT = """<footer>재미와 마음 정리를 위한 참고로만 봐 주세요.</footer>
</main>
<div data-counter="tarot" data-url="https://app.carroty.com/count" hidden></div>
<script src="https://app.carroty.com/counter.js?v=1"></script>
</body>
</html>
"""


def img_url(c):
    return BASE + "/" + "/".join(__import__("urllib.parse", fromlist=["quote"]).quote(p) for p in c["src"].split("/"))


def card_page(c):
    gl = GROUP_LABEL[c["gid"]]
    g = by_group[c["gid"]]
    prev_c = cards[c["idx"] - 1] if c["idx"] > 0 else None
    next_c = cards[c["idx"] + 1] if c["idx"] < 77 else None
    mid = f' · {c["n"]}번' if c["gid"] == "major" else ""
    title = f'{c["ko"]}({c["en"]}) 카드의 의미, 연애운, 재물운 | {SITE}'
    desc = f'{c["ko"]}({c["en"]}) 타로 카드의 의미와 연애운, 재물운. 키워드: {", ".join(c["kw"])}. {c["text"]}'
    canon = f'{BASE}/cards/{c["slug"]}/'
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": f'{c["ko"]}({c["en"]}) 카드의 의미',
                     "description": c["text"], "image": img_url(c), "inLanguage": "ko", "mainEntityOfPage": canon}, ensure_ascii=False)
    h = head(title, desc, canon, img_url(c), f'<script type="application/ld+json">{ld}</script>\n')
    h += f"""<div class="top"><p class="crumb"><a href="/">타로</a><i>›</i><a href="/cards/">카드 모음</a><i>›</i><a href="/cards/#{c["gid"]}">{e(gl)}</a><i>›</i>{e(c["ko"])}</p></div>
<h1>{e(c["ko"])} <small>{e(c["en"])}</small></h1>
<ul class="chips"><li class="g">{e(gl)}{mid}</li>{"".join(f"<li>{e(k)}</li>" for k in c["kw"])}</ul>
<div class="hero"><img src="/cards/img/{c["slug"]}.jpg" alt="{e(c["ko"])}({e(c["en"])}) 타로 카드" width="330" height="570"></div>
<section><h2>이 카드가 나왔다면</h2><p>{e(c["text"])}</p></section>
<section><h2>연애운</h2><p>{e(c["love"])}</p></section>
<section><h2>재물운</h2><p>{e(c["money"])}</p></section>
<section><h2>연애운에서 상대의 마음</h2><p>{e(c["love_other"])}</p></section>
<section><h2>재물운에서 걸림돌</h2><p>{e(c["money_block"])}</p></section>
<a class="cta" href="/">나도 한 장 뽑아 보기</a>
<nav class="pn" aria-label="이전과 다음 카드"><div>{f'<small>이전</small><a href="/cards/{prev_c["slug"]}/">{e(prev_c["ko"])} ‹</a>' if prev_c else ''}</div><div class="nx">{f'<small>다음</small><a href="/cards/{next_c["slug"]}/">› {e(next_c["ko"])}</a>' if next_c else ''}</div></nav>
<section><h2>같은 분류의 카드</h2><ul class="row">
"""
    # 같은 분류에서 바로 앞뒤 카드 4장(맨 끝이면 처음으로 이어서)
    near = [g[(c["n"] + d) % len(g)] for d in (-2, -1, 1, 2)]
    for o in near:
        h += f'<li><a href="/cards/{o["slug"]}/"><img src="/cards/thumbs/{o["slug"]}.jpg" alt="" width="110" height="190" loading="lazy">{e(o["ko"])}</a></li>\n'
    h += "</ul></section>\n" + FOOT
    return h


def hub_page():
    title = f"타로 카드 78장 모음, 카드별 의미와 키워드 | {SITE}"
    desc = "타로 카드 78장(메이저 아르카나 22장, 마이너 아르카나 56장)의 의미와 키워드를 카드별로 볼 수 있습니다."
    canon = BASE + "/cards/"
    h = head(title, desc, canon)
    h += f"""<div class="top"><p class="crumb"><a href="/">타로</a><i>›</i>카드 모음</p></div>
<h1>타로 카드 78장 모음 <small>뜻과 키워드를 한눈에</small></h1>
<p class="lead">메이저 아르카나 22장과 마이너 아르카나 56장의 의미를 카드별로 볼 수 있습니다. 궁금한 카드를 눌러 보세요.</p>
<a class="cta" href="/">오늘의 카드 뽑아 보기</a>
<ul class="tabs">{"".join(f'<li><a href="#{k}">{GROUP_LABEL[k]} {len(by_group[k])}</a></li>' for k in GROUP_LABEL)}</ul>
"""
    for k in GROUP_LABEL:
        h += f'<section id="{k}"><h2>{GROUP_LABEL[k]} ({len(by_group[k])}장)</h2><ul class="row">\n'
        for c in by_group[k]:
            h += f'<li><a href="/cards/{c["slug"]}/"><img src="/cards/thumbs/{c["slug"]}.jpg" alt="{e(c["ko"])} 카드" width="110" height="190" loading="lazy">{e(c["ko"])}</a></li>\n'
        h += "</ul></section>\n"
    return h + FOOT


open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(hub_page())
for c in cards:
    d = os.path.join(OUT, c["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(card_page(c))

urls = [BASE + "/", BASE + "/cards/"] + [f"{BASE}/cards/{c['slug']}/" for c in cards]
open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
print("카드 페이지", len(cards), "장, 목록 1장, 주소", len(urls), "개")
