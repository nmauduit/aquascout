#!/usr/bin/env python3
"""Load static global point datasets into Supabase table bulk_point (theme, id, name, props, geom).

  load_bulk.py hydrowaste HydroWASTE_v10.csv
  load_bulk.py salinity   Groundwaters_summary.csv Rivers_summary.csv Lakes_Reservoirs_summary.csv

Themes written: wwtp (HydroWASTE v1.0, Ehalt Macedo et al. 2022) and sal_gw / sal_rv / sal_lk
(Thorslund & van Vliet 2020 station summaries; electrical conductivity in µS/cm).
Needs SUPABASE_DB_URL in the environment."""
import csv, json, os, subprocess, sys, tempfile

db = os.environ.get("SUPABASE_DB_URL", "").strip().strip('"').strip("'").strip()
if db.startswith("postgres://"): db = "postgresql://" + db[len("postgres://"):]
kind, files = sys.argv[1], sys.argv[2:]

def num(v):
    try:
        f = float(v); return None if f != f else f
    except (TypeError, ValueError): return None

def clean(s): return (s or "").replace("\t", " ").replace("\n", " ").replace("\\", "/").strip()

rows = {}  # theme -> list of (id, name, props, lon, lat)
if kind == "hydrowaste":
    for r in csv.DictReader(open(files[0], encoding="utf-8-sig", errors="replace")):
        lat, lon = num(r["LAT_WWTP"]), num(r["LON_WWTP"])
        if lat is None or lon is None: continue
        p = {"cc": r["CNTRY_ISO"], "pop": num(r["POP_SERVED"]), "dis": num(r["WASTE_DIS"]), "lvl": r["LEVEL"],
             "cap": num(r["DESIGN_CAP"]), "st": r["STATUS"], "rq": num(r["RIVER_DIS"]), "df": num(r["DF"]),
             "coast": r["COAST_10KM"] == "1", "ql": num(r["QUAL_LOC"]),
             "out": [num(r["LON_OUT"]), num(r["LAT_OUT"])]}
        rows.setdefault("wwtp", []).append((r["WASTE_ID"], clean(r["WWTP_NAME"]), p, lon, lat))
elif kind == "salinity":
    for f in files:
        theme = "sal_gw" if "Ground" in f else "sal_rv" if "River" in f else "sal_lk"
        seen = set()
        for r in csv.DictReader(open(f, encoding="utf-8-sig", errors="replace")):
            lat, lon = num(r.get("Lat")), num(r.get("Lon"))
            ec = num(r.get("median"))
            if lat is None or lon is None or ec is None or not (-90 <= lat <= 90 and -180 <= lon <= 180): continue
            sid = clean(r.get("Station_ID"))[:80] or f"{lat},{lon}"
            if sid in seen: sid = f"{sid}@{lat:.4f},{lon:.4f}"
            seen.add(sid)
            p = {"ec": round(ec, 1), "max": num(r.get("max")), "min": num(r.get("min")), "n": int(num(r.get("n")) or 0),
                 "y0": (r.get("Start_date") or "")[:4], "y1": (r.get("End_date") or "")[:4],
                 "src": clean(r.get("Source")), "coast": r.get("Coastal_location") == "Yes"}
            if r.get("median_TDS"): p["tds"] = num(r["median_TDS"])
            rows.setdefault(theme, []).append((sid, None, p, lon, lat))
else:
    sys.exit("unknown kind " + kind)

for theme, items in rows.items():
    tmp = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8")
    for i, n, p, lon, lat in items:
        p = {k: v for k, v in p.items() if v not in (None, "", [None, None])}
        tmp.write("\t".join([clean(str(i)), n or "\\N", json.dumps(p, ensure_ascii=False, separators=(",", ":")).replace("\\", "\\\\"), repr(lon), repr(lat)]) + "\n")
    tmp.close()
    print(f"{theme}: {len(items)} rows")
    sql = f"""
set statement_timeout = 0; set lock_timeout = 0;
create temp table stg (id text, name text, props jsonb, lon double precision, lat double precision);
\\copy stg from '{tmp.name}' with (format text)
delete from bulk_point where theme = '{theme}';
insert into bulk_point (theme, id, name, props, geom)
select distinct on (id) '{theme}', id, name, props, st_setsrid(st_makepoint(lon, lat), 4326) from stg order by id;
"""
    sqlf = tmp.name + ".sql"; open(sqlf, "w").write(sql)
    subprocess.run(["psql", "--dbname=" + db, "-v", "ON_ERROR_STOP=1", "-q", "-f", sqlf], check=True)
    os.unlink(sqlf); os.unlink(tmp.name)
print("done")
