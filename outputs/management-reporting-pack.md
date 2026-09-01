# 84 — The management reporting pack

*Built 25 Aug 2026 to Jonathan's spec. Seven tabs, one close month, one benchmark. `tools/build_mgt_pack.py` and `tools/mgt_core.py`; verified by `tools/verify_mgt_pack.py`.*

## The spec, as ruled

| Decision | Ruling |
|---|---|
| Period columns | **Close month only.** Plus the current-quarter LBE as the last tab. |
| Comparators | **Q2 forecast only** — Apr-26 Reforecast, locked 2026-04-15 as LOCK-FY26-Q1. No budget memo column. |
| Revenue segmentation | **Product line** — Player, Courts, Academy. |
| Bridge | **Volume, price, mix and FX.** |

Seven tabs: P&L by cost category · Revenue · Gross margin · Opex by owner · Balance sheet · Cash · LBE Q3.

---

## What scoping the pack found

Two integrity failures, both live, both in the numbers already shipped.

### 1. Revenue was measured against the wrong plan

July revenue is 452,529.

| Compared with | Variance |
|---|---|
| FY26 Board Plan — what the pack actually used | 496,693 → **−44,164 (−8.9%)** |
| Apr-26 Reforecast — the plan of record | 461,317 → **−8,788 (−1.9%)** |

The LBE's own footnote said *"Fcst Q3 is the plan of record: Apr-26 Reforecast"* while its revenue row carried 1,424,740 — the board plan. The reforecast is 1,325,167. **99,573 of the quarter's revenue benchmark was the wrong artifact.** The variance commentary carried it too: *"revenue 453k vs 497k planned (−9%)"* on account 5050, where the real number against the ruled comparator is −1.9%.

**Why the control missed it.** `plan_guard` hashed `plan_by_account.csv`, which is expense-only — thirty-one accounts, not one of them a 4xxx. Revenue had never been inside the control. This is the same incident the guard was built for, in the one place the guard was not looking.

**Fixed.** `plan_guard.extract_topline()` now hashes revenue, COGS and the three opex blocks of the plan of record. `plan_rulings.csv` carries a `topline_hash` column. Ruling **PR-2026-08-r3** supersedes r2. Every caller that wants planned revenue goes through `revenue_plan_of_record()`, so there is one place the answer comes from.

**Effect on the Q3 LBE:** revenue variance moved from **−67,154 to +32,419**.

### 2. The plan of record exists in two forms and they disagree

| | July expense |
|---|---|
| `plan_apr26_reforecast.csv` — the locked summary the board saw | 950,119 |
| `plan_by_account.csv` — the bottom-up build the owners manage to | 976,947 |
| **Difference** | **26,828** |

Both carry `plan_version = "Apr-26 Reforecast"`. `LOCK-FY26-Q1` names the version, not the file, so which one is "the plan" is ambiguous by construction.

This has never mattered because no artifact put them side by side. The management pack does: tab 1 shows a category P&L against the bottom-up build, tab 4 shows the same money by owner, and the board's own summary is a third number. **Not plugged** — `build_plan.py` refuses residuals, and a top-down lock and a bottom-up budget are allowed to differ. **Reconciled on the page** instead, with both rows and the difference.

**Open for Jonathan's ruling:** which file `LOCK-FY26-Q1` actually locks, and whether the difference is disclosed each month or closed at the next lock.

---

## What the pack does that a template would not

**The revenue bridge is exact, not approximate.**

```
plan of record 461,317
  + re-basing to the driver model   +35,376
  + volume                          −19,048
  + price                            −3,923
  + FX                               +8,668
  + usage, packs, refunds           −29,862
= actual                           452,529
```

Volume is measured at forecast price and forecast FX, price at actual volume and forecast FX, FX at actual volume and actual price. The three terms telescope to actual minus forecast with no residual, so there is no "other" bar. Realized price is revenue ÷ volume ÷ FX, which makes volume × price × FX equal the ledger to the cent — and is also what a reader means by price.

**The re-basing bar is a finding, not an adjustment.** The Q2 reforecast moved the revenue line and never republished drivers, so 35,376 of the gap cannot be attributed to a subscriber, a price or a rate — no reforecast subscriber count exists to attribute it to. Folding it into volume would invent a comparator.

**There is no cross-product mix bar, on purpose.** The three lines are counted in subscribers, courts and seats; a mix bar across incomparable units is arithmetic, not information. And mix moves no dollars in any case — it redistributes them, so at the total it is always zero. Where mix genuinely lives is in a **rate**, and the pack puts it there:

- **Courts density.** Courts volume decomposes into clubs (236 vs 261.25) and courts per club (6.80 vs 6.80). The entire Courts shortfall is new logos; density is exactly on forecast. That is a sales problem, not a land-and-expand one.
- **Player cohort blend.** Realized ARPU is 10.76 against 11.00 planned, because the legacy cohort (29.8% of subscribers, 9.34 ARPU) and black_friday_2025 (7.1%, 5.95) sit below the current cohort's 11.98. No cohort mix was ever planned, so this explains the price bar — it is not a variance against a comparator nobody ruled.
- **Blended gross margin.** −2.52 points = rate −2.07 + mix −0.45, exact.

**The gross margin bridge has no "revenue at plan margin" bar.** That construction gives revenue growth a share of cost and then counts the volume-driven cost lines again for the same dollars. Here every dollar belongs to exactly one bar.

**The cash flow is a partition, not a list.** Double entry says the cash movement equals minus the movement of everything else, so the indirect walk enumerates *every* non-cash account rather than the items somebody remembered. The first version was a hand-written list and landed 54k short. Two traps handled explicitly: the stock comp credit to APIC is not an equity raise, and accumulated depreciation is the same entry as the add-back and cannot be counted twice.

**The balance sheet closes both years.** Account 3090 carries the deficit brought into the first period on file and nothing since, so a balance sheet read straight off the trial balance is out by every dollar lost since — 3,740,347 for the prior year alone.

---

## The open judgement the pack prices

Inference, storage and platform amortization go out on matches analyzed. A match is captured at a club — so on a **cause** basis almost all of it lands on Courts. But the match is consumed by the club *and* by the players in it, so on a **benefit** basis it splits.

| | cause basis | benefit basis | swing |
|---|---|---|---|
| Player | 96.6% | 70.3% | −26.4 pts |
| **Courts** | **11.9%** | **60.6%** | **+48.7 pts** |
| Academy | 97.9% | 70.3% | −27.6 pts |

A 48.7-point swing on the Courts margin, on a judgement nobody has ruled. The pack states it, shows both, and says *do not price, invest or cut on this line until the basis is ruled.* The bases, their rationale, their owner and their status live in `example/data/cogs_allocation.csv` — a declared instance file, not a constant in a script, because a judgement with that much riding on it does not belong where nobody can find it.

---

## Verification

`tools/verify_mgt_pack.py`, independent by construction — it recomputes from the CSVs and reads the pack's recalculated values, never its formulas.

Any pack can foot down a column. The failure that reaches a CEO is two tabs describing the same month with different numbers, so the cross-tab checks are the ones that matter:

- revenue identical on P&L, Revenue and Gross margin
- cost of revenue identical on P&L and Gross margin
- **operating expense by CATEGORY equals operating expense by OWNER** — the two cuts on tabs 1 and 4
- the month's result identical on P&L and Cash
- both bridges land with no plug; the balance sheet balances; the cash walk reaches the ledger cash account
- the benchmark is provably the plan of record **and provably not the board plan**
- the hosted LBE tab equals the standalone LBE artifact to the cent — one builder, hosted twice, so they cannot drift

18 of 18 pass. Recalc 0 errors on 268 formulas. House lexicon clean. Package purity clean. Full suite 8 of 8.


---

## Revision, 25 Aug — the FSLI cut, margins as rows, and the balance-sheet movement

Jonathan's edits, taken from a marked-up screenshot and three instructions.

### The pack is now eight tabs

`P&L by category` · **`P&L by FSLI`** · `Revenue` · `Gross margin` · `Opex by owner` · `Balance sheet` · `Cash` · `LBE Q3 M1`

Both P&L pages come from **one builder**. They are the same month, the same benchmark and the same subtotals; only the middle block differs. Two functions would have guaranteed that the next format change landed on one and not the other, and then the pack has two P&Ls that do not look like each other.

### Which FSLI an account belongs to

**The account's own name declares it.** 6010 is *"R&D — salaries & burden"*, 7010 is *"S&M — …"*, 8010 is *"G&A — …"*, and cost of revenue is the 5xxx accounts — which also makes it tie to the Gross margin tab exactly. An engineer sitting in the Infrastructure cost center still lands in R&D, which is where a reader expects an R&D salary to be.

The alternative basis is cost-center function, and **the two disagree on where 13,599 of July sits** — Customer Success, Field Operations and Infrastructure all carry function COGS while holding opex accounts. Both bases give the same total. The category tab's reconciliation is struck on function (that is how the locked summary labels its three blocks); the FSLI tab's is struck on prefix. Both land on the same 26,828, and both foot to 976,947.

> That reconciliation leaked when the FSLI cut was first written: an opex account in a COGS-function center fell into a bucket the tab never printed, and the bottom-up row quietly stopped being the plan by 13,600. The verifier now checks that both reconciliations foot to the same number.

### Margins are rows, not a column

The `% of revenue` column is gone. Each margin now sits directly under the line it belongs to, with **three figures: actual %, forecast %, and the move in POINTS.**

The point move is the number an operator argues about, and it is *not* the same as the percentage variance in column E. As a column the margin was a third decimal place on a crowded row; as a row it is a line of its own.

| | P&L by category | P&L by FSLI |
|---|---|---|
| Gross margin % | ✓ | ✓ |
| Total opex % of revenue | ✓ | ✓ |
| EBITDA % | ✓ | ✓ |
| Net margin % | ✓ | ✓ |
| R&D / S&M / G&A % of revenue | — | ✓ |

The bottom line is renamed **Net profit**.

### Balance sheet and cash carry the prior month

Both tabs now run close month · prior month · movement, and **both checks run on both columns** — the balance sheet balances in June as well as July, and the indirect cash walk reaches the ledger in both.

The July result reads off the balance sheet directly: the movement on *Result for the year to date* is −465,180, which is the net profit on both P&L tabs. That is now a verified check rather than a coincidence.

### Working capital ratios

| | Jul | Jun | Move |
|---|---|---|---|
| DSO — trade | 15.53 | 11.87 | **+3.67** |
| DSO — including unbilled | 18.54 | 14.87 | +3.68 |
| DPO | 47.66 | 40.99 | **+6.66** |
| Inventory days | 26.14 | 23.03 | +3.11 |
| **Cash conversion cycle** | **−5.98** | **−6.09** | +0.11 |
| Current ratio | 2.89 | 3.08 | −0.19 |
| Quick ratio | 2.81 | 3.01 | −0.20 |
| Net working capital | 5,368,365 | 5,813,938 | −445,573 |
| Deferred revenue — months | 2.45 | 2.08 | +0.37 |
| **Cash runway — months** | **18.87** | **20.49** | **−1.62** |

**A day-count ratio is a definition before it is a number.** Whether accrued expenses belong in DPO, whether unbilled receivable belongs in DSO, and whether the Stripe balance counts as cash are all judgements, and two finance teams answer them differently. They are declared in `example/data/bs_classification.csv` with the reason and the owner — the same doctrine as the COGS allocation — so the reader sees the definition instead of reverse-engineering it from the number.

Three choices worth naming:

- **DSO is split.** Trade receivable is a collection number. Adding unbilled usage measures a billing-cycle effect instead, and mixing them hides which one is moving. Both are shown; the gap is 3 days and it is stable.
- **Accrued payroll is out of DPO.** Payroll is not trade credit, and leaving it in makes a company look like it is stretching suppliers when it is only mid-cycle on salaries.
- **Every day-count is struck on the same month's activity**, annualized by that month's own day count — not on a trailing average. A management pack is read for the movement between two columns, and a trailing average damps exactly that. Runway is the one exception: a single month cannot carry it, so it is cash over the average net burn of the last three months, counting **only months that consumed cash** — averaging in a month that raised money flatters the answer.

### What the ratios say about July

DSO up 3.7 days and DPO up 6.7 days in the same month. The cash conversion cycle barely moved (−5.98 against −6.09) because the two effects offset — but they are not the same kind of news. Collecting slower is a receivables problem; paying slower is a decision, or a symptom of one. Payables rose 93k in the month against a 178k *reduction* in June, so July reversed the prior month's catch-up.

Runway fell 1.6 months, from 20.5 to 18.9.

### Verification

**37 of 37 checks pass**, up from 18. The new ones:

- every headline is identical on both P&L tabs — revenue, cost of revenue, gross margin, total opex, operating profit, EBITDA and net profit
- FSLI cost of revenue ties to the Gross margin tab
- both reconciliations land on the same difference and foot to the same bottom-up plan
- the balance sheet balances in the **prior** month too, and the cash walk reaches the ledger in the **prior** month too
- the year-to-date result moves by exactly the month's net profit
- closing cash equals the balance sheet cash accounts
- cash conversion cycle = DSO + inventory days − DPO, in both months
- DSO including unbilled is never below DSO on trade; the quick ratio is never above the current ratio
- **every balance sheet account is classified** current or non-current — an unclassified account would silently drop out of the current ratio

Recalc 0 errors on 390 formulas. House lexicon clean. Package purity clean. Full suite 8 of 8.


---

## Revision, 25 Aug (second) — every derived number is a formula, and the metric is named correctly

### "We need the formulas included"

The ratio block was typed. So were the revenue bridge bars, the gross margin bridge bars, and the mix split. That is a real defect and not a cosmetic one: **a typed ratio is a picture of a ratio.** Change a receivable and DSO sat there.

Everything derived is now a formula in the cell.

**The balance sheet had to be restructured to make it possible.** Two changes:

- **Classified current / non-current.** A current ratio built as a hand-listed `SUM` of account rows breaks the first time somebody adds an account. Built over a subtotal that already exists on the page, it cannot.
- **A "Ratio inputs" block, in blue.** A day-count needs two things a balance sheet does not carry — the month's revenue and the month's cash operating spend. They are ledger facts, so they are typed, in blue, per the house colour rule. Everything downstream is a formula on top of them.

```
DSO      =IFERROR(B11/B49*B54,"")                    receivable / revenue x days
DPO      =IFERROR((B28+B29)/B53*B54,"")              (AP + accrued) / cash spend x days
CCC      =B64+B67-B66                                DSO + inventory days - DPO
Current  =IFERROR(B15/B33,"")                        the two subtotals above
Runway   =IFERROR((B9+B10)/B60,"")                   cash / average net burn
Burn     =IFERROR(-AVERAGEIF(B57:B59,"<0"),0)        only months that consumed cash
```

The runway condition is worth calling out: **"only months that consumed cash" is in the formula, not in a footnote.** Four monthly cash movements are laid out once and the two runway columns take overlapping three-month windows, which is what makes the prior-month runway a formula too — and makes the overlap visible to anyone comparing the two.

**The revenue bridge bars are now written the way they are defined**, over the driver table above them:

```
Volume  =(B{d}-C{d})*E{d}*G{d}       (actual units - forecast) x forecast price x forecast FX
Price   =B{d}*(D{d}-E{d})*G{d}       actual units x (realized EUR - forecast) x forecast FX
FX      =B{d}*D{d}*(F{d}-G{d})       actual units x realized EUR x (actual rate - forecast)
```

Realized price is itself a formula — `=IFERROR(B{stream_revenue}/B{volume}/F{fx},"")` — so volume × price × FX equals the ledger by construction rather than by arithmetic done in private.

**Three precision bugs surfaced the moment the numbers became formulas**, and each one is the same lesson:

| What was stored | What broke | Fix |
|---|---|---|
| Density at 2 dp — `6.80` | Actual density is 6.8008 and the whole density effect lives in the fourth decimal. The bar computed as **zero** and the clubs+density split stopped tying to the Courts volume bar. | Store at 10 dp, display at 2 |
| Volumes at 2 dp — `14,970.83` | Player volume effect drifted 691.76 against 691.72 | Store at 6 dp |
| Matches at 0 dp — `204,298` | The plan carries 204,297**.5**. Half a match times the summed unit cost is **28 cents** — the difference between a bridge that ties and one that nearly does. | Store at 4 dp |

**A typed number can hide its own rounding. A formula cannot.** Every one of these was invisible while the effect was computed in Python and typed in.

The verifier now asserts formula-ness directly: it opens the workbook *without* `data_only` and checks that thirteen named ratio and bridge cells begin with `=`.

### Adjusted EBITDA

**EBITDA is earnings before interest, tax, depreciation and amortization. Stock comp is none of those four.** A line that adds it back and calls itself EBITDA gets queried in the first diligence call it survives to.

Renamed throughout — both P&L tabs, the LBE, the LBE register column (`ebitda_lbe` → `adj_ebitda_lbe`) and the back-test. And a table sits under each P&L showing the build rather than asserting the label:

| | Jul actual | Q2 forecast |
|---|---|---|
| Operating profit | (485,073) | (515,630) |
| Add back depreciation — 5040, 8090 | 14,447 | 14,447 |
| Add back amortization — 5070 | 11,771 | 11,771 |
| **EBITDA** | **(458,855)** | **(489,411)** |
| Add back stock comp — 8095 | 29,106 | 29,106 |
| **Adjusted EBITDA** | **(429,749)** | **(460,305)** |

Both measures are on the page. The unadjusted one is what a lender or an acquirer means by the word, and hiding it behind the adjusted number is how an add-back stops being visible.

The quarter's LBE carries the same build: EBITDA (1,518,196) and adjusted EBITDA (1,428,169) — a 90,027 gap that is exactly Q3 stock comp.

### The LBE layout, as ruled

- **`% of rev` column removed.** It is a row now, under the line it belongs to.
- **`Var %` moved to the end of the numbers**, after the LBE column. The eye goes forecast → variance → where it lands; the percentage is a gloss on the variance, not a step in the walk.
- **Margin rows** under gross margin, total operating expense and adjusted EBITDA — forecast margin, LBE margin, and the move in points.
- **A `Total operating expense` subtotal**, which the page did not have. There was no line to hang the opex margin on.

### Verification

**45 of 45 checks pass**, up from 37. New:

- adjusted EBITDA less EBITDA equals account 8095, on both P&L tabs
- the adjusted EBITDA build ties to the statement, on both P&L tabs and on the LBE
- EBITDA is stated *as well as* adjusted EBITDA, not instead of it
- the LBE carries a total operating expense subtotal
- **every ratio and every bridge bar is a formula, not a typed number** — asserted against the un-cached workbook

Recalc 0 errors on 508 formulas (up from 390). House lexicon clean on both workbooks. Package purity clean. Full suite 8 of 8.


---

## Revision, 25 Aug (third) — no assumptions, so no input colour

> *"There shouldn't be any blue colors anywhere in this reporting package. There's no assumptions here. We're reporting. No hardcoded numbers in the bridges."*

The blue was a category error and a revealing one. Blue means **typed input** — a lever, an assumption, something a reader may change. **A reporting pack has none.** Every figure in it is a ledger balance, a plan-of-record balance, or arithmetic over those. Colouring the ledger as an assumption invites exactly the wrong question.

Blue is gone. **0 blue cells**, and the verifier now asserts it.

### Each fact lives in one place; every other appearance points at it

A number typed on two tabs is a number that can differ on two tabs, and no reconciliation catches it because both sides foot. So ownership is now explicit:

| Fact | Owner | Who points at it |
|---|---|---|
| Revenue, by product line | **Revenue** tab | P&L ×2, Gross margin's margin block |
| The revenue benchmark (plan of record) | **Revenue** tab, bridge start | P&L ×2 |
| Cost of revenue, by account | **Gross margin** tab, account block | P&L ×2, and the summary line at the top of its own tab |
| The three non-cash add-backs | the **adjusted EBITDA build table** | the statement's single non-cash line |
| Revenue and spend for the close month | **P&L by category** | the balance sheet's ratio inputs |

The build order changed to make this possible: sheets are created in **reading** order and populated in **dependency** order — Revenue, then Gross margin, then the two P&Ls, then the balance sheet. Tab order is what the reader sees; fill order is what makes each figure live in exactly one cell.

### What "no hardcoded numbers" turned up

A workbook must have leaves — the question is *which* cells are allowed to be one. Auditing every numeric cell found several that were arithmetic wearing a value's clothes:

| Was typed | Is now |
|---|---|
| **Courts per club — density** (6.80) | `=B{courts}/B{clubs}` — it is courts over clubs, and both are on the page |
| **USD per match**, actual and forecast, on four COGS lines | `=IFERROR(B{acct}/B${matches},"")` |
| **Cohort share, ARPU and gap to current** on the Player mix table | share, ARPU and the gap are all arithmetic over the counted subscribers and their billed MRR |
| **Margin, weight, rate effect and mix effect** per product line | the block now shows allocated cost of revenue explicitly, so margin is `(revenue − cost) / revenue` and the two effects are written where they are defined |
| **Margin on the benefit basis** in the allocation-swing table | shows the alternative allocated cost, then divides |

Two new checks fell out of the rebuild and both pass at nil: the cohort table now ties to the Player driver row (same subscribers, same realized ARPU), and the rate-and-mix block ties to the margin move on the statement above it.

### Where the leaves are, and why each is allowed to be one

**593 of 897 numeric cells are formulas (66%).** The remaining 304 are reported facts, and every one is a balance or a count:

- account balances, actual and plan — the P&L's opex lines, the Gross margin account block, the Opex-by-owner rows, every balance sheet line, every cash-flow movement
- counted volumes — subscribers, courts, clubs, seats, matches analyzed, cohort headcounts
- published rates — plan price per unit, EUR/USD
- the two published plan artifacts on the reconciliation block
- prior-month revenue and spend on the balance sheet — the only figures there taken straight from the ledger, because this pack carries no prior-month P&L to point at

That last one is stated on the tab rather than hidden: the close month's ratio inputs read off the P&L, so a ratio and the statement cannot disagree.

### Verification

**48 of 48 checks pass.** New:

- **no cell is coloured as a typed input** — the pack is scanned for blue and must return zero
- **repeated figures point at the tab that owns them, never restate them** — seven named cross-tab links are checked for being references rather than values
- the margin block's revenue equals the Revenue tab's, line by line

Recalc 0 errors on 593 formulas (up from 508). House lexicon clean on both workbooks. Package purity clean. Full suite 8 of 8.
