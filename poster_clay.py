import json, math, random, qrcode
from shapely.geometry import shape, Point, box
import os
from clay_common import DATA, K, BASE, USE_PHOTOS, filters, icon

W, H = 4200, 2970  # 0.1 mm, A3 landscape
C = dict(bg="#E6ECF8", card="#F5F8FF", mapbg="#DCE4F4", neigh="#CFD8EC", ink="#2F3A5C", muted="#67718F",
         tones=["#F7D9A6", "#F2C99A", "#F6E2B8", "#EFD0A8", "#F9E6C4"], label="#B07A3E", grass="#9CC7A0")

a = json.load(open("ADM1_med.json")); b = json.load(open("ADM2_med.json"))
regions = {f["properties"]["shapeName"]: shape(f["geometry"]) for f in a["features"]}
reg = regions["Aktobe Region"]
dists = [(f["properties"]["shapeName"], shape(f["geometry"])) for f in b["features"]]
dists = [(n, g) for n, g in dists if reg.buffer(0.01).contains(g.representative_point())]
RU = {"Alginskiy": "Алгинский", "Aqtobe": "", "Aytekebiyskiy": "Айтекебийский", "Bayganinskiy": "Байганинский",
      "Irgizskiy": "Иргизский", "Kargalinskiy": "Каргалинский", "Khobdinskiy": "Кобдинский", "Khromtauskiy": "Хромтауский",
      "Martukskiy": "Мартукский", "Mugalzharskiy": "Мугалжарский", "Shalkarskiy": "Шалкарский", "Temirskiy": "Темирский", "Uilskiy": "Уилский"}
DLP = {"Martukskiy": (56.78, 50.66), "Kargalinskiy": (57.8, 50.78), "Khromtauskiy": (59.5, 49.83), "Alginskiy": (56.9, 49.8),
       "Khobdinskiy": (55.0, 50.25), "Uilskiy": (54.75, 48.85), "Temirskiy": (56.3, 49.0), "Mugalzharskiy": (58.0, 48.3),
       "Bayganinskiy": (55.8, 47.6), "Shalkarskiy": (59.3, 46.9), "Irgizskiy": (61.5, 48.7), "Aytekebiyskiy": (61.0, 50.6)}
LAY = {"abat-baitak": (-20, 250, -520, 300), "kobylandy": (150, -5, -280, 70), "eset-kokiuly": (240, 70, 140, 150),
       "khan-molasy": (0, -10, -360, 70), "kotibar": (0, -14, 90, 20), "eset-daribay": (0, -14, 90, 20), "kyzyltam": (215, -30, 120, 60)}

k = math.cos(math.radians(48.25)); lon0, lat1 = reg.bounds[0], reg.bounds[3]
MX, MY, S = 180, 540, 350.0
def P(lon, lat): return (MX + (lon - lon0) * k * S, MY + (lat1 - lat) * S)
def path(g, tol=0.008):
    g = g.simplify(tol, preserve_topology=True)
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    return "".join("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (P(*c) for c in ring.coords)) + "Z"
                   for p in polys for ring in [p.exterior] + list(p.interiors))
mapx0, mapy0, mapx1, mapy1 = 110, 410, 2700, 2840
def inv(x, y): return (lon0 + (x - MX) / (k * S), lat1 - (y - MY) / S)
lw, lt = inv(mapx0, mapy0); le, lb = inv(mapx1, mapy1); win = box(lw, lb, le, lt)
cols = {}
for n, g in sorted(dists, key=lambda t: -t[1].area):
    used = {cols[m] for m, h in dists if m in cols and g.buffer(0.02).intersects(h)}
    cols[n] = next(i for i in range(5) if i not in used)

def qr_path(url, size):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0); q.add_data(url); q.make()
    m = q.get_matrix(); n = len(m); c = size / n
    return f'<path d="{"".join(f"M{x*c:.2f},{y*c:.2f}h{c:.2f}v{c:.2f}h-{c:.2f}z" for y, r in enumerate(m) for x, v in enumerate(r) if v)}" fill="{C["ink"]}" shape-rendering="crispEdges"/>'

def clay_rect(x, y, w, h, r, fill, big=True):
    return f'<g filter="url(#dropL)"><rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r}" fill="{fill}" filter="url(#{"clayBig" if big else "clay"})"/></g>'

out = []; A = out.append
A(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="420mm" height="297mm" font-family="Nunito">
<defs>{filters()}
<filter id="dropL" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="14" dy="24" stdDeviation="22" flood-color="#5A6A9A" flood-opacity=".30"/></filter>
<filter id="blurS"><feGaussianBlur stdDeviation="16"/></filter>
<clipPath id="mapclip"><rect x="{mapx0}" y="{mapy0}" width="{mapx1-mapx0}" height="{mapy1-mapy0}" rx="70"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="{C['bg']}"/>''')

# soft background blobs
for cx, cy, r, col, op in [(3900, 160, 380, K["teal"], .16), (300, 2900, 420, K["terra"], .12), (2600, 120, 260, K["gold"], .18)]:
    A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}" filter="url(#blurS)"/>')

# ---------- map slab
A(clay_rect(mapx0, mapy0, mapx1 - mapx0, mapy1 - mapy0, 70, C["mapbg"]))
A('<g clip-path="url(#mapclip)">')
for name, g in regions.items():
    if name == "Aktobe Region": continue
    gi = g.intersection(win.buffer(1))
    if not gi.is_empty: A(f'<path d="{path(gi, .02)}" fill="{C["neigh"]}" stroke="{C["mapbg"]}" stroke-width="8"/>')
A('</g>')
for t, lo, la in [("РОССИЯ · Оренбургская обл.", 57.2, 51.55), ("Костанайская обл.", 63.6, 50.9), ("Кызылординская обл.", 63.2, 46.5),
                  ("Атырауская обл.", 54.4, 46.9)]:
    x, y = P(lo, la)
    A(f'<text x="{x:.0f}" y="{y:.0f}" font-weight="800" font-size="32" letter-spacing="6" fill="{C["muted"]}" fill-opacity=".75" text-anchor="middle">{t.upper()}</text>')

A(f'<path d="{path(reg, .006)}" transform="translate(20,34)" fill="#3A4A7A" opacity=".22" filter="url(#blurS)"/>')
for n, g in dists:
    A(f'<path d="{path(g, .006)}" fill="{C["tones"][cols[n]]}" stroke="{C["mapbg"]}" stroke-width="12" stroke-linejoin="round" filter="url(#clayBig)"/>')

random.seed(7)
avoid = [P(d["lon"], d["lat"]) for d in DATA] + [P(57.1669, 50.2839)]
placed = tries = 0
while placed < 60 and tries < 6000:
    tries += 1
    lon = random.uniform(reg.bounds[0], reg.bounds[2]); lat = random.uniform(reg.bounds[1], reg.bounds[3])
    if not reg.buffer(-0.15).contains(Point(lon, lat)): continue
    x, y = P(lon, lat)
    if any(math.hypot(x - ax, y - ay) < 320 for ax, ay in avoid): continue
    placed += 1
    if placed % 5 == 0:
        A(f'<g transform="translate({x:.0f},{y:.0f})"><rect x="-3" y="-30" width="6" height="30" rx="3" fill="{C["grass"]}"/>'
          f'<path d="M-12 -30 C-14 -52 -4 -50 0 -56 C4 -50 14 -52 12 -30 C8 -22 -8 -22 -12 -30Z" fill="{K["terra"]}" filter="url(#claySm)"/></g>')
    else:
        A(f'<g transform="translate({x:.0f},{y:.0f})" fill="{C["grass"]}"><ellipse cx="-10" cy="-10" rx="7" ry="14" transform="rotate(-20 -10 -10)"/><ellipse cx="0" cy="-16" rx="7" ry="18"/><ellipse cx="10" cy="-10" rx="7" ry="14" transform="rotate(20 10 -10)"/></g>')

for n, g in dists:
    if not RU[n]: continue
    x, y = P(*DLP[n])
    A(f'<text x="{x:.0f}" y="{y:.0f}" font-weight="800" font-size="31" letter-spacing="5" fill="{C["label"]}" fill-opacity=".85" text-anchor="middle">{RU[n].upper()}</text>')

ax, ay = P(57.1669, 50.2839)
A(f'<rect x="{ax-18}" y="{ay-18}" width="36" height="36" rx="8" transform="rotate(45 {ax} {ay})" fill="{C["ink"]}" filter="url(#claySm)"/>'
  f'<text x="{ax-30}" y="{ay-30}" font-weight="900" font-size="46" fill="{C["ink"]}" text-anchor="end">Актобе</text>')

for d in DATA:
    x, y = P(d["lon"], d["lat"]); ix0, iy0, tx0, ty0 = LAY[d["id"]]
    col = K["terra"] if d["kind"] == "red" else K["teal"]
    if math.hypot(ix0, iy0) > 60:
        A(f'<path d="M{x:.0f},{y:.0f} L{x+ix0:.0f},{y+iy0-8:.0f}" stroke="{C["ink"]}" stroke-width="6" stroke-dasharray="1 14" stroke-linecap="round" opacity=".6"/>')
    dash = '' if d["exact"] else 'stroke="#fff" stroke-width="6" stroke-dasharray="9 7"'
    A(f'<ellipse cx="{x+4:.0f}" cy="{y+18:.0f}" rx="18" ry="6" fill="{C["ink"]}" opacity=".2"/><circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="{col}" filter="url(#claySm)" {dash}/>')
    s = 1.12
    A(f'<g transform="translate({x+ix0-100*s:.0f},{y+iy0-200*s:.0f}) scale({s})" filter="url(#drop)">{icon(d["icon"])}</g>')
    tx, ty = x + tx0, y + ty0
    label = d["short"] + ("" if d["exact"] else " ≈"); tw = 104 + len(label) * 29
    A(f'<g transform="translate({tx:.0f},{ty:.0f})"><g filter="url(#drop)"><rect x="0" y="-46" width="{tw}" height="92" rx="46" fill="#FFFFFF" filter="url(#clay)"/></g>'
      f'<circle cx="46" cy="0" r="32" fill="{col}" filter="url(#claySm)"/><text x="46" y="14" font-weight="900" font-size="40" fill="{"#fff" if d["kind"]=="red" else "#123A47"}" text-anchor="middle">{d["n"]}</text>'
      f'<text x="92" y="17" font-weight="900" font-size="48" fill="{C["ink"]}">{label}</text></g>')

# compass + scale
cx, cy = 2470, 2060
A(f'<g transform="translate({cx},{cy})"><g filter="url(#drop)"><circle r="92" fill="{C["card"]}" filter="url(#clay)"/></g>'
  f'<path d="M0 -70 L20 0 L0 70 L-20 0Z" fill="{C["neigh"]}"/><path d="M0 -70 L20 0 L-20 0Z" fill="{K["terra"]}" filter="url(#claySm)"/>'
  f'<text y="-110" font-weight="900" font-size="42" fill="{C["ink"]}" text-anchor="middle">С</text></g>')
km100 = 100 / 111.32 * S; sx0, sy0 = cx - km100 / 2, 2290
A(f'<g font-weight="800" font-size="30" fill="{C["ink"]}"><rect x="{sx0:.0f}" y="{sy0}" width="{km100:.0f}" height="18" rx="9" fill="{C["card"]}" filter="url(#claySm)"/>'
  f'<rect x="{sx0:.0f}" y="{sy0}" width="{km100/2:.0f}" height="18" rx="9" fill="{C["ink"]}"/>'
  f'<text x="{sx0:.0f}" y="{sy0-16}">0</text><text x="{sx0+km100:.0f}" y="{sy0-16}" text-anchor="end">100 км</text></g>')

# legend (categories from the research paper)
lx, ly = 170, 2330
A(clay_rect(lx, ly, 1000, 460, 44, C["card"]))
rows = [("red", K["terra"], "красный — мавзолеи и некрополи", 4), ("blue", K["teal"], "синий — мемориальные комплексы", 3),
        ("green", K["green"], "зелёный — археологические объекты", 0), ("yellow", "#F2D46B", "жёлтый — памятники и сооружения", 0)]
A(f'<text x="{lx+44}" y="{ly+74}" font-weight="900" font-size="30" letter-spacing="6" fill="{C["muted"]}">УСЛОВНЫЕ ОБОЗНАЧЕНИЯ</text>')
for i, (_, colr, t, n) in enumerate(rows):
    y = ly + 136 + i * 64
    A(f'<circle cx="{lx+64}" cy="{y-10}" r="20" fill="{colr}" filter="url(#claySm)"/>'
      f'<text x="{lx+104}" y="{y}" font-weight="700" font-size="32" fill="{C["ink"]}" fill-opacity="{1 if n else .5}">{t}{"" if n else " · пока нет"}</text>')
y = ly + 136 + 4 * 64
A(f'<circle cx="{lx+64}" cy="{y-10}" r="18" fill="none" stroke="{C["ink"]}" stroke-width="5" stroke-dasharray="8 6"/><text x="{lx+104}" y="{y}" font-weight="700" font-size="32" fill="{C["ink"]}">≈ место указано примерно</text>')

# title
A(f'''<text x="130" y="178" font-weight="900" font-size="34" letter-spacing="8" fill="{K['terraD']}">АҚТӨБЕ ӨҢІРІ · ЦИФРОВАЯ КАРТА</text>
<text x="124" y="278" font-weight="900" font-size="92" fill="{C['ink']}">Исторические памятники</text>
<text x="124" y="378" font-weight="900" font-size="92" fill="{C['ink']}">Актюбинского края</text>''')

# right column: QR cards
colx = 2790; colw = W - colx - 110
A(f'''<text x="{colx}" y="178" font-weight="900" font-size="34" letter-spacing="8" fill="{K['tealD']}">QR-ЭКСКУРСИЯ</text>
<text x="{colx}" y="268" font-weight="900" font-size="66" fill="{C['ink']}">Наведи камеру на QR</text>
<text x="{colx}" y="334" font-weight="600" font-size="35" fill="{C['muted']}">Откроется метка: фото, район, период, справка,</text>
<text x="{colx}" y="380" font-weight="600" font-size="35" fill="{C['muted']}">координаты и ссылка на подробности</text>''')
cw, ch, gap = (colw - 44) / 2, 548, 44
cards = [dict(n=0, full="Весь тур: 7 памятников", l1="Карта и маршрут", l2="начни отсюда", url=BASE, kind="gold")] + \
        [dict(n=d["n"], full=d["name"], l1=d["district"], l2=d["period"], url=BASE + "#" + d["id"], kind=d["kind"], icon=d["icon"], id=d["id"]) for d in DATA]
def wrap(t, n):
    L, cur = [], ""
    for w in t.split():
        if len(cur + " " + w) > n and cur: L.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return L + [cur]
for i, c in enumerate(cards):
    r, q = divmod(i, 2); x = colx + q * (cw + gap); y = 440 + r * (ch + 44)
    col = {"red": K["terra"], "blue": K["teal"], "gold": K["gold"]}[c["kind"]]
    A(clay_rect(x, y, cw, ch, 48, C["card"]))
    A(f'<g transform="translate({x:.0f},{y:.0f})">')
    qs = 262; qx, qy = cw - qs - 44, 44
    A(f'<rect x="{qx-18:.0f}" y="{qy-18}" width="{qs+36}" height="{qs+36}" rx="26" fill="#fff" filter="url(#claySm)"/><g transform="translate({qx:.0f},{qy})">{qr_path(c["url"], qs)}</g>')
    if c["n"] and not USE_PHOTOS:
        A(f'<g transform="translate(20,112) scale(.8)" filter="url(#drop)">{icon(c["icon"])}</g>')
    elif c["n"]:
        import base64
        b64 = base64.b64encode(open(f"photos/{c['id']}.jpg", "rb").read()).decode()
        A(f'<clipPath id="ph{i}"><rect x="26" y="26" width="270" height="306" rx="30"/></clipPath>'
          f'<g filter="url(#drop)"><rect x="26" y="26" width="270" height="306" rx="30" fill="#fff"/></g>'
          f'<image href="data:image/jpeg;base64,{b64}" x="26" y="26" width="270" height="306" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph{i})"/>'
          f'<rect x="26" y="26" width="270" height="306" rx="30" fill="none" stroke="#fff" stroke-width="8"/>')
    else:
        A(f'<g transform="translate(40,120)">' + "".join(f'<circle cx="{(j%3)*52+26}" cy="{(j//3)*52+26}" r="20" fill="{[K["terra"],K["teal"]][DATA[j]["kind"]=="blue"]}" filter="url(#claySm)"/>' for j in range(7)) + '</g>')
    A(f'<circle cx="62" cy="62" r="38" fill="{col}" filter="url(#claySm)"/><text x="62" y="78" font-weight="900" font-size="{44 if c["n"] else 40}" fill="{"#fff" if c["kind"]=="red" else "#123A47"}" text-anchor="middle">{c["n"] or "★"}</text>')
    L = wrap(c["full"], 24); ty = 380
    for j, line in enumerate(L):
        A(f'<text x="40" y="{ty + j*46}" font-weight="900" font-size="40" fill="{C["ink"]}">{line}</text>')
    my = ty + len(L) * 46 + 4
    A(f'<text x="40" y="{my}" font-weight="700" font-size="30" fill="{C["muted"]}">{c["l1"]}</text><text x="40" y="{my+38}" font-weight="700" font-size="30" fill="{C["muted"]}">{c["l2"]}</text></g>')

PHOTO_NOTE = 'Фото: Google Maps (Мейрамбек Амангелдіұлы), Wild Ticket, открытые источники; на карте — иллюстрации.' if USE_PHOTOS else 'Изображения памятников — иллюстрации.'
A(f'<text x="130" y="{H-58}" font-weight="600" font-size="26" fill="{C["muted"]}">По исследовательской работе «Цифровая карта исторических памятников Актюбинского края». Координаты — Visit Aktobe. Границы — geoBoundaries (CC BY 4.0). {PHOTO_NOTE}</text>')
A('</svg>')
open(os.environ.get("OUT", "poster_clay.html"), "w").write('<!doctype html><meta charset="utf-8"><style>html,body{margin:0}svg{display:block}</style>' + "\n".join(out))
print("ok")
