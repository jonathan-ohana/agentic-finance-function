# 19 — The self-improvement loop

*Written 17 Aug 2026. Closes the largest unspecified part of the governance model: how a workflow earns autonomy, and how the system gets better instead of merely staying automated. Input to Fable #3 (Day 6, charters) and the build target for the Day 9 governance demo.*

---

## The gap

Doc 03 gives the human "improving the system itself — refining agent charters, tightening the semantic layer, expanding autonomy where trust is earned." One clause. The governance model has an autonomy ladder — draft-only → execute-with-approval → autonomous-with-audit — and the metric registry carries version numbers.

Nothing says how a workflow climbs the ladder, what evidence counts, or what sends it back down. That is the load-bearing part, and it is the first thing an experienced CFO will push on: *"when exactly would you let it run without you?"*

It also undercuts the economic claim. "One person plus agents covers what took three or four hires" holds only if the system compounds. A static automation degrades as the business changes — new pricing, a new contract shape, a new entity — so without a learning loop the pitch describes a set of scripts that were correct in month one.

---

## Component 1 — The review ledger

Every human checkpoint already produces a decision. Today it evaporates. Capture it.

| Field | Contents |
|---|---|
| `review_id`, `timestamp`, `reviewer` | who and when |
| `agent`, `workflow`, `run_id` | what produced the output |
| `artefact` | journal entry, variance narrative, forecast, deck slide, cash view |
| `decision` | `approved` / `approved_with_edits` / `rejected` / `escalated_by_agent` |
| `edit_type` | `none` / `cosmetic` / `material_number` / `material_narrative` / `missing_item` |
| `edit_description` | free text — what was wrong |
| `root_cause` | `definition` / `process` / `data_quality` / `model_error` |
| `materiality_usd` | size of the correction, where it is a number |
| `agent_flagged_uncertainty` | did the agent say it was unsure about this? |

`agent_flagged_uncertainty` is the important column. An agent that was wrong *and said it might be* is behaving correctly. An agent that was wrong and confident is the dangerous one, and without this field the two are indistinguishable in the statistics.

---

## Component 2 — Metrics on the agents, not from them

| Metric | Definition | Why |
|---|---|---|
| **Acceptance rate** | approved with no edits ÷ total outputs | The headline, and on its own misleading |
| **Material correction rate** | outputs with a `material_number` or `missing_item` edit ÷ total | The one that matters for trust |
| **Mean materiality** | average USD size of material corrections | Distinguishes rounding from real error |
| **Escalation precision** | escalations the reviewer agreed were warranted ÷ escalations raised | Catches an agent that escalates everything to look safe |
| **Escalation recall** | 1 − (material errors the human caught that the agent did not flag ÷ all material errors) | **The dangerous one.** Measures what the agent missed |
| **Cycle cost** | model spend per completed workflow | Pairs with doc 06's cost-per-workflow instrumentation |
| **Cycle time** | agent start to human sign-off | Where the headcount claim is actually proved |

Escalation recall is the metric the whole governance story rests on and the one nobody instruments. An agent with a 95% acceptance rate and 60% escalation recall is *more* dangerous than one at 70% acceptance and 100% recall, because the first one is quietly wrong and the second one asks.

---

## Component 3 — Promotion and demotion, stated as rules

The ladder becomes testable. Criteria are per **artefact instance**, not per cycle — a monthly close would take twenty months to earn promotion if measured per close, but it produces hundreds of transaction categorisations a month.

| Level | What the agent may do | Promotion criteria | Demotion trigger |
|---|---|---|---|
| **L0 — Draft only** | Produces output; human reviews everything before it goes anywhere | Starting level for every new workflow | — |
| **L1 — Execute with approval** | Acts on approval, batch-reviewed rather than line-by-line | ≥200 artefact instances, material correction rate <2%, escalation recall 100%, ≥3 calendar months | Any missed material error, or correction rate >4% over 50 instances |
| **L2 — Autonomous with audit** | Acts without prior review; sampled audit after the fact | ≥1,000 instances at L1, material correction rate <0.5%, escalation recall 100% over the full period, ≥6 months, and a documented rollback path | Any missed material error, any audit sample failure, or a change to an input system |
| **Never** | Money movement, external communication, anything entering the signed financial record | — | — |

**Demotion is one strike.** Promotion takes hundreds of instances and months; demotion takes a single missed material error. That asymmetry is the point, and it is what makes the ladder credible to an auditor rather than a marketing device.

**Any material change to an input system — new pricing, new billing platform, a new entity — automatically demotes every affected workflow to L0.** The agent's track record was earned on data that no longer exists.

---

## Component 4 — Correction routing

Every correction has exactly one destination. Without routing, corrections live in one person's head, which is the failure mode the whole architecture claims to fix.

| Root cause | Destination | Artefact produced |
|---|---|---|
| **Definition** | Semantic layer | New version of the metric, with the triggering review ID and what changed |
| **Process** | Agent charter | Charter amendment — new check, changed escalation threshold, new input |
| **Data quality** | Source system or ingestion rule | Either a fix upstream or a validation rule that catches it at ingestion |
| **Model error** | Prompt, or a task moved up a model tier | Recorded against doc 06's tiering policy — this is where "cheaper model" decisions get revisited with evidence |

The rule: **a correction is not closed until it has a destination and an artefact.** A correction that only got fixed in this month's output will recur next month.

---

## Component 5 — The drift auditor

A scheduled agent whose only job is to find where the system is rotting. Monthly, alongside close.

- Metric definitions not reviewed in six months
- Registry entries still `UNRESOLVED` past their decision date
- Escalation rules that **never fire** (too loose) or **always fire** (too tight)
- Metrics with no named owner
- Workflows at L1 or L2 whose correction rate has drifted above the demotion threshold but which nobody demoted
- Source systems whose schema changed without a corresponding ingestion-rule update
- Definitions that changed *without* a triggering review ID — undocumented drift, the worst kind

An agent that audits the agents. Its output goes to the human, always, at L0 permanently.

---

## The two oracles

This is the part that makes the loop demonstrable rather than asserted.

**In the build, the oracle is the answer key.** `answer_key/` already contains what each agent is supposed to produce — the P&L, the balance sheet, the cash flow, the ARR schedule, the aging, the edge-case manifest. An agent's output can be scored against it automatically: accuracy per line, whether it found each planted edge case, whether it escalated the ones designed to require escalation.

**In production, the oracle is the human review ledger.** There is no answer key at a real company; the reviewer's edits are the signal.

Same loop, different oracle. That symmetry is worth stating explicitly in the case study, because it answers the obvious objection — *"your demo has an answer key, the real world doesn't"* — with an architecture rather than a shrug.

---

## Where the loop itself fails

A self-improvement loop has its own failure modes. Naming them is part of the design.

**Rubber-stamping.** Acceptance rate looks excellent because the reviewer stopped reading. Counter: periodic blind re-review of a sample already approved, and treat a sudden jump in acceptance rate as a signal about the *reviewer*, not the agent.

**Goodhart on acceptance rate.** An agent optimised for approval becomes maximally conservative and escalates everything. Counter: escalation precision is measured alongside acceptance, so caution has a cost.

**Small-N promotion.** Twenty clean monthly closes is twenty months. Hence per-instance criteria — but be honest that some workflows (the board deck, the annual plan) genuinely have small N and should probably never leave L0. Low frequency plus high stakes is exactly the profile that stays human.

**Definitional churn.** This is the real tension: the loop wants to improve definitions, and the field input says the core anxiety is *numbers changing without explanation*. Improvement and stability pull against each other.

Resolution: **change control.** Definitions change on a published schedule — quarterly, with the board pack — except for outright errors, which change immediately and are disclosed on slide 10 of the next deck. Every change carries a version number, an effective date, and a triggering review ID. Restated prior periods are shown both ways for one cycle.

That rule is what lets you tell a board "the definition of ARR changed this quarter, here is why, here is the number both ways" instead of them noticing the number moved and losing confidence.

---

## What this looks like in the sprint

**Day 6 (Fable #3).** The promotion and demotion table above is an input. Fable's job is to attack the thresholds — are 200 instances and 2% the right numbers, and which of the six agents should never leave L0?

**Days 6–8.** Every agent run writes to the review ledger, even when the reviewer is Jonathan approving in one click. The ledger has to exist from the first run or there is no history.

**Day 9.** The governance demo gets much stronger. Instead of "here is one caught error," it becomes: *here is the agent's scorecard, here is the error it missed, here is the demotion it triggered, here is the semantic-layer version that came out of it, and here is the check that now prevents it.* A closed loop, shown end to end.

**Day 10.** The case study line: *"the system is designed to get more autonomous only by earning it, and to lose autonomy automatically when it doesn't."*
