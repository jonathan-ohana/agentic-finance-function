# 79 — Playbook 78 v0.2, wired into the engine

*Written 24 Aug 2026 against `tools/drivers.py`. One row per red-line correction: what it changed, and whether a machine now enforces it or a person does. A playbook nobody can point at in running code is a document; this is the map that stops it becoming one.*

## The rule this map exists to enforce

A correction is either **computed** — there is a test in `explain()` that fails differently because of it — or it is **written** — it binds how the Analyst phrases something and no arithmetic can check it. Both are real. Pretending a written standard is enforced is how a charter rots, so the two are separated here and the written ones are named as written.

## The map

| # | Correction | Status | Where it lives |
|---|---|---|---|
| 1 | T&E benchmark: budget/head × **budgeted** headcount, preserving the headcount-vs-rate split | **computed** | `explain()` family `TRIPS`. The variance now splits into a headcount effect `(actual − budgeted heads) × budget rate` and a spend-per-head effect measured at actual heads. This corrected a live defect: the engine divided the plan by ACTUAL heads, which is precisely the absorption the red-line names. |
| 2 | T&E depth threshold 30% → 5% | **already in force** | `THRESHOLD = 0.05` in `variance_core.py`, applied to every account. The 30% figure never reached the code. |
| 3 | T&E behaviour is event-driven; check the calendar | **computed, weakly** | `TRIPS` scans the month's entries and, where one named counterparty carries more than 40% of the month across more than one entry, says so and defers to the calendar. On this instance travel posts as a single generic accrual with no counterparty, so the test correctly stays silent — the evidence is not there to make the claim. |
| 4 | Payroll: employee-level roster incl. future hires, five named drivers | **computed** | `explain()` family `HEADS`. Attribution order is hire timing → attrition → off-budget hire rate → salary change, each sized at the budget rate, with the residual named. "Cost per head" is now the answer of last resort rather than the first sentence. |
| 5 | Payroll failure modes: bonus accrual basis; benefits PEPM election mix | **computed** | Election mix is family `BENEFITS`, which reports enrolment, dependant-carrying heads and their share of the charge, then names what the enrolment file cannot account for. The bonus-accrual-basis case surfaces through the `HEADS` rate-effect branch, which distinguishes a per-head figure that MOVED from last month (a comp or accrual event) from one that is flat (hires landing off budget rate). |
| 6 | Payroll owner question in plain language | **written** | No computable test. Binds the Analyst's phrasing. |
| 7 | Professional fees are four sub-classes | **computed** | `SUBCLASS` map: `6030` recurring, `6020` milestone, `8030` flat-fee, `8040` seasonal. Each carries a numeric trigger and stays silent without one — a standing instruction pasted onto every legal line is the boilerplate the rewrite exists to remove. Seasonal fires only on a spike above 1.4× the median month; flat-fee only when the line is over. |
| 8 | Professional fees depth: $5k **or 5%** | **already in force** | The materiality floor is adaptive — `max(min(3000, plan × 0.15), 250)` — so it is a proportion on a large line and a few hundred on a small one. |
| 9 | "Subscription schedule", licences tied to the hiring plan, tiered headroom | **written** | Vocabulary and a forecasting rule. The tiered-headroom point has no instance data to test against; it binds how the Analyst builds the forecast, not how the engine reads the month. |
| 10 | Missed prepaid entry: >$50k annual → 12-month spread; a treatment mismatch is an artifact, not spend | **computed** | `PREPAY_FLOOR = 50_000`. Every AP invoice is now allocated evenly across the months its service period covers, so a twelve-month contract can no longer look like a one-month cost. Anything still above the floor in a single month after that spread is a single-month invoice of that size, and the commentary says to check the treatment before reading it as spend. |
| 11 | Software owner question reframed to renewal cost | **written** | Binds the Analyst's question, not the engine's arithmetic. |
| 12 | Depreciation: rate deterministic, **volume is a business story** | **computed** | New family `DEPREC` on `5040`. Splits the schedule rate from install volume: a volume variance is narrated as expansion pace with the cost of revenue that follows it; a rate variance at constant volume is named a data-integrity item and sent to the asset register. The draft's "never narrate" rule is gone, as too absolute to be true. |

## What the corrections cost, and what they caught

Wiring #10 exposed the reason a false finding had been surviving. The engine had been reading a **120,000 prepaid compute purchase** as a month's invoice and reporting a 51k under-accrual against a line whose whole variance was 10k. Categories now declare whether they post to expense in their service month, invoices spread across the periods they cover, and the accrual test only runs where the AP subledger is at least 85% of the account. One accrual finding survives across the whole month, and it is real.

Wiring #1 exposed a defect of the same kind in the opposite direction: the T&E line divided the plan by actual headcount, so a centre could be over-hired and the commentary would report only a rate problem.

Both were found by taking a correction seriously enough to implement it. That is the argument for the red-line loop, and it is worth more than the eleven corrections themselves.

## Still open

- **#3** wants an events calendar the instance does not have. Until one is declared, the test can only look at entry concentration, which this ledger's posting convention defeats.
- **#7** wants a flat-fee arrangement register for legal and a milestone schedule for consulting. Neither is declared, so both sub-classes currently narrow the question rather than answer it.
- **#9** wants a subscription schedule with seats, rates and renewal dates. `8070` and `6040` are read from AP vendors instead, which gives the names but not the seats — so the tiered-headroom rule cannot yet be checked.

Each of these is an instance declaration, not an engine change: the same shape as `ap_category_map.csv` and the driver map. They belong on the onboarding list, and they are the honest answer to "what would make this better" — more declared knowledge, not more inference.
