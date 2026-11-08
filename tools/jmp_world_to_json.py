#!/usr/bin/env python3
"""Extract the JMP drinking-water service components by country from the world household workbook
(washdata.org/data/country/WLD/household/download, sheet 'wat') into data/jmp-components.json.

Components (share of population, %), per area r=rural, u=urban, t=total:
  av   improved source, water available when needed      (continuity)
  qual improved source, free from contamination           (safety)
  prem improved source, accessible on premises
  sm   safely managed
  pip  piped supply
  bas  at least basic (basic + safely managed is in 'basal')
  sw   surface water
For each country the latest year that has av or qual is kept (components are estimated less often than coverage).
Usage: python3 tools/jmp_world_to_json.py washdata/WLD_household.xlsx"""
import sys, json, os, re, unicodedata, difflib, openpyxl

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, '..')
out_path = os.path.join(root, 'data', 'jmp-components.json')

def norm(s):
    s = unicodedata.normalize('NFD', str(s)).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'\b(the|of|and|republic|rep|democratic|dem|plurinational|state|states|islands|federated|kingdom|united|people s|peoples)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

MANUAL = {  # JMP names that the country file spells differently
    "Bolivia (Plurinational State of)": "BOL", "Venezuela (Bolivarian Republic of)": "VEN", "Iran (Islamic Republic of)": "IRN",
    "United Republic of Tanzania": "TZA", "Democratic Republic of the Congo": "COD", "Congo": "COG", "Côte d'Ivoire": "CIV",
    "Republic of Korea": "KOR", "Democratic People's Republic of Korea": "PRK", "Lao People's Democratic Republic": "LAO",
    "Viet Nam": "VNM", "Russian Federation": "RUS", "Syrian Arab Republic": "SYR", "Republic of Moldova": "MDA",
    "United States of America": "USA", "United Kingdom": "GBR", "Micronesia (Federated States of)": "FSM", "Türkiye": "TUR",
    "Turkey": "TUR", "Czechia": "CZE", "Eswatini": "SWZ", "Cabo Verde": "CPV", "North Macedonia": "MKD",
    "State of Palestine": "PSE", "Dominican Republic": "DOM", "Dominica": "DMA", "Gambia": "GMB", "Bahamas": "BHS",
    "Netherlands (Kingdom of the)": "NLD", "Netherlands": "NLD", "Sint Maarten (Dutch part)": "SXM", "Saint Martin (French part)": "MAF",
    "China, Hong Kong SAR": "HKG", "China, Macao SAR": "MAC", "Curaçao": "CUW", "Réunion": "REU", "Kosovo": "XKX",
    "Sao Tome and Principe": "STP", "Guinea-Bissau": "GNB", "Equatorial Guinea": "GNQ", "Papua New Guinea": "PNG",
    "Central African Republic": "CAF", "South Sudan": "SSD", "Sudan": "SDN", "Niger": "NER", "Nigeria": "NGA",
    "Brunei Darussalam": "BRN", "Timor-Leste": "TLS", "Saint Kitts and Nevis": "KNA", "Saint Lucia": "LCA",
    "Saint Vincent and the Grenadines": "VCT", "Antigua and Barbuda": "ATG", "Trinidad and Tobago": "TTO",
    "Bosnia and Herzegovina": "BIH", "Turks and Caicos Islands": "TCA", "British Virgin Islands": "VGB",
    "United States Virgin Islands": "VIR", "Cayman Islands": "CYM", "Falkland Islands (Malvinas)": "FLK",
    "Northern Mariana Islands": "MNP", "Marshall Islands": "MHL", "Solomon Islands": "SLB", "Cook Islands": "COK",
    "Faroe Islands": "FRO", "Channel Islands": "CHI", "Wallis and Futuna Islands": "WLF", "Holy See": "VAT",
    "Bonaire, Sint Eustatius and Saba": "BES", "Saint Pierre and Miquelon": "SPM", "Western Sahara": "ESH",
}

cfeat = json.load(open(os.path.join(root, 'data', 'countries.geojson')))['features']
by_norm = {norm(f['properties']['n']): f['properties']['a3'] for f in cfeat}

def iso_of(name):
    if name in MANUAL: return MANUAL[name]
    n = norm(name)
    if n in by_norm: return by_norm[n]
    try:
        import pycountry
        c = pycountry.countries.lookup(name); return c.alpha_3
    except Exception: pass
    m = difflib.get_close_matches(n, list(by_norm), n=1, cutoff=0.88)
    return by_norm[m[0]] if m else None

def num(v):
    if v is None or v == '': return None
    if isinstance(v, (int, float)): return round(float(v), 1)
    s = str(v).strip()
    if s.startswith('<'): return 0.5
    if s.startswith('>'): return 99.5
    try: return round(float(s), 1)
    except ValueError: return None

COMP = {'av': 'wat_imp_av', 'qual': 'wat_imp_qual', 'prem': 'wat_imp_prem', 'sm': 'wat_sm', 'pip': 'wat_pip',
        'bas': 'wat_basal', 'sw': 'wat_sur'}

wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws = wb['wat']
rows = ws.iter_rows(values_only=True)
hdr = None
for r in rows:  # header row is the one containing 'name' and 'year'
    if r and 'year' in r and 'name' in r: hdr = r; break
ix = {h: i for i, h in enumerate(hdr) if h}
missing = [c for c in ('wat_imp_av_r', 'wat_imp_qual_r') if c not in ix]
if missing: print('WARNING missing columns', missing)
by = {}
for r in rows:
    if not r or r[ix['name']] is None: continue
    nm = str(r[ix['name']]).strip()
    try: y = int(r[ix['year']])
    except (TypeError, ValueError): continue
    rec = {}
    for a in 'rut':
        d = {}
        for k, col in COMP.items():
            c = f'{col}_{a}'
            if c in ix:
                v = num(r[ix[c]])
                if v is not None: d[k] = v
        if d: rec[a] = d
    if rec: by.setdefault(nm, {})[y] = rec

out, unmatched = {}, []
for nm, years in by.items():
    good = [y for y, rec in years.items() if any(('av' in rec.get(a, {}) or 'qual' in rec.get(a, {})) for a in 'rut')]
    if not good: continue
    y = max(good); iso = iso_of(nm)
    if not iso: unmatched.append(nm); continue
    out[iso] = {'name': nm, 'year': y, **years[y]}
json.dump(out, open(out_path, 'w'), ensure_ascii=False, separators=(',', ':'))
print('wrote', out_path, len(out), 'countries; unmatched:', unmatched[:40])
for k in ('COL', 'KEN', 'HTI', 'IND'):
    if k in out: print(k, out[k])
