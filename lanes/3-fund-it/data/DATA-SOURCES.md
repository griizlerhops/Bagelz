# Data sources for Lane 3: Fund it

Starting points for income limits, rates and costs, market prices, funding programs, land trusts
and donor sources. Checked November 6, 2026.

**These are a few places to start.** There's much more out there, and the best teams find sources
nobody else used.

**Status key.** VERIFIED means fetched and loaded, and the content matches the claim. UNVERIFIED
means it could not be confirmed, with the reason given. Anything UNVERIFIED is a lead, not a fact.
Some sites block automated fetches (403). Those opened through another tool and should open in a
normal browser. No dollar figure below was taken from anywhere but a page that was seen. Terms
change, so read the source before you build on it.

**Labels.** [READ] means seen on a fetched page. [INFERRED] means a hypothesis about how
practitioners work, not stated by a source. Test [INFERRED] items with a practitioner in your lane
room.

## What is hard today

- **Income limits are revised mid-year and differ by program.** The HCD 2026 State Income Limits
  memo is a revision dated June 23, 2026 that replaces the May 29, 2026 version. The State HOME
  table is a separate PDF effective June 1, 2026. A model hard-coded in May is already stale.
  [READ]
- **Rules sit in PDFs and statute text, not data.** HCD limits are PDFs, the cost cap is statute,
  and HUD limits and Fair Market Rent need an account and API token. No single machine-readable
  table of program, maximum assistance, income cap and term was found. [READ]
- **Definitions differ by source and date.** Health and Safety Code 50052.5 has separate rules for
  housing assisted before and on or after January 1, 1991. 50053 is a separate rental definition.
  Mixing rental and ownership logic, or old and new assistance, would produce the wrong cap. The
  full percentage tables were not read. [READ the start of each statute]
- **Program terms are hard to pin down.** The CalHFA MyHome page says up to 3.5% (FHA) or 3%
  (conventional). The Dream For All page says up to 20%, not to exceed $150,000, with voucher
  registration and a randomized drawing. Search results (not read at the source) say Dream For
  All ran out of money in 2023, and a 2022 CalHFA board handout described Forgivable Equity
  Builder as winding down. Program lists go stale. [READ the program pages]
- **Local programs are opaque.** Santa Ana and Garden Grove have pages. Programs for Anaheim,
  Costa Mesa and Fullerton could not be confirmed (their sites returned 403, and one Anaheim URL
  was an unrelated plan page). [READ]
- **Cost data is paid or old.** RSMeans is a paid subscription. The free Terner hard-cost paper
  is dated March 2020. Teams must inflate old numbers or state an assumption. [READ]
- **Rate sensitivity.** The Freddie Mac 30-year rate was 7.18% on 2026-11-05 against 7.40% on
  2026-10-08, a 0.22-point move in a month. With a price capped by income, a rate move changes the
  gap directly (that last part is arithmetic, not a sourced claim). [READ FRED]
- **The market is far from the cap.** The C.A.R. traditional affordability table's Orange row
  appears to show a $1,470,000 median price and $374,400 minimum qualifying income. The column
  meaning was inferred from the row, and the period was not noted. Check it on the page. [READ,
  with that caveat]
- **SHOP funds** land and infrastructure for sweat-equity builders rather than whole-home costs,
  which limits what a dollar can pay for. [READ]
- Funding rounds out of sync with closing, layered compliance and long resale restrictions:
  [INFERRED]. HOSN, CalHome and AHP are periodic or competitive programs, but round dates and
  compliance terms were not read.
- Pro formas as one-off spreadsheets and no shared program database: [INFERRED]. No public shared
  database or free template was found.

## 1. Income and affordability

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| HCD 2026 State Income Limits (revised June 23, 2026 memo + county tables) | AMI bands for Orange County for CalHome and state programs | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/income-limits-2026.pdf | VERIFIED (text extracted, "Revised 2026 State Income Limits") |
| HCD 2026 State HOME Income Limits (effective June 1, 2026) | HOME-funded buyer income caps | PDF, free | https://www.hcd.ca.gov/sites/default/files/docs/grants-and-funding/2026-california-HOME-income-limits_0.pdf | VERIFIED |
| HCD income limits landing page | Link hub, calculation guide, state vs federal limits | HTML, free | https://www.hcd.ca.gov/grants-and-funding/income-limits | VERIFIED (loads) |
| HUD USER Income Limits dataset | Federal 30, 50 and 80% limits by county. Download or API | XLSX/CSV + API, free | https://www.huduser.gov/portal/datasets/il.html | VERIFIED (page states data is available via API) |
| HUD Fair Market Rent API docs | FMR and income limits by API. Needs a free account and access token | JSON REST API, free token | https://www.huduser.gov/portal/dataset/fmr-api.html | VERIFIED (page documents token signup) |
| CA Health and Safety Code 50052.5 | Owner "affordable housing cost" formula. The cap on buyer price | HTML statute, free | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=HSC&sectionNum=50052.5 | VERIFIED (via another fetch tool; a plain fetch gets a 403 but browsers work) |
| CA Health and Safety Code 50053 | Affordable RENT definition. A contrast case, not ownership | HTML statute | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=HSC&sectionNum=50053 | VERIFIED (same note) |
| CA Health and Safety Code 50079.5 | "Lower income households" definition (ties to HUD limits) | HTML statute | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=HSC&sectionNum=50079.5 | VERIFIED (same note) |
| Census ACS 5-year via Census Data API | Income distribution, household size, tenure by tract or city | JSON API, free (key optional at low volume) | https://www.census.gov/data/developers/data-sets/acs-5year.html | VERIFIED (loads). API index https://api.census.gov/data.html also VERIFIED |

## 2. Rates and costs

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Freddie Mac PMMS | Weekly 30-year rate. A default for a rate slider | HTML | https://www.freddiemac.com/pmms | VERIFIED |
| Freddie Mac PMMS history CSV | Machine-readable rate history (columns: date, pmms30, pmms15, pmms51 ...) | CSV, free | https://www.freddiemac.com/pmms/docs/PMMS_history.csv | VERIFIED (header and rows read) |
| FRED MORTGAGE30US | Rate series page. Latest observation shown 2026-11-05 = 7.18% | HTML + CSV/JSON via FRED API (free key) | https://fred.stlouisfed.org/series/MORTGAGE30US | VERIFIED (via another fetch tool; a plain fetch timed out, so the page may be slow, not down) |
| OC Treasurer-Tax Collector | Property tax bill and rate lookup by parcel for a real building | Web app (needs JavaScript), free | https://tax.ocgov.com | VERIFIED (loads). A rate table was not confirmed. Use about 1% plus local assessments as an assumption and say so |
| OC Treasurer-Tax Collector home | Tax rate and assessment info entry point | HTML | https://www.octreasurer.com | VERIFIED (loads, not drilled) |
| CA Dept of Insurance wildfire and insurance data | Insurance availability context. County analysis PDFs referenced from this section | HTML + PDF, free | https://www.insurance.ca.gov/01-consumers/200-wrr/ | VERIFIED (loads; page is "Wildfire Response and Readiness"). The Orange County analysis PDF was not opened |
| CA FAIR Plan key statistics | Policies in force by county and ZIP | HTML + spreadsheets | https://www.cfpnet.com/key-statistics-data | UNVERIFIED (appeared in search results; not fetched). No county premium number was found. Do not invent one |
| Terner Center "Cost of Building Housing" series | Hard cost and development-fee benchmarks | HTML + PDFs, free | https://ternercenter.berkeley.edu/research-and-policy/the-cost-of-building-housing-series/ | VERIFIED (series covers development fees) |
| Terner Center: Hard Construction Costs (Mar 2020) | Per-sf hard cost drivers. Dated: inflate it and say so | PDF, free | https://ternercenter.berkeley.edu/wp-content/uploads/2020/08/Hard_Construction_Costs_March_2020.pdf | VERIFIED (PDF loads; 2020 data) |
| HCD Residential Impact Fee Study (Terner) | Impact fee cost per unit by city | PDF, free | https://www.hcd.ca.gov/policy-research/plans-reports/docs/Impact-Fee-Study.pdf | VERIFIED (loads, 5 MB; city figures not read) |
| Terner Center: Community Land Trusts, Irvine | CLT cost and financing case study for Irvine | PDF, free | https://ternercenter.berkeley.edu/wp-content/uploads/2020/10/Community_Land_Trusts_Irvine.pdf | UNVERIFIED (from a search result only, not fetched) |
| RSMeans data (Gordian) | Professional unit-cost estimating | Paid subscription | https://www.gordian.com/products/rsmeans-data/ | VERIFIED (loads). Paid, not hackathon-friendly |
| Craftsman Book Co. cost software | Cheaper cost-estimating references | Paid books and software | https://www.craftsman-book.com/ | VERIFIED (loads) |

## 3. Market prices

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Zillow Research data page | Index downloads: ZHVI (home value), rent, inventory | HTML | https://www.zillow.com/research/data/ | VERIFIED (via another fetch tool; a plain fetch was blocked with 403) |
| Zillow ZHVI metro CSV (all homes, mid tier, smoothed, seasonally adjusted) | Price comps by metro and time. Direct download | CSV, about 4 MB, free | https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv | VERIFIED (header read) |
| Redfin Data Center | Downloadable market data (metro, city, zip) | TSV/CSV, free | https://www.redfin.com/news/data-center/ | VERIFIED (title "Downloadable Housing Market Data"). The specific file URL was not located |
| C.A.R. Housing Affordability Index, traditional | Orange County minimum qualifying income, payment, price | HTML table, free | https://www.car.org/marketdata/data/haitraditional | VERIFIED (Orange row present) |
| C.A.R. market data hub | Median price, sales, other affordability variants | HTML | https://www.car.org/marketdata/data | VERIFIED (loads) |
| FHFA House Price Index datasets | Long-run appreciation by metro and ZIP, for resale-formula stress tests | CSV/XLSX, free | https://www.fhfa.gov/data/hpi/datasets | VERIFIED |
| HMDA data browser (CFPB / FFIEC) | Actual loan amounts, rates and incomes by tract | Web + CSV/API, free | https://ffiec.cfpb.gov/data-browser/ | VERIFIED (loads; JavaScript app). CFPB overview https://www.consumerfinance.gov/data-research/hmda/ also VERIFIED |

No free source for local sales comps (newspaper or ATTOM-style) was found or checked.

## 4. Funding programs

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| HCD CalHome | State homeownership loans to local agencies and nonprofits (down payment, rehab, self-help) | HTML, free | https://www.hcd.ca.gov/grants-and-funding/programs-active/calhome | VERIFIED (loads, "CalHOME Program") |
| HCD Homeownership Super NOFA (HOSN) | Current state NOFA bundling homeownership programs | HTML, free | https://www.hcd.ca.gov/funding/hosn | VERIFIED |
| HCD HOME program | Federal HOME via the state. Income limits tie to the HOME PDF above | HTML | https://www.hcd.ca.gov/grants-and-funding/programs-active/home-investment-partnerships-program | VERIFIED (loads) |
| HCD CDBG | State CDBG | HTML | https://www.hcd.ca.gov/grants-and-funding/programs-active/community-development-block-grant | VERIFIED (loads) |
| HUD Exchange HOME | Federal HOME rules | HTML | https://www.hudexchange.info/programs/home/ | VERIFIED |
| HUD Exchange CDBG Entitlement | City-level CDBG | HTML | https://www.hudexchange.info/programs/cdbg-entitlement/ | VERIFIED |
| HUD Exchange SHOP | Land and infrastructure funds for sweat-equity builders | HTML | https://www.hudexchange.info/programs/shop/ | VERIFIED (page mentions sweat equity and volunteer-based programs) |
| CalHFA homebuyer programs | MyHome (junior loan up to 3.5% FHA / 3% conventional per the page), CalPLUS, ZIP, MCC | HTML | https://www.calhfa.ca.gov/homebuyer/programs/ | VERIFIED |
| CalHFA Dream For All | Shared appreciation loan. Page says up to 20%, cap $150,000, voucher and drawing | HTML | https://calhfa.ca.gov/dream/ | VERIFIED (availability of funds not confirmed) |
| CalHFA Forgivable Equity Builder | Forgivable 0% loan up to 10% (news reports) | n/a | none found | UNVERIFIED (no official URL located; a 2022 board handout said it was winding down). Do not model it as open |
| FHLBank SF Community Programs | Parent page for WISH and AHP | HTML | https://www.fhlbsf.com/products/community-programs-grants | VERIFIED |
| FHLBank SF WISH | Grants for first-time buyer down-payment help via member banks | HTML | https://fhlbsf.com/products/community-programs-grants/wish | VERIFIED |
| FHLBank SF AHP | Affordable Housing Program (competitive grants and subsidized advances) | HTML | https://fhlbsf.com/products/community-programs-grants/ahp | VERIFIED (loads) |
| Orange County Housing Finance Trust | Countywide housing funding (NOFA page) | HTML | https://www.ochft.org/ | VERIFIED (loads). No homeownership text on the home page. Programs page https://ochft.org/programs loads and shows a NOFA |
| Santa Ana My First Home | City down-payment loan | HTML | https://santa-ana.org/my-first-home | VERIFIED (loads, "My First Home Program"). Loan terms came from a search snippet, not the page: read the page |
| Garden Grove 2025 first-time homebuyer guidelines | City down-payment program rules | PDF, 22 MB | https://ggcity.org/sites/default/files/2025-first-time-homebuyer-guidelines.pdf | VERIFIED (loads, not read in full). Dollar tiers came from a snippet only |
| Anaheim, Costa Mesa, Fullerton down-payment programs | City programs | n/a | n/a | UNVERIFIED (city sites block bots). No confirmed program found for these three. Check by phone. A "Homebuyer-Assistance" Anaheim URL seen elsewhere is actually a specific plan page: do not use it |
| Irvine Community Land Trust | Local CLT ownership | n/a | n/a | UNVERIFIED (official site not found). Start from the City of Irvine, https://www.cityofirvine.org/ (VERIFIED loads) |
| CDFI Fund | CDFI Program awards to lenders. A source of capital | HTML | https://www.cdfifund.gov/programs-training/programs/cdfi-program | VERIFIED |
| CRA (OCC) | Banks' Community Reinvestment Act obligations as a lending lever | HTML | https://www.occ.treas.gov/topics/consumers-and-communities/cra/index-cra.html | VERIFIED (loads). The FFIEC CRA data page returned 403: UNVERIFIED |
| Low Income Investment Fund | CDFI lender for affordable housing | HTML | https://www.liifund.org/ | VERIFIED (loads) |
| State housing bond | Housing bond money | n/a | n/a | UNVERIFIED (HCD URLs tried returned 404). Prop 1 (2024) is the behavioral health bond. No homeownership set-aside was confirmed |
| LIHTC | Rental only, not applicable to ownership | n/a | n/a | Note only |
| Employer-assisted housing examples | Employer down-payment programs | n/a | n/a | NOT FOUND: no verified source |

## 5. Community land trusts and shared equity

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| Grounded Solutions Network CLT pages | Shared-equity and CLT explainers, resale-formula guidance | HTML | https://groundedsolutions.org/strengthening-neighborhoods/community-land-trusts | VERIFIED |
| Grounded Solutions resource library | Documents and tools hub | HTML | https://groundedsolutions.org/tools-for-success/resource-library/ | VERIFIED (loads; redirects to the homepage) |
| Lincoln Institute data | Land and CLT data and research | HTML / data | https://www.lincolninst.edu/research-data/ | VERIFIED (loads) |
| NeighborWorks | Homeownership pro formas and resources | HTML | https://www.neighborworks.org/ | UNVERIFIED (blocked with a 403) |

## 6. Donors and earned revenue

| Source | Use it for | Format / cost | URL | Status |
|---|---|---|---|---|
| IRS charitable contribution deductions | Donor tax rules overview | HTML | https://www.irs.gov/charities-non-profits/charitable-organizations/charitable-contribution-deductions | VERIFIED |
| IRS Publication 561 (valuing donated property) | Fair market value of donated goods | HTML / PDF | https://www.irs.gov/publications/p561 | VERIFIED (PDF https://www.irs.gov/pub/irs-pdf/p561.pdf also loads) |
| IRS Form 8283 | Noncash donations over $500 | HTML / PDF | https://www.irs.gov/forms-pubs/about-form-8283 | VERIFIED |
| IRS Publication 526 | Charitable contributions for donors | PDF | https://www.irs.gov/pub/irs-pdf/p526.pdf | VERIFIED (loads) |
| eBay Browse API | Active-listing price comps by keyword or image | REST API, free developer account + OAuth | https://developer.ebay.com/api-docs/buy/static/api-browse.html | VERIFIED (loads). Sold data is NOT in Browse |
| eBay Marketplace Insights API | Sold listings (last 90 days) | Restricted access | https://developer.ebay.com/api-docs/buy/marketplace-insights/overview.html | UNVERIFIED (redirects to sign-in; limited release). Plan on Browse or manual comps |
| Goodwill valuation guide | Item value ranges for donors | n/a | n/a | UNVERIFIED (site returned 403; guide URL not confirmed) |
| Facebook Marketplace / OfferUp pricing | Price comps | No public API found | n/a | NOT CHECKED. Assume manual |

## 7. Pro forma templates

No free affordable-ownership pro forma template was confirmed. The Grounded Solutions library and
NeighborWorks (blocked) are the likeliest places. Teams can build their own from Health and Safety
Code 50052.5 plus the Freddie Mac rate series.

## A made-up deal for testing

[`synthetic-example-deal.json`](synthetic-example-deal.json) is a one-home example, the same bill
as the worked example in the background doc and the challenge brief. It is **SYNTHETIC**: not a
real project, program, city or buyer. Every number is a rounded **ASSUMPTION** (cost to create by
line, what the family can pay, subsidies, earned income and the fundraising gap, balancing to $0).
Use it to test your tool's math. Never cite it as a
benchmark or show it as real.
