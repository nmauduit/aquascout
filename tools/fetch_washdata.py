#!/usr/bin/env python3
"""Download WHO/UNICEF JMP files from washdata.org (run in GitHub Actions; the host is blocked from the dev container).
Saves washdata/{ISO3}.xlsm for every country with an 'inequalities' workbook, plus washdata/WLD_household.xlsx."""
import urllib.request, pathlib, sys, time

ISO = ("AFG BGD BTN IND KAZ KGZ MDV NPL PAK TJK TKM KHM IDN LAO MNG MMR PHL THA TLS VNM KIR PNG TON DZA ARM AZE EGY GEO IRQ "
       "JOR PSE SDN TUN TUR YEM ARG BRB BLZ BOL COL CRI CUB DOM SLV GTM GUY HTI HND JAM MEX NIC PAN PRY PER LCA SUR TTO URY "
       "AGO BEN BFA BDI CMR CAF TCD COM COG CIV COD SWZ ETH GAB GMB GHA GIN GNB KEN LSO LBR MDG MWI MLI MRT MOZ NAM NER NGA "
       "RWA STP SEN SLE SOM ZAF TGO UGA TZA ZMB ZWE ALB BLR BIH MNE MKD MDA SRB UKR").split()
out = pathlib.Path("washdata"); out.mkdir(exist_ok=True)
UA = {"User-Agent": "AquaScout/0.1 (open-data research tool)"}

def get(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    if len(data) < 5000 or data[:2] != b"PK":   # not an OOXML workbook
        return False
    dest.write_bytes(data); return True

ok, miss = [], []
for iso in ISO:
    dest = out / f"{iso}.xlsm"
    try:
        if get(f"https://washdata.org/data/country/{iso}/inequalities/download", dest): ok.append(iso)
        else: miss.append(iso)
    except Exception as e:
        miss.append(f"{iso}({e.__class__.__name__})")
    time.sleep(0.5)
for name, url in [("WLD_household.xlsx", "https://washdata.org/data/country/WLD/household/download"),
                  ("REG_household.xlsx", "https://washdata.org/data/country/REG/household/download")]:
    try: get(url, out / name)
    except Exception as e: print(name, "failed", e)
print("downloaded", len(ok), "inequalities files; missing:", " ".join(miss))
