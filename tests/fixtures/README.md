# Judge seed pack

A nil grading and a broken grader produce the same report. These fixtures are the only place
where "nothing failed" and "nothing ran" look different, so CI grades each one in seed-pack
mode, and the run passes only if **exactly** the planted failures come back FALSE.

| Fixture | Shape | Planted failures |
|---|---|---|
| [`run-fanout.jsonl`](run-fanout.jsonl) | Variance-commentary run: a lead and three slices (opex, cogs, revenue), one assembled deliverable | `B-ANL-001` in `analyst:opex`: commentary on a subject that nothing decomposed. `B-ANL-003` in `analyst:cogs`: a plan line re-derived and written back |
| [`run-opaque.jsonl`](run-opaque.jsonl) | One slice whose only step before its comment is a shell command | `B-ANL-001` and `B-ANL-004` in `analyst:opex`, **each carrying the recorder caveat**. The shell step may have read the decomposition and the agreement, and the record cannot say. CI also requires the map's `unobserved_reads` limitation on the verdict sheet. This seed fails if the caveat is ever dropped, because then a recorder blind spot would read as agent failure |

The rest of the run is built to be clean on everything a deterministic check can see: one
artifact in the delivery path, no write to a record path, causes stated with documents read,
a named refusal, a structural anomaly escalated. If a change to the judge or the specs makes
anything else FALSE here, the seed pack fails, and that is the signal that the judge changed.

This folder is not agent-facing and is not scanned for leakage. It names behavior IDs because
it is the seed manifest. The pack is owned by a human: add a seed when a judge miss is found,
never to make a run pass.

```
python3 package/judge.py --specs package/behaviors --run tests/fixtures/run-fanout.jsonl \
    --expect-false B-ANL-001,B-ANL-003
python3 package/judge.py --specs package/behaviors --run tests/fixtures/run-opaque.jsonl \
    --expect-false B-ANL-001,B-ANL-004
```

## Recorder fixture

The seed pack above tests the judge on trajectories written by hand. It cannot catch a
recorder that writes the wrong trajectory, and that is the failure the first live variance
run hit: every slice's return was recorded as one untyped output, so none of the escalations
it raised reached the map.

| Fixture | What it replays | Passes only if |
|---|---|---|
| [`recorder-mixed-return/`](recorder-mixed-return/README.md) | Raw hook events through [`package/instrumentation/variancetrace.py`](../../package/instrumentation/variancetrace.py): two background slices and one foreground slice, each returning prose with its typed rows inside it, one of them only through its transcript | Every slice's comment, escalation and refusal rows reach the map typed, no slice is recorded as an untyped `*` output, and both launch acknowledgements are recorded as reason steps |

```
python3 tests/fixtures/recorder-mixed-return/replay.py
```
