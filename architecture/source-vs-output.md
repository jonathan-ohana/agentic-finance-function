# 15 — Source Data vs. Agent Output: the architectural line

*Decided Mon 17 Aug 2026, mid-build, after a course correction. This is the rule that governs everything from Day 3 onward.*

---

## The mistake, stated plainly

The generator had started producing a profit and loss statement, a balance sheet, an indirect cash flow statement, an ARR schedule, working-capital ratios and rollforwards — and shipping them as part of the company's data.

That is backwards. **Those are agent outputs.** If they arrive pre-computed in the dataset, the Bookkeeper has nothing to close, the Analyst has nothing to calculate, and the Reporter is transcribing rather than assembling. The demo would prove only that an agent can read a CSV.

Jonathan's phrase for it: *j'ai mis la charrue avant les bœufs.*

## The rule

**The generator produces only what a real company's systems would contain. The agents produce everything a finance function would produce from them.**

| Layer | Contains | Who makes it |
|---|---|---|
| `data/` — source systems | General ledger journal, chart of accounts, AR invoices, AP bills, cash receipts and payments, bank transactions, payroll and EOR invoices, headcount roster, customer masters, usage logs, CRM export, FX rates, document index, the two board plans | The generator |
| `answer_key/` — expected outputs | P&L, balance sheet, indirect cash flow, ARR schedule, working-capital ratios, AR and AP aging, deferred revenue and fixed asset rollforwards, metric registry, edge-case manifest | The generator, **for grading only** — never given to an agent |

The answer key exists so the agents can be scored. It is not company data and must never appear in an agent's context.

## What survived the correction, and why

Two things built during the detour were kept, because they are properties of the **source data** rather than derived outputs:

**The settlement engine.** Cash now moves invoice by invoice and bill by bill. Each of the 819 receipts names the invoice it settles; each of the 807 payments names the bill. This is what a real bank feed and cash application look like, so it belongs in `data/`. It also removed the last plug in the dataset — nothing about cash is assumed any more.

**Document-level lineage.** Every one of the 5,832 journal lines carries a source document ID and a counterparty, resolving into a 3,521-row document index. Accruals point at named supporting schedules, which in turn declare their calculation basis. A real ERP has this; ours now does too, and the build fails if any line lacks it.

The three-statement work was *not* wasted either — it moved to the answer key, where it defines precisely what the Analyst and Reporter have to reproduce on Days 7 and 8. Building the answer first, then hiding it, is a legitimate way to specify a test.

## On the three-statement model and cash

The clarification that prompted this: the banker-style working-capital model — deriving cash from DSO, DPO and deferred-revenue days — belongs to the **forecast**, not to history.

- **Historical cash** is settled, not modelled. Every movement traces to a document.
- **Ratios** are computed *from* that settled history. `working_capital_ratios.csv` reports DSO two ways: the balance method (26.7 days at Jul-26) and the settlement method, measured from actual invoice-to-cash days (44.3). The gap between them is itself a finding.
- **Forecast cash** is where the ratios become drivers. That is the Day 7 Forecaster and the 13-week cash view, and it is exactly the technique an investment banker would apply.

Stated as one line for the case study: *historical cash is settled, forecast cash is modelled from settled history.*

## Consequences for the rest of the sprint

- **Day 3** — documents (contracts, order forms, SOWs, invoices as PDFs) are source data. They carry the same document IDs already present in the ledger, so ingestion has something real to reconcile against.
- **Day 5** — the semantic layer is an agent-facing artefact and must be *written*, not generated. The 22-row metric registry in the answer key is a draft specification for Fable #2, six entries of which are deliberately flagged `UNRESOLVED` because they are conventions rather than truths.
- **Days 6–8** — the Bookkeeper produces the trial balance and closes the month; the Analyst produces the P&L, the ARR schedule and the variance; the Reporter assembles the board pack. Each is scored against the answer key.
- **Grading becomes measurable.** "The Analyst reproduced the P&L to within $0.50 on every line, and correctly declined to annualise June's tournament revenue" is a far stronger claim than "the agent produced a plausible-looking report."

## Validation as it stands

51 checks, all passing, in five groups: double-entry integrity, three-statement articulation, subledger tie-outs, lineage, and working capital. Three of them are the ones worth quoting:

- Cash flow articulates — opening plus net change equals closing in all 19 periods, worst variance $0.02
- AP and AR control accounts tie to their open-item subledgers to the cent
- Every journal line carries a source document ID, and every ID resolves in the document index — 0 unsupported out of 5,832

The build is deterministic: `_build_manifest.csv` stamps the seed and a config hash, so any figure can be reproduced exactly.
