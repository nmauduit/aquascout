#!/usr/bin/env python3
"""Append India + Israel desalination plants to data/planned-desal.json."""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data" / "planned-desal.json"
d = json.loads(P.read_text())

BR_IL = "https://www.blackridgeresearch.com/blog/latest-list-of-top-largest-biggest-desalination-desal-water-treatment-plants-projects-israel"
SWM_IL = "https://smartwatermagazine.com/news/smart-water-magazine/five-of-israels-six-mediterranean-desalination-plants-offline-as-seawater-turbidity-halts-filtration-developing"
BR_IN = "https://www.blackridgeresearch.com/blog/top-major-biggest-largest-desalination-plants-projects-cost-in-india"
II = "https://indianinfrastructure.com/2025/06/08/seawater-strategy-tapping-the-desalination-market-to-meet-water-demand/"
LTTD = "https://en.wikipedia.org/wiki/Low-temperature_thermal_desalination"
def e(name, cc, region, lat, lon, status, cap, feed, power, serves, source, operator=None, tech="RO", approx=True):
    return {"name": name, "country": cc, "region": region, "lat": lat, "lon": lon, "approx": approx,
            "status": status, "capacity_m3d": cap, "feed": feed, "power": power, "technology": tech,
            "serves": serves, "operator": operator, "source": source}
TURB = " — offline Aug–Sep 2026 (Nile-delta algae turbidity)"
A = [
 # ---------- Israel ----------
 e("Sorek A SWRO", "IL", "Palmachim / Rishon LeZion", 31.95, 34.73, "operating since 2013" + TURB, 410000, "seawater", "grid", "central Israel — 150 Mm³/yr", BR_IL, "IDE / Hutchison Water"),
 e("Sorek B (Sorek 2) SWRO", "IL", "Palmachim / Rishon LeZion", 31.94, 34.72, "operating since 2024 — world's largest SWRO" + TURB, 548000, "seawater", "grid", "central Israel — 200 Mm³/yr", BR_IL, "IDE Technologies"),
 e("Hadera SWRO", "IL", "Hadera", 32.47, 34.88, "operating since 2009 — stayed online Sep 2026", 348000, "seawater", "grid", "N/central Israel — 127 Mm³/yr", BR_IL, "H2ID (IDE + Shikun & Binui)"),
 e("Ashkelon SWRO", "IL", "Ashkelon", 31.63, 34.52, "operating since 2005" + TURB, 323000, "seawater", "grid", "S Israel — 118 Mm³/yr", BR_IL, "VID (Veolia + IDE)"),
 e("Ashdod SWRO", "IL", "Ashdod", 31.83, 34.64, "operating since 2015" + TURB, 274000, "seawater", "grid", "100 Mm³/yr", BR_IL, "Mekorot"),
 e("Palmachim SWRO", "IL", "Palmachim", 31.93, 34.70, "operating since 2007" + TURB, 247000, "seawater", "grid", "90 Mm³/yr", BR_IL, "Via Maris Desalination"),
 e("Eilat BWRO/SWRO (Sabha)", "IL", "Eilat", 29.56, 34.95, "operating since the 1990s — brackish + seawater units; stayed online Sep 2026", None, "brackish groundwater + Red Sea water", "grid", "Eilat", SWM_IL, "Mekorot"),
 e("Western Galilee SWRO", "IL", "Western Galilee (near Shavei Zion)", 32.98, 35.08, "under construction — 100 Mm³/yr", 274000, "seawater", "grid", "N Israel", "https://en.wikipedia.org/wiki/IDE_Technologies"),
 # ---------- India ----------
 e("Minjur SWRO", "IN", "Chennai, Tamil Nadu", 13.27, 80.32, "operating since 2010 — 100 MLD; feasibility study for a new ₹4,800 cr plant", 100000, "seawater", "grid", "N Chennai", BR_IN, "Chennai Water Desalination Ltd (IVRCL + Befesa) / CMWSSB"),
 e("Nemmeli I + II SWRO", "IN", "Chennai, Tamil Nadu", 12.72, 80.22, "operating since 2013 (110 MLD) + 150 MLD expansion", 260000, "seawater", "grid", "S Chennai", BR_IN, "CMWSSB / VA Tech Wabag, IDE, JWIL"),
 e("Perur SWRO", "IN", "Chennai, Tamil Nadu", 12.65, 80.20, "under construction — completion Dec 2026, 400 MLD (2×200)", 400000, "seawater", "grid", "Chennai — ₹4,276 cr, JICA-funded", BR_IN, "CMWSSB / Metito + VA Tech Wabag (20-yr O&M)"),
 e("Pattipulam SWRO", "IN", "ECR, Tamil Nadu", 12.78, 80.24, "planned — 200 MLD expandable 400", 200000, "seawater", "grid", "Chennai", BR_IN, "CMWSSB"),
 e("Manori SWRO (Mumbai)", "IN", "Mumbai, Maharashtra", 19.21, 72.78, "planned — 200 MLD (→400); 2024 tender cancelled for lack of bidders, retendered", 200000, "seawater", "grid", "Mumbai — ₹3,520 cr", BR_IN, "BMC"),
 e("Jamnagar refinery desal (Reliance)", "IN", "Jamnagar, Gujarat", 22.35, 69.85, "operating since 1998 — MED + SWRO, expanding 2026", 160000, "seawater", "refinery power", "Reliance refinery complex", BR_IN, "Reliance / IDE / VA Tech Wabag", tech="MED + RO"),
 e("Dahej GIDC desal", "IN", "Dahej, Gujarat", 21.70, 72.57, "operating since 2022 — 100 MLD", 100000, "Narmada canal / estuary (not seawater)", "grid", "Dahej PCPIR industry", BR_IN, "GIDC"),
 e("Mandvi SWRO", "IN", "Kutch, Gujarat", 22.83, 69.35, "under construction — 100 MLD PPP, ~2027", 100000, "seawater", "grid", "Kutch municipal", II, "Gujarat Water Infrastructure Ltd (PPP)"),
 e("Gundiyali (Mandvi) SWRO", "IN", "Kutch, Gujarat", 22.80, 69.40, "under construction — 100 MLD industrial, ~2027", 100000, "seawater", "grid", "Kutch industry", II),
 e("Essar / Nayara refinery desal (Vadinar)", "IN", "Devbhumi Dwarka, Gujarat", 22.45, 69.72, "operating — 65 MLD", 65000, "seawater", "refinery power", "Vadinar refinery", II),
 e("Mullakadu (Tuticorin) desal", "IN", "Thoothukudi, Tamil Nadu", 8.73, 78.13, "planned — 60 MLD industrial by 2027", 60000, "seawater", "grid", "Tuticorin industry", II),
 e("Indosol solar PV plant desal", "IN", "Ramayapatnam, Andhra Pradesh", 15.03, 80.05, "planned — 100 MLD by 2027", 100000, "seawater", "grid", "Indosol PV manufacturing", II),
 e("Khavda RE park desal", "IN", "Khavda, Kutch, Gujarat", 23.85, 69.70, "upcoming — 1 MLD at Khavda renewable park", 1000, "brackish groundwater", "solar/wind park", "Khavda construction & O&M", II),
 e("Kavaratti LTTD (NIOT)", "IN", "Lakshadweep", 10.57, 72.64, "operating since 2005 — first LTTD plant", 100, "seawater (deep-cold + surface)", "grid (diesel)", "Kavaratti", LTTD, "NIOT / MoES", tech="LTTD (thermal)"),
 e("Chetlat LTTD (NIOT)", "IN", "Lakshadweep", 11.70, 72.71, "inaugurated 2025-01 — 1.5 lakh L/d; part of 6-island LTTD programme (Amini, Androth, Kadmat, Kalpeni, Kiltan)", 150, "seawater (deep-cold + surface)", "grid (diesel)", "Chetlat island", "https://x.com/MoesNiot/status/1880224594206068898", "NIOT", tech="LTTD (thermal)"),
 e("Kavaratti OTEC-powered desal (NIOT)", "IN", "Lakshadweep", 10.56, 72.63, "under construction — 100 m³/d, self-powered by OTEC", 100, "seawater", "OTEC (ocean thermal)", "Kavaratti", II, "NIOT", tech="LTTD + OTEC"),
 e("Narippaiyur solar-thermal FO desal (IIT Madras)", "IN", "Ramanathapuram, Tamil Nadu", 9.27, 78.90, "operating since 2021-06 — 20,000 L/d pilot", 20, "seawater", "solar thermal", "Narippaiyur village", "https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=1728530&reg=3&lang=2", "IIT Madras / Empereal-KGDS", tech="forward osmosis"),
]

existing = {(p["name"], p["country"]) for p in d["plants"]}
added = [p for p in A if (p["name"], p["country"]) not in existing]
d["plants"].extend(added)
d["_readme"] = d["_readme"].replace("Africa and Europe", "Africa, Europe, Israel and India")
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(f"added {len(added)}, total {len(d['plants'])}")
