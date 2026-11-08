#!/usr/bin/env python3
"""Convert JMP 'Inequalities' workbooks (washdata.org/data/country/{ISO3}/inequalities/download)
into data/jmp-subnational.json.  Usage: python3 tools/jmp_inequalities_to_json.py washdata/*.xlsm

Region → admin-1 mapping: manual entries in tools/jmp_region_map.json win; otherwise regions are matched
automatically against data/admin1.geojson names (accent-insensitive exact / containment / fuzzy).
Unmatched regions are written to tools/jmp_unmapped.json for manual completion."""
import sys, json, os, re, unicodedata, difflib, openpyxl
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, '..')
out_path = os.path.join(root, 'data', 'jmp-subnational.json')
map_path = os.path.join(here, 'jmp_region_map.json')
unm_path = os.path.join(here, 'jmp_unmapped.json')
rmap = json.load(open(map_path)) if os.path.exists(map_path) else {}
out = json.load(open(out_path)) if os.path.exists(out_path) else {}
unmapped = {}

def norm(s):
    s = unicodedata.normalize('NFD', str(s)).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r"\b(region|province|provincia|department|departamento|departement|district|state|estado|governorate|county|division|zone|oblast|prefecture|wilaya|gouvernorat|area|de|del|la|el|du|des|the|of|and|y|&)\b", ' ', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

# admin-1 names by country
adm = {}
for f in json.load(open(os.path.join(root, 'data', 'admin1.geojson')))['features']:
    p = f['properties']; adm.setdefault(p['a3'], []).append((p['n'], norm(p['n']), norm(p.get('alt') or '')))

def auto_map(iso, region):
    cands = adm.get(iso, []); r = norm(region)
    if not r or not cands: return []
    # 1. exact (name or alt)
    hit = [n for n, a, b in cands if r == a or r == b]
    if hit: return hit
    # 2. one contains the other (>= 4 chars)
    hit = [n for n, a, b in cands if len(r) >= 4 and (r in a or a in r or (b and (r in b or b in r)))]
    if len(hit) == 1: return hit
    # 3. region name lists several admin-1 ("Centre-Est", "Nord/Ouest", "Gaza & Inhambane")
    parts = [p for p in re.split(r'[,/&+]| and | y | et ', str(region)) if p.strip()]
    if len(parts) > 1:
        got = []
        for p in parts:
            m = auto_map(iso, p)
            if len(m) == 1: got += m
        if got: return sorted(set(got))
    # 4. fuzzy
    best = difflib.get_close_matches(r, [a for _, a, _ in cands], n=1, cutoff=0.86)
    if best: return [n for n, a, _ in cands if a == best[0]][:1]
    return []

for f in sys.argv[1:]:
    try:
        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    except Exception as e:
        print('skip', f, e); continue
    if 'data_summary' not in wb.sheetnames: print('skip', f, 'no data_summary'); continue
    rows = list(wb['data_summary'].iter_rows(values_only=True)); hdr = rows[0]; ix = {h: i for i, h in enumerate(hdr) if h}
    rk = sorted({int(m.group(1)) for h in ix for m in [re.match(r'region_(\d+)$', str(h))] if m})
    iso = None; by_year = {}
    for r in rows[1:]:
        if r[ix['var1']] != 'Water ladder': continue
        iso = r[ix['iso3']]; y = int(r[ix['year']]); lad = r[ix['var2']]
        Y = by_year.setdefault(y, {'regions': {}, 'rural_q1': {}, 'rural': {}, 'total': {}})
        for k in rk:
            nmc = f'region_{k}_name'; vc = f'region_{k}'
            nm = r[ix[nmc]] if nmc in ix else None; v = r[ix[vc]] if vc in ix else None
            if nm and v not in (None, 'N/A', ''):
                try: Y['regions'].setdefault(str(nm).strip(), {})[lad] = round(float(v), 1)
                except ValueError: pass
        def q(cols):
            vals = []
            for c in cols:
                if c in ix and r[ix[c]] not in (None, 'N/A', ''):
                    try: vals.append(float(r[ix[c]]))
                    except ValueError: pass
            return round(sum(vals) / len(vals), 1) if vals else None
        Y['rural_q1'][lad] = q(['rural_q1']); Y['rural'][lad] = q([f'rural_q{i}' for i in range(1, 6)]); Y['total'][lad] = q([f'total_q{i}' for i in range(1, 6)])
    if not iso or not by_year: print('skip', f, 'no water ladder rows'); continue
    # latest year that actually has regional values, else latest year
    years = [y for y in by_year if by_year[y]['regions']] or list(by_year)
    y = max(years); d = by_year[y]
    regs = {}
    for nm, vals in d['regions'].items():
        a1 = rmap.get(iso, {}).get(nm) or auto_map(iso, nm)
        if not a1: unmapped.setdefault(iso, []).append(nm)
        regs[nm] = {**vals, 'admin1': a1}
    out[iso] = {'year': y, 'source': os.path.basename(f), 'rural_q1': d['rural_q1'], 'rural_mean_q': d['rural'], 'total_mean_q': d['total'], 'regions': regs}
    print(iso, y, f"{len(regs)} regions, {sum(1 for v in regs.values() if v['admin1'])} mapped")
json.dump(out, open(out_path, 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(unmapped, open(unm_path, 'w'), ensure_ascii=False, indent=1)
print('wrote', out_path, 'countries:', len(out), '| unmapped regions in', len(unmapped), 'countries ->', unm_path)
