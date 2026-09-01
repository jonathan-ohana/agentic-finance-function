# 43 — The pack rebuilt: seven objections, six corrections and one question

**Date** 18 August 2026 · **Status** rebuilt and verified · **Prompted by** a seven-point critique from Jonathan

> *"The excel is not investment banking pedigree. Not sleek enough. Looks unfinished."*

Six of the seven were corrections. One was a question I had never answered, and it is the one that matters strategically. Taking them in the order they were given.

---

## 1 · Not investment-banking pedigree

Conceded. The rebuild is thirteen tabs against nine, with gridlines off, print titles and fit-to-width page setup on every sheet, tab colours grouping statements from extracts from analysis, hairline rules under detail lines and a double rule under totals, number formats that render a zero as an en dash and a negative in parentheses, and a cover that states what every colour means before the reader reaches a number.

That is presentation, and presentation was the least of it.

## 2 · Blue is wrong for a ledger posting

**A correction, and the sharpest one.**

Blue means *an assumption you may change to drive the model*. A ledger actual is not an assumption. Colouring it blue invites a reader to overwrite a fact, and it tells them the model has an input where it has a posting.

The convention now reads:

| | Means |
|---|---|
| **Blue** | A human input. Board goals and the FX rate a plan was built at. **Nothing else.** No actual is ever blue. |
| **Amber** | An extract from a system of record, on the three `Data_` tabs. The only hardcoded actuals in the workbook. |
| **Black** | A formula computed on the sheet you are looking at. |
| **Green** | A link to another tab in this workbook. |

There are exactly **eleven blue cells** in the whole pack: ten quarterly goals and one plan FX rate. The rate is one cell, and the other seventeen periods reference it — an assumption that can be changed in one month and not another is not one assumption. Everything else is amber, black or green.

My use of blue in v1 was defensible only in the sense that those cells genuinely *were* hardcoded. Which is point 3, and the real fault.

## 3 · The numbers should be linked to something

**This was not a formatting objection. It was the architectural one, and it drove the rebuild.**

The pack now separates **extract** from **schedule**:

```
Data_TB      general ledger trial balance    ← the only hardcoded actuals
Data_Ops     segment volumes, headcount      ← extract
Data_Plan    plan lines by version           ← extract
─────────────────────────────────────────────────────────────
everything else                              ← formulas onto those three
```

`Data_TB` holds one block of movements per account per period — 55 accounts × 18 periods, amber. Beneath it, closing balances are a **formula roll-forward**: opening plus movement, for every account, including a retained-earnings row that accumulates the P&L. Both blocks carry a check row that must read zero, because a trial balance that does not balance is not a trial balance.

**2,593 formulas. Three extract blocks. Nothing else in the workbook is a number.**

### The answer to the question you actually asked

> *"Is it that we'll integrate agentic workflow with whichever system of record (QuickBooks, Salesforce)? How realistic is this? Integration might be complex to do."*

**Three honest observations, and then the position.**

**First: the API is not the hard part, and it is not where projects die.** QuickBooks, Xero, NetSuite, Stripe and Salesforce all expose a trial balance or its equivalent through a documented REST endpoint, and there are aggregators — Codat, Rutter, Merge — that normalise a dozen ledgers behind one schema for a few hundred dollars a month. Pulling account-by-period movement out of QuickBooks is a weekend. Anyone who tells a Series A CEO that ledger integration is a quarter of engineering is selling something.

**Second: the hard part is the mapping, and the mapping is not a technical problem.** The thing that takes weeks is not *getting* account 7040, it is knowing that 7040 is S&M rather than G&A, that payment processing sits in cost of revenue rather than below the line, that this company's "deferred revenue" spans two accounts and its "cash" spans three. That is a set of rulings about the business. No connector delivers it, and no model should guess it.

Which is exactly what `mapping.json` already is. The install-time work of this package **is** the mapping — the same conversation, whether the data arrives by API or by CSV. So the connector does not add a project; it removes a manual export from a project that has to happen anyway.

**Third: Office Connect is the wrong shape for this.** Live workbook links to a server are how a reporting pack becomes unauditable — the number changes under the reader and the version they signed is not the version they open. **A close is a point in time.** The pack should be built against a dated extract, and that extract should be part of the evidence. `Data_TB` is that extract, stated on its own tab, with the connector's status printed above it.

**So the position is:**

> **Ship file-drop first, and make the connector a swap rather than a build.** The extract tabs are the contract. Today they are populated from a CSV export; a connector populates the same tabs from the same accounts on the same schedule, and *no other tab in the workbook changes*, because no other tab holds a number.

The Lineage tab now carries a connector-status block naming each system of record, what it delivers, which tab it feeds, and whether it is connected. One row reads **NOT CONNECTED** — the payment processor — and its note says why that is a disclosed gap and not a pending integration:

> *Funds in transit is asserted by the ledger with no processor statement behind it.*

That is the same discipline as the rest of the package: a thing that cannot be verified says so on the face of the artefact, and does not quietly become a thing that was verified.

**And the realism claim, stated narrowly:** a Series A finance team can have the ledger and the billing system feeding this within a fortnight, most of it spent on the chart-of-accounts mapping and none of it on the API. A team that says otherwise has usually been sold a data warehouse it did not need.

## 4 · A KPI tab tracked monthly against quarterly goals

Built. Ten KPIs across revenue, margin, cost, cash and operating volumes, each a link to a statement — thirteen monthly columns, then the quarter's aggregate, the goal, the variance, the variance percentage and a status.

Three properties are worth naming:

- **The goal is the only blue cell on the tab**, because a goal is the only thing on it a human sets.
- **A quarter with no goal reads `NO GOAL SET`, never zero.** An unmeasurable target is not a target met — the same rule the scorekeeper applies to metrics.
- **Status reads `QUARTER OPEN`, not `BELOW GOAL`, while the quarter is incomplete.** July is one month of Q3. A part-quarter judged against a whole-quarter goal fails by arithmetic, not by performance, and a status column that says `BELOW` for that reason is a column that trains its reader to ignore it.

## 5 · Detail behind R&D, S&M, G&A and COGS

Built, at the ledger account. Cost of revenue across eight accounts; operating expense across eighteen, grouped by function, each with month-on-month and percentage of revenue, each function total tied back to its P&L line by a check formula.

v1 stopped at the function line because that is where the plan stops. That conflated two different questions: *what can be compared to plan*, and *what can be seen at all*. The plan comparison still stops at the function. The detail does not.

## 6a · The revenue bridge is weak — volume or price?

**Conceded, and the fix is the most useful thing in the rebuild.**

A plan-to-actual bridge with one residual bar says nothing about why the actual moved, and this plan states totals with no units, so no volume leg can be isolated against it. That limitation is real and stated. But it is a limitation of the *plan*, and I had let it stop me decomposing the **actual**, where units do exist.

The month's own movement now splits three ways, per segment:

| | |
|---|---|
| volume | (V₁−V₀) × P₀ |
| price | (P₁−P₀) × V₀ |
| mix | (V₁−V₀) × (P₁−P₀) |

Those three sum to V₁P₁ − V₀P₀ **identically**, so the check column is zero by construction. That is the point: a decomposition that needs a plug is not a decomposition.

### What it found on its first run

| Segment | June | Volume | Price | Mix | July |
|---|---|---|---|---|---|
| Club subscription | 161,166 | +975 | +1,015 | +6 | 163,162 |
| Player subscription | 185,956 | **−4,597** | +682 | −17 | 182,024 |
| Academy | 40,699 | 0 | +558 | 0 | 41,257 |
| Usage overage | 36,340 | **+11,944** | +2,756 | +906 | 51,946 |
| Non-segment | 137,668 | *n/a* | *n/a* | **−118,599** | 19,070 |
| **Total** | **561,829** | **+8,322** | **+5,011** | **−117,703** | **457,459** |

**The entire July revenue decline is non-segment.** Every unit-bearing segment grew. The $104,370 fall is $118,599 of credit packs, events and refunds moving, against $13,333 of genuine growth across the four subscription lines.

That is a materially different sentence from "revenue fell 8.9%", and no version of this pack could produce it before.

**And the non-segment movement is stated whole, in its own column, labelled `Unclassified movement`.** It is not folded into mix. Credit packs, events and refunds carry no unit the semantic layer has ruled, so they carry no volume and no price — and putting a residual in the mix column would make it look like an explanation. Same principle as the Analyst's rule 3, in a different place.

## 6b · Everything in the cash statement should link to the P&L or the balance sheet

**Correct, and now true of every line.**

| Line | Derived from |
|---|---|
| Net income | `'P&L'!` net income |
| Depreciation add-back | `'P&L'!` cost-of-revenue depreciation, negated |
| Every working-capital line | the difference between two balance-sheet columns |
| Capital expenditure | balance-sheet fixed assets and inventory, net of the depreciation already added back |
| Equity issuance, debt | balance-sheet equity and debt movements |
| Opening cash | the prior balance-sheet column |
| Closing cash | opening plus net change |

**Nothing on the cash flow is typed.** Which required the balance sheet to gain a fourteenth column — the opening comparative — because a cash flow made of differences cannot compute its first period without one.

The consequence is worth stating precisely, because it is stronger than "the check passes":

> The articulation check is **zero by construction, not by luck**: the sum of every balance-sheet movement is zero because the balance sheet balances, and this statement is a rearrangement of exactly that sum.

## 7 · QoQ and YoY were wrong

**Conceded outright. They were month-on-month arithmetic wearing quarterly labels** — v1's "QoQ" compared the current month to three months earlier.

QoQ is one quarterly aggregate against the preceding quarterly aggregate, and it means something only once the quarter is complete. YoY is the like quarter of the prior year. A new **P&L Quarterly** tab does both, and does two further things:

**It suppresses rather than misleads.** July is month one of Q3 2026, so QoQ and YoY are computed on **Q2 2026**, the last complete quarter, and the banner says so:

> *QoQ AND YoY ARE SUPPRESSED FOR 2026-Q3 — the quarter is incomplete (1 of 3 months)... The final column is 2026-Q3 to date; it is not a quarter and nothing is computed from it.*

That column is greyed, and no growth rate references it.

**It reads the trial balance rather than the monthly P&L tab**, because Q2 2025 — the prior-year comparative — lies outside the thirteen months that tab displays. A YoY built only from what is on screen is a YoY that quietly changes meaning when the window moves. Twenty-six check formulas tie the quarterly sheet line by line against the monthly tab for the quarter they share: two independent paths to the same figure, both reading zero.

---

## Verification

**2,593 formulas, zero errors — and that is the weaker of the two claims.**

A green recalculation proves formulas *evaluate*, not that they are *right*. That lesson cost a cash flow that articulated to $573,366 of nothing while reporting zero errors. So every figure was checked against the answer key independently of the recalculation:

- **119 numeric check cells across nine tabs, all reading zero** — trial balance both blocks, balance sheet, cash articulation, revenue against the P&L, the three-way decomposition, each cost function against its P&L line, three bridge ties, and the quarterly-against-monthly tie.
- **Every P&L line, every balance-sheet line and the cash flow reconciled to the answer key** for all thirteen periods. Two differences, both presentation and neither an error: gross margin is stored as a fraction, and operating expense is stated negative throughout the pack.

### And the check found a defect the recalculation could not

**The Revenue and KPI tabs read the volume extract five columns out of position.** `Data_Ops` is built on the eighteen-period extract grid; both consuming tabs indexed it on the thirteen-month display grid. Every implied price on the Revenue tab was revenue divided by a volume from five months earlier.

It recalculated with **zero errors**, because the shifted columns still held numbers. Three of four segments produced plausible prices. The fourth divided by zero and left a text cell, which is the only reason it surfaced at all.

This is the $573,366 failure again, in a different tab, and it is worth saying plainly: **a workbook can be entirely formulas, tie on every check, recalculate clean, and be wrong**, if two sheets disagree about what a column means. The check that caught it was reading the numbers and asking whether they were the right ones.

---

## Defect 20, found on the way and not fixed here

`package/variance.py` still names this company's segments — `clubs`, `players`, `academy` — in its bridge construction and its unit builder. Same defect class as the one already conceded in the reporting engine: **a bespoke script wearing a package filename.**

It is recorded rather than quietly fixed because fixing it changes the Analyst's outputs, which would need re-running and re-verifying. The segment declaration it needs already exists in `mapping.json`, so the fix is the same shape as the one just applied here.

---

## What changed in the package

| | |
|---|---|
| `package/reporting_pack.py` | rebuilt — extract/schedule separation, corrected colour convention, correct quarterly logic, cost detail by account, KPI tab, three-way revenue decomposition, fully linked cash flow, IB page furniture |
| `example/mapping.json` | `reporting` gains `connectors`, `pl_structure`, `bs_structure`, `cf_structure`, `cost_detail`, `kpis`, `quarterly_goals`, `cash_lines`, `headcount_functions`, `non_segment_revenue_lines` |
| `package/charters/ingestion.md` | one illustrative example de-instanced |
| `build_deck.js` | every citation re-pointed at the new cells and the deck rebuilt |

**The engine knows nothing about this company.** Statement shape, account mapping, cash-flow derivation, segments, cost groupings, KPIs and goals are all declarations in the install's mapping file. Add a company there; do not edit the engine.

---

## Carried forward

- **Defect 20** — `variance.py` still knows this company's segments.
- The pack has no forecast column, because no forecast exists. In a management pack of this shape that column is the third of three; here it is absent by fact.
- The three-way decomposition works on the actual because units exist there. It still cannot run against plan, because neither plan states units — the same wall the Analyst hit, now visible in two places rather than one.
- The **−$118,599 of non-segment movement** is the largest single driver of July revenue and has no explanation on file. It is a better-specified version of the −$101,030 question already open, and it now has a number attached to a category rather than to nothing.
