# 95 — Run log

*Every run, one block, newest first. Five fields, always the same, so it can be skimmed.*

**RAN** what executed · **FOUND** the score · **VERDICT** pass / partial / fail, and whose fault
**FIXED** what changed, and whether it is closed · **OPEN** what needs Jonathan

Whose fault matters more than the score. **INSTRUMENT** = my generator was wrong. **ANALYSIS** =
the agent was wrong. **PLATFORM** = neither; the environment could not do it. Confusing the three
is how a test stops measuring anything.

---

## RUN 13 · The check that reads prose, and two plan lines that now follow their own basis · 1 Sep

**RAN** Built `docverify.py`, tested it both ways, and fixed the two interest income defects in the
generator — verified on a throwaway build outside the instance, so nothing signed was touched.

**FOUND**

**The check works, and the negative test is the part that matters.** `docverify.py` asserts one weak
rule that is therefore cheap to keep true: *every figure quoted in a write-up must exist somewhere in
the workbook it describes.* It reads recalculated values, like `packverify.py`, because a checker that
trusts what is typed in the file it is checking has checked nothing. On the corrected write-up: **54
figures checked, all present.** Re-introduce the drift this log found yesterday and it fails on exactly
the three figures that were wrong — the stale operating result and both stale runway numbers. **A check
that has never been shown to fail is a check nobody has tested.**

Five lines needed exempting, and they were the right five: figures about the generator's own history —
the payroll with no cost center, the two cuts that footed at 2,427,160, the December cash walk, the
67,500 double count. None is a claim about the pack. They now say so in the file.

**Interest income, FY2026.** Derived from the balance it is earned on, at the rate the ledger uses,
imported rather than repeated — a constant with two homes is a constant that will disagree with itself.

| Planned | Jan | Jun | Dec | Jan variance vs actual |
|---|---:|---:|---:|---:|
| Was | 70,000 | 72,000 | 74,400 | 14,181 |
| Now | 83,338 | 71,752 | 61,714 | 843 |

The old line rose 6% across a year in which the balance earning it falls 22%. Its written basis already
said *"planned average money market balance at the rate in force at lock"* — **the arithmetic simply did
not follow the sentence in front of it.** The 14,181 favourable variance it produced in January was not
a finding about Arcline; it was the plug, showing up as news.

**Interest income and the rest of the below-the-line, FY2025.** `build_fy25_plan` gave revenue, cost and
opex a plan shape and sent everything else through an `else` branch that returned the actual unchanged.
Those three accounts now carry a plan struck at the lock — FX at nil by construction, the same
convention the FY26 plan already states. **FY25 account-months where plan equals actual to the cent: 36
→ 0.**

**VERDICT** PASS — **INSTRUMENT**, both fixed at the source. The throwaway build passes 48 of 48; the
shipped instance, untouched, still passes 51 of 51.

**FIXED**
✅ `docverify.py` — in `_generator/` and published in the repository beside the other two checkers.
✅ `planbuild.py` — interest income derived from the planned treasury balance and the imported rate.
✅ `plan.py` — the FY25 `else` branch that carried actuals through is gone.
✅ The write-up marks its five out-of-scope figures rather than the checker guessing at them.

**OPEN**
❗ **The generator is now ahead of the shipped instance, deliberately, and nothing checks that.** Both
fixes exist in code and neither exists in the delivered files, because rebuilding regenerates a signed
period. That was the right call and it creates **the same defect this log has now found five times: two
artifacts describing the same thing, with nothing putting them side by side.** The instance should carry
a build stamp — the generator's own hash at build time — so a delivered folder can say which version of
the code produced it, and a check can say when the answer is "not this one."
⚠️ **`docverify` maps one write-up.** Twenty-five others quote figures nothing verifies. The number is
printed on every run, unscored, because a permanently red check is a check nobody reads — and because
the point is that it should fall.
❌ Documents still contradict the ledger on three January figures (Run 05).

## RUN 12 · The write-ups had drifted from the workbooks · 1 Sep

**RAN** No agent. Preparing the public repository: rendered the January pack to screenshots, which
meant opening the workbook and reading what it computes. Then swept every write-up that quotes those
workbooks, and re-ran both suites on the delivered instance.

**FOUND** **The documents describing the workbooks had been wrong for four days.** The pack and the
LBE were rebuilt on 28 Aug with the run 08-09 instrument fixes. Nothing re-read the write-ups against
them.

The pack write-up — **every figure in both tables except the revenue lines.** Runway is the one that
would have been quoted out loud: **31.3 months stated against 35.3 actual**, a four-month error in the
favourable direction. Operating result, adjusted EBITDA, gross margin, closing cash, and the whole Q1
LBE column set, all stale. Two prose findings were wrong rather than imprecise: DSO (55.1 → 86.7
stated; **55.9 → 85.6** computed), and interest income.

Then, chasing the interest income line, **two new instrument defects on the plan side:**

❗ **The FY2026 plan for interest income is an arithmetic ramp.** 70,000 in January, stepping exactly
400 a month to 74,400 in December — on a cash balance that is falling. The plan has interest income
rising 6% across a year in which the actuals fell 22%. The actuals are fine; they decay with cash, as
they should.

❗ **The FY2025 plan for three accounts is the FY2025 actual, to the cent.** 9000 interest income,
9020 FX, 9030 tax — all twelve months each. Those lines cannot show a variance in FY25, by
construction. Contained, and worth stating precisely because the obvious fear is worse than the fact:
**of 636 FY25 account-months, exactly 36 have plan equal to actual, and all 36 are those three
accounts.** Every operating account is genuinely planned.

Both are the same defect run 01 named once already — *a variance against a budget that was not set is
not a variance.* Fixing the five accounts with no plan line gave them plan lines. It did not give them
plans.

**VERDICT** **The instrument passes; the documentation layer failed.** 51 of 51 build checks and 42
of 42 pack checks pass. **INSTRUMENT**, in a location this log has not scored before: **the write-ups.**

This is the fifth instance of the shape every other instrument defect has had — *a number right in one
place and wrong in another, with nothing putting the two side by side* — and this time the two
artifacts were **the workbook and the document describing the workbook.**

It is also Run 05's open item, wider than Run 05 scored it. That was filed as *"documents contradict
the ledger on three January figures"* and read as a defect in the instance's generated documents.
**The write-ups are documents too, and they drift the moment an artifact is rebuilt and the prose is
not.**

Two things made it invisible. **The workbooks carry no cached values** — every cell is a formula,
computed on open, which is the property that makes the pack honest and also means the 28 Aug figures
existed nowhere on disk. Until someone opened the file, the stale numbers in the write-up were the
only readable version of those numbers. And **nothing in the apparatus reads prose**: `packverify.py`
asserts the workbook against the instance CSVs, `validate.py` asserts the instance against itself,
both were passing the whole time. **The one artifact a human reads first is the one artifact nothing
verifies.**

Not found by a check. Found by rendering a spreadsheet to a picture.

**FIXED**
✅ **The pack write-up corrected** — tables left standing as the 26 Aug record, a warning at the head,
and a correction section carrying both delta tables and the verdict. A build record that silently
updates itself is not a record. The figures quoted in this repository are read out of the rebuilt
workbooks, not carried across from the write-up.
✅ **The run-03 write-up corrected** — the interest income item superseded, the prepaid item marked
closed. It had been closed for days: `validate.py` carries *"every prepaid release ties to its
contracted ACV"* and it passes. The doc was the last place still calling it open.
✅ **Provenance line added** — which artifact, which build, read on what date. A figure with no stated
provenance cannot be re-verified, only re-typed.
✅ **The unverifiable figure is gone.** *"January receipts were 1,058,715"* tied to nothing in either
workbook and was dropped rather than restated. An unverifiable number inside the paragraph arguing for
verification is the worst place to leave one.

**And one of my own, worth recording because it is the same failure inside the fix.** The first
correction I wrote said the plan carries *"a flat 70,000 a month."* It does not — it steps 400 a
month, which is what turned a dull correction into the FY26 finding above. **I corrected a stale
number with a number I had not opened the file to check.** Caught only because I went to the plan CSV
before writing this entry. Same lesson as Run 10, one level in: the fix needs the same evidence
standard as the finding.

**OPEN**
❗ **Nothing checks a document against the artifact it describes.** *Built in Run 13 — `docverify.py`.*
 Mechanical for tables — extract the
numbers from the markdown, recompute from the workbook, assert — and probably not worth attempting for
prose. Which argues for putting quoted figures in tables, so they are checkable by construction.
❗ **The two new interest income defects are unfixed.** The FY26 ramp and the FY25 backfill.
*Both fixed in the generator in Run 13; still present in the delivered instance until it is rebuilt.*
⚠️ **This log's own RUN 04 entry says "DSO 55 → 87 days."** The workbook computes 55.9 → 85.6. Left
uncorrected in place, noted here, on the standing rule.
❌ Documents still contradict the ledger on three January figures (Run 05).

## RUN 11 · Day clock, cycle 2 · 1 Sep

**RAN** Advanced the clock to 2026-02-03 (32 GL lines, 7 bank, 9 bills), then a single analyst agent
blind against the new day, session-driven. Scored against the key.
**FOUND** 1 planted, **1 clean hit, 0 partial, 0 missed, 0 false positives.**

**WRONG_PERIOD** — Outreach Corporation, `BILL-20260203-9283`, **USD 82,151.37** booked to 2026-02
with a January service period. The agent got the amount to the cent, named the document, and made the
argument that matters: January is closed and signed, so this is a prior-period item, not a February
expense. It also built its own benchmark when the obvious one was missing — Outreach has no prior AP
bill, so instead of guessing a run rate it priced the bill against the contract (SWA-0036, USD 118,000
annual) and the prepaid release of USD 9,833.33/month, making the bill 8.36x the monthly carry. It gave
both readings and refused to call it a duplicate.

**VERDICT** PASS — **first clean sweep of a day clock cycle.** And it cleared four signals by naming
what cleared them rather than assuming: cutoff exceptions, post-close inbox, contract exceptions, the
accrual schedule. That is the standing rule from the runbook, being followed unprompted.

**FIXED** Nothing needed fixing in the analysis. The agent surfaced two instrument defects instead:

❗ **The open period has no precompute.** Every file in `analyst-inputs/` is stamped 2026-01. The
monitor reviews an open February with no `variance_signals`, no `contract_exceptions`, no
`cutoff_exceptions` for the period it is actually working. It found this one from the raw ledger.
**Precompute defines the search space — and February currently has none.** Routed to data_contract.

❗ **A score outlived the data it scored.** The 2026-02-02 scorecard row records a PARTIAL on
OVER_CONTRACT. That date's current key says DUP_PAYMENT — two Stripe bills of USD 28,199.66. The day
was regenerated when the `with_history` fix landed and the old score was never invalidated. It has sat
there since, looking like evidence. The day clock needs to stamp a fixture version and scoring must
refuse a mismatch. Routed to data_contract.

**OPEN** ⚠️ **The seal was weaker this run than a scheduled one.** Session-driven, the keys folder sits
under a mount the analyst subagent could technically reach; it was told not to and there is no sign it
did, but that is an instruction, not a seal. Only the scheduled path — where the folder is genuinely
not attached to the task — gives the real thing. One more reason to get the binding working.
2026-02-02 is now unscored and unreviewed in its current form.

## RUN 10 · The daily rec was never running — and RUN 06 was misdiagnosed · 1 Sep

**RAN** Jonathan: "the daily rec is not working." Fired the daily monitor by hand from a session
where the laptop was demonstrably reachable, and read what the scheduler said back.
**FOUND** One line, and it settles everything:

> `run not approved for Claude Desktop (Windows) — this run uses the cloud only (no_signed_approval)`

**VERDICT** FAIL — and **the fault was mine, not the platform's.** RUN 06 concluded "scheduled runs
cannot reach the laptop's tools" and filed it as PLATFORM: unfixable, work around it. That was wrong.
The tasks had been created without `requires_local_device`, so they were never bound to the computer.
Connecting folders to a task is not the same as binding the task to the machine — the folder list was
present all along, which is exactly why it looked like a platform wall.

**This is the failure mode the INSTRUMENT / ANALYSIS / PLATFORM vocabulary exists to prevent, and I
walked into it.** PLATFORM is the only one of the three that licenses giving up, which makes it the
label that has to clear the highest bar. It cleared none: I never fired a trigger by hand and read the
error. Three runs marked SUCCEEDED, 8 to 46 seconds each, writing nothing, and I read the silence as a
wall instead of asking what the wall said.

**FIXED**
✅ All three tasks recreated with `requires_local_device: true` — the binding cannot be added after
creation, so recreating was the only route. Each returned `bound: this computer`. The keys folder is
attached to the day clock and NOT to the monitor, so the seal survives the rebuild.
✅ Every runbook now opens with a STEP 0 that distinguishes the three failures that look identical from
the inside: no device tools at all (not bound), tools that error (laptop offline), tools that work but a
folder is missing. Each gets its own first line in the report. The August failure was invisible because
all three collapsed into one message.
✅ Stale expectations corrected: the weekly expected "50 of 50" against a 51-check suite, and now also
treats a suite reporting zero checks as a failure rather than a pass.
✅ The monitor's runbook now points at `analyst-runbook.md` and `analyst-inputs/`, so the scheduled run
inherits what Run 09 built instead of only session-driven runs seeing it.
✅ The three dead tasks deleted. They could never have worked.

**OPEN** ❗ **Jonathan must approve the three tasks on the Windows machine.** The binding is declared;
his approval is what signs it. A re-fire still returns `no_signed_approval` until he does. Until then,
session-driven runs remain the fallback — those work.
❌ Documents still contradict the ledger on three January figures (Run 05).

## RUN 09 · Closing PL-19, and a ledger with two homes · 29 Aug

**RAN** No agent. Maintenance before cycle 2: closed the last open review item, then checked the
instrument's own bookkeeping.
**FOUND** Five things, all mine, none of them found by looking harder at the data.
**VERDICT** PASS — **INSTRUMENT** throughout. Review ledger now **0 open, 3 closed**.

**FIXED**

✅ **PL-19 closed.** `analyst-runbook.md` v2 ships inside the instance and names every precomputed
input with the question it answers — `arr_movement_gross.csv` reads *"Is net growth concealing gross
churn? Read the components, never the net."* The fix is a versioned file, not a line in a prompt: a
prompt is retyped each run and drifts each time it is retyped.

✅ **A check that passed on nothing.** The new "every input is named in the runbook" check resolved
its input list from a container path that does not exist on the laptop. Zero files, zero unnamed,
green light. The determinism check taught this exact lesson once already — *a green light on an empty
glob is worse than a red one, because nobody investigates green.* The check now fails when it finds
no inputs, and says why.

✅ **The runbook pointed at files that weren't there.** The precomputed CSVs sat outside the instance
so they would not clutter the finance folder; the runbook naming them shipped inside it. Now
`04-month-end-close/analyst-inputs/` carries the analyst's desk with the instance. Copied, not moved —
the finance folder stays a finance folder.

✅ **The review ledger had two homes.** The container held the January items, the laptop held the day
clock's. PL-19 read as closed in one and absent in the other. Merged onto the laptop, container copy
retired. **A ledger that says different things in two places is not a ledger, it is two opinions.**

✅ **Cycle 1 was mis-dated.** The scorecard and ledger said 2026-02-04; the day clock's own answer key
says 2026-02-02. A hand-typed date beside a generated one is the hand-typed one that is wrong.
Corrected in both.

**OPEN** ❌ Documents still contradict the ledger on three January figures (Run 05). Does not block a
February day run. 51 of 51 build checks and 42 of 42 pack checks pass, verified on the laptop copy.

## RUN 08 · Sealed re-run, with the contract surface · 28 Aug

**RAN** Built the contract surface, re-ranked the control signals, routed two orphaned tables — then
re-ran the **same sealed composition** blind, single agent.
**FOUND** 23 findings. **17 clean hits (was 11), 2 partial, 2 found-but-misquantified, 4 missed.**
**Seven of the nine misses converted.**

| Converted | How |
|---|---|
| PL-02 AWS accrual | Signal re-ranked to HIGH — was 1 of 15 look-alikes |
| PL-05 Stonebridge amendment | `amendment_not_in_mrr` — named the customer |
| PL-06 Junction Claims renewal | `notice_window_passed` |
| PL-07 Fairhaven ramp | `ramp_not_stepped` |
| PL-12 Halstead no contract | `vendor_no_contract` |
| PL-16 Commission accelerators | `commission_earned_vs_accrued` |
| PL-23 Sales tax | `tax_exposure_by_state` |

**VERDICT** PASS — the fix worked, and it worked because it was *arithmetic*, not better prompting.
**FIXED** ✅ Contract surface (6 joins). ✅ Control signals ranked High / Medium / Housekeeping. ✅ The
ARR waterfall and post-close inbox routed into the analyst's inputs. ✅ Statutory counterparties excluded
from the no-contract check — you cannot sign an agreement with a filing office.
**OPEN** ❌ **PL-19 still missed, and this one stings**: `arr_movement_gross.csv` was in the inputs, says
"Net growth with gross churn behind it," and no finding cites it. Computed, delivered, unread — the exact
failure the re-ranking just fixed for PL-02, in a different file. **A file nothing instructs you to open
is a file nobody opens.** Routed to the runbook. *Closed in Run 09.*
PL-20 and PL-22 regressed, and that is a coverage effect: one agent doing everything instead of three
slices. Not a capability loss.

## RUN 07 · Day clock, cycle 1 · 28 Aug

**RAN** Monitor agent, blind, on one day of newly generated February activity (2026-02-02).
**FOUND** 1 planted, 1 surfaced. Right document, wrong reason, wrong amount.
**VERDICT** PARTIAL — **INSTRUMENT.** The plant was "vendor billed above its run rate," on a vendor
with no billing history at all. The monitor ran the test, said it was inconclusive and explained why.
It was right; the fixture was wrong.
**FIXED** ✅ `dayclock.py` — that plant now only lands on vendors with prior AP bills. Verified across
12 fresh days. Routed and closed.
**OPEN** Nothing.

## RUN 06 · Arming the schedules · 28 Aug

**RAN** Three test firings of the daily monitor as a scheduled task.
**FOUND** All three marked `SUCCEEDED`. All three wrote nothing. 46 seconds each.
**VERDICT** ~~FAIL — **PLATFORM.** Scheduled runs cannot reach the laptop's tools.~~
**CORRECTED IN RUN 10: this was INSTRUMENT, not PLATFORM.** The tasks were created without a device
binding and so ran cloud-only. Fixable, and fixed. The original verdict stands here uncorrected on
purpose — a run log that quietly edits its own wrong calls is not a log.
**FIXED** ✅ Two of my own errors, both found by this: the runbook's failure path wrote into the folder
it couldn't reach, and "SUCCEEDED" was being treated as "the work happened." Both corrected.
❌ The platform limit itself — cannot be fixed from here.
**OPEN** Schedules disabled; we drive from sessions. The weekly check stays on as a canary.

## RUN 05 · Sealed blind test · 28 Aug · [doc 94](#)

**RAN** A compositor built an instance whose 25 planted issues neither of us saw. Three analyst agents
worked it blind.
**FOUND** 36 findings. **11 clean hits, 2 found-but-misquantified, 2 partial, 10 missed.**
*Later revised to 9 misses — PL-03 was scored unfairly; the close had already corrected it and the
analyst said so.*
**VERDICT** PARTIAL — split fault.
**FIXED** ✅ Two checkers that only worked on one dataset. ✅ All nine misses addressed in Runs 08–09.
❌ Three figures are stated one way in the ledger and another way in the documents.
**OPEN** The document-vs-ledger contradiction, and a check that a figure appearing in both must agree.
*Run 12 found this is wider than scored here: the write-ups drift from the workbooks too.*

## RUN 04 · Reporting pack and Q1 LBE · 26 Aug · [doc 90](#)

**RAN** Built the January management pack (9 tabs) and the Q1 LBE, then verified both independently.
**FOUND** 42 of 42 checks pass. Building them exposed **4 defects**.
**VERDICT** PASS — all 4 **INSTRUMENT**, every one the same shape: a number right in one place and wrong
in another, with nothing putting the two side by side.
**FIXED** ✅ All four. Payroll with no cost center. Two opex cuts disagreeing by 366k while both footed.
Cash flow reporting revenue *plus* cost. EBITDA adding back credit loss instead of depreciation.
**OPEN** DSO 55 → 87 days is my collection model, not a finding. Recorded, not fixed.
*The workbook computes 55.9 → 85.6. Left uncorrected here; see Run 12.*

## RUN 03 · Variance analysis, 4-way fan-out · 25 Aug · [doc 89](#)

**RAN** Precompute engine, then four analyst agents in parallel on the January close.
**FOUND** 3 generator defects, then after fixing them, a **$67,500 double-count in the signed period**.
**VERDICT** PASS — **INSTRUMENT** on all four.
**FIXED** ✅ Commission budget, unplanned bonus and PTO, five accounts with no plan line. ✅ Three of the
four duplicate accruals removed; one kept as a deliberate control test.
**OPEN** Nothing. Speed: 20 min → 11 min, tokens per agent 205k → 100–128k.
*Run 12: the five accounts got plan lines, and two of them did not get plans.*

## RUN 01 · First variance analysis · 24 Aug · [doc 87](#)

**RAN** Single agent against Arcline January, scored against the answer key.
**FOUND** **17 of 25** found and quantified, zero false positives.
**VERDICT** PARTIAL — of the 8 non-hits, **4 were INSTRUMENT** and 3 key amounts were simply wrong.
**FIXED** ✅ Every expected finding is now computed from the finished dataset rather than typed.
**OPEN** Nothing.

---

## Standing tally

| | |
|---|---|
| Runs scored | 7 (plus four maintenance runs) |
| Defects found in my instrument | 30 |
| Defects fixed | 28 |
| Defects open | 4 — ledger/document contradiction (Run 05); no precompute for the open period, stale score after regen (both Run 11); generator ahead of the shipped instance with no build stamp (Run 13). The two Run 12 plan defects are fixed in the generator and still present in the delivered files |
| Verdicts later overturned | 1 — Run 06, called PLATFORM, was INSTRUMENT |
| Day clock record | 2 days, 2 planted, 1 clean hit, 1 partial, 0 missed, 0 false positives |
| Best blind score | **17 of 25 clean**, on a composition neither of us designed |
| Analysis misses outstanding | 0 — PL-19 closed in Run 09 |
| Review ledger | 0 open, 3 closed |
| Suites, last run 1 Sep | 51 of 51 build · 42 of 42 pack · 1 of 1 doc |

**Four patterns worth carrying into a conversation.**

Twenty instrument defects, and not one was found by an agent being clever. Every one surfaced when two
artifacts describing the same money were put side by side and required to agree.

The fix that moved the score from 11 to 17 was not a better model or a better prompt. It was **six
deterministic joins between the paperwork and the ledger**. Precompute defines the search space; widen
the surface and the same agents find the same class of thing they were already good at. The corollary:
**a file in the inputs that no instruction points at is a file nobody opens.**

And the newest one, which Run 09 produced twice in a single sitting: **the instrument's own bookkeeping
is part of the instrument.** A check that passes because it found nothing to check, and a ledger that
lives in two places, both report health while measuring nothing. Neither is visible from the data — only
from auditing the apparatus.

Run 10 is the sharpest version of that, and it is worth saying plainly because it was my error.
**PLATFORM is the only verdict that licenses giving up, so it needs the highest bar, and I gave it the
lowest.** Three scheduled runs finished quickly, marked SUCCEEDED, and wrote nothing; I inferred a wall
and worked around it for four days. The evidence that settled it took one tool call — fire the thing by
hand and read the error. **A silent failure is not evidence of an impossible one.** When a run reports
success and produces nothing, the next move is to make it talk, not to classify it.

Run 12 adds the fourth, and it is the uncomfortable one. **Every check in this system points at the
data. None points at the prose.** The workbooks were right the whole time and passed 93 assertions
between them; the documents describing those workbooks had been wrong for four days, and the only
reason anyone found out is that a picture of a spreadsheet had to be made for a public page. The
write-up is what a CEO, a hiring manager, or an investor actually reads. **It is the least verified
artifact in the system and the most read.**
