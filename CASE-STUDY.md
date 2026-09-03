# Case study: designing an AI-native finance function

## The one-minute version

I built and operated a governed finance-function prototype across bookkeeping, close, FP&A, management reporting, and reforecasting.

The first idea was “agents can run finance workflows.” The work changed that thesis. Calculation was not the hard or defensible part. The hard part was preserving judgment: which definition applies, what evidence supports a claim, when the system must refuse, how review changes future behavior, and when autonomy should be revoked.

The result is not a chatbot demo. It is a working operating model with agent charters, a semantic layer, versioned rulings, review contracts, exception ownership, a correction ledger, red-team findings, deployment gates, and decision-ready finance outputs.

| Scope | Published result |
|---|---|
| Finance operations | Close workflow, adjustments, exception register, reconciliation controls |
| FP&A | Variance analysis, Q1 LBE, 24-month forecast, long-range planning doctrine |
| Management reporting | Nine-tab management pack with 455 formula cells and explicit decisions required |
| Governance | Definitions, human rulings, evidence standards, approval boundaries, promotion and demotion rules |
| Product development | User trial, failure log, second synthetic instance, portability test, red-team remediation |
| Quality system | Financial, workbook, and prose verification layers |

## For a founder: the product judgment

### The wedge

The crowded pitch is “AI automates finance.” The sharper wedge is:

> A judgment and control layer for lean finance teams—installed on the existing stack, producing the work from day one, and earning lower-touch review one workflow at a time.

That wedge makes five deliberate product choices:

1. **Start with the monthly decision cycle.** Close, variance, reporting, and reforecast share definitions and evidence, so improvements compound across workflows.
2. **Use exports before integrations.** Prove the data contract and reviewer workflow before spending roadmap on connectors.
3. **Sell controlled output, not agent activity.** The unit of value is an approved pack or resolved exception, not a completed model call.
4. **Keep judgment visible.** Ambiguity, missing evidence, and limitations are product states—not failures to hide.
5. **Earn autonomy.** Trust expands from reviewed performance and contracts when a known failure recurs.

### The moat

The moat is not the number of agents or the prompt library. It is the company-specific decision history that accumulates through use:

- governed definitions and approved aliases;
- rulings on contested treatments;
- accepted commentary exemplars;
- evidence and lineage expectations;
- reviewer corrections and recurrence data; and
- workflow-specific autonomy records.

That system becomes more valuable as it learns the company while remaining inspectable by the finance owner.

### The next commercial proof

The next milestone is not another synthetic feature. It is one design partner, three consecutive closes, an independent reviewer, and measured movement in preparation time, review time, escaped defects, correction recurrence, and exception aging. The [executive brief](EXECUTIVE-BRIEF.md) defines the pilot gates.

## For a CFO: the control judgment

The design assumes that plausible numbers are more dangerous than obvious errors. Its controls therefore sit at the points where confidence can outrun evidence.

| Risk | Control | Evidence |
|---|---|---|
| A metric changes meaning between outputs | Versioned semantic definition and named human ruling | [Definitions](semantic-layer/definitions-instance.md) and [rulings](semantic-layer/rulings/) |
| An agent “improves” an approved input | Source hash blocks rendering after silent plan changes | [Plan-hash incident](what-broke/plan-hash-incident.md) |
| A calculated fact is presented as observed | Mandatory `read` versus `derived` provenance | [First review session](correction-loop/first-review-session.md) |
| A polished narrative invents a cause | Commentary contract requires driver evidence or an explicit unattributed remainder | [Commentary contract](contracts/commentary-contract.md) |
| An unresolved close item disappears | Exception requires impact, owner, due date, and consequence | [Management pack](outputs/management-reporting-pack.md) |
| A correction is repeated next month | Review-ledger entry becomes a rule or exemplar and is tested on a later run | [Loop verification](correction-loop/loop-verification.md) |
| Review is reduced too early | Autonomy is promoted and demoted per workflow | [Agent playbook](playbooks/agent-playbook.md) |

The honest boundary matters: the workbooks and governance artifacts are published; the engine and complete synthetic instance are not. This repository proves design depth and artifact quality. It does not yet prove production control effectiveness on real books.

## For a recruiter: the ownership signal

This project demonstrates more than the ability to produce a model or write a finance memo.

| Capability | What I owned | Inspect the work |
|---|---|---|
| Finance leadership | Defined the close, planning, reporting, and exception-management operating model | [Output contract](contracts/output-contract.md) and [management pack](outputs/management-reporting-pack.md) |
| Product strategy | Narrowed a broad automation idea into a differentiated judgment-layer thesis and sequenced adoption | [Architecture](architecture/blueprint.md) and [SaaS layer](architecture/saas-layer.md) |
| Product management | Specified users, workflow boundaries, failure states, acceptance gates, and staged autonomy | [Workflow slicing](architecture/slicing.md) and [install runbook](install/runbook.md) |
| Technical fluency | Designed tool boundaries, data contracts, model routing, and automated checks | [Live-instance spec](install/live-instance-spec.md) and [model-routing doctrine](install/model-routing/doctrine.md) |
| Quality and controls | Built independent checks, ran a red team, retained defects, and converted failures into controls | [Audit response](red-team/audit-response.md) and [what broke](what-broke/) |
| Executive communication | Turned detailed financial work into a decision-led pack, CEO briefing, and pilot recommendation | [CEO briefing](outputs/sealed-ceo-briefing.md) and [executive brief](EXECUTIVE-BRIEF.md) |
| Learning velocity | Used a fresh-workspace trial and a second instance to find happy-path assumptions and portability defects | [Scorecard](runs/scorecard.md) and [Arcline runs](runs/arcline/) |

The strongest signal is the correction history. The repository keeps the wrong turns: a “better” planning method that corrupted variance, an accurate fact that implied false causation, a checker that verified the wrong layer, a product that initially failed in its first two minutes, and prose that drifted from its source workbook. Each failure produced a system change and a recorded verification step.

## Three decisions that shaped the build

### 1. Organize around workflows, not synthetic job titles

“Bookkeeper agent” is easy to describe and hard to govern. A workflow such as variance commentary has a clear input, output contract, reviewer, known failure modes, and promotion history. Autonomy therefore belongs to the workflow.

### 2. Make refusal a first-class output

An unresolved metric, missing evidence, or unsupported driver should not become a best guess. The system names the blocker and the decision required. This makes incompleteness operable instead of invisible.

### 3. Stop polishing the fake company

More synthetic calibration would improve the demo while weakening the evidence. Company-specific thresholds, voice, and exemplars must be learned in deployment. The correct next experiment is a real close with independent review.

## What I would measure in production

| Outcome | Metric |
|---|---|
| Faster operations | Calendar days to close; human preparation hours; human review hours |
| Better control | Escaped critical defects; unsupported material claims; post-close corrections |
| Compounding judgment | Correction recurrence rate; percentage of accepted outputs using prior rulings or exemplars |
| Cleaner execution | Open-exception age; percentage with a named owner and due date |
| Earned trust | Clean reviewed runs and autonomy level by workflow |
| Adoption | Percentage of outputs approved, edited, refused, or abandoned—and why |

Success is not “the agent completed the task.” Success is that a finance owner approved a traceable output faster, with fewer repeated corrections, and knew exactly where judgment remained human.
