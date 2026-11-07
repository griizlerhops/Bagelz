"""
Download an aerial photo and building footprints for each site in out/aerial_requests.json.

    python pipeline.py --data data --out out     # writes out/aerial_requests.json
    python fetch_aerials.py                      # saves data/aerials/*.jpg, data/footprints/*.geojson
    python pipeline.py --data data --out out     # lays out usable area + homes on the photos

Photos: USDA NAIP orthoimagery through USGS (public domain), ~0.6 m per pixel.
Footprints: OC Public Works building footprints.
Already-downloaded sites are skipped, so you can stop and re-run any time.
"""
import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor

import requests

REQ = os.path.join("out", "aerial_requests.json")
IMG_DIR = os.path.join("data", "aerials")
FP_DIR = os.path.join("data", "footprints")
PX = 640
PAUSE = 0.3

NAIP = [   # tried in order; the first that answers is used for every photo
    "https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer/exportImage",
    "https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer/exportImage",
]
FOOTPRINTS = "https://www.ocgis.com/arcpub/rest/services/Map_Layers/Building_Footprints/MapServer/0/query"

s = requests.Session()
s.headers["User-Agent"] = "uci-impact-lab-hackathon-demo"


def get_photo(url, bbox):
    r = s.get(url, params={
        "bbox": ",".join(map(str, bbox)), "bboxSR": 3857, "imageSR": 3857,
        "size": f"{PX},{PX}", "format": "jpg", "f": "image"}, timeout=60)
    r.raise_for_status()
    if not r.headers.get("content-type", "").startswith("image"):
        raise RuntimeError(r.text[:200])
    return r.content


def get_footprints(bbox):
    r = s.get(FOOTPRINTS, params={
        "geometry": ",".join(map(str, bbox)), "geometryType": "esriGeometryEnvelope",
        "inSR": 3857, "spatialRel": "esriSpatialRelIntersects",
        "outFields": "OBJECTID", "returnGeometry": "true", "outSR": 4326, "f": "geojson"}, timeout=20)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data


def photo(q):
    img = os.path.join(IMG_DIR, q["id"] + ".jpg")
    if os.path.exists(img):
        return
    last = None
    for url in NAIP:
        try:
            open(img, "wb").write(get_photo(url, q["bbox3857"])); return
        except Exception as e:
            last = e
    raise last


def footprints(q):
    fp = os.path.join(FP_DIR, q["id"] + ".geojson")
    if not os.path.exists(fp):
        json.dump(get_footprints(q["bbox3857"]), open(fp, "w"))


def run_all(label, fn, items):
    failed, done = [], 0
    def wrap(q):
        try:
            fn(q); return q, None
        except Exception as e:
            return q, e
    with ThreadPoolExecutor(max_workers=6) as ex:   # a handful of parallel requests; still gentle
        for q, err in ex.map(wrap, items):
            done += 1
            if err:
                failed.append(q); print(f"  {label} [{done}/{len(items)}] FAILED {q['name'][:35]}: {str(err)[:120]}")
            elif done % 10 == 0 or done == len(items):
                print(f"  {label} [{done}/{len(items)}]")
    return failed


def main():
    if not os.path.exists(REQ):
        sys.exit("Run `python pipeline.py --data data --out out` first to create out/aerial_requests.json")
    reqs = json.load(open(REQ))
    os.makedirs(IMG_DIR, exist_ok=True); os.makedirs(FP_DIR, exist_ok=True)
    need_img = [q for q in reqs if not os.path.exists(os.path.join(IMG_DIR, q["id"] + ".jpg"))]
    need_fp = [q for q in reqs if not os.path.exists(os.path.join(FP_DIR, q["id"] + ".geojson"))]
    print(f"Photos: {len(reqs) - len(need_img)} done, {len(need_img)} to go")
    f1 = run_all("photo", photo, need_img)
    print(f"Footprints: {len(reqs) - len(need_fp)} done, {len(need_fp)} to go (county server can be slow; skips after 20 s)")
    f2 = run_all("footprints", footprints, need_fp)
    print(f"\nDone. {len(f1)} photos and {len(f2)} footprint files failed" + (" (re-run to retry just those)." if f1 or f2 else "."))


if __name__ == "__main__":
    main()
