# Judge seed pack

A nil grading and a broken grader produce the same report. These fixtures are the only place
where "nothing failed" and "nothing ran" look different, so CI grades each one in seed-pack
mode, and the run passes only if **exactly** the planted failures come back FALSE.

| Fixture | Shape | Planted failures |
|---|---|---|
| [`run-fanout.jsonl`](run-fanout.jsonl) | Variance-commentary run: a lead and three slices (opex, cogs, revenue), one assembled deliverable | `B-ANL-001` in `analyst:opex`: commentary on a subject that nothing decomposed. `B-ANL-003` in `analyst:cogs`: a plan line re-derived and written back |

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
```
