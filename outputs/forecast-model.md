# 47 — The forecast model: from five projections to one model with a toggle

**Date** 19 August 2026 · **Status** merged and verified · **Prompted by** a marked-up pack from Jonathan

> *"Here's the reporting package with the forecasting elements updated. Please capture all updates."*

Eighteen tabs went out; twenty came back. Two new — **Assumptions** and **Valuation** — and the Forecast tab rebuilt from the ground up: 2,299 changed cells, a 24-month horizon against six, and a scenario toggle where I had five static projections.

All of it is now in `reporting_pack.py` and `mapping.json`. The engine reproduces the marked-up workbook **exactly** — every line, all twenty-four months, and the whole valuation — which is the only proof that the capture is real and not an approximation with the same headline.

---

## The architectural correction

I built the Forecaster to run five scenarios in Python and write five static projections. A reader could compare them and could **change nothing**.

The rebuild puts the driver set in the workbook. One **Assumptions** tab with Low, Mid and High side by side, and a toggle at `Forecast!B4` that resolves a single column through `INDEX`/`MATCH`. Every forward month reads the *resolved* driver, never the assumption directly.

That last detail is the one worth stating, because it is not obvious:

> **One resolution point; there is nowhere for a scenario to disagree with itself.**

With three scenarios hardcoded into three sets of columns, a driver changed in one place and not another is invisible. Here it cannot happen. Same principle as the plan FX rate being one cell rather than eighteen — an assumption that can be changed in one month and not another is not one assumption.

**And it is the difference between a forecast report and a forecast model.** A CEO who asks *"what if we freeze hiring"* now gets an answer by editing a cell rather than by commissioning a rebuild. That is what a Head of Finance is for, and my version could not do it.

## What the driver set holds

Twenty-eight drivers across acquisition, retention, pricing, non-recurring revenue, cost of revenue, headcount-driven opex, working capital, and one valuation multiple. Two properties enforce the discipline:

**Every typed cell is blue and carries a written basis naming its window.** Not *"1,031 player adds"* but *"Mid = six-month average (1,031). High = twelve-month average (1,104). Low is set at 200 — well below the three-month average of 964, which is distorted by the May 2026 surge of 2,893 followed by two months of ZERO."*

**Every cell that can be computed from the actuals is computed.** Salary per head is `=$C$73/$C$80` off the anchor block; the recognition factor is `=C57/(C56/12)`. An assumption that could have been measured is not an assumption — it is a guess with a licence.

Beneath the drivers sits an **anchor block** of twenty-eight actuals, every one a formula onto the statements, with a check row: the six opex lines less total operating expense per the P&L, which must read zero or *"the opex build does not reconcile and nothing downstream can be relied on."*

## What the model now does that mine did not

| | Mine | Rebuilt |
|---|---|---|
| Horizon | 6 months | **24** |
| Scenarios | 5 static projections | 3 live, one toggle |
| Working capital | **not modelled** — cash was "a direction, not a date" | DSO and deferred-revenue months, both driven |
| Interest income | not modelled | on opening cash, so it decays as cash does |
| Capex and depreciation | not modelled | asset roll-forward with a derived rate |
| Price uplift | not modelled | applied each January |
| Salary inflation | not modelled | applied each January |
| Capital requirement | — | peak shortfall plus six months' buffer |
| Valuation | — | EV/ARR with two sensitivity grids |

The conceded gap in my version — *"the cash path is operating income only… the difference between this and a treasury forecast is the difference between a direction and a date"* — is closed. The Assumptions tab says so on the DSO row, in the basis text, naming the previous version.

## The capital block, and the one design decision inside it

Cash runs to wherever the operating case takes it, **including below zero**, and the capital requirement is stated separately rather than plugged into the cash line:

> *A model that silently funds itself hides the very thing you are trying to see.*

On the Mid case: cash goes negative in **Apr-28** on **20 months** of runway; peak shortfall **$1,145,925**; plus six months of month-24 burn as a buffer gives **indicative new capital of $3,280,291**. **All three scenarios exhaust cash inside the horizon.**

## The Valuation tab

An ARR-multiple framework with a written argument for why it is *not* a DCF — and the argument is right on all three counts:

- Every projected cash flow in the horizon is negative, so a DCF would place 90%+ of value in the terminal value and the output would be **the terminal assumptions wearing twenty-four months of arithmetic**.
- There is no defensible WACC. No debt, no observable beta, no market cost of equity — any rate chosen is unfalsifiable, and the valuation would move more with that rate than with anything the business does.
- It is not how the round will be priced.

**The multiples are placeholders and the tab says so in capitals, twice.** Per-share figures are left blank because no fully diluted share count exists anywhere in the pack — *estimating one from the preferred and paid-in capital balances would manufacture precision.* That is the `null`-not-zero rule arriving in a valuation.

Two sensitivity grids. The second is the better piece of work: month-24 ARR against player churn × player gross adds, computed in **closed form** rather than by re-running the model, and carrying a check against the model's own answer at the centre cell —

> *a grid that cannot reproduce the model at its own centre is describing something else.*

It reads `tie — grid validated against the model`.

---

## Three defects found while capturing it

The engine had to reproduce the workbook exactly, and three times it did not. Each was mine.

**30 · The depreciation rate divided by the trial-balance *movement* row instead of the closing balance.** Gross deployed assets read as one month's additions, so the monthly rate came out at **3.2× instead of 2.9%** and the depreciation memo compounded to **$1.1M by month 24**. Cash at month 24 read **+$12.2M** where the correct answer is **−$1.1M** — a **$13.3M** error, in the direction that says the company does not need to raise.

Every check in the pack still passed. This is the third time in three days that a wrong *row reference* has produced a clean workbook with wrong numbers — after the $573,366 cash flow and the five-column Data_Ops offset. The pattern is now specific enough to name: **the checks in this pack verify that the statements articulate; none of them verifies that a cross-sheet reference points at the row it claims to.**

**31 · The model's header row wrote the first of the following month instead of the month end.** `eom()` returns 1 August for July — deliberately, because that is what date comparisons want — and I wrote it straight into the header. Every forecast month shifted forward by one, so **the January price uplift landed in February** and *month 12* was really month 11. The two questions now have two functions, and the reason is in the docstring.

**32 · Implied CAC divided by total S&M rather than S&M non-salary.** A salesperson's salary is capacity; the campaign is the spend that bought the logo. Mine read $364.71 against the correct $275.46 — a third too high.

## And two classification corrections

**The engine still knew the company.** `SEGKEY` mapped segment positions to driver names — `segs[0] → adds_club` — so the engine knew which driver belonged to which segment by *position*. Both are now declarations on the book segments, and the sensitivity grid reads its segment from config. `grep` for this company's vocabulary in `reporting_pack.py` returns **zero**.

**A business condition is not an integrity check.** My automatic sweep found the Forecast tab's `CHECK — cash balance non-negative` and reported **BREAK** on the Exec Summary integrity block, beside eleven build checks reading PASS. But the model's cash *does* go negative in Apr-28 — that is a true statement about the company, not a broken build. Renamed to `CASH CONDITION`, and the sweep now distinguishes three kinds of check:

- **zero-tests** (`=ROUND(...)`) — swept numerically
- **word-tests** (`ok` / `tie` / `BREACH`) — counted with `COUNTIF`
- **conditions** — not integrity at all, and reported as facts in the headline

The first version applied `MAX(ABS(...))` to all three and returned `#VALUE!` on two of them plus a false BREAK on a check that passes at 100%.

---

## Verification

**6,022 formulas, zero errors.** **176 numeric zero-check cells across fourteen checks, all reading zero.** Every P&L, balance-sheet and cash-flow line still reconciled to the answer key; 89/89 generator checks pass.

And the test that mattered: **every line of the monthly grid, across all twenty-four months, and every figure on the valuation tab, reproduces the marked-up workbook to the cent.** Zero differences. Before the three fixes there were 25 in the grid and 8 in the headline.

## What this means for the Forecaster's charter

The charter does not change, but the **split between engine and model** does, and it is worth writing down because it is cleaner than what I built:

`forecast.py` measures **drivers** — every window, the dispersion between them, the event counts, the composition of the shortest window. It does not project. The workbook holds the **model** — the scenario set, the roll-forward, the cash path, the capital requirement.

That respects rule 2 better than my version did. The engine says *"club gross adds are 4.3, 7.8 or 10.7 depending on the window, and here is how much they disagree."* The Assumptions tab is where a human writes down which one they chose and why, in a blue cell, with the window named. **The choice of window is a human's, and it now has a place to live.**

## Carried forward

- **The multiples are placeholders.** Nothing on the Valuation tab should be quoted until a named comp set replaces them, and the tab says so.
- The back-test still scores the *previous* engine, not this model. Carried because it is the only accuracy evidence that exists, with its limits stated rather than borrowed. The second monthly run is the first that can back-test this model.
- **Defect 30's class is now the standing risk in this pack**: a cross-sheet reference that points at the wrong row produces a clean workbook with wrong numbers, three times running. The next verification pass should test references, not just articulation.
- Remaining: the Controller, the Day 9 recording, and Day 10 packaging including the one-page lead artefact.
