# 50 — Acting on the Fable audit: the front page, re-sequenced

**Date** 19 August 2026 · **Status** implemented and verified · **Source** doc 49

Fable's diagnosis was **sequence-within-the-page**, not volume — and it disproved the volume hypothesis with the attention budget rather than asserting it. Every tab had a legitimate home. The Exec Summary did not.

> *"The bottom third of the front page proves trustworthiness before the reader is told what to trust it about. Every sentence concludes; the page never does."*

That sentence is the audit. Nine of its recommendations are now in the engine.

---

## What changed

### 1 · The page concludes

**A verdict at row 7**, in the only red on the sheet, assembled with `TEXT()` off live cells:

> *"The recurring book shrank for a second month — churn removed $60,947 against $15,706 of new business; only $29,359 of FX held headline ARR flat. Burn accelerated to $582,465. On the only forward view that exists (MID, unratified), cash runs out Apr-28 and every scenario exhausts cash inside 24 months. **The decision this month is the raise timeline.**"*

Every figure in it is a reference. It cannot outlive the numbers it quotes, and it changes when the scenario toggle changes.

### 2 · The scorecard is six lines, not fourteen

**ARR · net new ARR · burn multiple · logo churn · gross margin · closing cash.** The other eight were duplicating the KPI tab verbatim.

**Burn multiple joins the front page; Rule of 40 leaves it.** Fable's reason for the eviction is the better half of the trade: *"F34 renders green ON TRACK while its own note predicts decay."* A metric that reads green for a reason its own footnote contradicts trains its reader to ignore the colour.

The burn multiple reads `n/a — no net new ARR` and is **forced to BEHIND**. Left to the generic rule it would have read `NO GOAL SET`, letting *the reason it cannot be computed* hide *the fact that produced it*. That needed a config field, `signal`, and the reason is recorded beside it.

### 3 · Colour selects again

Thirteen of fourteen scorecard rows carried a coloured chip. **ON TRACK now renders plain grey with no fill.** Amber and red appear only where attention is needed.

The result on July: three BEHIND (net new ARR, burn multiple, churn), two WATCH, one plain. **The line that matters is now the loudest thing on the page** rather than one of thirteen.

Red is reserved to two uses — the verdict, and a BEHIND chip. The DECISIONS header was a third; it is now grey. A third use is the fault the rule exists to prevent.

### 4 · The typographic scale is the right way up

Section heads were **9pt grey caps under 10.5pt body** — the reader's eye landed on the paragraph and worked backwards to the label. Now **22 / 16 / 14 / 11 / 10.5 / 9.5**: company, tab title, verdict and headline figures, section heads, body, notes.

### 5 · The charts carry the message

The revenue-and-gross-profit bars are **deleted** — they drew finding 1's misleading headline as a picture. Replaced with:

- **Net new committed ARR, 13 months** — the line the pack exists to surface
- **Cash: 13 months actual, then the MID forecast to zero**, with the cash-out month named in the caption

Both anchored below the scorecard, and the chart-source blocks moved to row 100. The old anchors floated over the audit-trail text at B82:B85 with their own caption underneath them.

### 6 · The decisions are re-ranked, and the raise comes first

Previously: comparator ruling, close signature, forecast, VAT, churn. **Now the raise leads, with the arithmetic**:

> *"Cash goes negative **Apr-28** on the live scenario. Working back: a term sheet must be signed by **Oct-27**, so the process must be in market by **Jun-27**. Indicative new capital is **$3,280,291** — peak shortfall plus six months of buffer, **NOT an ask.**"*

The comparator ruling drops to fifth, which is what pays for the new content.

### 7 · The strategic gap: the raise clock

Fable's §7, and the sharpest structural finding. The pack computed the amount and the deadline and **never the date the work starts** — the only one of the three that is a diary entry. Two formula rows on the Forecast headline block: cash-out less a six-month buffer gives the term-sheet date; less a four-month process gives the in-market date.

`Apr-28 → Oct-27 → Jun-27`. Fable estimated ≈Q2-27 by hand; the formula lands in the same quarter.

### 8 · CAC is suppressed where the feed is broken

`FEED DEFECT — SUPPRESSED` in any period where the consumer book records no acquisition.

**This settles the disclosure question I had answered unilaterally twice.** Fable's ruling:

> *Disclose the gap on the face — yes; print arithmetic built on it — never; in a real company, verify the feed before the CEO sees the pack. **Feed artefacts are ops tickets, not board topics.***

I had been printing $17,483 and $43,342 with a caveat beside them. A number that will be quoted survives its caveat; the caveat does not survive the quotation. The disclosure moves to decision 2 on the front page — verify the feed — which is where an ops ticket belongs when it has reached the board.

### 9 · CRM pipeline named as the next connector

Bookings and pipeline coverage are the forward revenue indicators a Series A CEO asks for and this pack cannot produce. **Named on Lineage as the next connector, not estimated** — a pipeline figure derived from anything but the CRM is a guess with a chart.

---

## What I did not do, and why

**Plant club churn events in the generator.** Fable is right that zero churn across 239 club logos over eighteen months is the least convincing thing in the dataset, and right that fixing it unlocks LTV-Club and de-absurdifies the HIGH scenario's observed zero.

It is not a presentation change. Regenerating moves every figure in the close pack, the variance pack, the forecast pack, the review ledger's cited instances and the board deck — and **the loop evidence in those artefacts is the portfolio, not the numbers.** Same reasoning that held for defect 23, and the same answer: it needs a decision, not an assumption. Costed below.

**ARPA noise.** Fable marked it optional; it is cosmetic against a hard stop at Day 10.

---

## Verification

**5,993 formulas, zero errors.** **176 numeric zero-check cells across fourteen checks, all reading zero.** Every P&L, balance-sheet and cash-flow line still reconciled to the answer key. 89/89 generator checks pass. `grep` for this company's vocabulary in the engine returns zero.

The Exec Summary went from 87 rows to 137 — **and that is the point**. It holds less in the two-minute zone and more below it. The first thirty rows now carry a verdict, six headline lines, a six-row scorecard and two charts; everything that was competing with them sits underneath.

---

## What Fable got right that I would not have found

Three things, and each is a class of error rather than an instance.

**The volume hypothesis was falsifiable and it was false.** Jonathan and I both suspected the pack was too big. Fable tested it with an attention budget, found every tab had a home, and located the fault one level down. *"Volume disproved at pack level, confirmed at page level."* I would have cut tabs.

**Signal saturation.** Thirteen of fourteen chips coloured means colour has stopped selecting. I built the conditional formatting and never counted how many rows it fired on. The fix — ON TRACK renders plain — is one line and changes the page completely.

**The audit trail as an obstacle.** This project's whole thesis is that the audit trail is the differentiator. Fable's closing line is the correction that thesis needed:

> ***"The audit trail is the moat — it just has to stop standing in front of the message."***

---

## Carried forward

- **The club churn decision** — cost stated above, decision outstanding.
- Fable's lines-not-to-cross are now the standing constraints on this pack: which scenario is true, the raise amount as an ask, the NRR proxy discipline, and any business interpretation of the consumer zeros before the feed is verified.
- Remaining sprint: the Controller, the Day 9 recording, and Day 10 packaging including the one-page lead artefact.
