# 75 — Portability: the check that was checking the wrong layer

*Written 23 Aug 2026, overnight. Executes the ruling filed in doc 74 §9.
Companion to doc 28 (the close-coverage audit) and doc 39 (loop verification).
Supersedes the grep.*

---

## The ruling

**The package's install claim is now proved by running it, not by reading it.**
`tools/portability_harness.py` runs every engine twice — once on the example
instance, once on the same data under opaque names with the mapping rewritten
to match — and diffs. Identical output means the engine read the mapping.

Result: **14 of 14.** It started at 3.

---

## 1. What was wrong with the old check

The claim is that the package installs at any company: you map your exports
into the data contract, and every engine reads through the mapping. It was
checked, from the first build, with a grep for the demonstration company's
name across `package/`.

That grep passed every single time it was run. It was checking the wrong layer.

`variance.py` does not contain the word "CourtIQ". It contains
`customers_clubs.csv` — the company's **file names**, read directly, bypassing
the mapping. Same dependency, wearing a costume a text search cannot see.

I found those by accident, during unrelated work. Nothing existed that would
have found them on purpose. That is the actual finding: not the five engines,
but that the only portability check in the project could not have caught any
of them.

## 2. The method: the same company under different names

A second company would prove portability and would also cost a second company —
which is exactly the work deferred until the outputs are verified.

It is not needed. **As far as the code is concerned, the same data under
different file names is a different company.** The numbers are identical, so
any output that changes was produced by something that read a name.

```
1. Copy every file to an opaque name.   customers_clubs.csv → ztbl0009.csv
2. Rewrite mapping.json to point at the opaque names. Nothing else changes.
3. Run every engine against both instances.
4. Map the names back, and diff.
```

Three kinds of finding, and the third is the one the harness is for:

| | |
|---|---|
| **CRASHED** | It went looking for a name and did not find it. The loud failure, and the lucky one. |
| **DIFFERS** | Different output from identical data. |
| **DEGRADED** | **Less** output, exit 0, no complaint. |

DEGRADED is the shape a hardcoded path actually takes here, and the reason is a
*good* rule: a missing optional input is a legitimate state everywhere in this
package, so an engine that hardcodes a path does not error at another company.
It produces nothing. The install looks successful. The only person who would
notice the absent output is the one who does not yet know it was supposed to
exist.

## 3. What it found

| Engine | Verdict | What it held |
|---|---|---|
| `variance.py` | DEGRADED, 68 fewer lines | Three customer files and the metric registry, by name; a `fallback_file` parameter on its own loader |
| `kpi.py` | DEGRADED, 8 fewer lines | Six file names |
| `cash.py` | DIFFERS, opening cash 0 | Six tables through a **second** mapping mechanism — `ar_file`, `bank_file` — beside the first |
| `forecast.py` | CRASHED, then DIFFERS | A hardcoded ledger, and plan discovery by filename prefix |
| `reporting_pack.py` | CRASHED | Ledger and chart of accounts by name; plan discovery by filename prefix |

Five, not the two I knew about.

**None of these authors was careless.** Each had a local reason and there was no
single function to reach for, so each engine grew its own loader and each loader
grew an escape hatch. A rule enforced by convention is enforced by whoever is in
a hurry. One loader with no escape hatch is a smaller ask than five authors'
discipline, which is why `instance_io.py` exists and why it will never take a
fallback filename.

## 4. Two wrong numbers, on the instance that was not scrambled

The harness was built to find portability bugs. It found two errors in the
**control** output — numbers that have been wrong on the demonstration company
this whole time.

Both come from the same idiom, which appears three times: *discover the plan by
walking the data directory for files whose name begins with `plan_`.*

The directory holds six such files. Two are plans. The other four are the
cost-centre split, the COGS detail, the line detail and the driver file — all of
which carry a `plan_version` and a `period` column, so every one of them was
swept in and treated as a plan version.

**The forecast's plan-headcount scenario reported 149 months of runway. It is
20.4.**

Planned headcount was built into one dictionary keyed on version and period, so
the last file to mention a period won. Sorted alphabetically, that was the
driver detail — 456 rows, one per driver per period — and the headcount the
forecast planned against was whichever row happened to sort last. Salary cost
came out near zero, cash lasted twelve years, and nothing ever disagreed.

Two more from the same cause:

- The board pack cover printed the plan comparator as **"FY26 Board Plan ()"** —
  blank vintage — because it took the version from the cost-centre split, which
  has no `plan_date`. Now **2026-01-15**.
- `plan_reconciliation.csv` held **150 rows across three phantom versions**, one
  of them "FY26 Board Plan" appearing twice with different dates. Now **50 rows
  across the two real ones**.

And one crash that had nothing to do with portability: the pack indexed
`[1]` into its list of plan comparators. **A company with one live plan version
— which is most companies — would have crashed the entire board pack.**

## 5. Two things the harness now declares, and one it will not

`constants` — a per-file literal stamped onto every row:

```json
"customers": {"files": [
  {"file": "clubs.csv",   "constants": {"segment": "Clubs"}},
  {"file": "players.csv", "constants": {"segment": "Players"}}]}
```

This exists because **a fact can live in the file layout rather than in a
field.** A company exporting three customer files has recorded which segment
each customer is in — in the name of the file. No engine reading a unioned
customer table can see it, so two engines recovered it the only way left: by
reading the three names. That worked, and it is precisely why they only ran here.

`constants` turns the inference into a declaration. The segment becomes an
ordinary column the semantic layer can rule on, and the knowledge moves from the
code to the instance. That is the whole architecture in one field.

It also quietly settles something from doc 74 §5, where I reported that revenue
by customer segment was *not computable* on this instance because segment was
not in the data. It was in the data. It was in the file names, and nothing could
read it. It is now a declared column.

`artefacts` — non-contract inputs (a metric registry, a published summary),
declared rather than assumed.

What the harness will **not** do is scramble the package's own outputs. A
mapping value that is a directory points at artefacts this package produced, and
an engine reading `scenario_summary.csv` out of one is reading its own contract.
The directory gets renamed; the files inside keep their names.

## 6. Three false positives I built, and what each cost

Worth recording, because a harness with a standing false positive is a harness
nobody reads — which defeats it more completely than missing a bug.

1. **Scrambled names appearing inside hashes.** Directories were named `d01`,
   `d02` — and `d02` occurs inside SHA-256 digests. The reverse-mapping step
   rewrote it, and two identical workbooks were reported as different. Every
   generated name now starts with `z`, which is not a hexadecimal digit.

2. **The word "data" rewritten inside prose.** The mapping was rewritten by
   blind text replacement. The data directory is called `data`, so every
   occurrence of that word in the mapping's comments was rewritten — and one of
   those comments is quoted onto a worksheet. A board pack driver note read *"the
   consequence of believing the zdir19"*. The harness had corrupted the instance
   and then reported the engine for it. It now walks the parsed JSON and rewrites
   only path-shaped values, segment by segment.

3. **Mapping-declared filenames treated as engine-held ones.** An engine reading
   a name the *instance* declared is behaving correctly — a different company
   writes a different mapping. Only a name the *engine* holds is a bug. The
   harness had to learn the difference before its findings meant anything.

## 7. What the harness cannot see

Stated plainly, because a check whose limits are not written down gets trusted
past them.

**It compares scrambled against control, so a fault present in both is
invisible.** While converting the engines I overwrote the `customers` column
renames in `mapping.json` and broke the contract's `customer_id` and `name`.
The harness reported PASS — both sides were equally broken. Only the
before-and-after snapshot against the original outputs caught it.

So the harness answers exactly one question: **if I point it at my exports, does
it find them.** It does not answer whether a hardcoded account code, currency,
or segment name is still in there. That is a different check and it does not
exist yet.

## 7a. The third layer, found later: the company's *vocabulary*

*Added 23 Aug, after §7 said this check did not exist.*

§7 ends by naming what the harness does not answer — whether a hardcoded
account code, currency or **segment name** is still in there. Running the old
name-grep over `package/` while committing something unrelated, it was.

Not in a way the harness could ever see, because it does not change behaviour
under scrambling. It was in `installer.py`'s synonym table: the list of column
names the installer recognises carried `club_id`, `player_id`, `coach_id`,
`coach_ref` and `club_name`. Also `courts` as the example unit in the data
contract, `club_by_id` as a variable in `variance.py`, and the demo company's
three customer exports as the worked example in `instance_io.py`'s docstring.

**The installer's demo ran well partly because the installer had been taught
this company's words.** That is the most flattering possible bug: it does not
fail, it makes the product look better than it is, on exactly the file the
prospect is watching. Strip the five aliases and the installer stops
recognising three of the customer files and drops a table.

The fix is the split `evidence.py` had already made and nothing else had
copied. There, the counterparty stopwords are in two lists: legal-form
suffixes and articles in the package, because every company has those, and the
industry nouns in the install's own file, because no two companies share them.
`installer.py` now does the same — `--column-hints`, a JSON of
`{contract_field: [extra aliases]}` that extends and cannot replace — and the
padel nouns live in `example/column_hints.json`, where they belong. Hinted,
the proposal is one column *better* than before.

So the three layers, and what catches each:

| | |
|---|---|
| **Name** — the company appears in a string | grep. Cheap, and it was never wrong, only insufficient |
| **Behaviour** — an engine holds a filename | the harness. Scramble and diff |
| **Vocabulary** — the package has been taught this industry's words | grep again, over a wider word list, *and* the judgement to ask whether a demo runs well because the package is good or because it has been coached |

The third has no automation and probably cannot have one: `courts` is a
padel word, `seats` is not, and only a person knows that `member_id` is
generic where `player_id` is not.

## 8. What was done

| | |
|---|---|
| `tools/portability_harness.py` | New. 14 engines, two instances, one verdict each |
| `package/instance_io.py` | New. The only loader. No fallback parameter |
| `variance.py` `kpi.py` `cash.py` `forecast.py` `reporting_pack.py` | Converted |
| `example/mapping.json` | `constants` on customers, `artefacts` block, `unit_segments`, `movement_reconciliation` keys |
| `package/installer.py` | `--column-hints`; five padel aliases out of the base list (§7a) |
| `example/column_hints.json` | New. This company's own words for things |
| git | **Initialised.** The project had no version control at all — no history, no diff, no way back from a bad edit. That is now two commits deep |

Every output is byte-identical before and after, except the two corrections in
§4 and the workbook's own save timestamp.

## 9. The line this earns

> *"Our install claim used to be checked with a grep for the company's name. It
> passed every time, and it was checking the wrong layer — five engines held the
> company's file names, which a text search cannot see. So now the check runs the
> package twice, once on the same data under opaque names, and diffs. It found
> the five. It also found that our forecast had been reporting a hundred and
> forty-nine months of runway on a scenario where the real answer is twenty,
> because planned headcount was being read out of a driver detail file that
> happened to sort last."*
