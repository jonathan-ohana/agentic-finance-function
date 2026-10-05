# Instrumentation: the variance run's trajectory recorder

[`variancetrace.py`](variancetrace.py) records an Analyst variance run as a trajectory: one
JSONL step per tool call, in the schema of [`../trajectory.py`](../trajectory.py), which is
what the [judge](../judge.py) grades from. It records from outside the agent, through Claude
Code hooks, so the trajectory is observed rather than narrated by the agent about itself.

This is the copy kept in the repository. An instance carries the same file at
`_instrumentation/variancetrace.py`, beside its `_generator/trajectory.py`; the recorder finds
`trajectory.py` in either place.

## Installing it in an instance

Copy `variancetrace.py` to `<instance>/_instrumentation/`, and register it for four hook events
in the instance's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse":    [{"matcher": ".*", "hooks": [{"type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/_instrumentation/variancetrace.py\" hook", "timeout": 30}]}],
    "PostToolUse":   [{"matcher": ".*", "hooks": [{"type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/_instrumentation/variancetrace.py\" hook", "timeout": 30}]}],
    "SubagentStart": [{"hooks": [{"type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/_instrumentation/variancetrace.py\" hook", "timeout": 30}]}],
    "SubagentStop":  [{"hooks": [{"type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/_instrumentation/variancetrace.py\" hook", "timeout": 30}]}]
  }
}
```

Between runs the hook does nothing. A failed hook writes to `hook-errors.log` in the state
folder, never to the agent's tool call.

## A run

1. `python _instrumentation/variancetrace.py start --period <YYYY-MM>` (add `--debug` to keep
   the raw hook payloads in the state folder).
2. The lead spawns each slice with the Agent tool, description `Variance slice: <name>`. The
   name becomes the slice's agent, `analyst:<name>`, matched to the subagent by its spawn
   prompt.
3. Each slice ends its reply with its rows: the typed fields of the slice return contract in
   [`contracts/commentary-contract.md`](../../contracts/commentary-contract.md), with
   `"kind": "escalation"` or `"kind": "refusal"` on rows that are one. A prose summary before
   the rows is fine. The recorder finds them inside a mixed return: a fenced or unfenced
   array, `{"rows": [...]}`, JSON lines or CSV, with other fences and bracketed prose around
   them.
4. `python _instrumentation/variancetrace.py finish --handoff <file>` writes the handoff,
   validates the log and prints the per-slice map. It does not grade.

Then grade:

```
python package/judge.py --specs package/behaviors --config <instance judge config> \
    --run <run>.jsonl --out verdict-sheet.md --ledger review-ledger.csv
```

## Where a slice's return is taken from

| How the slice ran | Where its return is recorded |
|---|---|
| Foreground | At SubagentStop when the slice is named from its spawn prompt; otherwise from the lead's Agent result |
| Background | At SubagentStop only. The Agent result is a launch acknowledgement: it is recorded as a reason step on the lead, never as the slice's return |

At SubagentStop the reply is the hook payload's last assistant message, or, when that is
empty, the last assistant message in the slice's own transcript (a hand-back tool carries its
report as tool input). A spawned slice never seen returning is recorded at `finish` as one
output with subject `*` and target `unobserved`, and `finish` warns. A gap is named, not
left as silence.

## What is and is not recorded

- **Recorded:** Read, Write, Edit, Grep, Glob and Agent calls and their results, per slice;
  every file whose modification time moved during a Bash or PowerShell command, as a write by
  the agent that ran it; each slice's returned rows; the handoff.
- **Not recorded:** what a Bash or PowerShell command reads. No read is inferred from the
  command text. The map names the gap instead: each such step is listed under its slice's
  `unobserved`, and the map carries a `limitations` entry that the judge prints on the verdict
  sheet and attaches as a caveat to any FALSE it could have caused.

## The fixture

[`tests/fixtures/recorder-mixed-return/`](../../tests/fixtures/recorder-mixed-return/README.md)
replays raw hook events through the recorder into a throwaway folder and checks the map.
CI runs it. It fails against the recorder as it was before the background-slice fix, with the
same signature that fix was written for: every slice recorded as one `*` output and no
escalation or refusal reaching the log.
