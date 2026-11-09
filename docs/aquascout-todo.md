# AquaScout — to-do list (updated 2026-11-08 19:30 PT)

Live: https://nmauduit.github.io/aquascout/ · Repo: github.com/nmauduit/aquascout

**Rule agreed:** the tool shows **publicly available data only** — no site knowledge typed in by the user; unknowns are shown as unknown (grey).

## A. Your actions
- [ ] Test location #2 and send screenshots of anything wrong, surprising or missing (location #1 Exuma / Torch Cay done).
- [ ] Decide: count people with WorldPop (B1).

## B. Next build items (suggested order)
1. **People count from WorldPop** — people within the radius and near the point; replaces "assumed 500 people"; demand and sizing follow.
2. **River check, honest version** — dry-season flow (GloFAS history), tidal/saline river mouths, large rivers 50–100 km away (Magdalena-type cases).
3. **Financing & payback** — water tariff or plant-as-a-service fee, payback, IRR, CAPEX per household.
4. **Calibrate costs** against published solar RO plants (Yotojoroin, Puerto Estrella, Kiunga, Witsand, Strongili).
5. **Utility performance (public)** — hours of service and losses (Superservicios SUI, IBNET).
6. **Crisis list** — add Caribbean islands and Africa; review twice a year.
7. **Batch screening** — rank communities in a region by need × sun × feed water × grid cost.
8. **Small-cay rule follow-ups** — shorter island-check wait or pre-baked Caribbean island polygons.
9. **Sizing refinements** — small-plant energy penalty, pumping head, brine disposal, 24-h mode (demand stays 100 L/person/day).
10. **Inventory gaps** — Haiti, Jamaica, Yemen, Libya, Mauritania, Vietnam, Fiji, Tonga, PNG; Osmosun; Elemental Water Makers.
11. **Subnational JMP leftovers** — Uganda, Turkey, Nepal, Lesotho, Palestine.
12. **Electricity tariffs** with fuel surcharge; SAIDI/SAIFI.
13. **UI** — ES/FR toggle; "last updated" badges.

## C. Backend
- Supabase 397 / 500 MB — room for about one more OSM region before Pro ($25/month).
- Pre-bake CORS-blocked rasters (GEBCO); batch-screening RPC.

## Done 2026-11-08
- [x] **Bulk files** — HydroWASTE (58,502 plants) and global salinity (138k cells) in Supabase; gridfinder predicted lines (11,299 static tiles). Jones 2019 not public (proprietary DesalData).
- [x] **Continuity & safety** — JMP service components (208 countries), rural/urban IRCA, two map layers.
- [x] **Supply-problem flag** — red, factual, separate from access need; crisis list (6 Colombian entries with sources).
- [x] **Fresh river option + "Alternatives to a new plant" card**; Santa Marta desal cancellation documented.
- [x] **Colours** — grey = no data; orange/red = real concern; feed water never red; sun tile on the year-round average.
- [x] **Utility "unknown"** where no open register (e.g. Bahamas).
- [x] **Small-cay rule** — access "unknown" on islands < 50 km² with no utility/desal mapped.
- [x] **Site-knowledge selector removed** (public data only).
- [x] **Map & scan** — click selects, Scan runs; no auto-scan on load; Stop button; honest progress header.
- [x] **Population density layer** (WorldPop 2020).
- [x] JMP files from washdata.org (2026-11-07), monthly refresh.
- [x] Supabase cache live (5 regions).

## Validation points
La Guajira 11.55,-72.90 · Nazareth 12.05,-71.95 · Santa Marta 11.174,-74.232 · Torch Cay 23.3931,-75.4739 · Lodwar 3.12,35.60 · Marseille 43.30,5.37 · Imperial Valley 32.8,-115.6 · Orinoco 8.5376,-60.6006 · Nordeste BR 7.2,-39.3
