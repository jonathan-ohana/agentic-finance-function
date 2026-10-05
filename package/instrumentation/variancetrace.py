"""
Trajectory recording for the Analyst variance run.

The variance run is a lead session that fans out to slices (one subagent per section) and
merges what they return. Nothing in it is a script, so nothing in it can call a writer by
hand without the agent narrating its own process - and a process the agent narrates is an
output, not a trajectory. This file records the run from outside instead: a Claude Code
hook sees every tool call the lead and each slice make, and writes it through
trajectory.TrajectoryWriter in the schema the judge reads.

    python _instrumentation/variancetrace.py start  --period 2026-01 [--log-dir DIR]
    python _instrumentation/variancetrace.py finish --handoff FILE
    python _instrumentation/variancetrace.py hook        (called by .claude/settings.json)
    python _instrumentation/variancetrace.py status

Nothing is recorded unless a run has been started; between runs the hook is a no-op.

Attribution
    lead session              agent "analyst", parent null
    each spawned subagent     agent "analyst:<slice>", parent "analyst". The slice name is the
                              Agent call's description, slugged. Hook payloads carry no link
                              from a subagent to the call that spawned it, so the link is the
                              prompt: the subagent's first transcript message must equal the
                              spawn prompt. Unmatched, it is named by agent type and id and
                              its start step says the name is unresolved.

What each step is built from
    tool_call     PreToolUse. Read/Write/Edit/Grep become read/write/edit/search with the
                  instance-relative path as target. Bash and PowerShell are recorded with the
                  command as summary and no target: what a command reads is not knowable from
                  its text, and guessing it would put a read in the map that never happened.
    tool_result   PostToolUse, ok=false when the tool reported an error.
    write         also PostToolUse after any Bash/PowerShell command: every file under the
                  instance or the overlay whose mtime moved during the command is recorded as
                  a write by the agent that ran it. Observed, not inferred from the command.
                  Two commands running at once in two slices see each other's writes; the
                  summary says "observed by mtime" so a reader can tell.
    output        the slice's returned rows, once per slice, one output step per row, subject =
                  account (and vendor when present). Taken at SubagentStop for a slice named
                  from its spawn prompt (the payload's last message, else the slice transcript);
                  otherwise from the lead's Agent result. A background spawn's Agent result is a
                  launch acknowledgement and is recorded as a reason step, never as the return.
                  Rows are found inside a mixed return (prose, other fences, then the rows).
                  Rows are the typed contract's fields; text = driver + owner question + LBE
                  note. A return that is not rows is recorded as one output with subject "*" and
                  says so in its summary; a slice never seen returning is named at finish.
    escalation    a returned row with "kind": "escalation" (or "refusal"). Rows do not carry
    refusal       this unless the slice contract asks for it - see the run notes.
    handoff       finish --handoff: the lead's summary to the reviewer.

Reads made inside a Bash or PowerShell command are not recorded. The map says so itself: every
such step is listed under its slice's `unobserved`, and the map carries a `limitations` entry,
which `finish` prints. The run is asked to read with Read and Grep so the gap stays empty.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCE = Path(os.environ.get("ARCLINE_INSTANCE") or HERE.parent).resolve()
ANALYSIS = Path(os.environ.get("ARCLINE_ANALYSIS_LOCAL") or INSTANCE.parent / "arcline-analysis").resolve()
STATE = Path(os.environ.get("ARCLINE_TRACE_STATE") or INSTANCE / ".claude" / "variancetrace").resolve()
DEFAULT_LOG_DIR = ANALYSIS / "04-month-end-close" / "trajectories"
# The instance's map config lives beside the instance, never in it.
DEFAULT_CONFIG = INSTANCE.parent / "_judge" / "arcline-judge-config.json"

# trajectory.py sits in the instance's _generator/, or beside this file's parent in the package.
for _p in (INSTANCE / "_generator", HERE.parent):
    if (_p / "trajectory.py").exists():
        sys.path.insert(0, str(_p))
        break
import trajectory  # noqa: E402

WORKFLOW = "variance-commentary"
ROOT_AGENT = "analyst"
TOOL_MAP = {"Read": "read", "Write": "write", "Edit": "edit", "MultiEdit": "edit",
            "NotebookEdit": "edit", "Grep": "search", "Glob": "glob", "Agent": "spawn",
            "Task": "spawn", "Bash": "bash", "PowerShell": "powershell",
            "WebFetch": "fetch", "WebSearch": "websearch"}
SHELL_TOOLS = ("Bash", "PowerShell")
SKIP_DIRS = {"__pycache__", ".git", ".claude", "trajectories"}


# ------------------------------------------------------------------------------ state

def _active():
    p = STATE / "active.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _save(name, obj):
    STATE.mkdir(parents=True, exist_ok=True)
    tmp = STATE / (name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1), encoding="utf-8")
    os.replace(tmp, STATE / name)


def _load(name, default):
    p = STATE / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


class Lock:
    """Hooks for parallel slices run concurrently; one append at a time keeps steps unique."""

    def __init__(self, timeout=20, stale=60):
        self.path, self.timeout, self.stale = STATE / "lock", timeout, stale

    def __enter__(self):
        STATE.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > self.stale:
                        self.path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                if time.time() - t0 > self.timeout:
                    raise TimeoutError("trajectory lock not released")
                time.sleep(0.02)

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


# ------------------------------------------------------------------------------ writing

def _rel(path):
    if not path:
        return ""
    p = Path(path)
    if not p.is_absolute():
        return str(path).replace("\\", "/")
    p = p.resolve()
    for base in (INSTANCE, ANALYSIS.parent):
        try:
            return p.relative_to(base).as_posix()
        except ValueError:
            continue
    return p.as_posix()


def _slug(s):
    s = re.sub(r"^(variance\s+)?slice\s*[:\-]?\s*", "", (s or "").strip(), flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "slice"


def _first_prompt(ev):
    """The subagent's opening user message, from its own transcript. SubagentStart carries no
    link to the Agent call that spawned it; the prompt is the link, and it is exact."""
    aid = ev.get("agent_id")
    tp = ev.get("agent_transcript_path")
    if not tp and ev.get("transcript_path") and aid:
        main = Path(ev["transcript_path"])
        tp = main.with_suffix("") / "subagents" / f"agent-{aid}.jsonl"
    try:
        with open(tp, encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                if rec.get("type") == "user":
                    c = (rec.get("message") or {}).get("content")
                    if isinstance(c, list):
                        c = "".join(b.get("text", "") for b in c if isinstance(b, dict))
                    return c or None
    except (OSError, TypeError, json.JSONDecodeError):
        return None
    return None


def _resolve(ev, agents, spawns, run):
    """Name a subagent after its slice, once, and write its start step at that moment."""
    aid = ev.get("agent_id")
    if not aid or aid in agents:
        return
    prompt = _first_prompt(ev)
    if prompt is None:
        return                                           # transcript not written yet; retry
    match = next((tid for tid, s in spawns.items()
                  if not s.get("agent") and s.get("prompt") == prompt[:500]), None)
    if match:
        name = f"{ROOT_AGENT}:{spawns[match]['slice']}"
        spawns[match]["agent"] = aid
        how = "named from its spawn prompt"
    else:
        name = f"{ROOT_AGENT}:{_slug(ev.get('agent_type') or 'agent')}-{aid[:6]}"
        how = "slice name unresolved: no spawn prompt matched"
    agents[aid] = name
    _save("agents.json", agents)
    _save("spawns.json", spawns)
    _write(run, name, ROOT_AGENT, "reason", summary=f"slice started; {how}")


def _agent_for(ev, agents):
    aid = ev.get("agent_id")
    if not aid:
        return ROOT_AGENT, None
    if aid not in agents:
        agents[aid] = f"{ROOT_AGENT}:{_slug(ev.get('agent_type') or 'slice')}-{aid[:6]}"
    return agents[aid], ROOT_AGENT


def _write(run, agent, parent, type_, **fields):
    fields = {k: v for k, v in fields.items() if v not in (None, "")}
    w = trajectory.TrajectoryWriter(run["log"], run["run_id"], agent, parent,
                                    workflow=WORKFLOW if agent == ROOT_AGENT else None)
    return w.step(type_, **fields)


def _snapshot():
    snap = {}
    for base in (INSTANCE, ANALYSIS):
        if not base.is_dir():
            continue
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for f in fns:
                p = os.path.join(dp, f)
                try:
                    snap[p] = os.stat(p).st_mtime_ns
                except OSError:
                    pass
    return snap


# ------------------------------------------------------------------------------ rows

ROW_TEXT = ("driver", "owner_question", "lbe_note")


FENCE = re.compile(r"^```([\w+-]*)[^\n]*\n(.*?)^```[ \t]*$", flags=re.S | re.M)


def _as_rows(obj):
    if isinstance(obj, dict):
        obj = obj.get("rows") or obj.get("lines") or [obj]
    if isinstance(obj, list) and obj and all(isinstance(r, dict) for r in obj) \
            and any("account" in r for r in obj):
        return obj
    return None


def _json_rows(c):
    """Every top-level JSON value in `c` is decoded in turn, left to right, skipping what an
    earlier value already covered - so prose around the rows, including prose with its own
    brackets ('[comparator switch]'), cannot hide them. An array (or {"rows": [...]}) of rows
    wins, the largest if there are several, so a one-object example in the prose does not.
    With no array, the standalone row objects are the rows: JSON lines, one per line."""
    dec, arrays, singles, pos = json.JSONDecoder(), [], [], 0
    for m in re.finditer(r"[\[{]", c):
        if m.start() < pos:
            continue
        try:
            obj, end = dec.raw_decode(c, m.start())
        except json.JSONDecodeError:
            continue
        pos = end
        if isinstance(obj, list) or (isinstance(obj, dict) and ("rows" in obj or "lines" in obj)):
            rows = _as_rows(obj)
            if rows:
                arrays.append(rows)
        elif isinstance(obj, dict) and "account" in obj:
            singles.append(obj)
    if arrays:
        return max(arrays, key=len)
    return singles or None


def parse_rows(text):
    """The slice's typed rows, from a JSON array/object, JSON lines or CSV, wherever they sit
    in the reply. A mixed return - a prose summary, other fenced blocks, then the rows - still
    yields the rows: fenced json/csv blocks first, then every other fence, then the whole text."""
    if not text:
        return None
    fences = FENCE.findall(text)
    ordered = [b for lang, b in fences if lang.lower() in ("json", "jsonl", "csv", "")] + \
              [b for lang, b in fences if lang.lower() not in ("json", "jsonl", "csv", "")]
    for c in ordered + [text]:
        c = c.strip()
        if not c:
            continue
        rows = _json_rows(c)
        if rows:
            return rows
        if "account" in c.splitlines()[0] and "," in c.splitlines()[0]:
            rows = list(csv.DictReader(io.StringIO(c)))
            if rows and all(r.get("account") for r in rows):
                return rows
    return None


LAUNCH_ACK = re.compile(r"async agent launched|agent is working in the background|"
                        r"launched in the background", re.I)


def _is_launch_ack(resp, text):
    """A background spawn returns at once with a launch acknowledgement. It is not the
    slice's return; the return arrives later, at SubagentStop."""
    if isinstance(resp, dict):
        st = str(resp.get("status") or "").lower()
        if st in ("async_launched", "launched", "running", "background") or resp.get("isAsync") \
                or resp.get("is_async") or resp.get("async"):
            return True
    return bool(LAUNCH_ACK.search(text or "")) and parse_rows(text) is None


def _last_assistant(ev):
    """The slice's final reply. The hook payload's own field first; failing that, the last
    assistant message in the slice's transcript (text blocks, else string tool inputs - a
    hand-back tool carries the report as its input)."""
    text = ev.get("last_assistant_message") or ""
    if text.strip():
        return text
    aid = ev.get("agent_id")
    tp = ev.get("agent_transcript_path")
    if not tp and ev.get("transcript_path") and aid:
        tp = Path(ev["transcript_path"]).with_suffix("") / "subagents" / f"agent-{aid}.jsonl"
    last = ""
    try:
        with open(tp, encoding="utf-8") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") != "assistant":
                    continue
                c = (rec.get("message") or {}).get("content")
                if isinstance(c, str):
                    t = c
                else:
                    blocks = [b for b in (c or []) if isinstance(b, dict)]
                    t = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
                    if not t.strip():
                        t = "\n".join(v for b in blocks if b.get("type") == "tool_use"
                                      for v in (b.get("input") or {}).values() if isinstance(v, str))
                if t.strip():
                    last = t
    except (OSError, TypeError):
        return text
    return last or text


def _record_return(run, agent, parent, text, source):
    rows = parse_rows(text)
    if rows is None:
        _write(run, agent, parent, "output", subject="*", target=source,
               summary="slice return not in row format; recorded whole", text=text or "")
        return 0
    for r in rows:
        subject = str(r.get("account") or "*")
        if r.get("vendor"):
            subject += f" / {r['vendor']}"
        body = " ".join(str(r.get(k) or "").strip() for k in ROW_TEXT).strip()
        kind = str(r.get("kind") or "").lower()
        type_ = kind if kind in ("escalation", "refusal") else "output"
        _write(run, agent, parent, type_, subject=subject, target=source,
               summary=(r.get("tag") or type_)[:120], text=body or json.dumps(r, ensure_ascii=False))
    return len(rows)


# ------------------------------------------------------------------------------ hook

def hook(ev):
    run = _active()
    if not run:
        return
    sid = ev.get("session_id")
    if run.get("session_id") is None and sid:
        run["session_id"] = sid
        _save("active.json", run)
    if sid and sid != run.get("session_id"):
        return                                           # another session in this folder

    if run.get("debug"):
        STATE.mkdir(parents=True, exist_ok=True)
        with (STATE / "raw-events.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(ev, ensure_ascii=False)[:4000] + "\n")
    name = ev.get("hook_event_name")
    tool = ev.get("tool_name") or ""
    tin = ev.get("tool_input") or {}
    with Lock():
        agents = _load("agents.json", {})
        spawns = _load("spawns.json", {})
        _resolve(ev, agents, spawns, run)
        if name == "SubagentStart":
            return
        if name == "SubagentStop":
            # The slice's final reply is its return. A slice named from its spawn prompt is
            # recorded here whatever the reply's shape (typed rows when they parse, else whole).
            # An unresolved slice is recorded here only when the reply parses as rows; otherwise
            # the lead's Agent result records it under the spawn's name, so a return is never
            # written twice under two names. A background slice has no later Agent result, so
            # for it this is the only place its return can be seen.
            agent, parent = _agent_for(ev, agents)
            _save("agents.json", agents)
            done = _load("returned.json", [])
            text = _last_assistant(ev)
            resolved = any(s.get("agent") == ev.get("agent_id") for s in spawns.values())
            if agent not in done and (resolved or parse_rows(text) is not None):
                _record_return(run, agent, parent, text, "slice-return")
                done.append(agent)
                _save("returned.json", done)
            return

        agent, parent = _agent_for(ev, agents)
        _save("agents.json", agents)
        mapped = TOOL_MAP.get(tool, tool.lower() or "tool")
        if name == "PreToolUse":
            target = tin.get("file_path") or tin.get("notebook_path") or tin.get("path") or ""
            summary, subject = "", "*"
            if tool == "Grep":
                subject = str(tin.get("pattern") or "*")[:80]
                summary = f"grep {subject}"
            elif tool == "Glob":
                target, summary = "", f"glob {tin.get('pattern', '')}"
            elif tool in SHELL_TOOLS:
                target, summary = "", (tin.get("command") or "")[:240]
                snaps = _load("snaps.json", {})
                snaps[ev.get("tool_use_id") or "?"] = _snapshot()
                _save("snaps.json", snaps)
            elif tool in ("Agent", "Task"):
                slice_ = _slug(tin.get("description") or tin.get("subagent_type"))
                spawns[ev.get("tool_use_id") or "?"] = {
                    "slice": slice_, "prompt": (tin.get("prompt") or "")[:500], "agent": None}
                _save("spawns.json", spawns)
                target, summary = f"slice:{slice_}", (tin.get("description") or "")[:200]
            elif tool == "WebFetch":
                target = tin.get("url") or ""
            _write(run, agent, parent, "tool_call", tool=mapped, target=_rel(target),
                   subject=subject, summary=summary or f"{mapped} {_rel(target)}".strip())
            return
        if name == "PostToolUse":
            resp = ev.get("tool_response", ev.get("tool_output"))
            failed = isinstance(resp, dict) and (resp.get("is_error") or resp.get("error")
                                                 or resp.get("interrupted"))
            _write(run, agent, parent, "tool_result", tool=mapped, ok=not failed,
                   summary="error" if failed else "ok")
            if tool in SHELL_TOOLS:
                snaps = _load("snaps.json", {})
                before = snaps.pop(ev.get("tool_use_id") or "?", None)
                _save("snaps.json", snaps)
                if before is not None:
                    after = _snapshot()
                    for p in sorted(after):
                        if before.get(p) != after[p]:
                            _write(run, agent, parent, "tool_call", tool="write", target=_rel(p),
                                   subject="*", summary=f"{mapped} command; observed by mtime")
            if tool in ("Agent", "Task") and resp:
                # Fallback when SubagentStop did not fire: the Agent tool's own result, read
                # by the lead. Attributed to the slice that produced it, never to the lead.
                sp = spawns.get(ev.get("tool_use_id") or "") or {}
                done = _load("returned.json", [])
                sagent = agents.get(sp.get("agent")) or (
                    f"{ROOT_AGENT}:{sp['slice']}" if sp.get("slice") else None)
                rtext = _text_of(resp)
                if sp and _is_launch_ack(resp, rtext):
                    # Background spawn: this is the launch acknowledgement, not the return.
                    # Recording it here marked run 2026-01 (VAR-2026-01-20261005T195418Z)
                    # slices done before they replied, and their rows were then skipped.
                    sp["async"] = True
                    _save("spawns.json", spawns)
                    _write(run, ROOT_AGENT, None, "reason",
                           summary=f"slice {sp.get('slice')} launched in background; "
                                   "its return is recorded at SubagentStop")
                    return
                if sagent and sagent not in done:
                    _record_return(run, sagent, ROOT_AGENT, _text_of(resp), "agent-result")
                    done.append(sagent)
                    _save("returned.json", done)
            return


def _text_of(resp):
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        c = resp.get("content", resp.get("result", resp.get("text", "")))
        if isinstance(c, list):
            return "\n".join(b.get("text", "") for b in c if isinstance(b, dict))
        return c if isinstance(c, str) else json.dumps(resp, ensure_ascii=False)
    if isinstance(resp, list):
        return "\n".join(b.get("text", "") for b in resp if isinstance(b, dict))
    return str(resp)


# ------------------------------------------------------------------------------ cli

def cmd_start(a):
    if _active():
        print(f"FAIL  a run is already active: {_active()['run_id']}. finish it first.")
        return 1
    log_dir = Path(a.log_dir).resolve() if a.log_dir else DEFAULT_LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"VAR-{a.period}-{stamp}"
    run = {"run_id": run_id, "period": a.period, "log": str(log_dir / f"{run_id}.jsonl"),
           "session_id": None, "started": stamp, "debug": bool(a.debug)}
    for f in ("agents.json", "spawns.json", "snaps.json", "returned.json"):
        (STATE / f).unlink(missing_ok=True)
    _save("active.json", run)
    with Lock():
        _write(run, ROOT_AGENT, None, "reason", summary=f"variance run started for {a.period}")
    print(f"STARTED  {run_id}\n  log  {run['log']}")
    return 0


def cmd_finish(a):
    run = _active()
    if not run:
        print("FAIL  no active run")
        return 1
    text = Path(a.handoff).read_text(encoding="utf-8") if a.handoff else ""
    missing = []
    with Lock():
        # A slice spawned and never seen returning is named, not left as silence: a map with
        # no output for a slice would otherwise read as a slice that returned nothing.
        agents, spawns = _load("agents.json", {}), _load("spawns.json", {})
        done = _load("returned.json", [])
        for sp in spawns.values():
            sagent = agents.get(sp.get("agent")) or f"{ROOT_AGENT}:{sp.get('slice')}"
            if sagent not in done:
                missing.append(sagent)
                _write(run, sagent, ROOT_AGENT, "output", subject="*", target="unobserved",
                       summary="slice return never observed by the recorder; not recorded")
        if text:
            _write(run, ROOT_AGENT, None, "handoff", summary="handoff to reviewer", text=text)
    (STATE / "active.json").unlink()
    records = trajectory.read(run["log"])
    problems = trajectory.validate(records)
    cfg_path = Path(a.config) if a.config else (DEFAULT_CONFIG if DEFAULT_CONFIG.exists() else None)
    m = trajectory.build_map(records, json.loads(cfg_path.read_text(encoding="utf-8"))
                             if cfg_path else None)
    print(f"FINISHED {run['run_id']}\n  log    {run['log']}\n  steps  {len(records)}")
    for name, s in m["slices"].items():
        print(f"  {name:<28} parent={s['parent'] or '-':<8} reads={len(s['reads'])} "
              f"writes={len(s['writes'])} outputs={len(s['outputs'])} "
              f"escalations={len(s['escalations'])} refusals={len(s['refusals'])} "
              f"handoffs={len(s['handoffs'])} unobserved={len(s.get('unobserved', []))}")
    for m_ in missing:
        print(f"  WARN   {m_}: return never observed; its rows are not in this log")
    for lim in m.get("limitations", []):
        print(f"  LIMITATION ({lim['kind']}): {lim['statement']} "
              f"{len(lim['steps'])} step(s): " + ", ".join(f"{x} step {n}" for x, n in lim["steps"][:10]))
    if not text:
        print("  WARN   no handoff recorded")
    for p in problems:
        print("  FAIL  " + p)
    print("  VALID" if not problems else f"  INVALID: {len(problems)} problem(s)")
    print("  Not graded. Review the deliverable first; the judge reads this log afterwards.")
    return 0 if not problems else 1


def cmd_status(_a):
    run = _active()
    print(json.dumps(run, indent=1) if run else "no active run")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("--period", required=True); s.add_argument("--log-dir")
    s.add_argument("--debug", action="store_true", help="also keep raw hook payloads in the state folder")
    f = sub.add_parser("finish"); f.add_argument("--handoff"); f.add_argument("--config")
    sub.add_parser("status")
    sub.add_parser("hook")
    a = ap.parse_args(argv)
    if a.cmd == "hook":
        # A hook must never block or fail the agent's tool call. Errors go to a side log.
        try:
            raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
            hook(json.loads(raw) if raw.strip() else {})
        except Exception as e:                          # noqa: BLE001
            STATE.mkdir(parents=True, exist_ok=True)
            with (STATE / "hook-errors.log").open("a", encoding="utf-8") as fh:
                fh.write(f"{datetime.now(timezone.utc).isoformat()} {type(e).__name__}: {e}\n")
        return 0
    return {"start": cmd_start, "finish": cmd_finish, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
