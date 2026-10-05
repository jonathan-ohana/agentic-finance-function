"""Replay the seed fixture through the recorder and check the map. See README.md."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIX = Path(__file__).resolve().parent
# The recorder lives at package/instrumentation/ in the repository and at _instrumentation/ in
# an instance; trajectory.py at package/ or the instance's _generator/.
TRACE = next(b / r for b in FIX.parents
             for r in ("package/instrumentation/variancetrace.py", "_instrumentation/variancetrace.py")
             if (b / r).exists())
for p in (TRACE.parent.parent / "_generator", TRACE.parent.parent):
    if (p / "trajectory.py").exists():
        sys.path.insert(0, str(p))
        break
import trajectory  # noqa: E402


def run(args, env, stdin=None):
    p = subprocess.run([sys.executable, str(TRACE)] + args, input=stdin, env=env,
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def main():
    tmp = Path(tempfile.mkdtemp(prefix="vt-fixture-"))
    env = dict(os.environ, ARCLINE_TRACE_STATE=str(tmp / "state"))
    try:
        rc, out = run(["start", "--period", "FIXTURE", "--log-dir", str(tmp / "log")], env)
        if rc:
            print(out); return 1
        fixture = FIX.as_posix()
        for line in (FIX / "events.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                run(["hook"], env, stdin=line.replace("{FIXTURE}", fixture))
        errs = tmp / "state" / "hook-errors.log"
        rc, out = run(["finish"], env)
        print(out.rstrip())
        log = next((tmp / "log").glob("*.jsonl"))
        records = trajectory.read(log)
        m = trajectory.build_map(records)
        exp = json.loads((FIX / "expected.json").read_text(encoding="utf-8"))
        fails = []
        if errs.exists():
            fails.append("hook errors: " + errs.read_text(encoding="utf-8").strip())
        for name, e in exp["slices"].items():
            s = m["slices"].get(name)
            if not s:
                fails.append(f"{name}: no steps"); continue
            for k in ("outputs", "escalations", "refusals"):
                if len(s[k]) != e[k]:
                    fails.append(f"{name}: {k} {len(s[k])}, expected {e[k]}")
            got = [x["subject"] for k in ("outputs", "escalations", "refusals") for x in s[k]]
            if sorted(got) != sorted(e["subjects"]):
                fails.append(f"{name}: subjects {got}")
        bad = [(a, x["subject"]) for a, s in m["slices"].items() for x in s["outputs"]
               if x["subject"] in exp["forbidden_output_subjects"]]
        if bad:
            fails.append(f"forbidden output subjects recorded: {bad}")
        acks = sum(1 for r in records if r["type"] == "reason"
                   and "launched in background" in (r.get("summary") or ""))
        if acks != exp["launch_acks_recorded_as_reason"]:
            fails.append(f"launch acknowledgements recorded as reason: {acks}, "
                         f"expected {exp['launch_acks_recorded_as_reason']}")
        for f in fails:
            print("  FIXTURE FAIL  " + f)
        print("  FIXTURE PASS" if not fails else f"  FIXTURE FAIL: {len(fails)}")
        return 0 if not fails else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
