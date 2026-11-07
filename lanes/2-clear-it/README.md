# Lane 2: Clear it

> How do we turn four years into two?

**Room:** any room. Your team picks one on the hub.

## The problem

Time is cost. Builders who have done it describe a path that can cut the timeline to about two
years:

- start on land that is already zoned correctly
- get a **ministerial** approval: if you meet the written rules, the city must say yes, with no
  hearing and no discretion
- use state-approved plans

The obstacle is finding that path. Every one of Orange County's 34 cities has its own forms, fees
and checklists. City forms sometimes misread state law, and the state housing department (HCD)
regularly issues letters telling cities they got it wrong.

And approval is only one delay. Projects also wait on plan-check corrections, utility and fire
sign-offs, funding rounds that open once a year, condo map paperwork and relocating tenants. Every
month of waiting costs money.

## Who is stuck

A nonprofit project manager, a small builder, a homeowner adding an ADU, or a city permit tech who
wants to get it right.

## The open question

The fast path exists on paper. Why is it so hard to find and follow in practice, and what would
make it the normal path instead of the rare one?

## Ideas to get you thinking (not a spec)

Each one comes from a place the process breaks today. Build something else if you like.

1. **Pick the path for one address.** An ADU, an SB 9 two-unit, an SB 9 lot split, a map for 10
   or fewer parcels and streamlined multifamily each have their own clock and tests. Help a person
   see which fit, and what each one costs in time.
2. **Catch old law in live documents.** ADU law was renumbered from Gov Code 65852.2 to 66310
   through 66342, but city checklists and HCD letters still use the old numbers. A checker that
   maps old to new, and flags what else looks stale, is a real tool.
3. **Audit a city's checklist.** State law requires cities to post online checklists and sample
   approved applications for certain project types. Nobody has checked every OC city. Compare one
   city's checklist and fees with what state law allows.
4. **Measure real timelines.** There is no open permit dataset in OC, but cities report
   applications, entitlements, permits and completions to HCD every year. Turn that into "how long
   does it really take in this city?" and say what the data cannot show.
5. **Make the enforcement letters findable.** HCD's letters to cities are behind an embedded
   dashboard. A searchable view by city and law helps a permit tech or an advocate. Mind the data
   rule: do not scrape at volume. HCD lists a contact for copies.

## Starting data

See [`data/DATA-SOURCES.md`](data/DATA-SOURCES.md): state law text, HCD guidance, permit
and progress-report data, city pages, and factory-built housing, each marked VERIFIED or
UNVERIFIED. Read its "statute numbers changed" note first.

Also here: [`data/oc-cities.json`](data/oc-cities.json), the 34 Orange County cities with empty
fields for each city's permit page, ADU checklist and fees (filling them is part of the work);
[`data/timeline.json`](data/timeline.json), the four-year baseline and the other delays; and
[`scenarios.json`](scenarios.json), three made-up users to design and test against.

Rules for everyone are in [ground rules](../../docs/ground-rules.md). Background is in
[background](../../docs/background.md) and the [glossary](../../docs/glossary.md).

A real case to test against: any publicly listed small building or lot in Orange County, roughly 4
to 12 homes. Label every assumed number.
