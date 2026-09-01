# 69 — The output contract: what a finance function is supposed to produce

*Built 21 Aug 2026. `package/output_contract.json`, `package/output_map.py`, `package/WHAT-IT-PRODUCES.md`.*

---

## The gap

The package has had a data contract since the first week. `data_contract.json` describes **29 input roles and 138 data points** — what a finance function needs from a company before anything can run. It is the file the installer matches against, the file the mapping table is generated from, the file the pre-flight scores. It is good, and it is half a contract.

**Nothing described the other end.** Every engine knew what it produced. No artefact said what the *system* produced. Which means the most obvious question anyone asks — a CEO deciding whether to hire, a buyer deciding whether to install, an auditor deciding where to start — had no answer short of reading five programs:

> *What do I actually get?*

The prompt that surfaced it was exact: *"We have a list of required documents with required inputs. We need now a list of required calculated sheets with the required output."*

---

## What it is

**22 calculated sheets, in five families.**

| | |
|---|---|
| **The statements** | P&L, balance sheet, indirect cash flow, and the articulation check that makes the three one model |
| **Reconciliations** | cash against the bank, AR and AP ageing and rollforwards, deferred revenue, payroll against the provider |
| **Schedules** | fixed assets and depreciation, accruals and prepaids, debt, leases and equity |
| **Analysis** | variance with its rate/volume/mix bridge, the 13-week cash forecast, the operating forecast and runway, the metric pack, the recurring-revenue schedule, the headcount bridge, working capital and unit economics |
| **Governance** | the close checklist with its evidence, the audit and PBC pack, the board reporting pack |

Every sheet carries five fields, and the fifth is the one that took the longest.

| | |
|---|---|
| **requires** | the input roles without which the sheet cannot be produced at all |
| **uses** | the roles that make it complete; absent them it is produced with the gap stated on its own face |
| **outputs** | the lines it must contain — a checklist, not a description |
| **ties to** | the sheets it must agree with, **with the residual reported in currency rather than a tick** |
| **refuses when** | the single condition under which it declines to produce a number |

---

## Why the refusal field is the point

A sheet that always produces something cannot be trusted, because there is no way to tell *this reconciles* from *this was rendered*.

- The **cash flow statement** refuses when the articulation check is non-zero. A cash flow that does not tie is not a draft, it is a defect.
- The **balance sheet** refuses when the trial balance does not balance. Presenting an out-of-balance ledger is a formatting exercise.
- The **P&L** refuses when a ledger account is absent from the chart of accounts — the subtotals below it would be *wrong*, not merely incomplete.
- **Variance** refuses when more than one plan version could be meant and the semantic layer names none. Choosing the closer of two budgets is the definition of a lever.
- The **accrual scan** refuses an estimate whose observed spread exceeds half the median, and reports it unusable rather than as a number.
- The **13-week cash grid** refuses to produce months-to-zero. That number belongs to one instrument and appears once in the system.
- Three sheets **never refuse** — the articulation check, the close checklist and the audit pack — because reporting what could not be done *is* their output.

Writing 22 of these is the exercise that proves the contract is real rather than a table of contents.

Nothing in the contract carries a verdict field, on either side. A sheet reports what is; whether that is good news is a judgement, and judgement stays with a person.

---

## The three views

`output_map.py` renders the same JSON three ways.

**The sheets**, as cards, grouped by family: requires, uses, outputs, ties, refusal, degradation.

**The map** — 29 input roles down, 22 sheets across, filled marks for required and hollow for used. The whole system on one grid. It shows at a glance that **the general ledger feeds 21 of the 22 sheets and the document index feeds 2**, which is a truer picture of where the leverage sits than any prose could give. Every input role feeds at least one sheet; a role that fed nothing would be a question asked at install for no reason, and the grid makes that impossible to hide.

**What a gap costs** — one row per input role, priced in the sheets it blocks and the sheets it degrades.

> *"We don't have a fixed-asset register"* is an easy sentence at install and an expensive discovery at audit. On that page it costs a named schedule, a supported balance-sheet line, and the capital expenditure line of the cash flow statement.

This is the page that changes an install conversation, because it converts a chase for a file into a priced decision. Pass `--mapping` and every sheet also carries whether it can be produced today: on the demonstration instance, **20 of 22, with the two exceptions named.**

---

## Why this is the commercially interesting half

Every vendor in this category publishes what data it needs. The prerequisite list is table stakes and it is doing sales work: *clean data, consistent coding, permissions, a validation process* — months of effort acknowledged in a sentence and stepped over.

**Nobody publishes what they produce, at the line level, with the refusal conditions attached.** The reason is obvious once stated: a checklist of required outputs is a list you can be held to. A refusal condition is a promise that the other months meant something. Both are commitments, and a demo is easier without commitments.

That asymmetry is the same one this package has been exploiting from the start. The market has converged on the work layer — do the task, faster. The judgement layer is untouched: what a number is allowed to mean, what must not be produced, when a machine may stop asking. **The output contract is that layer written down for the artefacts rather than for the metrics**, and it composes with the semantic layer exactly: the semantic layer rules what a metric means, the output contract rules which sheet it may appear on and what happens when it cannot be computed.

---

## What is not done

**The contract is documentation, not yet machinery.** The engines produce these sheets; they do not yet *read* `output_contract.json` to decide what to produce, to emit their refusal reasons from it, or to fail a build when a required output line is missing. The mapping table crossed that line months ago by being generated from `data_contract.json` — the same move is available here and has not been made. Until it is, the contract and the engines can drift, and only one of them is running.

**The tie residuals are specified and not yet computed centrally.** Each sheet knows what it must agree with; nothing yet walks the graph, computes all of them and publishes one page of residuals in currency. That page is small, and it is the single most persuasive artefact left unbuilt in this package.

---

*Recorded 21 Aug. Friction log FL-77.*
