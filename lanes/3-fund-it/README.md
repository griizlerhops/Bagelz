# Lane 3: Fund it

> Does it pencil, and who closes the gap?

**Room:** any room. Your team picks one on the hub.

## The problem

Developers say a project "pencils" when the numbers work. Affordable ownership almost never
pencils on its own. The family's price is capped by income: housing costs should stay around
30 to 35 percent of what they earn, so the price cannot rise to cover cost.

The gap gets filled from many sources:

- city, state and federal programs (CalHome, HOME, local housing funds)
- down-payment programs
- lenders
- employers
- donors
- earned revenue, such as donated-goods resale

Today that stack gets assembled by hand, one project at a time.

## Who is stuck

A nonprofit finance lead, a development director, a donor, or a city housing analyst.

## The open question

Every project has a gap. What makes it smaller, or makes the money that closes it easier to find?

## Ideas to get you thinking (not a spec)

Each one comes from a place the money breaks today. Build something else if you like.

1. **A gap calculator that tells the truth about dates.** Income limits are revised during the
   year and differ by program (State, State HOME, HUD). Pick the right table, show its date, and
   warn when it is stale.
2. **Rate sensitivity.** With the price capped by income, a move in the mortgage rate changes the
   gap directly. Show how far the gap moves when the rate moves. Use a published rate series and
   label it.
3. **Show a donor what a gift closes.** Turn a gap number into "your $X covers this line of this
   home". Keep the numbers honest: assumptions labelled, sources shown.
4. **Match a household to the help it can stack.** City down-payment loans, state programs and
   bank grants each have their own terms, and program lists go stale. Show what a household might
   qualify for, and mark anything whose funds are not confirmed.
5. **Price donated goods.** Resale of donated goods can be a funding line. Help a store price items
   fast and give donors a defensible value. Know what your price data can and cannot show.
6. **Build the missing pro forma.** No free pro forma template for affordable ownership has been
   confirmed. One built from the statute's affordable-cost formula plus a published rate would be
   useful on its own.

## Starting data

See [`data/DATA-SOURCES.md`](data/DATA-SOURCES.md): income limits, rates and costs, market prices,
funding programs, land trusts and donor sources, each marked VERIFIED or UNVERIFIED.

Also here: [`scenarios.json`](scenarios.json), three made-up users (a finance lead, a rate change,
a donor) to test against the example deal.

There is also a made-up example deal for testing:
[`data/synthetic-example-deal.json`](data/synthetic-example-deal.json). It is the same one-home
bill as the worked example in [background](../../docs/background.md): $535k to create, $285k the
family can pay, a $95k fundraising gap. It is synthetic. Every number in it is an assumption. Do
not cite it as a benchmark.

Rules for everyone are in [ground rules](../../docs/ground-rules.md). Background is in
[background](../../docs/background.md) and the [glossary](../../docs/glossary.md).

A real case to test against: any publicly listed small building or lot in Orange County, roughly 4
to 12 homes, new build, rehab or conversion. Label every assumed number.
