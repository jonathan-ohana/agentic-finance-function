# 77 — Entry triage and reforecast: the two loops that close on each other

*Written 24 Aug 2026. Builds the sixth workflow from the AI-native ledger playbook —
spend anomaly detection — as the thing it actually is, which is variance
analysis one level below the line. Companion to doc 33 (the analyst and the
variance engine) and doc 36 (the two loops).*

---

## The ruling

**A variance is explained at the level of an entry, decided by a person, and
only then allowed to reach a forecast.** Three artefacts, deliberately not
joined into one: an engine that finds, a file that records the decision, and
an engine that computes what the decision costs. Nothing crosses from one to
the next without a name and a date against it.

---

## 1. Why variance.py was not enough, and it was not a defect in it

`variance.py` works at the level of a LINE. It reports that professional
services ran over plan and decomposes the movement as far as the plan's own
grain allows. That is the right unit for a board pack and the wrong unit for
doing anything, because **a line is an aggregate and you cannot reclassify an
aggregate.**

Somebody still has to open the account and read the entries to find that the
overrun is one bill from a firm that has always posted to legal, coded to
audit by a new starter, in a month where the audit was already accrued. That
reading is the work. Everything above it is the summary of the work.

`entry_triage.py` does the reading. Two questions of every expense posting
above a declared floor:

| | |
|---|---|
| **Is it in the right place?** | account against the counterparty's own habit · cost centre present, and one the account has used · the period against the entry's date · the same amount twice |
| **Was it expected?** | against the plan at the grain the plan has · against the pair's own twelve months · against a month in the run with nothing in it |

## 2. What it found on the demonstration company

**A duplicate invoice, booked and paid, sitting in the books since March.**

```
  ET-2026-03-001   same_amount_twice   6020   41,445.55
    2 postings of 41,445.55 to account 6020 in 2026-03,
    of which 1 has been settled in cash.

    JE-001118  2026-03-31  (no counterparty)  SCH-OPEX-202603
               "Operating expenses (accrual)"
    JE-001119  2026-03-24  Helix Research Cloud  BILL-00612
               "ML research compute — vendor resubmission"   memo: duplicate

    settled: BILL-00612 by PAY-01442, 2026-04-21
```

ML research compute runs at about USD 41,000 a month all year. March is
82,891. Nothing in the package caught it before — not the close engine, not
the flux (one month at double is USD 41k against a 25k threshold, so it
*would* have shown, and the account is small enough that nobody looked), not
the tie-outs, which tie because the duplicate is genuinely in the ledger on
both sides.

The correction shape it states is the one that matters:

> *One of these has already been paid, so a reversal of the accrual does not
> recover the cash — that is a credit note or a refund, which is a
> conversation with the supplier and not a journal entry.*

## 3. The three false starts, because they are the content

**The engine's first run examined six postings out of 450 and reported that
payroll had not been paid in July.** One line caused both: a set of
expense-type names written from memory — `Expense`, `Cost of revenue`. This
company's chart says `Opex` and `COGS`, so almost nothing matched, almost
nothing entered the expected population, and every regular vendor came out
the far side as ABSENT.

It is the fault doc 75 found in the installer, in a new place: **the package
had been taught one company's vocabulary.** Wrong in the alarming direction
here; the same bug against a chart that spells it `Expenses` is wrong in the
silent one.

**So it was made to measure instead — and it put trade receivables in the
expense population**, because receivables build and collect and their
cumulative line comes back down the way a flow account's does. That is
`dimensions.py`'s lesson arriving again: a machine can measure the data and
cannot know the vocabulary.

The engine now **refuses**, names the account types it can see with the
evidence for each, and states the one line of mapping that unlocks it. The
refusal is the deliverable, as it is for the slicer.

**And the duplicate test found twelve false positives before it found
anything true.** Comparing a two-month window, July produced twelve pairs
that were payroll, share-based pay, rent and insurance costing the same in
June as in July — which is what those things do. A guard was tried (skip an
amount seen in three or more prior months) and does not work, because payroll
at the same figure in June, July and August has only one *prior* month inside
the window and clears the guard every time.

Twelve false positives against one real finding is not a tuning problem. It
is a test that gets ignored by the second month and therefore protects
nothing. It now looks inside one period only, where a standing charge posts
once and a resubmission posts twice — and says, in the source, what that
gives up: a duplicate split across two months needs the document, not the
amount, and that is a test on the AP subledger.

## 4. The file in the middle, and why the engines do not speak

The obvious build joins them: the triage says a bill arrived early, the
reforecast moves the money. One command, no file.

That build is wrong in a way that is invisible until an auditor asks.
**Between "this bill is bigger than its own history" and "the forecast should
move" sits a judgement no amount of ledger data contains** — price rise,
catch-up, duplicate, or a genuinely new commitment. Wire the engines together
and that judgement still gets made. It just gets made by whoever wrote the
joining code, once, for every future month, invisibly.

So they share `entry_dispositions.csv`, and it has six values, about **what
the thing is** rather than what to do about it:

`correctly_placed` · `reclassify` · `timing` · `accrue` · `new_commitment` ·
`one_off`

Only two reach the forecast. That is the point: most findings are not
forecast events, and a system that treats them all as forecast events
reforecasts on noise. The March duplicate is a `reclassify` and correctly
changes no forecast at all.

## 5. The part I would keep: timing into a closed month is not timing

> *"It's just timing"* is the most comfortable sentence in finance, because
> it means the year is fine.

It is true when the cost has moved from one OPEN month to another. Take it
out of September, put it in July, the year is unchanged and both months are
now right.

It is false when the month it belongs to is CLOSED. A July cost that belongs
to May cannot be moved into May — May is signed, filed and reported. It is a
prior-period item sitting in this year's numbers, and calling it timing
implies an offset in a month that will never receive one.

`reforecast.py` refuses the word, names the closed month, and puts the full
amount into the year. And the disposition ledger will not accept `timing`
without a month at all:

> *A cost that moved out of a month nobody can name has not moved — it has
> been renamed, and the year is short by the amount.*

## 6. Absorption: costed, never chosen

An unplanned commitment can be accepted — the year gets worse — or absorbed,
which means something else does not happen. The arithmetic is easy and the
choice is not.

```
  60,000 a month from 2026-08, 5 months left  ->  300,000

  [accept]  the year is worse by 300,000.00
  [absorb]  needs 44.4% of the 676,216 left in Engineering & ML
              6020    211,000.00  remaining at the last three months' rate
              6030    148,400.00
              6040     31,675.00
```

The engine marks nothing as discretionary, because nothing in a ledger says
what is discretionary — a contract that runs to December and a conference
nobody has booked look identical from here. **An engine that picks what to
cut has made a strategy decision wearing an arithmetic costume.**

It also will not choose the plan version. Two are live at this company and
the semantic layer has not ruled which is primary, so the version is named on
the command line by a person or the engine stops — the same refusal
`variance.py` already makes, for the same reason.

## 7. How it is verified, and why that mattered here

A scan that returns nothing on a clean ledger is indistinguishable from a
scan whose every test is broken — **and the first version WAS broken, and
said "nothing found" in exactly the same tone.**

So both engines are exercised against faults planted on purpose.
`tools/test_entry_triage.py` copies the instance, plants one fault of a known
shape, and asserts the matching test fires on that entry and that the clean
run does not. Seven of seven fire. `tools/test_reforecast_loop.py` runs the
full chain and checks the arithmetic by hand, including both refusals. Six of
six.

One of those tests found a real engine flaw rather than a test bug. The
counterparty-habit signal was being diluted by balance-sheet postings — a
compute supplier here is paid on a prepaid commitment and drawn down against
it, so they post to a prepayment as often as to cost of revenue, their "usual
account" was a coin toss, and a bill of theirs moved to a third account
produced nothing. **An expense account and a balance-sheet one are not two
candidate homes for the same cost.** Moving between them is capitalisation,
which is a different question with a different answer.

## 8. Where it sits in the close

Three new steps, and one existing one that now has a partner:

| | |
|---|---|
| **CL-31a** | Entry triage. Not blocking, expected nil, population always reported |
| **CL-31b** | Disposition of every finding. **Blocking** — signing a close over findings nobody closed is the failure this prevents |
| **CL-31c** | Reforecast from the dispositions. Feeds CL-35 |
| **CL-19** | Recurring accrual roll — now depends on CL-31b, because an entry disposed `accrue` becomes an expectation the scan must find reversed or billed next period |

That last dependency is what makes it a loop rather than two scripts: the
accrual scan finds what is missing before the close, the triage finds what
arrived wrong during it, and each one's output is the other's input a month
later.

## 9. Two things this does not do

**It does not post.** No `smtp`, no `requests.post`, no journal writer
anywhere in the package, and these three engines do not change that. A
`correction_shape` is the debits and credits a correction would carry, not an
instruction to carry them.

**It does not rank.** No severity, no confidence score, no ordering by
importance — because a ranking is a judgement with a number in front of it,
and the whole architecture holds that judgement belongs to a person.

## 10. The line this earns

> *"Ask it what happened in March and it does not give you a variance — it
> gives you the two postings of forty-one thousand four hundred and forty-five
> dollars and fifty-five cents that are both in account 6020, one of which the
> bank has already paid. Tell it that's a duplicate and the forecast doesn't
> move, because a duplicate isn't a forecast event. Tell it something's just
> timing and it asks which month, and if that month is closed it tells you it
> isn't timing — it's a prior-period item, the year is worse by the amount,
> and there is no offsetting month coming."*

---

## 11. The favourable half, added after the first build

*24 Aug, same day. The build above handles costs that ARRIVE. It had nothing
to say about a cost that does not, which is half the variance and the more
dangerous half.*

### Nobody investigates good news

An overrun gets a meeting. An underrun gets a line in the pack saying
"favourable timing" and no further questions — and four of the five things it
can be are not favourable at all:

| | |
|---|---|
| the spend is coming, later | a deferred cost, not a saving |
| the spend is coming, and bigger | a hire starting in September costs more in Q4 than the plan assumed for the year |
| the work is not happening | a genuine saving — and possibly a plan nobody is delivering |
| somebody stopped invoicing us | a payable accruing in silence |
| the cost went somewhere else | a coding error, and the money is in another centre |

Only the third is money. `underspend.py` gathers the evidence that separates
them — run rate against plan and its trend, suppliers gone quiet, planned
months with nothing spent, unpaid bills from that centre's own suppliers —
and states the evidence rather than the answer.

On this company it separates two positions that look identical in a pack:

```
  Club Sales        VP Sales           under by 139,657
      running at 57,837 a month against a plan of 81,599  (71%)  ·  declining

  Product & Design  Head of Product    under by 21,490
      running at 61,709 a month against a plan of 60,762  (102%) ·  flat or rising
```

Both are favourable YTD. One is still accruing at 71% of plan; the other has
already caught up and will not produce another dollar. **An underspend that
has stopped growing is not a source of future savings**, and nothing in a
variance column says which is which.

### The unit of the question is the owner

*"Can this underspend cover that overspend?"* is not an arithmetic question.
It is a question about authority, and the answer changes at every level:

| rung | who decides |
|---|---|
| inside one cost centre | the owner, today |
| across one owner's centres | the same owner — and they may not realise the two centres land on different lines of the statement |
| across two owners | somebody senior to both, and until they say so the money is not available: it is somebody else's |

An engine that nets one department's favourable variance against another's
unfavourable one produces **a company that is "on plan" and two managers who
are not.** So it nets in rungs, each naming its authority, and rung 3 is not
computed at all without a named authoriser — because the number itself is the
argument. A line reading "USD 217,370 is available across the company" has
already claimed the budgets are one pot. They are several people's, and each
of them agreed to a different number.

### And one owner's span can cross the gross margin line

At this company the **VP Engineering owns both Engineering & ML (R&D) and
Infrastructure (COGS).** Moving budget between them is entirely within their
authority, needs nobody's permission — and moves **reported gross margin**
while leaving operating income exactly where it was.

That is the most likely unintentional restatement in a company this size,
because the person with the authority has no reason to be thinking about the
margin line when they use it. Every cross-statement transfer now carries the
warning beside it. Verified by planting an underspend in Infrastructure and
watching the flag fire.

### Four dispositions, and only one of them is money

`not_yet_spent` · `release` · `offset` · `reallocate`

Nil, **minus the amount**, nil, nil. `release` is the only favourable
disposition that improves the year, and it is the one that says the work is
not happening — which is a harder sentence to sign than "favourable timing"
and is the point of making somebody choose. A deferred cost reported as a
saving gets **banked twice**: once now as a saving and once later as a cost.
The engine reports it on its own line, `deferred, NOT saved`.

The ledger refuses an `offset` with no `authorised_by`, and an `offset` that
does not name what it covers:

> *An offset against nothing in particular is a saving being spent in advance
> of a decision.*

### Verification

Thirteen checks, all on planted faults, including the gross-margin straddle
and both refusals. Portability 16/16.

### The line this earns

> *"Ask it about a favourable variance and it will not call it a saving. It
> tells you the centre is running at 71% of plan and still declining, that
> two of its suppliers have not invoiced in three months, and that after the
> unpaid bills there is less available than the variance says. Then it asks
> who may move it — and if the answer is another owner's budget, it does not
> add the two together, because a company that is on plan while two of its
> managers are not is not a company that is on plan."*

---

## 12. The fifth thing, which is not settled inside the year

*Same day. §11 listed five things a favourable variance can be and measured
four of them. The fifth needed its own arithmetic.*

### A deferred hire is not a saving with a delay. It is a saving and a cost.

A role planned from January that starts in September does not save eight
twelfths. It saves eight twelfths **once**, this year, and costs twelve
twelfths every year after. The number the next twelve months inherit is not
what this year averaged — it is **the rate the year ends on**.

Which makes this the underspend to be most careful with, because every month
it persists makes the in-year saving larger and the exit rate exactly as big
as it always was. **A deferral that reaches December looks like the best cost
control in the company.**

### The table that makes the point

Eight open roles here, all planned Aug–Dec:

```
   slip   in-year cost   saved here     Dec rate   ann. from Dec  ann. once landed  pushed to next yr
    0m        227,851            0      447,791       5,373,496         5,373,496                  0
    1m        153,941       73,909      437,733       5,252,792         5,373,496            120,704
    2m         90,091      137,760      425,487       5,105,848         5,373,496            267,648
    3m         38,485      189,365      403,839       4,846,072         5,373,496            527,424
```

Read the last two columns together. **A three-month slip saves USD 189,365
here and pushes USD 527,424 into next year — 2.8x.** The December rate falls,
which is what a pack would show; the cost once every role has landed does not
move by a dollar, because a role that slips past December has not been
cancelled, it has been moved into a year the report does not cover.

The first version of this engine got that wrong. It printed only the December
annualisation, watched it fall as roles slipped out of the year, and captioned
it *"does not move at all"* — a note contradicted by the table directly above
it. The invariant column exists because the falling one is a trap.

### And whether the plan is still arithmetically possible

```
  8 role(s) over 5 remaining month(s) requires 1.6 hires a month
  this company has achieved 1.25 a month over the last 12 months
  required is 1.28x what has been managed before
```

Two rates, side by side. The engine does not say the plan will miss. It says
what the plan now requires and what this company has managed before, and the
reader knows which of those is a fact.

### The two engines now speak

A favourable variance says whether open roles sit behind it:

```
  Club Sales        under by 139,657   2 open role(s) adding 15,525 a month once filled
  Customer Success  under by  25,586   2 open role(s) adding 14,432 a month once filled
  Product & Design  under by  21,490   1 open role   adding 10,059 a month once filled
  Legal             under by  26,361   —
```

Legal is the only one of the four with no roles behind it, which makes it the
only one that might be a saving in the ordinary sense.

### The schema problem that was not one

§11 closed by saying this needed a schema change, because `headcount.csv`
records the cost centre as a function. **That was wrong and worth recording.**
The columns are simply named the other way round — `function` holds the
department, `cost_center` holds the function — in both the roster and the
hiring plan. That is what `mapping.json`'s `columns` block is for, and the
fix is two lines.

The engines were right by accident and the contract was wrong on purpose:
every model here reads `function` and gets the department, so the workbooks
were correct, while anything reading the contract's `cost_center` off the
roster was getting "S&M". A mislabelled column is not a missing capability,
and calling it one closes a door that was open.

### Burden is declared or excluded, never invented

Employer cost on base is declared per employment type. Undeclared, the engine
runs on base salary and labels every figure understated — USD 4,224,000
instead of 5,373,496 here. An understated number with the understatement
named is usable. An invented burden rate is not.

### Verification

18 checks now, all on planted faults or measured invariants — including the
slip invariant, the burden fallback, and the refusal when no hiring plan is
mapped (*a company with no plan file has not deferred nothing — it has not
said*). Portability 17/17.

### The line this earns

> *"Show it a department under budget and it will not congratulate you. It
> tells you two roles are open in there, that filling them adds fifteen and a
> half thousand a month, and that if they slip another quarter you will save
> a hundred and eighty-nine thousand this year and hand five hundred and
> twenty-seven thousand to the next one. Then it tells you the plan now needs
> 1.6 hires a month and this company has never done better than 1.25."*
