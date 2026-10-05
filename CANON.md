# Canon

<!-- canon: canonical -->

Which write-up is the current word on its subject, which ones are history, and why this
repository is classified in place rather than rewritten.

The instrument is [`package/canonicity.py`](package/canonicity.py). This document is the
doctrine it enforces. House rules in [CLAUDE.md](CLAUDE.md) win over anything here.

---

## The problem

A repository built by correcting itself accumulates documents that were right when written
and are not the current word any more. A pack was rebuilt and its write-up was not; a
contract was amended twice and the amendments live below the original; a ruling resolved a
question that an earlier design document still leaves open. A human reader works out which
is current from dates and context. An agent retrieving documentation does not. It reads
whatever ranks first, and a superseded document reads exactly as confidently as its
successor.

[`docverify.py`](outputs/docverify.py) answers a different question: whether a write-up's
figures agree with the artifact it describes. Its classes (`current`, `record`,
`illustrative`, `unverifiable`) say what kind of claim a document makes about figures.
Canonicity says whether the document is the one to follow. The two are related and
independent: a charter can be `illustrative` to docverify and `superseded` here.

## Four statuses

Each document declares exactly one, as an HTML comment that does not render:

| Status | Meaning | Obligation |
|---|---|---|
| `canonical` | The current word on its subject. | Every successor named anywhere must be canonical. It may not send a reader to a superseded document except through a link marked historical. |
| `superseded` | Replaced. Kept because the replacement is easier to trust when the thing it replaced is still visible. | Names its successor with `superseded-by`. The successor names it back with `supersedes`. |
| `record` | A dated account of a run, a fix, an audit or a review. | **Never superseded.** A record was true on its date. Replacing it would make the history say something it never said. A later record can follow it; it does not replace it. |
| `external` | Describes something outside this repository. | Nothing here can supersede it; this repository does not own the subject. |

```
<!-- canon: superseded -->
<!-- superseded-by: path/to/successor.md -->
```

```
<!-- canon: canonical -->
<!-- supersedes: path/to/predecessor.md -->
```

A link from a canonical document to a superseded one is allowed only when the line carries
`<!-- canon: historical -->`, the same pattern as docverify's external marker. Pointing a
reader at history on purpose is fine. Pointing them at it by accident is a stale reference.

## What the checks enforce

Every document classified. Successors exist and are canonical. Relations symmetric in both
directions. No cycles. No record superseded. No stale references. No duplicate document
numbers where a numbered series exists, whether in H1 titles across the repository or as a
filename prefix within a folder. The register, `outputs/canon-register.md`, is generated and
diffed in CI under the same contract as
[`docverify-register.md`](outputs/docverify-register.md): a build output, never edited by hand.

`canonicity.py --export` writes the superseded list into the
[judge config](package/behaviors/judge-config.json), which is how the judge learns which
documents an agent should not be reading as current guidance. Until the first export, that
behavior is graded N.A. with the reason stated. That is the honest verdict, not a pass.

## Who classifies

**The owner, one document at a time.** Whether a document is still the current word is a
judgment about its subject, not about its age or its folder, and it is the same kind of
judgment as a ruling in the semantic layer. An agent may propose a classification in a PR,
with its reasoning. It does not tag the tree itself, for the same reason it does not edit
the registry.

The instrument ships before the rulings. It runs with `--allow-unclassified` while
classification is in progress, so that dangling successors, asymmetric relations, record
supersessions and stale references gate from the first tagged document onward. The flag
comes off when the owner says the classification is complete, in its own change.

## Why the repository is not being rewritten

The obvious fix for a tree whose documents disagree about what is current is to rewrite it:
fold the corrections into the documents they corrected, renumber the series, move every
write-up into a clean structure, delete what was superseded. We are not doing that.

Three checkers are anchored to the tree as it stands.

- [`verify_repository.py`](verify_repository.py) holds the published artifacts to the
  checksums in the manifest and resolves every relative link in every Markdown file, plus
  every repository link on the landing page.
- [`docverify.py`](outputs/docverify.py) classifies every figure-heavy write-up **by path**,
  and gates the `current` ones against the recalculated workbooks.
- [`packverify.py`](outputs/packverify.py) holds the shipped pack against the instance data
  it was built from.

Each one passed against this tree, and each pass is a statement about these files at these
paths. A rewrite would move the files out from under all three. Afterwards the checkers
would pass again, against the rewritten tree, and the record that the original was checked
would survive only as a claim in a commit message. **A rewrite converts a verified history
into an assertion that the history was verified.**

It also deletes the evidence. [`what-broke/`](what-broke/), [`red-team/`](red-team/) and the
[run log](runs/run-log.md) exist because the failures shaped the design. A superseded
document that stays in place, marked superseded and pointing at its successor, shows the
correction happening. A superseded document that has been deleted, or quietly rewritten to
agree with its successor, shows nothing, and the next reader cannot tell a corrected mistake
from one that never happened.

So the tree stays where it is, and canonicity is declared on top of it. Every status is one
comment in one file, reviewable in a diff, reversible in a line, and checked.
