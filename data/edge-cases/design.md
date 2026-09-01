# 12 — Edge-Case Design (Fable #1 deliverable)

*Supersedes the twelve-candidate list in doc 10. Day 1 of the Aug 17–28 sprint. Final: ten designed cases + ambient conditions + two generator-level traps.*

## The ten cases, each testing a distinct failure mode

| # | Case | Failure mode it uniquely tests | Agent under test |
|---|---|---|---|
| 1 | Club upsell 4→10 courts, co-terminated end date | Semantic rule application to clean data — expansion vs. new when contract structure is ambiguous | Analyst |
| 2 | Federation contract, no countersignature date | Extraction on non-standard documents — escalate, don't guess | Ingestion |
| 3 | Italian chain 8→5 courts, CRM tagged "Closed Lost — Renewal" | Overriding a wrong human label — contraction vs. churn; trust hierarchy between systems and people | Analyst |
| 4 | Black Friday annual cohort at 40% off | Recognition timing + list-vs-actual — billing export misstates economics; deferred revenue unwinds over 12 months | Bookkeeper |
| 5 | Nov 2025 model swap, gross margin +9pts | Causal attribution — plausible wrong narrative (the failure-demo anchor) | Analyst |
| 6 | ~90 negative-margin Player accounts (15–25 matches/mo at flat €12.99) | Aggregation masking — healthy 68% blend hides toxic cohort; requires unprompted drill-down | Analyst |
| 7 | June tournament events | Run-rate contamination — one-off revenue and COGS leaking into baselines | Forecaster |
| 8 | Prepaid compute commitment at ~71% utilisation | Accounting-vs-economics divergence — P&L fine, forward risk not | Controller / Forecaster |
| 9 | 7 clubs "Closed Won" in CRM, never installed, never billed | Cross-system reconciliation — pipeline ARR vs. billing ARR | Analyst |
| 10 | Variance vs. WHICH plan — Jan 2026 board plan or Apr 2026 reforecast | Baseline ambiguity — two defensible answers to "vs. plan"; only one belongs in the board pack | Analyst / Reporter |

Cases 1 and 3 are not duplicates: #1 tests whether the semantic rule handles a *correctly recorded* ambiguous contract; #3 tests whether the agent *distrusts an incorrectly recorded* unambiguous one. Different muscle.

## Demoted to ambient conditions (in the data, no design slots)

- **FX** — falls out of EUR-billing/USD-functional automatically; tested via one constant-currency ask in the board pack.
- **Camera inventory → CapEx** — simplified to monthly install batches; mechanics, not judgment; per-unit depreciation dates were pure generator cost.
- **Duplicate vendor invoice (Mar 2026)** — stays planted (one line of generator code; visible routine catch for the Bookkeeper) but is commodity AP-tool territory, not a designed edge case.

## Added at generator level (cost no slots)

- **Headcount drift + EOR mess.** People are the largest cost line and the EOR structure was chosen for messy payroll, yet nothing tested it. Two traps: a September-planned hire who actually started in November (plan-vs-actual on the biggest cost driver), and a one-time termination fee buried inside a routine monthly Deel invoice (does the Bookkeeper read invoices or patterns?).
- **A data gap.** One month of partial usage logs (Apr 2025). Tests behavior on absent data: flag the hole or silently interpolate. Nothing else tests absence, and silent gap-filling is precisely the failure a skeptical CFO expects from AI.

## Failure-demo confirmation

Case 5 remains the front-runner; case 4 is backup. Sharpening: don't let the +9pts arrive clean — let the May 2026 consumer surge partially offset it so the margin walk shows roughly +6 net and the Analyst must decompose two overlapping drivers before the vendor-rate-change checkpoint catches the misattribution. A compound story survives casual review far better than a single-driver one.

## Coverage check

Every agent has at least two cases pointed at it: Ingestion (2, plus federation terms feeding 1), Bookkeeper (4, duplicate invoice, EOR trap), Analyst (1, 3, 5, 6, 9, 10), Forecaster (7, 8, 10), Controller (8, cash lumpiness from annual prepay — ambient), Reporter (10, constant-currency ask, the $4.30M/$4.68M/$4.92M ARR decision).
