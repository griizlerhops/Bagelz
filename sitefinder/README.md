# OC Site Finder

Finds land for affordable homes in Orange County. Each candidate lot (public surplus land,
Housing Element sites, vacant lots, parking lots, religious sites) is checked against
California housing laws (SB 684/1123, SB 9, AB 2011, SB 4), scored for livability, ranked by
how far its city is behind its housing target, and shown on aerial photos with an animation
of how many homes fit.

Built for the Claude Impact Lab · UCI × SoCal Affordable Housing (Lane 1: Find It).

## Run it

Run these one at a time in a terminal inside this folder (PowerShell users: paste one line at a time):

```
pip install -r requirements.txt
python fetch_data.py
python pipeline.py --data data --out out
python fetch_aerials.py
python pipeline.py --data data --out out
```

Then open `out/index.html` in a browser. Every script skips what it already downloaded.

Small input files that can't be fetched by script are already in `data/`:
`noa_information.csv` (HCD Surplus Land Act notices) and `rhna_progress_6.csv` (HCD RHNA progress).
Also download the TCAC/HCD 2026 Opportunity Map and put `final_opp_2026_public.gpkg` in `data/`:
https://www.treasurer.ca.gov/sites/default/files/2025-11/shapefile.zip

## Files

| File | What it does |
|---|---|
| `fetch_data.py` | Downloads zoning, Housing Element sites, land use, hazards, transit, CalEnviroScreen, roads |
| `pipeline.py` | Builds candidate sites, runs the legal / livability / pressure checks, writes `out/` |
| `aerial.py` | Usable area (parcel minus buildings minus setback) and home-icon layout per lot |
| `fetch_aerials.py` | Downloads a NAIP aerial photo + building footprints per Santa Ana site |
| `rules.json` | Every legal number and assumption, with its source and a verified/secondary/assumed tag |
| `template.html` | The web page (Leaflet map, lot animation, site details) |

## Extending

- Fix or add a law: edit `rules.json`, not the code.
- Add a data source: a fetch in `fetch_data.py`, a loader + check in `pipeline.py`, a weight in `rules.json`.
- Aerial view for more cities: add them to `rules.json` > `aerial.cities`, then rerun the last three commands.

## Known gaps

- SCAG's Housing Element layer has no rows for Santa Ana, Costa Mesa, Huntington Beach, Tustin or Orange.
- Zoning, land use and hazards are fetched for Santa Ana first; widen `fetch_data.py` to cover more cities.
- Owner and price aren't in free public data (needs the OC Assessor roll).
- Santa Ana zone-code meanings and AB 2011 densities are tagged "assumed"/"secondary" in `rules.json`: verify.
