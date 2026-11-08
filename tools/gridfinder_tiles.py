#!/usr/bin/env python3
"""Cut gridfinder (Arderne et al. 2020, predicted MV/HV network) into 1°x1° static tiles for the browser.

  ogr2ogr -f GeoJSONSeq -simplify 0.002 /vsistdout/ grid.gpkg | python3 tools/gridfinder_tiles.py data/gf 0.002

Tile file data/gf/{floor(lat)}_{floor(lon)}.json = {"q":quantum_deg,"o":[lat0,lon0],"l":[[x0,y0,dx1,dy1,...],...]}
x = round((lon-lon0)/q), y = round((lat-lat0)/q); later vertices are deltas. Also writes data/gf/index.json (tile list)."""
import sys, json, os, math
out, q = sys.argv[1], float(sys.argv[2])
os.makedirs(out, exist_ok=True)
tiles = {}
def key(lon, lat): return (math.floor(lat), math.floor(lon))
def add(k, pts):
    if len(pts) < 2: return
    lat0, lon0 = k
    xy = []
    for lon, lat in pts:
        x, y = round((lon - lon0) / q), round((lat - lat0) / q)
        if xy and xy[-1] == (x, y): continue
        xy.append((x, y))
    if len(xy) < 2: return
    flat = [xy[0][0], xy[0][1]]
    for (a, b), (c, d) in zip(xy, xy[1:]): flat += [c - a, d - b]
    tiles.setdefault(k, []).append(flat)
n = 0
for line in sys.stdin:
    line = line.strip().lstrip("\x1e")
    if not line: continue
    g = json.loads(line).get("geometry") or {}
    parts = [g["coordinates"]] if g.get("type") == "LineString" else g.get("coordinates", []) if g.get("type") == "MultiLineString" else []
    for coords in parts:
        cur, ck = [], None
        for lon, lat in coords:
            k = key(lon, lat)
            if ck is None: ck = k
            if k != ck:
                cur.append((lon, lat)); add(ck, cur); cur, ck = [cur[-2] if len(cur) > 1 else (lon, lat)], k
            cur.append((lon, lat))
        add(ck, cur)
    n += 1
    if n % 500000 == 0: print(n, "features,", len(tiles), "tiles", file=sys.stderr)
total = 0
for (la, lo), ls in tiles.items():
    s = json.dumps({"q": q, "o": [la, lo], "l": ls}, separators=(",", ":"))
    open(os.path.join(out, f"{la}_{lo}.json"), "w").write(s); total += len(s)
json.dump(sorted(f"{la}_{lo}" for la, lo in tiles), open(os.path.join(out, "index.json"), "w"), separators=(",", ":"))
print(f"{n} features -> {len(tiles)} tiles, {total/1e6:.1f} MB", file=sys.stderr)
