# Analyst runbook

**Version 2** · Every precomputed input, and the question it exists to answer.

This file is the authority on what to read. If a file is in your inputs and is not listed
here, say so in your report - either it should be listed, or it should not have been handed
to you. If a question here has no file behind it, that is a gap and it is worth naming.

---

## The precomputed inputs

Read every one of these before touching the raw ledger. Each is arithmetic somebody has
already done, and skipping one is how a finding gets missed while sitting in plain sight.

| File | The question it answers |
|---|---|
| `contract_exceptions_<period>.csv` | **Does what we signed match what we booked?** Amendments never billed, notice windows that closed, ramps not stepped, vendors with no agreement, commission earned against accrued, tax charged where it is due. |
| `arr_movement_gross.csv` | **Is net growth concealing gross churn?** Read the components, never the net. A month can grow and still have lost its two largest logos. Check the `churn` and `contraction` columns and their counts, not just `net`. |
| `cutoff_exceptions_<period>.csv` | **Does anything belong to a period that is already closed?** The period the service falls in governs, not the period the paper arrived. |
| `variance_signals_<period>.csv` | **What did the controls catch?** RANKED - see below. |
| `variance_<period>.csv` | **Where did the money differ from plan?** Every account by vendor. |
| `variance_decomposition_<period>.csv` | **Was it volume or was it rate?** |
| `variance_trend_<period>.csv` | **Is this a trend or a calendar?** Coefficient of variation per account. |

## How to read the signals file

It is ranked, and the ranks are not decoration.

- **`Control exception - High`** - the entry moves an accrual the accrual schedule does not
  carry, or the same person prepared and approved it, or it is dated outside the period.
  Read every one. Do not skim past a High because there are Mediums around it.
- **`Control exception - Medium`** - worth a look.
- **`Control exception - Housekeeping`** - a routine system entry missing an attachment.
  Normally noise.

The flat version of this check produced fifteen identical-looking flags in one period, of
which fourteen were routine. An analyst correctly saw noise and triaged away the one that
mattered - a hand-typed entry cutting an accrual by sixty percent with nothing behind it.
The ranking exists because of that.

## The two standing rules

**A signal is cleared by naming the entry that clears it.** "Already handled in the close"
without a document reference is an assumption, not a clearance. If you clear something,
write down what cleared it.

**Quantify everything in USD.** An unquantified finding scores as a partial at best. State
resemblance, not conclusion, where the data supports two readings - and give both readings.

## What is out of scope

Anything below the materiality floor in `04-month-end-close/materiality.csv`. Closed and
signed periods, unless something in an open period belongs to one. Fixing anything: you
propose, a human resolves.
