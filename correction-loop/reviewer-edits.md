# 45 — The reviewer's edits, captured into the engine

**Date** 18 August 2026 · **Status** merged and verified · **Prompted by** a marked-up pack from Jonathan

> *"Here's the last version of the mgt reporting pack that I tweaked. Please capture all updates"*

Sixteen tabs went out; seventeen came back. Diffing the two workbooks found a new tab, a complete design-system change, seven charts, thirty conditional-format rules, **two of my formulas that were wrong**, and **one defect he found and deliberately left for me to decide on**.

All of it is now in `reporting_pack.py` and `mapping.json`. None of it is in the workbook by hand — which is the test that matters: an edit captured into the engine survives next month's rebuild, and an edit left in the file does not.

---

## The two formula errors

**1 · Percentage-point deltas rendered as zero.** My margin MoM cell was `=N24-M24` with a `0.0"pp"` format. The value is a fraction, so a real 2.4-point move rendered as **`0.0pp`**. He wrote `=(N24-M24)*100`.

Three cells: the P&L's MoM column and the quarterly sheet's QoQ and YoY on the margin row. Every one of them printed `0.0pp` for thirteen periods and I did not notice, because a zero in a delta column looks like *no change*, which is the most plausible thing a delta column can say. That is the whole failure: **a wrong number that agrees with your prior is invisible.**

**2 · The operating expense bridge attributed nothing.** He found this and wrote the caveat himself, on the Bridges tab, as a live formula:

> *"The base at C27 is a hardcoded zero, not the plan total of $803,094. The tie check at C33 still reads zero because the residual at C31 absorbs the entire plan. A passing check here is not evidence of attribution."*

He was right, and the cause was a comment I left in my own code — `# the opex bridge's plan bar is the sum of the three function plan lines` — describing a thing I never implemented. `plan_key=None` made the plan bar `=0`, the three function movements carried the full actuals, and a residual of −$803,094 swallowed the plan. **The tie check read zero throughout.**

Fixed: `plan_key` now accepts a list, so a bridge against several plan lines states their sum. The opex bridge now reads plan −$803,094 → R&D +$2,514 → S&M +$29,880 → G&A +$630 → **residual nil** → actual −$770,070.

**The lesson is sharper than the fix.** This project has spent two days building check rows on the argument that a formula cannot be true by assertion. Here was a check that read zero in every period, was a genuine formula, and certified nothing — because the residual is *defined* as whatever closes the gap. A tie check proves arithmetic closure. It does not prove attribution, and I had been treating the two as the same thing.

His note on it is the model response:

> *"Not corrected here — fixing it changes reported figures, which is the preparer's decision, not a formatting one."*

---

## Exec Summary — the tab that was missing

Seventeen tabs and no entry point. A reader who does not already know where to look learns nothing from completeness.

| Block | What it does |
|---|---|
| **The headline** | Six figures with prior month, MoM, and a read-through sentence built with `TEXT()` off live cells |
| **Scorecard** | Every KPI against the quarterly goal, with a `FLOW` / `BALANCE` basis, a declared polarity, and an `ON TRACK` / `WATCH` / `BEHIND` signal |
| **What actually moved** | Five findings, each a live figure plus a sentence assembled from the cells it describes |
| **Decisions required** | Five, each pulling its text from the Cover's own caveat rows |
| **Integrity** | Every check row in the pack, reduced to its worst period, reading `PASS` or `BREAK` |
| **How to trace any number** | The chain from extract to statement to KPI to this page |
| **Two pictures** | Revenue and gross profit; closing cash and committed ARR |

Three things in it are better than what I would have built.

**The narrative is formulas.** Not *"tournament revenue fell $111,850"* typed into a cell, but `="Tournament revenue went from "&TEXT('P&L'!M10,"$#,##0")&...`. A typed sentence outlives the number it describes; this one cannot. It is the same principle as the check rows, applied to prose — and I had not thought to apply it there.

**`FLOW` versus `BALANCE`** is the sharpest idea in the file. One month into a quarter, a flow line should read a third of goal and a balance line should read all of it. Applying one test to both is how a scorecard marks every cash line `BEHIND` in month one and teaches its reader to ignore the column. Both the basis and the polarity are blue, declared per KPI in `mapping.json`, and grouped out of the way at columns I–K:

> *The only typed cells are the Basis and Polarity columns of the scorecard... They are rulings about how to read a part-quarter, not data.*

**Polarity had to become a ruling rather than a derivation.** I had been deriving it from each KPI's `goal_direction`, which made headcount below plan read favourable — the same arithmetic that makes an underspend look like discipline. He set headcount to `+1`. Under-hiring against plan is a miss. Only a human can say which way a line points, which is exactly why it is blue.

**The integrity block generates itself.** The engine now sweeps every sheet for rows whose label contains `CHECK`, applies the conditional format, and emits one line per check onto the summary with its span and its address. Eleven checks, found rather than listed — so a check added later appears without anyone maintaining a register.

---

## The design system

Adopted wholesale. Arial 10 → **Segoe UI 10.5**, and every colour off the primaries:

| | Was | Now |
|---|---|---|
| Formula | `#000000` | `#101828` |
| Link to another tab | `#008000` | `#067647` |
| Extract | `#9A5B0E` | `#B54708` |
| Human input | `#0000FF` | `#175CD3` |
| Notes | `#6B7280` | `#98A2B3` |

**And the navy header bands are gone.** That is the change I would have argued with and would have been wrong about. A filled band draws the eye to the label rather than the number, and a schedule carrying ten of them reads as ten tables instead of one statement. Section rules are now small grey caps over a hairline. Hairline borders under every detail row are gone too — with the numbers properly aligned the eye does not need them.

Subtotal *values* are now bold, not just their labels. Ratio rows read grey rather than black, so a percentage does not compete with the currency beside it.

## Conditional formatting

Thirty rules, and the instinct behind them is right: **a check nobody looks at is a check that does not work.** A yellow cell reading `0.00` is a cell the eye learns to skip. Now every check row is green when it reads zero and white-on-red when it does not, every KPI status carries its own colour, and the headline MoM column is green or red by direction — with the direction set per line, so a smaller loss reads green.

## Charts

Seven, each drawn off a **chart-source block of formulas** rather than pasted values — a chart built on a copy is a chart that stops agreeing with the statement it illustrates. Revenue by segment, cash flow and closing cash, committed and net new ARR, what moved the ARR book, and the two on the summary.

One of his notes is a rule I should have written myself:

> *The expansion / contraction leg reads n/a on this book and is therefore ABSENT from the chart rather than drawn as zero. A leg that cannot be measured is not a leg that measured nothing.*

That is the `null`-not-zero rule from the scorekeeper, arriving in a place I had not thought to apply it. It is now in the engine.

---

## Verification

**3,891 formulas, zero errors. 171 numeric check cells across eleven checks, all zero.** Every P&L, balance-sheet and cash-flow line still reconciles to the answer key. 89/89 generator checks pass. Seventeen tabs, seven charts, sixteen blue cells plus the declared basis and polarity columns.

---

## Defects 27 and 28

**27 · Percentage-point deltas were computed on fractions and rendered `0.0pp` in every period.** Found by the reviewer. Wrong in the direction that reads as *no change*, which is why it survived a build, a rebuild and two verification passes.

**28 · The operating expense bridge started from a hardcoded plan of zero**, so its residual absorbed the entire plan while the tie check read zero. Found by the reviewer. Cause: a comment in my code describing an implementation that did not exist. **A tie check proves arithmetic closure, not attribution** — and the pack now says so on the Bridges tab as well as in the engine.

---

## What this says about the loop

Every defect before these was found by an agent, a tool, or me. **These two were found by the human reviewer, in the artefact, by reading it** — and one of them he diagnosed to the cell and then declined to fix, on the correct grounds that changing a reported figure is the preparer's decision.

That is the review ledger working outside the review ledger. The right next move is to put it inside: these two belong as entries against the Reporter with `found_by: human review`, which is the only route by which the ladder ever learns that a check can pass and still certify nothing.

## Carried forward

- The two defects should be filed as review-ledger entries against the Reporter, not just recorded here.
- Defect 20 — `variance.py`'s hardcoded segments — is still the only place the package knows this company.
- The board deck does not yet reference the Exec Summary. Slide 1 leads with ARR; the summary page is a better citation target for the TL;DR than three separate tabs.
