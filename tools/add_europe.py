#!/usr/bin/env python3
"""Append European desalination plants to data/planned-desal.json."""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data" / "planned-desal.json"
d = json.loads(P.read_text())

AEDYR = "https://aedyr.com/plantas-desaladoras-agua-mar-espana/"
WIKI = "https://en.wikipedia.org/wiki/Desalination_by_country"
SOLE = "https://en.ilsole24ore.com/art/in-sicily-desalination-plants-are-operating-but-the-networks-are-struggling-AJ2mSOh"
CYM = "https://cyprus-mail.com/2026/09/02/cabinet-approves-three-new-permanent-desalination-plants"
EJSD = "https://www.ecsdev.org/ojs/index.php/ejsd/article/download/466/463/927"
def e(name, cc, region, lat, lon, status, cap, feed, power, serves, source, operator=None, tech="RO", approx=True):
    return {"name": name, "country": cc, "region": region, "lat": lat, "lon": lon, "approx": approx,
            "status": status, "capacity_m3d": cap, "feed": feed, "power": power, "technology": tech,
            "serves": serves, "operator": operator, "source": source}
def es(name, region, lat, lon, cap, serves="municipal", status="operating", operator=None):
    return e(name, "ES", region, lat, lon, status, cap, "seawater", "grid", serves, AEDYR, operator)

A = [
 # ---------- Spain — mainland ----------
 es("Torrevieja SWRO", "Alicante", 37.97, -0.70, 240000, "Alicante/Murcia supply + irrigation — largest in Europe", operator="ACUAMED / ACCIONA"),
 es("El Prat (Llobregat) SWRO", "Barcelona", 41.31, 2.08, 200000, "Barcelona metro", operator="ATL"),
 es("La Tordera SWRO", "Blanes, Girona", 41.67, 2.78, 57600, "Costa Brava / Maresme"),
 es("Águilas–Guadalentín SWRO", "Águilas, Murcia", 37.42, -1.55, 210000, "Murcia irrigation + towns", operator="ACUAMED"),
 es("Valdelentisco SWRO", "Cartagena, Murcia", 37.57, -1.17, 137500, "Campo de Cartagena irrigation + towns", operator="ACUAMED"),
 es("Escombreras SWRO", "Cartagena, Murcia", 37.57, -0.95, 63000, "Cartagena"),
 es("San Pedro del Pinatar I + II SWRO", "Murcia", 37.83, -0.77, 130000, "Mancomunidad Canales del Taibilla", operator="MCT"),
 es("Virgen del Milagro SWRO (irrigators)", "Mazarrón, Murcia", 37.58, -1.30, 36000, "irrigation community"),
 es("Alicante I + II SWRO", "Alicante", 38.33, -0.52, 115000, "Alicante metro", operator="MCT"),
 es("Marina Baja (Mutxamel) SWRO", "Alicante", 38.42, -0.45, 50000, "Benidorm / Marina Baja"),
 es("Jávea SWRO", "Alicante", 38.79, 0.17, 28000, "Jávea"),
 es("Sagunto SWRO", "Valencia", 39.65, -0.22, 22900, "Sagunto"),
 es("Moncofa SWRO", "Castellón", 39.81, -0.14, 30000, "Moncofa"),
 es("Oropesa SWRO", "Castellón", 40.09, 0.14, 49000, "Oropesa / Marina d'Or"),
 es("Carboneras SWRO", "Almería", 36.99, -1.90, 120000, "Almería drinking water + irrigation", operator="ACUAMED"),
 es("Campo de Dalías SWRO", "Almería", 36.75, -2.73, 97200, "El Ejido / Poniente greenhouses", operator="ACUAMED"),
 es("Almería SWRO", "Almería", 36.83, -2.45, 50000, "Almería city"),
 es("Bajo Almanzora SWRO", "Almería", 37.22, -1.80, 60000, "Almanzora irrigation — damaged by 2012 flood, rebuilt", operator="ACUAMED"),
 es("Mar de Alborán SWRO", "Almería", 36.72, -2.60, 60000, "Poniente almeriense"),
 es("Marbella SWRO", "Málaga", 36.52, -4.88, 56000, "Costa del Sol"),
 es("Ceuta SWRO", "Ceuta", 35.89, -5.32, 31000, "Ceuta"),
 es("Melilla SWRO", "Melilla", 35.29, -2.95, 30000, "Melilla"),
 # ---------- Spain — Canary Islands ----------
 es("Las Palmas III + IV SWRO", "Gran Canaria", 28.12, -15.43, 82000, "Las Palmas city", operator="Emalsa"),
 es("Sureste II SWRO", "Gran Canaria", 27.92, -15.40, 33000, "SE Gran Canaria"),
 es("Maspalomas I + II SWRO", "Gran Canaria", 27.76, -15.58, 34000, "Maspalomas tourism"),
 es("Telde I + II SWRO", "Gran Canaria", 28.00, -15.40, 32000, "Telde"),
 es("Arucas II SWRO", "Gran Canaria", 28.13, -15.52, 16000, "Arucas / Moya"),
 es("Agragua I + II SWRO", "Gran Canaria", 27.95, -15.42, 15000, "irrigation"),
 es("Aldea de San Nicolás I + II SWRO", "Gran Canaria", 27.98, -15.78, 10000, "La Aldea"),
 es("Inalsa IV SWRO", "Lanzarote", 28.96, -13.55, 40000, "Lanzarote — island ~100 % desal", operator="Canal Gestión Lanzarote"),
 es("Lanzarote III + IV + V SWRO", "Lanzarote", 28.95, -13.56, 64000, "Lanzarote"),
 es("Janubio SWRO", "Lanzarote", 28.94, -13.83, 18000, "Lanzarote SW"),
 es("Puerto del Rosario SWRO", "Fuerteventura", 28.50, -13.86, 36500, "Fuerteventura", operator="CAAF"),
 es("Santa Cruz de Tenerife SWRO", "Tenerife", 28.45, -16.26, 20700, "Santa Cruz"),
 es("Adeje–Arona SWRO", "Tenerife", 28.06, -16.70, 22000, "S Tenerife tourism"),
 es("La Caleta SWRO", "Tenerife", 28.09, -16.75, 20000, "Adeje"),
 es("Granadilla / Abona SWRO", "Tenerife", 28.08, -16.50, 14000, "Granadilla"),
 es("Guía de Isora / Fonsalía SWRO", "Tenerife", 28.19, -16.82, 14000, "Guía de Isora"),
 # ---------- Spain — Balearics ----------
 es("Bahía de Palma SWRO", "Mallorca", 39.55, 2.70, 64800, "Palma"),
 es("Alcúdia SWRO", "Mallorca", 39.85, 3.12, 14000, "Alcúdia"),
 es("Andratx SWRO", "Mallorca", 39.57, 2.42, 14000, "Andratx"),
 es("Ciutadella SWRO", "Menorca", 40.00, 3.84, 10000, "Ciutadella"),
 es("Ibiza + San Antonio + Santa Eulalia SWRO", "Ibiza", 38.92, 1.42, 44500, "Ibiza island (3 plants)"),
 # ---------- Portugal ----------
 e("Algarve (Albufeira) SWRO", "PT", "Algarve", 37.10, -8.26, "under construction — main works to early 2028, start-up ~2029; Portugal's first SWRO", None, "seawater", "grid", "Algarve", "https://www.theportugalnews.com/news/2026-09-24/desalination-plant-in-algarve-sees-works-progressing/1090991", "Águas do Algarve / GS Inima consortium"),
 # ---------- Italy ----------
 e("Trapani mobile SWRO (Acciona)", "IT", "Sicily", 38.02, 12.52, "operating since 2025 — 96 L/s mobile; 192 L/s fixed plant planned", 8300, "seawater", "grid", "Trapani", SOLE, "Regione Siciliana / Acciona"),
 e("Gela mobile SWRO (Acciona)", "IT", "Sicily", 37.07, 14.25, "operating since 2025 — 96 L/s mobile; 192 L/s fixed plant planned", 8300, "seawater", "grid", "Gela", SOLE),
 e("Porto Empedocle mobile SWRO (Acciona)", "IT", "Sicily", 37.29, 13.53, "operating since 2025 — 96 L/s; fixed upgrade shelved", 8300, "seawater", "grid", "Agrigento", SOLE),
 e("Palermo east + west SWRO", "IT", "Sicily", 38.12, 13.36, "planned — 600–1,000 L/s, 6 bids received", 70000, "seawater", "grid", "Palermo metro", SOLE),
 # ---------- Malta ----------
 e("Pembroke SWRO", "MT", "Pembroke", 35.93, 14.48, "operating since 2016 (rebuilt)", 54000, "seawater", "grid", "Malta — 4 RO plants = 64 % of national water", WIKI, "Water Services Corporation"),
 e("Għar Lapsi SWRO", "MT", "Siġġiewi", 35.82, 14.43, "operating since 1982 (upgraded)", 20000, "seawater", "grid", "S Malta", WIKI, "Water Services Corporation"),
 e("Ċirkewwa SWRO", "MT", "Mellieħa", 35.99, 14.33, "operating", None, "seawater", "grid", "N Malta", WIKI, "Water Services Corporation"),
 e("Hondoq (Gozo) SWRO", "MT", "Gozo", 36.02, 14.31, "operating", None, "seawater", "grid", "Gozo", WIKI, "Water Services Corporation"),
 # ---------- Cyprus ----------
 e("Larnaca SWRO", "CY", "Larnaca", 34.88, 33.60, "operating since 2001", 64000, "seawater", "grid", "Larnaca / Nicosia", WIKI, "MN Larnaca Desalination Co"),
 e("Dhekelia SWRO (new permanent)", "CY", "Dhekelia", 34.98, 33.72, "approved 2026-09 — replaces existing Dhekelia plant", 80000, "seawater", "grid", "Famagusta / Nicosia", CYM, "Water Development Dept"),
 e("Ayia Thekla SWRO", "CY", "Famagusta district", 34.98, 33.93, "approved 2026-09 (replaces cancelled Ayia Napa mobile unit)", 30000, "seawater", "grid", "Ayia Napa / Paralimni", CYM),
 e("Polis Chrysochous SWRO", "CY", "Paphos district", 35.03, 32.42, "approved 2026-09", 10000, "seawater", "grid", "Polis", CYM),
 e("Limassol permanent SWRO", "CY", "Limassol", 34.68, 33.05, "planned", 60000, "seawater", "grid", "Limassol", CYM),
 e("Moni mobile SWRO units (UAE-donated)", "CY", "Limassol", 34.70, 33.18, "operating since 2025", None, "seawater", "grid", "Limassol — emergency drought units", CYM),
 # ---------- Greece (islands) ----------
 e("Syros SWRO cluster (14 units)", "GR", "Cyclades", 37.44, 24.94, "operating", 27370, "seawater", "grid", "Ermoupoli / Syros", EJSD),
 e("Mykonos SWRO (5 units)", "GR", "Cyclades", 37.45, 25.33, "operating (1980–2008)", 9250, "seawater", "grid", "Mykonos", EJSD),
 e("Milos wind-powered SWRO", "GR", "Cyclades", 36.73, 24.43, "operating — 3 units + 850 kW wind turbine", 3600, "seawater", "wind + grid", "Milos", EJSD),
 e("Kimolos geothermal desal", "GR", "Cyclades", 36.80, 24.57, "operating — low-enthalpy geothermal", 576, "seawater", "geothermal", "Kimolos", EJSD, tech="thermal"),
 e("Iraklia wind+PV SWRO", "GR", "Cyclades", 36.85, 25.47, "operating — 30 kW wind + PV (EU-funded)", 80, "seawater", "wind + solar PV", "Iraklia (~150 residents)", EJSD),
 e("Paros SWRO", "GR", "Cyclades", 37.08, 25.15, "operating", 1200, "seawater", "grid", "Paros", EJSD),
 e("Ios SWRO", "GR", "Cyclades", 36.72, 25.28, "operating", 1000, "seawater", "grid", "Ios", EJSD),
 e("Sifnos SWRO", "GR", "Cyclades", 36.97, 24.72, "operating", 500, "seawater", "grid", "Sifnos", EJSD),
 e("Santorini SWRO", "GR", "Cyclades", 36.42, 25.43, "operating (plus private units)", 380, "seawater", "grid", "Santorini", EJSD),
 e("Amorgos (Katapola) SWRO", "GR", "Cyclades", 36.83, 25.86, "operating since 2026-07", 1050, "seawater", "grid", "Amorgos", "https://greekcitytimes.com/2026/07/21/amorgos-desalination-plant-inaugurated"),
 e("Strongili solar SWRO (Temak)", "GR", "Dodecanese", 36.11, 29.63, "operating since 2018 — containerised PV + battery, off-grid", 5, "seawater", "solar PV + battery", "military outpost (~4 m³/d)", "https://www.aquatechtrade.com/news/desalination/solar-desalination-to-quench-greek-thirst", "Temak"),
 # ---------- France ----------
 e("Ironi Bé SWRO (Mayotte)", "FR", "Mayotte (Grande-Terre)", -12.82, 45.17, "commissioning 2025/26 — 10k, expansion to ~16.7k planned", 10000, "seawater", "grid", "Mayotte (water-crisis response)", "https://outremers360.com/bassin-indien-appli/mayotte-stereau-filiale-du-groupe-saur-fournira-bientot-10-000-m3-deau-potable-par-jour-sur-le-territoire-pour-lusine-de-dessalement", "LEMA / Stereau (Saur)"),
 # ---------- UK / Channel Islands ----------
 e("Beckton (Thames Gateway) BWRO", "GB", "East London", 51.52, 0.10, "operating on standby since 2010 — drought reserve", 150000, "brackish tidal Thames", "grid (biodiesel originally)", "London drought supply", WIKI, "Thames Water / Acciona"),
 e("La Corbière (Jersey) SWRO", "JE", "Jersey", 49.18, -2.23, "operating since 1970 (RO since 1997)", 6000, "seawater", "grid", "Jersey drought reserve", WIKI, "Jersey Water"),
 # ---------- Germany / Sweden / Gibraltar ----------
 e("Helgoland SWRO (2 plants)", "DE", "Helgoland", 54.18, 7.89, "operating since 1998", None, "seawater", "grid", "Helgoland island", WIKI),
 e("Kvarnåkershamn (Gotland) BWRO", "SE", "Gotland", 57.18, 18.22, "operating since 2019", 7500, "Baltic brackish", "grid", "S Gotland", WIKI, "Region Gotland"),
 e("Herrvik (Gotland) BWRO", "SE", "Gotland", 57.43, 18.92, "operating since 2016", 480, "Baltic brackish", "grid", "Herrvik", WIKI, "Region Gotland"),
 e("Gibraltar RO plants", "GI", "Gibraltar", 36.14, -5.35, "operating (several RO + MSF units)", None, "seawater", "grid", "Gibraltar", WIKI, "AquaGib"),
]

existing = {(p["name"], p["country"]) for p in d["plants"]}
added = [p for p in A if (p["name"], p["country"]) not in existing]
d["plants"].extend(added)
d["_readme"] = d["_readme"].replace("South America and Africa", "South America, Africa and Europe")
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(f"added {len(added)}, total {len(d['plants'])}")
