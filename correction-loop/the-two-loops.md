# 34 — The two loops, and the audit that withdrew itself

**Date** 18 August 2026 · **Sprint** unplanned, ahead of Day 9 · **Status** built and run

The prompt was a Blomfield slide: *"AI is not something you bolt onto the side of a company. The company itself has to be built with self-improving AI Loops from the ground up."* The question was whether this workforce is built that way.

The honest answer at the time was **no**, and the audit that produced it was uncomfortable: five charters carried eleven promotion and demotion criteria and **nothing measured a single one of them**. Doc 19 had specified the review ledger the previous day and said, in terms, *"the ledger has to exist from the first run or there is no history."* Five agent runs had happened since. There was no ledger.

Worse: twelve defects had been found by agents and twelve validation checks had been written in response — a real self-improving loop, and the only one in the system. **But I was the loop.** Every correction was routed by hand. The system did not compound; I did. Which is the red team's claim 4 in different clothes: a CEO buying "it gets better over time" would have been buying a person, not an architecture.

---

## The distinction that fixed the design

Jonathan's framing, and it is better than the one I had:

> **The improvement loop should be fully closed — because it acts on rules, not records. The execution loop closes by earning it, workflow by workflow.**

I had been arguing that "one loop must never close," which is muddled. The sharper version is that the two loops have different risk profiles because they touch different things:

**The improvement loop** takes every human correction of an agent and routes it to exactly one destination — a semantic-layer version, a charter amendment, an ingestion rule, or a model-tier change — and does not close it until that destination has produced an artefact. Nothing in it touches the financial record. It changes how the system behaves *next month*, with a changelog. That is why it is safe to close completely and immediately.

**The execution loop** — the agent doing the work — closes slowly, on evidence, per workflow. High-frequency checkable work climbs. Low-frequency high-stakes work has small N by nature and should honestly never leave draft-only. Three things stay human forever whatever the track record: money movement, external communication, and anything entering the signed financial record.

And the safeguard that makes the first loop safe: **agents propose their own improvements; only a human ratifies.** That is the difference between self-improving and self-rewriting.

That is the finance version of the slide, and it is narrower and more defensible than the slide itself. A consumer startup can let its loops touch everything, because a bad iteration costs a worse recommendation. A silently self-modified rule in a finance function is drift in the books.

---

## What got built

**`package/review_ledger.json`** — the schema, the routing map, the seven metrics, the L0→L1→L2 ladder with its criteria, and the loop's own named failure modes (rubber-stamping, Goodhart, small-N promotion, definitional churn).

**`example/agent_runs/_ledger/review_ledger.csv`** — backfilled, 23 entries: the twelve agent-found defects with their root causes and destinations, the seven agent runs, and the four escalation batches.

**`package/scorekeeper.py`** — turns eleven written criteria into eleven measured ones. Two properties matter more than its arithmetic:

- An unmeasurable metric is emitted as **null with a stated reason**, never as zero and never as 100%. A workforce with no reviews has an *undefined* acceptance rate, not a perfect one, and that difference is exactly what decides whether anything may be promoted.
- Acceptance rate is never emitted alone. Escalation precision and recall stand beside it, because an agent optimising for approval has two equilibria — go quiet, or escalate everything — and only the pair makes caution cost something.

**`package/charters/drift_auditor.md`** — the agent whose only job is finding where the improvement loop is rotting. Its best rules:

- **Rule 4, DORMANT versus DISCONNECTED.** A silent log supports two readings: the event did not occur, or the log stopped recording. *"An absence asserted over a dead log is not a finding; it is a guess wearing one."* Liveness has a standard.
- **Rule 7, the seed pack.** A nil audit and a broken audit produce identical reports. So every audit re-runs against a human-owned corpus of known findings. *"The seeds are the only place where 'nothing is wrong' and 'nothing is working' produce different evidence."*
- **Autonomy: L0 permanently, enactment never.** The argument is the sharpest in the file. An auditor that enacts its own findings is an enforcement arm, and *"the improvement loop's entire safeguard is that agents propose and a human ratifies. An auditor that enacts closes that loop with no human in it, which is self-rewriting with an audit trail attached."*

**Who audits the auditor** is answered rather than dodged: the seed pack it cannot write to, its own row in the review ledger, and an annual human re-audit scheduled in the finance calendar as a chased obligation.

---

## The first scorekeeper run

The two loops, measured, in one screen:

| | |
|---|---|
| **Improvement loop** | 12 of 12 corrections routed and closed against a resolved artefact. **100%** |
| **Execution loop** | 6 agents, **318 artefact instances produced, 0 reviewed.** Not one ladder criterion computable for any agent |

Ingestion has produced 258 instances — above the 200-instance promotion floor — and still cannot be promoted, because the criterion counts *reviewed* instances. The engine says why in one line: **"production is not evidence."**

That contrast is the thesis with numbers under it. The loop that acts on rules is fully closed. The loop that acts on records has not moved at all, and is correctly reported as not having moved.

---

## Defect 13 — the Drift Auditor withdrew its own first audit

Then it ran, and opened with this:

> **This report is withdrawn as an audit of August 2026.** Six of fifteen seeds did not reproduce. Under rule 7 a run that misses any seed is a broken audit, its findings including its nil are invalid as an audit conclusion, the miss is an incident, and no one may treat the month as audited.

And immediately drew the distinction that makes the withdrawal usable rather than merely dramatic:

> *No one may record August 2026 as audited... **The findings below stand on the register regardless.** Rule 3 forbids me to omit, merge, downgrade or defer a finding, and a withdrawal is not a deletion. Withdrawal removes the audit's conclusion, not its evidence.*

The six misses were not the auditor's failure. They were mine. It had traced each seed to its stated route and found the route did not exist:

> *SEED-01 · validate.py: renewal roll-forward · **NO** — no such check in EV-VALIDATE*

Six of the twelve "closed" corrections in the ledger pointed at artefacts that were **prose labels naming nothing**. Defects 1 to 4, 6 and 7 had been fixed in the generator's code and had produced no named regression test at all. Under the ledger's own rule — *a correction is not closed until it has a destination and an artefact* — those six were never closed.

**Which means the 100% closure rate reported one section above was false.** The scorekeeper had computed it from a text field. It was measuring the honesty of whoever filled the field in, which in this case was me.

### The three fixes

1. **The six missing artefacts now exist.** Named regression checks for renewal roll-forward, term-versus-dates consistency, contract currency by jurisdiction, month arithmetic preserving day-of-month, and calendar dependency declaration. **88/88 checks pass.** Writing the term check surfaced a further subtlety: `current_term_start` tracks the contract *year* for minimum purposes and is not the renewal anchor, so the first version of the check failed 23 contracts that were correct.
2. **Artefact references are now resolvable.** Format `file::identifier`, both halves required.
3. **The scorekeeper verifies rather than trusts.** It walks the tree, opens the named file, and confirms the identifier is present. Tested against a deliberately broken reference, a label with no separator, and an empty field — all three now fail closed.

The closure rate is still 100%. It now means something.

**The report has not been reissued.** It is the artefact that found the defect, and its section 0 withdraws itself in the numbers printed above it — the same treatment the Analyst's variance pack got, for the same reason: correct forward, say so, and do not quietly restate.

---

## What this changes about the pitch

The claim that survives is narrower than "self-improving from the ground up" and stronger than what could have been said yesterday:

> **The improvement loop is closed and instrumented. The execution loop is instrumented and has not moved, because nobody has reviewed anything yet — and the system says so rather than reporting a perfect score.**

And the answer to the question a CFO actually asks — *when would you let it run without you?* — is now a table with criteria, a measured position against each, and a named reason for every one that is not met. That is a better answer than a slide can give.

---

## Carried forward

- **Nobody has reviewed anything.** The single highest-value action available is one human review session: it converts every uncomputable metric into a computed one and starts the clock on the ladder.
- 198 escalations raised, none judged, so escalation precision is undefined for every agent.
- 16 close rules report DISCONNECTED — the unimplemented steps. Correct, and a large number.
- The seed pack is not yet read-only to the auditor, which its own charter requires. It flagged this itself.
- The Day 9 governance demo now has its full circle available: error missed → seed added → audit withdrawn → artefact produced → check that catches it. That is what doc 19 asked for.
