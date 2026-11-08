#!/usr/bin/env python3
"""Re-run region→admin-1 matching on data/jmp-subnational.json without the raw workbooks."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jmp_mapper import map_region, norm, MANUAL
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'jmp-subnational.json')
d = json.load(open(p)); unm = {}; tot = mapped = 0
for iso, c in d.items():
    for nm, v in c['regions'].items():
        v['admin1'] = map_region(iso, nm); tot += 1
    # exact-name preference: an admin-1 whose name equals a region's name belongs to that region only
    regs = c['regions']; exact = {}
    for nm, v in regs.items():
        if nm in MANUAL.get(iso, {}): continue
        ex = [a for a in v['admin1'] if norm(a) == norm(nm)]
        if ex: v['admin1'] = ex; exact.update({a: nm for a in ex})
    for nm, v in regs.items():
        if nm in MANUAL.get(iso, {}): continue
        v['admin1'] = [a for a in v['admin1'] if exact.get(a, nm) == nm]
    for nm, v in regs.items():
        if v['admin1']: mapped += 1
        else: unm.setdefault(iso, []).append(nm)
json.dump(d, open(p, 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(unm, open(os.path.join(os.path.dirname(p), '..', 'tools', 'jmp_unmapped.json'), 'w'), ensure_ascii=False, indent=1)
print(f'{len(d)} countries, {mapped}/{tot} regions mapped; unmapped in {len(unm)} countries')
