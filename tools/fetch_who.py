#!/usr/bin/env python3
"""Refresh data/who-wash.json from the WHO GHO OData API (run from GitHub Actions; GHO has no CORS for browsers)."""
import json, urllib.request, pathlib
IND = {"SDGWSHBOD": "Dim1 eq 'SEX_BTSX'", "WSH_DOMESTIC_WASTE_SAFELY_TREATED": None, "WSH_4": "Dim1 eq 'SEX_BTSX'", "WSH_WATER_SAFELY_MANAGED": None}
out = {"_readme": "WHO GHO indicators pre-baked for the map (GHO API has no CORS). Refreshed weekly by .github/workflows/who-data.yml; source https://ghoapi.azureedge.net/api/"}
for ind, filt in IND.items():
    url = f"https://ghoapi.azureedge.net/api/{ind}?$select=SpatialDim,SpatialDimType,TimeDim,NumericValue,Dim1,Dim2" + (f"&$filter={urllib.parse.quote(filt)}" if filt else "")
    try:
        j = json.load(urllib.request.urlopen(url, timeout=120))
    except Exception as e:
        print(ind, "failed", e); continue
    d = {}
    for x in j.get("value", []):
        if x.get("SpatialDimType") != "COUNTRY" or x.get("NumericValue") is None: continue
        if x.get("Dim2") and not any(s in str(x["Dim2"]).upper() for s in ("ALL", "TOTAL")): continue
        k, y = x["SpatialDim"], int(x["TimeDim"])
        if k not in d or y > d[k]["y"]: d[k] = {"v": round(float(x["NumericValue"]), 2), "y": y}
    out[ind] = d; print(ind, len(d))
pathlib.Path("data/who-wash.json").write_text(json.dumps(out, separators=(",", ":")))
