# 73 — The routing review: a standing cadence, not an event

*Ruled 23 Aug 2026. Makes doc 72 repeatable. Amends doc 70 (routing doctrine)
with a review cadence and a table that is a file rather than a paragraph.
Companion to doc 19 (self-improvement loop) and doc 06 (builder budget).*

---

## The ruling

**The routing table is reviewed on the first working day of every month,
whether or not anything looks wrong**, and off-cycle on any of five named
triggers. The review produces candidates and evidence. It never re-tiers
anything by itself.

## Why monthly, and why not quarterly

Doc 70 was written on 20 August. Opus 5 had shipped on 24 July — the top tier
had already halved in price four days before the doctrine that assigned it was
written, and nobody noticed for a month.

On a quarterly cadence that is up to **three months of paying twice for the
same capability**, and the loss is invisible: nothing errors, no check fails,
the pack still ties. A cost that only shows up when somebody goes looking is
exactly the class of cost that needs a diary entry rather than an instinct.

Monthly also matches the two things it has to line up with: the builder's
budget cycle, and the close. The review runs on the same month-end data the
close runs on.

## The five off-cycle triggers

Any one of these fires a review the same week, not at the next month end:

1. **A new model ships in any tier, or a published price changes.**
2. **The refusal gate regresses** on the Co-pilot eval suite — a behaviour
   change is a routing question even when nobody touched the routing.
3. **A materiality miss on a tier below where the step belongs.** One-strike.
4. **A step escalates on more than 10% of runs** across a full cycle.
5. **Spend exceeds the cap.**

Triggers 2 and 3 are quality events that happen to have a cost consequence.
They are on this list because a review that only fires on price is a review
that only ever finds savings, and that is not a review, it is a shopping trip.

## What the review reads

| Source | What it answers |
|---|---|
| `routing_table.json` | What we decided, when, and at what prices |
| The usage log | What actually ran, on which tier, at what token shape, and whether the human accepted it |
| `copilot_evals.json` + the scorer | Did behaviour hold |
| The review ledger | Which corrections were routed as model errors |
| Published prices | Did the ground move |

**The usage log is the instrument, and it has one column that matters more
than the rest: `accepted`.** Tokens tell you what a step cost. Only acceptance
tells you whether the tier was right. A log without it produces a cost report,
not a routing review, and the difference is that a cost report can only ever
argue for going cheaper.

## The asymmetry, and it is deliberate

**Promotion is one-strike.** A single materiality miss on a tier below where
the step belongs moves it up the same day, on the evidence of the one miss. No
threshold, no accumulation.

**Demotion is earned.** A sustained run of clean, accepted output — 50 runs is
the current threshold — then a shadow cycle where the cheaper tier runs beside
the incumbent and is scored before anything switches.

Getting this backwards is how a cost review becomes an incident. The two
errors are not symmetric: routing a step up costs money, and routing it down
costs a wrong number that survives review. **Cost is never a gate on its own** —
a cheaper table that loses a point of escalation recall is a worse table.

## Three levels, cheapest first

The review checks in this order, because the order is the cost of acting:

1. **Levers.** Is batch on where the step is not interactive? Is the standing
   context cached? These are configuration, not behaviour, and they need no
   trial, no shadow run and no ruling. On the demonstration instance they are
   currently worth more than the entire top tier.
2. **Prices.** Did the ground move. A table edit and a shadow trial — doc 72
   is the worked protocol.
3. **Assignments.** Is each step still on the right tier. This is the slow one
   and it is the only one that can make the system worse.

Anyone reaching for a re-tiering before the levers are collected is optimising
the expensive lever first.

## What the review may never do

- **Re-tier itself.** It produces candidates. A human signs the ruling, after a
  shadow run, exactly like a semantic-layer change.
- **Compare across effective dates without saying so.** Cost-per-workflow
  figures either side of a table version are not comparable, and every artefact
  quoting one names the version that produced it.
- **Demote on cost evidence alone.** Acceptance and escalation are the
  evidence; cost is the reason to look.

## The first review already found something, and it was not a price

Table v1.0 expected the top tier to be **~40% of spend**. It now measures
**23%** — with nothing routed differently. The 40% was struck when the top tier
cost $10/$50, so halving its price halved its share.

The expectation itself was stale. That is worth stating plainly because it is
the failure mode a periodic review exists to catch and the one nobody writes
down: **not the number being wrong, but the yardstick being wrong** — and a
yardstick nobody re-measures will eventually declare a healthy system broken,
or a broken one healthy. The threshold is restated at 22% with a note saying
why, which is what a versioned table is for.

## Owner and artefacts

**Owner:** Head of Finance. Not engineering — the judgement being made is
materiality, and materiality is a finance judgement wearing an infrastructure
costume.

| Artefact | What it is |
|---|---|
| `package/routing_table.json` | The table as a versioned file: tiers, prices, per-step assignments, materiality thresholds, review cadence and gates |
| `package/routing_review.py` | Reads the table and the usage log; reports spend by tier and workflow, promotion and demotion candidates with their evidence, and the levers left uncollected |
| `package/copilot_evals.json` · `copilot_eval.py` | The behaviour gates the review must clear before anything ships |
| The monthly report | Filed with the close, one row per month, so cost per workflow becomes a series rather than an anecdote |

## The line this earns

> *"Our model routing is a versioned file with a monthly review on it. Last
> month it flagged one step escalating a fifth of the time — that moved up the
> same day — and one that had been clean for 185 runs, which goes to a shadow
> cycle before it moves down. The two are not treated the same way, because
> being wrong upward costs money and being wrong downward costs a number
> somebody believed."*
