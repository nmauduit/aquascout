# AquaScout v0 — water data at any point

Single-file prototype of the solar-desal feasibility screen. Open `aquascout-v0.html` in a browser (double-click; no server needed), click the map or type a place / `lat, lon`, and it fans out to the open APIs that cover that point.

## What it queries (all free, no keys)

| Layer | Source | Coverage |
|---|---|---|
| Place, elevation | OSM Nominatim, Open-Meteo | global |
| Solar (GHI by month, worst month), rain, temp | NASA POWER climatology | global |
| River discharge | Open-Meteo Flood (GloFAS) | global |
| Water bodies, wells, springs, water works, WWTPs, desal plants, coastline, place population | OpenStreetMap / Overpass | global, uneven |
| Gauges, monitoring wells, latest readings | USGS Water Data API (OGC) | US |
| Chemistry (TDS, EC, Cl, Na, SO4, hardness, SiO2, B, NO3, As, F…) and microbiology (E. coli, coliforms, enterococci) | Water Quality Portal | US |
| Utility serving the point | EPA CWS service-area boundaries + SDWIS | US |
| Wastewater permits / POTWs | EPA ECHO | US |
| Tap-water chemistry + E. coli, distributor, piezometers, groundwater chemistry, river gauges | Hub'Eau, geo.api.gouv.fr | France + DOM |

Every click ends with a **coverage report** listing what was found, what nobody monitors there, and the minimum field campaign to fill the gap, plus a first-order **feed-water candidate table** with energy, PV, battery, genset and land estimates.

## Known limits of v0
- Browser-only: each API must allow CORS. If a card shows an error, that adapter needs to move to the backend proxy.
- Overpass can be slow or rate-limited; retry if it times out.
- Population comes from OSM `place` tags; enter it manually when missing.
- No adapters yet for Colombia, Brazil, UK, Bahamas (listed in the coverage card). No bulk datasets (Thorslund salinity, IGRAC, HydroWASTE, WorldPop) — these need a database.

## Next step (v1)
FastAPI on Render + Supabase/PostGIS: one adapter per source family exposed as MCP tools, bulk datasets loaded once, this page becomes the frontend, PDF-ingestion module for island reports.
