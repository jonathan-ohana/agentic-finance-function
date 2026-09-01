# 44 — The SaaS layer: what a reporting pack can measure, and what it must refuse

**Date** 18 August 2026 · **Status** built and verified · **Prompted by** a correction from Jonathan, with a reference model attached

> *"The reporting is missing SaaS specific concepts... I don't see anywhere any ARR, Net retention, churn, CAC, LTV mentions"*

**Correct, and the omission was worse than it looked.** SL-08 ruled the ARR family on 17 August. Nothing implemented it. A subscription business was reporting itself as a manufacturer — revenue, margin, cash — with no line anywhere about the book that produces them.

Sixteen tabs now, and one of them is new: **SaaS Metrics**, with **Data_Book** beneath it in the extract layer.

---

## The distinction that shaped the build

The reference model computes NDR, LTV, CAC and LTV:CAC on its `SaaS KPIs & Metrics` tab. It can, because it is a **forecast**: churn is an assumption on row 4 of `Home case`, ARPU growth is an assumption on row 9, and NDR falls out of the assumptions that produced it. Every one of those numbers is an input wearing an output's clothes.

**An actuals pack cannot do that.** Retention is a fact about what happened to a book of customers. It requires a subscription record with a history. So the first question was not *which metrics should we add* but *which metrics can this book support* — and the answer turned out to be the most useful thing in the tab.

---

## What was built

### Data_Book — the recurring revenue book, in the extract layer

Per segment, per period: logos live, logos opened, logos closed, the annualised contracted value of each, the same in constant currency, the billed value beside the contracted one, and a **twelve-month cohort base and survivor** pair for retention.

That is everything an ARR waterfall needs **except expansion and contraction**.

### SaaS Metrics — thirty-eight rows, every one a formula

| Block | What it holds |
|---|---|
| **The ARR family** | MET-009 contracted, MET-009 billed as a memo, the leakage between them, the trailing-three-month usage run-rate, MET-010, and MET-011 shown as `PROHIBITED` |
| **The waterfall** | Opening, FX, new, churn, expansion/contraction, unattributed, closing — per segment and total, each with a tie check |
| **Retention** | Logo churn monthly and annualised, gross revenue retention on a twelve-month cohort, per segment, and NRR |
| **Unit economics** | ARPA blended and per segment, logos opened, CAC, CAC payback, LTV per segment, LTV:CAC |
| **Efficiency** | Net new ARR in constant currency, burn multiple, magic number, Rule of 40 |

Four of these are now KPIs with quarterly goals on the KPI tab.

---

## What it can measure

**Committed recurring ARR (MET-009) — $4,743,222 at 31 July**, on the contracted price per MET-021, growing 176% year on year.

**Gross revenue retention, 88.8% blended** — 100% on both B2B segments, **73.5% on the consumer book**. That split is the number, and the blend hides it.

**The waterfall ties in every period**, with FX on its own line so the commercial movement is constant-currency:

| July, total book | |
|---|---|
| Opening | 4,758,957 |
| FX translation | +29,357 |
| New logos | +15,706 |
| Churned logos | **−60,947** |
| Expansion / contraction | *not observable* |
| Unattributed | 0.01 |
| **Closing** | **4,743,222** |

**Net new ARR is negative — $45,241 in July and $14,800 in June.** The book is shrinking in constant currency. The P&L cannot say that; revenue was roughly flat across the same two months. That is the single most useful sentence the new tab produces, and it now leads slide 1 of the board deck.

---

## What it refuses to measure, and why that is the point

Four rows read `NOT COMPUTABLE` or `NOT OBSERVABLE`. Each names its blocker and what would clear it.

**Expansion and contraction — NOT OBSERVABLE.** The subscription files hold **one row of current state** per customer: today's court count, today's price, no effective date on a change. Two contract changes are known to exist in this population — CLB-0042's upsell from four courts to ten in January, and one downgrade. **Both are invisible.** The book reports the post-change value in every historical period, so the change never happened and every period before it is misstated.

The tell is that the waterfall ties **to the cent**. A book with real expansion in it that reconciles perfectly is not a well-controlled book; it is a book that cannot see the expansion.

**Net revenue retention — NOT COMPUTABLE.** It needs the two lines above. A monthly proxy is shown on its own row, labelled a proxy, with the sentence *"do not quote it as NRR"* on the face of it.

**CAC payback and LTV:CAC — NOT COMPUTABLE**, and this is the one worth the argument.

CAC is computable: all S&M over all logos opened. But it is **fully loaded** (no ruling exists on which part of S&M is acquisition and which is retention) and **blended across a B2B and a B2C motion** (S&M carries no segment in the ledger). So the numerator is a cost incurred overwhelmingly to win club contracts, while the denominator of payback would be gross profit per logo on a book that is **94% consumer subscribers by count**.

The first version of this tab computed it anyway and printed **2,558 months of CAC payback**. That is not a long payback; it is two different populations in one fraction. The row now refuses, and says which ruling unblocks it.

**LTV where no churn has been observed** reads `n/a — no churn observed`, not a large number. Neither B2B segment has recorded a single churn event in eighteen periods. An unmeasured life is not a long one — and an LTV:CAC ratio built on it is how a SaaS model produces a number that survives right up until diligence.

---

## SL-24 — the retention family, ruled

Six new metrics, **three of them ruled NOT COMPUTABLE**, which is a ruling and not an omission. Two named unresolved blockers with owners and review dates:

- **SL-24a** — effective-dated change history on the subscription record. *The billing system holds it and does not export it.* Unblocks NRR and the lower bound on GRR.
- **SL-24b** — an S&M segmentation between the two motions and between acquisition and retention. Unblocks CAC at segment level, payback, and LTV:CAC.

And one methodological ruling worth stating on its own, because the first build got it wrong:

> **MET-028 gross revenue retention is a twelve-month COHORT measure** — of the value live twelve months ago, how much is still live. Twelve months of churn over an opening base is **prohibited**: it charges the base with the churn of customers who were never in it.

My first version used the prohibited form and reported **31% retention on the consumer book**. The cohort form reports **73.5%**. The pack was about to tell a board that three-quarters of its consumer revenue evaporates annually, when the truth is one quarter.

**What it costs**, stated in the ruling: the pack reports fewer SaaS metrics than a competitor's, and two of the four an investor asks for first read NOT COMPUTABLE. Accepted, because *a diligence analyst who finds that our NRR was a proxy does not merely discount NRR — they re-price every other number we gave them.*

---

## Three defects found by building it

**22 · The ARR schedule computes MET-009 on the billed price where MET-021 rules contracted.** `arr_schedule.csv` — the Analyst's ARR source and the board number — uses `actual_price_eur`. MET-021 rules the metric on `contracted_price_eur` and calls the gap leakage. **$109,510 a year understated at July.** The pack computes on the ruled basis, carries the billed figure as a memo, and shows the leakage on its own line rather than defining it away.

The class of fault matters: this is not a calculation error. It is **a ruling that was written and never propagated to the thing it rules**, which is the exact failure mode the semantic layer exists to prevent and the one nobody checks for.

**23 · The consumer book records zero logos opened in the two most recent periods.** 999 signups in April, **2,893 in May**, then **zero in June and July**, while churn continues at ~390 a month. Cause traced to a single line in the generator: `need = target − active`, with `range(max(0, need))` — so once the May surge pushed the active count above target, gross adds went to nil and the book ran off. The comment above it says the surge *"pulls growth forward"*; what it produces is a business that stopped acquiring.

**Recorded, disclosed, not fixed.** Regenerating would change every figure in the close pack, the variance pack, the review ledger's cited instances and the board deck — and the loop evidence in those artefacts is the portfolio, not the numbers. Same treatment as defect 12. The SaaS tab discloses it on a row that reads `NONE IN CONSUMER BOOK`, and every metric that divides by new logos says so rather than dividing.

**24 · Seven won-but-not-installed contracts were counted as courts in service.** Thirty-seven courts that bill nothing sat in the denominator of implied price per court and understated it. Found while making Data_Ops read its files from the mapping rather than knowing them.

---

## And the claim from yesterday, corrected

Doc 43 said *"the engine knows nothing about this company."* It was not true. `sheet_ops` named this company's four CSV files, and the lineage table was twenty-three hardcoded rows in the driver.

Both are now declarations in `mapping.json`: segments carry their own file, date fields and exclusions; the lineage table is data. `grep` for this company's vocabulary in `reporting_pack.py` returns **zero**.

Defect 20 — `variance.py`'s hardcoded segments — remains open and is now the only instance left.

---

## Verification

**3,520 formulas, zero errors, 171 numeric check cells across ten tabs all reading zero**, and every P&L, balance-sheet and cash-flow line still reconciled to the answer key after the refactor. 89/89 generator checks pass. Sixteen blue cells: fourteen quarterly goals and one plan FX rate, plus the legend.

The check that mattered most was not the recalculation. It was reading a retention figure of 31%, asking whether a consumer subscription with 2.4% monthly logo churn could really lose 69% of its revenue in a year, and finding that it could not.

---

## Carried forward

- **SL-24a and SL-24b** are the two rulings that unblock four metrics between them. Both have owners and a 30 September review.
- **Defect 22** should be corrected in `arr_schedule.csv` and the Analyst re-run, or the schedule retired in favour of Data_Book. The pack is already on the ruled basis; the answer key is not.
- **Defect 23** is disclosed, not fixed. If the dataset is ever regenerated, that line is the first fix.
- The board deck now leads with ARR and its constant-currency movement. Slide 4's `LTV : CAC — NOT PRODUCED` is now backed by a ruling rather than by absence.
