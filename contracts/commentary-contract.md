# 81 — Variance commentary contract v2 + gold exemplar pairs

*Ruled 21 Aug 2026 from Jonathan's line-by-line review of variance_FY26_9.xlsx ("Variance by account", cols Q/R). Five repeated corrections → one contract. Wire into the Analyst charter; add the sum-check to the engine. Companion to docs 78 (playbooks) and 19 (correction routing).*

## The contract (max three sentences per account comment, in order)

1. **Attribution first.** Open by decomposing the variance into signed dollar drivers that visibly sum to it: "(11k) volume: 10 courts installed vs 80 planned; rate on plan at 163." Business-cause language, not arithmetic narration. Drivers must sum to within 10% of the variance or the unexplained remainder is stated. Context may only follow attribution — a fact that doesn't explain part of THIS number doesn't belong in this cell.
2. **Persistence tag, compressed.** Recurring variance = one clause: "recurring — 6th month, ~4k/mo."
3. **Forward implication, always, closing.** Exactly one of: (a) no forecast impact + why; (b) reforecast candidate, quantified ("at current attainment, Q3 commissions ~15k under plan"); (c) closed-form question to owner per playbook protocol. "The assumption has moved" may never be an ending — only a quantified reforecast recommendation may follow it.

## Placement rules

- Rollup rows: one clause — "Driven by sales commissions (4% attainment)."
- Watch items (seats to reclaim, renewals, tier headroom) → separate Watch Items section, never inside a variance cell.
- Discretionary lines (events, sponsorship): answer "was this item in the plan?" first — budgeted-and-exceeded vs unbudgeted are different stories.

## Classification rules (new)

- **Timing vs Forecast miss:** an item that moved months is Timing only if the move postdates the last plan vintage. A reforecast that occurred after the move was knowable and didn't capture it → classify FORECAST MISS and say so. (Source: Lisbon forum, row 15 — the Jun reforecast should have moved it.)
- **Escalate, don't narrate, structural anomalies:** no plan / no cost centre / treatment contradicting CoA design → one line "flagged for reclassification: [reason]" + posting question to Bookkeeper. (Source: row 9 — IUS capitalisation belongs under the R&D cost centre via a contra account, not narrated as scenery.)

## Engine check (mechanical — runs before the pack renders)

Sentence-1 attribution figures must sum to column N within 10%. Failure = the comment does not ship. This converts the most frequent human correction into a check that never needs a human again.

## Gold exemplar pairs (before → after; teach by contrast)

**Row 13 · 7015 Sales commissions — add the forward look**
- AGENT: "Bookings 12k against 325k of quota — 4% attainment, from 11% in Jun. The plan carries full attainment. Under plan in every closed month — 6.1k a month against 24k planned, so not a Jul event."
- JONATHAN: "4% attainment in Jul vs plan at 100%. Q3 expected at x% attainment after Jul results. Q3 commissions expected xk under plan."

**Row 36 · 5045 Installation — the perfect shape (keep producing this)**
- AGENT: "10 courts installed against 80 planned (-87%) — volume variance -11k. Installation cost per court is on plan at 163."
- JONATHAN: "(11k) volume driven: 10 courts installed vs 80 planned in Jul. Installation cost per court on plan." *(format only: signed amount leads)*

**Row 54 · 5010 GPU inference — attribution format**
- AGENT: "228k matches analysed against 204k planned (+12%) — volume variance 7.6k. Inference cost per match 0.333 against 0.323 planned — rate variance 2.3k. It peaked at 0.413 in Jun…"
- JONATHAN: "+8k volume driven (+12% matches analyzed vs plan); +2k inference cost per match differential."

**Row 51 · 8070 Software — the failure case (never produce this)**
- AGENT: five interleaved facts (schedule gap, Figma seats, Amplitude headroom, persistence, assumption-vs-spend) — reviewed as "confusing and incomprehensible."
- JONATHAN'S PRINCIPLE: subscriptions tie item-by-item to plan; actual ≈ budget by construction; variance arises only from a missed prepaid entry, a renewal delta, or unexpected licenses. Lead with which one it is; seats/renewals → Watch Items.

## Correction-routing entries (doc 19)

| Correction | Destination |
|---|---|
| Attribution-first + sum rule | Charter (process) + engine check |
| Forward-implication mandatory | Charter (process) |
| Watch Items separation | Charter (output structure) |
| Timing vs Forecast-miss vintage rule | Shared method, doc 78 |
| Structural-anomaly escalation | Bookkeeper charter cross-reference |
| Row-51 software principle | Playbook 7 (confirms v0.2 red-line) |

---

## Amendment v2.1 (21 Aug) — ending-selection rules, from the v10 rerun review

**v10 verdict:** contract compliance achieved (attribution sums, escalation of row 9, Lisbon reclassified as forecast miss, gold format on row 36) — but judgment collapsed into template-filling: "reforecast candidate" stamped on 10 of 17 comments via single-month extrapolation, owner questions extinct (0 of 17), one internally contradictory comment (row 60: trend tag under plan, reforecast over plan, no explanation). Diagnosis: given three permitted endings, the agent always chose the computable one.

**New rules — the ending is determined by the playbook, not chosen:**

1. **Run-rate extrapolation is permitted only when ALL hold:** the account's playbook behavior is smooth or volume-driven; the variance is fully explained; the basis is trailing-3-month or YTD, never a single month. The reforecast sentence names its basis ("at trailing-3M run rate of X…").
2. **Milestone, event, and discretionary accounts** (Playbooks 5, 6, 8-volume): schedule-based restatement or owner question — never run-rate extrapolation.
3. **An unexplained variance always ends in an owner question.** No extrapolation of unexplained amounts (v10 row 64 violation: extrapolated a variance its own first sentence called unexplained).
4. **Sign-coherence:** a recurring-tag direction that disagrees with the reforecast direction must state the reason for the flip, or the comment fails. → New engine check alongside the sum-check.

**Escalation logged (to Bookkeeper, pack integrity — resolves before any v10 commentary is accepted):** July plan cells changed between v9 and v10 on some lines only (7050: 10,549→8,487; 7030: 23,345→15,480; Club Sales rollup: 75,025→72,963) while others held and actuals are identical. Suspected line-level comparator rebase or plan-extract change — violates the uniform-ruled-comparator rule on the Cover. Several v10 "new" variances (7050 flipping sign) may be benchmark artifacts, not business events.

**Iteration log:** v1 failed on attribution → contract. v2 failed on mechanical judgment → selection rules. Each failure narrower than the last; record as the improvement loop's worked example.

---

## Escalation resolved (21 Aug) — plan-comparator drift, root cause found

**Finding (forensic diff, v9 vs v10 Plan tabs):** plan version unchanged (Apr-26 Reforecast, identical headers). Two plan lines silently RE-DERIVED on a new basis, all 12 months each (24 rows): 7030 app store fees — base narrowed from "consumer share of plan revenue" to "plan's consumer subscription revenue" (Jul 23,345 → 15,480); 7050 partner commissions — blended courts rate replaced by named-partner contractual basis ("Global Racquet Partners — 15.0% of courts revenue it sourced", Jul 10,550 → 8,487). Club Sales rollup delta is exactly the 7050 flow-through. The v10 7050 variance sign-flip was a benchmark artifact, not a business event.

**Ruling required (Jonathan):** the new basis is methodologically better AND was adopted silently — the only wrong answer. Options: (a) RECOMMENDED — adopt via change control as "Apr-26 Reforecast r2": document the two-line re-derivation with rationale, show both bases for one cycle, disclose on the Cover; or (b) revert to v9 basis. Either way, log how the agent came to re-derive plan lines at all.

**Permanent control (engine):** hash the plan extract per run; any diff vs prior run = BLOCKING escalation with row-level diff attached; pack does not render until ruled. Plan values are inputs the Analyst reads, never recomputes.

**Review-ledger entry:** root_cause = process; destination = engine check + Analyst charter ("plan is read-only"); materiality = sign-flip on 7050 variance. Diary note: an unscripted, subtle, diagnostic failure — an agent improving plan methodology and thereby corrupting the variance — caught by human review, now caught by a hash check. The governance story, live.

---

## Amendment v2.2 (22 Aug) — learning acceleration + house lexicon, from the v11 review

**v11 verdict:** structurally close — 8 comments accepted with cosmetic trims, owner questions restored, trailing-3M basis landed. Remaining corrections split into three kinds routed to three channels; feeding all of them back as prose rules is the slowest loop and over-constrains (the v10 lesson).

### 1 · Accepted-commentary memory (the biggest lever)

Per account, store Jonathan's final approved wording each month. Charter instruction #1 becomes: **match the accepted exemplar for this account before applying any rule.** Rules carried the agent to ~80%; voice, horizon and phrasing are learnable only from exemplars, and every accepted month enriches the reference.

### 2 · House style (from Jonathan's v11 edits)

- **"LBE" (latest best estimate)** is the house term for the forward view — never "reforecast candidate."
- **Horizon = current quarter** ("Q3 LBE: (23k) vs plan") — never remaining-months-on-the-year.
- **Questions near-term and catch-up-framed:** "Should we expect a catch-up before end of the quarter?" — not schedule-arithmetic framing.
- **Rollups: one clause + cause in-line:** "(18k) — driven by (23k) 7015 sales commissions (4% attainment)."
- $ on unit rates ($163, $89); no restating figures the row already shows.

### 3 · House lexicon — US English, enforced by engine check

**Global setting: US English.** The agent currently writes UK finance idiom throughout. Banned → preferred (regex-checkable; a banned term fails the comment before render; list extendable by Jonathan at any time):

| Banned | Preferred |
|---|---|
| subscription schedule / register | **software agreements list** (Jonathan to confirm term) |
| charge / charged | **post / posted** (to the GL) |
| "the schedule doesn't carry X" | "**no agreement on file for [vendor]**" / "not in the agreements list" |
| licences | licenses |
| programmes | programs |
| enrolment | enrollment |
| analysed | analyzed |

### 4 · Playbook amendments (reasoning order)

- **Playbook 10 / benefits (8015):** mandatory decomposition FIRST — benefits = heads × PEPM; actual vs plan heads (hiring plan), then actual vs plan PEPM (elections, rates); only the residual after both escalates to the carrier invoice. Never open with a data-gap statement.
- **Playbook 7 / software (6040, 8070):** the closed explanation list is Jonathan's four causes — renewal delta · tool switch · license overage vs agreement · missed prepaid entry. Any posted amount not attributable to a vendor on the agreements list must be named VENDOR BY VENDOR with amounts — never aggregated into "on no agreement."

### 5 · Data-gap routing (out of the commentary loop)

The incomplete software agreements list and the enrollment snapshot are CLOSE ITEMS (Bookkeeper/data layer), not commentary failures. Added to the close checklist: build the agreements list from vendor-level actuals; obtain a dated enrollment extract or the carrier invoice. Until done, accounts 6040/8070/8015 are graded on escalation clarity only.

### 6 · Read-back protocol (process)

After each review, the agent immediately regenerates ONLY the corrected rows in-session for a same-day glance. Misreadings die in thirty seconds instead of surviving to the next close. (v11 example: Harrow & Blake LLP — Jonathan reads a slipped milestone with catch-up expected; the agent read the schedule as working. The read-back settles whose reading the data supports.)

**Iteration log addendum:** v1 attribution → contract · v2 mechanical judgment → selection rules · v3 voice + two reasoning bugs + data gaps → exemplar memory, lexicon, decomposition order, close-item routing. Edit types per round shrinking; next round is scored on style-match rate against the exemplar store.

---

## Refinement freeze (22 Aug) — ruling

Variance-commentary refinement on CourtIQ data is FROZEN after one final mechanism-test run. Rationale: the machinery (contract, selection rules, engine checks, exemplar memory, read-back, correction routing) is PACKAGE — done, portable, proof banked across three iterations plus the plan-hash incident. The calibration (voice, LBE, thresholds, accepted exemplars) is EXAMPLE — company-specific by nature and non-transferable; further polish trains the agent for a company that doesn't exist, while real-company calibration is cheap in situ by design (one review per close, shrinking monthly).

**Closing actions (~half day, cheap-model session):**

1. **Mechanism-test run.** Execute v2.2 once. Scored question: does the exemplar store pull Jonathan's accepted wording per account — not "is the prose good." Record the edit-count trajectory v1→v4 (v1 baseline ~17 rewrites). Stop regardless of result.
2. **Mark the seams.** Tag every CourtIQ-specific parameter in the playbooks and charter — thresholds, account numbers, owner names, the four software causes, the lexicon's confirmed terms — as `REPLACE-ON-INSTALL`.
3. **Day-one protocol (five lines, into the Analyst charter):** at a new company: month one is draft-only, 100% human review; exemplar store starts empty and fills only from the reviewing human's accepted wording; playbook parameters re-derived from the new CoA and plan; promotion clock (doc 19) restarts from zero — the track record was earned on data that no longer exists; lexicon re-confirmed with the new team's terms.

**Case-study note:** the freeze itself is exhibit material — knowing when refinement stops paying, and why fake-data calibration doesn't transfer while the learning machinery does, is the judgment being sold.
