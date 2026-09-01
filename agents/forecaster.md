# 46 — The Forecaster: the difference between a forecast and an extrapolation

**Date** 18 August 2026 · **Status** built, run and verified · **Closes plan-day 7**

The last half-shipped row on the scorecard, and the one every other artefact had been pointing at. The pack's cover said *"NONE — last refresh April 2026, four cycles ago."* The Exec Summary's third decision was *"commission a forecast."* Runway was captioned *"not a forecast — none exists."* Slide 7 of the board deck read NOT PRODUCED.

Built: `package/forecast.py`, `package/charters/forecaster.md`, a first run on July 2026, and an eighteenth tab on the reporting pack.

---

## The design question

A forecast and an extrapolation produce a number of the same shape, and **only one of them can be argued with.**

A reader cannot disagree with *8% growth* — there is nothing in it to disagree with. A reader can disagree with *"eleven gross adds a month at an average contracted value of $606"*, because that is a claim about the world with a person's name attachable to it. So rule 1 is absolute: every forecast line resolves to a driver, every driver to a measurement over a stated window, and the engine will not compute a growth rate on a total.

Which surfaces the question the engine exists to answer, and which nobody asks because the answer is normally invisible:

> **Estimated over which window?**

Fifteen drivers, each measured over three, six and twelve months, all three reported side by side with the dispersion between them. **Where those answers disagree materially, the choice of window *is* the forecast** — and under rule 2 it is not the agent's to make.

## What that produced on the first run

| Scenario | Assumes | Months to zero cash |
|---|---|---|
| W12 | The last twelve months are representative | **18.8** |
| W6 | The last six months are | 16.2 |
| W3 | The last three months are the new level | 14.4 |
| **RUNOFF** | **Not one further logo is signed** | **13.2** |
| W12_PLANHC | W12, hiring to the April reforecast | 18.6 |

**Runway is 13.2 to 18.8 months, and the entire 5.6-month spread comes from the choice of estimation window.** Not a market view, not a price, not a hiring plan — which months of history count as representative.

Two readings fall straight out of the table.

**The hiring plan is not the question.** Hold at 33 heads versus hire to the April reforecast moves the runway by **0.2 months**. The window question is worth 4.4. The decision usually taken first is worth a fifth of the decision nobody has been asked.

**The floor sits below the front page.** RUNOFF assumes no new business at all — it is not a forecast and cannot be wrong about sales. It gives **13.2 months**. The Exec Summary carries **16.1** on trailing-three-month burn. The number a reader meets first is three months above the floor.

---

## The back-test, which goes above the headline and not below it

The engine re-runs itself as at an earlier date, on that date's history only.

| Horizon | Forecast | Actual | Error |
|---|---|---|---|
| +1 month | 368,930 | 395,692 | **−6.8%** |
| +2 months | 387,048 | 396,592 | −2.4% |
| +3 months | 404,937 | 395,269 | **+2.5%** |

Rule 5 puts this beside the headline at the same weight, not in an appendix: **a forecast issued without its own back-test is an opinion with a spreadsheet attached.** And the untested claim is stated as loudly as the tested one — the method has never been scored beyond three months, so the six-month figures carry no error estimate and the pack says so on the tab.

---

## Five of fifteen drivers cannot carry a forecast

### Two rates with no events at all — rule 4

`churn_rate::Club` and `churn_rate::Academy`: **zero churn events in eighteen periods.**

Not zero. **Unmeasured**, and emitted as such with the event count and the length of history that produced none. Both books are held flat because there is no basis to do otherwise, and the pack says in terms that **this is not a retention assumption and no lifetime may be computed from it.**

Forecasting zero churn forever is how a model produces infinite customer life. It is the same finding the SaaS tab reports as `n/a — no churn observed`, arriving from the opposite direction.

### Two levels where the window is the whole answer — rule 2

| Driver | 3m | 6m | 12m | Dispersion | Consecutive declines |
|---|---|---|---|---|---|
| Club gross adds | 4.3 | 7.8 | 10.7 | **2.46×** | **5** |
| Academy gross adds | 20.0 | 34.8 | 48.2 | **2.41×** | **7** |

Club runs 14, 13, 14, 11, 9, 7, 4, 2. Academy runs 64, 60, 57, 50, 42, 32, 21, 7.

**Neither series is noisy. Both decline monotonically toward zero.** There is no statistical answer to which window is right, because the disagreement is not statistical — it is a question about whether something changed, and the data cannot say. Escalated as FC-01, worth 4.4 months of runway, with the observation that pipeline, quota attainment and marketing spend would settle it in an afternoon and none of them is in a connected source.

### One mean that averages two states the business was never in — rule 3

`gross_adds::Player`: three-month mean **964.3**, and the three months it averages are **2,893, nil, nil.**

Dispersion across windows is a tame **1.15×** — which is exactly what makes it dangerous. **The instability is inside the window, not between windows, and a dispersion test alone passes it.** That is why the engine also measures the shortest window's own composition: minimum, maximum, and how many of its months contained no event.

Rule 3: a period with no event is not a low reading, it is the absence of one. Two consecutive months of zero gross adds against ~390 monthly churn in a live consumer subscription is **a fact about the data feed before it is a fact about the business** — and it is said in that order. This is **defect 23**, arriving independently from the forecast side.

---

## What the charter forbids

Eight rules. The three that carry the most weight:

**Rule 6 — a scenario is a driver change, not a percentage on the answer.** *"Downside"* is not a scenario. And the labels are banned outright: **conservative, prudent, stretch, base, realistic** describe how somebody feels about a number and conceal what was changed to produce it. Each scenario is named for the assumption that distinguishes it.

**Rule 7 — the forecast is not the plan and does not become the plan.** It reconciles; it is not anchored. And it does not recommend: *a forecast that recommends is a forecast with an interest in its own outcome.*

**Autonomy: L0, draft-only, permanently — and the reason is not the instance count.**

> Every other agent here can be promoted because something downstream refuses to balance when it is wrong. Nothing refuses to balance here.

A forecast is a claim about a period that has not happened, addressed to people who will make irreversible decisions on it. The back-test that catches a wrong one arrives after the decision. The twelve-a-year cadence makes the 200-instance floor moot anyway, but the charter says explicitly that **the floor is not the reason**, so that nobody later reads the volume as the only obstacle.

One narrow class is promotable: the driver register alone — measurements of history, no scenario, no projection, no sentence about the future.

### And the pressure this will fail under

Rule 7's closing note names it, because it is not the failure mode people expect:

> *The pressure on a forecast is not a request to change a number; it is a request to **include** something — a deal in late-stage negotiation, a hire already verbally accepted, a price rise agreed but not papered. Each is real, each is knowable, and each is a driver value with no measurement behind it. The line between a forecast and a wish is one signature, and the request will always be to cross it a fortnight early.*

The answer is not refusal: an unmeasured driver enters as a **named scenario with its author recorded**, never as an adjustment inside the base view. *"It will be tested in month two, and by someone who is right."*

---

## What changed in the pack

An eighteenth tab, **Forecast** — back-test first, then scenarios with the runway spread as a formula, then the full driver register with unusable drivers ambered, then the omissions, then the cash-path chart. Everything on it is amber, because it is an extract from another agent's artefact, and it carries `DRAFT — NOT RATIFIED` on its face.

**And two things the pack used to say became false, so they changed.**

The cover read *"No forecast exists."* It now reads *"The only forward view in this pack is agent-produced and UNRATIFIED. No management forecast has been refreshed since April 2026."* The distinction matters: the company still has no forecast, and an agent draft is not one.

The Exec Summary's decision 3 moved from *"commission a forecast"* to *"ratify or reject the draft forecast"* — with the sentence that its runoff floor is below the runway on the page above it.

## What is not forecast, and why the cash line is a direction not a date

Rule 8 requires the omissions to be listed, because **an omission that is not listed reads as a nil, and a nil is a claim.** Usage overage and credit packs (no forward basis ruled, SL-08), tournament revenue (non-recurring, and the largest single mover last month), expansion and contraction (NOT OBSERVABLE, SL-24a — so the forecast understates any book that expands), VAT (no account, SL-13).

And working capital, which is the one that matters for how the runway is read: **the cash path is operating income only.** Deferred revenue and payables timing moved cash $162,549 in July alone. The difference between this and a treasury forecast is the difference between a direction and a date, and a reader looking at "13.2 months" will not make that distinction unless it is put in front of them.

Revenue is on the **contracted book basis**: 395,269 a month against 386,443 of recognised recurring revenue in the P&L, **+2.3%**, from price leakage and recognition timing. Stated as a reconciliation rather than adjusted away.

---

## Defect 29, found by the loop while filing the loop entries

The two reviewer-found defects were filed as review-ledger entries RL-0036 and RL-0037 — the first entries in the ledger with `found_by: human review`. Filing them dropped improvement-loop closure from **100% to 90%**, and the scorekeeper named why.

Two of my references did not resolve. One was a wrapped comment — the identifier spanned two lines and the resolver correctly refused it. The other is the interesting one:

**RL-0035 pointed at a docstring line that the v2 rewrite deleted.** The correction is still in force — the P&L's shape does come from config — but the artefact that proved it had been rewritten out from under the reference.

That is a lifecycle hole the ledger design did not anticipate. **A route is checked for existence at the moment it is written and never again, so any refactor can silently unresolve a closed correction** and nobody would know unless the scorekeeper happened to be re-run. Re-pointed at `mapping.json`, which is where the rule now lives, and recorded as defect 29.

The loop is back to **21 of 21, 100%** — and this time the number means something it did not mean an hour ago.

---

## Verification

Every figure quoted in the forecast pack was re-derived from the engine's CSVs and checked: twelve claims, twelve matches, plus the three spread arithmetic claims (4.4, 5.6, 0.2 months). The reporting pack recalculates at **3,898 formulas, zero errors, 171 check cells all zero**, every statement line still reconciled to the answer key, 89/89 generator checks. `grep` for this company's vocabulary in `forecast.py` and `forecaster.md` returns zero.

## Carried forward

- **FC-01** is the escalation that matters: did new business change in the last two quarters? It is worth 4.4 months of runway and nobody has been asked.
- **Defect 29** — routes should be re-resolved on every scorekeeper run, not only when written. They now are, by accident; the check should be deliberate.
- The board deck's slide 7 still reads NOT PRODUCED for *forecast vs prior forecast*, and correctly: there is no prior forecast to compare to. The second run is the first one that can populate it.
- Remaining: the Controller, the Day 9 recording, and Day 10 packaging including the one-page lead artefact.
