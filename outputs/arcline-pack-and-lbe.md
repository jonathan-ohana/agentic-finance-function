# 90 — Arcline: the January reporting pack and the Q1 LBE

**Instance** Arcline AI, Inc. · **Period** 2026-01 closed and signed · **Built** 26 Aug 2026
**Predecessors** doc 84 (pack doctrine), doc 82 (planning cadence and the LBE layout), doc 89 (run 03)
**Figures** as computed by the shipped workbooks (rebuilt 3 Sep 2026 with the corrected plan —
RUN 14 in the [run log](../runs/run-log.md)); re-read from them at that rebuild. The workbooks carry
no cached values — every figure is a formula, computed on open — so these are what a reader sees,
not what was typed here.

Two deliverables, both single workbooks, both verified independently.

```
05-lbe/FY2026/LBE_Q1_2026_M1.xlsx                    3 tabs
08-reporting/FY2026/FY2026-01-management-pack.xlsx   9 tabs
```

**Both workbooks ship in this folder** — [`FY2026-01-management-pack.xlsx`](FY2026-01-management-pack.xlsx) and [`LBE_Q1_2026_M1.xlsx`](LBE_Q1_2026_M1.xlsx) — along with [`packverify.py`](packverify.py), the independent verifier that recomputes every figure from the instance CSVs and asserts the 42 checks below. Open the pack, then read the verifier: the claim is not that the numbers are right, it is that a program that did not build them says so.

---

## The Q1 LBE

All change suggestions from the January flux analysis are ratified in this build. **43 of the 63
classified lines move the forecast; 16 are absorbed by the quarter and move nothing.**

| Q1 2026, USD | Fcst (plan of record) | Variance | LBE | Var % |
|---|---:|---:|---:|---:|
| Revenue | 5,782,547 | (148,126) | 5,634,420 | (2.6%) |
| Cost of revenue | (1,410,115) | 30,437 | (1,379,678) | 2.2% |
| **Gross profit** | **4,372,431** | **(117,689)** | **4,254,742** | **(2.7%)** |
| Gross margin % | 75.6% | | 75.5% | −0.1 pts |
| Operating expense | (7,388,272) | 956 | (7,387,316) | 0.0% |
| **Operating result** | **(3,015,840)** | **(116,733)** | **(3,132,574)** | **(3.9%)** |
| EBITDA | (2,879,640) | (121,851) | (3,001,492) | |
| **Adjusted EBITDA** | **(2,180,938)** | **(121,851)** | **(2,302,789)** | |

**Sticks (26,522) · materializes (53,486) · total effect on the Q1 operating result (116,733).**

The two halves are never merged, per the doc-82 correction. A closed month is fact and the only
question about it is whether the quarter absorbs it; an open month has not happened, so nothing in
it can stick. Using one word for both would tell the reader the engine is equally sure of a number
in the ledger and a number in a run rate.

`LBE = Fcst + Variance` is a formula in every cell it appears in, subtotals included. So is every
margin and every point move. The verifier opens the workbook *without* cached values and asserts it.

### The two design decisions worth keeping

**Opex is shown by cost center owner, and the allocation is derived rather than assumed.** Where a
finding sits on an account and vendor that span several centers, its effect is split on the
proportions the January ledger itself shows for that pair. Nothing is spread on a rule of thumb.

**Absorbed lines are listed, not deleted.** Sixteen lines were classified absorbed and move the
forecast by nothing. They sit in their own block on the page, each naming what absorbs it. A line
that vanishes because it nets is indistinguishable from a line nobody looked at. Eight of the
sixteen — the software renewal lines — now show a variance of exactly zero: the data fixes of run 08
removed the variances the analyst originally classified. They stay listed at zero, because the
classification is the analyst's record and the zero is the ledger's.

---

## The pack

Nine tabs, reading order: **P&L by FSLI · Revenue and ARR · Gross margin · Opex by owner · Balance
sheet · Cash · SaaS metrics · LBE Q1 M1 · Exceptions.**

| January 2026 | Actual | Plan | Prior month |
|---|---:|---:|---:|
| Revenue | 1,770,353 | 1,844,649 | 1,833,031 |
| Gross margin | 74.2% | 74.8% | 75.1% |
| Operating result | (1,115,302) | (1,021,332) | (756,585) |
| Adjusted EBITDA | (855,088) | (748,632) | (536,277) |
| Closing cash | 23,785,740 | | 24,861,062 |
| Runway | 35.3 months | | 56.1 months |

Three rules, all enforced by the verifier rather than asserted in a footnote:

- **Every derived number is a formula.** 455 of them. A typed ratio is a picture of a ratio.
- **No input colour anywhere.** Blue means a typed assumption a reader may change; a reporting pack
  has none. Verified at zero blue cells.
- **Each fact lives on one tab and every other appearance points at it.** Revenue is owned by the
  Revenue tab, cost of revenue by the Gross margin tab, opex by the Opex tab, the non-cash add-backs
  by the EBITDA build, and the month's revenue and cash spend by the P&L — which is what the balance
  sheet's ratio block divides by, so a ratio and the statement it describes cannot disagree.

Build order is **dependency** order and tab order is **reading** order. They are not the same, and
the difference is what lets each figure live in exactly one cell.

### What building it found

Four defects, all in my generator, all now fixed and guarded. Every one of them is the same shape:
**a number that was right in one place and wrong in another, where nothing put the two side by
side.** That is precisely what a management pack does, and it is the argument for building one.

**1. Payroll posted with no cost center — so opex by owner could not be struck at all.**

`payroll_model` aggregated by account and dropped the employee's cost center at the moment of
posting, even though every employee has one. Account 6000 carried 505,847 of 557,740 with no center;  <!-- docverify: external -->
6010, 7010 and 8010 had none whatsoever. The budget had owners and the ledger did not.  <!-- docverify: external -->

This is the single most consequential find. Opex by owner is *the* cut a cost center owner is managed
on, and it was unbuildable from the actuals. Fixed at the source: payroll is now keyed
`(account, cost_center)`, and bonus and PTO follow the people they belong to instead of landing
wholesale on CC-200 and CC-400 — which had Engineering carrying Applied Research's and Product's
bonus accrual. Guarded: *every operating expense line carries a cost center*.

**2. The two cuts disagreed by hundreds of thousands while both still footed.**

With the ledger fixed, the by-owner and by-FSLI cuts still differed — R&D by +366k, S&M by −219k —
and both totalled 2,427,160. The cause: I had assigned one FSLI per cost center. But **the account's  <!-- docverify: external -->
own name declares the FSLI** (6010 is "R&D — payroll taxes", 8050 is "G&A — software and tools") and
a center is free to spend across several — an Executive salary is G&A while the same center's
engineering spend is R&D. The grain is `(cost center, FSLI)`, not cost center. At that grain the two
cuts are equal by construction, on the plan side too, and the verifier proves it rather than assuming
it. *Two cuts that foot and disagree are the failure that reaches a CEO.*

**3. The cash flow's net result was the SUM of revenue and cost, negated.**

The trial balance carries revenue as a credit, so revenue accounts are negative there. One sign was
wrong, and December 2025 reported a net result of (4,364,118) against the P&L's (698,057) — out by  <!-- docverify: external -->
twice revenue, every month of the year, in a file nobody had put next to the P&L.

Rewritten as a **partition** rather than a list: double entry says the cash movement equals minus the
movement of everything else, so every non-cash account is enumerated and assigned to exactly one
bucket. `unexplained` is nil by construction and is printed anyway, so a future account that lands in
no bucket announces itself instead of being absorbed. Two traps handled explicitly — the stock comp
credit to APIC is not an equity raise, and the depreciation add-back and the movement on accumulated
depreciation are the same entry.

**4. The EBITDA add-back was reading the wrong account.** 8080 is depreciation; 8090 is credit loss
expense, which is not a D or an A. A neighbouring pair, and an add-back that had started describing a
provision.

### What the pack surfaced about the business

**DSO went from 55.9 days to 85.6.** Trade receivables rose 1,582,613 in a month on revenue of
1,770,353, against a 1.8–1.9M billing run rate. This is a **generator artifact**, not an
Arcline finding: my collection model only sees a partial window in the first month of the year. I am
recording it rather than fixing it, because rebuilding January would disturb a signed period.

But the mechanism is worth naming. A P&L-only pack would never have raised it. The working-capital
block did, on its first run, and the reason it could is that the ratios are formulas over a
classified balance sheet rather than figures typed beside one.

**Interest income was a plug, and the plug was on the plan side — fixed at the source in the 3 Sep
rebuild.** The FY26 plan used to carry 70,000 for January, stepping exactly 400 a month all year: an
arithmetic ramp, on a cash balance that is falling.  <!-- docverify: external -->
It is now derived the way the ledger derives the actual — a rate on the balance the plan itself
projects — printing 83,338 for January and declining every month thereafter, against an actual of
84,181.
The January variance on this line fell from 14,181, which was the plug showing up as news, to 843, which is a variance.  <!-- docverify: external -->
Putting the assumption and the outturn on the same line is what made the plug visible instead of
buried in a variance file; deriving the assumption is what retired it.

---

## Verification

`packverify.py` is independent by construction: it recomputes every figure from the instance CSVs and
reads the workbook's **recalculated** values, never its formulas. A verifier that reads the same
formula the builder wrote proves the builder is self-consistent and nothing else.

**42 of 42 checks pass**, and the instance suite is at **49 of 49** (up from 39).

The ones that matter are cross-tab, because any pack can foot down a column:

- revenue identical on the P&L and the Revenue tab, and equal to the ledger
- the benchmark is provably the plan of record
- **operating expense by FSLI equals operating expense by OWNER**, in total and on each of the three lines
- the balance sheet balances in December as well as January, and every account is classified
- the cash walk reaches the ledger in both months with no residual, and its net result is the P&L's
- the ARR waterfall foots to the ARR schedule from the change log, not from a stated total
- adjusted EBITDA less EBITDA equals stock comp exactly; EBITDA is stated as well as adjusted EBITDA
- **the hosted LBE tab equals the standalone artifact to the cent** — one builder, hosted twice, so they cannot drift
- the LBE's variance column equals the sum of the approved changes, and nothing else
- zero blue cells; every named ratio and derived headline begins with `=`

---

## Still open in the generator

Carried from doc 89, plus one new:

- **January collections are ~45% below run rate** (new) — the DSO artifact above.
- The prepaid release schedule does not tie to contracted ACV.
- Interest income is a plug.
- The `variance_signals` "expense account in credit" check false-positives on contra account 6080.
- The post-close inbox picks vendors that already have a January bill — the USD 67,500 double-count,  <!-- docverify: external -->
  which remains recorded in the signed period rather than rebuilt away.

---

## What this says about the product

Doc 89's argument was that precomputing the variance surface is what an incumbent copilot does not
do. This build adds the other half of it.

**The pack is where the numbers get confronted with each other.** Every defect above existed happily
in the instance until two views of the same money were put on facing pages and required to agree.
Nothing found them because nothing had ever asked. A variance report asks "is this line different
from plan"; a pack asks "do these two descriptions of the same month agree", and that is a question
with far more failure modes behind it.

The corollary for the product: the value is not the tabs. It is **the cross-tab checks, and the fact
that they run every time.** A finance team that builds the same pack by hand each month re-derives
its consistency by hand each month, which means it re-derives it less carefully each month. Here the
consistency is the artifact — 42 assertions that run in ninety seconds and would have caught all four
defects on the day they were written.

---

**Next:** the vendor spend review agent (PL-09 to PL-12) is still unfired, and the sealed month
protocol remains unarmed. The M2 LBE is the natural next artifact — it back-tests this one.
