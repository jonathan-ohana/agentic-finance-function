# 82 — Planning cadence: budget, LBE, and the lock

*Ruled 22 Aug 2026 from Jonathan's description of his operating cadence. Wires into the semantic layer (benchmark governance), the Forecaster and Analyst charters, and the plan-hash engine check. Resolves edge case #10 ("which plan") and completes the plan-integrity incident's fix.*

## The cadence

- **Year-end:** annual budget built and LOCKED. Opens the year as plan of record.
- **Month 1 and Month 2 of each quarter, after close:** build the LBE (latest best estimate) — soft forecast, outside reporting tools, quarter-scoped, CEO-facing: where the quarter lands on latest information.
- **Month 3 / quarter close:** books closed, forecast for the remaining year LOCKED → new plan of record. Cycle repeats.

## Benchmark rules (semantic layer)

1. **Plan of record** = the latest LOCKED artifact (budget until Q1 lock; then each quarterly lock). Variance primary comparator, always.
2. **Original budget** survives all year as memo comparator (vs-budget column) — board reporting carries both.
3. **The LBE is never a benchmark.** It never appears in a variance column. A soft forecast used as a target recreates numbers-changing-without-explanation.
4. **Locks are versioned and disclosed:** plan of record vN, effective date, Cover disclosure, one cycle showing old and new where lines re-derive.

## Engine: plan-hash check, completed

Sanctioned change = a quarter-close lock executed through the ruling process (new version, expected diff, disclosed). ANY other plan diff = unsanctioned drift = blocking escalation (the incident case). The hash check now consults the lock calendar.

## The LBE artifact (Forecaster assembles, human ratifies, CEO reads)

One page, after M1 and M2 closes: quarter landing by P&L line and key metric · delta vs plan of record · top three drivers · open owner questions that move the number. Built as the roll-up of the variance commentary's forward implications ("Q3 LBE: (23k) vs plan" endings) plus the revenue outlook — the commentary contract's ending sentences are the LBE's line items. The quarter's plan figures are shown on the artifact (v11 gap: "I don't know Q3 planned number").

## Governance

- **LBE: draft-only PERMANENTLY** (low-frequency, high-judgment — the doc-19 profile that never leaves L0). Ratified by the human before the CEO sees it.
- **Soft ≠ unlogged:** every LBE stamped and retained. LBE vs actual quarter landing = the Forecaster's standing accuracy metric — a free back-test accruing every quarter, feeding the doc-19 evidence base and the walkthrough's "no forecast without a back-test" rule.
- **Lock approval is a human signature event**, recorded in the review ledger.

## Charter wiring

- **Analyst:** commentary endings quarter-scoped (already house style); endings tagged for LBE roll-up.
- **Forecaster:** owns LBE assembly (M1/M2) and the lock candidate (M3); **may not lock** — the human approves; accuracy metric reported each quarter.
- **Reporter:** board pack carries plan-of-record + budget memo; LBE never in the pack unless the CEO explicitly shares it.

## REPLACE-ON-INSTALL note

The cadence (quarterly lock, M1/M2 LBE) is Jonathan's practice and a sensible default; a real company may run different rhythm (semi-annual locks, monthly rolling). The **structure** (locked benchmark ladder + soft intra-period estimate + never-benchmark rule + sanctioned-change hash) is PACKAGE; the **calendar** is EXAMPLE.

## LBE layout spec (Jonathan, 22 Aug — from his sketch; decisions closed)

Columns: `Fcst Q` (plan of record, quarter) · `Variance` (expected delta vs plan = the roll-up of commentary forward-implication endings, plus revenue outlook) · `LBE` (= Fcst Q + Variance, always — the identity is a formula, never typed) · `Comments` (one clause per line: driver + open item if any).

Rows: Revenue · COGS · GM (with % beside $) · Opex by business owner (one row per cost centre: Finance, Legal, Engineering, …) · Operating profit · Non-cash · EBITDA.

Rules settled by the sketch:

- Opex granularity = COST CENTRE, not GL account. Each centre's Variance = sum of its accounts' commentary endings; drill-down to account level available on request via the Co-pilot, not on the page.
- Scope = P&L to EBITDA. No cash line (Controller's 13-week view remains the cash instrument).
- Open owner questions: LBE column carries the point estimate at the question's stated default; Comments flags the open item ("pending Field Ops: catch-up assumption").
- Sign convention follows the pack (costs negative, favourable variance reduces cost).

Versioning: one saved artifact per build — `LBE_Q3_M1`, `LBE_Q3_M2` — stamped, never overwritten. Accuracy metric compares each to the actual quarter landing at Q close; both versions score, so the metric also shows whether M2 LBEs beat M1 LBEs (they should — later information).

Tie rule: every Variance cell must trace to the commentary endings and revenue outlook that compose it — same sum-check discipline as the commentary contract: composition within 10% or the unexplained remainder is stated on the line.

---

## Build status (24 Aug 2026)

**Built and running.** Six pieces:

| Piece | Where |
|---|---|
| Lock calendar — budget lock, three quarter locks, status per lock | `example/data/plan_lock_calendar.csv` (EXAMPLE) |
| Benchmark ladder — `plan_of_record(period)` returns the latest LOCKED artifact and the budget memo comparator | `tools/plan_guard.py` (PACKAGE) |
| Sanctioned-change test — a diff is sanctioned only if a lock authorises it AND the ruling executed it; the block now names the lock it was expecting | `tools/plan_guard.py` |
| Endings tagged for roll-up — every commentary ending records the quarter delta it implies, its basis, and whether an owner question is open | `tools/drivers.py`, `F["lbe"]` |
| The artifact | `tools/build_lbe.py` → `deliver/sheets/LBE_Q3_M1.xlsx` |
| Accuracy metric | `tools/lbe_backtest.py`, `example/data/lbe_register.csv` |

**Q3 M1, built on information to the July close:** revenue LBE 1,358k against 1,425k of plan (−67k); EBITDA −1,447k against −1,376k (−71k). Nine of twelve cost-centre rows carry an open owner question, so nine of them sit at the question's stated default rather than at a prediction — which is what the ruling asks for and also the honest read of where the quarter is.

**The tie rule found something on the first run.** Two centres — Executive and Finance — carry a quarter variance that traces to no commented line, because each account's July move was below the commentary threshold while the centre's total was not. The line says so: *"+3.6k on lines below the commentary threshold — closed-month fact, open months at plan."* Untraced is not the same as unexplained, and the distinction is now on the page.

**One exclusion, stated on the artifact.** The +32k of capitalised software labour posted with no cost center is flagged for reclassification on the variance pack and is **not** forecast to an owner here. Putting it in a row would attribute it to somebody, which is precisely what is wrong with it.

**The back-test is armed and correctly refuses to score.** Q3 has two of three months closed, so `lbe_backtest.py` reports the build as held for scoring at quarter close rather than grading it against a partial quarter. At Q3 close it scores M1 and M2 against the landing and reports whether M2 beat M1.

**Not built, and deliberately:** the vs-budget memo column on the variance pack (rule 2). The board plan is on file and the ladder returns it, but adding a second comparator column to the pack is a layout change worth ruling on its own — where it sits, whether it carries its own commentary, whether a centre rollup shows both. Flagged rather than guessed at.

---

## Correction — the LBE test is absorption, not recurrence (25 Aug 2026)

**Jonathan, 25 Aug:** *"What do you mean by 'the variance recurs'? The question is: do we believe the variance that occurs in July will be absorbed/offset by the end of quarter? If yes, no change in forecast. If not, we need to adjust the forecast into LBE."*

The first build asked the wrong question. It filtered lines by whether the variance would **recur**, and dropped the ones that would not. That is a different and less useful test, and it is wrong in both directions: a variance can happen exactly once and still be sitting there at the quarter close, and it can repeat every single month and still net to nothing by the close. What the CEO is being told is where the quarter *lands*, so the only test that matters is whether the remaining months take it back.

### The rule as it now stands

Two questions per line, asked separately, both recorded with their reason:

1. **Will the rest of the quarter absorb the closed month's variance?** If yes, the forecast does not move and the variance is listed in the excluded block with the thing that absorbs it. If no, it stays in the forecast in full — a closed month is fact.
2. **Do the open months add MORE of the same?** A rate that changed keeps changing it. An amount nobody has explained licenses no projection either way.

```
LBE variance = (0 if absorbed else the closed variance) + further expected deviation
#                ^ "stays in"
```

### What counts as absorption

| Case | Absorbed? |
|---|---|
| Timing, and the offsetting month is **inside** this quarter | Yes — it nets |
| Timing, and the offsetting month is in the **prior** quarter | **No** — nothing in this quarter takes it back |
| A milestone due before the quarter close explains a schedule underspend | Yes |
| Unexplained, or named but not explained | No — and no projection either |
| A driver that moved and stayed moved | No — stays in, plus the trailing-3M rate on the open months |
| A one-off | No — it stays in once and adds nothing further |

The timing row is the one the correction actually turned over. The old rule said "timing nets and carries nothing" flat. The Lisbon forum was budgeted in June and posted in July; June is Q2. Q3 does not absorb it, and the engine now tests the quarter of the month it moved from before it claims the variance nets.

### What changed on the Q3 M1 build

- **9.6k of closed-month fact** that the recurrence framing dropped now stays in the forecast, across nine lines.
- **One line is genuinely absorbed:** 8030 legal, (909), because Harrow & Blake LLP's post-closing filings milestone is due in August, inside the quarter. It is the only entry in the excluded block, and it names what absorbs it.
- **EBITDA barely moves** — −1,428k against −1,427k — because the amounts that stay in largely offset each other. That is the point: the total was accidentally right and the per-line reasoning was wrong, which is the failure mode that survives a reconciliation and gets caught in a review.

### Terminology

`share-based pay` → **`stock comp`** on every line we author: the LBE non-cash row, the headcount model row label, the opex prose. Enforced by a house-lexicon rule. The GL is untouched — account 8095 keeps its own name and the journal descriptions keep theirs, on the standing rule that a house-style rule which renames a GL account is worse than the usage it was fixing.

`% of rev` now runs on **every row**, not only the margin subtotals, against the same revenue cell throughout — which is what makes the column addable down the page (cost of revenue −35.8% + gross margin 64.2% = 100%).


### Wording — sticks and materializes (Jonathan, 25 Aug)

*"I don't know what carries mean. Is it UK wording?"* — It was not British. It was jargon, and mine: a word doing work it had not earned. *"Can we use materialize or stick?"*

**Both, because the two halves of the LBE variance are not the same kind of thing.**

```
LBE variance = (0 if absorbed else the closed variance) + further expected deviation
                 sticks ──┘                                └── materializes
```

The closed month has already happened. It is in the ledger, it is fact, and the only question about it is whether it **STICKS** to the quarter close or gets absorbed. The open months have not happened, so nothing in them can stick — the question there is whether a further deviation **MATERIALIZES**.

Using one word for both would tell the reader the engine is equally sure of a number in the ledger and a number in a run rate. It is not, and the sentence now says so:

> *Q3 LBE: +21k vs plan — Jul sticks, plus +11k materializing on the open months at the trailing-3M run rate of 76k a month.*

The `F["lbe"]` field is `sticks`. A house-lexicon rule enforces both terms — deliberately narrowed to the intransitive sense (*"the closed month carries"*, *"it carries"*), because *"a real change to carry into the forecast"* is plain English. The first, broader version of that rule flagged exactly that phrase and silently suppressed a good comment on 7060, taking the pack from 17 comments to 16. **Second time a house-style rule has done more damage than the usage it was fixing** — the first renamed a GL account. Both were rules written against a phrase rather than against a sense.
