# 51 — The club churn plant: an objection I had never tested

**Date** 19 August 2026 · **Status** planted, regenerated, verified · **Source** Fable audit doc 49 §6

Fable's only dataset recommendation: plant two or three club churn events. I had refused the same class of change twice — for defect 23 — on the grounds that regenerating would invalidate the loop evidence, which is the portfolio.

**I had never measured it.** When I did, the objection did not hold.

---

## The measurement

Prototyped in a scratch copy, regenerated, and diffed every file.

**Byte-identical after regeneration:**

`customers_players.csv` (19,065) · `customers_academy.csv` · `ingested_contracts.csv` (240) · `ingested_payroll.csv` · `ingestion_escalations.csv` (143) · `bookings.csv` · `headcount.csv` · `payroll_us.csv` · `payroll_eor_invoices.csv` · `pricing_configuration_drift.csv` (2,704) · `_manifest_edge_cases.csv` · `chart_of_accounts.csv` · `fx_rates.csv`

**The twelve-agent sweep over 673 documents — 226 AGREES, 12 CONTRADICTED, 143 escalations — survives untouched.** That was the entire objection, and it was wrong.

The reason is that the generator is fully seeded and already carries a **mutate-by-ID** pattern for edge cases: the upsell, the downgrade, the cadence anomaly and the federation contract are all applied by picking a record *after* creation. Planting churn the same way perturbs three clubs' revenue and nothing in the random stream.

**What did change**, correctly: `customers_clubs.csv` (3 rows), `gl_journal.csv` (6,047 → 6,037 postings), the AR subledger, usage, the document index, and every answer-key statement.

---

## What it cost, and what it bought

| | |
|---|---|
| Committed recurring ARR | $4,743,222 → **$4,714,376** |
| Total revenue, July | $457,459 → **$452,529** |
| Gross margin | 69.5% → **69.4%** |
| Runway, trailing burn | 16.1 → **19.9 months** |
| **Club GRR, 12m cohort** | 100% *by absence* → **98.3% measured** |
| **Club LTV** | `n/a — no churn observed` → **$209,581** |
| Club churn rate | unmeasured → **0.29% / 0.14%** (3m / 12m), 2.10× dispersion |
| Runway range across scenarios | 13.2–18.8 → **13.8–19.0 months** |
| Indicative new capital | $3.28M → **$3.38M** |

**The story did not move.** Cash-out is still Apr-28, the raise clock is still Oct-27 / Jun-27, net new ARR is still −$45,241, and the burn multiple is still the most damaging number in the pack. What moved is that the dataset now survives the first question a Series A CFO asks.

Three clubs left: **Racket Center Barcelona** (4 courts, Feb-26), **Break Point Madrid** (8, May-26), **Set Point Lyon** (12, Jun-26).

---

## Three defects the plant surfaced

**43 · Four of five contract checks read `end_date` as an expiry.** Planting three terminations failed all four: renewed contracts have an end date in the future; term length agrees with the dates it is stated between; month arithmetic preserves the day of month; current term start is the expiry less the current term length.

None was wrong about renewals. All four assumed **no contract ever ends early** — which is exactly the assumption the dataset itself encoded. *A validation suite can hold the same blind spot as the data it validates, and this one did.* All four now exclude terminated contracts, and the distinction is written down: **a termination date is not an expiry date.**

**44 · The verdict hardcoded its verbs.** The Exec Summary's verdict is assembled with `TEXT()` off live cells — every *figure* in it is a reference. But "shrank", "held flat" and "accelerated" were typed. On the new dataset burn **fell 20%**, from $566,074 to $453,162, and the verdict still read *"Burn accelerated to $453,162."*

That is the precise failure this pack's whole discipline exists to prevent, in the one sentence on the front page that matters most. The verbs are formulas now:

> *"The recurring book **shrank** — churn removed $60,947 against $15,706 of new business; FX of $29,182 **did not cover it**. Burn **eased to** $453,162."*

A typed "thirteen consecutive months of decline" went the same way; it now counts.

**45 · LTV measured its churn rate on the current month alone.** So it read `n/a — no churn observed` in every month a B2B book happened not to lose anyone — which is most months. Club churn became measurable and LTV still refused, because July had no club closure.

Moved to a **trailing twelve-month** rate. It now refuses only when no event has been observed in a year. Same class as *a mean is not a level*: a rate measured over one period is not a rate.

**Only the plant could have surfaced any of the three.** Each needed a churn event to exist before it could fail.

---

## The correction to my own reasoning

I refused this twice, and both times the refusal was reasonable-sounding and untested:

> *"Regenerating would change every figure in the close pack, the variance pack, the review ledger's cited instances and the board deck — and the loop evidence in those artefacts is the portfolio, not the numbers."*

The second half is true. The first half was an assumption about a seeded generator I had written and could have measured in ten minutes. **The blast radius was a guess wearing a cost estimate**, which is the same fault the Analyst's rule 2 names about variance commentary — a claim that cannot be checked against anything else.

The rule that follows: **a cost used to refuse a change is a claim, and it gets measured like one.**

---

## Verification

**89/89 generator checks. 5,972 formulas, zero errors. 176 numeric zero-check cells all reading zero.** Every P&L, balance-sheet and cash-flow line reconciles to the regenerated answer key. Improvement loop **27 of 27, 100%** after RL-0044's reference was re-pointed at a line that had wrapped. Package purity zero.

Re-issued against the new dataset: the board deck's quoted figures, the forecast pack, and the SaaS retention section that had begun contradicting itself.

## Carried forward

- **Academy churn is still zero across 940 accounts.** Fable asked for club events and the club book was the load-bearing one, but the same argument applies here and the same fix is available.
- The forecast pack's back-test now reads −6.6% / −2.0% / +2.9% — marginally better than before, and still untested beyond three months.
- Remaining: the Controller, the Day 9 recording, and Day 10 packaging.
