# Data sources for Lane 2: Clear it

Starting points for state law text, HCD guidance, permit and progress-report data, Orange County
city pages and factory-built housing. Compiled November 6, 2026.

**These are a few places to start.** There's much more out there, and the best teams find sources
nobody else used.

**Status key.** VERIFIED means fetched and the content confirmed. VERIFIED-EXA means a plain
fetch was blocked (403), so the content was confirmed through a different fetch tool. It opens
fine in a normal browser. UNVERIFIED means it could not be confirmed, with the reason given.
Anything UNVERIFIED is a lead, not a fact. Be kind to city servers: several block automated
requests, and the event rule is not to scrape at a volume that gets a site to block us.

## Read this first: statute numbers changed

- **ADU law is no longer Gov Code 65852.2.** SB 477 (March 2024) renumbered it to **Gov Code 66310
  to 66342**. ADU approvals are 66314 to 66331. JADU is 66333. Confirmed on leginfo and in HCD's
  March 2026 ADU Handbook. Old section numbers 65852.2, .22, .23 and .26 still appear in older
  city documents and HCD letters.
- 2025 changes: Gov Code 66324, 66327 and 66332 became 66311.5, 66313.5 and 66311.7. 66333.5 was
  added (per the Handbook, page 13).
- **SB 684 is Gov Code 66499.41** (ministerial map for 10 or fewer parcels). The companion
  building-permit rule is **65913.4.5**. SB 1123 amended these. Confirm the exact text before you
  build rules on it.
- Gov Code 65852.28 has four versions on leginfo. It was not read in detail. Do not hard-code it
  without checking.
- AB 2234 post-entitlement permit timelines are **Gov Code 65913.3**. Checklists and sample
  approved applications must be online. It applies to ADU, duplex, multifamily, mixed use and
  townhome.
- HCD has direct enforcement authority over 65852.21 and 66411.7 (SB 9) since January 1, 2024
  (AB 434).
- Leginfo blocks plain automated fetches, so the statute rows below are VERIFIED-EXA. Bulk raw
  text is at downloads.leginfo.legislature.ca.gov.

## What is hard today

Every item below comes from a page that was read, unless marked not sourced.

- Every city publishes its own checklist and fees. Separate, differently structured pages exist
  for Irvine, Santa Ana, Anaheim, Costa Mesa, Fullerton, Huntington Beach, Garden Grove, Orange
  and Tustin. Fee detail sits in separate PDFs.
- Old statute numbers are still in live city documents. Anaheim's November 2025 checklist still
  cites Gov Code 65852.2 and 65852.22 for the JADU covenant.
- Local rules get ahead of, or behind, state law. Terner found 7 of 10 sampled cities set SB 9
  objective standards stricter than for ADUs or single-family homes.
- A city can simply stop processing. HCD says Huntington Beach voted in February 2023 to stop
  accepting ADU and SB 9 applications. The state sued March 8 and the council resumed processing
  March 21.
- No open permit data in OC. No Socrata or ArcGIS building-permit dataset was found for any OC
  city. Cities use their own submittal portals: IrvineReady, GG Ready, TESSA (Costa Mesa), EasyDev
  (Fullerton), Civic Portal (Orange), Citizen Self Service Portal (Tustin), AnaheimNext.
- City sites block automated fetching. Anaheim, Costa Mesa, Fullerton and Orange returned 403 to a
  plain fetch.
- HCD's enforcement letters are only an embedded dashboard. Some letters say "contact HCD for a
  copy".
- Some programs are paper or staff-mediated. Santa Ana pre-approved ADUs are over-the-counter with
  paper copies only.
- Sign-offs sit outside the planning clock. Anaheim's checklist lists sewer capacity verification
  "up to four days" and a meter spot inspection within "two to three business days". Pre-approved
  plans still need site-specific review.
- Pre-approved plans can expire. Costa Mesa says approved plans must be resubmitted after each
  triennial building code update.
- Plan-check rounds, hidden discretionary steps and AB 2234 timeline misses: not sourced. No data
  on correction cycles was found. Nobody has audited any OC city against AB 2234. That is an open
  task a team could do.

## 1. State law text (leginfo)

All are `codes_displaySection.xhtml?lawCode=GOV&sectionNum=N` pages.

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Gov 66314 (ADU approvals, ministerial, 60 days) | Core ADU rule engine. Replaces 65852.2 | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66314 | VERIFIED-EXA |
| Gov 66411.7 (SB 9 urban lot split) | Lot-split eligibility and 60-day clock | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66411.7 | VERIFIED-EXA |
| Gov 65852.21 (SB 9 two-unit development) | Two-unit ministerial approval | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=65852.21 | VERIFIED-EXA |
| Gov 66499.41 (SB 684 / SB 1123 small subdivision, 10 or fewer parcels) | Ministerial parcel, tentative and final map path | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66499.41 | VERIFIED-EXA |
| Gov 65913.4.5 (building permit for 10-or-fewer-unit lots being subdivided) | Rule to get a permit before the final map | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=65913.4.5 | VERIFIED-EXA |
| Gov 65913.4 (SB 35 / SB 423 streamlined ministerial approval) | Multifamily by-right path and eligibility tests | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=65913.4 | VERIFIED-EXA |
| Gov 65912.101 (AB 2011 / SB 6 definitions; chapter 65912.100 to .140) | Commercial-corridor and office-to-housing by-right | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=65912.101 | VERIFIED-EXA |
| Gov 65950 (Permit Streamlining Act, decision deadlines) | Deadlines by project type. Deemed-approved logic | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=65950 | VERIFIED-EXA |
| Gov 65913.3 (AB 2234 post-entitlement permits) | Required online checklists and example applications. Permit-phase timelines. Basis for a "does this city's checklist match" checker | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=65913.3 | VERIFIED-EXA |
| Gov 65589.5 (Housing Accountability Act) | Grounds a city can and cannot use to deny or downsize a project | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=65589.5 | VERIFIED-EXA |
| Gov 66427.1 (condo conversion findings, tenant notices) | Steps and notice periods for apartment-to-condo conversions | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66427.1 | VERIFIED-EXA |
| Gov 66000 (Mitigation Fee Act definitions; chapter 66000 to 66008) | Which fees are impact fees and must be justified. Fee-checker logic | HTML, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66000 | VERIFIED-EXA |
| Leginfo bulk downloads | Machine-readable full code text for a rules database. Avoids scraping | Zip of .dat/.lob files, free | https://downloads.leginfo.legislature.ca.gov/ | VERIFIED (HEAD only: 200; pubinfo_Mon.zip returns application/zip; contents not opened) |
| Leginfo bill text pages for SB 684 and SB 1123 | Original bill text | HTML | `billTextClient.xhtml?bill_id=202320240SB684` and `...202520260SB1123` | UNVERIFIED (blocked, not fetched). Use the section pages above instead |
| OPR/LCI Permit Streamlining Act guide | Plain-English guide | PDF | https://lci.ca.gov/docs/20230801-Permit_Streamlining_Act.pdf | UNVERIFIED (URL redirects in a loop). Do not rely on it |

## 2. HCD guidance and enforcement

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| HCD ADU Handbook (March 2026, English) | ADU and JADU rules with section cites under the new numbering. FAQ. Changes 2022 to 2026 | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/policy-and-research/adu-handbook-update.pdf | VERIFIED (cover reads "March 2026") |
| HCD ADU Handbook page (also ES, VI, ZH translations) | Landing page and translated PDFs | HTML + PDFs | https://www.hcd.ca.gov/building-standards/adu/handbook | VERIFIED |
| HCD ADU main page | Entry to the ADU Portal, technical assistance letters, ordinance submission | HTML | https://www.hcd.ca.gov/building-standards/adu | VERIFIED |
| HCD ADU Ordinances | Which cities have had ordinance findings letters | HTML | https://www.hcd.ca.gov/building-standards/adu/ordinance | VERIFIED (title confirmed; letter list not parsed) |
| HCD ADU additional resources | Partner guides, city programs | HTML | https://www.hcd.ca.gov/building-standards/adu/resources | VERIFIED |
| HCD SB 9 Fact Sheet | Eligibility, lot-split rules, 60-day clock, HCD enforcement from 2024 | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/sb-9-fact-sheet.pdf | VERIFIED. An older `sb9factsheet.pdf` link in 2023 letters is now 404 |
| HCD Housing Law Fact Sheet: Duplexes and Lot Splits (SB 9) | Short version. Review timeline, 30-day completeness check, 3-year owner affidavit | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/lot-splits-and-duplexes-sb-9.pdf | VERIFIED |
| HCD SB 35 guidelines (updated, Gov 65913.4) | Step-by-step eligibility checklist for streamlined ministerial approval | PDF, free | https://www.hcd.ca.gov/policy-research/docs/SB-35-Guidelines-Update-Final.pdf | VERIFIED |
| HCD AB 2011 draft guidelines (65912.100 to .140) | Rule set for corridor and office-to-housing by-right | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/draft-ab-2011-guidelines.pdf | VERIFIED (labelled Draft on the cover) |
| HCD SMAP determination methodology | Which jurisdictions are subject to streamlining | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/smap-determination-methodology.pdf | VERIFIED (loads as PDF; contents only skimmed) |
| HCD SMAP dashboard (SB 35 / SB 423 status by jurisdiction) | Per-city "is streamlining available here" lookup | HTML dashboard | https://www.hcd.ca.gov/planning-and-community-development/streamlined-ministerial-approval-process-dashboard | VERIFIED (page loads; underlying data export not checked) |
| HCD Statutory Determinations, Guidelines, Technical Resources | Index of guidelines and determinations | HTML | https://www.hcd.ca.gov/planning-and-community-development/statutory-determinations | VERIFIED |
| HCD Accountability and Enforcement (HAU home) | Explains the Housing Accountability Unit, links to the letters dashboard and portal | HTML | https://www.hcd.ca.gov/planning-and-community-development/accountability-and-enforcement | VERIFIED |
| HCD Technical Assistance and Enforcement Letters Dashboard | The list page for HAU notices of violation, technical assistance letters and ordinance findings. Filter by jurisdiction, law and statute cite | HTML dashboard with PDF letters | https://www.hcd.ca.gov/hau/enforcement-letters | VERIFIED (data dictionary read). The dashboard is an embedded app, so scraping needs browser automation. Contact HAUportal@hcd.ca.gov for copies |
| HCD Housing Accountability Dashboard | Counts of HAU cases and outcomes | HTML dashboard | https://www.hcd.ca.gov/housing-open-data-tools/housing-accountability-dashboard | VERIFIED |
| HCD Huntington Beach notice of potential violation on ADU permit freeze | Worked example of a violation letter with statute cites | PDF | https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/HAU/HuntingtonBeachNOPV-ADU-022123.pdf | VERIFIED. Cites the old 65852.2 numbering. The letter date line reads 2022 but the body refers to a February 21, 2023 council item |
| HCD memos index | Policy memos | HTML | https://www.hcd.ca.gov/planning-and-research/hcd-memos | VERIFIED |
| HCD Housing Law Fact Sheets, 2026 combined | 22 fact sheets in one file | PDF | https://www.hcd.ca.gov/sites/default/files/docs/policy-and-research/housing-law-fact-sheets-2026-combined.pdf | UNVERIFIED (returns 404). Use the individual sheets above |

## 3. Annual Progress Report and RHNA data (machine-readable)

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| data.ca.gov: Housing Element APR Data by Jurisdiction and Year | Parcel-level permit pipeline. Modified 2026-10-30 | CSV + CKAN datastore API, free, no key | https://data.ca.gov/dataset/housing-element-annual-progress-report-apr-data-by-jurisdiction-and-year | VERIFIED (API call returned data) |
| APR Table A (applications submitted, approved or disapproved, SB 35 flag) | Per-application submit date and outcome. Raw material for real approval-time benchmarks. 358,215 rows | CSV / API `resource_id=c78b769d-cc02-4050-91ef-79ded665b5a8` | https://data.ca.gov/api/3/action/datastore_search?resource_id=c78b769d-cc02-4050-91ef-79ded665b5a8&q=IRVINE | VERIFIED (Irvine query returned 274 rows with APN, submit date, status) |
| APR Table A2 (entitlements, building permits, certificates of occupancy) | Dates for entitlement, permit issue and CO per project. `UNIT_CAT` includes ADU. Compute entitlement-to-permit-to-CO lags by city. 927,006 rows | CSV / API `resource_id=fe505d9b-8c36-42ba-ba30-08bc4f34e022` | https://data.ca.gov/api/3/action/datastore_search?resource_id=fe505d9b-8c36-42ba-ba30-08bc4f34e022&limit=5 | VERIFIED (schema returned: ENT_APPROVE_DT1, BP_ISSUE_DT1, CO_ISSUE_DT1, etc.) |
| data.ca.gov: RHNA Progress Report (5th and 6th cycle) | RHNA progress by jurisdiction | CSV, free | https://data.ca.gov/dataset/rhna-progress-report | VERIFIED (4 resources listed via API) |
| HCD APR Data Dashboard and Downloads | HCD's own viewer and download page | HTML dashboard | https://www.hcd.ca.gov/housing-open-data-tools/apr-dashboard | VERIFIED |
| HCD Annual Progress Reports landing | Submission context | HTML | https://www.hcd.ca.gov/apr | VERIFIED |
| HCD RHNA Progress dashboard page | 6th-cycle progress by jurisdiction | HTML | https://www.hcd.ca.gov/planning-and-community-development/housing-open-data-tools/regional-housing-needs-allocation-progress | VERIFIED |
| HCD Housing Open Data Tools index | Index of all dashboards | HTML | https://www.hcd.ca.gov/planning-and-community-development/housing-open-data-tools | VERIFIED |
| BackyardADU.net permits_ca.csv (third party) | ADU permits per city per year 2013 to 2025, derived from APR Table A2 and a legacy dataset | CSV, free, CC0 for the merged file | https://backyardadu.net/data/permits_ca.csv | VERIFIED (header and rows fetched). Third party: cite the APR for anything official |
| BackyardADU.net build_times.csv (third party) | Median days from building permit to CO for ADUs, by jurisdiction. Example rows: City of Orange median 263 days, Orange County unincorporated 328 | CSV, free | https://backyardadu.net/data/build_times.csv | VERIFIED (rows fetched). Permit-to-CO only, not application-to-permit |

## 4. Orange County city resources

Anaheim, Costa Mesa, Fullerton and Orange block plain fetches (403), so their content was
confirmed through another tool.

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Irvine: Project: Constructing an ADU | Submittal list (ADU Verification Form, covenant, hold harmless, school fee form, TCA form), IrvineReady portal steps, about a 2-business-day completeness check | HTML | https://cityofirvine.gov/building-permits-and-inspections/project-constructing-accessory-dwelling-unit-adu | VERIFIED |
| Irvine: Pre-Approved ADU Plans Program (AB 1332) | Plan vendors list. Site-specific review still required | HTML | https://cityofirvine.gov/building-permits-and-inspections/pre-approved-adu-plans-program | VERIFIED |
| Irvine: Fee Schedule | Fee structure. ADU planning review is hourly ($210.70/hr, $1,500 deposit in the fee PDF). Fees rose Aug 15, 2025 | HTML + PDFs | https://www.cityofirvine.gov/community-development/fee-schedule | VERIFIED |
| Santa Ana: Pre-Approved ADU Plans (10 plans, ZIP downloads) | Plan catalog and eligibility screens (not flood zone A/AE, not in listed historic districts) | HTML + ZIP | https://santa-ana.gov/pre-approved-adu-plans/ | VERIFIED |
| Santa Ana: Pre-Approved ADU Plan Submittal Process | Five-step process. Over-the-counter, paper only. "As little as one day" | HTML | https://santa-ana.gov/pre-approved-adu-plan-submittal-process/ | VERIFIED |
| Anaheim: ADU Anaheim | Three tracks including ADU Express (1 to 3 day review) | HTML | https://www.anaheim.net/6349/ADU-Anaheim | VERIFIED-EXA |
| Anaheim: Pre-Approved Plan Catalogue | 4 free plans, 224 to 1,199 sf | HTML | https://www.anaheim.net/6351/Pre-Approved-Plan-Catalogue | VERIFIED-EXA |
| Anaheim: ADU Submittal Requirements Checklist (Nov 2025) | A real city checklist to test against state law (sewer verification, meter spot, new address, JADU covenant). Still cites old 65852.2 and .22 numbers | PDF | https://www.anaheim.net/DocumentCenter/View/35053/Accessory-Dwelling-Unit-Submittal-Requirements-Checklist | VERIFIED-EXA |
| Costa Mesa: ADU page | Local deltas (150 sf minimum, optional parking, objective standards) | HTML | https://www.costamesaca.gov/government/departments-and-divisions/economic-and-development-services/planning/accessory-dwelling-units-adu | VERIFIED-EXA |
| Costa Mesa: Pre-Engineered ADUs and Safe ADU Legalization Program | Pre-approval program via TESSA. Plans listed as "coming soon" in the page text seen (may be stale). AB 2533 unpermitted-ADU path | HTML | https://www.costamesaca.gov/government/departments-and-divisions/economic-and-development-services/planning/accessory-dwelling-units-adu/pre-engineered-adus | VERIFIED-EXA |
| Fullerton: ADU page (Ordinance 3343, June 17, 2025) | Current ordinance link | HTML | https://www.cityoffullerton.com/government/departments/community-and-economic-development/planning-zoning/zoning/accessory-dwelling-units-granny-units | VERIFIED-EXA |
| Fullerton: Building information bulletins | ADU guidelines, AB 2533 process guide and checklist | HTML + PDFs | https://www.cityoffullerton.com/government/departments/community-and-economic-development/building-and-safety/information-bulletins | VERIFIED-EXA |
| Huntington Beach: ADU page | Ministerial review statement. Coastal zone may need a Coastal Development Permit | HTML | https://www.huntingtonbeachca.gov/departments/community_development/planning_zoning/accessory_dwelling_units_%28adus%29.php | VERIFIED |
| HCD press release: state sues Huntington Beach | Timeline: city stopped ADU and SB 9 applications Feb 2023, state sued Mar 8, council resumed Mar 21, state later added a housing-element claim | HTML | https://www.hcd.ca.gov/about-hcd/newsroom/california-sues-huntington-beach-violating-state-housing-element-law | VERIFIED |
| State's preliminary-injunction brief (Huntington Beach) | Primary source filed in the case | PDF | https://oag.ca.gov/system/files/attachments/press-docs/Filed%20Memorandum%20of%20Points%20and%20Authorities%20in%20Support%20of%20Motion%20for%20a%20Preliminary%20Injunction.pdf | VERIFIED (loads as PDF; excerpt read through search) |
| Garden Grove: ADU Go | Pre-approved program, 4 free city plans. Applications via GG Ready | HTML | https://ggcity.org/adu-go | VERIFIED |
| Garden Grove: ADU main page | Process walkthrough | HTML | https://ggcity.org/adu | VERIFIED |
| City of Orange: Planning Division | ADU and JADU application via Civic Portal | HTML | https://www.cityoforange.org/business/planning-division | VERIFIED-EXA |
| Tustin: Accessory Dwelling Units | Definitions, Ordinance 1517 (Dec 2021, may predate the 2024-25 changes). City handbook "coming soon" | HTML | https://www.tustinca.org/1378/Accessory-Dwelling-Units | VERIFIED |
| Civic Data Works: Santa Ana preapproved plans catalog (third party) | Cross-city plan catalog. Notes any city can adopt another agency's preapproved plans under Gov 65852.27(a)(5) | HTML | https://landinventory.civicdataworks.com/plans-catalog/santa-ana-ca/ | VERIFIED (page loads). Its claims about 65852.27 are the site's own, not independently checked |
| SoCal ADU Tracker, Huntington Beach page (third party) | A possible existing tool to benchmark: per-city ADU rules and "state law check" notes | HTML | https://socaladutracker.com/adu-permits/huntington-beach | VERIFIED (loads; accuracy not audited) |

Not found: Fullerton, Garden Grove, Anaheim and Santa Ana fee schedule PDFs were not separately
fetched. Only Irvine's fee page was. Huntington Beach's pre-approved plan program was not checked.

## 5. Permit data (OC)

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| County of Orange Open Data (GIS hub) | County GIS layers for address lookup | ArcGIS Hub, shapefile, GeoJSON, CSV, free | https://data-orangecountygis.hub.arcgis.com/ | VERIFIED (loads; individual layers not enumerated). Layers, not permits |
| OC Public Works permit table (Geocortex REST) | Fields: PermitType, WorkClass, PermitStatus, ApplicationDate, IssueDate, FinaledDate | Geocortex REST table, free | https://maps.orcity.org/Geocortex/Essentials/REST/sites/OCWebMaps/map/mapservices/79/tables/5 | UNVERIFIED (seen in search results only). The host is orcity.org, which is the City of Orange, not the County. Confirm the owner before relying on it |
| U.S. Census Building Permits Survey | Monthly residential permit counts by place (no addresses) | CSV/Excel, free | https://www.census.gov/construction/bps/ | VERIFIED |
| Buildstats Orange County permits | Permit records since 1988 with application, issue and completion dates | Paid | https://buildstats.com/data/california/orange-county | UNVERIFIED (not fetched; claims from a search snippet only). Treat as a paid fallback |

No OC city with an open Socrata or ArcGIS building-permit dataset was found. The APR tables in
section 3 are the practical free substitute.

## 6. Research and trackers

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Terner Center: SB 9 Turns One (Jan 2023) | SB 9 application counts in 13 cities | HTML, free | https://ternercenter.berkeley.edu/research-and-policy/sb-9-turns-one-applications/ | VERIFIED |
| Terner Center: State Law, Local Interpretation (SB 9 ordinances, June 2022) | How local objective standards undercut SB 9. 7 of 10 cities stricter than for ADUs | HTML | https://ternercenter.berkeley.edu/research-and-policy/state-law-local-interpretation-senate-bill-9/ | VERIFIED |
| Terner Center: Will Duplexes and Lot Splits Create New Homes (2021) | Jurisdiction-level SB 9 eligibility and feasibility file (cities with 5,000+ single-family parcels) | HTML + downloadable results file | https://ternercenter.berkeley.edu/research-and-policy/duplexes-lot-split-sb-9/ | VERIFIED (page loads; results file link not tested) |
| Terner Center: Measuring the Permitting Process in San Francisco | Method for measuring permit timelines | HTML | https://ternercenter.berkeley.edu/research-and-policy/measuring-the-housing-permitting-process-in-san-francisco/ | VERIFIED (San Francisco only, not OC) |
| Terner Center research index | Find newer ADU and permitting work | HTML | https://ternercenter.berkeley.edu/research-and-policy/ | VERIFIED |
| YIMBY Law SB 9 implementation tracker | Table of cities' SB 9 ordinances and violations | HTML table, free | https://www.yimbylaw.org/sb9 | VERIFIED |
| California YIMBY: SB 9 (2025) page | A 2025 law letting HCD void non-compliant local ADU ordinances (signed Oct 10, 2025). Note: this is a different bill from the 2021 SB 9 | HTML | https://cayimby.org/legislation/2025-sb-9/ | VERIFIED |
| Casita Coalition: Guidebooks and Resources | Pre-approved ADU plans guidebook, ADU Best Practices Guide, SB 9 and multifamily-ADU guides | HTML + PDFs, free | https://www.casitacoalition.org/guidebooks-and-resources | VERIFIED |
| eScholarship: Factors Affecting Approval Process in Transit-Accessible Areas of Southern California | Survey-based approval-time evidence | PDF | https://escholarship.org/content/qt2x39p8ds/qt2x39p8ds.pdf | UNVERIFIED (seen in search results only) |

## 7. Factory-built and modular

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| HCD Factory-Built Housing program | State oversight of factory-built housing. Gateway to laws, inspections, insignia, third-party agencies | HTML | https://www.hcd.ca.gov/building-standards/fbh | VERIFIED |
| HCD FBH Laws and Regulations | Statutory basis (state approval vs local permits) | HTML | https://www.hcd.ca.gov/building-standards/fbh/laws-and-regulations | VERIFIED |
| HCD FBH Third-Party Agencies | Which agencies can review and inspect modular plans | HTML | https://www.hcd.ca.gov/building-standards/fbh/third-party-agencies | VERIFIED |
| HCD FBH Insignia | Insignia of approval for factory-built units | HTML | https://www.hcd.ca.gov/building-standards/fbh/insignia | VERIFIED |
| HCD FBH forms (for example HCD FBH 314) | Application forms | PDF | https://www.hcd.ca.gov/building-standards/manufactured-modular-factory-built/factory-built-housing/docs/hcdfbh314.pdf | UNVERIFIED (linked from the FBH page but not fetched) |

No statewide list of state-approved ADU plans was found. Anaheim's FAQ notes no prefab or modular
plans in its catalogue yet.

## Gaps to know about

- No OC open permit dataset with application dates. Use APR Table A and A2 for benchmark
  timelines, and city portals for single-address lookups.
- HCD's letters dashboard is an embedded app, not a CSV. Plan for browser automation or manual
  sampling, within the data rule.
- Several city pages still cite 65852.2. A checker that compares city text to state law should map
  old numbers to new (65852.2 to 66310 through 66342).
- Tustin's ADU page cites a December 2021 ordinance, and Costa Mesa's page says pre-approved plans
  were coming in early 2025. Both look stale and were not confirmed against current ordinances.
