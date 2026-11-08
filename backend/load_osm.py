#!/usr/bin/env python3
"""Load an osmium-exported GeoJSONSeq file into Supabase (osm_feat) via psql COPY.

Usage: load_osm.py <region-slug> <theme water|power> <file.geojsonseq>
Needs SUPABASE_DB_URL in the environment (Postgres connection string).
"""
import json, os, subprocess, sys, tempfile

region, theme, path = sys.argv[1], sys.argv[2], sys.argv[3]
db = os.environ.get("SUPABASE_DB_URL", "").strip().strip('"').strip("'").strip()
if db.startswith("postgres://"): db = "postgresql://" + db[len("postgres://"):]

WATER_KEEP = {"natural": {"water", "coastline", "spring"},
              "waterway": {"river", "canal", "stream"},
              "man_made": {"water_well", "water_works", "wastewater_plant", "desalination_plant", "reservoir_covered",
                            "water_tower", "pumping_station"},
              "landuse": {"reservoir", "salt_pond", "basin"}}
POWER_KEEP = {"power": {"line", "minor_line", "cable", "substation", "plant", "generator"}}

def keep(tags):
    if theme == "power":
        return tags.get("power") in POWER_KEEP["power"] and (tags.get("power") != "generator" or "generator:source" in tags)
    if "place" in tags and "population" in tags:
        return True
    for k, vals in WATER_KEEP.items():
        if tags.get(k) in vals:
            # drop unnamed streams/ditches to keep the table small
            if k == "waterway" and tags[k] == "stream" and "name" not in tags:
                return False
            return True
    return False

TAGKEYS = ("name", "name:en", "natural", "waterway", "man_made", "landuse", "place", "population", "power", "voltage",
           "operator", "substation", "plant:source", "plant:output:electricity", "generator:source",
           "generator:output:electricity", "capacity", "plant:method", "plant:source", "source", "water_source",
           "disused", "construction", "proposed", "intermittent", "salt", "seasonal", "ele")

tmp = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8")
n = 0
with open(path, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip().lstrip("\x1e")
        if not line:
            continue
        f = json.loads(line)
        tags = f.get("properties") or {}
        if not keep(tags):
            continue
        oid = tags.get("@id") or f.get("id") or ""
        if not oid:
            continue
        slim = {k: v for k, v in tags.items() if k in TAGKEYS}
        geom = json.dumps(f["geometry"], separators=(",", ":"))
        tj = json.dumps(slim, ensure_ascii=False, separators=(",", ":"))
        tmp.write("\t".join([str(oid), theme, region, tj.replace("\\", "\\\\").replace("\t", " "), geom]) + "\n")
        n += 1
tmp.close()
print(f"{region}/{theme}: {n} features to load")

sql = f"""
set statement_timeout = 0;
set lock_timeout = 0;
create temp table stg (osm_id text, theme text, region text, tags jsonb, gj text);
\\copy stg from '{tmp.name}' with (format text)
delete from osm_feat where region = '{region}' and theme = '{theme}';
insert into osm_feat (osm_id, theme, region, tags, geom, center)
select osm_id, theme, region, tags,
       st_multi(case when st_npoints(g) > 8 then st_simplifypreservetopology(g, 0.0003) else g end),
       st_pointonsurface(g)
from (select osm_id, theme, region, tags, st_makevalid(st_setsrid(st_geomfromgeojson(gj),4326)) g from stg where gj is not null) s
where g is not null and not st_isempty(g)
  -- slim: unnamed ponds under 1 ha add nothing to a feasibility screen
  and not (coalesce(tags->>'natural', '') = 'water' and not (tags ? 'name') and coalesce(st_area(g::geography), 0) < 10000)
on conflict (region, theme, osm_id) do update set tags=excluded.tags, geom=excluded.geom, center=excluded.center, loaded_at=now();
insert into osm_region (region, feat_{theme}, bbox, loaded_at)
select '{region}', count(*) filter (where theme = '{theme}'), st_envelope(st_extent(center)::geometry), now() from osm_feat where region='{region}'
on conflict (region) do update set feat_{theme}=excluded.feat_{theme},
  bbox = st_envelope(st_union(coalesce(osm_region.bbox, excluded.bbox), excluded.bbox)), loaded_at=now();
"""
sqlf = tmp.name + ".sql"
open(sqlf, "w").write(sql)
subprocess.run(["psql", "--dbname=" + db, "-v", "ON_ERROR_STOP=1", "-q", "-f", sqlf], check=True)
os.unlink(sqlf)
os.unlink(tmp.name)
print("done")
