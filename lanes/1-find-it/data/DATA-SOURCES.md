# Data sources for Lane 1: Find it

Starting points for parcels, zoning, housing-element sites, surplus land, constraints and statute
text. Checked November 6, 2026 by fetching the page or calling the service.

**These are a few places to start.** There's much more out there, and the best teams find sources
nobody else used.

**Status key.** VERIFIED means fetched, and the contents matched the claim. UNVERIFIED means it
could not be confirmed, with the reason given. Anything UNVERIFIED is a lead, not a fact. Terms and
data change, so read the source yourself before you build on it. Be kind to public servers: cache
what you download.

**Tips.** OC county services return State Plane coordinates (wkid 2230 / 102646). Pass
`outSR=4326` and `inSR=4326` for latitude and longitude. County services return at most 1,000
records per request. FEMA's flood service can time out on the first call, so retry.

## What is hard today

Each is from a source read on the day unless marked inferred.

- Ownership type is not in the free parcel data. The county parcel layer has APN, address, year
  built and bedrooms. This is the central missing field for SB 4.
- Each law has stacked site tests. One yes or no needs several layers.
- Local code still matters inside state law. SB 9 lets cities impose objective standards (parking
  up to one space per unit, setbacks up to four feet).
- Terner Center had to work around missing zoning data. For SB 9 it says its estimates are not
  meant to predict development on any given parcel.
- Housing-element site lists can go stale (inferred: inventories are submitted when elements are
  adopted or amended).
- Surplus-notice data is messy: many rows are "Archive", and parcel size is sometimes text like
  "9,005 SF".
- Assessor roll data costs money and is not self-serve. The OC Assessor says roll products are in
  person or by written request.
- City portals differ and some do not respond. Santa Ana, Anaheim and Fullerton use different
  field names for APN and zoning. No official parcel or zoning API was found for Costa Mesa,
  Garden Grove or Irvine. SCAG's regional layers cover them.
- Eligibility does not produce homes by itself. Terner reports some of the largest cities got
  just a handful of SB 9 applications.

## 1. Parcels

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| OC Public Works / OC Survey "Parcels" (countywide) | 703,000 parcel polygons with APN (`ASSESSMENT_NO`), site address, year built, bedrooms. No owner name. No lot-size field: compute from geometry | ArcGIS REST FeatureServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/Parcels/FeatureServer/0 | VERIFIED (count + sample record). One test point-in-polygon query returned 0 features, so test your own spatial queries |
| OC Public Works service directory | Index of every county layer | ArcGIS REST directory, free | https://www.ocgis.com/arcpub/rest/services | VERIFIED |
| OC Survey service directory | Second county server. Has Zoning_2025 and ParcelFeatures | ArcGIS REST directory, free | https://ocgis.com/survey/rest/services | VERIFIED |
| OC Open GIS Data Portal | Browse and download county datasets as CSV, GeoJSON, SHP | Web hub, free | https://data-ocpw.opendata.arcgis.com/ | VERIFIED (page loads; individual downloads not tested) |
| OC Real Estate Parcels Analysis | County-held real estate parcels | ArcGIS REST FeatureServer, free | https://www.ocgis.com/arcpub/rest/services/CEO_RealEstate/Real_Estate_Parcels_Analysis/FeatureServer | VERIFIED (listed in directory; fields not inspected) |
| OC Building Footprints | 754,811 building polygons with height, address, city. Use to find vacant or low-coverage parcels | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/Building_Footprints/MapServer/0 | VERIFIED (count 754,811) |
| Santa Ana Assessor Parcels | 57,926 parcels with APN, site and mailing address, land and improvement value | ArcGIS REST MapServer, free | https://gis.santa-ana.org/server/rest/services/Public/GIS_AssessorParcels/MapServer/0 | VERIFIED |
| Anaheim PropertyInfo | 68,442 parcels, zoning (2,909 polygons) and general plan land use (1,572) in one service | ArcGIS REST MapServer, free | https://gis.anaheim.net/map/rest/services/PropertyInfo/MapServer | VERIFIED (layers 0, 2, 3 counted) |
| Fullerton Parcels and HIOZ Sites | 35,825 parcels with general plan code, zoning class and values; also Housing Opportunity Overlay Zone sites and 8 "Opportunity Sites" | ArcGIS REST FeatureServer, free | https://services6.arcgis.com/yMM0eCpNU0fzBaIm/arcgis/rest/services/Fullerton_Parcels_and_HIOZ_Sites/FeatureServer | VERIFIED (layers + counts). Published under a Fullerton GIS account; not confirmed as the city's official service |
| City of Anaheim GIS hub | Anaheim open data portal | Web hub, free | https://data-anaheim.opendata.arcgis.com/ | VERIFIED (loads) |
| City of Irvine open data | Irvine layers | Web hub, free | https://data-cityofirvine.opendata.arcgis.com/ | UNVERIFIED (page is a JavaScript shell; no dataset contents confirmed) |
| City of Garden Grove open data | Garden Grove layers | Web hub, free | https://data-ggcity.opendata.arcgis.com/ | UNVERIFIED (JavaScript shell only) |

Gap: no verified official parcel or zoning endpoint for Costa Mesa, Garden Grove or Irvine. Use
the SCAG and county layers for those cities.

## 2. Zoning and general plan

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| SCAG Zoning_poly_OR | Zoning per parcel: `APN24`, `CITY`, `ZN24_CITY` (local code), `ZN24_SCAG` (regional category), `ACRES`, `SLOPE`. Best single zoning source across all 34 OC cities | ArcGIS REST MapServer, free; max 2,000 per request | https://maps.scag.ca.gov/scaggis/rest/services/LDX/Zoning_poly_OR/MapServer | VERIFIED (fields + sample Santa Ana records) |
| SCAG GeneralPlan_poly_OR | General plan land use per parcel | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/LDX/GeneralPlan_poly_OR/MapServer | VERIFIED (service and layer listed; fields not inspected) |
| SCAG Existinglanduse_poly_OR | Existing land use per parcel. Find vacant, parking, low-intensity uses | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/LDX/Existinglanduse_poly_OR/MapServer | VERIFIED (listed; fields not inspected) |
| SCAG SpecificPlan_poly_OR | Specific plan boundaries | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/LDX/SpecificPlan_poly_OR/MapServer | VERIFIED (listed) |
| SCAG REST services index (LDX) | Catalog of SCAG land-data layers | ArcGIS REST directory, free | https://maps.scag.ca.gov/scaggis/rest/services/LDX | VERIFIED |
| OC unincorporated Zoning_Boundaries | Zoning for unincorporated county land only (450 polygons: `ZONECLASS`, `CATEGORY`) | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/Zoning_Boundaries/MapServer/0 | VERIFIED |
| OC Zoning_2025 (OCLandInsights) | County zoning by APN with `ZCLASS`, `ZC_DESCR`, `ACRES` | ArcGIS REST MapServer, free | https://ocgis.com/survey/rest/services/OCLandInsights/Zoning_2025/MapServer | VERIFIED (fields listed; coverage and feature count not confirmed) |
| OC General_Plan | County general plan layer | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/General_Plan/MapServer | VERIFIED (service description matches) |
| Santa Ana Zoning Classifications | 3,192 zoning polygons: `ZONECLASS`, `ZONEDESC`, `ZONEOVERLAY`, ordinance number and date | ArcGIS REST FeatureServer, free | https://gis.santa-ana.org/server/rest/services/Public/PBA_ZoningClassifications/FeatureServer/0 | VERIFIED |
| Huntington Beach Zoning | 3,030 zoning polygons (`Base`, `ZoneType`, `Overlay`) | ArcGIS REST FeatureServer, free | https://services2.arcgis.com/KaS5yngHhCOBHXdC/arcgis/rest/services/Zoning/FeatureServer/0 | VERIFIED (counts and fields). Owner account is `HB_GIS`; not confirmed as the city's official account |

## 3. Housing-element site inventories

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| SCAG HousingElementSite_poly_scag | 189,627 adopted housing-element sites region-wide (2,126 in Orange County, `COUNTY='Orange'`) with `Assessor_Parcel_Number`, `Jurisdiction` and lower, moderate and above-moderate capacity | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/LDX/HousingElementSite_poly_scag/MapServer | VERIFIED (counts + sample records) |
| SCAG HousingElementRezone_poly_scag | Sites in housing elements that require rezoning | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/LDX/HousingElementRezone_poly_scag/MapServer | VERIFIED (listed; description matches; not queried) |
| HCD Housing Element Sites Inventory page | Official statewide inventory, submission template and instructions, link to HCD map app | Web + XLSX + PDF, free | https://hcd.ca.gov/housing-element/sites-inventory | VERIFIED |
| HCD Sites Inventory form template | Column schema every city used for its inventory | XLSX, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/sites-inventory-template.xlsx | VERIFIED (downloads as Excel; sheets not opened) |
| HCD Sites Inventory form instructions | Explains each field | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/sites-inventory-instructions-09152022.pdf | VERIFIED |
| HCD statewide sites inventory map app | Interactive statewide map of inventory sites | ArcGIS Experience app, free | https://experience.arcgis.com/experience/670e112e04ae415e9755f2d65fded76c/ | UNVERIFIED (JavaScript shell; content not rendered) |
| HCD Housing Element APR data | Permits, entitlements and completions by jurisdiction and year. Shows what actually got built | CSV via data.ca.gov, free | https://data.ca.gov/@california-department-of-housing-and-community-development/housing-element-annual-progress-report-apr-data-by-jurisdiction-and-year | VERIFIED (record lists CSV resources) |
| HCD Housing and Local Land Development Opportunity Map intro | Explains HCD's land-opportunity map for sites | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/introduction-to-the-housing-and-local-land-development-opportunity-map.pdf | VERIFIED |

## 4. Surplus and excess public land

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| HCD Surplus Land Act Notices of Availability (data.ca.gov) | 3,095 notices statewide with APN, address, city, lat/lon, gross acres, general plan and zoning, existing use, status and contact. About 160 rows match OC city names (rough text match, not an exact count). Last modified 2026-10-30 | CSV (+ DOCX data dictionary), free | https://data.ca.gov/dataset/surplus-land-act-notices-of-availability-received | VERIFIED (CSV downloaded and parsed). Some `Parcel Size` values are text like "9,005 SF". An older `lab.data.ca.gov` URL did not connect; use this one |
| HCD Notices of Availability map | Visual map of the same notices | Web map, free | https://hcd.ca.gov/housing-open-data-tools/notices-available-surplus-land-map | VERIFIED |
| HCD Surplus Land Act program page | Program overview, accessing land, standard vs exempt dispositions, violations | Web, free | https://www.hcd.ca.gov/planning-and-research/public-lands/surplus-land | VERIFIED |
| HCD Surplus Land Act Guidelines (2024, final) | The rules: surplus and exempt surplus land, affordable-housing requirements, notice process | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/final-updated-surplus-land-act-guidelines-2024.pdf | VERIFIED (title page read; read it yourself for the exact tests) |
| HCD Excess State Land (EO N-06-19) | State-owned excess sites screened from 44,000+ parcels (July 2024), map, developer interest portal, lease templates | Web + PDFs, free | https://www.hcd.ca.gov/planning-and-research/public-lands/excess-state | VERIFIED (page text confirms EO N-06-19, 44,000 parcels screened) |
| HCD State Excess Sites map | Interactive map of the screened sites | ArcGIS Experience app, free | https://experience.arcgis.com/experience/f9b1ccf48e864ac8af8014cbb89371b8/ | UNVERIFIED (JavaScript shell only) |
| DGS EO N-06-19 Affordable Housing Development page | DGS side of the excess-state-land program | Web, free | https://www.dgs.ca.gov/RESD/Projects/Page-Content/Projects-List-Folder/Executive-Order-N-06-19-Affordable-Housing-Development | VERIFIED (title matches) |
| Executive Order N-06-19 | The order itself | PDF, free | https://www.gov.ca.gov/wp-content/uploads/2019/01/EO-N-06-19.pdf | VERIFIED (loads; text not read) |
| OC County Property List (Oct 2025) | 783 county-owned or leased properties with address, status, square feet, owner | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/CEO_RealEstate/County_of_Orange_Property_List_OCT2025/MapServer/0 | VERIFIED (783 records) |
| OC School Districts boundaries | 25 school district polygons for matching district-owned surplus | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/School_Districts/MapServer/0 | VERIFIED |
| CDE California Public Schools 2025-26 | 9,946 school sites with district, status, open or closed date. Closed schools are surplus candidates | ArcGIS REST FeatureServer + CSV, free | https://services3.arcgis.com/fdvHcZVgB2QSRNkL/arcgis/rest/services/SchoolSites2526/FeatureServer/0 | VERIFIED (count + fields) |
| Caltrans GIS open data | Caltrans layers | ArcGIS Hub, free | https://gisdata-caltrans.opendata.arcgis.com/ | VERIFIED (loads), but no Caltrans excess-land layer was found. Treat as a gap |

Gaps: no verified machine-readable Caltrans excess parcel list, and no school-district surplus
inventory.

## 5. Faith and nonprofit-college land (SB 4)

There is no public "religious-owned parcel" layer. These are building blocks for a proxy. Owner
and tax-exempt fields live in the Assessor roll, which was not verified as a free download.

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| OpenStreetMap `amenity=place_of_worship` tag docs | Find worship sites with `religion=*` and `denomination=*`, and join to parcels spatially | Tag docs; data via Overpass or an extract, free (ODbL) | https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dplace_of_worship | VERIFIED (wiki page). A live Overpass query failed on 2026-11-06 (server at capacity, 502). Plan for an extract or a retry |
| IRS Exempt Organizations Business Master File | Nonprofits by name, address, NTEE code and subsection. Filter to religious orgs, match address to parcels | CSV download, free | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | VERIFIED (page loads; file not downloaded) |
| ProPublica Nonprofit Explorer API | Look up an org by name or EIN, with Form 990 summaries | JSON API, free | https://projects.propublica.org/nonprofits/api | VERIFIED (docs page loads; no calls made) |
| Terner Center: housing potential on faith-based and college land | Method and findings for sizing SB 4 land supply, and how parcels were identified | Web report, free | https://ternercenter.berkeley.edu/research-and-policy/faith-based-and-college-land-housing/ | VERIFIED (title matches) |
| Terner Center: mapping faith-based housing development | Barriers and mapping approach for faith-based sites | Web report, free | https://ternercenter.berkeley.edu/research-and-policy/faith-based-housing-development/ | VERIFIED (title matches) |

Gap: parcel owner and tax-exempt fields are not in the free OC parcel layer. Confirming ownership
needs the county Assessor roll or paid owner data. Label any proxy as a proxy.

## 6. Constraints: flood, fire, seismic, environment, transit, opportunity

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| FEMA NFHL (National Flood Hazard Layer) | Flood hazard zones (layer 28: `FLD_ZONE`, `SFHA_TF`, base flood elevation) | ArcGIS REST MapServer, free | https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer | VERIFIED (service and layer 28 fields). Slow: first call timed out, second worked |
| OC Floodplains (county) | Floodplain polygons (`FLD_ZONE`, depth). Fallback if FEMA is slow | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/Floodplains/MapServer/0 | VERIFIED (1,880 polygons) |
| SCAG ENV_Flood_Zones_PL_SCAG | Regional copy of FEMA flood zones | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/OpenData/ENV_Flood_Zones_PL_SCAG/MapServer | VERIFIED (description matches) |
| CAL FIRE Fire Hazard Severity Zones (statewide) | SRA, LRA and federal zones | ArcGIS REST MapServer, free | https://services.gis.ca.gov/arcgis/rest/services/Environment/Fire_Severity_Zones/MapServer | VERIFIED (layers: SRA 2007, LRA 2011, awaiting zoning, federal). Older zone vintages |
| OC Fire_Hazard_Severity_Zones_LRA | County copy for local responsibility areas | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/Fire_Hazard_Severity_Zones_LRA/MapServer/0 | VERIFIED (listed, query capability on) |
| CAL FIRE FHSZ LRA effective 2025 (CNRA hub) | Newest LRA map, download as CSV, SHP or GeoJSON | ArcGIS Hub, free | https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::fire-hazard-severity-zones-in-lra-effective-2025 | UNVERIFIED (JavaScript shell; download URL not extracted) |
| OC Liquefaction (CGS zones, county copy) | 229 quad-level liquefaction zone polygons | ArcGIS REST MapServer, free | https://www.ocgis.com/arcpub/rest/services/Map_Layers/Liquefaction/MapServer/0 | VERIFIED (229 features) |
| CGS Landslide Zones | 41,769 landslide zone polygons statewide | ArcGIS REST FeatureServer, free | https://services2.arcgis.com/zr3KAIbsRSUyARHG/arcgis/rest/services/CGS_Landslide_Zones/FeatureServer/0 | VERIFIED |
| CGS Seismic Hazards (EQ Zones of Required Investigation) | Official liquefaction and fault zones | Web app + REST | https://maps.conservation.ca.gov/cgs/EQZApp/ | UNVERIFIED (403 to automated fetch; the CGS REST liquefaction service returned "Token Required") |
| CalEnviroScreen 5.0 results | 9,106 census tract polygons with score and indicators. Pollution burden and disadvantaged-community status | ArcGIS REST + SHP/GDB, free | https://services1.arcgis.com/PCHfdHz4GlDNAhBb/arcgis/rest/services/calenviroscreen50results_F_070126_gdb/FeatureServer/2 | VERIFIED (count + fields). Source record on data.ca.gov updated 2026-10-28 |
| CalEnviroScreen 4.0 | Prior version, still used by many programs | SHP/GDB/XLSX, free | https://data.ca.gov/@california-office-of-environmental-health-hazard-assessment/calenviroscreen-4-0 | VERIFIED |
| Caltrans CA HQ Transit Areas (HQTA) | 21,039 high-quality transit area polygons statewide (`hqta_type`, `agency_primary`) | ArcGIS REST FeatureServer + CSV, free | https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/CA_HQ_Transit_Areas/FeatureServer/0 | VERIFIED |
| SCAG Major Transit Stops (2022) | Regional major transit stops | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/OpenData/Major_Transit_Stops_Plan_Year_2022/MapServer | VERIFIED (service listed; description + layer) |
| HCD Technical Advisory: AB 2097 (no minimum parking) | Parking prohibition near transit and its effect on yield | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/policy-and-research/ab-2097-ta.pdf | VERIFIED |
| OCTA GTFS feed | Bus routes, stops, schedules for frequency-based transit checks | GTFS zip, free | https://octa.net/current/google_transit.zip | VERIFIED (downloaded; 10 files; calendar dated 2026-08) |
| TCAC/HCD 2026 Opportunity Maps (adopted Dec 2025) | Resource category per tract (highest, high, moderate, low) for fair-housing scoring | SHP zip + XLSX, free | https://www.treasurer.ca.gov/ctcac/opportunity.asp | VERIFIED (page lists 2026 maps). Shapefile https://www.treasurer.ca.gov/sites/default/files/2025-11/shapefile.zip returned 200, application/zip, 5.2 MB; zip not opened |
| SCAG TCAC 2021 Opportunity Areas (REST) | Queryable older TCAC layer. Use only if the 2026 shapefile is too heavy | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/HousingElements/TCAC_2021_Opportunity_Areas/MapServer | VERIFIED (listed; one layer) |
| Berkeley 2026 CTCAC/HCD AFFH mapping tool | Web viewer for the 2026 opportunity maps | Web, free | https://belonging.berkeley.edu/2026-ctcachcd-affh-mapping-tool | UNVERIFIED (page returned 719 bytes, a shell) |
| SCAG Absolute and Variable constraint areas | Regional environmental constraint layers used for housing-element capacity | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/HousingElements/Absolute_and_Variable_constraint_areas/MapServer | VERIFIED (listed in directory; not queried) |

## 7. Statute text and HCD guidance

HCD publishes fact sheets for most of these laws in one combined PDF (71 pages, April 2026
versions). The legislature's own site (leginfo) returned 403 to automated fetch on every bill and
code URL tried, but a normal browser will likely work. HCD fact sheets and CalMatters pages are
the usable fallback.

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| HCD Housing Law Fact Sheets, combined | One document covering ADU (including SB 684 / SB 1123 cites, Gov Code 65852.28, 66499.41), AB 2011, SB 4, SB 6, AB 2243, SB 9 and more | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/housing-law-fact-sheets.pdf | VERIFIED (text searched for each law) |
| HCD fact sheet: Duplexes and Lot Splits (SB 9) | Eligibility rules, Gov Code 65852.21 and 66411.7 | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/lot-splits-and-duplexes-sb-9.pdf | VERIFIED (page 1 read) |
| HCD SB 9 Fact Sheet (Implementation) | Longer implementation guidance | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/sb-9-fact-sheet.pdf | VERIFIED (title page read) |
| HCD fact sheet: Faith and Higher Ed Lands (SB 4) | By-right approval, Gov Code 65913.16, effective July 2, 2024 through Jan 1, 2036 | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/aff-hsg-faith-higher-ed-sb-4.pdf | VERIFIED (page 1 read) |
| HCD memos index | Housing element memos, SB 35 guidelines, site inventory memo | Web, free | https://www.hcd.ca.gov/planning-and-research/hcd-memos | VERIFIED |
| CalMatters Digital Democracy: SB 4 (2023) | Bill text, history, analyses | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_202320240sb4 | VERIFIED (title matches) |
| CalMatters Digital Democracy: SB 9 (2021) | Bill text and analyses | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_202120220sb9 | VERIFIED (HTTP 200; title not extracted) |
| CalMatters Digital Democracy: SB 684 (2023) | Small-lot (10-unit) streamlined subdivision bill | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_202320240sb684 | VERIFIED (HTTP 200; title not extracted) |
| CalMatters Digital Democracy: SB 1123 (2023) | Companion to SB 684 | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_202320240sb1123 | VERIFIED (HTTP 200; title not extracted) |
| CalMatters Digital Democracy: AB 2011 (2021) | Affordable housing on commercial corridors | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_201920200ab2011 | VERIFIED (HTTP 200; title not extracted) |
| CalMatters Digital Democracy: SB 6 (2021) | Middle Class Housing Act | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_202120220sb6 | VERIFIED (HTTP 200; title not extracted) |
| CalMatters Digital Democracy: AB 2243 (2021) | Builds on AB 2011 and SB 6 | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_202120220ab2243 | VERIFIED (HTTP 200; title not extracted) |
| CalMatters Digital Democracy: AB 2097 (2021) | Parking prohibition bill | Web, free | https://calmatters.digitaldemocracy.org/bills/ca_202120220ab2097 | VERIFIED (HTTP 200; title not extracted) |
| leginfo.legislature.ca.gov | Authoritative statute text, for example Gov Code 65852.21, 66411.7, 65913.16, 54221 | Web, free | https://leginfo.legislature.ca.gov/ | UNVERIFIED (HTTP 403 to automated fetch; a browser will likely work) |

Gap: the Surplus Land Act statute (Gov Code 54220 and following) is covered here only through the
HCD guidelines PDF in section 4. No direct statute text was verified.

## 8. Existing tools and research to learn from

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Terner Center: Duplexes and lot splits (SB 9) analysis | Method for estimating how many parcels can use SB 9, and why most do not | Web report, free | https://ternercenter.berkeley.edu/research-and-policy/duplexes-lot-split-sb-9/ | VERIFIED (title matches) |
| Terner Center: SB 9 Turns One | First-year application data and insights | Web report, free | https://ternercenter.berkeley.edu/research-and-policy/sb-9-turns-one-applications/ | VERIFIED |
| Terner Center: Mapping Oakland's Vacant Parcels | Example of a parcel-screening method | Web report, free | https://ternercenter.berkeley.edu/research-and-policy/mapping-oaklands-vacant-parcels/ | VERIFIED |
| Regrid Parcel API (commercial) | Nationwide parcels with owner, zoning, building data | REST API. 30-day free sandbox, then paid | https://regrid.com/api | VERIFIED (page loads; "Free for 30 days" text found; pricing and OC coverage not checked) |
| Zoneomics (commercial) | Zoning lookups and land-use data via API | Web + API, paid (free tier not confirmed) | https://www.zoneomics.com/ | VERIFIED (loads; pricing not checked) |
| UrbanFootprint (commercial) | Planning and land analysis platform | Paid platform | https://urbanfootprint.com/ | VERIFIED (loads; capabilities not tested) |

## 9. Census, geocoding, building footprints

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Census ACS 5-year API (2023) | Income, rent burden, tenure, household size by tract or block group | JSON API, free (key recommended) | https://api.census.gov/data/2023/acs/acs5.html | VERIFIED (loads; variables list also loads) |
| Census ACS 5-year dataset overview | Docs for ACS tables and API | Web, free | https://www.census.gov/data/developers/data-sets/acs-5year.html | VERIFIED |
| Census Geocoder | Address to lat/lon plus tract. Free batch geocoding | Web + REST, free | https://geocoding.geo.census.gov/geocoder/ | VERIFIED (loads; no geocode run) |
| Census TIGER 2024 tracts | Tract boundary shapefiles to join with ACS | SHP download directory, free | https://www2.census.gov/geo/tiger/TIGER2024/TRACT/ | VERIFIED (directory loads) |
| Microsoft US Building Footprints | Building polygons (US) | GeoJSON, free (ODbL) | https://github.com/microsoft/USBuildingFootprints | VERIFIED (repo loads; license not read) |
| Microsoft Global ML Building Footprints | Newer worldwide footprints, about 1% false positive rate per its README | GeoJSONL gz, free | https://github.com/microsoft/GlobalMLBuildingFootprints | VERIFIED (README text read) |
| SCAG Tract_boundary_SCAG | Tract polygons on the same server as the land-use layers | ArcGIS REST MapServer, free | https://maps.scag.ca.gov/scaggis/rest/services/LDX/Tract_boundary_SCAG/MapServer | VERIFIED (listed) |

## Biggest gaps

1. Owner and tax-exempt status per parcel (needed for SB 4) is not in any free verified layer.
   Only proxies: worship sites and the IRS exempt-organizations file.
2. No verified official parcel or zoning API for Costa Mesa, Garden Grove or Irvine. SCAG
   Zoning_poly_OR covers them at parcel level.
3. Official statute text (leginfo) blocks automated fetch. HCD fact sheets and CalMatters pages
   are the usable references.
