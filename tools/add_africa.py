#!/usr/bin/env python3
"""Append African desalination plants (operating / under construction / planned / idle) to data/planned-desal.json."""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data" / "planned-desal.json"
d = json.loads(P.read_text())

WIKI = "https://en.wikipedia.org/wiki/Desalination_by_country"
SWM_MA = "https://smartwatermagazine.com/news/smart-water-magazine/desalination-morocco-a-vast-pipeline-projects"
DNE = "https://www.dailynewsegypt.com/2026/10/"
def e(name, cc, region, lat, lon, status, cap, feed, power, serves, source, operator=None, tech="RO", approx=True):
    return {"name": name, "country": cc, "region": region, "lat": lat, "lon": lon, "approx": approx,
            "status": status, "capacity_m3d": cap, "feed": feed, "power": power, "technology": tech,
            "serves": serves, "operator": operator, "source": source}

A = [
 # ---------- Algeria (SWRO, grid power) ----------
 e("Hamma (Algiers) SWRO", "DZ", "Algiers", 36.75, 3.08, "operating since 2008", 200000, "seawater", "grid", "Algiers", WIKI, "Algerian Energy Co. / GE"),
 e("Fouka SWRO", "DZ", "Tipaza", 36.67, 2.75, "operating since 2008", 120000, "seawater", "grid", "Tipaza / W Algiers", WIKI),
 e("Fouka 2 SWRO", "DZ", "Tipaza", 36.66, 2.74, "operating since 2025", 300000, "seawater", "grid", "Algiers / Tipaza / Blida", WIKI),
 e("Cap Djinet SWRO", "DZ", "Boumerdès", 36.87, 3.72, "operating since 2012", 100000, "seawater", "grid", "Boumerdès", WIKI),
 e("Cap Djinet 2 SWRO", "DZ", "Boumerdès", 36.88, 3.73, "operating since 2025-03", 300000, "seawater", "grid", "Boumerdès / E Algiers / Tizi Ouzou", WIKI),
 e("Beni Saf SWRO", "DZ", "Aïn Témouchent", 35.30, -1.38, "operating since 2009", 200000, "seawater", "grid", "Oran / Aïn Témouchent", WIKI),
 e("Honaine SWRO", "DZ", "Tlemcen", 35.17, -1.65, "operating since 2011", 200000, "seawater", "grid", "Tlemcen", WIKI),
 e("Souk Tlata SWRO", "DZ", "Tlemcen", 35.12, -1.87, "operating since 2011", 200000, "seawater", "grid", "Tlemcen", WIKI),
 e("Mostaganem SWRO", "DZ", "Mostaganem", 35.93, 0.09, "operating since 2012", 200000, "seawater", "grid", "Mostaganem", WIKI),
 e("Magtaa SWRO (Oran)", "DZ", "Oran", 35.80, -0.30, "operating since 2014", 500000, "seawater", "grid", "Oran — largest in Africa until Casablanca", WIKI, "Hyflux"),
 e("Cap Blanc SWRO (Oran)", "DZ", "Oran", 35.82, -0.87, "operating since 2025", 300000, "seawater", "grid", "Oran", WIKI),
 e("Ténès SWRO", "DZ", "Chlef", 36.52, 1.30, "operating since 2015", 200000, "seawater", "grid", "Chlef", WIKI),
 e("Skikda SWRO", "DZ", "Skikda", 36.88, 6.90, "operating since 2009", 100000, "seawater", "grid", "Skikda", WIKI),
 e("Koudiet Eddraouche SWRO", "DZ", "El Tarf", 36.87, 7.78, "operating since 2025", 300000, "seawater", "grid", "El Tarf / Annaba", WIKI),
 e("Tighremt (Béjaïa) SWRO", "DZ", "Béjaïa", 36.65, 5.00, "under construction", 300000, "seawater", "grid", "Béjaïa", WIKI),
 e("Algeria 2030 programme (Tlemcen, Chlef, Mostaganem + 6 sites)", "DZ", "national", 35.5, 1.5, "planned — target 5.6–5.8 M m³/d by 2030, incl. inland groundwater desal in the south", None, "seawater + brackish groundwater", "grid", "national", WIKI),
 # ---------- Morocco ----------
 e("Casablanca SWRO", "MA", "Casablanca-Settat (Bir Jdid)", 33.37, -8.00, "under construction — phase 1 2026, 548k→822k m³/d", 548000, "seawater", "grid + renewables (planned)", "Casablanca metro ~7.5 M", SWM_MA, "ACCIONA / Afriquia-Green of Africa"),
 e("Agadir–Chtouka SWRO", "MA", "Souss-Massa", 30.25, -9.60, "operating since 2022 — 275k, expandable 400k", 275000, "seawater", "grid", "Agadir drinking water + Chtouka irrigation", SWM_MA, "Coxabengoa / SEDA"),
 e("Jorf Lasfar OCP SWRO", "MA", "El Jadida", 33.12, -8.63, "operating — 75k→100k", 100000, "seawater", "grid (OCP)", "OCP phosphate + El Jadida", SWM_MA, "OCP"),
 e("Safi OCP SWRO", "MA", "Safi", 32.30, -9.25, "operating / expanding to 2026", 100000, "seawater", "grid (OCP)", "OCP Safi + city", SWM_MA, "OCP"),
 e("Laayoune SWRO", "MA", "Laayoune-Sakia El Hamra", 27.15, -13.20, "operating", 62000, "seawater", "grid", "Laayoune", SWM_MA, "ONEE"),
 e("Al Hoceima SWRO", "MA", "Tanger-Tétouan-Al Hoceima", 35.25, -3.93, "operating since 2020", 17300, "seawater", "grid", "Al Hoceima", SWM_MA, "Tedagua"),
 e("Dakhla wind-powered SWRO", "MA", "Dakhla-Oued Ed-Dahab", 23.70, -15.93, "under construction", 100000, "seawater", "wind (dedicated farm)", "Dakhla + 5,000 ha irrigation", SWM_MA, "DAWEC (Engie + Nareva)"),
 e("Tarfaya OCP SWRO", "MA", "Tarfaya", 27.94, -12.93, "planned", 164000, "seawater", "renewables (planned)", "OCP / Tan-Tan region", SWM_MA, "OCP"),
 e("Essaouira SWRO", "MA", "Essaouira", 31.51, -9.77, "planned", 145000, "seawater", "grid", "Essaouira region", SWM_MA),
 e("Guelmim SWRO", "MA", "Guelmim", 28.98, -10.06, "planned", 96000, "seawater", "grid", "Guelmim region", SWM_MA),
 e("Oriental (Nador) SWRO", "MA", "Oriental", 35.17, -2.93, "planned — tender", 274000, "seawater", "grid", "Nador / Oujda region", SWM_MA),
 e("Tangier SWRO", "MA", "Tanger", 35.76, -5.83, "stalled", None, "seawater", "grid", "Tangier", SWM_MA),
 # ---------- Tunisia ----------
 e("Djerba SWRO", "TN", "Médenine", 33.80, 10.85, "operating since 2018 — extension seeking finance", 50000, "seawater", "grid", "Djerba island", "https://kapitalis.com/tunisie/2026/06/20/entree-en-service-dune-usine-de-dessalement-a-sfax/", "SONEDE"),
 e("Zarat (Gabès) SWRO", "TN", "Gabès", 33.68, 10.35, "operating since 2024 — doubling to 100k announced 2025", 50000, "seawater", "grid", "Gabès, Matmata, El Hamma", "https://www.tunisienumerique.com/zarat-va-doubler-sa-capacite-de-dessalement-pour-repondre-a-la-crise-de-leau-a-gabes/", "SONEDE"),
 e("Sfax (Gargour) SWRO", "TN", "Sfax", 34.62, 10.72, "operating since 2026-06 — expandable 200k", 100000, "seawater", "grid", "~600,000 in Sfax region", "https://kapitalis.com/tunisie/2026/06/20/entree-en-service-dune-usine-de-dessalement-a-sfax/", "SONEDE (JICA loan)"),
 e("Sousse SWRO", "TN", "Sousse", 35.75, 10.70, "commissioning 2026 — expandable 100k", 50000, "seawater", "grid", "Sousse / Sahel", "https://kapitalis.com/tunisie/2026/06/20/entree-en-service-dune-usine-de-dessalement-a-sfax/", "SONEDE"),
 # ---------- Egypt ----------
 e("Kilo 17 (El Arish) SWRO", "EG", "North Sinai", 31.13, 33.75, "operating", 100000, "seawater", "grid", "El Arish", DNE),
 e("Yusr SWRO", "EG", "Red Sea (Hurghada area)", 27.20, 33.83, "operating", 80000, "seawater", "grid", "Red Sea coast", DNE),
 e("Rumaila 1–3 SWRO", "EG", "South Sinai", 28.10, 33.60, "operating", 60000, "seawater", "grid", "South Sinai", DNE),
 e("Rumaila 4 SWRO", "EG", "South Sinai", 28.10, 33.61, "operating", 65000, "seawater", "grid", "South Sinai", DNE),
 e("Ras Sidr / Abu Zenima / New Nuweiba SWRO", "EG", "South Sinai", 29.60, 32.72, "operating (3 plants)", 65000, "seawater", "grid", "Gulf of Suez / Aqaba towns", DNE),
 e("El-Tor + New Dahab SWRO", "EG", "South Sinai", 28.24, 33.62, "operating (2 plants)", 45000, "seawater", "grid", "El Tor, Dahab", DNE),
 e("Sharm El-Sheikh SWRO", "EG", "South Sinai", 27.91, 34.33, "operating", 30000, "seawater", "grid", "Sharm El-Sheikh", DNE),
 e("El Dabaa SWRO", "EG", "Matrouh", 31.03, 28.44, "operating", 40000, "seawater", "grid", "Dabaa", DNE),
 e("Egypt national desal programme (19 under construction)", "EG", "national", 28.5, 31.0, "under construction — 687k m³/d; 10 M m³/d target 2050; Suez & Port Said PPPs in tender", 687000, "seawater", "grid + solar (PPP phase)", "national — ~129 plants / 1.4 M m³/d already operating", DNE),
 # ---------- West Africa ----------
 e("Mamelles (Dakar) SWRO", "SN", "Dakar", 14.72, -17.50, "commissioning ~2025 — 50k→100k", 50000, "seawater", "grid", "Dakar metro", "https://www.jica.go.jp/english/overseas/senegal/", "SONES / Toyota Tsusho–Eiffage–Wabag (JICA)"),
 e("Teshie-Nungua SWRO", "GH", "Greater Accra", 5.59, -0.10, "IDLE — commissioned 2015, shut 2018/2019/2024; $235M arbitration award 2026", 60000, "seawater", "grid", "~500,000 in Teshie / Nungua", "https://www.myjoyonline.com/explained-ghanas-water-plant-deal-that-produced-a-235m-judgment-debt-instead-of-water-for-500000-people/", "Befesa Ghana (Abengoa → Cox)"),
 # ---------- East Africa ----------
 e("Kiunga solar SWRO (GivePower)", "KE", "Lamu", -1.74, 41.49, "operating since 2018 — award-winning", 75, "seawater", "solar PV + battery", "~25,000–35,000 people, Kiunga & villages", "https://nation.africa/kenya/climate/lamu-s-solar-desalination-plant-wins-global-award-for-transforming-border-community-5393838", "GivePower"),
 e("Likoni solar SWRO (GivePower)", "KE", "Mombasa", -4.08, 39.66, "operating since 2020", 70, "seawater", "solar PV + battery", "Likoni community", "https://en.wikipedia.org/wiki/GivePower", "GivePower"),
 e("Mombasa Mainland SWRO", "KE", "Mombasa", -4.02, 39.62, "planned since 2018 — not built", 100000, "seawater", "grid", "Mombasa North Mainland", "https://en.wikipedia.org/wiki/Mombasa_Mainland_Desalination_Plant", "Almar Water Solutions / Mombasa County"),
 e("Likoni Major SWRO", "KE", "Mombasa", -4.09, 39.65, "planned — not built", 70000, "seawater", "grid", "Likoni / South Coast", "https://en.wikipedia.org/wiki/Mombasa_Mainland_Desalination_Plant", "Aqua Swiss"),
 e("Djibouti PEPER solar SWRO (Doraleh)", "DJ", "Djibouti", 11.58, 43.08, "operating since 2021 — phase 2 adds 46 MW solar", 22500, "seawater", "grid + solar PV (EU-funded)", "~250,000 in Djibouti city", "https://www.esi-africa.com/news/djibouti-solar-powered-desalination-plant-to-tackle-water-scarcity/", "ONEAD / Eiffage-Tedagua"),
 # ---------- Southern Africa ----------
 e("Erongo (Orano) SWRO", "NA", "Erongo — 35 km N of Swakopmund", -22.35, 14.40, "operating since 2010 — 17.6 M m³ in 2025 (record)", 62000, "seawater", "grid", "Uranium mines + NamWater (Swakopmund/Walvis Bay)", "https://thebrief.com.na/2026/01/oranos-erongo-plant-produces-record-17-6m-m%C2%B3-of-water-in-2025/", "Orano Mining Namibia"),
 e("Erongo 2 (NamWater–Swakop Uranium) SWRO", "NA", "Erongo — Mile 6", -22.55, 14.50, "planned — N$2.1 bn JV approved 2025", 20000, "seawater", "grid", "Central coast + mines", "https://www.namibiansun.com/", "NamWater / Swakop Uranium"),
 e("Mossel Bay SWRO", "ZA", "Western Cape", -34.18, 22.14, "operating since 2011 (standby/partial)", 15000, "seawater", "grid", "Mossel Bay + PetroSA", WIKI, "Mossel Bay Municipality"),
 e("Saldanha Bay SWRO", "ZA", "Western Cape", -33.01, 17.94, "operating", 2400, "seawater", "grid", "Saldanha", WIKI),
 e("Knysna SWRO", "ZA", "Western Cape", -34.04, 23.05, "operating / standby", 2000, "seawater", "grid", "Knysna", WIKI),
 e("Plettenberg Bay SWRO", "ZA", "Western Cape", -34.05, 23.37, "operating / standby", 2000, "seawater", "grid", "Plettenberg Bay", WIKI),
 e("Bushman's River SWRO", "ZA", "Eastern Cape", -33.69, 26.66, "operating", 1800, "seawater", "grid", "Bushman's River Mouth / Kenton", WIKI),
 e("Lambert's Bay SWRO", "ZA", "Western Cape", -32.09, 18.30, "operating", 1700, "seawater", "grid", "Lambert's Bay", WIKI),
 e("Witsand solar SWRO (Osmosun)", "ZA", "Western Cape", -34.39, 20.84, "operating since 2018-12 — 100 m³/d solar-direct, 300 m³/d with grid", 100, "seawater", "solar PV (no battery, Osmosun)", "Witsand village", "https://en.wikipedia.org/wiki/Witsand_Solar_Desalination_Plant", "Mascara / Hessequa Municipality"),
 e("Cape Town Paarden Eiland SWRO", "ZA", "Western Cape", -33.90, 18.47, "planned — 50–70 ML/d, feasibility/procurement", 50000, "seawater", "grid", "Cape Town", "https://african.business/2021/10/energy-resources/can-desalination-plants-solve-africas-water-crisis", "City of Cape Town"),
]

existing = {(p["name"], p["country"]) for p in d["plants"]}
added = [p for p in A if (p["name"], p["country"]) not in existing]
d["plants"].extend(added)
d["_readme"] = ("Curated list of existing, planned, under-construction, stalled or cancelled desalination plants: "
                "Colombia, Bahamas, Caribbean, South America and Africa. Coordinates marked approx:true are the "
                "town/community, not the plant parcel. Every entry has a source URL. Updated 2026-11-07.")
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(f"added {len(added)}, total {len(d['plants'])}")
