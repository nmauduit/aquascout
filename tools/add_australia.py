#!/usr/bin/env python3
"""Append Australian desalination plants to data/planned-desal.json."""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data" / "planned-desal.json"
d = json.loads(P.read_text())

WL = "https://en.wikipedia.org/wiki/List_of_desalination_plants_in_Australia"
NS = "https://nsanalytic.com/2026/04/09/australias-desalination-industry-from-drought-insurance-to-core-water-infrastructure/"
WC = "https://www.watercorporation.com.au/about-us/media-releases/2026/march-2026/expanded-desalination-plant-to-help-secure-pilbaras-water-supply"
def e(name, region, lat, lon, status, cap, feed, power, serves, source, operator=None, tech="RO", approx=True):
    return {"name": name, "country": "AU", "region": region, "lat": lat, "lon": lon, "approx": approx,
            "status": status, "capacity_m3d": cap, "feed": feed, "power": power, "technology": tech,
            "serves": serves, "operator": operator, "source": source}

A = [
 # ---- six metropolitan plants ----
 e("Perth Seawater Desalination Plant (Kwinana)", "WA", -32.20, 115.77, "operating since 2006 — 45 GL/yr", 130000, "seawater", "grid + wind farm offset (Emu Downs)", "Perth", WL, "Water Corporation"),
 e("Southern Seawater Desalination Plant (Binningup)", "WA", -33.14, 115.67, "operating since 2012 — 100 GL/yr", 270000, "seawater", "grid + renewable offset", "Perth / South West", WL, "Water Corporation"),
 e("Sydney Desalination Plant (Kurnell)", "NSW", -34.02, 151.21, "operating since 2010 — drought-triggered; 84 GL/yr; expansion under study", 250000, "seawater", "grid + wind offset (Capital wind farm)", "Sydney", WL, "Sydney Desalination Plant Pty"),
 e("Victorian Desalination Plant (Wonthaggi)", "VIC", -38.58, 145.52, "operating since 2012 — 150 GL/yr, ordered annually", 410000, "seawater", "grid + renewable offset", "Melbourne", WL, "AquaSure"),
 e("Adelaide Desalination Plant (Port Stanvac)", "SA", -35.11, 138.47, "operating since 2012 — 100 GL/yr, minimum production mode (~10 % of SA water)", 300000, "seawater", "grid + renewable offset", "Adelaide", WL, "SA Water / AdelaideAqua"),
 e("Gold Coast Desalination Plant (Tugun)", "QLD", -28.15, 153.49, "operating since 2009 — standby/minimum mode; expansion business case for 2030/31", 125000, "seawater", "grid", "SE Queensland grid", WL, "Seqwater"),
 # ---- under construction / planned ----
 e("Alkimos SWRO", "WA", -31.62, 115.68, "under construction — Stage 1 50 GL/yr, first water 2028; Stage 2 +50 GL", 137000, "seawater", "grid + renewables", "Perth north", NS, "Water Corporation"),
 e("Eyre Peninsula SWRO (Billy Lights Point)", "SA", -34.73, 135.88, "under construction — 5.3 GL/yr, first water end-2026", 14500, "seawater", "grid", "Eyre Peninsula (replaces over-drawn Uley basin)", NS, "SA Water"),
 e("Dampier SWRO (Rio Tinto / WA Govt)", "WA", -20.66, 116.71, "Stage 1 under construction (2026), Stage 2 doubling to 8 GL/yr by 2027 — A$606 M", 22000, "seawater", "grid (Pilbara)", "Karratha / Dampier / Rio Tinto ops", WC, "Water Corporation / Rio Tinto"),
 e("Onslow SWRO (new)", "WA", -21.64, 115.11, "under construction — 1.5 ML/d (→2), production 2026", 1500, "seawater", "grid (Onslow solar-battery microgrid)", "Onslow", NS, "Water Corporation"),
 e("Lower Great Southern SWRO (Nanarup/Albany)", "WA", -34.98, 118.05, "planning — 3 GL/yr initial, needed by 2030", 8200, "seawater", "grid", "Albany region", NS, "Water Corporation"),
 e("Belmont drought-response SWRO", "NSW", -33.03, 151.66, "approved contingency — built only if Hunter storages fall to 35 %", 30000, "seawater", "grid", "Lower Hunter / Newcastle", "https://www.planningportal.nsw.gov.au/major-projects/projects/belmont-drought-response-desalination-plant?page=0", "Hunter Water"),
 e("Northern Water Project (Whyalla / Cape Hardy)", "SA", -33.03, 137.57, "proposed — 140 ML/d for green-iron / hydrogen industry", 140000, "seawater", "grid + renewables", "Upper Spencer Gulf industry", WL, "SA Government"),
 e("Point Lowly / Port Bonython (BHP Olympic Dam)", "SA", -32.99, 137.78, "CANCELLED — approved 2011, never built", 280000, "seawater", "grid", "Olympic Dam mine", WL, "BHP"),
 e("Toukley SWRO", "NSW", -33.26, 151.54, "approved 2007 — construction deferred", 20000, "seawater", "grid", "Central Coast", WL, "Central Coast Council"),
 # ---- mining / industrial ----
 e("Cape Preston SWRO (Sino Iron)", "WA (Pilbara)", -20.86, 116.20, "operating", 140000, "seawater", "on-site gas power", "Sino Iron magnetite project", WL, "CITIC Pacific"),
 e("Burrup SWRO", "WA (Pilbara)", -20.60, 116.76, "operating", 16400, "seawater", "grid", "Burrup industrial estate", WL),
 e("Barrow Island SWRO (Gorgon)", "WA", -20.80, 115.40, "operating", 7000, "seawater", "LNG plant power", "Gorgon LNG", WL, "Chevron"),
 e("Whyalla Steelworks desal", "SA", -33.02, 137.58, "operating", 4000, "seawater", "grid", "steelworks", WL),
 e("Port Augusta Sundrop Farms solar-thermal desal", "SA", -32.52, 137.79, "operating since 2016 — concentrated solar tower drives desal + greenhouse", 8000, "seawater (Spencer Gulf)", "concentrated solar thermal (CSP) + gas backup", "20 ha greenhouse", WL, "Sundrop Farms", tech="thermal + RO"),
 # ---- small regional / island / remote ----
 e("Rottnest Island SWRO", "WA", -32.00, 115.52, "operating — island supply with wind + solar", 550, "seawater", "wind + solar + diesel microgrid", "Rottnest Island", WL, "Rottnest Island Authority"),
 e("Long Island (Abrolhos) SWRO", "WA", -28.47, 113.77, "operating", 17, "seawater", "diesel/solar", "fishing community", WL),
 e("Hawker BWRO", "SA", -31.89, 138.42, "operating", 440, "brackish groundwater", "grid", "Hawker township", WL, "SA Water"),
 e("Leigh Creek BWRO", "SA", -30.60, 138.40, "operating", None, "brackish groundwater", "grid", "Leigh Creek", WL, "SA Water"),
 e("Marion Bay SWRO", "SA", -35.23, 136.98, "operating since 2008", 60, "seawater", "grid", "Marion Bay", WL, "SA Water"),
 e("Penneshaw (Kangaroo Head) SWRO", "SA", -35.72, 137.94, "operating — upgraded late 2024", 300, "seawater", "grid", "Penneshaw, Kangaroo Island", NS, "SA Water"),
 e("Hamilton Island SWRO", "QLD", -20.35, 148.95, "operating", 1500, "seawater", "island diesel/solar", "resort island", WL),
 e("Green Island SWRO", "QLD", -16.76, 145.97, "operating", 60, "seawater", "island", "resort", WL),
 e("Agnes Water / 1770 SWRO", "QLD", -24.21, 151.90, "operating since 2010", 1500, "seawater", "grid", "Agnes Water", WL, "Gladstone Regional Council"),
 e("Christmas Island desal", "Christmas Island", -10.42, 105.68, "operating", 4500, "seawater/brackish", "diesel + solar", "Christmas Island", WL),
 e("Home Island (Cocos Keeling) desal", "Cocos (Keeling) Islands", -12.12, 96.90, "operating", 350, "brackish lens", "diesel + solar", "Home Island", WL),
]

existing = {(p["name"], p["country"]) for p in d["plants"]}
added = [p for p in A if (p["name"], p["country"]) not in existing]
d["plants"].extend(added)
d["_readme"] = d["_readme"].replace("Israel and India", "Israel, India and Australia")
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(f"added {len(added)}, total {len(d['plants'])}")
