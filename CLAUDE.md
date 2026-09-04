# CLAUDE.md

House rules for this repository. Read this before touching prose, figures, or the
verifiers. It is deliberately short: everything here is enforced somewhere, and the
enforcement is named next to the rule.

This repository is a worked prototype of a finance function run by agents under a
governance layer. The product is not the arithmetic — it is the layer that stops a
finance function silently changing definitions, inventing causes, or repeating a
corrected mistake. Edits that make the prose tidier at the cost of that layer are
regressions, even when every number in them is right.

---

## 1. The judgment-layer doctrine

Three rules. They outrank helpfulness, tidiness, and the desire to close a task.

**Agents propose, never enact.** A proposal is a drafted ruling in the record format
of [`semantic-layer/definitions-template.md`](semantic-layer/definitions-template.md)
Part 3, with the forcing case and the evidence attached. The best proposals arrive
pre-written and are accepted verbatim; they still arrive as proposals. In this
repository that means: open a PR, state the ruling and its evidence, and let a human
merge it. Do not write a new ruling into the change log or the registry as though it
had been ratified.

**A refusal is a valid output — and a named refusal beats a silent one.** `NOT
COMPUTABLE`, `NOT OBSERVABLE`, `n/a — no churn observed`, and the `unverifiable`
class in the register are all correct answers. What is never correct is producing a
plausible number to avoid producing none, or dropping a figure quietly because it
could not be supported. Say which artifact or which ruling would be needed. See
SL-24 in [`semantic-layer/definitions-instance.md`](semantic-layer/definitions-instance.md)
for the pattern.

**Every figure traces to an artifact or a registry entry.** A number in prose is
either recalculated from a workbook that ships in this repository, or it is a figure
whose basis is a registry entry cited by ID and version — `MET-009@1.0`, not "ARR".
The bare word *ARR* is banned by SL-08; the same discipline applies to any metric
with more than one defensible basis. A figure that traces to neither is not a
rounding problem, it is an unsourced claim.

**Corollary — the semantic layer is read-only.** Rule 6 of the template:
`semantic-layer/definitions-instance.md` is the one artefact every agent reads and no
agent writes. An agent that can edit the definition it is measured against can make
any output correct by construction. Propose the ruling in the PR body; the owner
writes it in. This holds even when the ruling is obviously right.

---

## 2. The docverify contract

[`outputs/docverify.py`](outputs/docverify.py) asks one question: *does the write-up
still agree with the artifact it describes?* It writes
[`outputs/docverify-register.md`](outputs/docverify-register.md), and CI regenerates
that file and diffs it against the committed one — so the register is a build output,
never hand-edited.

**Three obligations, in order:**

1. **Any new figure-heavy write-up must be classified in `outputs/docverify.py` or CI
   fails.** The threshold is `UNCLASSIFIED_FAIL_AT` figures. Adding a doc that quotes
   figures without deciding what kind of claim it makes is a failure, not an omission.
   Below the threshold it is noted rather than failed, because two incidental figures
   do not make a write-up a claim.
2. **Run `python3 outputs/docverify.py .` from the repository root** after any change
   that adds, removes, or moves a figure — including a change to a `record` or
   `illustrative` doc, because figure counts and the side-by-side section both move.
3. **Commit the regenerated register with the doc change, in the same commit.** A doc
   change with a stale register fails the `git diff --exit-code` step in
   [`.github/workflows/verify.yml`](.github/workflows/verify.yml) even when every
   figure is right.

**What it needs to run:** `pip install openpyxl` and a real spreadsheet engine —
`libreoffice-calc` specifically, not just `libreoffice-core`. The workbooks carry no
cached values, so the checker recalculates them; a checker that trusts what is typed
in the file it is checking has checked nothing. With only `libreoffice-core`
installed, conversion fails with *"source file could not be loaded"* and the run dies
in `openpyxl` on a missing temp file — install `libreoffice-calc` and rerun.

**Escape hatch, used sparingly.** A line that legitimately quotes a figure from
outside the artifact carries a trailing `<!-- docverify: external -->`. It exempts the
whole line from both the artifact check and the side-by-side. Reach for a
reclassification before reaching for this.

**The side-by-side section** lists every named metric quoted with more than one value,
with doc and line for each. It is reported, not scored — across dated records a moving
figure is usually the design working. The one case with no innocent reading, and the
one that fails the build, is **two `current` docs disagreeing on the same metric and
stated period**. Do not "fix" a side-by-side entry by rewriting a record; see §3.

---

## 3. The four write-up classes

Every write-up that quotes figures carries exactly one, declared in
`outputs/docverify.py`.

| Class | One-line definition | What it obliges |
|---|---|---|
| `current` | Describes a shipped artifact. | Every quoted figure must exist in the **recalculated** workbook. A `current` doc from which no figures can be extracted also fails: a check that can pass on an empty set is not a check. |
| `record` | A dated account of a run, a fix, or an audit. | Not gated against today's artifact. Its figures were true when written and are kept because the failures changed the design. **Never restate a record to match the present** — gating history against the present would force the record to lie. Annotate it instead: a dated pointer to what superseded it. |
| `illustrative` | Charters, contracts, specs, playbooks, the registry. | Figures are worked examples or rulings, not claims about a shipped artifact. They must still be internally consistent and must not claim a metric name whose ruled basis they do not use. |
| `unverifiable` | Describes an artifact not published in this repository. | The verdict is a named refusal, not silence. The register states which artifact would be needed to check it. |

**Choosing between them.** Ask what kind of claim the doc makes, not how old it is.
A dated run report that quotes figures from a workbook that ships here is still a
`record` — the date is the point. A spec whose figures are design parameters is
`illustrative` even if it happens to agree with a shipped workbook today.

**The classifications are themselves the deliverable.** "Not checked" was silence;
*"record, 25 Aug, superseded by the shipped pack"* is a statement someone can dispute.

---

## 4. Working conventions

- **Two other verifiers, both cheap to run:** `python3 verify_repository.py` (checksums,
  workbook structure, every relative Markdown link resolves) and
  [`outputs/packverify.py`](outputs/packverify.py) (the shipped pack against the
  instance CSVs). Run `verify_repository.py` after adding any link.
- **Two instances live here.** The published workbooks are **Arcline**. The
  demonstration instance — the padel/courts company — has most of the rulings and
  most of the quoted figures, and its workbooks are *not* published here. That is why
  several docs are `unverifiable` rather than `current`. Do not reconcile a figure
  across the two.
- **Failures are kept, not cleaned up.** [`what-broke/`](what-broke/),
  [`red-team/`](red-team/), and the [run log](runs/run-log.md) exist because the
  failures shaped the design. Deleting a wrong number from a record destroys the
  evidence that the correction happened.
- **Say what was actually compared.** Rule 7 of the template: a verdict asserts only
  what was compared and must say what that was. "The figures reconcile" when two of
  five were checked is an accurate sentence that misleads.
