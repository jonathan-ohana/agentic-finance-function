# The judge layer and the canon register

**Date** 5 October 2026 · **Status** built and run against a fixture; not yet run against a live trajectory · **Prompted by** two problems in the correction loop

Two problems, one build.

**The rubric was in the agent's context, and the agent overfit to it.** The variance
commentary rubric lived in the Analyst's charter. Given three permitted endings, the agent
stamped the computable one on 10 of 17 comments, owner questions went to zero, and judgment
collapsed into template-filling. The [commentary contract](../contracts/commentary-contract.md)
records it as the ending-selection amendment. The diagnosis there is right: *given three
permitted endings, the agent always chose the computable one.* An agent that can read the
rubric it will be graded on learns the rubric, not the work.

**The only oracle runs at human speed.** Every correction in this repository was found by a
human reading the output line by line, by an agent auditing another agent, or by a check
written after a human found the failure. The review ledger is the loop's memory, and nothing
fills it faster than one person can read.

---

## The separation

The fix is to split what the agent reads from what grades it.

| | Charter | Behavior spec |
|---|---|---|
| Says | How to work, in general terms | What a correct run looks like, specifically |
| Read by | The agent, at runtime | The judge, after the run |
| Shown to the agent | Always | Never |

The charter stays general and the agent keeps reading it. The specific version moves into
[`package/behaviors/`](../package/behaviors/README.md), which no agent ever sees, and the
judge grades the run against it afterwards. An agent can only meet a rubric it cannot read
by doing the work the rubric describes.

That separation is the whole design, so it is a check rather than an intention.
`judge.py --check-leakage` fails if a behavior ID, or any condition or expectation sentence
from a spec, appears in an agent-facing file: the charters, CLAUDE.md, the README, the
plugin skill, and every topic folder holding write-ups. This document is one of those files,
which is why it names no behavior by ID and quotes none.

**The check caught my own first draft.** One of the commentary behaviors restated a
classification rule from the commentary contract word for word. The contract is wired into
the Analyst's charter, so the sentence was already in the agent's context. The leakage scan
named the contract and the spec, and the spec was reworded before anything was committed. It
is a small catch, and it is exactly the leak the check exists for: a spec written by
copying the charter it is meant to be kept apart from.

## What got built

**Behavior specs.** One behavior per block, five required fields: severity, condition,
expectation, evidence, rationale. Twelve variance-commentary behaviors for the Analyst,
derived from the commentary contract and the playbook library. They cover decomposition
before prose, drivers that sum or a named remainder, the read-only plan, causes joined to
documents, account nature governing the question, the timing-versus-forecast-miss vintage
rule, escalating structural anomalies, the forward close, playbook-selected endings,
sign coherence, judgments stated at handoff, and flagged uncertainty. Eight shared
behaviors apply to every agent. No figures, account numbers or names: those are calibration,
and `--check-specs` fails a spec that carries them. Every rationale cites the repository
document where its correction is recorded, and the check resolves each path.

**Trajectory record and map.** [`package/trajectory.py`](../package/trajectory.py) defines
the step record an agent writes and builds the map the judge reads. A fan-out run is a tree,
so the map keeps one entry per slice (its reads, writes, outputs, escalations, refusals,
handoffs and step order) under its parent. A finding names the slice it happened in, not
the run. The map keeps each reasoning step's one-line summary and drops its text, which is
most of a trajectory and the least of what a grader needs.

**The judge.** [`package/judge.py`](../package/judge.py) grades from the map. Seven checks
are deterministic. Five decide their behavior outright: decomposition precedes commentary
per subject, no write touches a plan, exactly one artifact in the delivery path, no write to
the record, no superseded document read. Two establish a necessary condition and pass the
rest to the grader: a run that names causes must have read at least one document, and a
configured bare metric term must carry a registry ID. Everything else goes to a pluggable
LLM grader, which is off by default.

With no grader, a behavior that needs one is **N.A., ungraded**, with the reason stated, and
sits in its own section of the verdict sheet. That is the scorekeeper's null-not-100% rule
again: an ungraded behavior counted as clean would be the most dangerous line on the sheet.
A FALSE becomes a review-ledger row with `reviewer = judge:<grader>` and an empty root
cause. Judge findings route exactly like human corrections, and the diagnosis stays with the
human, which is where the [first review session](first-review-session.md) showed it has to
stay.

**The canon register.** [`package/canonicity.py`](../package/canonicity.py) and
[CANON.md](../CANON.md): four statuses declared per document, symmetric successor relations,
records that are never superseded, stale-reference and duplicate-number checks, and an export
that tells the judge which documents are superseded.

## The seed pack

A nil grading and a broken grader produce the same report: no FALSE anywhere. The fixture
is the only place where the two look different. It is a hand-built fan-out run with a lead
and three slices, and two planted failures. In one slice, commentary is written on a subject
before anything decomposes it. In another, a plan line is re-derived and written back, which
is the plan-hash incident in miniature.

The judge found both, each attributed to the slice that did it, and nothing else came back
FALSE. Two behaviors read TRUE, one read N.A. because no superseded list has been exported
yet, and fifteen read N.A., ungraded, because no grader is configured. In CI the fixture
runs in seed-pack mode: it passes only if exactly the planted failures are FALSE. A missed
seed means the judge is broken. An extra FALSE means the judge changed, or the specs did.

## The canon register against this tree

Run against the 81 write-ups under the topic folders and the root, the register finds none
classified, which is expected because classification is the owner's call. It also finds
something that was not expected: **four document numbers each name two documents.** The
pairs are #82, #83, #84 and #85, numbers from the original series carried in H1 titles. Each
pair is a real collision, and docverify classifies documents by path, so it could not have
seen them.

They are not fixed here. Renumbering decides which document of each pair keeps the number,
and that is a ruling. Until it is made, a canonicity job in CI would fail on these four even
with unclassified documents tolerated. That is one more reason the job is not wired in yet.

*Annotation, 5 Oct 2026, later the same day: resolved. All four pairs were unrelated documents that collided by accident, not replacements. The later document of each pair was renumbered to 200 to 203, with a renumbered line under its title, and inbound citations were updated. See [the canon register](../outputs/canon-register.md).*

## What this does not do yet

- **No live trajectory has been graded.** The engines that would write trajectories run in
  the private instance, not in this repository. The judge has graded the fixture and nothing
  else. That is a named limit, not a result.
- **No grader ships.** Fifteen of the twenty behaviors need one: thirteen entirely, and two for everything past their deterministic precondition. Until a grader is configured,
  they are reported ungraded on every run, which is correct and not useful.
- **The canonical-reads behavior is N.A. until the first export**, and there is nothing to
  export until the owner classifies a document as superseded.

## Carried forward

- Classify the tree, one document at a time, by the owner. Then export the superseded list.
- Rule the four number collisions.
- Wire the canonicity job into CI with unclassified documents tolerated, once the collisions
  are ruled; take the tolerance off when classification is complete.
- Configure a grader and run the judge on a real close. The first live FALSE that a human
  reviewer agrees with is the evidence that this is a second signal and not a second opinion.
