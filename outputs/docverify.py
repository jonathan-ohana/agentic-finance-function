"""
Does the write-up still agree with the artifact it describes?

Nothing else in this instance reads prose. packverify.py asserts the workbook against the
instance CSVs; validate.py asserts the instance against itself. Both pass while a document
quoting those workbooks goes stale, which is exactly what happened between 28 Aug and 1 Sep:
the pack was rebuilt, the write-up was not, and the only figures a reader could see were the
wrong ones.

The rule this enforces is deliberately weak and therefore cheap to keep true:

    every figure quoted in a write-up must exist somewhere in the workbook it describes.

It does not check that a figure is in the right row. A number in the wrong row is a different
defect and needs a different check. This one catches the failure that actually occurs — an
artifact is rebuilt and the prose keeps yesterday's numbers — because a stale figure almost
never survives as a coincidence somewhere else in the same workbook.

The workbooks carry no cached values, so this reads RECALCULATED values, the same way
packverify does. A checker that trusts what is typed in the file it is checking has checked
nothing.

    python3 docverify.py <instance folder> <docs folder>

Exempt a line that legitimately quotes a figure from outside the artifact with a trailing
marker:  <!-- docverify: external -->
"""
import os, re, sys, subprocess, tempfile
from openpyxl import load_workbook

FOLDER = (sys.argv[1] if len(sys.argv) > 1 else
          os.environ.get("ARCLINE_FOLDER", "/home/claude/out/Arcline-Finance"))
DOCS = (sys.argv[2] if len(sys.argv) > 2 else
        os.environ.get("ARCLINE_DOCS", os.path.join(FOLDER, "..", "docs")))

# Which write-up describes which artifacts. A doc with no entry here is not checked -
# and that is the gap to watch: an unlisted doc is an unverified doc.
DESCRIBES = {
    "outputs/arcline-pack-and-lbe.md": [
        ("08-reporting/FY2026", "FY2026-01-management-pack.xlsx"),
        ("05-lbe/FY2026", "LBE_Q1_2026_M1.xlsx"),
    ],
}

MONEY_TOL = 1.0      # the doc rounds to whole units
PCT_TOL = 0.06       # the doc rounds a percentage to one decimal
DEC_TOL = 0.06       # ... and a day-count or month-count the same way

EXEMPT = "docverify: external"
METRIC_WORDS = ("dso", "runway", "days", "months", "pts")

results = []


def chk(name, ok, detail=""):
    results.append((bool(ok), name, detail))
    print(("PASS  " if ok else "FAIL  ") + name + ("  " + str(detail) if detail else ""))


def recalc(path, out):
    """Open the workbook and let the spreadsheet engine compute it, exactly as a reader would."""
    subprocess.run(["libreoffice", "--headless", "--convert-to", "xlsx", "--outdir", out, path],
                   check=True, capture_output=True, timeout=420)
    return os.path.join(out, os.path.basename(path))


def workbook_values(paths):
    """Every number the workbooks actually compute, in the three shapes a doc quotes them."""
    money, pct, dec = set(), set(), set()
    with tempfile.TemporaryDirectory() as tmp:
        for p in paths:
            wb = load_workbook(recalc(p, tmp), data_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    for c in row:
                        v = c.value
                        if not isinstance(v, (int, float)) or isinstance(v, bool):
                            continue
                        money.add(round(abs(float(v))))
                        pct.add(round(abs(float(v)) * 100, 1))   # 0.0256 -> 2.6
                        pct.add(round(abs(float(v)), 1))         # already a percentage
                        dec.add(round(abs(float(v)), 1))
    return money, pct, dec


MONEY_RE = re.compile(r'\(?\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b\)?')
PCT_RE = re.compile(r'\b\d+\.\d+\s*%')
DEC_RE = re.compile(r'(?<![\d,.])\d+\.\d(?![\d%])')


def figures(line):
    """The figures a reader would take from this line as facts about the artifact."""
    out = []
    for m in MONEY_RE.findall(line):
        out.append(("money", abs(float(m.strip("()").replace(",", "")))))
    for m in PCT_RE.findall(line):
        out.append(("pct", abs(float(m.rstrip("% ").strip()))))
    if any(w in line.lower() for w in METRIC_WORDS):
        for m in DEC_RE.findall(line):
            out.append(("dec", abs(float(m))))
    return out


def near(value, pool, tol):
    return any(abs(value - p) <= tol for p in pool)


def main():
    if not os.path.isdir(DOCS):
        chk("Docs folder is reachable", False, DOCS)
        return 1

    checked_docs = 0
    for rel, arts in DESCRIBES.items():
        doc = os.path.join(DOCS, rel)
        if not os.path.exists(doc):
            chk(f"{rel} exists", False, doc)
            continue
        checked_docs += 1
        paths = [os.path.join(FOLDER, d, f) for d, f in arts]
        missing = [p for p in paths if not os.path.exists(p)]
        if missing:
            chk(f"{rel} - its artifacts exist", False, missing)
            continue

        money, pct, dec = workbook_values(paths)
        pools = {"money": (money, MONEY_TOL), "pct": (pct, PCT_TOL), "dec": (dec, DEC_TOL)}

        orphans, quoted = [], 0
        for n, line in enumerate(open(doc, encoding="utf-8").read().splitlines(), 1):
            if EXEMPT in line:
                continue
            for kind, v in figures(line):
                quoted += 1
                pool, tol = pools[kind]
                if not near(v, pool, tol):
                    orphans.append(f"line {n}: {v:,.1f} ({kind})")

        chk(f"{rel} - every quoted figure exists in the artifact",
            not orphans,
            f"{quoted} figures checked" + (f", {len(orphans)} orphaned: " + "; ".join(orphans[:6])
                                           if orphans else ""))

    # An unlisted write-up is an unverified write-up. Say so rather than reporting silence.
    unlisted = []
    for root, _, files in os.walk(DOCS):
        if os.sep + "." in root:
            continue
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), DOCS).replace(os.sep, "/")
            if rel in DESCRIBES:
                continue
            text = open(os.path.join(root, f), encoding="utf-8").read()
            if sum(1 for ln in text.splitlines() for _ in MONEY_RE.findall(ln)) >= 8:
                unlisted.append(rel)
    # Reported, not scored. A permanently red check is a check nobody reads; the point of this
    # line is that the number should fall over time, and that somebody sees it when it does not.
    print(f"\nNOTE  {checked_docs} write-up(s) mapped to an artifact and checked. "
          f"{len(unlisted)} figure-heavy write-up(s) quote numbers nothing verifies:")
    for rel in sorted(unlisted):
        print(f"        {rel}")

    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)} of {len(results)} checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
