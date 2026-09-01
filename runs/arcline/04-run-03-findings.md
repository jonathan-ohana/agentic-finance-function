# 89 — Arcline run 03: the speed architecture, and what it found

**Instance** Arcline AI, Inc. · **Period** 2026-01, closed and signed, ten adjustments posted
**Run** 03 (post-engine, four-way fan-out) · **Predecessor** doc 87 (run 01), doc 88 (v2 fixes)

---

## Why this run exists

Run 02 took roughly twenty minutes of wall clock for a single January variance analysis, and Jonathan's
response was the right one: *"The workflow needs to be faster."* Twenty minutes is not a demo problem.
It is the product problem. A controller who has to wait twenty minutes for a flux analysis will open
Excel instead, and the tool never gets a second use.

The diagnosis was not model speed. It was that a single agent was spending its context re-deriving the
P&L from nine thousand journal lines before it could form a single judgment. Arithmetic was eating the
thinking budget.

## The architecture

**One sentence: computation belongs in the engine, judgment belongs in the agent.**

Two changes, and they compound.

### 1. A precompute layer (`varianceengine.py`)

The engine joins actual to the bottom-up vendor budget at vendor grain and emits four tables before any
agent starts. They are written to the **work directory**, not the finance folder — see *One deliverable*
below:

| Table | What it holds |
|---|---|
| `variance` | 111 account × vendor rows, 37 above materiality, each carrying the budget's own basis / driver / owner |
| `variance_decomposition` | volume × rate on the driver accounts, heads × rate on payroll |
| `variance_signals` | 20 mechanical signals — accrual pairing, control exceptions, renewal uplift, idle seats |
| `variance_trend` | 53 accounts with trailing-3m, FY25 average, coefficient of variation, smooth/moderate/bumpy |

None of it is judgment. All of it is arithmetic the agent would otherwise have done by hand, badly, at
the cost of its own context.

The trend table matters more than it looks. A coefficient of variation is the cheapest possible test for
"is this a trend or a calendar", and it is exactly the test step 2 of the ladder (doc 78) asks for. The
agent no longer has to pull twelve months to answer it.

### 2. Four-way fan-out by slice

Revenue and cost of revenue · R&D · S&M · G&A and below. Each slice reads the four engine tables, not the
ledger, and returns rows against a typed contract. A merge step normalizes and renders.

## What it cost

| | Run 01 / 02 | Run 03 |
|---|---|---|
| Longest path, wall clock | ~20 min | ~11 min |
| Tokens per agent | 205k | 100–128k |
| Agents | 1 | 4 + merge |

**I estimated 4–6 minutes and it came in at 11.** Worth being honest about: the fan-out removed the
arithmetic but the slices are still doing real reading, and the merge is serial behind the slowest of
four. The next reduction is not more parallelism — it is narrowing what each slice reads.

## One deliverable, not six

The engine's four CSVs shipped into `03-actuals/FY2026/` beside the workbook, the merged detail CSV and
the commentary markdown alongside them. Jonathan opened the folder and found **six files named
`variance_*`** and asked the obvious question: why so many, I need one.

He is right, and the mistake is a specific one worth naming. *Engine output is agent input. It is
plumbing, not a deliverable.* I had let the pipeline's internals surface in the folder a controller
actually browses, and the effect was to bury the only file anybody opens under five files that look
exactly like it.

Now: the engine writes its CSVs to `/home/claude/work` where the agents read them, and the single
delivered artifact is `variance_analysis_2026-01.xlsx` with seven tabs — **Commentary** (the narrative,
first, because that is what gets opened), **Flux analysis** (63 classified lines, the bridge at top),
**Taxonomy**, then **Variance detail** (all 111 rows including below-materiality), **Decomposition**,
**Signals**, **Trend** as the evidence behind it. Nothing was dropped; it stopped being loose.

Guarded by a check, so it cannot drift back: *January variance analysis is a single deliverable* fails if
`03-actuals/FY2026/variance*` matches anything other than the one workbook.

The general rule, and it should hold for the product too: **the number of files in the output folder is a
design decision, not a byproduct of the pipeline.** Every intermediate that leaks into the deliverable
folder is a small tax on the one human who has to find the right file.

## Two contract failures worth keeping

Both are my fault, both are cheap to prevent, and both will recur in any fan-out design.

**Three of four slices wrote prose into a numeric column.** `lbe_effect` was specified without a type,
so three agents wrote sentences into it. Fixed by splitting the field: `lbe_effect_usd` (plain signed
number) and `lbe_note` (prose). *An unspecified column type is a specification defect, not an agent
defect.*

**Three slices coined their own permanence vocabulary** — Permanent / Temporary / Reverses / Recurring /
Non-recurring — even though doc 82 fixes the register at `sticks` / `absorbed` / `materializes`. The
merge normalized it. But a shared lexicon that lives only in a doc the agent was not handed is not a
lexicon. It has to travel in the contract.

## What the run found

### In my generator (found, fixed, rebuilt)

1. **Commission budget ignored the opening deferred balance.** The FY26 plan amortized new cohorts only.
   Fixed: opening balance runs off, each planned cohort adds to it.
2. **Bonus and PTO were unplanned.** Both post to the salary account, so the loaded rate the budget
   implied was below the rate the ledger produced — a permanent phantom favorability in every payroll line.
3. **Five accounts had actuals and no plan line at all** (6070, 6080, 9000, 9020, 9030). A variance
   against a budget of zero is not a variance.

### In the signed period (recorded, not rebuilt away)

**USD 67,500 accrued twice.** ADJ-2026-01-005 through -008 accrued four post-cut-off invoices —
Meridian Brand Agency, Cooley, Thoughtbolt, Robert Half — and every one of those vendors already had a
January bill posted for the same service period.

I chose to leave January signed and carry this as a finding rather than regenerate the period. That is
the right call for two reasons. It is a true control failure of exactly the kind the instance exists to
surface — *the cut-off review is both the control that should have caught it and the process that
produced it* — and a signed period that gets silently rebuilt when something ugly turns up is not a test
instance, it is a demo.

### Still open in the generator

- **The prepaid release schedule does not tie to contracted ACV.** Eight G&A subscriptions release at
  exactly 59.03% of ACV/12; R&D releases at 120.77% and steps 4.0% in January, which straight-line
  cannot do.
- **Interest income prints exactly USD 70,000 three months running.** It reads as a plug because it is one.
- **`variance_signals` false-positives on contra account 6080** — "expense account in credit" fires on an
  account whose credit balance is correct.
- **The post-close inbox picks vendors that already have a January bill** — the root of the USD 67,500.

## Three infrastructure lessons from the sync

None is about FP&A, all three are about running an agentic workflow over a generated dataset.

**The close working paper stopped shipping and nothing noticed.** It was only written while the period
was open, so closing January silently dropped the file the close is evidenced by. It now ships worked —
the ten approved entries in the JE columns and the JE tab — as the record of what was posted.

**A rebuild destroyed a full run of agent output.** `emit.py` rmtree's the output folder, which is
correct — a generated instance should be reproducible from source and nothing else. But the agents were
writing their deliverables *into* that tree. One rebuild and a run's work was gone (recovered only
because a sync zip happened to predate it). Fixed with `overlay.py`: agent deliverables live outside the
generated tree and are laid over it after the build, and the overlay **raises on a path collision** —
two owners for one path is how a file silently reverts.

**A green check was passing on nothing.** The determinism scan globbed `_generator/*.py` in the *output*
folder. The mirror step was a manual copy I had stopped running, so the glob returned empty and the
check passed vacuously. Fixed twice over: the build now mirrors its own source, and validate asserts the
mirror is populated before scanning it. *A check that can pass on an empty set is not a check.* Same
failure class as doc 88's orphan detection comparing disk-before to disk-after.

Validation now stands at **39 checks, 0 failed, 164 files**.

## What this says about the product

The precompute layer is the transferable idea, and it is worth stating plainly because it is the thing
an incumbent copilot does not do.

A copilot bolted onto a planning tool answers questions *about* the numbers by querying them. This
design computes the full variance surface — every account × vendor cell, both decompositions, the trend
statistics, the mechanical exception signals — *before the conversation starts*, and hands the agent a
board rather than a database. The agent's entire budget goes to the part a human actually wants: which
three of these thirty-seven lines earn prose, what each one means for the quarter, and who has to answer
for it.

It also happens to be the reason the analysis got faster. Those are the same fact.

And the corollary from the six-files episode: **the user never sees the board.** They see one workbook.
Everything the engine computed is in it, arranged so the narrative is the first tab and the evidence is
behind it. A pipeline that is proud of its intermediates ships them; a product hides them.

---

**Next:** the vendor spend review agent (PL-09 to PL-12) is still unfired, the reporting pack agent is
still unbuilt, and the sealed month protocol remains unarmed.
