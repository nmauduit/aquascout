#!/usr/bin/env python3
"""Append solar / renewable-powered desalination plants to data/planned-desal.json."""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data" / "planned-desal.json"
d = json.loads(P.read_text())

OSM = "https://www.osmosun.com/en/our-locations/our-references/"
GP = "https://givepower.org/wp-content/uploads/2024-Annual-Report_FIN.pdf"
ATM = "https://www.atmosfair.de/en/climate-protection-projects/solar-energy/kenia-solar-powered-water-treatment-plants/"
def e(name, cc, region, lat, lon, status, cap, feed, power, serves, source, operator=None, tech="RO", approx=True):
    return {"name": name, "country": cc, "region": region, "lat": lat, "lon": lon, "approx": approx,
            "status": status, "capacity_m3d": cap, "feed": feed, "power": power, "technology": tech,
            "serves": serves, "operator": operator, "source": source}
PV = "solar PV (Osmosun, battery-free)"
A = [
 # ---- utility-scale solar-powered / solar-assisted ----
 e("Al Khafji solar SWRO", "SA", "Al Khafji, Eastern Province", 28.43, 48.50, "operating since ~2018 — first large-scale solar SWRO (hybrid solar + grid)", 60000, "seawater", "solar PV 10 MW + grid", "Al Khafji", "https://en.wikipedia.org/wiki/Al-Khafji_solar_desalination_plant", "SWCC / KACST (AWT–Abengoa)"),
 e("Sharqiyah (Sur) SWRO — solar farm", "OM", "Sur", 22.55, 59.50, "operating — 17 MWp PV since 2023-11 covers 100 % of daytime load", 131000, "seawater", "solar PV 17 MWp + grid", "Sharqiyah governorate", "https://www.omanobserver.om/article/1188047/business/oman-expands-solar-use-in-water-desalination", "Veolia / TotalEnergies"),
 e("Barka 5 SWRO — solar", "OM", "Barka", 23.72, 57.88, "operating since 2024-09; 6.5 MW PV commissioned 2026 (~11 % of energy)", 100000, "seawater", "grid + solar PV 6.5 MW", "Muscat / Batinah", "https://www.omanobserver.om/article/1188047/business/oman-expands-solar-use-in-water-desalination", "GS Inima"),
 e("Ghantoot renewable-energy desal pilot (Masdar)", "AE", "Ghantoot, Abu Dhabi", 24.87, 54.85, "pilot 2013–2018 — 5 vendors (Abengoa, Suez, Veolia, Trevi, Mascara/Osmosun); up to 75 % energy saving", None, "seawater", "solar PV / solar thermal", "test bed", "https://masdar.ae/en/news/newsroom/masdars-renewable-energy-desalination-pilot-programme-finds-solar-energy-powered-desalination", "Masdar"),
 e("Marsa Shagra solar SWRO (KarmWater)", "EG", "Marsa Alam, Red Sea", 25.25, 34.80, "operating — 30 % solar now, 100 % by 2033; 25-yr water purchase agreement", 300, "seawater", "solar PV (partial) + grid", "Red Sea Diving Safari resort", "https://www.zawya.com/en/projects/utilities/karmwater-opens-1st-solar-powered-desalination-plant-in-marsa-alam-y7mgzspk", "KarmWater"),
 e("Canada Industrial Estate solar SWRO ×2", "KN", "St Kitts", 17.30, -62.72, "under construction since 2024-03 (UAE–CREF funded) — 2 plants, 12 m³/h", 288, "seawater", "solar PV", "St Kitts", "https://wicnews.com/caribbean/st-kitts-and-nevis-govt-breaks-ground-to-construct-2-solar-powered-water-desalination-plants-321669526", "Govt of St Kitts & Nevis / UAE-CREF"),
 e("Tuvalu SolarRO SW40 container", "TV", "outer atolls", -7.48, 178.68, "delivered 2025 — 1.6 m³/h, 21.5 kW PV, optional battery", 38, "seawater", "solar PV 21.5 kW", "remote atoll community", "https://solarwatersolutions.com/news/solar-desalination-brings-clean-water-to-remote-pacific-islands-in-tuvalu/", "Solar Water Solutions"),
 e("Ksar Ghilène PV-RO", "TN", "Kebili (Sahara oasis)", 32.98, 9.63, "operating since 2006 — autonomous PV-RO, 8+ yrs uninterrupted (ITC/CIEMAT)", None, "brackish groundwater", "solar PV + battery", "oasis village ~300", "https://link.springer.com/chapter/10.1007/978-1-4020-9892-5_8", "SONEDE / ITC Canarias"),
 # ---- GivePower solar water farms (PV + battery, containerised SWRO/BWRO) ----
 e("GivePower Bamburi solar water farm", "KE", "Mombasa", -3.98, 39.72, "operating since 2021-06", 75, "seawater/brackish", "solar PV + battery", "Bamburi", GP, "GivePower"),
 e("GivePower Mtongwe solar water farm", "KE", "Mombasa", -4.09, 39.64, "operating since 2022-12", 75, "seawater/brackish", "solar PV + battery", "Mtongwe", GP, "GivePower"),
 e("GivePower Mshomoroni solar water farm", "KE", "Mombasa", -4.00, 39.68, "operating since 2023-08", 75, "brackish", "solar PV + battery", "Mshomoroni", GP, "GivePower"),
 e("GivePower Migadini solar water farm", "KE", "Mombasa", -4.03, 39.65, "operating since 2024-06", 75, "brackish", "solar PV + battery", "~130,000 people", GP, "GivePower"),
 e("GivePower Mtwapa solar water farm", "KE", "Kilifi", -3.95, 39.74, "operating since 2024-11", 75, "brackish", "solar PV + battery", "Mtwapa (~90,000)", GP, "GivePower"),
 e("GivePower Ukunda solar water farm (Mobi+)", "KE", "Kwale", -4.28, 39.57, "operating since 2024-12", 15, "brackish", "solar PV + battery", ">38,000 people", GP, "GivePower"),
 e("GivePower Mokowe solar water farm (Mobi)", "KE", "Lamu", -2.25, 40.85, "operating since 2022-06", 15, "brackish", "solar PV + battery", "Mokowe", GP, "GivePower"),
 e("GivePower Kitengela solar water farm", "KE", "Kajiado", -1.47, 36.96, "operating since 2022-05", 75, "brackish borehole (fluoride)", "solar PV + battery", "Kitengela", GP, "GivePower"),
 e("GivePower Kajiado Town solar water farm (Mobi+)", "KE", "Kajiado", -1.85, 36.78, "operating since 2023-07", 15, "brackish borehole", "solar PV + battery", "Kajiado", GP, "GivePower"),
 e("GivePower Wote / Makindu / Mwingi (Mobi+) ", "KE", "Makueni / Kitui", -2.28, 37.83, "operating 2022–2024 — 3 inland brackish units", 15, "brackish borehole", "solar PV + battery", "Ukambani towns", GP, "GivePower"),
 e("GivePower Anse-à-Galets solar water farm", "HT", "La Gonâve", 18.83, -72.87, "operating since 2020-05", 75, "seawater", "solar PV + battery", "La Gonâve island", GP, "GivePower"),
 e("GivePower Pointe-à-Raquette solar water farm (Mobi+)", "HT", "La Gonâve", 18.78, -73.12, "operating since 2023-04", 15, "seawater/brackish", "solar PV + battery", "La Gonâve west", GP, "GivePower"),
 e("GivePower Cabo de la Vela solar water farm (Mobi)", "CO", "Uribia, La Guajira", 12.20, -72.17, "operating since 2021-10", 15, "seawater", "solar PV + battery", "Wayuu community", GP, "GivePower"),
 # ---- Boreal Light / WaterKiosk ----
 e("WaterKiosk / Boreal Light solar RO kiosks (34 sites)", "KE", "coast + Wajir/Garissa/Turkana (Mombasa Old Town, Diani, Likoni, Nyali, Mtwapa, Lodwar ×2, Wajir ×4, Habaswein, Takaba, Garissa, Voi…)", -3.60, 39.80, "operating — 34 locations by 2023 (pilot Burani 2019)", None, "brackish borehole / seawater", "solar PV (Planet Cube ASW2000)", "kiosk water sales", ATM, "WaterKiosk Africa / Boreal Light"),
 e("Kibaha solar RO (WaterKiosk Africa)", "TZ", "Kibaha, Pwani", -6.77, 38.92, "operating since 2022-01 — largest solar desal in Tanzania", 100, "brackish borehole", "solar PV", "Kibaha", "https://pumps-africa.com/solar-powered-desalination-system-inaugurated-in-kibaha-tanzania/", "Boreal Light / DEG"),
 # ---- Osmosun (Mascara) battery-free PV-RO references ----
 e("Bora Bora Osmosun 13 SW", "PF", "Bora Bora", -16.50, -151.74, "operating", 80, "seawater", PV, "resort/community", OSM, "Osmosun"),
 e("Hao + Nukutepipi Osmosun SW", "PF", "Tuamotu", -18.07, -140.95, "operating (2 islands)", None, "seawater", PV, "atoll communities", OSM, "Osmosun"),
 e("Rodrigues Island Osmosun SW", "MU", "Rodrigues", -19.70, 63.42, "operating — first solar desal in Indian Ocean", 20, "seawater", PV, "Rodrigues (up to 60 m³/d)", OSM, "Osmosun / CWA"),
 e("Ileret Osmosun BW (Turkana Basin Institute)", "KE", "Marsabit, Lake Turkana", 4.31, 36.23, "operating", 20, "brackish", PV, "research station + community", OSM, "Osmosun"),
 e("Bethanie Osmosun BW (NamWater)", "NA", "ǁKaras", -26.50, 17.15, "operating — Adaptation Fund", None, "brackish groundwater", PV, "Bethanie village", OSM, "NamWater"),
 e("Gandiaye Osmosun BW (GIZ)", "SN", "Kaolack", 14.23, -16.27, "operating — ~5,000 inhabitants", None, "brackish groundwater", PV, "Gandiaye", OSM, "Osmosun / GIZ"),
 e("Moia Moia + Brava Osmosun", "CV", "Santiago / Brava", 15.08, -23.52, "operating (2 units)", None, "brackish + seawater", PV, "villages", OSM, "Osmosun"),
 e("Gaza province Osmosun BW ×2", "MZ", "Gaza", -24.00, 33.50, "operating — rural drinking water", None, "brackish groundwater", PV, "rural communities", OSM, "Osmosun"),
 e("Tica Osmosun SW", "MZ", "Sofala", -19.40, 34.60, "operating", None, "seawater", PV, "Tica", OSM, "Osmosun"),
 e("Tulear Osmosun BW ×2", "MG", "Toliara", -23.35, 43.67, "operating", None, "brackish", PV, "Toliara town", OSM, "Osmosun"),
 e("Mogadishu Osmosun container SW", "SO", "Mogadishu", 2.05, 45.32, "commissioned ~2020", None, "seawater", PV, "Mogadishu", OSM, "Osmosun"),
 e("Lac du Goubet Osmosun SW", "DJ", "Goubet", 11.55, 42.60, "operating — 10 M litres produced", None, "seawater", PV, "Goubet community", OSM, "Osmosun"),
 e("Nouadhibou Osmosun SW", "MR", "Nouadhibou", 20.93, -17.03, "operating", None, "seawater", PV, "Nouadhibou", OSM, "Osmosun"),
 e("Tagant + Tiris Zemmour Osmosun BW", "MR", "inland Mauritania", 18.55, -11.50, "operating (2 sites)", None, "brackish groundwater", PV, "oasis towns", OSM, "Osmosun"),
 e("Guelmim-Oued Noun Osmosun BW", "MA", "Guelmim", 28.98, -10.06, "operating — first Osmosun unit in Morocco", None, "brackish groundwater", PV, "agricultural/rural", OSM, "Osmosun"),
 e("Ad-Dakhla oasis Osmosun BW", "EG", "New Valley", 25.50, 29.00, "operating", None, "brackish groundwater", PV, "Dakhla oasis", OSM, "Osmosun"),
 e("Fathkait wind/solar BW", "OM", "Dhofar", 17.50, 54.50, "operating — wind-powered", None, "brackish", "wind + solar", "local population", OSM, "Osmosun"),
 e("Papagarang Island Osmosun", "ID", "Komodo, NTT", -8.53, 119.62, "operating", None, "seawater", PV, "island community", OSM, "Osmosun"),
 e("Dinagat Islands Osmosun Nomad", "PH", "Dinagat", 10.13, 125.60, "deployed 2021-12 — Typhoon Odette response", None, "seawater", PV, "disaster response", OSM, "Osmosun"),
 e("Poum Osmosun SW", "NC", "New Caledonia north", -20.23, 164.02, "operating", None, "seawater", PV, "Poum", OSM, "Osmosun"),
 e("Malekula islets Osmosun SW ×6 (Wala, Rano, Vao, Atchin)", "VU", "Malampa", -15.93, 167.40, "operating — 6 installations", None, "seawater", PV, "small-island communities", OSM, "Osmosun"),
 e("Europa Island Osmosun Nomad", "FR", "Îles Éparses", -22.37, 40.37, "operating", None, "seawater", PV, "military/scientific base", OSM, "Osmosun"),
 e("Dubbo Osmosun (Australia)", "AU", "NSW", -32.25, 148.60, "operating", None, "brackish", PV, "demonstration", OSM, "Osmosun"),
]

existing = {(p["name"], p["country"]) for p in d["plants"]}
added = [p for p in A if (p["name"], p["country"]) not in existing]
d["plants"].extend(added)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(f"added {len(added)}, total {len(d['plants'])}")
