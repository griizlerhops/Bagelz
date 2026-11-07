# Lane 1: Find it

> Where can the next affordable home go?

**Room:** any room. Your team picks one on the hub.

## The problem

Nonprofits mostly find sites by luck: a city calls about surplus land, or a church offers its
parking lot. Meanwhile California has passed a wave of laws that open up land that used to be
off-limits. Examples include:

- lot splits on single-family lots (SB 9)
- small-lot subdivisions of up to 10 homes without a hearing (SB 684 / SB 1123)
- housing on commercial corridors (AB 2011)
- housing on faith and nonprofit-college land (SB 4)
- converting existing apartments to ownership condos

The laws are public and so is the parcel data, but nobody has connected the two in a way a small
nonprofit can use.

And a legal site isn't always a usable one. Teams still need to know who owns it and whether
they'd sell, whether it can actually be built on (slope, contamination, fire or flood zones, water
and sewer capacity), and whether a nonprofit can move before a market-rate buyer does. Land is the
biggest line on the bill.

## Who is stuck

A nonprofit acquisitions lead with no GIS team, a congregation sitting on an underused lot, or
city housing staff.

## The open question

The laws are public. The parcel data is public. So why does finding a site still come down to
luck, and what would change that?

## Ideas to get you thinking (not a spec)

Each one comes from a place the data breaks today. Build something else if you like.

1. **A yes / no / unknown with a reason.** Each law has stacked site tests. SB 9 excludes
   historic districts. SB 4 excludes fire zones, fault zones, flood zones, wetlands and more. One
   answer for one parcel needs several map layers. Show which test passed, which failed and which
   could not be checked.
2. **Fill the ownership gap with a proxy.** There is no free layer that says a parcel is owned by
   a religious institution or an independent college, which SB 4 needs. Worship-site maps and the
   IRS exempt-organizations file are building blocks. Say clearly that a proxy is a lead, not a
   fact.
3. **Clean up the surplus-land notices.** They are public data, but many rows are marked
   "Archive" and parcel size is sometimes text like "9,005 SF". Make them usable, join them to
   zoning, and show who to call.
4. **Catch stale sites.** Housing-element site lists are submitted when a plan is adopted, so a
   parcel may have since sold or been built. Compare the list with building footprints or existing
   land use.
5. **Be the city rules layer.** State law lets cities apply objective standards, such as parking
   and setbacks. A tool that answers "does state law allow it here?" also has to read the city's
   rules. Pick one city and do it well.

## Starting data

See [`data/DATA-SOURCES.md`](data/DATA-SOURCES.md): parcels, zoning, housing-element sites,
surplus land, constraints and statute text, each marked VERIFIED or UNVERIFIED.

Also here: [`data/pathways.json`](data/pathways.json), the five land pathways from the brief with
official sources, and [`scenarios.json`](scenarios.json), three made-up users to design and test
against.

Rules for everyone are in [ground rules](../../docs/ground-rules.md). Background is in
[background](../../docs/background.md) and the [glossary](../../docs/glossary.md).

A real case to test against: any publicly listed small building or lot in Orange County, roughly 4
to 12 homes, new build, rehab or conversion. Label every assumed number.
