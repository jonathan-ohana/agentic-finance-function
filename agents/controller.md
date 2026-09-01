# 53 — The Controller: the cash agent, and the four defects it found on the way in

**Date** 19 August 2026 · **Plan-day** 8 · **Status** shipped and verified

---

## Why this one, and not the recording

The red team's sharpest paragraph, from doc 29:

> *"The five agents that would actually produce what that operator asked for (Bookkeeper through Reporter, **including Controller, the cash agent**) are the five that do not exist. Every agent that has run is meta-work: agents that watch, audit, and schedule a finance function whose spine has never executed."*

The one real operator ever consulted asked for four things: **cash view, stable inputs only, usage excluded, compliance later.** The cash view was the first item on that list and the last thing built. Three artefacts still named its absence this morning — slide 6 of the board pack read `NOT PRODUCED — no Controller agent exists`, the forecast pack disclosed that its cash path carried no working capital, and the glossary listed the Controller as *not yet built*.

It is built.

---

## What `cash.py` is, and what makes it a different engine from `forecast.py`

`forecast.py` projects the P&L and derives cash from operating income. That path is a **direction**. It cannot be a **date**, because it contains no working capital — no receivable collected late, no payable held, no payroll that funds on the second of the month whatever the month before earned. In this company's July those timing effects moved cash by $162,549.

`cash.py` is **direct**. Every weekly figure resolves to an identified item — an invoice, a bill, a payroll run, a processor payout — or to a measured behaviour applied to one.

### The four refusals, in the docstring where they belong

**It will not plug the opening balance.** Opening cash comes from the bank record and is independently recomputed from the ledger. **The two agree to $0.00**, and if they had not, the difference would be reported as a difference. A cash forecast whose first cell is wrong is wrong in every cell.

**It will not collect an overdue invoice on the average day.** This is the piece of the engine I am most pleased with. An invoice raised sixty days ago is not going to be paid on day thirty-four — **that outcome has already been disproved by the fact that it is still open.** Applying the unconditional mean to an aged item pulls cash forward into weeks that observation has already ruled out, silently and in the flattering direction every time. Open items are collected on the **conditional tail** of the measured distribution, re-normalised over the days that remain.

And an item aged past the *whole* observed distribution is not quietly placed in week one. **$28,215 of receivables across 9 invoices, and $113,250 of payables across 19 bills, have no measured week at all** and are emitted as unplaceable with the reason. Week one is where an optimistic forecast puts the debts it has given up on.

**It will not forecast a line it cannot measure.** Zero is a forecast that a thing will not happen, and that is a claim. The $27,245 income-tax accrual has a real liability and no recorded payment date, so it is stated without a week — **not spread evenly, because an even spread would be an invention with a shape.** VAT has no account in the ledger at all.

**It will not net.** $1.26M arrives and $2.38M leaves. Week 12 nets to +$14,802 on $75,550 in and $60,748 out, and calling that a good week would describe neither fact in it.

---

## The finding: the grid is quarter-resolution and it says so above itself

The back-test re-ran the engine as at 30 April on the history available then, and scored it week by week against what the bank actually did through July.

| | |
|---|---|
| Cumulative error over thirteen weeks | **15.5%** — under-called the cash fall by $186,800 |
| Mean absolute weekly error | **$79,248** |
| Mean absolute weekly movement | $130,049 |
| Weekly error as a share of weekly movement | **61%** |
| Direction of the week called correctly | **7 of 13** |

**The two statistics disagree, and the weekly one governs how the grid may be described.** Over the quarter the instrument is directionally useful and about a sixth light. Over a single week it is close to uninformative.

This is the failure mode the charter was written around, and it is worth naming precisely: **a thirteen-week grid *looks* like thirteen weekly answers, because that is what a column means.** Nothing downstream catches it. The grid articulates to the cent, opening plus movements equals closing, every check reads zero — **and a receipt in the wrong week ties exactly as well as a receipt in the right one.** It is the only artefact in this workforce that can be wrong in a way invisible to arithmetic and visible to the bank.

So rule 1 puts the back-test **above** the grid, and the Reporter is forbidden from printing the grid without the sentence that says what resolution it has.

### And the failure is diagnosable

| Week | Error | What the bank actually did |
|---|---|---|
| 8 | **+$301,951** | $420,105 of supplier payments went out in **one week**. The engine had spread them across four. |
| 4 | **−$128,167** | $17,002 of supplier payments went out — near nothing. The engine had placed a normal week there. |
| 1 | **+$105,944** | Payroll funded at $387,328, above the measured level. |

**This book pays in batches; the engine pays on a distribution.** A measured lag curve is the right method for four hundred bills across a year and the wrong method for the particular fortnight in which eighty of them go out together. It is right about the total and wrong about the column — which is the same sentence as the back-test, arrived at from the other end.

The fix is not a tuned curve. It is the payment run itself as an input, and no connected system supplies it. **Named on Lineage as a connector gap rather than modelled around.**

### The window is worth $119,823, and it is not mine to choose

Every recurring level runs above its twelve-month average, and the grid is built on the twelve-month column.

| Level, per month | 3m | 12m |
|---|---|---|
| Payroll funding | (378,386) | **(317,249)** |
| Supplier billing | (521,838) | **(458,427)** |
| Invoicing | 214,044 | **172,197** |
| Processor payouts | 253,750 | **210,990** |

Re-running on the three-month window makes the quarter **$119,823 worse**. The back-test under-called the fall by $186,800. **The window choice accounts for about two thirds of the measured bias** — the same mechanism, measured twice, from two directions.

---

## Four defects, three of which exist only because a second engine was built

**Defect 37 — two engines, two opening balances.** `forecast.py` opens at **$7,937,626.42**; `cash.py` opens at **$7,911,300.72**. The $26,325.70 is account 1020, Stripe balance in transit — **cash to an accountant and unavailable to a treasurer**, who cannot pay a supplier with it this week.

Both are correct answers to different questions, and **neither engine was changed to match the other.** The difference is declared in the mapping and printed by both, under a rule that is now in the charter: *two engines that agree because one was adjusted have not been reconciled; they have been made to stop disagreeing, which is the opposite of a control.*

**Defect 38 — dispersion on signed values.** Every payment stream is stored negative, so `max/min` returned **0.838** for payroll's true 1.19× instability. A dispersion below one is not a value the statistic can take, and it was wrong on exactly the lines that matter, because every cost line is negative.

**Defect 39 — sized on 7.7 days, stepped on 8.** A weekly stream apportioned on the fractional measured cadence and stepped on the rounded one fits one fewer payout into the horizon than the monthly level implies, and loses ~3% of the line to a rounding convention nobody would look for. Found by checking the line total against level × horizon, not by reading the code.

**Defect 40 — the register was audited twelve times; the repository never was.** The document repository holds **709 PDFs. Its index lists 670.** Thirty-nine documents — 31 employee offer letters and **8 customer invoices** — are on disk and in no register, so they are invisible to every agent, because every agent reads the index.

This one is the keeper. The twelve-agent sweep that reported *239 of 239 contracts* was telling the truth about the index and could not have discovered the index was short. **A register is a claim about a repository, and this project had spent a week auditing the claim.** Found by counting the files.

### And the one-pager was wrong twice in one day

Worth writing down because it is uncomfortable. Yesterday's provenance line claimed **670 source documents**. This morning I could not trace it, "corrected" it to **3,601** — which is `data/document_index.csv`, the *transaction* index, a different file — and recorded in the scorecard that the 670 traced to nothing.

**It traced to `example/documents/_document_index.csv`, which has exactly 670 rows.** The original figure was right, the correction was wrong, and the note explaining the correction was wrong.

The artefact now reads **709**, which is the number of documents that exist on disk. The lesson is not that verification failed. It is that **verification against the wrong file is indistinguishable from verification**, and only counting the objects themselves settled it — which is also how defect 40 was found, in the same command.

---

## What the pack says

**Cash falls $1,125,480 over thirteen weeks to $6,785,821, and the low point is the final week** — the projection does not turn inside the horizon. Implied burn on the horizon $376,415 a month.

**It refuses to state a runway.** Thirteen weeks cannot produce one; annualising a quarter of measured collection behaviour gives a number of the same shape as a runway with none of its content, and it would be quoted, because it is the number everyone came for. Runway stays the Forecaster's single line, from the instrument built for it.

**It does cross-check.** The Forecaster's W12 puts cash at $6,611,113 on 31 October; this view puts it at $6,785,821 on 30 October — **2.6% apart on entirely different methods.** A corroboration, not a precision claim.

**And it states its own optimism.** Three of the six unforecastable lines have a known direction: they are payments. **The closing balance is light by at least $140,495 of identified amount plus an unmeasured VAT position**, before anything unknown.

Seven escalations, none resolved. The first is the sharpest: **payroll funded twice in August 2026** — the 2nd for July, the 17th for August, against twelve consecutive single-funding months. Either the cycle moved forward a fortnight, in which case every week of this grid is wrong by $378,154, or one is a duplicate and the money should not have left. The occurrence-per-month counter is the only reason it is visible at all; a monthly total cannot see it.

---

## Verification

**89/89 generator checks. 5,972 formulas, zero errors. Improvement loop 30 of 30 (100%).** Board deck rebuilt: **NOT PRODUCED cells 7 → 6.** `grep` for this company's vocabulary in `cash.py` and `controller.md` returns zero.

Three of the four new ledger entries route to a rule that now exists as a named line in the engine, and the fourth (defect 40) is **open**, routed to a validation check that has not been written yet. It is recorded open rather than closed because it is a real gap in the document repository and closing it means a generator change.

---

## Carried forward

- **Defect 40 open** — 39 unindexed documents, and the validation check that would have caught it.
- **Defect 20 still open** — `variance.py` and `kpi.py` name this company's segments. `cash.py` does not.
- **The payment-run connector** — the single change that would make the weekly columns mean anything.
- Remaining sprint: **the Day 9 recording, and Day 10 packaging.** The build stops there.
