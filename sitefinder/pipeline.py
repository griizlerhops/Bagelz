"""
Site screening pipeline for affordable ownership housing in Orange County.

    python pipeline.py --data ../data --out out/

Every input is optional except the Surplus Land Act notices: each layer that is
present adds checks, and missing layers show up as "pending" in the output
instead of breaking the run. Adding a data source = a loader + a check.

Inputs (put them in --data):
  noa_information.csv              HCD Surplus Land Act notices (data.ca.gov)
  rhna_progress_6.csv              HCD 6th-cycle RHNA progress (data.ca.gov)
  final_opp_2026_public.gpkg       TCAC/HCD 2026 Opportunity Map
  *.geojson from fetch_data.py     zoning, Housing Element sites, hazards, transit,
                                   CalEnviroScreen (picked up automatically)
"""
import argparse, json, math, os, re
from datetime import date

import geopandas as gpd
import pandas as pd
import shapely

import aerial

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = json.load(open(os.path.join(HERE, "rules.json")))
SQFT_PER_ACRE = 43560
METRIC = 3310  # California Albers-ish equal-area (EPSG:3310) for distances/areas


# ---------------------------------------------------------------- helpers
def find(data_dir, *names):
    for n in names:
        for f in os.listdir(data_dir):
            if f.lower() == n.lower() or re.fullmatch(n, f, re.I):
                return os.path.join(data_dir, f)
    return None


def parse_acres(text):
    """'9,005 SF' -> 0.207, 'approximately 18 acres' -> 18, '.3' -> 0.3."""
    if text is None or (isinstance(text, float) and math.isnan(text)):
        return None
    s = str(text).lower().replace(",", "")
    m = re.search(r"(\d*\.?\d+)", s)
    if not m:
        return None
    v = float(m.group(1))
    if "sf" in s or "sq" in s or "square" in s:
        v /= SQFT_PER_ACRE
    return v if v > 0 else None


def zone_class(text):
    """Rough zoning category from free-text zoning / general plan."""
    s = (str(text) if text is not None else "").lower()
    if not s or s == "nan":
        return "unknown"
    if "open space" in s and "commercial" in s:
        return "commercial_option"
    if re.search(r"\b(r-?1|e-?\d|single[- ]family|estate|low density residential)\b", s):
        return "single_family"
    if re.search(r"\b(r-?[2-9]|multi|mixed|medium|high density|residential|rmx|mu)\b", s):
        return "multi_family"
    if re.search(r"\b(c-?\d|commercial|retail|office|cd|downtown)\b", s):
        return "commercial"
    if "specific plan" in s or re.search(r"\bsp-?\d", s):
        return "specific_plan"
    if "open space" in s or "park" in s or "golf" in s:
        return "open_space"
    if re.search(r"industrial|\bm-?\d\b", s):
        return "industrial"
    if re.search(r"public|institution|school|civic", s):
        return "public"
    return "other"


# ---------------------------------------------------------------- loaders
def load_tracts(data_dir):
    p = find(data_dir, "final_opp_2026_public.gpkg")
    if not p:
        raise SystemExit("Need final_opp_2026_public.gpkg (TCAC 2026 Opportunity Map)")
    t = gpd.read_file(p)
    return t[t.county_name == "Orange"][
        ["fips", "oppscore", "oppcat", "env_burden_flag", "geometry"]].to_crs(4326)


def load_surplus(data_dir, tracts):
    p = find(data_dir, r".*noa_information\.csv")
    d = pd.read_csv(p, encoding_errors="replace")
    d["x"] = pd.to_numeric(d.x, errors="coerce")
    d["y"] = pd.to_numeric(d.y, errors="coerce")
    g = gpd.GeoDataFrame(d, geometry=gpd.points_from_xy(d.x, d.y), crs=4326)
    g = g[g.within(tracts.union_all())].copy()          # inside Orange County
    g["acres"] = g["Parcel Size (Gross Acres)"].map(parse_acres)
    g["issued"] = pd.to_datetime(g["Date Notice Issued"], format="%m-%d-%Y", errors="coerce")
    g = g.sort_values("issued").drop_duplicates("APN", keep="last")
    return g


OC_CITIES = ["Aliso Viejo", "Anaheim", "Brea", "Buena Park", "Costa Mesa", "Cypress", "Dana Point",
             "Fountain Valley", "Fullerton", "Garden Grove", "Huntington Beach", "Irvine", "La Habra",
             "La Palma", "Laguna Beach", "Laguna Hills", "Laguna Niguel", "Laguna Woods", "Lake Forest",
             "Los Alamitos", "Mission Viejo", "Newport Beach", "Placentia", "Rancho Santa Margarita",
             "San Clemente", "San Juan Capistrano", "Santa Ana", "Seal Beach", "Stanton", "Tustin",
             "Villa Park", "Westminster", "Yorba Linda", "Orange"]   # Orange last: substring of others


def city_of(r):
    """Postal city from the notice; if blank, fall back to the agency name."""
    c = str(r.City).strip() if pd.notna(r.City) else ""
    c = c.replace("Westminister", "Westminster")
    for name in OC_CITIES:
        if c.lower() == name.lower():
            return name
    agency = str(r["Local Agency"])
    for name in OC_CITIES:
        if name.lower() in agency.lower():
            return name
    return c.title() if c else "Orange County (other agency)"


def group_sites(g):
    """Adjacent parcels in one notice (same agency, date, street) become one site."""
    def street(a):
        a = str(a or "").lower()
        a = re.sub(r"^\s*\d+\s*", "", a)
        return re.sub(r"[^a-z ]", "", a).replace(" street", " st").strip()

    # Cluster parcels from the same notice whose points sit within ~35 m of each other
    # (a parcel-polygon adjacency test replaces this once parcel geometry is loaded).
    g = g.copy()
    thr = RULES["surplus_land"]["cluster_distance_m"]
    gm = g.to_crs(METRIC)
    g["gkey"] = None
    for nkey, idx in gm.groupby([gm["Local Agency"].astype(str), gm["Date Notice Issued"].astype(str)]).groups.items():
        idx = list(idx)
        label = {i: i for i in idx}
        def root(i):
            while label[i] != i:
                i = label[i]
            return i
        for a_ in idx:
            for b_ in idx:
                if a_ < b_ and gm.geometry[a_].distance(gm.geometry[b_]) <= thr:
                    label[root(b_)] = root(a_)
        for i in idx:
            g.at[i, "gkey"] = f"{nkey}|{root(i)}"
    g.loc[g.geometry.is_empty | g.x.isna(), "gkey"] = "apn|" + g.APN.astype(str)
    sites = []
    for key, grp in g.groupby("gkey"):
        first = grp.iloc[-1]
        acres = grp["acres"].dropna()
        # some notices repeat the whole-site acreage on every row (e.g. golf course)
        total = acres.max() if acres.nunique() == 1 and len(acres) > 1 else acres.sum()
        addr = first["Address"] if isinstance(first["Address"], str) else ""
        sites.append({
            "id": "SLA-" + re.sub(r"[^0-9A-Za-z]", "", str(first.APN))[:14],
            "source": "surplus_land",
            "name": (addr.strip() or f"APN {first.APN}") +
                    (f" (+{len(grp) - 1} adjoining parcels)" if len(grp) > 1 else ""),
            "city": city_of(first),
            "apns": [str(a) for a in grp.APN],
            "agency": str(first["Local Agency"]),
            "notice_date": first.issued.date().isoformat() if pd.notna(first.issued) else None,
            "notice_status": str(first["NOA Status"]),
            "notice_link": first["Notice Website Link"] if isinstance(first["Notice Website Link"], str) else None,
            "zoning_text": str(first["General Plan/Zoning"]) if pd.notna(first["General Plan/Zoning"]) else None,
            "existing_use": str(first["Existing Use/Vacancy"])[:160] if pd.notna(first["Existing Use/Vacancy"]) else None,
            "acres": round(float(total), 3) if len(acres) else None,
            "lon": float(grp.geometry.x.mean()), "lat": float(grp.geometry.y.mean()),
        })
    # Same land re-noticed under a different notice: keep the newest
    seen, uniq = {}, []
    for s in sorted(sites, key=lambda s: s["notice_date"] or "", reverse=True):
        k = (re.sub(r"[^a-z0-9]", "", s["name"].lower().split("(")[0]), s["acres"]) if not s["name"].startswith("APN") \
            else tuple(sorted(s["apns"]))
        if k in seen:
            continue
        seen[k] = 1
        uniq.append(s)
    used = {}
    for s in uniq:                      # stable ids: suffix only on a real collision
        base = s["id"]
        used[base] = used.get(base, 0) + 1
        if used[base] > 1:
            s["id"] = f"{base}-{used[base]}"
    return uniq


def load_he_sites(data_dir):
    """Housing Element inventory parcels -> sites (touching parcels in one city merged)."""
    g = optional_layer(data_dir, "scag_he_sites")
    if g is None:
        return []
    rz = optional_layer(data_dir, "scag_he_rezone")
    rz_cap = dict(zip(rz.Assessor_Parcel_Number, rz.Rezone_Capacity)) if rz is not None else {}
    gm = g.to_crs(METRIC)
    sites = []
    for jur, grp in gm.groupby("Jurisdiction"):
        blobs = gpd.GeoDataFrame(geometry=[grp.buffer(1).union_all()], crs=METRIC).explode(index_parts=False)
        blobs["cid"] = range(len(blobs))
        j = gpd.sjoin(grp.assign(geometry=grp.representative_point()), blobs, predicate="within")
        for cid, c in j.groupby("cid"):
            parcels = grp.loc[c.index]
            pt = gpd.GeoSeries([parcels.union_all().representative_point()], crs=METRIC).to_crs(4326).iloc[0]
            apns = [str(a) for a in parcels.Assessor_Parcel_Number]
            city = jur.title()
            sites.append({
                "id": "HE-" + re.sub(r"[^0-9]", "", apns[0])[:12],
                "source": "housing_element",
                "name": f"APN {apns[0]}" + (f" (+{len(apns) - 1} adjoining parcels)" if len(apns) > 1 else ""),
                "city": "Orange County (unincorporated)" if city == "Orange County" else city,
                "apns": apns, "agency": None,
                "acres": round(float(parcels.area.sum()) / 4046.86, 3),
                "lon": float(pt.x), "lat": float(pt.y),
                "he_capacity": {
                    "lower": int(parcels.Low_Income_HE_Capacity.sum()),
                    "moderate": int(parcels.Moderate_Income_HE_Capacity.sum()),
                    "above_moderate": int(parcels.Above_Moderate_Income_HE_Capacity.sum()),
                    "total": int(parcels.Total_HE_Capacity.sum())},
                "rezone_capacity": int(sum(rz_cap.get(a, 0) for a in apns)) or None,
                "_geom": gpd.GeoSeries([parcels.union_all()], crs=METRIC).to_crs(4326).iloc[0],
            })
    return sites


def land_use_sites(data_dir):
    """Vacant lots, parking lots and religious facilities from SCAG existing land use."""
    elu = optional_layer(data_dir, "scag_existing_landuse")
    if elu is None:
        return []
    cfg = RULES["land_use_candidates"]
    pick = elu[elu.LU24.isin(cfg["codes"].keys()) & (elu.ACRES >= cfg["min_acres"])].copy()
    zon = optional_layer(data_dir, "scag_zoning")
    zmap = dict(zip(zon.PID24, zon.ZN24_CITY)) if zon is not None else {}
    if zon is not None:                       # only cities whose zoning was fetched
        pick = pick[pick.CITY.isin(set(zon.CITY))]
    gm = pick.to_crs(METRIC)
    sites = []
    for (city, lu), grp in gm.groupby(["CITY", "LU24"]):
        blobs = gpd.GeoDataFrame(geometry=[grp.buffer(1).union_all()], crs=METRIC).explode(index_parts=False)
        blobs["cid"] = range(len(blobs))
        j = gpd.sjoin(grp.assign(geometry=grp.representative_point()), blobs, predicate="within")
        for cid, c in j.groupby("cid"):
            parcels = grp.loc[c.index]
            pt = gpd.GeoSeries([parcels.union_all().representative_point()], crs=METRIC).to_crs(4326).iloc[0]
            apns = [f"{a[:3]}-{a[3:6]}-{a[6:8]}" if len(str(a)) == 8 else str(a) for a in parcels.APN24]
            code = next((zmap.get(p_) for p_ in parcels.PID24 if zmap.get(p_)), None)
            use = cfg["codes"][lu]
            sites.append({
                "id": "LU-" + str(parcels.PID24.iloc[0])[-10:],
                "source": "land_use",
                "name": f"{use}, APN {apns[0]}" + (f" (+{len(apns) - 1})" if len(apns) > 1 else ""),
                "city": str(city).title(), "apns": apns, "agency": None,
                "acres": round(float(parcels.ACRES.sum()), 3),
                "lon": float(pt.x), "lat": float(pt.y),
                "existing_use": use,
                "land_use_code": lu,
                "zone_code": code,
                "owner_type": "religious_proxy" if lu in cfg["sb4_proxy_codes"] else None,
                "_geom": gpd.GeoSeries([parcels.union_all()], crs=METRIC).to_crs(4326).iloc[0],
            })
    return sites


def merge_he_into_surplus(sla, he):
    """A Housing Element parcel that is also public surplus land is one site, not two."""
    by_apn = {a.replace(" ", ""): s for s in sla for a in s["apns"]}
    out = []
    for h in he:
        hit = next((by_apn[a] for a in h["apns"] if a in by_apn), None)
        if hit:
            hit["he_capacity"] = h["he_capacity"]
            hit["rezone_capacity"] = h["rezone_capacity"]
        else:
            out.append(h)
    return sla + out


def zone_from_code(city, code):
    for pat, cls in RULES["zone_code_classes"].get((city or "").upper(), []):
        if re.search(pat, code or "", re.I):
            return cls
    return None


def coverage(data_dir):
    """Bounding box each layer was fetched for; checks outside it are 'pending', not 'clear'."""
    p = find(data_dir, "_manifest.json")
    m = json.load(open(p)) if p else {}
    return {k: v.get("bbox") for k, v in m.items()}


def load_pressure(data_dir, today):
    p = find(data_dir, r".*rhna_progress_6\.csv")
    if not p:
        return {}
    d = pd.read_csv(p)
    out = {}
    for _, r in d.iterrows():
        start, end = [pd.to_datetime(x.strip()) for x in r["Planning Period"].split("-")]
        elapsed = min(max((pd.Timestamp(today) - start) / (end - start), 0), 1)
        built = r["VLI UNITS"] + r["LI UNITS"]
        target = r["RHNA VLI"] + r["RHNA LI"]
        pct = built / target if target else None
        on_pace = target * elapsed
        out[r["Jurisdiction"].strip().upper()] = {
            "period": r["Planning Period"],
            "lower_income_built": int(built), "lower_income_target": int(target),
            "lower_income_pct": round(pct, 3) if pct is not None else None,
            "cycle_elapsed_pct": round(float(elapsed), 3),
            "behind_pace_homes": max(int(round(on_pace - built)), 0),
            "all_income_built": int(built + r["MOD UNITS"] + r["ABOVE MOD UNITS"]),
            "all_income_target": int(target + r["RHNA MOD"] + r["RHNA ABOVE MOD"]),
            # 0 = on or ahead of pace, 100 = nothing built
            "score": round(100 * min(max(1 - (pct / elapsed if elapsed else 1), 0), 1)) if pct is not None else None,
        }
    return out


def optional_layer(data_dir, name):
    p = find(data_dir, f"{name}.geojson")
    if not p:
        return None
    g = gpd.read_file(p)
    return g if len(g) else None


# ---------------------------------------------------------------- checks
def check_pathways(site, hazards):
    zc = zone_from_code(site["city"], site.get("zone_code")) or zone_class(site.get("zoning_text"))
    acres = site.get("acres")
    sqft = acres * SQFT_PER_ACRE if acres else None
    vacant = "vacant" in (site.get("existing_use") or "").lower()
    P = RULES["pathways"]
    out = []

    def add(pid, status, homes, why):
        out.append({"id": pid, "name": P[pid]["name"], "plain": P[pid]["plain"],
                    "status": status, "homes": homes, "why": why,
                    "rule_status": P[pid]["status"], "source": P[pid].get("source"),
                    "ownership": P[pid].get("ownership", False)})

    # SB 684 / SB 1123
    r = P["SB684_SB1123"]
    if sqft is None:
        add("SB684_SB1123", "unknown", None, "Lot size unknown.")
    elif zc == "multi_family" and acres <= r["max_acres_multifamily_zone"]:
        n = min(r["max_homes"], int(sqft // r["min_new_lot_sqft"]))
        add("SB684_SB1123", "likely", n, f"Multifamily zoning, {acres:.2f} acres (limit {r['max_acres_multifamily_zone']}).")
    elif zc == "single_family" and acres <= r["max_acres_singlefamily_zone_vacant"]:
        n = min(r["max_homes"], int(sqft // r["min_new_lot_sqft_singlefamily"]))
        add("SB684_SB1123", "likely" if vacant else "maybe", n,
            "Single-family zoning under 1.5 acres" + ("" if vacant else "; lot must be vacant (current use says otherwise)."))
    elif zc in ("multi_family", "single_family"):
        add("SB684_SB1123", "no", 0, f"Lot is {acres:.2f} acres, over the size limit.")
    else:
        add("SB684_SB1123", "no", 0, f"Zoning reads as {zc.replace('_', ' ')}, not residential.")

    # SB 9
    r = P["SB9"]
    if zc != "single_family":
        add("SB9", "no", 0, "Only applies in single-family zones.")
    elif sqft and sqft < 2 * r["min_new_lot_sqft"]:
        add("SB9", "no", 0, "Too small to split into two 1,200 sq ft lots.")
    elif hazards.get("fire_vh") or hazards.get("flood_sfha"):
        add("SB9", "maybe", r["max_homes"], "In a very high fire or flood hazard zone: allowed only with mitigation.")
    else:
        add("SB9", "likely", r["max_homes"], "Single-family zone, big enough to split into two lots of 1,200+ sq ft.")

    # AB 2011: two variants
    comm = zc in ("commercial", "commercial_option")
    caveat = " Zoning is open space with a commercial option: confirm commercial use is allowed." \
        if zc == "commercial_option" else ""
    r = P["AB2011_100"]
    if comm and sqft:
        add("AB2011_100", "maybe" if caveat else "likely", int(acres * r["density_du_per_acre"]),
            f"Commercial zoning, {r['density_du_per_acre']} homes/acre (metro minimum)." + caveat)
    else:
        add("AB2011_100", "no", 0, "Not commercially zoned.")
    r = P["AB2011_MIXED"]
    if comm and sqft:
        near = site.get("major_transit_mi") is not None and site["major_transit_mi"] <= 0.5
        if near:
            dens, why = r["density_near_major_transit"], "within ½ mile of a major transit stop"
        elif acres < 1:
            dens, why = r["density_lt_1_acre"], "site under 1 acre"
        else:
            dens, why = r["density_ge_1_acre_corridor_lt_100ft"], \
                f"1+ acre; {r['density_ge_1_acre_corridor_ge_100ft']}/acre if the street is 100+ ft wide"
        add("AB2011_MIXED", "maybe", int(acres * dens),
            f"{dens} homes/acre ({why}). Must front a commercial corridor (70–150 ft wide street): check frontage. "
            "For-sale: 15% lower-income or 30% moderate-income homes." + caveat)
    else:
        add("AB2011_MIXED", "no", 0, "Not commercially zoned.")

    # SB 4: needs a faith/college owner
    if site.get("owner_type") == "religious_proxy" and acres:
        d = P["SB4"]["density_residential_zone_du_per_acre"] if zc in ("single_family", "multi_family") \
            else P["SB4"]["density_nonresidential_zone_du_per_acre"]
        add("SB4", "maybe", int(acres * d),
            f"Used as a religious facility today, so likely faith-owned (proxy: confirm owner with the Assessor). "
            f"{d} homes/acre, 100% affordable (up to 20% moderate).")
    elif site.get("owner_type") in ("religious", "college"):
        d = P["SB4"]["density_residential_zone_du_per_acre"] if zc in ("single_family", "multi_family") \
            else P["SB4"]["density_nonresidential_zone_du_per_acre"]
        add("SB4", "likely", int(acres * d) if acres else None, f"Faith/college owner, {d} homes/acre.")
    else:
        add("SB4", "no" if site["source"] == "surplus_land" else "unknown", 0,
            "Public agency owner, so SB 4 does not apply." if site["source"] == "surplus_land"
            else "Owner type unknown (needs Assessor or proxy data).")

    # City's own Housing Element capacity
    he = site.get("he_capacity")
    if he and he["total"]:
        add("HOUSING_ELEMENT", "likely", he["total"],
            f'Listed for {he["total"]} homes: {he["lower"]} lower-income, {he["moderate"]} moderate, '
            f'{he["above_moderate"]} above-moderate.'
            + (f' Also on the rezone list ({site["rezone_capacity"]} homes once rezoned).' if site.get("rezone_capacity") else ""))
    else:
        add("HOUSING_ELEMENT", "no" if he is not None or site["source"] == "surplus_land" else "unknown", 0,
            "Not on the city's Housing Element site list.")

    # Base zoning
    dens = RULES["zone_density"]
    code = next((k for k in dens if not k.startswith("_") and k.lower() in (site.get("zoning_text") or "").lower()), None)
    if code and acres:
        add("BASE_ZONING", "likely", int(acres * dens[code]), f"Zone {code}: {dens[code]} homes/acre.")
    else:
        add("BASE_ZONING", "unknown", None, "Allowed density for this zone not yet in the tool.")

    if zc in ("open_space", "public", "industrial", "specific_plan", "other", "unknown"):
        note = {"open_space": "Open space: would need rezoning.",
                "specific_plan": "Specific plan: read the plan for allowed density.",
                "industrial": "Industrial: would need rezoning or a state law override."}.get(zc)
        site["zoning_note"] = note
    site["zone_class"] = zc
    viable = [p for p in out if p["status"] in ("likely", "maybe") and p["homes"]]
    # Prefer ownership pathways (the brief is about ownership homes), then certainty, then size
    best = max(viable, key=lambda p: (p["status"] == "likely", p["ownership"], p["homes"]), default=None)
    site["pathways"] = out
    site["best_pathway"] = best["id"] if best else None
    site["homes"] = best["homes"] if best else 0
    return site


def people_for(homes):
    p = RULES["people"]
    avg_br = sum(int(k) * v for k, v in p["bedroom_mix"].items())
    return round(homes * avg_br * p["persons_per_bedroom"]), round(avg_br, 2)


def livability(site, comps):
    W = RULES["livability_weights"]
    have = {k: v for k, v in comps.items() if v is not None}
    if not have:
        return None
    return round(sum(W[k] * v for k, v in have.items()) / sum(W[k] for k in have))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    today = RULES["pressure"]["today"]

    tracts = load_tracts(a.data)
    sites = merge_he_into_surplus(group_sites(load_surplus(a.data, tracts)), load_he_sites(a.data))
    taken = {x.replace(" ", "") for s in sites for x in s["apns"]}
    lu_sites = [s for s in land_use_sites(a.data) if not any(x in taken for x in s["apns"])]
    sites += lu_sites
    pressure = load_pressure(a.data, today)
    cover = coverage(a.data)

    pts = gpd.GeoDataFrame(sites, geometry=gpd.points_from_xy([s["lon"] for s in sites],
                                                              [s["lat"] for s in sites]), crs=4326)
    opp = gpd.sjoin(pts, tracts, how="left", predicate="within")
    opp = opp[~opp.index.duplicated()]

    layers = {n: optional_layer(a.data, n) for n in
              ["caltrans_hqta", "calenviroscreen5", "oc_floodplains", "oc_fire_lra",
               "oc_liquefaction", "cgs_landslide", "scag_major_transit_stops"]}
    pts_m = pts.to_crs(METRIC)

    zon = optional_layer(a.data, "scag_zoning")
    if zon is not None:
        zj = gpd.sjoin(pts, zon[["APN24", "ZN24_CITY", "CITY", "ACRES", "SLOPE", "geometry"]], how="left", predicate="within")
        zj = zj[~zj.index.duplicated()]
        for i, s in enumerate(sites):
            code = zj.iloc[i].get("ZN24_CITY")
            if isinstance(code, str) and code.strip() and not s.get("zone_code"):
                s["zone_code"] = code.strip()
                s["slope"] = None if pd.isna(zj.iloc[i].get("SLOPE")) else float(zj.iloc[i]["SLOPE"])

    if zon is not None:
        zcities = set(zon.CITY.str.title())
        zb = zon.total_bounds
        for s in sites:
            outside = not (zb[0] <= s["lon"] <= zb[2] and zb[1] <= s["lat"] <= zb[3])
            if s["city"] in zcities and outside:
                s["city_note"] = f"{s['city']} mailing address; parcel is outside {s['city']} city limits (likely unincorporated county)"
                s["city"] = "Orange County (unincorporated)"

    def covered(name, s):
        b = cover.get(name)
        return b is None or (b[0] <= s["lon"] <= b[2] and b[1] <= s["lat"] <= b[3])

    def hits(name, i):
        L = layers[name]
        if L is None or not covered(name, sites[i]):
            return None
        return L[L.intersects(pts.geometry.iloc[i])]

    for i, s in enumerate(sites):
        row = opp.iloc[i]
        s["tract"] = row.get("fips")
        s["opportunity_category"] = row.get("oppcat")
        s["env_burden_top5"] = bool(row.get("env_burden_flag") == 1)

        hz, comps, pending = {}, {}, []
        comps["opportunity"] = round(row.oppscore / 9 * 100) if pd.notna(row.get("oppscore")) else None

        if layers["caltrans_hqta"] is not None and covered("caltrans_hqta", s):
            h = layers["caltrans_hqta"].to_crs(METRIC)
            d_mi = h.distance(pts_m.geometry.iloc[i]).min() / 1609.34
            s["transit_distance_mi"] = round(d_mi, 2)
            comps["transit"] = round(max(0, 100 * (1 - d_mi)))       # 100 inside, 0 at 1 mile
        else:
            comps["transit"] = None; pending.append("transit (Caltrans HQTA)")

        if layers["calenviroscreen5"] is not None and covered("calenviroscreen5", s):
            c = hits("calenviroscreen5", i)
            col = next((k for k in c.columns if re.search(r"ciscorep|ces.*pctl|percentile", k, re.I)), None)
            if len(c) and col:
                comps["environment"] = round(100 - float(c.iloc[0][col]))
        else:
            comps["environment"] = None; pending.append("environment (CalEnviroScreen)")

        if (layers["oc_floodplains"] is not None and covered("oc_floodplains", s)) or \
           (layers["oc_fire_lra"] is not None and covered("oc_fire_lra", s)):
            score = 100
            f = hits("oc_floodplains", i)
            if f is not None and len(f):
                zones = ",".join(map(str, f.get("FLD_ZONE", pd.Series(["?"])).unique()))
                hz["flood_zone"] = zones
                if re.search(r"\b(A|AE|AH|AO|V|VE)\b", zones):
                    hz["flood_sfha"] = True; score -= 40
            fr = hits("oc_fire_lra", i)
            if fr is not None and len(fr):
                txt = " ".join(map(str, fr.drop(columns="geometry").iloc[0].values)).lower()
                hz["fire_zone"] = txt[:60]
                if "very high" in txt:
                    hz["fire_vh"] = True; score -= 40
            if hits("oc_liquefaction", i) is not None and len(hits("oc_liquefaction", i)):
                hz["liquefaction"] = True; score -= 10
            if hits("cgs_landslide", i) is not None and len(hits("cgs_landslide", i)):
                hz["landslide"] = True; score -= 30
            comps["hazard"] = max(score, 0)
        else:
            comps["hazard"] = None; pending.append("hazards (flood, fire, ground)")

        if layers["scag_major_transit_stops"] is not None and covered("scag_major_transit_stops", s):
            mts = layers["scag_major_transit_stops"].to_crs(METRIC)
            s["major_transit_mi"] = round(mts.distance(pts_m.geometry.iloc[i]).min() / 1609.34, 2)
        s["hazards"] = hz
        s["livability_parts"] = comps
        s["livability"] = livability(s, comps)
        s["livability_pending"] = pending
        s["pressure"] = pressure.get(s["city"].upper())
        check_pathways(s, hz)
        s["people"], s["avg_bedrooms"] = people_for(s["homes"])
        s["lot_sqft"] = round(s["acres"] * SQFT_PER_ACRE) if s.get("acres") else None

    oc_cities = sorted({k for k in pressure if k in {
        "ALISO VIEJO", "ANAHEIM", "BREA", "BUENA PARK", "COSTA MESA", "CYPRESS", "DANA POINT",
        "FOUNTAIN VALLEY", "FULLERTON", "GARDEN GROVE", "HUNTINGTON BEACH", "IRVINE", "LA HABRA",
        "LA PALMA", "LAGUNA BEACH", "LAGUNA HILLS", "LAGUNA NIGUEL", "LAGUNA WOODS", "LAKE FOREST",
        "LOS ALAMITOS", "MISSION VIEJO", "NEWPORT BEACH", "ORANGE", "PLACENTIA",
        "RANCHO SANTA MARGARITA", "SAN CLEMENTE", "SAN JUAN CAPISTRANO", "SANTA ANA", "SEAL BEACH",
        "STANTON", "TUSTIN", "VILLA PARK", "WESTMINSTER", "YORBA LINDA", "ORANGE COUNTY"}})

    # Parcel outlines for surplus sites (APN match against the parcel land-use layer)
    elu = optional_layer(a.data, "scag_existing_landuse")
    if elu is not None:
        by_apn = {str(k): g for k, g in zip(elu.APN24, elu.geometry)}
        for s in sites:
            if s.get("_geom") is None:
                gs = [by_apn.get(re.sub(r"[^0-9]", "", x)) for x in s["apns"]]
                gs = [g for g in gs if g is not None]
                if gs:
                    s["_geom"] = gpd.GeoSeries(gs, crs=4326).union_all()

    # Aerial view: photo requests for the configured cities, then usable area + icons
    acfg = RULES["aerial"]
    aerial_sites = [s for s in sites if s["city"] in acfg["cities"] and s["homes"] > 0 and s.get("_geom") is not None]
    os.makedirs(a.out, exist_ok=True)
    n_req = aerial.write_requests(aerial_sites, a.out)
    n_done = aerial.build_aerials(aerial_sites, a.data, a.out, RULES)
    print(f"aerial: {n_req} photo requests written to {a.out}/aerial_requests.json, {n_done} photos laid out")

    # Map layers as compact GeoJSON for the pan/zoom map (no tile server needed)
    def gj(gdf, tol, props=()):
        if gdf is None or not len(gdf):
            return None
        g = gdf.to_crs(4326).copy()
        g["geometry"] = shapely.set_precision(g.geometry.simplify(tol, preserve_topology=True), 1e-5)
        g = g[~g.geometry.is_empty]
        return json.loads(g[list(props) + ["geometry"]].to_json(drop_id=True))

    roads = optional_layer(a.data, "roads")
    if roads is not None:
        roads["major"] = roads.MTFCC.isin(["S1100", "S1200"]).astype(int)
        roads["FULLNAME"] = roads.FULLNAME.fillna("")
    flood = layers.get("oc_floodplains")
    if flood is not None and "FLD_ZONE" in flood.columns:
        flood = flood[flood.FLD_ZONE.astype(str).str.match(r"^(A|AE|AH|AO|V|VE)$")]
        flood = gpd.GeoDataFrame(geometry=[flood.union_all()], crs=flood.crs) if len(flood) else None
    hq = layers.get("caltrans_hqta")
    hq = gpd.GeoDataFrame(geometry=[hq.union_all()], crs=hq.crs) if hq is not None else None
    tr = tracts.rename(columns={"oppcat": "cat"})
    map_layers = {
        "tracts": gj(tr, 0.0006, ["cat"]),
        "roads": gj(roads, 0.00002, ["FULLNAME", "major"]) if roads is not None else None,
        "transit": gj(hq, 0.0003),
        "flood": gj(flood, 0.0003),
        "bounds": [[float(tracts.total_bounds[1]), float(tracts.total_bounds[0])],
                   [float(tracts.total_bounds[3]), float(tracts.total_bounds[2])]],
    }
    to_ll = lambda x, y: gpd.GeoSeries.from_xy([x], [y], crs=3857).to_crs(4326).iloc[0]
    for s in sites:
        if s.get("_geom") is not None and s["city"] in acfg["cities"]:
            g = shapely.set_precision(s["_geom"].simplify(0.000005), 1e-6)
            s["outline"] = json.loads(gpd.GeoSeries([g]).to_json())["features"][0]["geometry"]
        if s.get("aerial") and s.get("_bbox_merc"):
            b = s["_bbox_merc"]; sw, ne = to_ll(b[0], b[1]), to_ll(b[2], b[3])
            s["aerial"]["bounds"] = [[round(sw.y, 7), round(sw.x, 7)], [round(ne.y, 7), round(ne.x, 7)]]

    os.makedirs(a.out, exist_ok=True)
    payload = {
        "map": map_layers,
        "generated": date.today().isoformat(),
        "rules": RULES,
        "cities": {c: pressure[c] for c in oc_cities},
        "sites": sites,
        "sources": [
            {"name": "HCD Surplus Land Act notices", "url": "https://data.ca.gov/dataset/surplus-land-act-notices-of-availability-received"},
            {"name": "HCD 6th-cycle RHNA progress", "url": "https://data.ca.gov/@california-department-of-housing-and-community-development"},
            {"name": "SCAG Housing Element sites, zoning and 2024 land use", "url": "https://maps.scag.ca.gov/scaggis/rest/services/LDX"},
            {"name": "TCAC/HCD 2026 Opportunity Map", "url": "https://www.treasurer.ca.gov/ctcac/opportunity.asp"},
            {"name": "CalEnviroScreen 5.0 (OEHHA)", "url": "https://oehha.ca.gov/calenviroscreen"},
            {"name": "Caltrans high-quality transit areas", "url": "https://gisdata-caltrans.opendata.arcgis.com/"},
            {"name": "OC Public Works floodplains, liquefaction, building footprints", "url": "https://www.ocgis.com/arcpub/rest/services"},
            {"name": "CGS landslide zones · CAL FIRE hazard zones", "url": "https://maps.conservation.ca.gov/cgs/"},
            {"name": "USDA NAIP aerial imagery (via USGS)", "url": "https://imagery.nationalmap.gov/"},
            {"name": "US Census TIGER roads", "url": "https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html"},
            {"name": "State housing law: HCD fact sheets", "url": "https://www.hcd.ca.gov/planning-and-research/hcd-memos"},
        ],
    }
    for s in sites:
        s.pop("_geom", None); s.pop("_bbox_merc", None)
    json.dump(payload, open(os.path.join(a.out, "sites.json"), "w"), indent=1, default=str)
    tpl = open(os.path.join(HERE, "template.html")).read()
    open(os.path.join(a.out, "index.html"), "w").write(
        tpl.replace("/*__DATA__*/null", json.dumps(payload, default=str)))
    print(f"{len(sites)} sites, {sum(1 for s in sites if s['homes'])} with a likely/maybe pathway, "
          f"{len(payload['cities'])} OC cities with RHNA pressure -> {a.out}/")


if __name__ == "__main__":
    main()
