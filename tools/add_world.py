#!/usr/bin/env python3
"""Append rest-of-world desalination plants (Gulf/Middle East, Asia, Pacific, North America, Chile, Caribbean, Cabo Verde)."""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data" / "planned-desal.json"
d = json.loads(P.read_text())

WIKI = "https://en.wikipedia.org/wiki/Desalination_by_country"
BR_SA = "https://www.blackridgeresearch.com/blog/latest-list-of-top-largest-biggest-desalination-desal-water-treatment-plants-projects-saudi-arabia-ksa-middle-east-gcc"
BR_W = "https://www.blackridgeresearch.com/blog/latest-list-worlds-largest-biggest-water-treatment-desalination-plants-projects-capacity-cost-location-project-detail"
LYN = "https://lynceans.org/all-posts/status-of-desalination-plants-in-california-2/"
SOPAC = "https://gsd.spc.int/sopac/docs/SOPAC%20Technical%20Report%20437%20Desalination%20for%20Pacific%20Island%20Countries.pdf"
CPI = "https://cpichile.org/los-proximos-proyectos-de-desalinizacion-en-chile/"
ENC = "https://encyclopedia.pub/9223"
def e(name, cc, region, lat, lon, status, cap, feed, power, serves, source, operator=None, tech="RO", approx=True):
    return {"name": name, "country": cc, "region": region, "lat": lat, "lon": lon, "approx": approx,
            "status": status, "capacity_m3d": cap, "feed": feed, "power": power, "technology": tech,
            "serves": serves, "operator": operator, "source": source}
SW, G = "seawater", "grid"

A = [
 # ===== Saudi Arabia =====
 e("Shoaiba power & desalination complex", "SA", "Mecca Province", 20.67, 39.52, "operating — world's largest complex (MSF + RO phases)", 2998000, SW, "co-generation", "Jeddah / Mecca / Taif", WIKI, "SWCC", tech="MSF + RO"),
 e("Ras Al Khair IWPP", "SA", "Eastern Province", 27.55, 49.20, "operating since 2014 — hybrid MSF+RO, 2.4 GW", 1036000, SW, "co-generation", "Riyadh / Eastern Province", WIKI, "SWCC", tech="MSF + RO"),
 e("Jubail JWAP (MED)", "SA", "Jubail", 27.03, 49.62, "operating since 2010", 800000, SW, "co-generation", "Jubail industrial city", BR_SA, "Marafiq", tech="MED"),
 e("Jubail 3A SWRO", "SA", "Jubail", 27.05, 49.60, "operating since 2023", 600000, SW, G, "Riyadh / Qassim", BR_SA, "ACWA Power"),
 e("Al Khobar 2 SWRO", "SA", "Al Khobar", 26.25, 50.20, "operating since 2018", 630000, SW, G, "Eastern Province", BR_SA, "SWCC"),
 e("Jeddah desalination complex", "SA", "Jeddah", 21.75, 39.10, "operating (phases since 1994)", 364000, SW, "co-generation", "Jeddah", WIKI, "SWCC"),
 e("Yanbu complex (MSF/MED/RO)", "SA", "Yanbu, Medina Province", 24.03, 38.07, "operating (1998; MED expansion)", 467000, SW, "co-generation", "Medina / Yanbu", WIKI, "SWCC", tech="MSF + MED + RO"),
 e("Yanbu 4 SWRO", "SA", "Ar Rayis, Medina Province", 23.60, 38.60, "operating since 2023", 450000, SW, G, "Medina", BR_SA, "SWCC / Lantania"),
 e("Rabigh 3 SWRO", "SA", "Rabigh", 22.80, 39.03, "operating since 2022", 600000, SW, G, "Mecca / Jeddah", BR_SA, "ACWA Power"),
 e("Rabigh 4 SWRO", "SA", "Rabigh", 22.82, 39.02, "online 2026-05", 600000, SW, G, "Mecca / Jeddah", "https://www.mees.com/2026/5/15/news-in-brief/saudis-rabigh-4-desalination-plant-brought-online/bbf4c1c0-505f-11f1-b35e-596b88c62fc2", "SWPC / ACWA"),
 e("Ras Mohaisen SWRO", "SA", "Al Qunfudhah, Mecca Province", 19.13, 41.08, "under construction", 300000, SW, G, "Al Baha / Mecca south", "https://www.lantania.com/en/lantania-will-build-ras-mohaisen-desalination-plant-in-the-kingdom-of-saudi-arabia/", "SWCC / Lantania"),
 e("Shuqaiq 3 SWRO", "SA", "Shuqaiq, Jazan Province", 17.68, 42.03, "operating since 2021", 450000, SW, G, "Jazan / Asir", WIKI, "ACWA Power / Marubeni"),
 # ===== UAE =====
 e("Jebel Ali power & desalination complex", "AE", "Dubai", 24.98, 55.07, "operating — 43 MSF units + 2 SWRO", 2227600, SW, "co-generation", "Dubai", WIKI, "DEWA", tech="MSF + RO"),
 e("Taweelah RO", "AE", "Abu Dhabi", 24.75, 54.72, "operating since 2022/23 — world's largest RO until Sorek B", 909200, SW, "grid + solar PV", "Abu Dhabi", WIKI, "ACWA Power / EWEC"),
 e("Taweelah A1/A2/B (MSF/MED)", "AE", "Abu Dhabi", 24.76, 54.70, "operating (1999–2005)", 1349800, SW, "co-generation", "Abu Dhabi", WIKI, "TAQA", tech="MSF/MED"),
 e("Shuweihat S1 + S2", "AE", "Al Ruwais, Abu Dhabi", 24.13, 52.60, "operating (2001, 2009)", 918000, SW, "co-generation", "Abu Dhabi west", WIKI, "TAQA", tech="MSF"),
 e("Fujairah F1 + F2", "AE", "Fujairah (Qidfa)", 25.30, 56.37, "operating (2006, 2007) — hybrid MSF/MED + RO", 1195500, SW, "co-generation", "Abu Dhabi + Northern Emirates", WIKI, "EWEC", tech="MSF/MED + RO"),
 e("Umm Al Quwain IWP (RO)", "AE", "Umm Al Quwain", 25.55, 55.60, "operating since 2023", 681900, SW, G, "Northern Emirates", BR_W, "ACWA Power / FEWA"),
 e("Umm Al Nar", "AE", "Abu Dhabi", 24.45, 54.50, "operating since 2003", 432000, SW, "co-generation", "Abu Dhabi", WIKI, tech="MSF"),
 e("Mirfa IWPP", "AE", "Mirfa, Abu Dhabi", 24.11, 53.45, "operating since 2014", 241000, SW, "co-generation", "Al Dhafra", WIKI, "Mirfa IPWC", tech="MSF + RO"),
 e("Hamriyah SWRO", "AE", "Sharjah", 25.47, 55.49, "operating", 90000, SW, G, "Sharjah", WIKI, "SEWA"),
 e("Ghalilah SWRO", "AE", "Ras Al Khaimah", 25.98, 56.07, "operating", 68000, SW, G, "RAK", WIKI, "Aquatech"),
 e("Khor Fakkan + Kalba + Layyah SWRO", "AE", "Sharjah east coast", 25.34, 56.35, "operating (small units)", 60000, SW, G, "Sharjah east coast", WIKI, "SEWA"),
 # ===== Qatar / Kuwait / Bahrain / Oman =====
 e("Ras Abu Fontas (RAF A/A2/A3/B)", "QA", "Doha", 25.20, 51.62, "operating (1981→)", 160000, SW, "co-generation", "Doha", WIKI, "Kahramaa", tech="MSF + RO"),
 e("Qatar planned desal (735k, Facility E etc.)", "QA", "Qatar", 25.00, 51.50, "planned — 735,000 m³/d in two projects", 735000, SW, "co-generation", "Qatar", WIKI, "Kahramaa"),
 e("Az-Zour power & desalination", "KW", "Al Ahmadi", 28.72, 48.38, "operating", 524000, SW, "co-generation", "Kuwait", WIKI, "MEW", tech="MSF + RO"),
 e("Doha West + Doha East", "KW", "Jahra", 29.35, 47.82, "operating", 693000, SW, "co-generation", "Kuwait City", WIKI, "MEW", tech="MSF"),
 e("Subiya", "KW", "Jahra", 29.60, 48.10, "operating", 455000, SW, "co-generation", "Kuwait", WIKI, "MEW", tech="MSF"),
 e("Shuaiba North + South", "KW", "Al Ahmadi", 29.05, 48.15, "operating", 341000, SW, "co-generation", "Kuwait", WIKI, "MEW", tech="MSF + RO"),
 e("Shuwaikh", "KW", "Kuwait City", 29.37, 47.93, "operating", 225000, SW, G, "Kuwait City", WIKI, "MEW"),
 e("Al Hidd power & desalination", "BH", "Muharraq", 26.22, 50.65, "operating since 2000", 272760, SW, "co-generation", "Bahrain", WIKI, "Al Hidd Power Co", tech="MSF + MED"),
 e("Durrat Al Bahrain SWRO", "BH", "Durrat Al Bahrain", 25.85, 50.62, "planned", 36000, SW, G, "Durrat resort islands", WIKI, "Energy Central"),
 e("Barka 4 SWRO", "OM", "Ar Rumays, Al Batinah", 23.70, 57.85, "operating since 2018", 281000, SW, G, "Muscat / Batinah", WIKI, "Suez / Barka Desalination Co"),
 e("Ghubrah power & desalination", "OM", "Muscat", 23.62, 58.50, "operating (MSF + RO phases)", None, SW, "co-generation", "Muscat", WIKI, "OPWP", tech="MSF + RO"),
 e("Sur SWRO", "OM", "Sur", 22.57, 59.52, "operating since 2009", 80000, SW, G, "Sharqiyah", WIKI, "Veolia / Sharqiyah Desalination"),
 e("Sohar power & desalination", "OM", "Sohar", 24.47, 56.62, "operating", None, SW, "co-generation", "Sohar", WIKI),
 # ===== Iran / Iraq / Jordan / Kazakhstan =====
 e("Bandar Abbas – Persian Gulf water transfer (WASCO)", "IR", "Hormozgan", 27.10, 56.05, "phased — phase 1 ~2024, feeds Kerman/Yazd pipeline", None, SW, G, "Hormozgan + central plateau industry", WIKI, "WASCO"),
 e("Basra (Grand Faw) mega SWRO", "IQ", "Basra", 29.98, 48.47, "under construction since 2025-07 — 3 × 335k lines + 300 MW plant", 1000000, SW, "dedicated 300 MW power plant", "Basra governorate", "https://www.iraq-businessnews.com/2025/07/26/work-starts-at-major-seawater-desalination-project-in-basra/", "PowerChina / Al-Rida"),
 e("Aqaba–Amman Water Desalination & Conveyance", "JO", "Aqaba", 29.45, 34.98, "planned — construction 2027, first water 2030; 300 Mm³/yr, 450 km pipeline, US$2.5 bn+", 851000, "seawater (Red Sea)", "solar PV (310–724 MW dedicated)", "Amman + governorates", "https://en.wikipedia.org/wiki/Aqaba%E2%80%93Amman_Water_Desalination_and_Conveyance_Project", "MWI / Meridiam–SUEZ"),
 e("MAEK Aktau (nuclear-era) desal", "KZ", "Aktau, Mangystau", 43.65, 51.17, "operating since 1968 (modernised 2023)", 120000, "Caspian seawater", "co-generation", "Aktau", WIKI, "MAEK-Kazatomprom", tech="MED/MSF + RO"),
 e("Caspiy SWRO", "KZ", "Aktau", 43.60, 51.20, "operating since 2011", 20000, "Caspian seawater", G, "Aktau", WIKI),
 e("Kendirli SWRO", "KZ", "Mangystau (S of Zhanaozen)", 42.80, 52.00, "operating since 2025-07", 50000, "Caspian seawater", G, "Zhanaozen region", WIKI),
 # ===== East / South / SE Asia =====
 e("Tianjin Beijiang power-plant MED", "CN", "Tianjin", 39.20, 117.90, "operating — never above ~25 % capacity", 200000, SW, "co-generation (coal)", "Tianjin / Beijing supply", WIKI, tech="MED"),
 e("Zhoushan Zhejiang Petroleum SWRO+MED", "CN", "Zhoushan, Zhejiang", 30.00, 122.20, "operating", 180000, SW, "industrial", "refinery", ENC, tech="RO + MED"),
 e("Tianjin Dagang New Spring SWRO", "CN", "Tianjin", 38.85, 117.50, "operating", 100000, SW, G, "Dagang industry", ENC),
 e("Qingdao Befesa + Dongjiakou SWRO", "CN", "Qingdao, Shandong", 36.05, 120.30, "operating (2 × 100k)", 200000, SW, G, "Qingdao", ENC),
 e("Caofeidian SWRO", "CN", "Tangshan, Hebei", 38.95, 118.50, "operating", 50000, SW, G, "Caofeidian industrial zone", ENC),
 e("Ledong solar-driven MED (Hainan)", "CN", "Ledong, Hainan", 18.75, 109.17, "operating pilot — solar-thermal MED", 30, SW, "solar thermal", "demonstration", ENC, tech="solar MED"),
 e("South China Sea island RO units (Yongxing etc.)", "CN", "Paracel/Spratly islands", 16.83, 112.33, "operating — 100–1,000 m³/d units", 1000, SW, "solar/diesel", "island garrisons", ENC),
 e("Tseung Kwan O SWRO (Hong Kong)", "HK", "Hong Kong", 22.30, 114.27, "operating since end-2023 (inaugurated 2024-12)", 135000, SW, G, "Hong Kong (5 % of supply)", "https://www.acciona.com/updates/articles/acciona-inaugurates-tseung-kwan-o-desalination-plant-hong-kong", "WSD / Acciona-China State"),
 e("Tuas South SWRO", "SG", "Tuas", 1.28, 103.63, "operating since 2013", 318500, SW, "co-generation (411 MW)", "Singapore", WIKI, "PUB / Hyflux→Keppel"),
 e("SingSpring SWRO", "SG", "Tuas", 1.30, 103.64, "operating since 2005 — first in Singapore", 136380, SW, G, "Singapore", WIKI, "PUB / Keppel"),
 e("Tuas (3rd) SWRO", "SG", "Tuas", 1.29, 103.62, "operating since 2017", 137000, SW, G, "Singapore", WIKI, "PUB"),
 e("Marina East dual-mode (river/sea)", "SG", "Marina East", 1.29, 103.88, "operating since 2020 — variable salinity", 137000, "reservoir water or seawater", G, "Singapore", WIKI, "PUB"),
 e("Jurong Island SWRO", "SG", "Jurong Island", 1.26, 103.70, "operating since 2022", 137000, SW, G, "Singapore", WIKI, "PUB"),
 e("Nanliao SWRO (Hsinchu)", "TW", "Hsinchu", 24.85, 120.93, "operating since 2021-02", 13000, SW, G, "Hsinchu science park", WIKI),
 e("Uminonakamichi Nata SWRO (Fukuoka)", "JP", "Fukuoka", 33.67, 130.37, "operating since 2005 — Japan's largest", 50000, SW, G, "Fukuoka", "https://en.wikipedia.org/wiki/Uminonakamichi_Nata_Seawater_Desalination_Center", "Fukuoka District Waterworks Agency"),
 e("Cordova SWRO (Cebu)", "PH", "Cordova, Cebu", 10.25, 123.95, "operating since 2024", 20000, SW, G, "Cordova / Metro Cebu", WIKI),
 e("Tuban GRR&P power + desal", "ID", "Tuban, East Java", -6.80, 111.95, "planned — JDA signed, target 2027", 363480, SW, "co-generation", "Tuban refinery + region", "https://southeastasiainfra.com/using-seawater-desalination-in-sea/", "ACWA Power / Pertamina NRE"),
 e("Penang SWRO (proposed)", "MY", "Penang", 5.37, 100.37, "proposed — 250 MLD on deck above the sea", 250000, SW, G, "Penang", "https://southeastasiainfra.com/using-seawater-desalination-in-sea/", "MPDT Capital"),
 e("EEC desal (Map Ta Phut / Pattaya)", "TH", "Rayong / Chonburi", 12.68, 101.15, "planned PPP — 200k by 2027, 300k by 2037", 200000, SW, G, "Eastern Economic Corridor", "https://southeastasiainfra.com/using-seawater-desalination-in-sea/"),
 e("Gwadar SWRO", "PK", "Gwadar, Balochistan", 25.12, 62.33, "operating since 2018", 960, SW, G, "Gwadar town", WIKI),
 e("Malé MWSC SWRO", "MV", "Malé, Kaafu Atoll", 4.17, 73.51, "operating since 2003 (+5,000 TPD unit 2025)", 11000, SW, "diesel grid", "Malé", WIKI, "MWSC"),
 # ===== Pacific islands =====
 e("South Tarawa SWRO + solar (ADB/GCF)", "KI", "South Tarawa", 1.33, 173.02, "under implementation — 2 RO plants + solar plant", 6000, SW, "solar PV + grid", "South Tarawa ~65,000", "https://www.waterdiplomat.org/story/2024/03/climate-resilient-water-supply-south-tarawa", "PUB Kiribati / ADB"),
 e("Betio SWRO", "KI", "Betio, South Tarawa", 1.36, 172.92, "operating (1999) — Betio only", 110, SW, "diesel grid", "Betio", SOPAC),
 e("Funafuti RO units", "TV", "Funafuti", -8.52, 179.20, "operating (65 m³/d units, 1999 + 2006 Japan) — older units broken", 130, "lagoon seawater", "diesel + solar (JICA PV project)", "Funafuti", SOPAC),
 e("Nauru power-station SWRO", "NR", "Aiwo", -0.53, 166.92, "operating (3 × 120 m³/d), below capacity; MED decommissioned 2002", 360, SW, "diesel power station", "Nauru", SOPAC),
 e("Ebeye SWRO", "MH", "Ebeye, Kwajalein", 8.78, 167.74, "operating — one unit (~380 m³/d output); MED decommissioned", 735, SW, "diesel", "Ebeye ~10,000", SOPAC),
 e("Majuro emergency RO units", "MH", "Majuro", 7.09, 171.38, "intermittent — drought units, several decommissioned", 50, SW, "diesel", "Majuro", SOPAC),
 e("Tonga deployable RO (Navy)", "TO", "Nuku'alofa", -21.14, -175.20, "operating — portable unit for outer islands", 16, SW, "generator", "outer islands emergency", SOPAC),
 # ===== United States =====
 e("Claude 'Bud' Lewis Carlsbad SWRO", "US", "Carlsbad, California", 33.14, -117.34, "operating since 2015 — 50 MGD, largest in the Americas", 189000, SW, G, "San Diego County ~10 %", LYN, "Poseidon / SDCWA"),
 e("Charles E. Meyer SWRO (Santa Barbara)", "US", "Santa Barbara, California", 34.41, -119.69, "operating — reactivated 2017 (built 1991)", 25000, SW, G, "Santa Barbara", LYN, "City of Santa Barbara"),
 e("Doheny Ocean Desalination", "US", "Dana Point, California", 33.46, -117.68, "under construction — 5 MGD (slant wells), target 2028/29", 19000, "seawater via subsurface slant wells", G, "South Orange County", LYN, "South Coast Water District"),
 e("Cal-Am Monterey Peninsula SWRO (Marina)", "US", "Marina, California", 36.70, -121.80, "approved 2022 — 4.8 MGD, target 2027", 18000, "seawater via slant wells", G, "Monterey Peninsula", LYN, "California American Water"),
 e("Poseidon Huntington Beach SWRO", "US", "Huntington Beach, California", 33.64, -117.98, "CANCELLED — Coastal Commission denial 2022, withdrawn 2023", 189000, SW, G, "Orange County", LYN, "Poseidon"),
 e("People's Moss Landing / DeepWater desal", "US", "Moss Landing, California", 36.80, -121.79, "stalled / withdrawn", 45000, SW, G, "Monterey Bay", LYN),
 e("Sand City coastal BWRO", "US", "Sand City, California", 36.62, -121.85, "operating since 2010 — only CA city fully desal-supplied", 1000, "brackish beach wells", G, "Sand City", LYN),
 e("Goldsworthy Desalter (WRD Torrance)", "US", "Torrance, California", 33.84, -118.34, "operating since 2001 (expanded 2018; +1 MGD funded)", 19000, "brackish groundwater (seawater intrusion barrier)", G, "Torrance", LYN, "Water Replenishment District"),
 e("Catalina Island SWRO (SCE)", "US", "Avalon, Catalina Island", 33.34, -118.33, "operating — 2 units", 1300, SW, "island diesel/solar grid", "Avalon", LYN, "Southern California Edison"),
 e("Cambria CSD brackish desal", "US", "Cambria, California", 35.56, -121.08, "operating since 2015 (emergency supply)", 850, "brackish mixed water", G, "Cambria", LYN),
 e("Diablo Canyon NPP SWRO", "US", "San Luis Obispo County", 35.21, -120.86, "operating — plant supply", 5700, SW, "nuclear plant", "Diablo Canyon", LYN, "PG&E"),
 e("Tampa Bay SWRO", "US", "Apollo Beach, Florida", 27.80, -82.40, "operating since 2007 (standby/variable)", 95000, SW, G, "Tampa Bay region", WIKI, "Tampa Bay Water"),
 e("Cape Coral BWRO", "US", "Cape Coral, Florida", 26.60, -81.97, "operating since 1977/1985 — first large US municipal RO", 57000, "brackish groundwater (Floridan aquifer)", G, "Cape Coral", WIKI),
 e("South Florida brackish RO cluster (33 plants)", "US", "South Florida", 26.20, -80.30, "operating — 245 MGD combined (2012)", 927000, "brackish groundwater", G, "SE Florida utilities", WIKI),
 e("Kay Bailey Hutchison BWRO (El Paso)", "US", "El Paso, Texas", 31.78, -106.30, "operating since 2007 — largest inland BWRO", 104000, "brackish groundwater (Hueco Bolson)", G, "El Paso + Fort Bliss", WIKI, "El Paso Water"),
 e("Yuma Desalting Plant", "US", "Yuma, Arizona", 32.72, -114.70, "idle — built 1992, run only in pilot mode", 276000, "brackish agricultural drainage (Wellton-Mohawk)", G, "Colorado River salinity control", WIKI, "US Bureau of Reclamation"),
 e("Corpus Christi Hillcrest SWRO", "US", "Corpus Christi, Texas", 27.82, -97.42, "REJECTED by council Sep 2026 (2nd time) — 30 MGD, $979 M", 114000, SW, G, "Corpus Christi / Coastal Bend", "https://www.texastribune.org/2026/09/01/corpus-christi-water-desalination-plant-city-council-vote-texas/", "City of Corpus Christi"),
 e("Harbor Island SWRO (Nueces River Authority)", "US", "Port Aransas, Texas", 27.84, -97.07, "proposed — 100 MGD regional, one permit pending", 379000, SW, G, "Coastal Bend cities", "https://www.texastribune.org/2026/09/01/corpus-christi-water-desalination-plant-city-council-vote-texas/", "Nueces River Authority"),
 e("Kalaeloa SWRO (Oahu)", "US", "Kapolei, Hawaii", 21.30, -158.08, "planned — 1.7 MGD BOO contract", 6400, SW, G, "Honolulu west", "https://www.sec.gov/Archives/edgar/data/0000928340/000110465926093370/cwco-20260630x10q.htm", "Consolidated Water / BWS"),
 # ===== Mexico / Chile =====
 e("Rosarito SWRO (Aguas de Rosarito)", "MX", "Rosarito, Baja California", 32.33, -117.05, "stalled — contract cancelled 2020, relaunch discussed (US–MX binational 2026)", 380160, SW, G, "Tijuana / Rosarito (+ San Diego)", WIKI, "Consolidated Water (AdR)"),
 e("Los Cabos 2nd SWRO (Cabo San Lucas)", "MX", "Cabo San Lucas, BCS", 22.89, -109.92, "under construction — 30 % Mar 2025, 50 % capacity early 2026", None, SW, G, "Cabo San Lucas (deficit ~600 L/s)", "https://tribunademexico.com/desalinizadora-registra-30-avance/", "OOMSAPAS Los Cabos"),
 e("Aguas Antofagasta La Chimba SWRO", "CL", "Antofagasta", -23.55, -70.40, "operating (2025, >1,400 L/s) — +634 L/s expansion in works; Antofagasta ~100 % desal", 121000, SW, G, "Antofagasta + Mejillones", "https://www.idrawater.org/news/chiles-water-shift-from-drought-to-national-blueprint-for-reuse-and-desalination/", "Aguas Antofagasta (EPM)"),
 e("Los Pelambres mine SWRO (Los Vilos)", "CL", "Coquimbo", -31.90, -71.50, "operating since 2024-03 — 400 L/s, doubling by 2027", 34600, SW, G, "Los Pelambres copper mine", "https://www.idrawater.org/news/chiles-water-shift-from-drought-to-national-blueprint-for-reuse-and-desalination/", "Antofagasta Minerals"),
 e("Caldera SWRO (Atacama)", "CL", "Caldera, Atacama", -27.07, -70.82, "operating since 2022", 100000, SW, G, "Copiapó / Caldera / Chañaral", WIKI, "Econssa / Nueva Atacama"),
 e("Collahuasi phase II SWRO", "CL", "Tarapacá", -20.55, -70.17, "under construction — 1,050 L/s", 90700, SW, G, "Collahuasi mine", CPI, "Collahuasi"),
 e("Aguas Pacífico Aconcagua SWRO", "CL", "Quintero, Valparaíso", -32.78, -71.52, "under construction — 1,000 L/s (+1,000 L/s expansion in review)", 86400, SW, G, "Aconcagua valley multi-use", CPI, "Aguas Pacífico"),
 e("Coquimbo regional SWRO (state concession)", "CL", "Coquimbo", -29.95, -71.34, "concession tender + environmental review — 1,200 L/s", 103700, SW, G, "Coquimbo / La Serena", CPI, "MOP concession"),
 e("Enapac SWRO (Atacama)", "CL", "Caldera, Atacama", -27.20, -70.95, "plant approved, east pipeline in review — 2,630 L/s", 227000, SW, "solar PV (planned)", "Atacama mining + agriculture", CPI, "Energías y Aguas del Pacífico"),
 e("Aguas Marítimas mega-SWRO", "CL", "Antofagasta", -23.00, -70.50, "environmental review — 8,000 L/s", 691000, SW, G, "Antofagasta region multi-use", CPI, "Aguas Marítimas"),
 e("Arica SWRO (Aguas del Altiplano)", "CL", "Arica", -18.48, -70.32, "environmental review — 200 L/s", 17300, SW, G, "Arica", CPI, "Aguas del Altiplano"),
 e("Fishing-cove RO units (30 caletas)", "CL", "Tarapacá→Los Lagos coast", -25.40, -70.45, "operating — ~190 m³/d total, state-funded", 190, SW, "solar/diesel", "30 fishing communities", "https://es.wikipedia.org/wiki/Catastro_nacional_de_plantas_y_proyectos_de_desalinizaci%C3%B3n_de_agua_de_mar_en_Chile"),
 # ===== Caribbean / Atlantic =====
 e("Point Lisas SWRO (Desalcott)", "TT", "Point Lisas, Trinidad", 10.40, -61.48, "operating since 2003 (expanded) — largest in Caribbean", 109000, SW, G, "Point Lisas industry + WASA", WIKI, "Desalcott"),
 e("Ionics Bridgetown SWRO", "BB", "Spring Garden, Barbados", 13.11, -59.62, "operating since 2000", 30000, "brackish coastal wells", G, "Barbados Water Authority", WIKI),
 e("Balashi / WEB Aruba desalination", "AW", "Balashi, Aruba", 12.50, -70.00, "operating — island ~100 % desal (MSF → RO)", 42000, SW, "co-generation", "Aruba", WIKI, "WEB Aruba", tech="RO (ex-MSF)"),
 e("St. Croix Richmond SWRO", "VI", "St. Croix, USVI", 17.75, -64.70, "operating — BOO, expanded from 0.5 to 1.5 MGD", 5700, SW, G, "St. Croix (WAPA)", "https://sevenseaswater.com/case-studies/desalination-projects-in-the-usvi/", "Seven Seas Water"),
 e("St. Thomas Harley SWRO", "VI", "St. Thomas, USVI", 18.33, -64.95, "operating — permanent plant after 2 MGD emergency units", 7600, SW, G, "St. Thomas (WAPA)", "https://sevenseaswater.com/case-studies/desalination-projects-in-the-usvi/", "Seven Seas Water"),
 e("Ffryes Beach SWRO", "AG", "Antigua (SW coast)", 17.06, -61.88, "operating since 2025-03 — 1 M IMGD", 4500, SW, G, "Antigua (APUA)", "https://www.businesswire.com/news/home/20250325978847/en/Seven-Seas-Water-Group-and-APUA-Deliver-Ffryes-Beach-Desalination-Plant-in-Record-Time", "Seven Seas Water / APUA"),
 e("Grand Cayman SWRO plants (West Bay, Red Gate, Abel Castillo, Britannia)", "KY", "Grand Cayman", 19.32, -81.33, "operating — island ~100 % desal", None, SW, G, "Grand Cayman", WIKI, "Cayman Water / OC-Cayman (Consolidated Water)"),
 e("São Vicente SWRO (Mindelo)", "CV", "São Vicente, Cabo Verde", 16.88, -24.98, "operating", 20000, SW, G, "Mindelo", "https://www.acciona.com/projects/swro-cabo-verde", "Electra / Acciona"),
 e("Praia SWRO", "CV", "Santiago, Cabo Verde", 14.92, -23.52, "operating", 5000, SW, G, "Praia", "https://www.acciona.com/projects/swro-cabo-verde", "Electra / Acciona"),
]

existing = {(p["name"], p["country"]) for p in d["plants"]}
added = [p for p in A if (p["name"], p["country"]) not in existing]
d["plants"].extend(added)
d["_readme"] = ("Curated global list of existing, planned, under-construction, stalled or cancelled desalination plants "
                "(Americas, Caribbean, Africa, Europe, Middle East, Asia, Pacific, Australia). Coordinates marked "
                "approx:true are the town/community, not the plant parcel. Every entry has a source URL. Updated 2026-11-07.")
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(f"added {len(added)}, total {len(d['plants'])}")
