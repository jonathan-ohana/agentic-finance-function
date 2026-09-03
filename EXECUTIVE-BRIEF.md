# Executive brief: from finance automation to a governed finance function

## The decision

Run a 30-day, read-only pilot on one completed month-end close if the company has reliable exports, a named finance owner, and leadership willing to rule on metric definitions.

Do not buy this as “AI that replaces finance.” Evaluate it as a control and judgment layer that makes a lean finance team faster, more consistent, and easier to audit.

## Why this matters

Most finance automation stops at moving and classifying data. The hard work begins where the ledger ends:

- Which ARR definition is valid for this audience?
- Is a variance caused by price, volume, mix, timing, or missing evidence?
- Which close exceptions can be carried, by whom, and until when?
- When has an agent earned the right to act with less review?

This prototype turns those decisions into versioned assets: definitions, rulings, playbooks, output contracts, evidence requirements, review history, and promotion or demotion rules. The aim is not a clever answer. It is a finance function that does not quietly change its mind.

## What is demonstrated

| Claim | Published evidence | Executive implication |
|---|---|---|
| Agents produced a close, variance analysis, management pack, and reforecast | [Management reporting pack](outputs/management-reporting-pack.md), [run log](runs/run-log.md), and two downloadable workbooks | The workflow reaches a decision-ready output, not just a chat response |
| Numbers are governed by explicit definitions and rulings | [Definitions](semantic-layer/definitions-instance.md) and [rulings](semantic-layer/rulings/) | Metric disputes become decisions with owners and history |
| Human corrections persist | [Loop verification](correction-loop/loop-verification.md) | Review effort can compound instead of repeating every month |
| Known failure modes are tested and retained | [What broke](what-broke/) and [red-team findings](red-team/audit-findings.md) | The control model is shaped by observed failures, not hypothetical safety claims |

The evidence is strong for a prototype and deliberately narrow: one simulated company, a second synthetic portability instance, one operator, and self-grading. It does not yet prove production reliability, economic ROI, or control effectiveness on real books.

## The operating model

```
Exports → preflight gate → semantic rulings → agent workflow → controller checks
                                                        ↓
Human approval ← exceptions + evidence ← decision-ready output
       ↓
review ledger → versioned rule or exemplar → next run
```

Six controls carry most of the risk reduction:

1. **Read-only source access.** Agents cannot post journals, pay vendors, or alter source systems during the pilot.
2. **A hard data gate.** No production run proceeds when required inputs or periods are missing.
3. **One governed definition per reported metric.** Ambiguity results in a question or refusal, not a best guess.
4. **Provenance on observed and derived facts.** A value read from a source is distinguished from one calculated by the system.
5. **Approval at the output boundary.** Agents produce the work from day one; a human decides when it counts.
6. **Earned autonomy by workflow.** Review can decrease only after clean runs, and known failure modes trigger demotion.

## A decision-grade 30-day pilot

### Scope

Choose one legal entity, one completed month, one management reporting pack, and no source-system writes. Include the general ledger, chart of accounts, bank, billing or receivables, payroll, CRM, budget, and available contracts.

### Baseline before the run

Record the current close duration, human preparation hours, number of post-close corrections, number of unsupported management-pack figures, and age of unresolved exceptions. These are the economic and control baselines; model output volume is not.

### Pass gates

| Gate | Pass condition |
|---|---|
| Data readiness | All mandatory inputs mapped; missing inputs explicitly block or degrade a named output |
| Financial integrity | Pack ties to the approved source balances; every material check passes |
| Traceability | 100% of material reported figures resolve to a source, governed definition, or disclosed derivation |
| Exception control | 100% of carried exceptions have impact, owner, due date, and consequence of non-resolution |
| Judgment safety | No contested definition is silently selected; no unverified cause is presented as fact |
| Review quality | Zero critical issues escape the human review into the approved pack |
| Repeatability | The second run reproduces accepted rules and does not repeat corrected errors |

Time savings and close acceleration should be measured, but they are not substitutes for these gates. A fast pack with an untraceable number fails.

### Stop conditions

Stop or narrow the pilot if source totals cannot be reconciled, required definitions have no accountable decision-maker, the workflow needs write access to demonstrate value, or reviewers cannot reproduce material claims from the evidence provided.

## The 90-day product path

| Horizon | Product outcome | Promotion evidence |
|---|---|---|
| Days 0–30 | One supervised close and management pack | Data gate passed; pack approved; defects and reviewer edits logged |
| Days 31–60 | Repeated close plus first live reforecast | Prior corrections applied; stable definitions; review time and exception aging measured |
| Days 61–90 | Scheduled monitoring and selective lower-touch review | Clean-run history by workflow; demotion triggers tested; second reviewer can operate the process |

Move to a hosted service with role-based approvals when multiple finance users, audit requirements, or non-finance self-service make a desktop workflow insufficient. The semantic layer, charters, contracts, and correction ledger should remain portable; the host should not be the control system.

## The product roadmap, in order

1. **Prove the real-company loop.** One design partner, three closes, independent review, measured baseline and outcome.
2. **Publish a reproducible demo.** Ship a sanitized input bundle and the minimum engine needed to rebuild one output end to end.
3. **Build the review surface.** Give reviewers one queue for exceptions, evidence, approvals, rulings, and diffs from the prior run.
4. **Instrument control effectiveness.** Track unsupported claims, escaped defects, correction recurrence, review effort, and workflow-level autonomy.
5. **Add integrations last.** Connect source systems only after the data contract and review workflow are stable.

The moat is not agent count or prompt sophistication. It is the accumulated, reviewable record of how a company defines its numbers, resolves ambiguity, and learns from corrections without weakening its controls.
