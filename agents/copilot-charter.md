# 21 — The Co-pilot: a read-only query layer over the finance function

*Written 18 Aug 2026. Adds a seventh agent to the blueprint in doc 03 — the first one that answers questions rather than producing artefacts. Input to Fable #3 (charters) and a candidate build for Day 8.*

---

## The idea, and why the constraint is the feature

The workflows produce standard outputs on a cadence. Someone always wants something the standard output doesn't show, or wants the same thing cut a different way. Today that request goes to the finance person and takes a day.

A chat box over the finance data solves it — but only if it is **bounded correctly**. The bound, stated by Jonathan and worth quoting because it is the entire design:

> *"The idea of the co-pilot is not to come up with new numbers. It's to surface numbers that exist somewhere in the dataset. The second thing it can do is slice the numbers differently if asked. Same data, just sliced differently."*

That constraint is not a limitation. It is the thing that makes the tool safe enough to put in front of a CEO.

An assistant that *computes* on demand is the fastest possible way to manufacture the exact problem this whole project exists to solve: a fourth version of ARR, produced in a side conversation, that nobody can trace and that doesn't tie to the board pack. Restricting the Co-pilot to retrieval and re-aggregation means **every answer it gives already exists somewhere with a lineage**.

---

## The contract

### It MAY

**Retrieve.** Return a figure that exists in the ledger, a statement, a subledger, a document, or a registered metric — with its source.

**Re-aggregate.** Return the same underlying facts grouped, filtered, or expressed differently: by country instead of by segment, by quarter instead of by month, in constant currency, excluding one-offs, for a customer cohort rather than the whole book.

**Explain.** Show a metric's registered definition and version, walk the lineage from a number back to its journal lines and source documents, and decompose a movement into the drivers the Analyst already attributed.

**Compare.** The same registered metric across periods, segments, plans, or definitions — including showing two registered definitions of ARR side by side, because both are registered.

### It MAY NOT

**Invent a definition.** If the question requires a convention that is not in the metric registry, the Co-pilot does not choose one.

**Forecast, estimate or extrapolate.** Forward-looking numbers come from the Forecaster, with its assumptions attached. The Co-pilot may *retrieve* a forecast; it may not *make* one.

**Reclassify.** It cannot decide that an item belongs in a different bucket, even if the requester asks. That is a semantic-layer change with a version number.

**Answer without provenance.** No figure is returned bare.

### What it does when asked to cross the line

This is the most important behaviour in the charter. Asked *"what's our ARR including the pipeline that's about to close?"*, the correct response is not a number:

> That would need a definition we haven't registered. The closest registered metrics are MET-009 committed recurring ARR ($4.64M at Jul-26) and MET-011 the commercial view including trailing event revenue ($5.30M). Counting unclosed pipeline would be a new convention — it needs a ruling in the semantic layer, an owner and a version, because whatever answer we give here will be quoted back to us. Want me to draft the registry entry for review?

**The Co-pilot converts an ad-hoc question into a governance event.** That is the opposite of what an unbounded assistant does.

---

## The dimensional model

"Slice it differently" only works if the dimensions are declared. Re-aggregation is bounded by this list; anything outside it is a new definition.

| Dimension | Values |
|---|---|
| **Time** | month, quarter, year, trailing twelve months, custom range, plan period |
| **Revenue segment** | Player, Courts, Academy, usage overage, credit packs, events |
| **Geography** | country, EU vs US, Iberia vs rest |
| **Customer** | individual account, signup cohort, size band by courts or spend, partner-sourced vs direct, contract term length, billing cadence, has-minimum vs no-minimum |
| **Currency** | EUR, USD reported, USD constant currency |
| **P&L** | account, account group, cost centre, function (R&D / S&M / G&A) |
| **Recognition state** | billed, recognised, unbilled, deferred, collected |
| **Plan version** | actuals, FY26 board plan, Apr-26 reforecast |
| **Contract state** | active, renewed, contracted-not-installed, churned |

The interesting cuts fall straight out of this. *Gross margin by customer size band. ARR by country in constant currency for clubs on 36-month terms. Overage revenue for partner-sourced clubs only. The July P&L on the January plan versus the April reforecast.* All of these are the same facts, re-grouped — no new judgement required.

---

## Provenance on every answer

Every response carries, without being asked:

- **The metric registry ID and version** for each figure
- **Where it ties** — "this is the same number as slide 2 of the July board pack"
- **The lineage path** — which accounts, which journal lines, which source documents, available on request
- **The as-of date and the close status** of the period
- **A confidence marker** where the underlying data is known-incomplete (April 2025's usage gap, anything in the open month)

That last one matters. Asked about April 2025 usage, the Co-pilot must say the logs for that month are 42% complete before giving a figure.

---

## Where it sits in governance

The Co-pilot is **read-only and non-mutating**, which changes the autonomy argument from doc 19. The ladder there governs *actions*; this agent takes none. Its risk is not that it does something wrong, but that it says something wrong which a human then acts on.

So it gets a different treatment:

- **Autonomy: autonomous, with full query logging.** No approval step — a query that returns a wrong number blocks nobody and breaks nothing directly.
- **Every query and answer is logged** with the metrics cited, the lineage returned, and who asked. If a number surfaces in a board meeting, you can find the query that produced it.
- **Hard line, permanently: it never writes.** Not to the ledger, not to the registry, not to a report. It may *draft* a proposed registry entry for human review, which is a document, not a change.
- **It inherits demotion from the semantic layer**: if a definition is under review, metrics depending on it are returned with a flag until the review closes.

---

## The query log feeds the improvement loop

This is the part that compounds, and it connects directly to doc 19.

The questions people ask are evidence about what the standard reporting is missing. If the CEO asks for the same re-slice three months running, that cut belongs in the board pack. If five different questions all fail because they need the same unregistered convention, that convention has just earned a place at the top of the semantic-layer queue.

Two metrics to track on the Co-pilot itself:

- **Refusal rate and refusal reasons** — a rising refusal rate concentrated on one convention is a prioritised backlog, generated for free
- **Repeat-query clusters** — candidate standard views, and evidence for what to add to slide 2

An ad-hoc query tool is normally a leak in the reporting process. Logged and analysed, it becomes the requirements-gathering mechanism for the reporting process.

---

## Failure modes

**It becomes the number factory.** Everyone gets their own cut, cites it in a meeting, and the organisation is back to numbers that don't agree. Mitigation: provenance on every answer, and the tie-out line — *"this is the same number as slide 2"* — is not optional garnish, it is the control.

**Plausible re-aggregation of the wrong base.** Slicing revenue by country is fine; slicing *gross margin* by country requires allocating shared COGS, which is a judgement. The dimensional model must mark which measures are safely sliceable on which dimensions, and the Co-pilot must refuse the rest rather than silently allocating.

**Confident answers on incomplete periods.** The open month always looks like a collapse in revenue. Every answer touching an unclosed period must say so.

**Question drift into advice.** *"Should we raise prices?"* is not a retrieval question. The Co-pilot answers with what the data shows about price cohorts and declines the recommendation — that is the human's job, and it is the job being sold.

---

## Why this is worth building for the demo

It is the most *legible* part of the whole system. A hiring manager can evaluate a data pipeline only by taking your word for it. They can evaluate a chat box in ninety seconds by asking it something hard.

The demo sequence writes itself:

1. **A retrieval question.** *"What was gross margin in July?"* → 69.6%, MET-003 v1.0, ties to slide 2.
2. **A re-slice.** *"Now split that by revenue segment and show me the same thing in constant currency."* → same facts, different cut, still tied.
3. **A lineage question.** *"Why did it move from April?"* → the driver decomposition the Analyst already produced, tracing to the November model swap and the May surge.
4. **A refusal.** *"What's ARR if we include the seven clubs that signed but aren't installed?"* → *that's not a registered definition; here's why; here's what I'd need ruled; want me to draft the entry?*

Step four is the one that wins the room. Every other AI finance demo answers the fourth question with a confident number.

---

## Open questions for Fable #3

- Does the Co-pilot get its own charter, or is it an interface *over* the other six agents' outputs? Leaning: its own charter, because its refusal behaviour is a distinct design and it has a hard line the others don't.
- Should it be able to retrieve from **documents** as well as the ledger — *"show me the payment terms in the federation contract"*? Leaning yes, since that is retrieval, and it makes the Day 4 ingestion work visible.
- Name. "Co-pilot" is the industry term and clear. "The Librarian" describes the constraint better — it fetches what exists and knows where everything is; it does not write new books.
