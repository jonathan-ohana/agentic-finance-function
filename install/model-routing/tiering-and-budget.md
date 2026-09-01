# 06 — Model tiering and budget policy

**Status:** operating rule for all work in this project, from Phase 2 onward.
**Revised 23 Aug 2026** on the Opus 5 re-tiering — see doc 72. The principle
below is unchanged; only the names and the arithmetic moved, which is the
whole point of having written it down as a table.

## The principle

Same split the blueprint applies to humans: *the role shifts from producing analysis to directing and auditing.* Apply it to model choice too — **the top tier for the thinking, cheaper models for the producing.**

## The constraint that forces it

- Cap: **$15/month**, unchanged.
- **Opus 5 — $5/M input, $25/M output** — is the default thinking model.
- **Fable 5 — $10/M input, $50/M output** — is reserved for two or three adversarial tasks a month, where the output is a page and being second-best is expensive.
- Output is the expensive side. Any task with voluminous output is the wrong task for either of them.
- Budget reality: roughly **14 good thinking sessions per month** inside the same cap — about double the pre-swap shape, because the top tier halved in price on 24 July.

A workable month:

```
12 Opus 5 sessions   @ ~$0.75   =  $9.00
 2 Fable 5 sessions  @ ~$1.50   =  $3.00
                                  ------
                                  $12.00   ($3.00 headroom)
```

## Worth the top tier (high judgment-per-token)

1. **The deliberate failure case.** Success criteria require "at least one case where the agent fails and the governance catches it." The highest-leverage task in the project, and one of the two that stays on **Fable**: a weaker model produces a strawman — an obvious typo obviously caught. What's needed is a failure that is subtle, realistic, and diagnostic: the agent produces a *plausible wrong number* that survives casual review and is caught only because a specific checkpoint exists. Requires adversarial reasoning about our own system. Tiny output, enormous credibility payoff.
2. **The semantic layer.** The keystone, and the densest judgment-per-token artifact we'll produce. ARR movement rules across new / expansion / contraction / churn; COGS allocation boundaries; CRM stage → forecast mapping; whether a mid-year upsell with a co-terminated end date is expansion or new. Errors here don't announce themselves — they propagate silently into every agent's output. Low volume, high consequence. **Opus 5**, with a Fable pass over any ruling that restates prior periods.
3. **Red-teaming the blueprint before building.** The five docs are internally consistent and sourced from people who agree with us. Before spending four sprints: spend ~$2 having **Fable** attack the thesis. Where does Wave-4 "agentic-native" actually break? What does a skeptical Series A CEO say to "no team before Series C"? Where is the strongest honest case against the approach? Get the sharpest version of it in advance, not live. The second of the two Fable tasks.
4. **Agent charters and autonomy boundaries.** Six agents × charter, inputs, outputs, cadence, escalation, plus placement on draft-only → execute-with-approval → autonomous-with-audit. The design is the deliverable; the writing is short. A misplaced boundary is what an experienced CFO spots in the demo immediately. **Opus 5.**
5. **Edge-case design for the synthetic data.** *Which* eight or ten messes to build in, so each exercises a different failure mode. That's the design. Generating them is not. **Opus 5.**

## Not worth the top tier

- **Sprint 1 in bulk** — 18 months of GL transactions, 50 contracts, invoices, payroll records. A mountain of output tokens and the worst possible use of budget. **Write code to generate it**: deterministic, reproducible, tunable, and more internally consistent than any model produces by hand.
- Doc formatting, summarizing, source-gathering, and routine sprint execution once charters are defined.

## Operational note

Use the thinking tier in **short, dense, single-purpose sessions** where only the relevant doc is pasted in — not long agentic sessions that crawl files. Agentic sessions resend accumulating context every turn; input tokens compound fast even before output. A focused session runs ~$0.50–$1.00; a sprawling one can still eat the whole month, at half the rate, which buys twice as long to notice. **Cheaper models make the discipline less urgent, not less correct.**

**Cache the standing context.** The semantic layer, the active charter and the output contract are the same bytes in every session. A cache read costs **0.1×** the input rate and a one-hour write costs 2×, so the break-even is two reads and every sprint clears it on the first morning. This is now the largest remaining lever on builder spend, and it is a configuration change rather than a behaviour change.

**Batch what is not interactive.** 50% off, and the cheapest tier's work — extraction, categorisation, matching, reconciliation prep — is exactly the latency-tolerant workload it exists for. Batch and fast mode are mutually exclusive; nothing in the build needs fast mode.

## Instrument it — cost-per-workflow

Track model spend per workflow across the fake-company build. *"The close costs $2.30 in model spend; variance analysis $1.10"* is a slide no one else's demo has. It converts model-tiering discipline into evidence of exactly the judgment being sold — matching capability to task instead of pointing the most expensive thing at everything. Same graduated-autonomy instinct as the governance layer, applied to spend.

**Quote the ratio, not the model.** Cost figures now sit either side of the 24 July re-tiering and are not comparable across it. Any artefact carrying one must say which side of the line it is on, and the durable claim is the ratio — *top-tier judgment steps are 3% of tokens and 40% of spend* — which survives the next release. The model name does not.
