# 86 — Arcline AI: the second instance

*Built 25 Aug 2026. A complete synthetic finance function for a US B2B AI SaaS company, built as a
second test instance for the agentic close-and-analyse workflow. Delivered to
`C:\Users\jonat\Downloads\Arcline-Finance`. The generator travels with it in `_generator/`.*

---

## Why a second company

Doc 75 §2 made the case for portability by scrambling one company's file names, and was explicit
that it was doing so *because a second company would cost a second company*. This is that second
company. It is not a rename of CourtIQ; it is a different business with a different revenue
model, a different cost structure, a different set of failure modes, and a different set of things
the data cannot answer.

The padel instance is EUR-denominated, club-and-consumer, seasonal, usage-metered per match, with
tournament revenue and credit packs. Arcline is USD, B2B-only, page-metered, with model-API cost of
revenue, a UK subsidiary, capitalised internal-use software, and multi-year prepayments. **Anything
in `package/` that runs on both is portable in a way the scramble harness cannot prove.**

---

## The company

**Arcline AI, Inc.** — Delaware C-corp, San Francisco, founded June 2021. AI document and contract
intelligence for insurance, logistics, healthcare, lending and legal operations. Platform
subscription with an included monthly page allowance, metered overage above it, implementation
services. Subsidiary **Arcline AI UK Ltd**, London, cost-plus 8%, EMEA contracts papered there from
July 2025.

| | |
|---|---|
| FY2025 revenue | USD 17.89m |
| FY2025 gross margin | 72.3% |
| FY2025 adjusted EBITDA | USD (8.32m) |
| Committed ARR, 31 Dec 2025 → 31 Jan 2026 | 17.60m → 18.30m |
| Headcount, 31 Dec 2025 | 94 |
| Cash, 31 Jan 2026 | USD 25.4m |
| Series B | USD 24.0m, closed 20 Feb 2025 |

**Where the clock is:** early February 2026, business day 6. The January close is **open and
unsigned** — six blocking steps outstanding, three exceptions raised. `08-reporting/FY2026/` is
empty on purpose; producing it is the task.

---

## What is in the folder

140 files, 5 MB, thirteen periods of actuals (2025-01 through 2026-01).

```
00-company/          CoA (100 accounts), 18 cost centres, 2 entities, 25 JE types, policies,
                     close calendar, delegation of authority, systems inventory, data dictionary
01-lrp/              FY26-FY30 base and downside, 22 levers with owner / status / written basis,
                     four marked OPEN. XLSX with the assumptions tab isolated.
02-budget/           FY2026 annual plan monthly by account and by cost centre, hiring plan, capex;
                     FY2025 plan. Year one of the LRP *is* the budget, by construction.
03-actuals/          9,300 GL lines across 4,500 balanced entries; AP at vendor level, AR at
                     customer level, bank, payroll, usage, ARR schedule and waterfall, deferred
                     revenue rollforward, capitalised software register, fixed assets,
                     commission calculation, bonus attainment, post-close inbox
04-month-end-close/  twelve closed months with signed sign-offs; 2026-01 in mid-flight —
                     34-step checklist with status and exceptions, JE log with approver and
                     attachment columns, accrual and prepaid schedules, seven reconciliations,
                     open items, an unsigned sign-off, an empty flux file
05-lbe/ 06-forecast/ the process documents and the Q1 input file
07-contracts/        136 customer agreements with an effective-dated MRR change log (188 events),
                     amendments, 12 full order forms; 81 vendors, 34 software agreements with
                     licences-purchased vs licences-active, 14 vendor packets
08-reporting/        FY2025 board pack. FY2026 empty.
09-metrics/          15-entry metric registry (3 UNRESOLVED), mapping.json in the package's shape
99-answer-key/       SEALED. 25 planted defects with expected values and how each is findable.
_generator/          the code, deterministic and re-runnable, plus a 25-check validator
```

---

## What ties to what

One general ledger. Everything else derives from it and nothing is a second opinion about it.
`_generator/validate.py` reads the **output files**, never the generator's working numbers, and runs
25 checks: every entry balances, debits equal credits, the TB nets to zero in all thirteen periods
and ties to the GL account-by-account, the balance sheet balances in every period, P&L subtotals
foot and tie to the GL, the ARR waterfall ties, the subledgers foot to their control accounts within
band, every account / cost centre / JE type used is defined, and three planted issues are spot-checked
as present. **25 of 25 pass.**

The lever that makes this hold: non-payroll expense targets are set at account-month level and then
*allocated* to real vendors in proportion to their spend profile. Vendor-level detail is therefore
correct by construction rather than by reconciliation.

---

## The January variance, by design

| | Actual | Plan | Variance |
|---|---|---|---|
| Revenue | 1,795 | 1,844 | (49) |
| Cost of revenue | 578 | 476 | (101) |
| **Gross margin** | **67.8%** | **74.2%** | **(6.4) pts** |
| Research and development | 1,111 | 931 | (181) |
| Sales and marketing | 611 | 812 | 201 |
| General and administrative | 726 | 700 | (26) |
| Total operating expense | 2,449 | 2,443 | (6) |
| **Operating result** | **(1,226)** | **(1,071)** | **(156)** |

The shape is deliberate. **Total opex is flat to plan and every component is wrong**, because a
USD 215,000 reclass with no support, self-approved, posted 9 February into the January period, moved
money from S&M demand generation to R&D research compute. An engine that reports "opex on plan" has
read the subtotal and stopped.

The gross margin miss is three things pulling in two directions: a December accrual that was never
reversed (+48.8k), model-training GPU capacity charged to cost of revenue (+88.5k), and an AWS
accrual booked at the prior month's amount (−31.6k). Correct all three and the variance flips
favourable — which is the point.

---

## The 25 planted defects

Grouped by what they test, not by severity:

**Arithmetic and completeness** — duplicate vendor invoice; stale accrual; accrual never reversed;
AP cut-off (four late invoices in the post-close inbox); missing Q4 commission accelerators;
unreconciled bank difference carried three months.

**Classification** — training GPU in COGS; unsupported reclass; over-capitalised research project;
post-implementation cost capitalised; multi-year prepay entirely in current deferred revenue with
USD 45k routed straight to revenue.

**Contract-to-ledger** — billing that never followed an amendment; auto-renewal nobody tracked;
ramped deal carried in ARR at the year-two rate.

**Estimates** — bonus accrued at 100% of target against an 82% assessed attainment; intercompany
balance not revalued since September.

**Vendor and spend** — software renewed at a 42% uplift inside a closed notice window; shelfware on
two agreements; two live call-recording platforms; USD 128k of spend with no agreement on file.

**Judgement and narrative** — a usage cliff at one customer worth USD 456k annualised that nothing
flags; churn hidden by a same-month upsell; a favourable payroll variance caused by hiring failure,
three of the missing heads quota-carrying; sales tax never charged in states where SaaS is taxable;
a credit memo issued 3 February for a December SLA breach.

The key also names **three things that are true and unflattering and are not planted** — G&A at 36%
of revenue, burn at roughly half of revenue, revenue per head near USD 200k — because an engine that
reports those as data problems has a different defect from one that misses them.

---

## What this instance deliberately provides that the padel one does not

**An effective-dated MRR change log.** SL-24a on the padel instance is UNRESOLVED precisely because
the subscription record holds one row of current state per customer, so expansion and contraction are
not observable and NRR is NOT COMPUTABLE. Arcline ships `customer_mrr_changes.csv`: 188 events typed
New / Expansion / Contraction / Price uplift / Churn, each with `mrr_before`, `mrr_after`, effective
date and source document. The ARR waterfall is built from it and ties in every period.

This is a deliberate contrast, not an inconsistency. The padel instance tests **what a metric engine
does when the data cannot support the metric**. Arcline tests **whether it uses the data when it
can** — a book with a change log that still gets differenced into a net movement is a different
failure, and one nothing has tested yet.

---

## Open questions this raises for the package

1. **`unit_segments` and the `constants` block** (doc 75 §5) were built around three customer export
   files. Arcline exports one, with segment as an ordinary column. Both shapes need to work, and
   only one has ever been run.
2. **Two currencies and two entities.** The padel instance is single-entity. Consolidation,
   elimination and the plan-rate constant-currency ruling (SL-10) have never been exercised against
   an instance that has a subsidiary.
3. **The metric registry ships with three entries UNRESOLVED and none wired to an output column.**
   That is the correct starting state for an install, and it is what the Co-pilot's refusal
   behaviour (doc 74 §5) should be measured against on a company it has not seen.
4. **The sealed month protocol (doc 74 §7) is still not armed.** This instance is a better candidate
   for it than the padel one, because the answer key was written before any agent touched the data.

---

## Re-running it

`_generator/` is deterministic — one seed, no wall-clock reads. `python3 emit.py` rebuilds the whole
folder; `python3 validate.py` re-runs the 25 checks against the output. Changing a number in
`core.py`, `econ.py` or `plan.py` re-derives everything consistently, including the LRP, which is
computed from the FY26 plan rather than typed beside it.
