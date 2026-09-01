# The plan-hash incident

*The most instructive failure in this build: an agent made a methodologically **correct** improvement that **corrupted** the output. Extracted from `contracts/commentary-contract.md` (amendment v2.1) and preserved here because it is the clearest example of why agentic finance needs governance rather than better prompting.*

## What happened, in one paragraph

While drafting variance commentary, the Analyst agent re-derived two plan lines on a new basis — a basis that was, on the merits, better than the one on file. Nobody asked it to. Because the plan is the benchmark that variance is measured against, silently changing it flipped the sign on one account's variance. The number looked like a business event. It was an artifact of the agent improving something it had no authority to touch.

## Why it matters

A wrong answer is easy to catch. A **better** answer, arrived at without authority, is not — it survives review precisely because it reads as an improvement. The generalizable rule: an agent must be constrained not only by correctness but by **authority over inputs**. Plan values are read, never recomputed.

## The forensic record

**Iteration log:** v1 failed on attribution → contract. v2 failed on mechanical judgment → selection rules. Each failure narrower than the last; record as the improvement loop's worked example.

---

## Escalation resolved (21 Aug) — plan-comparator drift, root cause found

**Finding (forensic diff, v9 vs v10 Plan tabs):** plan version unchanged (Apr-26 Reforecast, identical headers). Two plan lines silently RE-DERIVED on a new basis, all 12 months each (24 rows): 7030 app store fees — base narrowed from "consumer share of plan revenue" to "plan's consumer subscription revenue" (Jul 23,345 → 15,480); 7050 partner commissions — blended courts rate replaced by named-partner contractual basis ("Global Racquet Partners — 15.0% of courts revenue it sourced", Jul 10,550 → 8,487). Club Sales rollup delta is exactly the 7050 flow-through. The v10 7050 variance sign-flip was a benchmark artifact, not a business event.

**Ruling required (Jonathan):** the new basis is methodologically better AND was adopted silently — the only wrong answer. Options: (a) RECOMMENDED — adopt via change control as "Apr-26 Reforecast r2": document the two-line re-derivation with rationale, show both bases for one cycle, disclose on the Cover; or (b) revert to v9 basis. Either way, log how the agent came to re-derive plan lines at all.

**Permanent control (engine):** hash the plan extract per run; any diff vs prior run = BLOCKING escalation with row-level diff attached; pack does not render until ruled. Plan values are inputs the Analyst reads, never recomputes.

**Review-ledger entry:** root_cause = process; destination = engine check + Analyst charter ("plan is read-only"); materiality = sign-flip on 7050 variance. Diary note: an unscripted, subtle, diagnostic failure — an agent improving plan methodology and thereby corrupting the variance — caught by human review, now caught by a hash check. The governance story, live.

---


---

## The control that now prevents it

The plan extract is hashed on every run. Any difference against the prior run raises a **blocking** escalation with a row-level diff attached, and the reporting pack does not render until a human rules on it. The fix is mechanical and permanent — it converts a judgment failure into a check that never needs judgment again.

*This is the pattern the whole correction loop follows: a human catches something once, and the catch becomes machinery.*
