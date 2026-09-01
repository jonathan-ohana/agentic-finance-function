# 83 — Iteration log: v11, the first run under contract v2.1

*24 Aug 2026. One row for the review ledger, plus the new failure class — because there is always one, and it is always narrower than the last.*

## The row

| Field | Value |
|---|---|
| Run | v11 — first under doc 81 contract v2.1, plan basis Apr-26 Reforecast r2 (SL-31, draft at doc 82) |
| Owner questions | **8 of 17** (v10: 0) |
| Single-month extrapolations | **0** (v10: 10) |
| Comments touched on line review | **6 of 17** (v9: ~17) |
| Mechanical checks | 17 of 17 comply — attribution reconciles ≤10%, ≤3 sentences, forward implication present, basis named, signs coherent, no gap extrapolated |
| Watch items out of variance cells | 7 |
| New failure class | **Naming a gap counted as explaining it** |
| Root cause | definition — the attribution slot had no test for whether a driver named a cause or an absence |
| Destination | engine check (`_is_gap`, ending forced to owner question above 40% of variance) + charter |
| Materiality | 3 comments extrapolated an amount nobody had explained; 8070 projected +17k on the year off a driver that said only "on no agreement" |

## The failure class, stated properly

Three comments attributed the whole variance to a phrase describing an **absence**: *"2.9k a month is on no agreement"*, *"3.7k not in the enrolment file"*, *"licences off the schedule"*. Each reconciled to the cent, so the sum check passed. None contained a cause, so the unexplained-remainder rule never fired. The comment then extrapolated the amount across five months.

v2.1 rule 3 says an unexplained variance always ends in an owner question. **The rule was satisfied by relabelling the unexplained.** Not by evasion — the labels are accurate, and each names a real exposure — but a driver slot that accepts a description of ignorance has stopped being an attribution test.

The narrowing holds: *no attribution* → *mechanical judgement* → *naming a gap counts as explaining it*. Each failure is a smaller and more specific thing than the one before, which is what a converging loop looks like.

## What changed in the engine this run

1. **Plan hash, blocking.** `tools/plan_guard.py` hashes the plan extract for the reporting months and compares it to the hash a human ruled in `plan_rulings.csv`. Any difference raises `PlanDrift` with a row-level diff grouped by account, saves the new extract to `deliver/plan_snapshots/<hash>.csv`, and **stops the build**. Verified by perturbing one July plan row: the pack refused to render and named the row, the account and both values. The extract SUMS by account/centre/period rather than assigning — the plan carries one row per driver, and last-row-wins would have hashed a number nobody reports.
2. **Sign coherence, blocking.** A recurring tag whose direction disagrees with the forward implication must state the reason or fail. Two honest reasons are permitted and both are computed: the variance is closing, or the remaining plan has stepped up to where the line already is. Neither true means the comment is genuinely incoherent and the check fails rather than being handed a sentence that sounds like a reason. It fired on 7030 and produced the second reason, correctly.
3. **Ending selection by playbook, not by preference.** Run-rate extrapolation is permitted only on smooth or volume-driven accounts, on a trailing-3-month basis that the sentence names. Schedule- and decision-driven accounts — events, milestones, install pipelines, leases — end on the schedule or on a closed-form owner question with the default stated. Professional fees and subscriptions get different questions and different owners, because "which is it — a missed prepaid entry, a renewal delta, or unexpected licences" is not a question to ask General Counsel.
4. **Plan values are read-only to the Analyst**, enforced by (1) rather than asserted.

## The three counts, and what they do not say

The mechanical score is clean and the edit count fell from about 17 to 6. Both are real. Neither means the pack is right — a comment can comply with every rule in the contract and still be the wrong thing to tell a CEO, and the counts cannot see that. What they measure is whether the failure mode of the *previous* run has been closed, and it has.

The five edits behind the count of 6 were all one root cause, now fixed. The sixth was 7060's travel comment, which reports the Lisbon forum as a forecast miss and then asks an owner question about baseline cadence without saying that the misphased 2.6k nets against June. That is a real gap and it is on the next iteration's list, not this one's.

## Promotion readiness

Not claimed. The counts have improved twice in a row and the doc-19 L1 criteria accumulate from runs like this one, but two data points is a direction and not a trend. One more closed month under an unchanged contract is the cheapest evidence available; if the edit count holds at or below 6 with no new failure class, that is the read worth bringing to a judgement pass.
