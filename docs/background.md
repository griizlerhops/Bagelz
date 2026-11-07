# Background

Five minutes of context for people who have never worked in housing finance, land use or permits.
Claims come from the event brief or from the sources linked. Checked November 6, 2026. Laws change
and get renumbered, so read the source before you build on it.

## The $0 equation

Every affordable ownership home has to balance this:

> **What the family can afford to pay + public subsidies + fundraising − the cost to create the home = $0**

In Orange County, a median home costs about $1.47 million, and only about 15% of households can
afford one (C.A.R., Q3 2026). That leaves teachers, nurses, firefighters and the kids who grew up
here two choices: leave, or commute an hour or more each way.

Nonprofits that build affordable ownership homes do exist. So do community land trusts, faith
communities with land, employers trying to house their own workforce, and city housing offices.
They all face the same equation. In OC, the cost side usually wins by six figures per home.

How the lanes map onto it: the family's share is fixed by income. **Lane 1 (Find it)** lowers the
cost of land. **Lane 2 (Clear it)** lowers the cost of time. **Lane 3 (Fund it)** grows subsidies
and fundraising to close the gap that's left.

### Worked example: one home's bill

Mock numbers, rounded, based on a typical project. Not a real deal.

| Cost to create | | Paid by | |
|---|---|---|---|
| Land and building purchase (Lane 1) | $360k | Family's price (fixed by income) | $285k |
| Time costs while waiting: loan interest, taxes, insurance, management (Lane 2) | $85k | Public subsidies (Lane 3) | $100k |
| Construction and repairs | $40k | Rent earned while waiting (Lane 3) | $55k |
| Fees, design, legal, sales | $50k | **Fundraising: the gap (Lane 3)** | **$95k** |
| **Total** | **$535k** | **Total** | **$535k** |

Paid by − cost to create = $0. When this project's schedule slipped 10 months, the fundraising it
needed grew about 7 times. Time is money on both sides of the equation. The same example is in
[`lanes/3-fund-it/data/synthetic-example-deal.json`](../lanes/3-fund-it/data/synthetic-example-deal.json).

## Why there is a gap

Price is set by the market. What a buyer can pay is set by income. Affordable housing is usually
defined so that housing costs stay around 30 to 35 percent of what a household earns, so the price
cannot rise to cover cost. California's definition of affordable housing cost for owners, by income
category, is in [Health and Safety Code 50052.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=HSC&sectionNum=50052.5).

The difference between cost and what the buyer can pay is the gap. It gets filled from many
sources: city, state and federal programs, down-payment programs, lenders, employers, donors and earned
revenue such as donated-goods resale. Today that stack gets assembled by hand, one project at a
time. That is Lane 3.

Income limits are set by program and revised during the year. HCD's 2026 State Income Limits were
revised June 23, 2026, and the State HOME table is a separate document
([HCD income limits](https://www.hcd.ca.gov/grants-and-funding/income-limits)).

## Four years to two

A home typically takes about four years from finding land to handing over keys:

| Step | About |
|---|---|
| Rezoning | a year |
| Entitlements | a year |
| Plans | six months to a year |
| Build | a year |

Every month of that adds cost.

Builders who have done it describe a path that can cut this to about two years:

1. Start on land that is already zoned correctly.
2. Get a **ministerial** approval. If you meet the written rules, the city must say yes, with no
   hearing and no discretion.
3. Use state-approved plans.

The obstacle is finding that path. Every one of OC's 34 cities has its own forms, fees and
checklists. City forms sometimes misread state law, and the state housing department (HCD)
regularly issues letters telling cities they got it wrong. That is Lane 2.

## Land

Coastal Southern California has almost no vacant land, so new homes come from re-using land.
California has passed a wave of laws that open up land that used to be off-limits. The laws are
public and so is the parcel data, but nobody has connected the two in a way a small nonprofit can
use. That is Lane 1.

## The laws in one paragraph each

These summaries stay close to HCD's own fact sheets. They are orientation, not legal advice. Each
law has several tests that all have to be met. Read the source.

**SB 9: lot splits and duplexes.** Lets a single-family lot be split in two and allows up to two
units on each lot, approved without a hearing if the written tests are met. Sections: Gov Code
65852.21 and 66411.7. HCD's fact sheet describes a 60-day decision clock and a 30-day completeness
check. It excludes historic districts and requires no tenant occupancy in the prior three years.
Cities may apply objective standards, such as parking up to one space per unit and setbacks up to
four feet. Source: [HCD SB 9 fact sheet](https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/lot-splits-and-duplexes-sb-9.pdf).

**SB 684 and SB 1123: small-lot subdivisions.** Allow lots to be subdivided into 10 or fewer
parcels, for small-lot homes, through a ministerial process with no hearing. The map rule is Gov
Code 66499.41. The companion building-permit rule is Gov Code 65913.4.5. SB 1123 amended these.
Confirm the exact text before you build rules on it. Sources: [66499.41](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66499.41),
[HCD fact sheets](https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/housing-law-fact-sheets.pdf).

**AB 2011: housing on commercial corridors.** Allows affordable housing by right on certain
commercial and office sites. The rules are in Gov Code 65912.100 to 65912.140. HCD's guidelines
for it were labelled Draft when we checked. Source: [HCD draft AB 2011 guidelines](https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/draft-ab-2011-guidelines.pdf).

**SB 4: faith and nonprofit-college land.** Allows by-right approval of housing on land owned by
a religious institution or an independent college as of January 1, 2024. Units must be 100% lower
income, with up to 20% moderate and 5% for staff. The site must pass tests: it excludes very high
fire zones, earthquake fault zones, special flood hazard areas, wetlands, farmland and sites near
certain industrial uses, and needs 75% of the perimeter adjoining urban uses. Gov Code 65913.16,
effective July 2, 2024 through January 1, 2036. Source: [HCD SB 4 fact sheet](https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/aff-hsg-faith-higher-ed-sb-4.pdf).

**Surplus Land Act.** Local agencies disposing of land must first offer it for affordable housing
and publish a notice of availability. The notices are published as data. The State also screened
44,000+ state-owned parcels for excess sites under Executive Order N-06-19, with a developer
interest portal. Sources: [HCD Surplus Land Act](https://www.hcd.ca.gov/planning-and-research/public-lands/surplus-land),
[HCD Excess State Land](https://www.hcd.ca.gov/planning-and-research/public-lands/excess-state).

**ADU law.** Accessory dwelling unit approvals are ministerial, with a 60-day clock and
deemed-approved if the city misses it, per HCD's ADU Handbook (March 2026). ADU law is no longer
Gov Code 65852.2. It was renumbered to Gov Code 66310 to 66342 (SB 477, March 2024), but older
city documents and HCD letters still use the old numbers. Source: [HCD ADU Handbook](https://www.hcd.ca.gov/sites/default/files/docs/policy-and-research/adu-handbook-update.pdf).

**Converting apartments to ownership condos.** The Subdivision Map Act has steps and notice periods
for conversions, including tenant notices. Start at Gov Code 66427.1. Source: [66427.1](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=66427.1).

## Where enforcement shows up

HCD has direct enforcement authority over the SB 9 sections (65852.21 and 66411.7) since January
1, 2024. Its Housing Accountability Unit publishes technical-assistance and violation letters to
cities ([letters dashboard](https://www.hcd.ca.gov/hau/enforcement-letters)). One example: HCD says
Huntington Beach voted in February 2023 to stop accepting ADU and SB 9 applications. The state
sued on March 8 and the council resumed processing on March 21
([HCD press release](https://www.hcd.ca.gov/about-hcd/newsroom/california-sues-huntington-beach-violating-state-housing-element-law)).

## Progress against targets

HCD publishes 6th-cycle RHNA progress and Housing Element Annual Progress Report data, which show
how far each city is behind its housing target. See Lane 2 and Lane 1 data lists.

## The closing question

After the awards: if we combined the best Find, Clear and Fund tools from today, could one
affordable home in Orange County hit $0?
