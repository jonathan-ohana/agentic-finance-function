# Seed fixture - a slice return that is not only rows

Replays raw hook events through `variancetrace.py hook` into a throwaway state and log
folder, then checks the map. It reproduces the January rerun's recording failure
(VAR-2026-01-20261005T195418Z: four slices, 56 escalations and 2 refusals returned, zero
recorded) and two neighbouring shapes:

| Slice | How it ran | Where its return is | Shape of the return |
|---|---|---|---|
| `bg-mixed` | background | SubagentStop `last_assistant_message` | prose with brackets, a `bash` fence, then a fenced JSON array: comment, escalation, refusal |
| `bg-handback` | background | only in its transcript, as a hand-back tool input; the hook's message field is empty | prose, then JSON lines (no array): comment, escalation |
| `fg-mixed` | foreground | the Agent tool result | prose containing a one-object example row, then a fenced JSON array: comment, escalation |

The January failure was the first row. The Agent tool's immediate result for a background
spawn is a launch acknowledgement. The recorder took it for the slice's return, recorded it
as one `*` output and marked the slice done, so SubagentStop later skipped the real rows.
The prose in front of the JSON was never the cause: the parser already looked inside fences.

    python _instrumentation/fixtures/seed-mixed-return/replay.py      (in an instance)
    python tests/fixtures/recorder-mixed-return/replay.py             (in the repository)

Exit 0 when every count in `expected.json` holds. Nothing in the instance or the overlay is
touched; the run is written under a temporary folder and removed.
