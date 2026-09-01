# 70 — Model routing doctrine: the right model per request

*Ruled 20 Aug 2026 (Fable). Extends doc 06 (builder-side tiering) to the product itself. Companion to docs 19 (self-improvement loop) and 68 (MVP spec).*
*Table re-tiered 23 Aug 2026 on the Opus 5 release — see doc 72. Structure unchanged; only the assignments moved.*
*The table now lives as a versioned file, `package/routing_table.json`, reviewed monthly under doc 73. The markdown below is the reading copy; the file is the one the tools read.*

## The ruling: a routing table, not a router

Work arrives through six charters whose workflows are known at trigger time, so model assignment is decided at design time, per workflow step, and versioned in the semantic layer like any other ruling. No runtime classifier for charter work — a dynamic router is one more nondeterministic component to govern; a table is auditable by reading it.

## Assignment principle: judgment density × verifiability

The engines already compute deterministically, so most volume never touches a model. For agent steps: **the cheaper the verification, the cheaper the model.**

| Tier | Model | $/M in · out | Steps | Why safe |
|---|---|---|---|---|
| Cheapest | Haiku 4.5 | 1 · 5 | Extraction, categorization, matching, reconciliation prep — **via batch** wherever the step is not interactive | Output lands in tie-outs; errors caught mechanically |
| Mid | Sonnet 5 | 2 · 10 | Variance commentary, close narratives, escalation write-ups | Human-reviewed drafts, medium per-instance stakes |
| Top | **Opus 5** | 5 · 25 | Causal attribution, anomaly interpretation, scenario reasoning, semantic-layer changes | No downstream check exists; plausible-wrong survives review (the failure-demo class) |
| Adversarial | Fable 5 | 10 · 50 | Red-teaming, failure-case design, attacking a ruling before it is issued | Peak reasoning *is* the deliverable; output is a page |

Two levers below the model choice, and for the workloads they touch both are larger than it: **batch** at 50% off on the cheapest tier, and **prompt caching** at 0.1× on a read for the standing context every agent receives. Batch and fast mode are mutually exclusive; nothing in the product needs fast mode, because nothing is waiting on a human.

## The finance-native rule: materiality routing

Dollar materiality escalates tier within a workflow — a $50k accrual estimate is not the same request as a $500 one. Four escalation triggers, each logged: validation check fails; model flags own uncertainty; out-of-distribution input (new vendor, unseen contract shape); materiality threshold crossed. Escalate one tier and re-run. Never downgrade silently.

## Self-improving, both directions

Doc 19's correction routing already carries `model_error → up a tier, with evidence`. Symmetric rules: **promotion to a better model is one-strike** (a single materiality miss on the cheap tier); **demotion to a cheaper tier is earned** (sustained perfect acceptance over N instances, then a shadow-checked trial cycle). The review ledger is the evidence base — the router is the self-improvement loop pointed at spend.

**A model substitution is a third case, and it is governed like a semantic-layer change**, not like a setting: shadow trial, scored evidence, versioned ruling, comparability note. Cost may never be a gate on its own. Doc 72 is the worked example.

**None of it happens unless it is diaried.** Doc 73 puts the table on a monthly review with five off-cycle triggers, and `routing_review.py` produces the candidates and the evidence from the usage log. Opus 5 shipped four days before this doctrine was written and went unnoticed for a month — a doctrine with no cadence on it is a paragraph, not a control.

## Circuit breakers and context discipline

Per-workflow token budgets in the charter; a run exceeding budget escalates to the human, never to a bigger loop. Agents receive semantic-layer excerpts, not whole documents — context volume is a cost decision made at charter design.

## The one true router: the ad-hoc surface

Free-form Co-pilot questions get a one-call cheap-model triage: lookup → cheap + tools; analysis → mid; judgment/advice → top tier or defer to human. Triage test: does the answer change a decision or enter the record? If yes, up-tier.

The triage is scored, not assumed: `copilot_evals.json` carries the expected tier on every case, and `copilot_eval.py` reports tier accuracy beside the behaviour gates. Tier accuracy is **reported and not gated** — a cheaper route that answers correctly is a finding to promote, not a fault to fix.

## Instrumentation (product surface + interview line)

Cost-per-workflow made real by the table: MVP screen 3 shows tier, escalation count, cycle cost beside escalation recall. Figures either side of a re-tiering are not comparable and must say which side they sit on. Principle: matching model capability to task materiality is the same graduated-autonomy judgment as the governance layer — spend is governed the way autonomy is: earned, evidenced, reversible.
