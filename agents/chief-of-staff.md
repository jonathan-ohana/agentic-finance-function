# 28 — Accounting coverage, the close checklist, and the CFO Chief of Staff

**Date** 18 August 2026 · **Sprint day** 4 (extended) · **Status** built and run

Two questions were asked. The first was an audit: does this workforce actually do the accounting a Series A head of finance does? The second was a design request: an agent that holds the CFO accountable to the finance calendar.

The first answer turned out to be the reason the second one matters.

---

## Part 1 — What the accounting audit found

### The honest answer: partial, and lopsided in a specific way

The ledger contains real accounting. Payroll accruals with a timing dict captured at posting. Operating expense accruals. Prepaid amortisation on the compute commitment. A fixed asset roll with depreciation. A deferred revenue rollforward. Unbilled receivable and its reclass on invoice. AR and AP aging. Bank transactions that tie to the cash accounts. Three-statement articulation to $0.02 across all nineteen periods.

That is more than most demo datasets and it is not nothing.

But when I enumerated the 37 named activities that constitute a real close and marked each one, **21 are performed and 16 are not** — and the 16 sort themselves with uncomfortable neatness:

> Everything that happens **inside** the close is done. Everything that happens **outside** it is not.

Every implemented step is one an agent performs on data it already has. Every unimplemented step needs a person, a system nobody connected, or a policy decision nobody made. That is not a coincidence — it is a portrait of what automation naturally reaches, and it is exactly the blind spot a package like this would ship with if nobody looked.

### The specific gaps, in order of how much they matter

**1. No VAT. Anywhere.** No invoice carries tax. No account in the chart of accounts holds it. For a business selling B2C consumer subscriptions across Spain, France, Portugal and Italy alongside B2B club contracts, this is the largest single omission in the dataset — three different tax treatments on the same product (domestic supply, cross-border B2B reverse charge, B2C One-Stop-Shop) and none of them represented.

Sized: **$1,828,527 of consumer revenue** in the twelve months to July. European consumer prices are quoted inclusive of tax. If €12.99 is what the customer pays, revenue is overstated by roughly **$317,000** — 7.9% of total — against a liability that has never been recognised.

The sharpest version of this only appeared when the Chief of Staff ran. VAT *is* being computed — the Evidence agent's unfiled-source sweep surfaces a spreadsheet, `2025 VAT returns summary`, holding output and input VAT by quarter for 2025 and netting to $27,245 payable. It sits outside every governed system, covers one year, and has no 2026 equivalent. None of it reaches the ledger.

That is worse than an omission, because it looks like a process. It is also the clearest illustration in this project of why the Evidence agent and the Chief of Staff belong to the same workforce: one found the file, the other knew what deadline it was evidence for.

**2. Accounts that exist and have never been posted to.** Three of them, and each is a missing close step wearing a chart-of-accounts entry:

| Account | Purpose | Lines |
|---|---|---|
| 1150 | Allowance for doubtful accounts | 0 |
| 9010 | FX gain / (loss) | 0 |
| 9090 | Income tax | 0 |

Account 1150 is empty in a business where **393 of 760 collections in the period settled late**, averaging fifteen days past due. There is aging and no provision.

Account 9010 is empty although **810 of 869 invoices are euro-denominated** and the rate moved from 1.052 to 1.118 over the period. I checked why: every euro invoice in the dataset settles at exactly its booking rate. Not one cent of realised FX exists, which means the generator implicitly fixes a rate per invoice — economically wrong, internally consistent, and invisible.

**3. The accrual that is a plug.** Account 2020 carries exactly nineteen journal lines — one per month. That is an aggregate estimate, not a goods-received-not-invoiced accrual. A real one is a list of vendors with a reason each.

**4. What is modelled rather than computed.** Employer costs run at exactly 31.200% in every one of nineteen months while headcount grew from fourteen to twenty-five. A blended statutory rate moves with country mix. A constant one is a parameter.

**5. Never performed, no record in any period.** Revenue cut-off testing. Vendor statement reconciliation. Bonus and untaken-leave accrual — and untaken leave is a cash liability on termination in several of these jurisdictions, not a policy. Recovery of hardware from churned club sites, which matters because deployed cameras are assets the company does not physically control.

**6. No close sign-off. Eighteen closed months, no signature on any of them.**

### What I did about it

Two things, and deliberately not a third.

I wrote `package/close_checklist.json` — 37 steps with owners, dependencies, evidence produced, and a per-step `implemented` flag that is **false for all sixteen gaps**. The package ships with its own gap list visible in the artefact. Hiding it would have been easy and would have made the package worse: a finance lead installing this needs to know what it does not do before they trust what it does.

I did not backfill the missing accounting into the generator. Building VAT into the dataset now would take a day and would remove the most instructive thing about this artefact — that a competent automated close, validating 78 out of 78 checks, was missing 7.9% of revenue in tax treatment and nobody noticed until someone asked the right question.

That goes on the Day 9 list as a candidate, not into the generator today.

### One design idea worth keeping

The checklist carries two day columns per step: `manual_day` and `agentic_day`. The close is BD+12 manual, BD+5 agentic.

Three steps have identical values in both columns — the cut-off notice, the payroll input freeze, and the sign-off. Two are deadlines imposed on people outside finance and the third is a human signature. **Nothing an agent does moves any of them**, and they are the boundary of what automation can claim.

One step has `manual_day: "never"`. That is the opportunity register, and it is not a joke — a two-person finance team does not reach it. It is what the recovered days are supposed to buy.

---

## Part 2 — The CFO Chief of Staff

### The insight the agent is built on

Agents compress work. They do not compress the calendar.

The EOR needs payroll inputs five business days before the month it is paying for has ended, whether the close takes twelve days or two. The board meets on a date set six months ago. The VAT return is due twenty calendar days after the quarter. Insurance renews on 1 November.

Two consequences follow, and they are the agent's entire remit.

**The binding constraint moves from throughput to attention.** When the close took twelve days, a missed deadline was a capacity problem and everyone saw it coming. When the close takes two, the deadline arrives while finance is idle, and it is missed through inattention. Inattention is harder to spot and harder to forgive.

**The recovered slack gets taken.** Nobody defends it. Seven days came out of the close; they will be filled by whoever asks loudest, usually with a data request that should have been a self-serve query. If nothing protects that space it is gone in two months and the company has bought speed and spent it on nothing.

### The six rules

The full charter is `package/charters/chief_of_staff.md`. Three of the six are the ones that took thinking.

**Never do the work you are chasing.** If the bank reconciliation is late, this agent says it is late; it does not reconcile the bank. Not a capability limit — the only thing that keeps the agent honest. An agent that can complete the task it is measuring will complete it rather than report it missing, and a task quietly completed by the monitor is a control that has stopped existing.

**Distinguish the deadline you can move from the one you cannot.** Every obligation carries an authority: statutory, contractual, governance, internal. Only internal is negotiable. In CourtIQ's calendar, of fifteen recurring obligations, **four are internal**. Everything else is a wall. An agent that proposes "moving the VAT deadline" has failed at the only judgement it makes.

**Ration escalation, or be ignored.** Never more than three items in a standup. If there are more than three, the fourth is a capacity finding about the function, not a fourth item. An item amber for three weeks is not amber — reclassify it as accepted risk, name who accepted it, and stop mentioning it. Silence is a valid output.

### The autonomy split

This is the only agent in the workforce with a split grant, and the asymmetry is the design.

**L2, autonomous, for notification.** Reminders, status, deadline transitions. The one class of action where being wrong is cheap: an unnecessary reminder costs thirty seconds, a missed statutory deadline costs a penalty and a diligence footnote. Escalate early, accept the false positives.

**L0, draft-only, for anything that changes the calendar.** Moving a date, accepting a risk, marking a step not required. A monitor that can quietly lower the bar it measures against is not a monitor.

> **It may tell anyone anything at any time. It may not change what anyone owes.**

There is no promotion path. There is a demotion trigger: any deadline missed without a prior at-risk flag returns it to L0 for a full cycle and requires a written post-mortem. A monitor that failed to warn has failed at the only thing it does.

### The two artefacts it walks

`finance_calendar.json` — fifteen recurring obligations, each with cadence, anchor, authority, owner, effort in business days, lead time, dependencies, and a plain-language consequence of missing it. Plus four weekly standing reviews, of which the most useful is the renewal watch, because renewal notice windows expire silently and nowhere else looks at them.

`close_checklist.json` — the 37 steps.

`calendar.py` resolves both against a date. Business-day arithmetic with a holiday calendar spanning five jurisdictions, dependency walking, and a latest-safe-start computed backwards from each deadline rather than forwards from today.

---

## Part 3 — What the first run found

Run against the real 18 August 2026 state. The scheduler returned seven items. Under rule 4 the agent escalated three and raised the rest as one finding.

**The structural conflict is the output I did not anticipate and it is the best thing here.**

The Q3 board pack is due Wednesday 2 September, five business days before the 10 September meeting. The August close is due Tuesday 8 September — six business days *after* the pack, and two days before the meeting.

So the September board meeting discusses **July** actuals, eighteen business days stale on the day the pack goes out, alongside a forecast last refreshed in **April**.

Nothing is late. Nobody is behind. The dates simply cannot all hold, and this has been true of every board meeting this year. It is the kind of thing a finance function absorbs as normal and never states out loud, and it took a scheduler walking a dependency graph to make it visible.

The agent's resolution is correct and characteristic: two options, both human decisions, and a refusal to take the third path. *"What I will not do is present the pack as current. That is a representation, and representations are not mine to make."*

The scheduler also surfaced that **the live forecast is four months old** — `plan_apr26_reforecast.csv` is the most recent plan in the dataset, so four rolling forecast cycles have been missed.

### The agent breaking its own rule, and saying so

Rule: produce no financial number. The standup ends:

> *"I have produced no financial number in this standup that I computed myself. The FX figures are the exception and are labelled as such — they exist only because a step that should have produced them does not run, and I judged that reporting 'not performed' without a magnitude would have been read as either alarming or ignorable, and I could not tell which. That judgement is on the edge of my charter and I am flagging it rather than hiding it."*

The FX numbers are $6,499 cumulative and $578 unrealised. Immaterial — **and that is the point.** Nobody knows it is immaterial because nobody computes it. A step whose expected result is nil is still a step, and there are four steps in this checklist with no completion record in any period. Not a nil result. No result.

---

## Sprint impact

Agent count 11 → 12. Two package artefacts and one runnable tool added; nothing in `package/` mentions padel.

The Chief of Staff is cheap to build relative to the others because it computes no financial numbers — dates, dependencies and a rule about when to speak. It is also the agent that most changes what the package *is*: without it this is a faster close, and a faster close is a feature. With it, this is a finance function that knows what it owes and to whom, and that is a different product.

**Carried forward:** the sixteen unimplemented close steps are now a visible list rather than an unexamined absence. VAT is the one worth building — it is 7.9% of revenue and the most credible thing a Series A finance lead would ask about in an interview. Day 9 candidate.
