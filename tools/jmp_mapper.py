"""Match JMP survey regions to Natural Earth admin-1 names (used by the converter and by remap_jmp.py).

Order: manual table (tools/jmp_region_map.json) → admin-1 name/alt names → Natural Earth 'region' grouping
→ containment → multi-part names ("Gaza & Inhambane") → fuzzy."""
import json, os, re, unicodedata, difflib
here = os.path.dirname(os.path.abspath(__file__))
IDX = json.load(open(os.path.join(here, 'admin1_index.json')))
MANUAL = json.load(open(os.path.join(here, 'jmp_region_map.json')))
STOP = r"\b(region|regions|province|provincia|department|departamento|departement|district|distrito|state|estado|governorate|county|division|zone|oblast|prefecture|wilaya|gouvernorat|area|de|del|la|el|du|des|the|of|and|y|et|in|regiao)\b"
STEM = [('northeastern', 'northeast'), ('northwestern', 'northwest'), ('southeastern', 'southeast'), ('southwestern', 'southwest'),
        ('northern', 'north'), ('southern', 'south'), ('eastern', 'east'), ('western', 'west')]

def norm(s):
    s = unicodedata.normalize('NFD', str(s)).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'^\s*[.\d]+\s*', '', s)            # "33 Central Java", "..LE Rural"
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    s = re.sub(STOP, ' ', s)
    for a, b in STEM: s = re.sub(r'\b' + a + r'\b', b, s)
    return re.sub(r'\s+', ' ', s).strip()

def strip_num(s): return re.sub(r'^\s*[.\d]+\s*', '', str(s)).strip()

def map_region(iso, region):
    man = MANUAL.get(iso, {})
    for k in (region, strip_num(region)):
        if k in man: return man[k]
    cands = IDX.get(iso, []); r = norm(region)
    if not r or not cands: return []
    # 1. admin-1 name or any of its alternate names
    hit = [c['n'] for c in cands if any(norm(x) == r for x in c['names'])]
    if hit: return sorted(set(hit))
    # 2. Natural Earth 'region' grouping (exact, then unique prefix)
    regs = {}
    for c in cands:
        if c['region']: regs.setdefault(norm(c['region']), []).append(c['n'])
    if r in regs: return sorted(regs[r])
    pre = [k for k in regs if k.startswith(r + ' ')]
    if len(pre) == 1: return sorted(regs[pre[0]])
    # 3. containment, single hit only (>= 5 chars to avoid "norte" ⊂ "norte de santander")
    hit = sorted({c['n'] for c in cands for x in c['names'] if len(r) >= 5 and (r in norm(x) or norm(x) in r) and len(norm(x)) >= 5})
    if len(hit) == 1: return hit
    # 4. names listing several units
    parts = [p for p in re.split(r'[,/&+]| and | y | et ', str(region)) if p.strip()]
    if len(parts) > 1:
        got = []
        for p in parts:
            m = map_region(iso, p)
            if len(m) == 1: got += m
        if got: return sorted(set(got))
    # 5. fuzzy on names
    allnames = {norm(x): c['n'] for c in cands for x in c['names']}
    best = difflib.get_close_matches(r, list(allnames), n=1, cutoff=0.82)
    if best: return [allnames[best[0]]]
    return []
