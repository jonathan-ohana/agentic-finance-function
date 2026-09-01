# 76 — Slicing: why "by segment" is a ruling, not a group-by

*Written 23 Aug 2026, overnight. Builds stage 1 of the modify-navigate-slice
surface. Companion to doc 74 (the live instance) and doc 75 (portability),
which made this possible by turning a fact hidden in file names into a column.*

---

## The ruling

**A metric may be split only by a dimension the instance has declared, and
every split states its own reconciliation.** Members, the metric's published
total, and the difference — computed each time, never asserted. Unlabelled rows
appear as a named member. Everything else refuses.

---

## 1. Three ways a group-by is wrong, and all of them are quiet

Asked for revenue by product line, the obvious implementation groups the ledger
and sums. It returns columns that look right and add up.

**The parts do not equal the whole.** 3.3% of this instance's operating expense
postings carry no cost centre. Group and sum and they vanish. The columns look
complete and total to slightly less than the metric, and the reader comparing
the chart to the P&L finds a difference nobody mentioned.

**The metric is not additive.** You cannot sum 66% and 71% into a gross margin.
A ratio needs both sides sliced and divided per member, and if either side
cannot be sliced the answer is not a smaller number — it is no number.

**The split was never ruled.** A column existing in the data is not a dimension
being declared. Revenue by region computed off whatever region field happens to
be populated is a new metric wearing a registered one's name, and it will
disagree with the one somebody rules next quarter.

## 2. What a declaration carries

`dimensions.csv`, one row per metric per dimension. Beyond the obvious — which
table, which column, which population — three fields do the work:

| | |
|---|---|
| `unlabelled` | the member name blanks appear under, or the word `refuse`. Never dropped. |
| `kind` / `ratio_of` | `additive`, or a ratio naming its two sides |
| `sign` | `credit` is presented positive, as the statement does. Declared rather than inferred from the account range, because inferring it means this module knows a chart of accounts. |

And one that matters more than the rest.

## 3. `min_fill`, which is the part I would keep

A dimension declared when its field was 98% populated, drifting to 71% because
somebody stopped filling it in, **does not fail**. It produces the same chart
with a fatter "Unattributed" bar. Same shape, same total, one column a little
bigger. Nobody looks at a chart to check whether its denominator is still being
collected.

Below the declared floor the slice refuses, and says what the fill rate is now
and what it was declared at.

This is the same idea `kpi_definitions.json` already carries about checks: a
check that stopped running and a check that passes produce identical silence, so
the only defence is to measure whether it ran. A dimension is a check on a
population, and it rots the same way.

## 4. What the demonstration instance declares, and what it refuses

**One dimension.** `DIM-01 Product line` on `MET-001 Total revenue`, from
`gl_journal.account_name` over accounts 4xxx, floor 99%, ruled under SL-29.

```
  Total revenue  by  Product line  ·  2026-07
  MET-001@1.0  ·  DIM-01 SL-29  ·  from gl_journal.account_name

    Subscription revenue — Player      182,024.36
    Subscription revenue — Courts      160,757.76
    Usage revenue — match overage       49,590.97
    Subscription revenue — Academy      41,257.16
    Credit pack revenue                 21,189.90
    Refunds, credits & chargebacks      -2,291.49

    parts         452,528.66
    published     452,528.66   (MET-001@1.0)
    difference          0.00   ties
```

Everything else refuses, and the four refusals are the deliverable:

- **An undeclared dimension** returns the declared list and a suggestion to ask.
- **A metric with no declarations at all** says so, and offers the total.
- **A ratio with an unsliceable side** — `MET-003 Gross margin %` by product
  line — refuses, because slicing one side of a ratio and not the other yields a
  value per member and a meaning for none of them. Cost of revenue is not
  attributable to product line in this ledger; that is a real limit, not a bug.
- **A fill-rate breach** — cost centre is 96.3% populated on opex, so a
  declaration at 99% refuses and names both numbers.

## 5. `--propose` measures; it does not declare

It reports every column that is populated often enough and takes few enough
values to be a split, with its fill rate, its cardinality and a sample. It
writes nothing.

On this instance it surfaces fifteen candidates — cost centre, account name,
account type, source system, country, currency, and segment. All are usable.
None is declared, because a dimension says *this company stands behind this
split, on this population, down to this fill rate*, and no tool can say that.

Same discipline as the alias proposer in doc 74 §4, for the same reason: the
machine can measure the data and cannot know the vocabulary or the commitment.

## 6. What doc 75 unlocked

Doc 74 §5 reported that revenue by customer segment was *not computable* here
because segment was not in the data.

It was in the data. It was in the **file names** — this company exports clubs,
players and academy customers as three files — and nothing could read it, so it
looked absent. The `constants` block added in doc 75 declares what the layout
means, and segment is now an ordinary column at 100% fill across 20,250
customers.

It is a candidate, not a declaration. Splitting *revenue* by it still needs a
join from postings to customers that this ledger does not carry on every row —
half the revenue postings are batched self-serve billing runs with no
counterparty. So the honest position is: the dimension exists, the metric it
would most usefully split cannot reach it yet, and that is a schema-change entry
rather than a number.

## 7. Not built, deliberately

**Saved views.** A view somebody saves and returns to is a report, and it
belongs next to the `answer_and_offer_pin` loop and the query log's repeat
clusters — the same feature from two ends — rather than bolted onto the slicer.
That is stage 1b.

## 8. The line this earns

> *"Ask it for revenue by product line and you get the six lines, the total from
> the P&L, and the difference between them — computed, not claimed. Ask for it by
> region and it tells you region was never ruled here and offers to draft the
> declaration. And if the field a declared split depends on quietly stops being
> filled in, it refuses instead of growing a bigger 'unattributed' bar, because
> that bar is what a broken dimension looks like when nothing is watching."*
