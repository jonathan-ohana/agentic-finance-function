# 88 — Arcline v2: repairing the instrument

*25 Aug 2026. Executes the worklist filed in doc 87. The answer key is now **computed from the
finished dataset**, four plant defects are fixed, two generator artefacts the agents surfaced are
closed, and the tie-out suite has grown from 25 checks to 29. All green.*

---

## The ruling

**Nothing in the answer key is typed any more.** `plants.build_manifest()` runs last, after every
statement is derived, and computes each of the twenty-five expected findings from the data it is
describing. The three wrong amounts doc 87 records — PL-03, PL-16, PL-18 — could not recur, because
there is no longer a place to write a number that the data does not produce.

This is the same move doc 85 made on the LRP (year one is the budget by construction, not by
assertion) and doc 75 made on portability (prove by running, not by reading). It was overdue here
and it was found by an agent rather than by me, which is the argument for running the thing.

---

## What changed

### 1. The key is derived

Twenty of the twenty-five amounts are now computed. The five that remain literal are the ones that
*define* the plant rather than describe it — the size of the duplicate invoice, the reclass, the
prepayment. Everything downstream of those is computed: the gross-margin points a misclassification
costs, the months a leak has been running, the annualised value of a usage cliff, the tax exposure
by state.

Two things fell out of doing this that a typed key had been hiding:

- **PL-07 was pointing at a contract that had finished its ramp.** The expected finding computed to
  **USD 0**. It had presumably been wrong since the instance was built; nobody could tell, because
  the key asserted USD 168,000. The selector now picks a contract that is demonstrably mid-ramp at
  January and the finding computes to USD 167,119 at 73% of the contracted fee, month 7.
- **PL-10 and PL-11 were double-counting Chorus** — once as shelfware, once as duplicate tooling.
  Two findings, one vendor, one amount claimed twice.

`build_manifest` now refuses to return a manifest containing a zero, which is how PL-07 announced
itself.

### 2. Four plant defects, fixed

**Split customer identity — the root cause was phase ordering.** `plants.apply()` ran after the
change log, the usage file and the AR subledger were built, so its renames reached only the files
written later. The fix is structural, not cosmetic: plants now run in **two phases**.

```
plant_data()    contract terms, usage, amendments   -> BEFORE the revenue model
plant_ledger()  journal entries only                -> after the ledger is built
build_manifest()                                    -> last, from the finished data
```

The renames are gone entirely — the generated names were always as good, and the IDs are what
anything sensible joins on. And the split fixed a second bug nobody had noticed: **the usage cliff
was being applied after revenue was computed**, so `usage_2026-01.csv` did not foot to account 4010.
It does now, in all thirteen periods, and there is a check for it.

**PL-20 is now planted on the account where it matters.** The target is chosen from December
volumes rather than by index, so it lands on the largest overage payer in the book. December
overage USD 31,551 against January USD 3,503: **USD 25,422 in the month, USD 305,059 annualised**,
and it is the top row of any month-on-month usage ranking. The previous version sat on an account
with zero January overage and a real impact of USD 1,472 — which is why run 01's agent found it,
ranked it eighth and dismissed it, correctly.

**PL-06 is now detectable.** The test is `notice_deadline < today <= current_term_end AND auto_renew
= Y AND renewals_to_date = 0` — renewal has become certain and nothing recorded it. Exactly one
contract in the book trips it. The expected finding is also stated correctly for the first time: it
is not current ARR that is understated, it is **backlog** — USD 308,160 that drops out of every
forward view after February and is contractually owed.

**PL-05 now has a structured trail and stays the hard case.** The amendment is in `amendments.csv`,
so a join to the change log and to invoiced amounts finds it. The amount and the reason are in the
order form prose. The key says which route is which, and the preamble states that nineteen of the
twenty-five are reachable from structured data alone and four need a document read.

### 3. Two generator artefacts the agents surfaced

**Preparer and approver names now exist on the headcount register.** S. Patel, M. Halloran and
T. Byrne appeared on several hundred entries and no roster. The finance cost centre's names and
titles are pinned, and there is a check that every named preparer and approver matches a person.

**The prepaid release schedule no longer steps by an identical factor.** January non-payroll costs
were set as absolute targets, independent of the December run rate, so every vendor inside an
account jumped by the same ratio — 1.64× across all ten S&M software vendors. January is now
**derived from December** at a per-account ratio, mostly 1.02 to 1.07, with three named exceptions
that are the variance story (legal at 1.48 on two enterprise renewals, Delaware franchise tax due
31 January, events down 8%).

### 4. A bug the new checks found on their own

The ARR solve counted a customer churning on 31 December as **still live** at 31 December, while
`mrr_series` read the same change log and counted them gone. Committed ARR at Dec-25 landed
USD 209,709 short of target — exactly twelve months of the December churn. It had been latent since
the instance was built and only surfaced because the December churn moved when the RNG stream
shifted. Fixed, and the boundary is now commented in the code so it is not re-broken.

### 5. Sales tax became computable rather than asserted

`customer_agreements.csv` carries a `billing_state`, and PL-23's exposure is computed as annualised
revenue in states that tax SaaS times the published combined rate: **roughly USD 396,000 a year**.
Run 01 found the issue but quantified it at USD 62,000 — the stale balance on account 2070 — because
the exposure was not derivable from anything in the folder. Now it is.

---

## The tie-out suite: 25 checks to 29, all green

Four new checks, each of which would have caught something this pass fixed:

| | |
|---|---|
| Usage overage foots to account 4010 in every period | catches the phase-ordering bug |
| Every `customer_id` carries one name in every file | catches split identity |
| Every named preparer and approver is on the headcount register | catches invented people |
| Every manifest entry states an expected finding, and none computes to zero | catches a plant that did not take |

The suite still reads the **output files** and never the generator's working numbers.

---

## The January variance is unchanged, which is the point

| USD | Actual | Plan | Variance |
|---|---|---|---|
| Revenue | 1,770,891 | 1,819,391 | (48,500) |
| Cost of revenue | 571,145 | 469,745 | (101,400) |
| **Gross margin** | **67.7%** | **74.2%** | **(6.5) pts** |
| Research and development | 1,094,200 | 913,600 | (180,600) |
| Sales and marketing | 566,281 | 767,281 | 201,000 |
| **Total operating expense** | **2,304,052** | **2,298,452** | **(5,600)** |
| Operating result | (1,104,306) | (948,806) | (155,500) |

Every absolute variance is identical to v1, because the plan is derived as actual plus a designed
delta per account. The underlying numbers moved; the test did not. That is the property worth
having.

FY2025 now reads revenue USD 16.98m, gross margin 71.1%, operating result USD (11.75m). ARR at
31 January USD 18.23m across 121 live logos.

---

## What is not fixed, deliberately

**G&A still runs at roughly 36% of revenue.** Run 01's agent flagged it and the sealed key already
says it is true, unflattering and not planted. It stays.

**The close checklist names evidence workbooks that do not exist** (`CL-01_2026-01.xlsx` and the
rest). Both agents noticed. This is arguably the most realistic thing in the folder — a checklist
that claims evidence nobody can produce — and it is now stated as such in the key rather than left
as an oversight.

---

## Next

- [ ] Vendor spend review agent, against v2. PL-09 to PL-12 are the target and all four now compute
      from `software_agreements.csv` and `vendor_master.csv`. Run 01 established that the close loop
      has no vendor lens; this establishes whether a vendor lens finds them cleanly.
- [ ] Then the reporting pack agent, against a corrected close.
- [ ] Re-run variance and accruals only when there is a reason — after the pack, or as the sealed
      month. Re-running now would re-measure what doc 87 already established.
