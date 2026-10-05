# Behavior specs

The rubric the judge grades a run against, and the one thing in this repository that no
agent is ever shown.

## The never-shown rule

**No text in this folder enters an agent's context: not in a charter, a prompt, a skill, a
playbook, CLAUDE.md, or a retrieved document.** The agent reads its charter, which is
general and read at runtime. The judge reads this folder, which is specific and read only
after the run.

The reason is a measured failure, not a precaution. The commentary rubric used to live in
the Analyst's charter. Given the permitted endings in writing, the agent chose the one it
could compute on most of the comments in a run, and judgment collapsed into template-filling
([commentary contract, the ending-selection amendment](../../contracts/commentary-contract.md)).
A rubric the agent can read becomes a template the agent fills. A rubric it cannot read can
only be met by doing the work.

This is a check, not an intention. `judge.py --check-leakage` fails the build if any
behavior ID, or any condition or expectation sentence from a spec here, appears in an
agent-facing file. Paraphrasing a spec into a charter to get past the check defeats the
design as surely as pasting it; the check catches the second and only review catches the
first.

## Format

One file per agent and workflow, with two header lines. `*` means all:

```
agent: analyst
workflow: variance-commentary
```

One behavior per block, five required fields and one optional:

```
### B-XXX-NNN · Title
- **severity:** blocking | material | advisory
- **condition:** when the behavior applies
- **expectation:** what the run does when it applies
- **evidence:** what in the trajectory map the grader looks at
- **rationale:** why, and the correction it traces to, citing a repository path
- **check:** the name of a deterministic check in judge.py (omit for grader-only)
```

## Grading

Each behavior is graded **TRUE**, **FALSE** or **N.A.**

- **N.A. means the condition did not arise. It is not a pass.** A run that wrote no
  commentary has not met the commentary behaviors; it has not been tested on them.
- A behavior that needs judgment and has no grader configured is **N.A., ungraded**, with
  the reason stated. It gets its own section of the verdict sheet, so it is never counted
  as clean. That is the scorekeeper's rule: an unmeasurable metric is null with a reason,
  never one hundred percent.
- A deterministic check either decides the behavior or establishes a necessary condition
  and hands the rest to the grader. It never upgrades an ungraded behavior to TRUE.
- A FALSE at blocking or material severity fails the run and writes a review-ledger row with
  `reviewer = judge:<grader>`. Judge findings route exactly like human corrections, and the
  root cause is left for the human to diagnose.

## Authoring rules

1. **Prefer one general behavior over fifty brittle ones.** A behavior names a pattern of
   reasoning that holds across accounts and companies. If it only makes sense for one line,
   it is calibration.
2. **No figures, no account numbers, no names.** Thresholds, accounts, owners, vendors and
   lexicon belong to the instance and to the exemplar store. A spec carrying them stops being
   mechanism and starts being a fixture of one company. `--check-specs` enforces the figures
   and the instance terms listed in the judge config.
3. **Name the evidence.** The evidence field points at something the judge can read: an
   entry in the map (a read, a write, an escalation, the step order) or the text of an
   output. Evidence that is output text alone is a narrower claim — what the deliverable
   says, not how the run reached it — and is gradeable from the deliverable without a
   trajectory. Where one correction has both a process half and an output half, write them
   as two behaviors, one per kind of evidence, so a verdict never mixes what was said with
   how it was reached. If the evidence field can point at neither, the behavior is not
   gradeable and should not be written yet.
4. **Every behavior traces to a correction.** The rationale cites the repository document
   where the correction is recorded, by path. The review ledger itself lives in the private
   instance, so the published record of the correction is the trace here. `--check-specs`
   resolves every cited path and fails on one that does not exist.
5. **Do not edit a spec to make a run pass.** If a check is wrong, say so in a PR and let the
   owner rule. A spec changed to fit the output it grades is the rubric version of
   recomputing the plan.

## Files

| File | What it holds |
|---|---|
| [`analyst-variance.md`](analyst-variance.md) | The Analyst's variance-commentary behaviors |
| [`shared.md`](shared.md) | Behaviors every agent is graded on |
| [`judge-config.json`](judge-config.json) | Instance paths, tool names and markers. The code holds none of them |
