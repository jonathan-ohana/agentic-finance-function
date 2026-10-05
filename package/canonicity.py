"""
Which document is the current word on its subject, and which ones are history.

Every write-up declares one status in an HTML comment, invisible when rendered:

    <!-- canon: canonical -->     the current word on its subject
    <!-- canon: superseded -->    replaced; names its successor with
    <!-- superseded-by: path -->
    <!-- canon: record -->        a dated account - true on its date, never superseded
    <!-- canon: external -->      describes something outside this repository

and a successor names what it replaces:

    <!-- supersedes: path -->

Paths are repository-relative. A link from a canonical document to a superseded one is a
stale reference unless the line carries `<!-- canon: historical -->`.

Checks, each a failure:

    every document classified (reported, not failed, under --allow-unclassified)
    one status per document
    a superseded document names its successor; only a superseded document does
    every successor exists and is canonical
    the relations are symmetric in both directions
    no cycles in the supersedes graph
    a record is never superseded - it was true on its date, and replacing it would make the
      history say something it never said
    no canonical document links to a superseded one unless the link is marked historical
    no duplicate document numbers where a numbered series exists: the number in an H1 title
      ("# 81 - ...") repository-wide, and a filename prefix ("01-...") within its folder

Writes the register (outputs/canon-register.md by default) with the same contract as
docverify-register.md: generated, never hand-edited, diffed in CI. --export writes the
superseded list into the judge config, so the judge's canonical-reads behavior stops
returning N.A.

The doctrine, and why this classifies the tree in place rather than rewriting it, is in
CANON.md.

    python3 canonicity.py [--root .] [--config package/behaviors/judge-config.json]
                          [--allow-unclassified] [--register PATH] [--export]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

STATUSES = ("canonical", "superseded", "record", "external")
STATUS_RE = re.compile(r"<!--\s*canon:\s*([a-z-]+)\s*-->")
SUPERSEDES_RE = re.compile(r"<!--\s*supersedes:\s*(\S+?)\s*-->")
SUPERSEDED_BY_RE = re.compile(r"<!--\s*superseded-by:\s*(\S+?)\s*-->")
HISTORICAL = "historical"
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
H1_NUM = re.compile(r"^#\s+(\d+[a-z]?)\s+[—–-]\s")
FILE_NUM = re.compile(r"^(\d+)-")
DEFAULT_CONFIG = Path(__file__).resolve().parent / "behaviors" / "judge-config.json"


def documents(root, roots, exclude):
    out = set()
    for r in roots:
        if any(ch in r for ch in "*?["):
            out.update(p for p in root.glob(r) if p.is_file())
        elif (root / r).is_dir():
            out.update(p for p in (root / r).rglob("*.md") if ".git" not in p.parts)
        elif (root / r).is_file():
            out.add(root / r)
    rels = {p.relative_to(root).as_posix() for p in out}
    return sorted(rels - set(exclude))


def strip_code(text):
    """Examples of the syntax inside code are not declarations. Fenced blocks become blank
    lines so line numbers still match the file."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def read_doc(root, rel):
    text = strip_code((root / rel).read_text(encoding="utf-8"))
    lines = text.splitlines()
    statuses = [s for s in STATUS_RE.findall(text) if s != HISTORICAL]
    h1 = next((l for l in lines if l.startswith("# ")), "")
    m = H1_NUM.match(h1)
    links = []
    for n, line in enumerate(lines, 1):
        for target in LINK_RE.findall(line):
            t = target.strip().split(maxsplit=1)[0].strip("<>")
            if not t or t.startswith(("#", "http://", "https://", "mailto:")):
                continue
            f = unquote(t.split("#", 1)[0])
            if not f:
                continue
            resolved = ((root / rel).parent / f).resolve()
            try:
                links.append((n, resolved.relative_to(root.resolve()).as_posix(),
                              f"<!-- canon: {HISTORICAL} -->" in line))
            except ValueError:
                continue
    return {
        "statuses": statuses,
        "status": statuses[0] if statuses else None,
        "supersedes": SUPERSEDES_RE.findall(text),
        "superseded_by": SUPERSEDED_BY_RE.findall(text),
        "h1_number": m.group(1) if m else None,
        "file_number": (FILE_NUM.match(Path(rel).name) or [None, None])[1],
        "links": links,
    }


def check(root, docs, allow_unclassified):
    fails, notes = [], []
    unclassified = [d for d, v in docs.items() if not v["status"]]
    for d in unclassified:
        (notes if allow_unclassified else fails).append(f"{d}: unclassified")

    for d, v in docs.items():
        if len(v["statuses"]) > 1:
            fails.append(f"{d}: {len(v['statuses'])} status comments - one per document")
        if v["status"] and v["status"] not in STATUSES:
            fails.append(f"{d}: status '{v['status']}' is not one of {', '.join(STATUSES)}")
        if v["status"] == "superseded" and not v["superseded_by"]:
            fails.append(f"{d}: superseded with no superseded-by - a superseded document names its successor")
        if v["superseded_by"] and v["status"] != "superseded":
            fails.append(f"{d}: names a successor but is {v['status'] or 'unclassified'}, not superseded")
        if v["status"] == "record" and v["superseded_by"]:
            fails.append(f"{d}: a record is never superseded - it was true on its date")
        for s in v["superseded_by"]:
            if s not in docs:
                fails.append(f"{d}: dangling successor {s} - no such document")
                continue
            if docs[s]["status"] != "canonical":
                fails.append(f"{d}: successor {s} is {docs[s]['status'] or 'unclassified'}, not canonical")
            if d not in docs[s]["supersedes"]:
                fails.append(f"{d}: names {s} as successor, but {s} does not list it under supersedes")
        for s in v["supersedes"]:
            if s not in docs:
                fails.append(f"{d}: supersedes {s} - no such document")
                continue
            if docs[s]["status"] == "record":
                fails.append(f"{d}: supersedes the record {s} - a record is never superseded")
            if d not in docs[s]["superseded_by"]:
                fails.append(f"{d}: supersedes {s}, but {s} does not name it as superseded-by")

    # Cycles in the supersedes graph.
    graph = {d: [s for s in v["supersedes"] if s in docs] for d, v in docs.items()}
    state, cycles = {}, set()

    def visit(n, path):
        state[n] = 1
        for m in graph[n]:
            if state.get(m) == 1:
                cycles.add(" -> ".join(path[path.index(m):] + [m]))
            elif not state.get(m):
                visit(m, path + [m])
        state[n] = 2
    for d in sorted(graph):
        if not state.get(d):
            visit(d, [d])
    fails.extend(f"supersedes cycle: {c}" for c in sorted(cycles))

    # Stale references: a canonical document pointing a reader at a superseded one.
    for d, v in docs.items():
        if v["status"] != "canonical":
            continue
        for n, target, historical in v["links"]:
            if docs.get(target, {}).get("status") == "superseded" and not historical:
                fails.append(f"{d}:{n}: canonical document links to superseded {target} "
                             f"without <!-- canon: historical -->")

    # Duplicate numbers, where a numbered series exists.
    by_h1, by_file = {}, {}
    for d, v in docs.items():
        if v["h1_number"]:
            by_h1.setdefault(v["h1_number"], []).append(d)
        if v["file_number"]:
            by_file.setdefault((str(Path(d).parent), v["file_number"]), []).append(d)
    for num, ds in sorted(by_h1.items(), key=lambda kv: (int(re.sub(r"\D", "", kv[0])), kv[0])):
        if len(ds) > 1:
            fails.append(f"duplicate document number #{num} in H1 titles: {', '.join(sorted(ds))}")
    for (folder, num), ds in sorted(by_file.items()):
        if len(ds) > 1:
            fails.append(f"duplicate filename number {num} in {folder}/: {', '.join(sorted(ds))}")
    return fails, notes, unclassified


def register(docs, fails, notes, allow_unclassified):
    counts = {s: sum(1 for v in docs.values() if v["status"] == s) for s in STATUSES}
    counts["unclassified"] = sum(1 for v in docs.values() if not v["status"])
    out = ["# Canon register", "",
           "*Generated by `package/canonicity.py`. Do not edit; rerun. No date on purpose: CI "
           "regenerates this file and diffs it against the committed one, so its content may depend "
           "only on the tree.*", "",
           "Which write-up is the current word on its subject, and which are history. The doctrine is "
           "in [CANON.md](../CANON.md).", "",
           "| Status | Documents |", "|---|---:|"]
    out += [f"| {k} | {v} |" for k, v in counts.items()]
    out += ["", f"Unclassified documents are {'reported, not failed (--allow-unclassified)' if allow_unclassified else 'failures'}.", "",
            "## Findings", ""]
    out += [f"- FAIL {f}" for f in fails] or ["None."]
    out += ["", "## Documents", "", "| Document | Status | Number | Supersedes | Superseded by |",
            "|---|---|---|---|---|"]
    for d, v in docs.items():
        num = v["h1_number"] or v["file_number"] or ""
        out.append(f"| {d} | {v['status'] or 'unclassified'} | {num} | "
                   f"{', '.join(v['supersedes'])} | {', '.join(v['superseded_by'])} |")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--allow-unclassified", action="store_true",
                    help="report unclassified documents without failing on them")
    ap.add_argument("--register", help="where to write the register (default: from config; '-' for stdout)")
    ap.add_argument("--export", action="store_true",
                    help="write the superseded list into the judge config")
    a = ap.parse_args(argv)

    root = Path(a.root).resolve()
    cfg_path = Path(a.config)
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    canon = cfg.get("canonicity", {})
    rels = documents(root, canon.get("roots", ["*.md"]), canon.get("exclude", []))
    if not rels:
        print("FAIL  no documents under the configured roots - a check that can pass on an empty set "
              "is not a check")
        return 1
    docs = {r: read_doc(root, r) for r in rels}
    fails, notes, unclassified = check(root, docs, a.allow_unclassified)

    for f in fails:
        print("FAIL  " + f)
    if notes:
        print(f"NOTE  {len(notes)} document(s) unclassified (allowed)")
    reg = register(docs, fails, notes, a.allow_unclassified)
    target = a.register or canon.get("register", "outputs/canon-register.md")
    if target == "-":
        print(reg)
    else:
        path = Path(target) if Path(target).is_absolute() else root / target
        path.write_text(reg, encoding="utf-8")
        print(f"Register written to {target}")

    if a.export:
        if fails:
            print("REFUSED  --export: a register that fails is not a source for the judge")
            return 1
        cfg["superseded_docs"] = sorted(d for d, v in docs.items() if v["status"] == "superseded")
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        print(f"Exported {len(cfg['superseded_docs'])} superseded document(s) to {cfg_path}")

    print(f"{'CLEAN' if not fails else 'FAILED'}: {len(docs)} documents, {len(fails)} failure(s), "
          f"{len(unclassified)} unclassified")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
