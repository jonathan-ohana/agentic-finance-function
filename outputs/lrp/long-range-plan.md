# 85 — The long range plan, FY26 to FY30

*Rev 3, 25 Aug 2026. `tools/build_lrp.py`, `tools/lrp_core.py`, verified by `tools/verify_lrp.py`. **Nine tabs, 36 levers, 33 per-function cost drivers, 6 named software projects, two cases, 1,430 formulas.** Recalc 0 errors, 44 of 44 checks.*

## What it is, and what doc 82 says about it

Driver-built, five years, one switch. It exists to answer one question: **how much capital it takes to reach the point where the company funds itself, and when that arrives.**

Doc 82 rule 3 keeps the LBE out of every variance column. **The same applies here for the same reason** — a soft forward view used as a target is how numbers start moving without an explanation. The LRP never appears in a variance column and never becomes a plan of record. The annual budget is built *from* it, and the **budget** is what gets locked. The verifier checks that no cell of the reporting pack mentions it.

---

## The instrument, tab by tab

```
Summary                 the whole plan on one page, FY25A alongside FY26–FY30
Assumptions             every typed judgement, and nothing else typed anywhere
Revenue build           clubs -> courts -> matches -> subscribers -> four streams
Cost of revenue         compute, storage, hosting, install, cameras, revenue share
Opex by owner           eleven functions, thirty-three driver lines, one owner each
Capex — IUS             the software project register, by project
Capex — Equipment       cameras and IT equipment, gross / accumulated / net
Three-statement model   P&L, then balance sheet, then cash — on one page
FY26 base               the seams of year one: actual, LBE, plan of record
```

---

## The three statements are one statement

They were three tabs — a P&L on the Summary, a balance sheet, a cash flow. That is three lists. **They are now one tab, in the order the model is built:**

```
1 · Profit and loss        revenue -> gross profit -> FSLI opex -> EBIT
                           -> EBITDA -> Adjusted EBITDA -> result
2 · Balance sheet          working capital driven off the P&L rows directly
                           above; fixed assets from the two capex tabs;
                           cash from statement 3 -> CHECK = nil
3 · Cash flow              the result, plus what moved no cash, plus the
                           movement on statement 2, less capex -> the
                           funding requirement -> closing cash, which
                           carries UP to statement 2
```

**Cash is last because cash is the result.** Every term of the cash statement comes from the two statements above it — the result from the P&L, the add-back from the same three registers the P&L charges, the working capital from the balance sheet's own movement. A cash statement built *beside* the balance sheet instead of *from* it is a second opinion about the year, and two opinions is one more than a model can carry.

**Working capital reads off the P&L on the same page.** Receivables are the revenue row directly above ÷ 365 × DSO. Inventory and payables are the cost row ÷ 365 × their days. Deferred revenue is revenue ÷ 12 × months. There is no second copy of revenue anywhere in the ratio block, and the verifier now checks the formulas themselves — not the values — to prove it.

**The check at the foot of statement 2 is what the merge buys.** Cash on the balance sheet is the closing cash of the statement below it; the working capital in that statement is the movement of the balance sheet above it. The loop closes on one page, so `assets − liabilities − equity` is a test of the whole model. It reads **0.00 in all five years, both cases.**

The Summary now owns nothing. Every figure on it points at the three-statement model, which points at the build tabs — one chain, one direction. A reader who wants to know where a number comes from follows it rather than hunting for a second copy.

---

## The colour rule inverts, and that is the point

The management pack has **no blue in it**, because a report has no assumptions — every figure is a ledger balance or arithmetic over one.

An LRP is the exact opposite instrument. **It is assumptions**, and the whole value of it is that a reader can find one, change it, and watch the plan move. So blue is back and it means what it has always meant: *somebody typed this and it is a judgement.*

The verifier enforces the boundary: **no forward year is typed anywhere outside the Assumptions tab.** All 1,430 formulas, seven tabs, FY27 through FY30, checked.

---

## Year one is not a forecast, and FY25 is not fabricated

Every five-year plan is wrong about year five and nobody minds. What sinks an LRP is being wrong about **year one**, because year one is checkable.

So FY26 is three artifacts that already exist, and the `FY26 base` tab shows its seams:

| Months | Source | FY26 revenue |
|---|---|---|
| Jan–Jul | **ACTUAL**, from the ledger | 2,810,862 |
| Aug–Sep | the **Q3 LBE**, ratified | 905,057 |
| Oct–Dec | the **plan of record**, Apr-26 Reforecast | 1,397,896 |
| | **FY26** | **5,113,815** |

**FY25 on the Summary is the ledger, not a plug.** The instruction was to fake it. There was no need: the ledger carries **eleven real months, Feb–Dec 2025** — revenue 1,876,074, gross margin 52.9%, adjusted EBITDA (3,860k), 28 heads. The tab says **FY25 IS 11 MONTHS, NOT TWELVE** on its face, because a comparative that is short two months and does not say so is worse than no comparative. Two figures in that column were nearly fabricated and were caught: FY25 stock comp and IT depreciation had been pro-rated as *the FY26 figure × 11/12*. The ledger says **94,987** and **16,067**.

---

## The driver tree

```
net new clubs -> clubs -> courts -> matches -> compute cost
                              |            `-> usage revenue
                              |-> courts revenue
                              `-> subscribers -> player revenue
```

**One club signed moves seven lines.** The match count is deliberately **one number**: it drives usage revenue on the revenue tab *and* three cost lines on the next one. A plan that lets volume flatter the top line without paying for it below has been tuned rather than built.

---

## Operating expense is modelled per function, not per growth rate

**Lever L21 — "non-payroll opex growth, % per year" — is marked SUPERSEDED.** Every non-payroll line sits in `lrp_opex_drivers.csv`: **33 lines across 11 functions**, each with a named owner, a driver type and a written basis.

| Function | Owner | Lines |
|---|---|---|
| Engineering & ML | VP Engineering | ML research compute · developer tooling · contractors (× contractor-months) |
| Product & Design | Head of Product | research, testing and design tools |
| Club Sales | VP Sales | commission (% of new-court revenue) · field travel · trade events (× events) |
| Growth Marketing | Head of Growth | paid acquisition (per net new subscriber) · app store fees · partner commissions |
| Customer Success | Head of CS | success tooling and onboarding, per club |
| Executive | CEO | board and governance · corporate travel and IR |
| People & Ops | Head of People | recruiting fees (% of new-hire cost) · EOR and benefits admin · L&D |
| Finance | Head of Finance | audit · tax and transfer pricing · outsourced accounting · bank and FX fees |
| **Legal** | **General Counsel** | **corporate counsel (× financing events) · commercial contracting (per new club) · litigation (× active matters) · IP and regulatory** |
| IT | Head of IT | software and subscriptions · security, identity and compliance |
| Facilities | Head of People | office and coworking (× in-office ratio) · insurance |

**LEG-3 litigation** = `LEG-3Q` active matters × cost per matter. Both halves are levers, so "optimize litigation cost" is expressible two ways that give different numbers a General Counsel can be asked about.

**Payroll is not one blended rate either.** Each function carries its own loaded cost per head from the FY26 ledger — Executive 231k, Engineering 171k, People & Ops 129k, Growth 123k, Product 120k, Club Sales 116k, Customer Success 109k. L19 is now only the annual rise on each.

---

## The software register — a rate is not a capitalization policy

`Capex — IUS` was a rate: 22% of engineering payroll, in and out. It gave a number and **could not say what the number was for**, which is the first question an auditor asks and the second question a board asks. It is now a register, and the tab is built in three parts:

**1 · The pool — what qualifies.** Engineering payroll × **L33** plus product payroll × **L34**, off the hiring plan. Two rates because the teams are different: L33 is 22% falling to 20%, L34 is 12% falling to 11%. Design and product work is capitalizable only where it is application development on a named project, not discovery — *a plan that capitalizes the same share of both is not reading its own timesheets.*

**2 · The register — what is being built.** Six named projects, each with a team, an owner, a scope and a status:

| | Project | Team | FY27 | FY28 | FY29 | FY30 |
|---|---|---|---|---|---|---|
| IUS-1 | **Match ingestion and video pipeline v2** | Engineering | 180k | 60k | — | — |
| IUS-2 | Highlight and clip engine | Engineering | 70k | 120k | 40k | — |
| IUS-3 | Club operations console | Product | 55k | 60k | — | — |
| IUS-4 | Player app rebuild — subscriptions and cohorts | Product | — | 90k | 70k | — |
| IUS-5 | Billing and revenue recognition platform | Engineering | — | 95k | 45k | — |
| IUS-6 | Multi-tenant provisioning and deployment | Engineering | — | — | 130k | 90k |
| | **Named** | | **305k** | **425k** | **285k** | **90k** |
| | *Balance of the pool — not yet scoped* | | *112k* | *144k* | *327k* | *580k* |
| | **Total capitalized** | | **417k** | **569k** | **612k** | **670k** |

**IUS-1 is the main project of the plan**, and it is the one that makes L12 — inference cost per match — a lever the company can actually move rather than a number it hopes falls. IUS-4 carries the cohort and legacy-pricing fix that **L06 assumes happens**, so if the project slips the ARPU recovery slips with it: the plan now shows that dependency instead of leaving it in two unconnected places.

**3 · The unnamed balance is the honest part.** It is 27% of the pool in FY27 and 87% by FY30, because a company cannot name its FY30 projects in FY26 and should not pretend to. **L35 is the control that reads it** — a stated floor for the named share, falling 70% → 15% across the horizon. Naming a project later moves money *out* of the unnamed line and changes nothing else in the plan. Inventing six projects to fill the FY30 column would have looked more complete and been worth less.

**Amortization is per project, from the year it goes live.** Half a year in the first year and half in the tail, on the 36-month life. So IUS-1 is a FY27 project still costing the P&L in FY30 — which is exactly what capitalizing does and exactly why it is not free. **The half-year weights are derived from L24, not written in as literals**, so changing the life moves the charge the way a lever is supposed to.

**And the direction of the entry reversed.** The Opex tab's *"less capitalized software labour"* credit is now `= −'Capex — IUS'!total`, not a rate applied independently beside it. The register decides what gets capitalized; the credit is the consequence. Two derivations of one number is how a model quietly stops tying.

**L22 is marked SUPERSEDED** — kept so the lever id does not disappear from a plan somebody has already read.

---

## `Capex — Equipment`

Two classes on one tab because they behave differently and land in different places:

- **Cameras** — 260 per court falling to 240, on every new court commissioned, 36-month life. Camera depreciation is **cost of revenue**: it is the capital intensity of this business and it belongs above the gross margin line.
- **IT equipment** — 2,400 per new head, 36-month life. IT depreciation is **operating expense**.

A single "capex" line would have put camera depreciation in opex and quietly overstated gross margin by roughly a point and a half a year.

---

## Base case

| | **FY25A** | FY26 | FY27 | FY28 | FY29 | FY30 |
|---|---|---|---|---|---|---|
| | *11 mths* | | | | | |
| Revenue | 1.88m | 5.11m | 7.73m | 12.04m | 17.56m | **23.70m** |
| Gross margin % | 52.9% | 64.1% | 55.4% | 58.7% | 63.0% | **67.5%** |
| R&D | (1.08m) | (2.02m) | (2.91m) | (3.70m) | (4.22m) | (4.46m) |
| S&M | (2.20m) | (4.76m) | (6.14m) | (7.73m) | (8.45m) | (8.57m) |
| G&A | (1.74m) | (2.86m) | (3.90m) | (4.22m) | (4.22m) | (4.36m) |
| Stock comp | (0.09m) | (0.35m) | (0.47m) | (0.62m) | (0.74m) | (0.83m) |
| Depreciation, IT | (0.02m) | (0.03m) | (0.03m) | (0.04m) | (0.05m) | (0.05m) |
| **Total opex** | (5.01m) | (9.64m) | (13.45m) | (16.32m) | (17.67m) | (18.27m) |
| **Adjusted EBITDA** | (3.86m) | (5.70m) | (8.29m) | (7.93m) | (4.83m) | **(0.27m)** |
| — % of revenue | (206%) | (111%) | (107%) | (66%) | (28%) | **(1.1%)** |
| Memo — EBITDA | | (6.05m) | (8.77m) | (8.55m) | (5.57m) | (1.10m) |
| Free cash flow | | (5.77m) | (7.95m) | (7.76m) | (4.61m) | (0.32m) |
| Equity raised | | — | 9.0m | 8.0m | 2.0m | — |
| **Cumulative capital** | | — | 9.0m | 17.0m | **19.0m** | 19.0m |
| ARR at year end | | 5.93m | 9.44m | 14.39m | 20.29m | **26.65m** |
| Clubs / heads | 236 / 28 | 266 / 33 | 418 / 45 | 611 / 54 | 820 / 58 | 1,031 / 60 |
| Rule of 40 | | (111%) | (56%) | (10%) | 18% | **34%** |

**19m of equity, raised across FY27, FY28 and FY29, takes the company to within 1.1% of breakeven in FY30 — and not past it.**

**The base case does not reach profitability inside the horizon, and it was not tuned until it did.** L01 — net new clubs a month — is an OPEN lever, and moving an open lever until the plan lands where somebody wanted it is the failure this whole system was built to prevent. The lever's written basis says so, in the file, where the next reader will find it. The honest read: *at these assumptions the company is about a year past FY30 from self-funding, and closing that year is a conversation about L01, not a modelling exercise.*

## Downside case — not a haircut

The base case with the July run rate held flat: 8–9 clubs a month, CAC that never improves, ARPU that never recovers, EUR/USD at a five-year low, **and only two software projects funded**.

| | FY30 base | FY30 downside |
|---|---|---|
| Revenue | 23.70m | **10.67m** |
| Adjusted EBITDA | (0.27m) | **(5.25m)** |
| Cumulative capital | 19.0m | **23.0m** |

**The downside costs 4m more capital and ends further from profitability**, still raising in FY30 with no end in sight. That is the right shape for a downside, and it is a verified check rather than a claim.

---

## The four open levers

Thirty-two levers are contracted rates or measured run rates. Four are **OPEN**:

| | Lever | Owner | Why it is open |
|---|---|---|---|
| L01 | Net new clubs a month | VP Sales | The whole plan turns on it. ~6/month observed; base assumes it roughly triples. **Not moved to make the plan reach breakeven.** |
| L05 | Subscribers per court | Head of Growth | 9.36 measured. No cohort evidence that it holds as later clubs get smaller. |
| L06 | ARPU recovery | Head of Growth | 10.76 realized against 11.00 planned. **Depends on IUS-4 shipping** — the register now names that dependency. |
| L12 | Inference cost per match | Head of Infrastructure | 0.3329 against 0.3226 planned. **IUS-1 is what would move it**, and the register says when. |

Two projects on the register also carry OPEN: **IUS-4** (scope not yet cut) and **IUS-6** (a FY29 project named in FY26).

---

## What the build turned over this revision

**A third house-rule over-reach, and this one was in the lexicon.** The rule `\bcharge[sd]?\b` banned the word outright with "post / posted (to the GL)" as the replacement. It was written for the verb — *charged to 5070* — but as written it banned the accounting **noun**: the depreciation charge, the amortization charge, the charge for the year. Five correct sentences in the new tabs failed on it. Narrowed to `\bcharg(e|es|ed|ing)\s+(it\s+|them\s+)?(to|against)\b`, which bans everything the rule meant and nothing it did not. **The narrowing is recorded in the note column and flagged for your confirmation or reversal** — the rule is yours, dated 22 Aug.

That is the third time: `carry into the forecast` silently suppressed a comment; the lexicon renamed a GL account; and now this. The pattern is consistent — a rule that fires on a *word* rather than a *usage* will eventually hit the term of art.

**A verifier that read the wrong row and passed.** The register carries every project twice — once for what it spends and once for what it charges — and `find()` returns the first match. The check "no project amortizes more than it cost" was comparing the spend rows against the spend rows and passing on an identity. `find_after()` now exists and the check reads the amortization block. **A test that passes on the wrong number is worse than no test**, because it is counted.

**Earlier in the same build, four balance-sheet bugs** the check caught before the tabs were merged: stock comp added back in cash but never credited to paid-in capital; accrued payroll flexing with DPO because it sat inside AP; equipment capex sign-flipped so capex *added* cash; opening camera and IT balances typed rounded.

---

## Verification

`tools/verify_lrp.py` — **44 of 44 pass.**

1. **Year one ties to the close** — revenue, cost of revenue and the owner split of operating expense all reconcile to actuals + the ratified LBE + the plan of record, to the cent.
2. **Nothing forward is typed** — seven tabs, FY27 to FY30, every cell a formula.
3. **The three statements are on one tab and cash is last** — the section order is checked, not assumed.
4. **Working capital is driven off the P&L on the same page** — checked against the *formulas*: receivables and deferred revenue point at the revenue row, inventory and payables at the cost row.
5. **The balance sheet balances** in every year, cash on it *is* the closing cash of the statement below, and stock comp is credited to capital.
6. **The software register foots to the pool** — named + unnamed = total capitalized, every forward year; the pool is two rates on two teams; no project amortizes more than it cost; the first year is half a year and the weight comes off L24.
7. **The unnamed balance grows across the horizon** — 27% of the pool in FY27 to 87% in FY30, which the plan states rather than papers over.
8. **The driver tree holds** — courts = clubs × density; matches = courts × rate; the inference formula provably points at the same match row usage revenue does.
9. **The two cases are different plans** — the switch moves revenue by 13.0m and the funding requirement by 4.0m, and the downside is verified to cost *more* capital while ending further below breakeven.
10. **The LRP is not a benchmark** — no cell of the reporting pack references it.

Recalc **0 errors on 1,430 formulas**, both scenarios. House lexicon clean across 834 strings. Package purity clean. Full suite: 7 verifiers and 2 test harnesses, all green.
