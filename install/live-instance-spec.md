# 74 — The live instance: a Co-pilot you can ask anything

*Written 23 Aug 2026. Builds the infrastructure doc 71 (free-form Co-pilot)
specified and doc 21 (the Co-pilot charter) governs. Companion to doc 70
(routing), doc 72 (re-tiering) and doc 73 (routing review). The sealed-month
protocol in §7 is **written and not armed** — deliberately.*

---

## The ruling

**The Co-pilot does not get the files.** It gets a read-only tool surface over
one governed instance, and that surface has no function that returns an
unregistered number.

Everything below follows from that sentence.

---

## 1. Why the tools carry the control, and not the prompt

The obvious build is: point a capable model at the CSVs, write a careful prompt
about only using ruled definitions, and let it be clever. It would work. Most of
the time.

The problem is the rest of the time, and specifically that **the failures are
indistinguishable from the successes at the moment they happen**. A model that
sums three accounts because the ruled metric was awkward produces a number with
a decimal point, in the same tone, from the same real ledger. Nothing errors.
The tie-out suite never sees it, because the number never entered an output. The
person who asked has no way to tell, and neither does anyone they repeat it to.

A prompt asks a model to decline. A tool surface with no function for the wrong
answer does not have to ask.

So the control moved into `mcp_server.py`, and what is left in
`copilot_instructions.md` is only the part a tool genuinely cannot enforce:
tone, framing discipline, what to do with a refusal, and when to stop before a
verdict. That is a much smaller prompt with a much better chance of surviving
its next revision.

**The test of this design is not that it answers well.** It is that a session
which tries to misbehave finds nothing to misbehave with.

---

## 2. What was built

| Artefact | What it is |
|---|---|
| `package/mcp_server.py` | Read-only stdio JSON-RPC MCP server over one instance. 14 tools. No dependencies, no network, no model call. |
| `package/registry.py` | Metric resolution: a phrase in, one of three outcomes out. Also audits and proposes registry wiring. |
| `package/query_log.py` | Append-only JSONL of every question, and the report that turns it into a backlog. |
| `package/copilot_instructions.md` | The standing instructions — the half of the contract a tool cannot enforce. |
| `package/instance.template.json` | One descriptor per company: which governed files the read surface may see. |
| `example/instance.json` | The demonstration instance, wired. |

### The tool surface

| Tool | What it does |
|---|---|
| `frame` | Instance, currency, basis, entity, registry and layer versions, periods present |
| `resolve_phrase` | A form of words → a registered metric, candidates, or nothing |
| `list_metrics` · `get_metric` | The registry, and one entry in full with its governing rulings |
| `get_metric_series` | The value by period, from the sheet the registry names |
| `list_dimensions` · `slice_metric` | Declared splits only |
| `query_ledger` | Postings and sums of postings — explicitly not a metric surface |
| `lineage` | A posting to its document, and back |
| `list_outputs` · `get_output` | The produced sheets |
| `search_semantic_layer` | The rulings. Read-only; there is no writer in the file |
| `open_items` | UNRESOLVED register, schema gaps, not-computable metrics, evidence gaps |
| `log_query` | The only write on the server |

---

## 3. Resolution has three outcomes, and one of them is not "best guess"

This is the load-bearing piece.

```
RESOLVED     exactly one registered metric matches — by ID, ruled name,
             or governed alias
AMBIGUOUS    more than one matches. Hand back the candidates. Do not pick.
UNRESOLVED   nothing matches. Decline, and draft the entry.
```

**An AMBIGUOUS result is a success**, and the demonstration instance proves why
on the most ordinary question anyone asks a finance team:

> **"What's ARR?"** → five registered metrics contain that word. Committed
> recurring (MET-009), including usage run-rate (MET-010), the commercial total
> (MET-011), constant currency (MET-012), and the price basis itself (MET-021).
> SL-08 exists precisely because they differ by more than rounding, and MET-011
> is barred from board material by that ruling.

A helpful model picks one. This one asks. The difference is a board number.

Two further properties, both deliberate:

**A single candidate is still not a resolution.** "Margin" matching only *Gross
margin %* does not mean gross margin was meant — it may mean operating margin
was never registered. It returns `ambiguous` with `single_candidate: true`, and
the instruction is *confirm*, not *answer*.

**The loose rungs never resolve on their own.** Word-overlap produces candidates
for a question. It cannot produce an answer. A metric sharing half its words
with a sentence has not been identified by it.

---

## 4. Aliases are governed, and the package cannot write them

Doc 71 asked for alias lists so free-form phrasing reaches registered metrics.
Building it surfaced the more interesting half of the requirement.

**An alias is a pointer.** It carries no definition, no formula and no version.
It resolves a phrasing and gets out of the way; every answer still cites the
entry at version, and adding an alias can never change a number. That is why
aliases can be proposed mechanically where definitions cannot.

**But almost nothing is safely mechanical.** `--propose` ran over 32 ruled
entries and could write **one** alias. The rungs it rejected are the lesson:

- **Initialisms are not derivable.** Whether anyone says "GRR" out loud is a
  fact about the company, not about the string. And a manufactured initialism
  is worse than an absent one — `CR` is *credit* in most of finance before it
  is *Committed revenue*, `ER` is an exchange rate. An alias that is a common
  abbreviation for something else does not fail to resolve. It resolves
  confidently to the wrong entry, which is the exact failure this module exists
  to prevent, arriving through the module's own front door.
- **Removing a word can change what is named.** "Runway months" without its unit
  is still runway. **"Deferred revenue days" without its unit is a balance-sheet
  line** — a different object entirely, which a person asking for it would
  happily accept as an answer. Nothing mechanical separates those two cases, so
  the proposer lists them and writes neither. Of the three proposed, two were
  ruled in and one was ruled out. By a person, in about four seconds, which is
  the correct cost of that decision.

So: `--propose` produces a **confirm list**, not a registry. The vocabulary a
company actually uses in the corridor is added by the owner, under the same
governance as the entry it points at. That is not a limitation of the tool. It
is the tool declining to decide something that was never its to decide.

---

## 5. What the demonstration instance refuses, and why that is the demo

Wiring the read surface to the existing answer key produced an honest gap, and
it is worth stating rather than closing quietly.

| | |
|---|---|
| Registered metrics | 32 (29 computable, 3 ruled not computable) |
| Wired to an output column | 12 |
| **Not wired** | **17 — the entry does not declare which column holds its value** |
| Declared dimensions | **0 — every slice refuses** |

> **Amended 23 Aug 2026.** The claim below that revenue by customer segment is
> *not in the data* was wrong, and wrong in an instructive way. Segment was in
> the data — it was in the **file names**, encoded by the fact that this company
> exports clubs, players and academy customers as three files. Nothing could
> read it, so it looked absent. `mapping.json` now carries a `constants` block
> that declares what the file layout means (doc 75 §5), and segment is an
> ordinary column. The dimension is declarable; it still has to be *declared*
> and ruled before any slice returns a number.

Asked for one of the 17, the server says: *this entry does not declare which
column of that sheet holds its value; this is a registry gap, and the entry
needs an `output_column` declared by the owner.* It does not go and find a
column that looks similar.

**That refusal is a better demonstration than a fabricated wiring**, because a
plausible column mapping is precisely the error that survives every downstream
check: real number, real file, ruled definition it was never computed from,
nothing malformed anywhere. The gap is on the worklist in §8. It closes by
declaration, in minutes, by the person accountable for the definitions.

Zero declared dimensions means every `slice_metric` call refuses today. Also
correct: no split has been ruled on this instance, and a re-aggregation nobody
ruled is a new metric wearing a registered one's name.

---

## 6. The log is the requirement document nobody writes

A reporting pack is asked for by a calendar. An ad-hoc surface is asked whatever
is on people's minds that week, in their own words — and that stream is the most
direct evidence a finance function can get about what its reporting does not
cover. It arrives free, it decays by Friday, and nobody keeps it.

Three outputs with no other source:

**The reporting backlog.** Questions cluster on their content words, not their
wording, so *"what's ARR"*, *"what is our ARR right now"* and *"can you give me
the ARR please"* are one cluster of three, not three singletons. A question
asked eleven times in six weeks is a standing report that does not exist yet,
and the cluster is its specification, already written by the people who need it.

**The layer's growth list.** Every phrase that did not resolve is either an alias
the registry should carry or a metric nobody has ruled. Neither is visible from
inside the registry.

**The refusal series.** The eval suite proves refusal behaviour survived a
change. Only the log shows what it costs on real traffic, and whether the
surface has drifted into declining things it could answer.

Two design notes that took a second pass to get right:

- **The log does not store the answer text.** An answer is reproducible from its
  metric, version and frame. Storing the prose invites someone to quote the log
  instead of re-running the number, and a quoted answer six weeks old computed
  under a superseded version is exactly what registry versioning exists to
  prevent.
- **The report recomputes the fingerprint rather than reading it back.** The log
  is immutable; the reading of it is not. A stored fingerprint would freeze
  clustering to whatever the filler list was on the day the question was asked,
  so improving the clusterer would leave every historical question grouped the
  old way.

---

## 7. The sealed month — written, not armed

Fable's build order ended with a sealed month: a generated period whose answers
are known to a config nobody reads until after the system has produced its own.
The protocol:

1. A cheaper model generates one period of activity from a config it holds and
   the operator does not read.
2. The config is sealed — same discipline as doc 57 — with the answer key inside.
3. The system closes the period, produces the pack, and answers a fixed question
   set through the Co-pilot.
4. Only then is the config opened and scored.

**It is not armed, and the reason is a sequencing judgement.** A sealed month
tests whether the system finds what was planted. Run against a surface whose
outputs have not themselves been verified, a miss is unattributable: the plant
was missed, or the plant was found and the output was wrong, or the question
never reached the right metric. Every one of those looks the same from outside
the seal, and the seal is the one thing that cannot be re-opened and re-run.

So the order is: **verify the outputs, then arm the seal.** The seal is a
one-shot instrument and firing it early wastes it.

Nothing about the living company is built. No new numbers, no new entities, no
generator config.

---

## 8. The worklist, in order

**Before the Co-pilot is used in anger**

- [ ] Declare `output_column` on the 17 unwired entries. Declaration, not
      computation — the columns exist; nobody has said which is which.
- [ ] Populate aliases from the vocabulary actually used. The audit is the
      worklist; `--propose` cannot do this and says so.
- [ ] Declare dimensions where a split has been ruled, and leave the rest
      refusing.
- [ ] Version the instance's semantic layer in the descriptor. It currently
      states the *template's* version and its own only in the change log — two
      different numbers that must not be confused.

**Before the seal is armed**

- [ ] Verify every agent output against the answer key, which is the condition
      §7 is waiting on.
- [ ] Run `copilot_eval.py` against the live surface and record the control.
- [ ] Fix the instance leakage in §9.

---

## 9. A finding this build turned up, and it is not small

> **Resolved 23 Aug 2026 — see doc 75.** The finding below understated it:
> five engines were affected, not two, and the fix uncovered two wrong numbers
> on the demonstration instance itself. All five are converted, a harness now
> proves the claim by running the package rather than reading it, and it is
> green at 14 of 14. The account below stands as written because the reasoning
> that led to filing it rather than patching it is the reasoning doc 75 acts on.


Grepping `package/` for instance-specific vocabulary — the standing check that
the package ships to any company — found two engines that **only run on the
demonstration company**:

| File | What it does |
|---|---|
| `package/variance.py` | Reads `customers_clubs.csv`, `customers_players.csv`, `customers_academy.csv` **by literal filename, bypassing the mapping**, and hardcodes those three as the segment list |
| `package/kpi.py` | Reads `customers_players.csv` the same way |

Every other engine goes through `mapping.json`. These two do not, so on any
other company they find no files and produce nothing — silently, since a missing
optional file is a legitimate state everywhere else in the package.

The fix is a design change, not a rename: **segments must come from the mapping**,
as a declared block naming each segment's customer table and its unit-price key.
It is filed rather than patched here because it changes a contract, and a
contract change gets its own ruling.

Three further hits are cosmetic and were left: a "courts" in a synonym list of
unit names, and two illustrative mentions in comments.

---

## 10. The line this earns

> *"The Co-pilot takes free-form questions and has no function that returns an
> unregistered number. Ask it for ARR and it names the five registered
> readings and asks which — because on that instance they differ by more than
> rounding and one of them is barred from board material. Ask it for something
> nobody ruled and it drafts the registry entry instead of computing it. Every
> question it is asked gets logged, and the questions it refused are the half
> that tells you what your reporting is missing."*
