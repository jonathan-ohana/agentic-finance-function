# 204 — The variance loop, end to end: what has run

<!-- canon: record -->

**Date** 5 October 2026 · **Run graded** `VAR-2026-01-20261005T195418Z`, the January 2026
variance commentary rerun on Arcline, a four-way fan-out · **Predecessor** doc 89 (run 03) and
the [judge layer build record](../../correction-loop/judge-layer-and-canonicity.md)

*Classified `record`. It states what the loop had and had not done on this date. The owner
closed calibration of the variance commentary on the same date, so no further calibration
work follows from it. The run's deliverable was not reviewed line by line, so nothing here
compares the judge with a human reviewer.*

---

## The loop, and the plain answer

The loop is four links: **a run emits a trajectory → the map builds → the judge grades → a
FALSE writes a review-ledger row.**

**It does not work end to end on real output yet.** Each link has executed. No real slice
return has ever travelled the whole chain to a verdict. The first live run broke the first
link for slice returns, which left nothing for the later links to act on.

| Link | On real output | Only on a reconstruction | Never run |
|---|---|---|---|
| Run emits trajectory | Yes for reads, writes, spawns, shell steps and the handoff. **No for slice returns:** each slice became one untyped output | Typed slice rows (comment, escalation, refusal) reaching the log: the recorder fixture only | The recorder fix on a live run |
| Map builds | Yes. The log validated, and the map built with five agents, each slice named after its spawn | The map holding typed slice outputs, escalations and refusals | |
| Judge grades | Yes. The judge read the real log and wrote a verdict sheet without error | Planted FALSEs found and attributed to their slice, with the recorder caveat: the seed pack | Any grader. Every behavior without a deterministic check has only ever been reported ungraded |
| FALSE writes a ledger row | No. The run produced no FALSE, so the ledger file holds a header only | Two rows written from the seed pack's planted FALSEs, by hand, on this date. CI runs the seed pack without the ledger option | A ledger row from real output. A ledger for the rows to land in (see below) |

## What broke in the first link

The slices ran in the background. For a background spawn, the Agent tool's immediate result
is a launch acknowledgement. The recorder took it for the slice's return, logged it as one
untyped output and marked the slice done. About ten minutes later each slice finished, and
its real return was skipped as already recorded. All four untyped outputs carry the same
timestamp, seconds after the spawns.

The slices had returned their rows typed per the slice return contract (amendment v2.3 in the
[commentary contract](../../contracts/commentary-contract.md)): 56 escalation rows and 2
refusal rows, alongside their comments. They are in the deliverable and the run's working
files. They are not in the trajectory, and the working files are the lead's transcription, not
an observation, so they cannot stand in for it.

**A first diagnosis was wrong.** The run's lead first attributed the gap to the prose summary
each slice put before its rows. The log contradicts that: the untyped outputs were written
before any slice had replied, and the parser already searched fenced blocks.

**Fixed** in [`package/instrumentation/variancetrace.py`](../../package/instrumentation/README.md):

- A launch acknowledgement is recorded as a reason step on the lead, never as a slice's return.
- A slice named from its spawn prompt is recorded at SubagentStop whatever the shape of its
  reply. The reply comes from the hook payload, or from the slice's own transcript when the
  payload is empty.
- The parser finds rows inside a mixed return: other fences, bracketed prose, JSON lines, or a
  one-object example in the prose.
- A slice never seen returning is named at `finish`, not left as silence.

**Proved against the fixture only.** [`tests/fixtures/recorder-mixed-return/`](../../tests/fixtures/recorder-mixed-return/README.md)
replays hook events through the recorder and runs in CI. It was also run against the recorder
with the old behavior restored, and failed with the January signature: untyped outputs and no
escalation reaching the map. The event payloads in it are constructed. The launch
acknowledgement text matches the one the live run received. The SubagentStop payload of a live
background slice has never been captured.

## The January run, graded

The judge ran with the instance's judge config and a ledger file, and graded the run against
every behavior in the spec set. The owner asked for four behaviors, all graded from the
trajectory, and excluded the two escalation behaviors for this run because they would read
FALSE for the recorder's reason.

| Behavior asked for | Verdict | A sensible verdict? |
|---|---|---|
| Decomposition comes before prose | TRUE | **No.** It was graded against the four untyped launch acknowledgements, and credited because the lead had read the decomposition file at an earlier step. It says nothing about the slices' comments |
| A named cause joins to a document | N.A., the condition did not arise | **No.** The slices' comments name causes, but none reached the map, so the check found no causal output |
| Timing is not claimed over a move that was knowable (plan vintage) | N.A., ungraded | **No verdict.** No grader is configured |
| The ending follows the playbook, not what is computable | N.A., ungraded | **No verdict.** No grader is configured. A grader would have found no comment text in the map to grade |

**The machinery did not produce a sensible verdict on any of the four.** It also produced one
plausible-looking TRUE out of a record that held no commentary. A TRUE drawn from an empty
record is the most misleading line a verdict sheet can carry.

Three other deterministic verdicts rest only on reads and writes, which the recorder did
capture, and they agree with what the run did:

- The plan is read-only: TRUE, on 39 plan reads and no plan write.
- Nothing is written to the record: TRUE, on 16 writes.
- One artifact in the delivery path: TRUE.

Of the other behaviors, one more was N.A. because no superseded list has been exported, and
the remaining fifteen were ungraded. The verdict sheet and the empty ledger file live with the
instance, outside this repository.

## Proven, reconstructed, never run

**Proven on real output**
- Hook recording of each slice's reads, writes and spawns, and attribution of every subagent
  to its slice by spawn prompt. All four slices were named correctly.
- The recorder's blind spot is named: the run's three shell steps were listed as unobserved
  and carried onto the verdict sheet.
- A real trajectory validates, its map builds, and the judge grades it end to end without
  error.
- Deterministic checks on reads and writes give verdicts consistent with the run.

**Proven only against a reconstruction**
- Typed slice rows reaching the map, including escalations and refusals: the recorder fixture.
- The judge finding planted failures and attributing each to its slice: the seed pack.
- The recorder caveat travelling with a FALSE that a shell step could have caused: the seed
  pack.
- A FALSE becoming a review-ledger row with the judge as reviewer and the root cause left
  empty: the seed pack, run by hand with the ledger option.

**Never run**
- A grader. No grader exists, so every behavior without a deterministic check has only ever
  been reported ungraded.
- A FALSE on a real trajectory, and so a ledger row from real output.
- A review ledger for the rows to land in. The judge appends to whatever file it is given. No
  ledger with its columns exists in the instance, and the instance's only ledger code (the
  monitor's) uses a different column set.
- A human filling a root cause on a judge row.
- The recorder fix on a live run.
- The canonical-reads check with a superseded list.
- The bare-metric check finding a registry ID in Arcline output. The instance writes registry
  IDs and versions in a different convention from the one the judge config expects.
