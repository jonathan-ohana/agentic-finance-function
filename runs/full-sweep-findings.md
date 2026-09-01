# 27 — The full sweep: 239 contracts, 19 payroll invoices

*18 Aug 2026. Closing the coverage loose end from Day 4. Twelve agents across nine batches, working independently from the same charter.*

---

## Coverage, now complete

| | Extracted | Verdicts |
|---|---|---|
| Club contracts | **239 of 239** | 226 AGREES · 12 CONTRADICTED · 1 INCOMPLETE |
| EOR payroll invoices | **19 of 19** | 19 AGREES, every line tying to the cent |
| Customer invoices | sampled, not swept | the subledger already holds them; PDF extraction is verification, not capture |

Output: `data/ingested_contracts.csv` (239 rows, 64 fields), `data/ingested_payroll.csv` (19 rows), `data/ingestion_escalations.csv` (142 escalations).

## Six new escalation classes

The first 48 documents produced four defects. The remaining 191 produced six classes nobody had considered — and unlike the first batch, most of these are not generator bugs. They are the kind of thing that is wrong in real companies.

**1 — Two billing cadences collapsed into one field.** Every agreement has two: platform fees *in advance* (annual or quarterly, clause 6) and overage *quarterly in arrears* (clause 4). The ledger's single `billing_frequency` records only the first. For the annual-prepay clubs, a quarterly arrears obligation is therefore invisible to anything driven off that field — deferred revenue release, period-end accrual, cash forecasting, collections. **This is a data contract defect, not a data error**, and it would have propagated silently into the Controller's 13-week forecast.

**2 — The customer key is not a key.** Fifty-two club names are shared across two to five separate contract records. `club_name` reads like an identifier and is not one. Three agents found this independently, one by noticing three separate contracts all called "Padel House Faro" with different terms and no cross-reference. Any metric keyed on name — logo count, churn, NRR, cohort, concentration — either merges unrelated clubs or splits one club into several. **Ingestion cannot fix this**: the contracts cite a free-text client name and never a customer ID.

**3 — Concurrent agreements with no supersession.** Several clients hold two live contracts with overlapping terms, different court counts and different minimums, neither referencing the other. Set Point Valencia has 8 courts to July 2027 and 4 courts to July 2028. Two sites, a renegotiation that should have replaced the earlier contract, or a duplicate — and the three readings give different contracted revenue, different deployed hardware and different shortfall exposure. Every agent that found one refused to decide which governs, as the charter requires.

**4 — Nobody watches the renewal notice window.** CLB-0113 expires **on the day of the sweep**. Its 60-day non-renewal notice deadline passed on 19 June. The ledger still shows zero renewals and no renewal document exists. The contract has either auto-renewed for another year or ended today, and neither state is recorded. Ten more contracts in one batch alone sit in the same position. The agent's phrasing: *"the state change passes silently on the day it occurs. Every evergreen contract in the estate carries the same exposure."*

**5 — The template contradicts itself on minimums.** In every "no minimum" contract, clause 3 states that none applies while clause 7 still requires payment of "any minimum shortfall calculated on a pro rata basis" on termination. Boilerplate that was never conformed to the variant — either dead text or an unquantified termination charge held nowhere. Found in four separate batches.

**6 — AGREES means less than it looks.** Raised by three agents unprompted: the ledger holds no field for unit price, allowance, allowance reset, overage rate, overage cadence, renewal notice or payment terms. Two of the charter's own six material terms have no ledger counterpart. So *"AGREES" means the document agrees with the five fields the ledger stores*, not that price is confirmed. A mispriced contract would pass this sweep undetected.

That last one is the most valuable output of the entire exercise, because it is an agent auditing the limits of its own verdict.

## The payroll invoices

Nineteen documents, every line tying to the ledger — and seven escalations that are all timing and control observations rather than errors:

**DEEL-202604 is the only invoice with a fourth line** — the $8,400 separation settlement, with the employee reference withheld. The ledger records it correctly but with nothing marking it non-recurring: *"absorbed into payroll it overstates the April run-rate by 8,400 and, if carried forward, inflates forecast payroll by USD 100,800 a year."* The planted trap, found by shape rather than by amount.

**DEEL-202608 is dated thirteen days in the future**, for a service period that has not elapsed, on an invoice whose own footer says charges are billed in arrears — with amounts identical to June and July to the cent. *"It reads as an estimate or rolled-forward accrual carrying an invoice number, not an actual."* That is a genuine accrual-versus-invoice distinction nobody asked the agent to look for.

**Employer costs are exactly 31.200% of gross on all nineteen invoices**, across nineteen months and headcount from 14 to 25. *"A rate constant to three decimals over that span is modelled, not computed; no true-up has ever appeared on the series."*

And a control observation: **payment terms are net 5 days while the query window is 10** — payment falls due five days before the right to dispute expires.

## What this settles about the charter

**Material correction rate: zero across 258 documents.** No extraction had to be corrected. Every finding landed on the documents or the data contract.

Against doc 19's promotion criteria — 200+ instances, correction rate under 2%, escalation recall 100% — the Ingestion agent now **clears the bar for L1**, on synthetic documents. That qualifier matters and is recorded: three templates are far more uniform than any real corpus.

The behaviour that produced everything above came from the prohibitions, not the instructions. Nine independent agents, no coordination, and not one of them made a document agree with the ledger.

## What Day 5 now inherits

The semantic layer has to rule on five things this sweep surfaced, none of which were on its list:

1. Which billing cadence `billing_frequency` means, and how the second one is represented
2. Whether a client name identifies a customer, and what does if it does not
3. Whether two concurrent agreements are one customer or two — a definition, not a data problem
4. Whether "no minimum" and "minimum of zero" are the same thing
5. What "AGREES" is allowed to assert when half the material terms have no ledger field

And the data contract needs six new fields before the Analyst can use any of this: unit price, allowance, allowance reset, overage rate, overage cadence, payment terms, plus a customer key that is actually a key.
