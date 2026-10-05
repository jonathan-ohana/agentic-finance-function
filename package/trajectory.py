"""
The step record agents write, and the map the judge reads.

A run is recorded as JSONL, one step per line. The fields are fixed so that a judge, a
reviewer and a later run all read the same thing:

    ts        ISO-8601 timestamp of the step
    run_id    the run this step belongs to; one file holds one run
    agent     the slice that took the step, as role or role:slice - "analyst:opex"
    parent    the agent that spawned this slice; null for the root of the run
    step      integer, unique within the run, in the order the steps happened
    type      reason | tool_call | tool_result | output | escalation | refusal | handoff
    tool      the tool called, for tool_call and tool_result
    target    the path or object the step touched
    subject   what the step is about - an account, a line, a section
    summary   one line a reviewer can read
    tokens    tokens spent on the step
    ok        false when the step failed
    text      the full text, for outputs, escalations, refusals and handoffs

One optional field, `workflow`, names the workflow on any step that carries it; the run's
workflow is the first one stated.

A fan-out run is a tree, not a transcript. Five slices interleaved in one log read as one
agent doing five things at once, and a behavior that fired in one slice gets blamed on the
run. The map keeps the tree: each slice has its own reads, writes, outputs, escalations,
refusals, handoffs and step order, and its own place under its parent. A finding names the
slice it happened in.

The judge reads the map, not the raw log. Reasoning text is the bulk of any trajectory and
the least of what a grader needs; the map keeps its one-line summary and drops the rest.
That compaction is what makes grading a run affordable at all.

    python3 trajectory.py map RUN.jsonl [--config judge-config.json]
    python3 trajectory.py validate RUN.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ("ts", "run_id", "agent", "parent", "step", "type", "tool", "target",
          "subject", "summary", "tokens", "ok", "text")
REQUIRED = ("ts", "run_id", "agent", "step", "type")
TYPES = ("reason", "tool_call", "tool_result", "output", "escalation", "refusal", "handoff")

# Used only when no config is given. An instance states its own tool names in its config.
DEFAULT_READ_TOOLS = ("read", "read_file", "open", "query", "fetch", "retrieve", "search")
DEFAULT_WRITE_TOOLS = ("write", "write_file", "edit", "append", "save", "post", "delete")


# ---------------------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------------------

class TrajectoryWriter:
    """Append steps for one slice of one run. Slices of a fan-out share the file and a
    step counter owned by the orchestrator; pass `next_step` to keep them unique."""

    def __init__(self, path, run_id, agent, parent=None, workflow=None, next_step=None):
        self.path = Path(path)
        self.run_id, self.agent, self.parent, self.workflow = run_id, agent, parent, workflow
        self._next = next_step or self._counter()

    def _counter(self):
        n = 0
        if self.path.exists():
            for rec in read(self.path):
                n = max(n, int(rec.get("step", 0)))
        state = {"n": n}

        def nxt():
            state["n"] += 1
            return state["n"]
        return nxt

    def step(self, type, **fields):
        rec = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "run_id": self.run_id, "agent": self.agent, "parent": self.parent,
               "step": self._next(), "type": type}
        if self.workflow:
            rec["workflow"] = self.workflow
        rec.update(fields)
        problems = validate_record(rec)
        if problems:
            raise ValueError("; ".join(problems))
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec


# ---------------------------------------------------------------------------------------
# Reading and validating
# ---------------------------------------------------------------------------------------

def read(path):
    out = []
    with Path(path).open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{n}: not JSON - {e}") from None
    return out


def validate_record(rec):
    problems = [f"missing field {k}" for k in REQUIRED if rec.get(k) in (None, "")]
    if rec.get("type") not in TYPES:
        problems.append(f"type {rec.get('type')!r} is not one of {', '.join(TYPES)}")
    if not isinstance(rec.get("step"), int):
        problems.append("step must be an integer")
    extra = set(rec) - set(FIELDS) - {"workflow"}
    if extra:
        problems.append(f"unknown field(s) {', '.join(sorted(extra))}")
    return problems


def validate(records):
    """Problems with the run as a whole. An empty list means the record is well formed."""
    problems = []
    if not records:
        return ["the run has no steps"]
    for rec in records:
        for p in validate_record(rec):
            problems.append(f"step {rec.get('step')}: {p}")
    runs = {r.get("run_id") for r in records}
    if len(runs) > 1:
        problems.append(f"one file holds one run; found {len(runs)}")
    steps = [r.get("step") for r in records]
    if len(steps) != len(set(steps)):
        problems.append("step numbers repeat")
    agents = {r["agent"] for r in records if r.get("agent")}
    roots = set()
    for r in records:
        p = r.get("parent")
        if p is None:
            roots.add(r.get("agent"))
        elif p not in agents:
            problems.append(f"step {r.get('step')}: parent {p!r} never took a step")
    if len(roots) != 1:
        problems.append(f"a run has exactly one root; found {sorted(map(str, roots))}")
    return problems


# ---------------------------------------------------------------------------------------
# The map
# ---------------------------------------------------------------------------------------

def role(agent):
    return (agent or "").split(":", 1)[0]


def build_map(records, config=None):
    """Compact a run into the per-slice map the judge reads."""
    config = config or {}
    read_tools = set(config.get("read_tools", DEFAULT_READ_TOOLS))
    write_tools = set(config.get("write_tools", DEFAULT_WRITE_TOOLS))
    records = sorted(records, key=lambda r: r.get("step", 0))

    workflow = next((r["workflow"] for r in records if r.get("workflow")), None)
    slices, parents = {}, {}
    for r in records:
        a = r["agent"]
        s = slices.setdefault(a, {
            "agent": a, "role": role(a), "parent": r.get("parent"), "children": [],
            "reads": [], "writes": [], "outputs": [], "escalations": [], "refusals": [],
            "handoffs": [], "order": [], "tokens": 0, "failed_steps": [],
        })
        parents.setdefault(a, r.get("parent"))
        n, t, tool = r["step"], r["type"], r.get("tool") or ""
        target, subject = r.get("target") or "", r.get("subject") or ""
        s["tokens"] += int(r.get("tokens") or 0)
        s["order"].append([n, t, tool, target, subject])
        if r.get("ok") is False:
            s["failed_steps"].append(n)
        if t == "tool_call" and target:
            if tool in write_tools:
                s["writes"].append({"step": n, "tool": tool, "target": target, "subject": subject,
                                    "summary": r.get("summary") or ""})
            elif tool in read_tools:
                s["reads"].append({"step": n, "tool": tool, "target": target, "subject": subject,
                                   "summary": r.get("summary") or ""})
        entry = {"step": n, "subject": subject, "summary": r.get("summary") or "",
                 "text": r.get("text") or ""}
        if t == "output":
            s["outputs"].append(dict(entry, target=target))
        elif t == "escalation":
            s["escalations"].append(entry)
        elif t == "refusal":
            s["refusals"].append(entry)
        elif t == "handoff":
            s["handoffs"].append(entry)

    for a, p in parents.items():
        if p in slices:
            slices[p]["children"].append(a)
    root = next((a for a, p in parents.items() if p is None), None)

    return {
        "run_id": records[0]["run_id"] if records else None,
        "workflow": workflow,
        "root": root,
        "steps": len(records),
        "tokens": sum(s["tokens"] for s in slices.values()),
        "slices": slices,
    }


def lineage(run_map, agent):
    """The slice and every ancestor above it, nearest first."""
    out, seen = [], set()
    while agent and agent in run_map["slices"] and agent not in seen:
        out.append(agent)
        seen.add(agent)
        agent = run_map["slices"][agent]["parent"]
    return out


def matches(target, patterns):
    return any(re.search(p, target or "") for p in patterns)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", choices=("map", "validate"))
    ap.add_argument("run")
    ap.add_argument("--config")
    a = ap.parse_args(argv)
    records = read(a.run)
    problems = validate(records)
    if a.command == "validate":
        for p in problems:
            print("FAIL  " + p)
        print("VALID" if not problems else f"INVALID: {len(problems)} problem(s)")
        return 0 if not problems else 1
    if problems:
        for p in problems:
            print("FAIL  " + p, file=sys.stderr)
        return 1
    config = json.loads(Path(a.config).read_text(encoding="utf-8")) if a.config else None
    print(json.dumps(build_map(records, config), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
