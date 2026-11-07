"""
Aerial view helpers: parcel outlines -> photo requests -> usable area + home icons.

Coordinates for the page overlay are pixels on a square Web Mercator (EPSG:3857)
photo, so the parcel lines sit exactly on the NAIP image fetch_aerials.py downloads.
"""
import json, math, os, re, shutil

import geopandas as gpd
from shapely.geometry import Point, box, shape
from shapely.ops import unary_union

IMG_PX = 640
MERC = 3857


def safe_id(s):
    return re.sub(r"[^A-Za-z0-9_-]", "_", s)


def photo_bbox(geom_merc):
    """Square box around the parcel(s) with some context around the edges."""
    minx, miny, maxx, maxy = geom_merc.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    side = max(maxx - minx, maxy - miny) * 1.5 + 40     # metres (≈, Mercator at 33.7°N)
    side = max(side, 90)
    return [cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2]


def write_requests(sites, out_dir):
    reqs = []
    for s in sites:
        g = s.get("_geom")
        if g is None:
            continue
        gm = gpd.GeoSeries([g], crs=4326).to_crs(MERC).iloc[0]
        s["_bbox_merc"] = photo_bbox(gm)
        reqs.append({"id": safe_id(s["id"]), "bbox3857": [round(v, 2) for v in s["_bbox_merc"]],
                     "name": s["name"], "city": s["city"]})
    json.dump(reqs, open(os.path.join(out_dir, "aerial_requests.json"), "w"), indent=1)
    return len(reqs)


def to_px(geom, bb):
    """Shapely geometry in 3857 -> SVG path string in image pixels."""
    xmin, ymin, xmax, ymax = bb
    k = IMG_PX / (xmax - xmin)

    def ring(coords):
        return "M" + "L".join(f"{(x - xmin) * k:.1f},{(ymax - y) * k:.1f}" for x, y in coords) + "Z"

    parts = []
    geoms = getattr(geom, "geoms", [geom])
    for g in geoms:
        if g.is_empty or g.geom_type != "Polygon":
            continue
        parts.append(ring(g.exterior.coords) + "".join(ring(r.coords) for r in g.interiors))
    return "".join(parts)


def layout(usable, n, bb):
    """Spread n icons evenly over the usable polygon (grid, shrinking until n fit)."""
    if n <= 0 or usable.is_empty:
        return [], 0
    xmin, ymin, xmax, ymax = usable.bounds
    step = math.sqrt(usable.area / n)
    for _ in range(40):
        pts = []
        y = ymax - step / 2
        while y > ymin:
            x = xmin + step / 2
            while x < xmax:
                p = Point(x, y)
                if usable.contains(p.buffer(step * 0.25)):
                    pts.append(p)
                x += step
            y -= step
        if len(pts) >= n:
            break
        step *= 0.88
    if len(pts) > n:            # spread evenly over the whole lot, not just the top rows
        pts = [pts[int(i * len(pts) / n)] for i in range(n)]
    bxmin, bymin, bxmax, bymax = bb
    k = IMG_PX / (bxmax - bxmin)
    return [{"x": round((p.x - bxmin) * k, 1), "y": round((bymax - p.y) * k, 1)} for p in pts], step * k


def build_aerials(sites, data_dir, out_dir, rules):
    cfg = rules["aerial"]
    img_dir = os.path.join(data_dir, "aerials")
    fp_dir = os.path.join(data_dir, "footprints")
    os.makedirs(os.path.join(out_dir, "aerials"), exist_ok=True)
    done = 0
    for s in sites:
        if "_bbox_merc" not in s:
            continue
        sid = safe_id(s["id"])
        img = os.path.join(img_dir, f"{sid}.jpg")
        has_img = os.path.exists(img)
        bb = s["_bbox_merc"]
        parcel = gpd.GeoSeries([s["_geom"]], crs=4326).to_crs(MERC).iloc[0]
        # Mercator metres are stretched by 1/cos(lat): convert areas to true sq ft
        scale = math.cos(math.radians(s["lat"])) ** 2
        fp_path = os.path.join(fp_dir, f"{sid}.geojson")
        bldg = None
        stale = None
        if os.path.exists(fp_path):
            fp = gpd.read_file(fp_path)
            if len(fp):
                fp = fp.set_crs(4326, allow_override=True).to_crs(MERC)
                bldg = unary_union(list(fp.geometry.buffer(0))).intersection(parcel)
        # Lots the notice or land-use data call vacant/parking: footprints are often out of date
        use = (s.get("existing_use") or "").lower()
        if bldg is not None and not bldg.is_empty and any(w in use for w in ("vacant", "parking", "paved lot")):
            stale = round(bldg.area * scale * 10.7639)
            bldg = None
        setback = cfg["setback_m"] / math.cos(math.radians(s["lat"]))
        usable = parcel.buffer(-setback)
        if bldg is not None and not bldg.is_empty:
            usable = usable.difference(bldg.buffer(cfg["building_clearance_m"] / math.cos(math.radians(s["lat"]))))
        usable = usable.buffer(0)
        # drop slivers too thin to build on
        usable = unary_union([g for g in getattr(usable, "geoms", [usable])
                              if g.area * scale >= cfg["min_patch_sqm"]]) if not usable.is_empty else usable

        best = next((p for p in s["pathways"] if p["id"] == s["best_pathway"]), None)
        homes = s["homes"]
        house_mode = best is not None and best["id"] in cfg["house_pathways"]
        per_block = 1 if house_mode else max(cfg["homes_per_block"], math.ceil(homes / cfg["max_blocks"]))
        n_icons = homes if house_mode else math.ceil(homes / per_block) if homes else 0
        icons, step_px = ([], 0)
        if n_icons and not usable.is_empty:
            icons, step_px = layout(usable, n_icons, bb)
        sqm = lambda g: 0 if g is None or g.is_empty else g.area * scale
        s["aerial"] = {
            "img": f"aerials/{sid}.jpg" if has_img else None, "px": IMG_PX,
            "metres_across": round((bb[2] - bb[0]) * math.cos(math.radians(s["lat"]))),
            "parcel": to_px(parcel, bb),
            "buildings": to_px(bldg, bb) if bldg is not None and not bldg.is_empty else "",
            "usable": to_px(usable, bb) if not usable.is_empty else "",
            "parcel_sqft": round(sqm(parcel) * 10.7639),
            "building_sqft": round(sqm(bldg) * 10.7639),
            "usable_sqft": round(sqm(usable) * 10.7639),
            "footprints_loaded": os.path.exists(fp_path),
            "stale_footprint_sqft": stale,
            "icon": "house" if house_mode else "block",
            "homes_per_icon": per_block,
            "icons": icons,
            "icon_px": round(min(max(step_px * 0.62, 9), 34), 1),
            "fits": len(icons) >= n_icons,
        }
        if has_img:
            shutil.copy(img, os.path.join(out_dir, "aerials", f"{sid}.jpg"))
            done += 1
    return done
