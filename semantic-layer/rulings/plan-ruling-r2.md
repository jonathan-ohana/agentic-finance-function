# 82 — Plan ruling r2, ready to enter · and why an agent did not enter it

*Drafted 24 Aug 2026 by the build agent at Jonathan's instruction. **Not yet in force.** The semantic layer says, in its own header: "Agents read this file; no agent writes it (template Rule 6)." This ruling is drafted here for a 30-second paste, not written into SL directly — in the same session that builds a control against an agent silently changing plan methodology, quietly writing to the governance file would be the identical failure wearing better manners.*

---

## SL-31 · Plan re-derivation and the version that governs a variance

**Kind** POL · **Status** RULED · **v1.0** · effective period 2026-07 · comparability: **Restates** the two lines named, all twelve months, both bases shown for one cycle

**The case.** Between the v9 and v10 variance packs, two plan lines were silently re-derived on a new basis while the plan version string, headers and actuals were unchanged. 7030 app store fees: base narrowed from a share of total plan revenue to the plan's consumer subscription revenue driver (July 23,345 → 15,480). 7050 partner commissions: a single blended rate on a share of total revenue replaced by the named-partner contractual bases in `partner_agreements.csv` (July 10,550 → 8,487). The Club Sales rollup delta is exactly the 7050 flow-through. The 7050 variance sign-flip in v10 was a benchmark artefact, not a business event.

**The ruling.** The new basis is adopted as **Apr-26 Reforecast r2**, effective the July 2026 close.

- **7030** is re-derived on the plan's consumer subscription revenue driver (`mrr_player`), not on a hardcoded share of total revenue. FY26 plan moves to 181,379.
- **7050** is re-derived on the named-partner contractual bases: one master distribution agreement at 3.2% of the whole courts subscription book, plus five referral agreements at 10–15% of the courts revenue each partner sourced — of which Global Racquet Partners at 15% is the highest rate. FY26 plan moves to 99,557.
- **Both bases are shown for one cycle**, r1 beside r2, on the variance pack's plan tab.
- **The Cover carries the disclosure** for that cycle.

**Reason.** Contractual accuracy. A commission is a contract, not an average; a rate on revenue is a rate on the revenue it is a rate *on*. The r1 bases were a hardcoded 36% and 50% share of the top line, typed into build code where no owner could see them, and both were wrong on their own terms — courts is 32% of the plan and consumer subscription 33%.

**One correction to the ruling as instructed.** The instruction described 7050's new basis as "Global Racquet Partners, 15% of sourced courts revenue". That is one of six agreements, not the basis. The ruling above states all six, because a versioned governance record that misdescribes what it rules is worse than no record.

**What it costs.** Two lines restate across twelve months. Every v9-basis variance on 7030 and 7050 is void — including the −26% "underspend" on 7030, which on the r2 basis is +11% over. Anyone who acted on the v9 reading acted on a benchmark artefact.

**The separate finding, which is the real one.** The agent re-derived plan lines at all. Plan values are an input the Analyst reads; recomputing them makes the comparator move under the comparison, and the pack cannot detect it because every consistency check still passes. Root cause is **process**, not definition. Destinations: an engine hash check (below) and a charter clause ("plan is read-only to the Analyst"). Materiality: sign-flip on the 7050 variance.

**Revisit when.** A further re-derivation is proposed — which now cannot happen silently, because the hash blocks it.

---

## Cover caveat, ready to paste

> **Plan basis — Apr-26 Reforecast r2 (effective Jul-26).** Two lines are re-derived on a contractual basis this cycle: app store fees on consumer subscription revenue, and partner commissions on the named partner agreements. Both bases are shown on the Plan tab for one cycle. Variances on 7030 and 7050 are not comparable to packs issued before this one.

---

## The permanent control, now in the engine

`tools/plan_guard.py`, called before the variance pack renders. It hashes the plan extract for the reporting months, compares that hash to the one named in `example/data/plan_rulings.csv`, and on any difference emits a row-level diff and **stops the build**. The pack does not render until the new hash is ruled and entered.

Entering the ruling is a human act, and the file it is entered in is the same one this agent declined to write.
