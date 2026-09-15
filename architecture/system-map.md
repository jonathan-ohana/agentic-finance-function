# The system map: the compiled state, end to end

*Written 15 Sep 2026. Beyond the evidence base published here, a second build exists: an
installable, company-neutral package developed against a simulated company's messy exports. It
reached the state [the workflow lifecycle](lifecycle.md) calls Compile. This page is its anatomy,
read top to bottom as the data flows. The engine code is not published. Every figure below is a
measurement taken from that build.*

---

## The rule that shapes everything

**Engines compute. Agents judge. No engine output contains a verdict field**, so an agent can
never inherit a judgment it did not reach itself.

Two words, used precisely from here down:

- **Deterministic engine** — Python. Testable. No opinions.
- **Agent** — a written charter with an explicit list of prohibitions.

---

## Layer 0 — What the company actually has

Twenty-four files, exported the way real companies export them: ledger CSVs one per quarter, a
CRM dump, `Copy of Book1`, `FY26 Budget v7 FINAL (2)`, a Slack export, a mailbox, and a folder of
signed PDFs. Underneath them, 709 source documents, 6,036 journal lines, 19 months of history.

Two programs stand between that pile and any promise.

**`installer.py`** profiles every file, infers which contract table it is, and proposes the
mapping. The proposal lands in `mapping.json`, one file per company.

**`preflight.py`** is the honest gate, run before anything is promised. It asks one question —
can this company's data support an agentic finance function at all — reads only, writes nothing,
and sorts what it finds into four kinds of gap: **mapping, export, system, process**. The last
two are not IT problems. Separating them is what stops the answer being "we need a better
export" when the answer is that nobody owns the approval.

## Layer 1 — The rulebook, written before any agent runs

This is the part usually missing in the market: the rulebook exists before the first engine runs,
not as a reconstruction afterwards. Four artifacts.

| Artifact | What is in it |
|---|---|
| **Semantic layer** | 24 rulings over 18 metrics, 3 still open — which of three competing numbers may be called ARR, and who may change a definition. Unresolved stays marked unresolved. |
| **Close checklist** | 37 steps, 21 compressible, 16 not, each with an owner and a blocking status |
| **Finance calendar** | 15 obligations and 4 standing reviews across five jurisdictions, with the holidays that move them |
| **Data contract** | The 15 tables every engine reads |

Company vocabulary lives in `mapping.json`, never in code. The package is company-neutral by
test, not by intention.

## Layer 2 — Engines: deterministic and deliberately opinion-free

9,034 lines of Python. Each engine refuses something, and the refusal is the design rather than a
limitation of it.

| Engine | What it does | What it refuses |
|---|---|---|
| `close.py` | runs and reconciles month-end | the plug |
| `variance.py` | bridges plan to actual; decomposes cost into rate versus volume | the distributed residual |
| `forecast.py` | 15 drivers over 3-, 6- and 12-month windows, with the disagreement between them reported | a growth rate on a total |
| `cash.py` | 13 weeks direct — receipts and payments, never operating income | a plugged opening balance |
| `reporting_pack.py` | builds the 20-tab workbook as formulas, never values — 5,973 of them | a sentence that outlives its number |
| `kpi.py` | computes the registry's metrics | a zero standing in for something unmeasurable |
| `evidence.py`, `calendar.py` | observability, document lineage, what is due when | — |
| `scorekeeper.py` | scores the finance function on itself | — |

Three of those need a sentence each. In `reporting_pack.py` the prose is `TEXT()` off live cells,
so a sentence cannot outlive the number it quotes; 176 check cells, every one of them reading
zero. In `kpi.py` an unmeasurable metric is null with a reason attached, never zero — a zero is a
measurement and a null is a refusal, and a reader cannot tell them apart after the fact.
`scorekeeper.py` asks whether every correction was routed to a rule that actually exists: loop
closure, 33 of 34.

### The line no engine crosses

An engine can say that a tie check is $0.00 and that twelve of sixteen close steps produced no
evidence. It cannot say the close is fine. That word has to be typed by something that can be
held to it.

## Layer 3 — Agents: a charter each, a prohibition list, an earned autonomy level

The spine, in the order the work moves:

| Agent | Says | Where it stops |
|---|---|---|
| **Bookkeeper** | what happened | refuses to sign a close it cannot evidence. L1, 10 escalations, no sign-off |
| **Analyst** | why | attributes variance to the drivers the plan was built from and no further. L1; the comparator question came back BLOCKED |
| **Forecaster** | what follows | names the estimation window on every figure. L0 permanently — 4 drivers cannot carry a forecast |
| **Controller** | when the money moves | L0 on figures; 7 of the 13 weeks called right |
| **Reporter** | carries it to the board | prints NOT PRODUCED rather than an estimate. L0; 6 cells say what is missing |

And the support roles:

- **Ingestion** reads the signed documents and reports where they contradict the ledger without
  bending either: 239 of 239 contracts read, 12 contradicted.
- **Advisor** and **Chief of Staff** say what to do about it and when it is due. Neither may
  judge quality.
- **Drift Auditor** audits the others. It withdrew its own first audit when six of its
  corrections turned out to point at artifacts that did not exist. Call that what it is: the
  demonstration that the auditing is not theatre.

## Layer 4 — What comes out

- **Close pack** — what is done, what is not, and what blocks the signature.
- **Variance pack** — bridges whose unexplained residual is computed, never chosen.
- **Forecast pack** — the back-test printed above the forecast rather than beneath it, and the
  sentence saying the weeks are not forecasts.
- **Cash pack** — the 13 weeks, receipts and payments.

Every figure traces back to a document.

---

## How this relates to the lifecycle

[The workflow lifecycle](lifecycle.md) sets out three phases. This build is the Compile phase
realized: the rulebook written down first, the mechanics in deterministic code, the model kept
only at the nodes where judgment is required. The public repository you are reading documents the
Operate phase and the doctrine that governs both. The promotion gates between them — what a
workflow must show before it earns compilation, and what sends it back to Explore — are on that
page, not this one.

## The honest limits

One simulated company. The engine code is not published, so this page describes an artifact
rather than being one; nothing here can be run by a reader. The figures are the build's own
measurements, self-graded — 33 of 34 is a number the system gave itself, and no independent party
has recomputed it. No real company's exports have been through the installer.
