import json, math
from shapely.geometry import shape
import os, base64
from clay_common import DATA, K, BASE, USE_PHOTOS, filters, icon

a = json.load(open("ADM1_med.json")); b = json.load(open("ADM2_med.json"))
reg = [shape(f["geometry"]) for f in a["features"] if f["properties"]["shapeName"] == "Aktobe Region"][0]
dists = [(f["properties"]["shapeName"], shape(f["geometry"])) for f in b["features"]]
dists = [(n, g) for n, g in dists if reg.buffer(0.01).contains(g.representative_point())]

k = math.cos(math.radians(48.25)); lon0, lat0, lon1, lat1 = reg.bounds
PAD = 40; S = (1000 - 2 * PAD) / ((lon1 - lon0) * k)
VW = 1000; VH = round(2 * PAD + (lat1 - lat0) * S)
def P(lon, lat): return (PAD + (lon - lon0) * k * S, PAD + (lat1 - lat) * S)
def path(g, tol=.01):
    g = g.simplify(tol, preserve_topology=True)
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    return "".join("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (P(*c) for c in p.exterior.coords)) + "Z" for p in polys)

TONES = ["#F7D9A6", "#F2C99A", "#F6E2B8", "#EFD0A8", "#F9E6C4"]
cols = {}
for n, g in sorted(dists, key=lambda t: -t[1].area):
    used = {cols[m] for m, h in dists if m in cols and g.buffer(0.02).intersects(h)}
    cols[n] = next(i for i in range(5) if i not in used)
district_svg = "".join(f'<path d="{path(g)}" fill="{TONES[cols[n]]}" stroke="#E8EDF8" stroke-width="7" stroke-linejoin="round" filter="url(#clayBig)"/>' for n, g in dists)
region_shadow = f'<path d="{path(reg)}" transform="translate(10,18)" fill="#2F3A5C" opacity=".18" filter="url(#blurS)"/>'

CREDIT = {"kobylandy": "Мейрамбек Амангелдіұлы / Google Maps", "eset-daribay": "Wild Ticket", "kyzyltam": "Wild Ticket"}
stops = []
for d in DATA:
    x, y = P(d["lon"], d["lat"])
    dd = {k2: v for k2, v in d.items()}
    dd["x"], dd["y"] = round(x, 1), round(y, 1)
    if USE_PHOTOS and os.path.exists(f"photos/{d['id']}.jpg"):
        dd["photo"] = "data:image/jpeg;base64," + base64.b64encode(open(f"photos/{d['id']}.jpg", "rb").read()).decode()
        dd["credit"] = CREDIT.get(d["id"], "открытые источники")
    stops.append(dd)
ax, ay = P(57.1669, 50.2839)
ICONS = {d["icon"]: icon(d["icon"]) for d in DATA}

html = open("app_template.html").read()
html = (html.replace("__FILTERS__", filters() + '<filter id="blurS"><feGaussianBlur stdDeviation="10"/></filter>')
        .replace("__VIEWBOX__", f"0 0 {VW} {VH}")
        .replace("__DISTRICTS__", region_shadow + district_svg)
        .replace("__DATA__", json.dumps(stops, ensure_ascii=False))
        .replace("__ICONS__", json.dumps(ICONS, ensure_ascii=False))
        .replace("__AKTOBE__", json.dumps([round(ax, 1), round(ay, 1)]))
        .replace("__BASE__", BASE))
OUT = os.environ.get("OUT", "tour.html")
if os.environ.get("STANDALONE") == "1":
    # полноценная HTML-страница для GitHub Pages
    cut = html.index("<svg width=\"0\"")
    head, body = html[:cut], html[cut:]
    reset = "<style>html{-webkit-text-size-adjust:100%}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>"
    html = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="description" content="Цифровая карта исторических памятников Актюбинского края">\n'
            + reset + "\n" + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
open(OUT, "w").write(html)
print("ok", VW, VH, len(html))
