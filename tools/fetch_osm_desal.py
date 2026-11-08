#!/usr/bin/env python3
"""Pre-bake every OSM man_made=desalination_plant worldwide into data/osm-desal.json (run weekly in GitHub Actions)."""
import json, urllib.request, urllib.parse, pathlib
Q = '[out:json][timeout:180];nwr["man_made"="desalination_plant"];out tags center 10000;'
for m in ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter", "https://lz4.overpass-api.de/api/interpreter"]:
    try:
        req = urllib.request.Request(m, data=urllib.parse.urlencode({"data": Q}).encode(), headers={"User-Agent": "AquaScout/0.1 (open-data research tool)"})
        r = json.load(urllib.request.urlopen(req, timeout=240)); break
    except Exception as e:
        print(m, "failed", e); r = None
if not r: raise SystemExit("all Overpass mirrors failed")
out = []
for e in r.get("elements", []):
    t = e.get("tags", {}); la = e.get("lat", (e.get("center") or {}).get("lat")); lo = e.get("lon", (e.get("center") or {}).get("lon"))
    if la is None: continue
    out.append({"name": t.get("name") or t.get("name:en") or "Desalination plant", "la": round(la, 5), "lo": round(lo, 5),
                "operator": t.get("operator", ""), "capacity": t.get("capacity") or t.get("plant:output", ""),
                "method": t.get("plant:method") or t.get("desalination") or t.get("method", ""),
                "feed": t.get("plant:source") or t.get("source") or t.get("water_source", ""),
                "status": "disused" if "disused" in t else "under construction" if "construction" in t else "proposed" if "proposed" in t else "existing",
                "id": f'{e["type"]}/{e["id"]}'})
pathlib.Path("data/osm-desal.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print(len(out), "plants")
