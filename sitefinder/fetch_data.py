"""
Fetch the public layers for the parcel-screening demo and save them as files.

Run on your own laptop (needs internet):
    pip install requests
    python fetch_data.py                 # default city: Santa Ana
    python fetch_data.py --city "Anaheim"

Output goes to ./data/ as GeoJSON (or Esri JSON if a server can't do GeoJSON),
plus data/_manifest.json recording the URL, query and fetch time for each layer.
Zip the data/ folder and send it back.

Be kind to public servers: this pauses between requests and skips layers
already downloaded (delete a file to re-fetch it).
"""
import argparse, json, os, sys, time
from datetime import datetime, timezone

import requests

OUT = "data"
PAUSE = 0.5          # seconds between requests
CHUNK = 500          # object IDs per request
TIMEOUT = 90
MIN_ACRES = 0.2      # target 4-12 home sites; drops tiny lots to keep files small

SCAG = "https://maps.scag.ca.gov/scaggis/rest/services"
OCGIS = "https://www.ocgis.com/arcpub/rest/services"

session = requests.Session()
session.headers["User-Agent"] = "uci-impact-lab-hackathon-demo"
manifest = {}


def get(url, params, tries=3):
    for i in range(tries):
        try:
            # Long object-ID lists overflow a GET URL; ArcGIS accepts the same query as a POST
            if len(str(params)) > 1500:
                r = session.post(url, data=params, timeout=TIMEOUT)
            else:
                r = session.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                raise RuntimeError(data["error"])
            return data
        except Exception as e:
            if i == tries - 1:
                raise
            print(f"    retry {i + 1} after error: {e}")
            time.sleep(3 * (i + 1))   # FEMA/others often fail on first call


def layer_url(service_url, layer_id=None):
    """Return .../MapServer/<id>. If no id given, use the service's first layer."""
    if layer_id is not None:
        return f"{service_url}/{layer_id}"
    info = get(service_url, {"f": "json"})
    layers = info.get("layers") or []
    if not layers:
        raise RuntimeError(f"No layers listed at {service_url}")
    print(f"    using layer {layers[0]['id']} ({layers[0]['name']})")
    return f"{service_url}/{layers[0]['id']}"


def fetch(name, *args, **kw):
    """One failing layer is reported and skipped; the rest still download."""
    try:
        _fetch(name, *args, **kw)
    except Exception as e:
        print(f"[FAILED] {name}: {str(e)[:300]}")
        failed.append(name)


failed = []


def _fetch(name, service_url, layer_id=None, where="1=1", bbox=None,
          out_fields="*", geometry=True):
    path_geo = os.path.join(OUT, f"{name}.geojson")
    path_esri = os.path.join(OUT, f"{name}.esri.json")
    if os.path.exists(path_geo) or os.path.exists(path_esri):
        print(f"[skip] {name} (already downloaded)")
        return
    print(f"[fetch] {name}")
    url = layer_url(service_url, layer_id)

    base = {"where": where, "outSR": 4326}
    if bbox:
        base.update({
            "geometry": ",".join(str(v) for v in bbox),
            "geometryType": "esriGeometryEnvelope",
            "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects",
        })

    # Page by object IDs: works on every ArcGIS version, unlike resultOffset.
    ids = get(f"{url}/query", {**base, "returnIdsOnly": "true", "f": "json"})
    oids = sorted(ids.get("objectIds") or [])
    oid_field = ids.get("objectIdFieldName", "OBJECTID")
    print(f"    {len(oids)} features")

    features, fmt = [], "geojson"
    for start in range(0, len(oids), CHUNK):
        chunk = oids[start:start + CHUNK]
        params = {
            "objectIds": ",".join(map(str, chunk)),
            "outFields": out_fields,
            "returnGeometry": "true" if geometry else "false",
            "outSR": 4326,
            "f": fmt,
        }
        try:
            page = get(f"{url}/query", params)
        except Exception:
            if fmt == "geojson":          # older servers: fall back to Esri JSON
                print("    GeoJSON not supported, switching to Esri JSON")
                fmt = "json"
                params["f"] = "json"
                page = get(f"{url}/query", params)
            else:
                raise
        features.extend(page.get("features", []))
        print(f"    {min(start + CHUNK, len(oids))}/{len(oids)}")
        time.sleep(PAUSE)

    os.makedirs(OUT, exist_ok=True)
    if fmt == "geojson":
        with open(path_geo, "w") as f:
            json.dump({"type": "FeatureCollection", "features": features}, f)
        saved = path_geo
    else:
        with open(path_esri, "w") as f:
            json.dump({"features": features, "objectIdField": oid_field}, f)
        saved = path_esri

    manifest[name] = {
        "url": url, "where": where, "bbox": bbox, "count": len(features),
        "format": fmt, "file": os.path.basename(saved),
        "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    save_manifest()


def save_manifest():
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "_manifest.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(manifest)
    json.dump(old, open(p, "w"), indent=2)


def fetch_roads(bbox):
    """Census TIGER roads for Orange County: freeways and major roads county-wide,
    every street inside the focus city's box. Public domain."""
    out = os.path.join(OUT, "roads.geojson")
    if os.path.exists(out):
        print("[skip] roads (already downloaded)"); return
    try:
        import geopandas as gpd
        url = "https://www2.census.gov/geo/tiger/TIGER2024/ROADS/tl_2024_06059_roads.zip"
        print("[fetch] roads (Census TIGER, ~15 MB)")
        z = os.path.join(OUT, "tl_2024_06059_roads.zip")
        if not os.path.exists(z):
            r = session.get(url, timeout=300); r.raise_for_status(); open(z, "wb").write(r.content)
        g = gpd.read_file(f"zip://{z}").to_crs(4326)
        major = g[g.MTFCC.isin(["S1100", "S1200"])]
        local = g[(g.MTFCC == "S1400") & g.intersects(gpd.GeoSeries.from_xy([bbox[0], bbox[2]], [bbox[1], bbox[3]]).envelope.union_all().envelope)]
        roads = gpd.GeoDataFrame(pd_concat([major, local]), crs=4326)[["FULLNAME", "MTFCC", "geometry"]]
        roads["geometry"] = roads.geometry.simplify(0.00002)
        roads.to_file(out, driver="GeoJSON")
        manifest["roads"] = {"url": url, "count": len(roads), "bbox": None,
                             "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        save_manifest()
        print(f"    {len(roads)} road segments")
    except Exception as e:
        print(f"[FAILED] roads: {str(e)[:300]}"); failed.append("roads")


def pd_concat(frames):
    import pandas as pd
    return pd.concat(frames)


def bbox_of(geojson_path, pad=0.005):
    xs, ys = [], []

    def walk(c):
        if isinstance(c[0], (int, float)):
            xs.append(c[0]); ys.append(c[1])
        else:
            for x in c:
                walk(x)

    for f in json.load(open(geojson_path))["features"]:
        if f.get("geometry"):
            walk(f["geometry"]["coordinates"])
    return [min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", default="Santa Ana")
    city = ap.parse_args().city
    city_sql = city.upper().replace("'", "''")

    # 1. Parcel-level zoning for the city (APN, zone, ACRES, SLOPE). Backbone layer.
    fetch("scag_zoning", f"{SCAG}/LDX/Zoning_poly_OR/MapServer",
          where=f"UPPER(CITY) LIKE '%{city_sql}%' AND ACRES >= {MIN_ACRES}")

    zoning = os.path.join(OUT, "scag_zoning.geojson")
    if not os.path.exists(zoning):
        sys.exit("Zoning came back in Esri JSON; send me the folder and I'll adapt.")
    bbox = bbox_of(zoning)
    print(f"    city bounding box: {bbox}")

    # 2. Housing Element sites, all of Orange County (2,126 rows).
    fetch("scag_he_sites", f"{SCAG}/LDX/HousingElementSite_poly_scag/MapServer",
          where="COUNTY='Orange'")
    fetch("scag_he_rezone", f"{SCAG}/LDX/HousingElementRezone_poly_scag/MapServer",
          bbox=bbox)

    # 3. General plan + existing land use (vacant / parking / low-intensity).
    fetch("scag_general_plan", f"{SCAG}/LDX/GeneralPlan_poly_OR/MapServer",
          bbox=bbox)
    fetch("scag_existing_landuse", f"{SCAG}/LDX/Existinglanduse_poly_OR/MapServer",
          bbox=bbox)

    # 4. City assessor values (Santa Ana only): no geometry, just APN + values.
    if "SANTA ANA" in city_sql:
        fetch("santa_ana_assessor",
              "https://gis.santa-ana.org/server/rest/services/Public/GIS_AssessorParcels/MapServer",
              layer_id=0, geometry=False)

    # 5. Hazards.
    fetch("oc_floodplains", f"{OCGIS}/Map_Layers/Floodplains/MapServer",
          layer_id=0, bbox=bbox)
    fetch("oc_fire_lra", f"{OCGIS}/Map_Layers/Fire_Hazard_Severity_Zones_LRA/MapServer",
          layer_id=0, bbox=bbox)
    fetch("oc_liquefaction", f"{OCGIS}/Map_Layers/Liquefaction/MapServer",
          layer_id=0, bbox=bbox)
    fetch("cgs_landslide",
          "https://services2.arcgis.com/zr3KAIbsRSUyARHG/arcgis/rest/services/CGS_Landslide_Zones/FeatureServer",
          layer_id=0, bbox=bbox)

    # 6. Livability: transit + environmental health.
    fetch("caltrans_hqta",
          "https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/CA_HQ_Transit_Areas/FeatureServer",
          layer_id=0, bbox=bbox)
    fetch("calenviroscreen5",
          "https://services1.arcgis.com/PCHfdHz4GlDNAhBb/arcgis/rest/services/calenviroscreen50results_F_070126_gdb/FeatureServer",
          layer_id=2, bbox=bbox)
    fetch("scag_major_transit_stops",
          f"{SCAG}/OpenData/Major_Transit_Stops_Plan_Year_2022/MapServer", bbox=bbox)

    # 7. Public land.
    fetch("oc_county_property",
          f"{OCGIS}/CEO_RealEstate/County_of_Orange_Property_List_OCT2025/MapServer",
          layer_id=0, bbox=bbox)

    # 8. Streets for the map
    fetch_roads(bbox)

    if failed:
        print("\nThese layers failed (re-run to retry just them):", ", ".join(failed))
    print("\nDone. Now grab the manual downloads listed in the chat, put them in data/, "
          "zip the folder and send it.")


if __name__ == "__main__":
    main()
