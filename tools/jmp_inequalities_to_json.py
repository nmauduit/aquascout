#!/usr/bin/env python3
"""Convert JMP 'Inequalities' workbooks (washdata.org/data/country/{ISO3}/inequalities/download)
into data/jmp-subnational.json. Usage: python3 tools/jmp_inequalities_to_json.py file1.xlsm file2.xlsm ...
Region→admin-1 mappings live in tools/jmp_region_map.json (add one block per country)."""
import sys, json, os, openpyxl
here=os.path.dirname(os.path.abspath(__file__))
out_path=os.path.join(here,'..','data','jmp-subnational.json')
map_path=os.path.join(here,'jmp_region_map.json')
rmap=json.load(open(map_path)) if os.path.exists(map_path) else {}
out=json.load(open(out_path)) if os.path.exists(out_path) else {}
for f in sys.argv[1:]:
    wb=openpyxl.load_workbook(f,read_only=True,data_only=True)
    if 'data_summary' not in wb.sheetnames: print('skip',f); continue
    rows=list(wb['data_summary'].iter_rows(values_only=True)); hdr=rows[0]; ix={h:i for i,h in enumerate(hdr)}
    iso=None; by_year={}
    for r in rows[1:]:
        if r[ix['var1']]!='Water ladder': continue
        iso=r[ix['iso3']]; y=int(r[ix['year']]); lad=r[ix['var2']]
        Y=by_year.setdefault(y,{'regions':{},'rural_q1':{},'rural':{},'total':{}})
        for k in range(1,7):
            nm=r[ix.get(f'region_{k}_name')] if f'region_{k}_name' in ix else None; v=r[ix[f'region_{k}']] if f'region_{k}' in ix else None
            if nm and v not in (None,'N/A'): Y['regions'].setdefault(str(nm).strip(),{})[lad]=round(float(v),1)
        def q(cols):
            vals=[r[ix[c]] for c in cols if c in ix and r[ix[c]] not in (None,'N/A')]
            return round(sum(map(float,vals))/len(vals),1) if vals else None
        Y['rural_q1'][lad]=q(['rural_q1']); Y['rural'][lad]=q([f'rural_q{i}' for i in range(1,6)]); Y['total'][lad]=q([f'total_q{i}' for i in range(1,6)])
    if not iso: continue
    y=max(by_year); d=by_year[y]
    out[iso]={'year':y,'source':os.path.basename(f),'rural_q1':d['rural_q1'],'rural_mean_q':d['rural'],'total_mean_q':d['total'],
              'regions':{nm:{**vals,'admin1':rmap.get(iso,{}).get(nm,[])} for nm,vals in d['regions'].items()}}
    print(iso,y,list(d['regions']))
json.dump(out,open(out_path,'w'),ensure_ascii=False,separators=(',',':'))
print('wrote',out_path)
