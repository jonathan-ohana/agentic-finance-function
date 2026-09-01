# An agentic finance function, built and run end to end

A working prototype of a finance function — bookkeeping, month-end close, variance analysis, management reporting, reforecast — run by AI agents under a governance layer that makes every number traceable and every judgment call recorded.

Built and pressure-tested in a simulated B2B SaaS company environment, working from standard system exports rather than custom integrations.

---

## What it produces

The January management pack, built by the agents and verified by an independent checker. Every derived number on this page is a formula referencing the tab that owns it — 455 of them, and no typed ratios.

![Profit and loss by financial statement line, January 2026](docs/pack-pl.png)

The tab that makes it a finance function rather than a report. Ten adjustments posted, six items carried out of the close knowingly — each with an owner, a due date, and what happens if it is not resolved — and three items cleared, recorded so the next reader can see the change.

![What the close found, and what it left open](docs/pack-exceptions.png)

Download the workbooks: [the January pack](outputs/FY2026-01-management-pack.xlsx) (9 tabs) and [the Q1 LBE](outputs/LBE_Q1_2026_M1.xlsx) (3 tabs).

---

## Why this exists

AI-native finance tools are good at **ledger attribution** — what moved, in which account, in which entity. They cannot tell you **why** in business terms, because the *why* isn't in the ledger. The value of a finance professional is still to see the story through the noise.

So the interesting question was never *"can agents do the close?"* It was:

> **What layer captures a finance professional's judgment and compounds it, so the function gets smarter every month instead of re-deciding the same things?**

This repository is that layer, with the agents underneath it.

---

## Honest limits, stated first

- One simulated company (a second instance, Arcline, was built to test portability — see `runs/arcline/`).
- One operator. Self-graded.
- No real company's books have been through this.
- The learning mechanism is **demonstrated** — one human correction became a versioned rule, and a later agent run cited that correction by ledger ID as the reason it behaved differently. That is a **demonstrated mechanism, not a demonstrated track record.** The distinction matters and is kept throughout.
- The calibration (thresholds, voice, account-specific rules) is company-specific by design and does **not** transfer. The machinery does.

---

## What it proves — four claims, four exhibits

| Claim | Open this | Time |
|---|---|---|
| Agents ran the close, variance analysis and reporting end to end | [`outputs/management-reporting-pack.md`](outputs/management-reporting-pack.md) + [`runs/run-log.md`](runs/run-log.md) | 3 min |
| Every number traces to a versioned definition, with human rulings on contested items | [`semantic-layer/definitions-instance.md`](semantic-layer/definitions-instance.md) + [`semantic-layer/rulings/`](semantic-layer/rulings/) | 3 min |
| Commentary is trained on exemplars, under a contract it must satisfy | [`contracts/commentary-contract.md`](contracts/commentary-contract.md) — the gold exemplar pairs | 2 min |
| **Corrections persist: each close is smarter than the last** | [`correction-loop/loop-verification.md`](correction-loop/loop-verification.md) | 3 min |

### The one exhibit that matters most

From `correction-loop/loop-verification.md` — a human corrected an agent; the correction became a versioned rule; a later run of that agent applied the rule, **cited the correction by ledger ID as its reason**, and did not repeat the error — while still escalating a real problem it would have been easier to stay quiet about:

> *"Escalating this as a contradiction would repeat review ledger RL-0024, where four contracts were wrongly flagged on computed expiry dates."*

Four contracts that failed under charter v1.0 were re-extracted blind under v1.1 by two independent agents, with a control and a genuine contradiction included as checks. All four read the header correctly. Zero false escalations. The real contradiction was still raised.

That is the loop closing, observed rather than asserted.

---

## The ten-minute path

1. **[`outputs/management-reporting-pack.md`](outputs/management-reporting-pack.md)** — read the cover. Every caveat you see was raised by an agent and survived to the board-facing surface without being softened. One chart carries, on its face, *"the remaining −$101,030 carries NO attributed driver."* A conventional deck shows the chart and lets the reader assume.
2. **[`correction-loop/loop-verification.md`](correction-loop/loop-verification.md)** — the correction loop, verified.
3. **[`what-broke/`](what-broke/)** — three failures, unedited. See below.
4. **[`semantic-layer/rulings/`](semantic-layer/rulings/)** — pick any ruling. Note who decided, when, why, and what the system refused to compute until they did.
5. **[`red-team/`](red-team/)** — the brief, the auditor's findings, and [`audit-response.md`](red-team/audit-response.md): nine of its recommendations implemented and verified.

---

## What broke — the part worth reading

**The agent silently improved the plan.** During a variance run, the Analyst re-derived two plan lines on a methodologically *better* basis than the one on file — and thereby corrupted the variance, flipping a sign. Nobody asked it to. The improvement was correct; the behavior was wrong. Plan values are inputs an agent reads, never recomputes. Caught by human review; now caught by a hash check that blocks the pack from rendering. → [`what-broke/plan-hash-incident.md`](what-broke/plan-hash-incident.md)

**Judgment collapsed into template-filling.** Given three permitted ways to end a variance comment, the agent chose the computable one every time — "reforecast candidate" stamped on 10 of 17 comments by single-month extrapolation, owner questions extinct (0 of 17). Contract compliance achieved; judgment lost. Fix: the ending is determined by the playbook, not chosen by the agent. → [`contracts/commentary-contract.md`](contracts/commentary-contract.md), amendment v2.1

**A derived value reported as an observed one.** Four contract expiry dates were computed, then reported as if read from the document, then escalated as contradictions against documents that didn't contradict themselves. Not an arithmetic error — a **provenance** error. Charter amended to require `basis: read` with a quote, or `basis: derived` with the derivation. → [`correction-loop/first-review-session.md`](correction-loop/first-review-session.md)

Also included unedited: **[`what-broke/friction-log.md`](what-broke/friction-log.md)** — everything that was slower, dumber or more brittle than it should have been.

---

## Knowing when to stop

Refinement on the simulated company was deliberately **frozen**, and the reasoning is itself part of the artifact:

> The machinery — contract, selection rules, engine checks, exemplar memory, read-back, correction routing — is **package**: done, portable, proof banked. The calibration — voice, thresholds, accepted exemplars — is **example**: company-specific by nature and non-transferable. Further polish trains the agent for a company that doesn't exist, while real-company calibration is cheap in situ by design.

Every company-specific parameter in the playbooks and charters is tagged `REPLACE-ON-INSTALL`. See [`install/`](install/).

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│  JUDGMENT LAYER  (this repo)                          │
│  semantic layer + rulings · playbooks + exemplars     │
│  output contracts · correction ledger · red team      │
├──────────────────────────────────────────────────────┤
│  AGENTS                                               │
│  Bookkeeper · Analyst · Reporter · Forecaster ·       │
│  Controller · Evidence · Chief of Staff               │
├──────────────────────────────────────────────────────┤
│  SOURCE SYSTEMS  (exports only — no integrations)     │
│  GL · billing · CRM · payroll · bank                  │
└──────────────────────────────────────────────────────┘
```

The ledger is a buy. The judgment layer is made of decisions no vendor can ship, and it is the only layer here meant to outlive the tools underneath it.

Autonomy is earned **per workflow**, never per agent, on instances reviewed with no material correction — with a documented demotion trigger and a named known failure mode for each. See [`playbooks/agent-playbook.md`](playbooks/agent-playbook.md).

---

## How it's organized

| Folder | What's in it |
|---|---|
| `architecture/` | The org blueprint, source-vs-output design, how work is sliced |
| `semantic-layer/` | Definitions (template + instance), rulings, glossary |
| `contracts/` | Output contract, commentary contract with gold exemplar pairs |
| `playbooks/` | Variance playbooks, agent promotion ladder, wiring |
| `agents/` | One charter per agent |
| `correction-loop/` | The two loops, review sessions, loop verification, iteration log |
| `red-team/` | The audit brief, the auditor's findings, and what was changed in response |
| `runs/` | Run logs, scorecard, ingestion sweeps, the Arcline second instance |
| `outputs/` | Reporting pack, CEO briefing, forecast model, long-range plan — including the generated workbooks themselves ([management pack](outputs/FY2026-01-management-pack.xlsx), [Q1 LBE](outputs/LBE_Q1_2026_M1.xlsx)) and their independent verifier |
| `what-broke/` | Plan-hash incident, failure case, friction log |
| `data/` | Simulated company spec, dataset build notes, planted edge cases, the 25-check tie-out suite ([`validate.py`](data/validate.py)) |
| `install/` | Runbook, portability, org assessment, model routing |

---

## What's in this repo, and what isn't

The **engine itself** — the ~30 Python modules that generate the instance, run the close, precompute the variance surface and build the reporting pack — runs on the live instance and is deliberately not published. This repository carries what the engine cannot fake: its outputs ([the January pack](outputs/FY2026-01-management-pack.xlsx), [the Q1 LBE](outputs/LBE_Q1_2026_M1.xlsx)), two of its independent checkers, and every design decision, ruling and failure recorded along the way.

The checkers are here so the scores are inspectable rather than asserted: [`outputs/packverify.py`](outputs/packverify.py) recomputes every figure in the pack from the instance's data and asserts 42 cross-tab checks against the workbook's recalculated values; [`data/validate.py`](data/validate.py) is the 25-check tie-out suite the instance must pass before any agent touches it. Both read the live instance's data files, so they don't run from this repo alone — they are evidence, not a demo.

Also deliberately absent: the sealed answer key (publishing it would spoil future blind runs), vendor comparisons, market research, and the scaffolding that surrounded this work. This repository is the artifact, not the diary.

---

*Built by Jonathan Ohana, 2026. Questions welcome — the fastest way to find the holes in this is to ask.*
