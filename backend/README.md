# AquaScout backend (Supabase + GitHub Actions)

- **Supabase project** `aquascout` (us-east-1): PostGIS tables `osm_feat`, `osm_region`, `scan_cache`; RPC `osm_near(lat,lon,r_m,theme,lim)` and `osm_covered(lat,lon)`; anon read-only via RLS.
- **Weekly cache**: `.github/workflows/osm-cache.yml` downloads Geofabrik extracts listed in `backend/regions.txt`, filters water + power themes with osmium, and loads them with `backend/load_osm.py` (psql COPY). Runs Mondays 03:17 UTC or on demand (Actions → Run workflow, optional region list).
- **Secret required**: `SUPABASE_DB_URL` (repo Settings → Secrets → Actions) = the project's Postgres connection string (Session pooler, port 5432).
- **Frontend**: `index.html` calls the RPC first; if the point is not in a loaded region (or the call fails) it falls back to Overpass.

Space budget: free tier 500 MB. Unnamed streams are dropped; geometries simplified on output. Check `select region, feat_water, feat_power, pg_size_pretty(pg_total_relation_size('osm_feat')) from osm_region;`.
