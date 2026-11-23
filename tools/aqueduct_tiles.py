#!/usr/bin/env python3
"""Rasterise WRI Aqueduct 4.0 (baseline annual + future annual, CC-BY 4.0) into small static tiles.

Grid 0.05 deg; one JSON per 5x5 deg tile in data/aq/{lat}_{lon}.json (SW corner), land tiles only:
  {"f":[field names], "u":[[values per distinct Aqueduct unit]], "r":[run-length pairs: unit index (-1 = no data), count]}
Rows run north to south, 100 x 100 cells per tile.
Usage: python3 tools/aqueduct_tiles.py <extracted dir> [--probe]"""
import sys, os, json, glob
import numpy as np, pyogrio, geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin

src = sys.argv[1]; probe = '--probe' in sys.argv
gdbs = glob.glob(os.path.join(src, '**', '*.gdb'), recursive=True)
print('gdb:', gdbs)
gdb = gdbs[0]
layers = [l[0] for l in pyogrio.list_layers(gdb)]
print('layers:', layers)
base_l = next(l for l in layers if 'baseline' in l.lower() and 'annual' in l.lower())
fut_l = next((l for l in layers if 'future' in l.lower() and 'annual' in l.lower()), None)
info = pyogrio.read_info(gdb, layer=base_l); cols = list(info['fields'])
print('baseline fields', len(cols), cols[:60])
if fut_l:
    fcols = list(pyogrio.read_info(gdb, layer=fut_l)['fields']); print('future fields', len(fcols), fcols[:80])
if probe: sys.exit(0)

IND = ['bws', 'bwd', 'iav', 'sev', 'gtd', 'drr', 'rfr', 'cfr', 'ucw']
want = ['pfaf_id'] + [f'{i}_cat' for i in IND] + ['bws_raw', 'gtd_raw', 'w_awr_def_tot_cat']
want = [c for c in want if c in cols]
g = gpd.read_file(gdb, layer=base_l, columns=want, engine='pyogrio')
print('baseline rows', len(g)); print(g.drop(columns='geometry').head(3).to_string())
fut = None; FUT = []
if fut_l:
    FUT = [c for c in ['bau30_ws_x_c', 'bau50_ws_x_c', 'opt50_ws_x_c', 'pes50_ws_x_c', 'bau30_ws_x_r', 'bau50_ws_x_r'] if c in fcols]
    fut = pyogrio.read_dataframe(gdb, layer=fut_l, columns=['pfaf_id'] + FUT, read_geometry=False).drop_duplicates('pfaf_id').set_index('pfaf_id')
    print('future rows', len(fut), FUT)

RES = 0.05; W, H = int(360 / RES), int(180 / RES)
tr = from_origin(-180, 90, RES, RES)
g = g[g.geometry.notna() & ~g.geometry.is_empty].reset_index(drop=True)
shapes = [(geom, i + 1) for i, geom in enumerate(g.geometry)]
r1 = rasterize(shapes, out_shape=(H, W), transform=tr, fill=0, dtype='int32')
r2 = rasterize(shapes, out_shape=(H, W), transform=tr, fill=0, dtype='int32', all_touched=True)
ras = np.where(r1 > 0, r1, r2); del r1, r2
print('cells with data', int((ras > 0).sum()))

def num(v, nd=None):
    try:
        v = float(v)
    except (TypeError, ValueError): return nd
    if v != v or v <= -9000: return nd
    return v
fields = [c for c in want if c != 'pfaf_id'] + FUT
attrs = g.drop(columns='geometry')
def rec(i):
    row = attrs.iloc[i]; out = []
    for c in fields:
        if c in FUT:
            v = None
            if fut is not None and 'pfaf_id' in attrs.columns and row['pfaf_id'] in fut.index: v = num(fut.at[row['pfaf_id'], c])
        else: v = num(row[c])
        if v is not None: v = round(v, 3) if c.endswith('_raw') or c.endswith('_r') else int(v)
        out.append(v)
    return out

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'aq'); os.makedirs(out_dir, exist_ok=True)
for f in glob.glob(os.path.join(out_dir, '*.json')): os.remove(f)
T = int(5 / RES); n = 0; size = 0
for ty in range(0, H, T):
    for tx in range(0, W, T):
        sub = ras[ty:ty + T, tx:tx + T]
        if not sub.any(): continue
        ids = np.unique(sub); ids = ids[ids > 0]
        idx = {int(v): k for k, v in enumerate(ids)}
        flat = sub.ravel(); runs = []; prev = None; cnt = 0
        for v in flat:
            k = idx.get(int(v), -1)
            if k == prev: cnt += 1
            else:
                if prev is not None: runs += [prev, cnt]
                prev, cnt = k, 1
        runs += [prev, cnt]
        lat = 90 - (ty + T) * RES; lon = -180 + tx * RES
        p = os.path.join(out_dir, f'{int(round(lat))}_{int(round(lon))}.json')
        json.dump({'f': fields, 'u': [rec(int(v) - 1) for v in ids], 'r': runs}, open(p, 'w'), separators=(',', ':'))
        n += 1; size += os.path.getsize(p)
json.dump({'source': 'WRI Aqueduct 4.0 (2023), CC-BY 4.0', 'res_deg': RES, 'tile_deg': 5, 'fields': fields, 'tiles': n}, open(os.path.join(out_dir, '_meta.json'), 'w'))
print('tiles', n, 'bytes', size)
