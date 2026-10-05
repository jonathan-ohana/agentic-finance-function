"""
The behavior judge: grades how a run reasoned, from its trajectory map, against specs the
agent never saw.

The only oracle this finance function has is a human reading the output line by line, and
that runs at human speed. The judge is a cheaper second signal that routes into the same
review ledger. It does not replace the reviewer and does not diagnose: a FALSE becomes a
ledger row with `reviewer = judge:<grader>` and an empty root cause, which is the human's
to fill in. Diagnosing before routing is where the first review session found the route was
wrong.

Two kinds of grading:

    deterministic   whatever can be decided from the map alone - decomposition precedes
                    commentary per subject, no write touches a plan, exactly one artifact in
                    the delivery path, no write to the record, no superseded document read,
                    no run that names causes without reading a single document. Some checks
                    decide the behavior; some establish a necessary condition and hand the
                    rest to the grader.
    grader          a pluggable LLM grader for everything else. Off by default.

With no grader configured, a behavior that needs one is N.A. with the reason stated, never a
pass - the scorekeeper's rule that an unmeasurable metric is null with a reason, not 100%.
Ungraded behaviors get their own section of the verdict sheet. N.A. for "the condition did
not arise" and N.A. for "nobody graded this" are different statements and are never merged.

The grader is any command that reads one JSON request on stdin and writes one JSON verdict
on stdout:

    request   {"behavior": {...}, "run_id", "workflow", "slices": {agent: slice map},
               "deterministic_note": str|null}
    verdict   {"verdict": "TRUE"|"FALSE"|"N.A.", "reason": str, "slices": [agent, ...]}

A grader that errors, times out or answers out of format leaves the behavior ungraded, with
the error as its reason. That is also why the fixture exists: a nil grading and a broken
grader produce identical reports, and the seed pack is the only place where "nothing failed"
and "nothing ran" look different.

    python3 judge.py --specs DIR --run RUN.jsonl [--out sheet.md] [--json v.json]
                     [--ledger ledger.csv] [--grader-cmd "CMD"] [--grader-name NAME]
                     [--expect-false ID,ID]
    python3 judge.py --specs DIR --check-specs
    python3 judge.py --specs DIR --check-leakage PATH [PATH ...]

Exit codes: 0 clean; 1 a blocking or material behavior is FALSE, a spec is malformed, spec
text leaked, or --expect-false did not match exactly; 2 the inputs could not be read.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trajectory  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^B-[A-Z]{3}-\d{3}$")
ID_ANY = re.compile(r"\bB-[A-Z]{3}-\d{3}\b")
HEAD_RE = re.compile(r"^###\s+(\S+)\s+·\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^-\s+\*\*([a-z]+):\*\*\s*(.*)$")
REQUIRED = ("severity", "condition", "expectation", "evidence", "rationale")
OPTIONAL = ("check",)
SEVERITIES = ("blocking", "material", "advisory")
FAILING = ("blocking", "material")
LEAK_SUFFIXES = (".md", ".txt", ".json", ".yml", ".yaml", ".toml", ".html")
LEAK_MIN_CHARS = 40


# ---------------------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------------------

@dataclass
class Behavior:
    id: str
    title: str
    file: str
    line: int
    fields: dict = field(default_factory=dict)

    def __getattr__(self, name):
        f = self.__dict__.get("fields", {})
        if name in REQUIRED + OPTIONAL:
            return f.get(name)
        raise AttributeError(name)


@dataclass
class SpecFile:
    path: str
    agent: str | None
    workflow: str | None
    behaviors: list


def parse_specs(spec_dir):
    files = []
    for p in sorted(Path(spec_dir).glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        agent = workflow = None
        behaviors, cur = [], None
        for n, line in enumerate(lines, 1):
            if cur is None:
                m = re.match(r"^agent:\s*(\S+)\s*$", line)
                if m and agent is None:
                    agent = m.group(1)
                m = re.match(r"^workflow:\s*(\S+)\s*$", line)
                if m and workflow is None:
                    workflow = m.group(1)
            h = HEAD_RE.match(line)
            if h:
                cur = Behavior(h.group(1), h.group(2), str(p), n)
                behaviors.append(cur)
                continue
            f = FIELD_RE.match(line)
            if f and cur is not None:
                cur.fields[f.group(1)] = f.group(2).strip()
        files.append(SpecFile(str(p), agent, workflow, behaviors))
    return files


def all_behaviors(specs):
    return [b for s in specs for b in s.behaviors]


def strip_code(text):
    return re.sub(r"`[^`]*`", "", text or "")


def check_specs(specs, config, root=ROOT):
    """Spec hygiene. Returns a list of problems; empty means every spec is well formed."""
    problems = []
    if not specs or not all_behaviors(specs):
        return ["no behaviors found - a check that can pass on an empty set is not a check"]
    seen = {}
    terms = config.get("calibration_terms", [])
    for s in specs:
        rel = os.path.relpath(s.path, root)
        if not s.agent:
            problems.append(f"{rel}: missing the 'agent:' header")
        if not s.workflow:
            problems.append(f"{rel}: missing the 'workflow:' header")
        if not s.behaviors:
            problems.append(f"{rel}: no behaviors")
        for b in s.behaviors:
            where = f"{rel}:{b.line} {b.id}"
            if not ID_RE.match(b.id):
                problems.append(f"{where}: ID is not of the form B-XXX-NNN")
            if b.id in seen:
                problems.append(f"{where}: ID already used at {seen[b.id]}")
            seen.setdefault(b.id, where)
            for k in REQUIRED:
                if not b.fields.get(k):
                    problems.append(f"{where}: missing required field '{k}'")
            for k in b.fields:
                if k not in REQUIRED + OPTIONAL:
                    problems.append(f"{where}: unknown field '{k}'")
            if b.severity and b.severity not in SEVERITIES:
                problems.append(f"{where}: severity '{b.severity}' is not one of {', '.join(SEVERITIES)}")
            if b.check and b.check not in CHECKS:
                problems.append(f"{where}: check '{b.check}' is not a deterministic check in judge.py")
            cited = re.findall(r"`([^`]+)`", b.rationale or "")
            paths = [c for c in cited if "/" in c or c.endswith(".md") or c.endswith(".py")]
            if not paths:
                problems.append(f"{where}: rationale cites no repository path - every behavior traces to a correction")
            for c in paths:
                if not (Path(root) / c).exists():
                    problems.append(f"{where}: rationale cites {c}, which does not exist")
            prose = " ".join([b.title] + [b.fields.get(k, "") for k in REQUIRED])
            if re.search(r"\d", strip_code(prose)):
                problems.append(f"{where}: carries a figure - figures are calibration, not mechanism")
            for t in terms:
                if re.search(r"\b" + re.escape(t) + r"\b", prose, re.I):
                    problems.append(f"{where}: names the instance term '{t}' - calibration, not mechanism")
    return problems


# ---------------------------------------------------------------------------------------
# Leakage
# ---------------------------------------------------------------------------------------

def normalize(text):
    return " " + re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip() + " "


def spec_fragments(b):
    """The condition and expectation, whole and sentence by sentence."""
    out = []
    for k in ("condition", "expectation"):
        v = b.fields.get(k) or ""
        for frag in [v] + re.split(r"(?<=[.;:])\s+", v):
            n = normalize(frag)
            if len(n.strip()) >= LEAK_MIN_CHARS:
                out.append((k, n))
    return out


def leakage(specs, paths, spec_dir):
    """Every place a behavior ID or a spec sentence appears in an agent-facing file."""
    behaviors = all_behaviors(specs)
    if not behaviors:
        return 0, ["no behaviors found - a leakage check over an empty spec set checks nothing"]
    spec_root = Path(spec_dir).resolve()
    files = []
    for p in paths:
        p = Path(p)
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for q in sorted(p.rglob("*")):
                if q.is_file() and q.suffix.lower() in LEAK_SUFFIXES and ".git" not in q.parts:
                    files.append(q)
        else:
            return 0, [f"{p}: scan target does not exist"]
    files = [f for f in files if spec_root not in f.resolve().parents]
    if not files:
        return 0, ["no agent-facing files found - a leakage check over nothing checks nothing"]
    ids = {b.id for b in behaviors}
    frags = [(b.id, k, n) for b in behaviors for k, n in spec_fragments(b)]
    hits = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            for m in ID_ANY.finditer(line):
                if m.group(0) in ids:
                    hits.append(f"{f}:{n}: behavior ID {m.group(0)}")
        norm = normalize(text)
        for bid, k, frag in frags:
            if frag in norm:
                hits.append(f"{f}: {k} text of {bid}")
    return len(files), sorted(set(hits))


# ---------------------------------------------------------------------------------------
# Deterministic checks. Each returns a Result. DEFER means a necessary condition holds and
# the rest is a judgment for the grader; it is never a pass.
# ---------------------------------------------------------------------------------------

@dataclass
class Result:
    verdict: str            # TRUE | FALSE | N.A. | DEFER
    reason: str
    slices: list = field(default_factory=list)


def _steps(run_map, agents, kinds):
    for a in agents:
        for e in run_map["slices"][a][kinds]:
            yield a, e


def _all(run_map):
    return list(run_map["slices"])


def _caveat(blind):
    """A FALSE on reads or order that a shell step could have caused says so in its reason."""
    where = ", ".join(f"{a} step {n}" for a, n in blind[:6]) + (" ..." if len(blind) > 6 else "")
    return (f" [CAVEAT: {len(blind)} earlier shell step(s) whose reads are not observed ({where});"
            " this FALSE may be the recorder's limitation, not the agent's]")


def decomposition_precedes_commentary(run_map, agents, cfg):
    outs = [(a, o) for a, o in _steps(run_map, agents, "outputs") if o["subject"]]
    if not outs:
        return Result("N.A.", "no commentary output names a subject")
    tools = set(cfg.get("decomposition_tools", []))
    targets = cfg.get("decomposition_targets", [])
    decomp = {}
    for a, s in run_map["slices"].items():
        decomp[a] = [(n, subj) for n, t, tool, target, subj in s["order"]
                     if t in ("tool_call", "tool_result")
                     and (tool in tools or trajectory.matches(target, targets))]
    misses, seen = [], set()
    for a, o in outs:
        if (a, o["subject"]) in seen:
            continue
        seen.add((a, o["subject"]))
        ok = any(n < o["step"] and subj in (o["subject"], "*")
                 for anc in trajectory.lineage(run_map, a) for n, subj in decomp[anc])
        if not ok:
            blind = trajectory.unobserved_before(run_map, a, o["step"])
            misses.append((a, f"{a} step {o['step']}: commentary on '{o['subject']}' with no prior decomposition"
                           + (_caveat(blind) if blind else "")))
    if misses:
        return Result("FALSE", "; ".join(m for _, m in misses), sorted({a for a, _ in misses}))
    return Result("TRUE", f"{len(seen)} subject(s) commented, each after its decomposition")


def no_plan_write(run_map, agents, cfg):
    pats = cfg.get("plan_paths", [])
    touched = [e for _, e in list(_steps(run_map, agents, "reads")) + list(_steps(run_map, agents, "writes"))
               if trajectory.matches(e["target"], pats)]
    if not touched:
        return Result("N.A.", "no plan artifact read or written")
    bad = [(a, e) for a, e in _steps(run_map, agents, "writes") if trajectory.matches(e["target"], pats)]
    if bad:
        return Result("FALSE", "; ".join(f"{a} step {e['step']}: {e['tool']} to plan artifact {e['target']}"
                                         for a, e in bad), sorted({a for a, _ in bad}))
    return Result("TRUE", f"plan read {len(touched)} time(s), never written")


def no_record_write(run_map, agents, cfg):
    writes = list(_steps(run_map, agents, "writes"))
    if not writes:
        return Result("N.A.", "the run wrote nothing")
    bad = [(a, e) for a, e in writes if trajectory.matches(e["target"], cfg.get("record_paths", []))]
    if bad:
        return Result("FALSE", "; ".join(f"{a} step {e['step']}: {e['tool']} to record path {e['target']}"
                                         for a, e in bad), sorted({a for a, _ in bad}))
    return Result("TRUE", f"{len(writes)} write(s), none to a record path")


def single_delivery_artifact(run_map, agents, cfg):
    hits = [(a, e) for a, e in _steps(run_map, agents, "writes")
            if trajectory.matches(e["target"], cfg.get("delivery_paths", []))]
    targets = sorted({e["target"] for _, e in hits})
    if not targets:
        return Result("N.A.", "nothing was written to the delivery path")
    if len(targets) > 1:
        return Result("FALSE", f"{len(targets)} artifacts in the delivery path: " + ", ".join(
            f"{t} ({', '.join(sorted({a for a, e in hits if e['target'] == t}))})" for t in targets),
            sorted({a for a, _ in hits}))
    return Result("TRUE", f"one artifact delivered: {targets[0]}")


def cause_requires_document(run_map, agents, cfg):
    markers = [m.lower() for m in cfg.get("cause_markers", [])]
    causal = [(a, o) for a, o in _steps(run_map, agents, "outputs")
              if any(m in (o["text"] + " " + o["summary"]).lower() for m in markers)]
    if not causal:
        return Result("N.A.", "no output names a cause")
    docs = [e for _, e in _steps(run_map, _all(run_map), "reads")
            if trajectory.matches(e["target"], cfg.get("document_paths", []))]
    if not docs:
        blind = sorted({b for a, o in causal for b in trajectory.unobserved_before(run_map, a, o["step"])})
        return Result("FALSE", f"{len(causal)} output(s) name a cause and the run read no document: "
                      + ", ".join(f"{a} step {o['step']}" for a, o in causal)
                      + (_caveat(blind) if blind else ""),
                      sorted({a for a, _ in causal}))
    return Result("DEFER", f"{len(causal)} causal output(s), {len(docs)} document read(s) in the run; "
                  "whether each cause joins to one is a judgment")


def bare_metric_term(run_map, agents, cfg):
    outs = list(_steps(run_map, agents, "outputs"))
    if not outs:
        return Result("N.A.", "no output")
    reg = re.compile(cfg.get("registry_id_pattern", r"$^"))
    bad = []
    for a, o in outs:
        text = o["text"] + " " + o["summary"]
        for term in cfg.get("bare_metric_terms", []):
            if re.search(r"\b" + re.escape(term) + r"\b", text) and not reg.search(text):
                bad.append((a, f"{a} step {o['step']}: '{term}' with no registry ID"))
    if bad:
        return Result("FALSE", "; ".join(m for _, m in bad), sorted({a for a, _ in bad}))
    return Result("DEFER", "no configured bare term without a registry ID; metrics outside the "
                  "configured terms are a judgment")


def canonical_reads(run_map, agents, cfg):
    superseded = [s.strip("/") for s in cfg.get("superseded_docs", [])]
    if not superseded:
        return Result("N.A.", "no superseded list in the judge config - canonicity.py --export has not been run")
    docs = [(a, e) for a, e in _steps(run_map, agents, "reads") if e["target"].endswith(".md")]
    if not docs:
        return Result("N.A.", "no documentation read")
    marker = cfg.get("historical_read_marker", "historical").lower()
    bad = [(a, e) for a, e in docs
           if any(e["target"].strip("/").endswith(s) for s in superseded)
           and marker not in (e["subject"] + " " + e["summary"]).lower()]
    if bad:
        return Result("FALSE", "; ".join(f"{a} step {e['step']}: read superseded {e['target']}" for a, e in bad),
                      sorted({a for a, _ in bad}))
    return Result("TRUE", f"{len(docs)} document read(s), none superseded")


CHECKS = {f.__name__: f for f in (decomposition_precedes_commentary, no_plan_write, no_record_write,
                                   single_delivery_artifact, cause_requires_document,
                                   bare_metric_term, canonical_reads)}


# ---------------------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------------------

@dataclass
class Verdict:
    id: str
    title: str
    severity: str
    verdict: str            # TRUE | FALSE | N.A.
    kind: str               # deterministic | grader | ungraded
    reason: str
    slices: list
    file: str


def applies(spec, run_map):
    if spec.workflow not in ("*", run_map["workflow"]):
        return []
    return [a for a, s in run_map["slices"].items() if spec.agent in ("*", s["role"])]


def call_grader(cmd, request, timeout=300):
    try:
        p = subprocess.run(cmd, input=json.dumps(request), capture_output=True, text=True,
                           timeout=timeout, shell=isinstance(cmd, str))
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"grader failed: {e}"
    if p.returncode != 0:
        return None, f"grader exited {p.returncode}: {p.stderr.strip()[:200]}"
    try:
        v = json.loads(p.stdout)
    except json.JSONDecodeError:
        return None, "grader answered out of format: not JSON"
    if v.get("verdict") not in ("TRUE", "FALSE", "N.A.") or not v.get("reason"):
        return None, "grader answered out of format: needs verdict TRUE|FALSE|N.A. and a reason"
    return v, None


def grade(run_map, specs, cfg, grader_cmd=None, grader_name=None):
    verdicts, skipped = [], []
    for spec in specs:
        agents = applies(spec, run_map)
        if not agents:
            skipped.append(spec.path)
            continue
        for b in spec.behaviors:
            note = None
            if b.check:
                r = CHECKS[b.check](run_map, agents, cfg)
                if r.verdict != "DEFER":
                    verdicts.append(Verdict(b.id, b.title, b.severity, r.verdict, "deterministic",
                                            r.reason, r.slices, spec.path))
                    continue
                note = r.reason
            if not grader_cmd:
                reason = "no grader configured" + (f"; deterministic precondition holds: {note}" if note else "")
                verdicts.append(Verdict(b.id, b.title, b.severity, "N.A.", "ungraded", reason, [], spec.path))
                continue
            request = {"behavior": {"id": b.id, "title": b.title, **b.fields},
                       "run_id": run_map["run_id"], "workflow": run_map["workflow"],
                       "limitations": run_map.get("limitations", []),
                       "slices": {a: run_map["slices"][a] for a in agents},
                       "deterministic_note": note}
            v, err = call_grader(grader_cmd, request)
            if err:
                verdicts.append(Verdict(b.id, b.title, b.severity, "N.A.", "ungraded", err, [], spec.path))
            else:
                verdicts.append(Verdict(b.id, b.title, b.severity, v["verdict"], "grader", v["reason"],
                                        v.get("slices") or ([] if v["verdict"] != "FALSE" else ["run"]),
                                        spec.path))
    return verdicts, skipped


# ---------------------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------------------

def sheet(run_map, verdicts, skipped, grader_name, run_path):
    order = {s: i for i, s in enumerate(SEVERITIES)}
    false = sorted([v for v in verdicts if v.verdict == "FALSE"], key=lambda v: (order[v.severity], v.id))
    true = [v for v in verdicts if v.verdict == "TRUE"]
    na = [v for v in verdicts if v.verdict == "N.A." and v.kind != "ungraded"]
    ungraded = [v for v in verdicts if v.kind == "ungraded"]
    out = [f"# Verdict sheet · {run_map['run_id']}", "",
           f"*Generated by `package/judge.py` from `{run_path}`. The judge read the trajectory map, "
           f"not the raw log.*", "",
           f"- **Workflow:** {run_map['workflow'] or 'unstated'}",
           f"- **Slices:** {len(run_map['slices'])} ({', '.join(run_map['slices'])})",
           f"- **Steps:** {run_map['steps']}",
           f"- **Grader:** {grader_name or 'none configured'}",
           f"- **Graded:** {len(verdicts)} behaviors · **FALSE** {len(false)} · **TRUE** {len(true)} · "
           f"**N.A., condition did not arise** {len(na)} · **N.A., ungraded** {len(ungraded)}", ""]
    for lim in run_map.get("limitations", []):
        out += [f"> **Recorder limitation ({lim['kind']}):** {lim['statement']} "
                f"{len(lim['steps'])} step(s): "
                + ", ".join(f"{a} step {n}" for a, n in lim["steps"][:12])
                + (" ..." if len(lim["steps"]) > 12 else ""), ""]
    if skipped:
        out += ["Spec files not applicable to this run: " + ", ".join(f"`{os.path.relpath(s, ROOT)}`" for s in skipped), ""]

    def table(title, rows, blurb):
        out.extend([f"## {title}", "", blurb, ""])
        if not rows:
            out.extend(["None.", ""])
            return
        out.extend(["| Behavior | Severity | Graded by | Slice | Reason |", "|---|---|---|---|---|"])
        for v in rows:
            out.append(f"| {v.id} · {v.title} | {v.severity} | {v.kind} | {', '.join(v.slices) or '-'} | "
                       f"{v.reason.replace('|', '/')} |")
        out.append("")

    table("FALSE", false, "Each row is a review-ledger entry when `--ledger` is given. Root cause is left "
          "for the reviewer.")
    table("TRUE", true, "The behavior's condition arose and the run met it.")
    table("N.A. - the condition did not arise", na, "Not a pass. The run was not tested on these.")
    table("N.A. - ungraded", ungraded, "Not a pass. These need a judgment nobody made in this run; the "
          "reason says why.")
    return "\n".join(out)


def ledger_rows(run_map, records, verdicts, grader_name, cfg):
    ts = max((r.get("ts") or "" for r in records), default="")
    delivered = sorted({e["target"] for s in run_map["slices"].values() for e in s["writes"]
                        if trajectory.matches(e["target"], cfg.get("delivery_paths", []))})
    artefact = delivered[0] if len(delivered) == 1 else f"run:{run_map['run_id']}"
    rows = []
    for v in verdicts:
        if v.verdict != "FALSE":
            continue
        reviewer = "judge:deterministic" if v.kind == "deterministic" else f"judge:{grader_name}"
        for sl in v.slices or ["run"]:
            rows.append({
                "review_id": f"JDG:{run_map['run_id']}:{v.id}:{sl}",
                "timestamp": ts, "reviewer": reviewer,
                "agent": trajectory.role(sl) if sl != "run" else trajectory.role(run_map["root"]),
                "workflow": run_map["workflow"] or "", "run_id": run_map["run_id"],
                "artefact": artefact,
                "decision": "rejected" if v.severity == "blocking" else "approved_with_edits",
                "edit_type": "cosmetic" if v.severity == "advisory" else "material_narrative",
                "edit_description": f"{v.id} {v.title}: {v.reason}",
                "root_cause": "", "materiality_usd": "", "agent_flagged_uncertainty": "",
                "behavior_id": v.id, "severity": v.severity, "slice": sl,
            })
    return rows


def write_ledger(path, rows, columns):
    path = Path(path)
    new = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--specs", required=True, help="directory of behavior spec files")
    ap.add_argument("--config", help="judge config JSON (default: <specs>/judge-config.json)")
    ap.add_argument("--root", default=str(ROOT), help="repository root for resolving rationale paths")
    ap.add_argument("--check-specs", action="store_true", help="spec hygiene only")
    ap.add_argument("--check-leakage", nargs="+", metavar="PATH",
                    help="fail if spec IDs or text appear in these agent-facing files or folders")
    ap.add_argument("--run", help="trajectory JSONL to grade")
    ap.add_argument("--out", help="write the verdict sheet here (default: stdout)")
    ap.add_argument("--json", help="write verdicts as JSON here")
    ap.add_argument("--ledger", help="append review-ledger rows for every FALSE to this CSV")
    ap.add_argument("--grader-cmd", help="command implementing the grader protocol (overrides config)")
    ap.add_argument("--grader-name", help="name recorded as reviewer=judge:<name>")
    ap.add_argument("--expect-false", help="comma-separated IDs; exit 0 only if exactly these are FALSE")
    a = ap.parse_args(argv)

    cfg_path = Path(a.config or Path(a.specs) / "judge-config.json")
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        specs = parse_specs(a.specs)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR  cannot read specs or config: {e}", file=sys.stderr)
        return 2

    if a.check_specs:
        problems = check_specs(specs, cfg, Path(a.root))
        for p in problems:
            print("FAIL  " + p)
        n = len(all_behaviors(specs))
        print(f"{'CLEAN' if not problems else 'FAILED'}: {len(specs)} spec file(s), {n} behaviors, "
              f"{len(problems)} problem(s)")
        return 0 if not problems else 1

    if a.check_leakage:
        scanned, hits = leakage(specs, a.check_leakage, a.specs)
        for h in hits:
            print("LEAK  " + h)
        print(f"{'CLEAN' if not hits else 'FAILED'}: {len(all_behaviors(specs))} behaviors checked against "
              f"{scanned} agent-facing file(s), {len(hits)} leak(s)")
        return 0 if not hits else 1

    if not a.run:
        ap.error("one of --check-specs, --check-leakage or --run is required")
    try:
        records = trajectory.read(a.run)
    except (OSError, ValueError) as e:
        print(f"ERROR  {e}", file=sys.stderr)
        return 2
    problems = trajectory.validate(records)
    if problems:
        for p in problems:
            print("ERROR  " + p, file=sys.stderr)
        return 2

    grader = a.grader_cmd
    name = a.grader_name
    if not grader and cfg.get("grader"):
        grader = cfg["grader"].get("command")
        name = name or cfg["grader"].get("name")
    if grader and not name:
        name = shlex.split(grader)[0] if isinstance(grader, str) else str(grader[0])

    run_map = trajectory.build_map(records, cfg)
    verdicts, skipped = grade(run_map, specs, cfg, grader, name)
    text = sheet(run_map, verdicts, skipped, name, a.run)
    if a.out:
        Path(a.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if a.json:
        Path(a.json).write_text(json.dumps([v.__dict__ for v in verdicts], indent=2) + "\n", encoding="utf-8")
    if a.ledger:
        write_ledger(a.ledger, ledger_rows(run_map, records, verdicts, name, cfg),
                     cfg.get("ledger_columns"))

    false = sorted(v.id for v in verdicts if v.verdict == "FALSE")
    print(f"\nFALSE: {', '.join(false) or 'none'}", file=sys.stderr)
    if a.expect_false is not None:
        want = sorted(x.strip() for x in a.expect_false.split(",") if x.strip())
        missed, extra = sorted(set(want) - set(false)), sorted(set(false) - set(want))
        for m in missed:
            print(f"FAIL  seed {m} expected FALSE and was not - the judge missed a planted failure", file=sys.stderr)
        for x in extra:
            print(f"FAIL  {x} FALSE and not a planted seed", file=sys.stderr)
        print(f"SEED PACK {'REPRODUCED' if not missed and not extra else 'BROKEN'}: "
              f"{len(want) - len(missed)} of {len(want)} planted failures found, {len(extra)} unexpected",
              file=sys.stderr)
        return 0 if not missed and not extra else 1
    return 1 if any(v.verdict == "FALSE" and v.severity in FAILING for v in verdicts) else 0


if __name__ == "__main__":
    sys.exit(main())
