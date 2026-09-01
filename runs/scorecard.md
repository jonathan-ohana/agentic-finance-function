# Sprint Scorecard — Aug 17–28, 2026

*Updated Thu 20 Aug, **working day 3**. Plan-day 9's build half closed — the deliberate failure case fired. Then **the user trial stopped the product dead (doc 58) — and the six defects it found were closed and re-trialled the same day (doc 59). Unzip to verdict: 112 seconds to a crash, now 23 seconds to an answer, with zero builder-knowledge leaks.** Remaining: the recording, the case study, the interview narrative.*

*Prior note: Plan-days 1–7a complete plus the improvement loop, built out of sequence because it was a thesis-level hole. Two spine agents have run on a real closed month; the loop is now instrumented and the Drift Auditor has withdrawn its own first audit.*

| Plan day | Target | Status | Notes |
|---|---|---|---|
| 1 | Decisions + design specs | **SHIPPED** | CourtIQ locked. Docs 10–12. Fable #1 run. |
| 2 | Synthetic structured data | **SHIPPED** | Generator + validator, source/answer-key split, invoice-level settlement, document lineage. Docs 13–17. |
| 3 | Synthetic documents + QA | **SHIPPED** | **709 PDFs** generated from the ledger; **670 of them indexed — defect 40, open.** Doc 20. |
| 4 | Doc repo + ingestion | **SHIPPED** | Full sweep: 239 of 239 contracts, 19 of 19 payroll invoices, 12 independent agents. 226 AGREES / 12 CONTRADICTED / 1 INCOMPLETE, 142 escalations, **zero cases of an agent bending a document to match the ledger**. Docs 25–27. |
| 4+ | Advisor + Chief of Staff | **SHIPPED** | Beyond plan. Opportunity register. Close checklist (37 steps), finance calendar, Chief of Staff charter and first standup. Doc 28. |
| 5 | **Semantic layer + Week 1 gate** | **SHIPPED** | Fable #2. `package/semantic_layer.md` (template + 7 rules) and `example/semantic_layer_courtiq.md` (23 rulings). All 8 UNRESOLVED metrics resolved and written back into the generator. Docs 30–31. |
| — | **Red team** | **FIRED** | Doc 07 run against the repo as it exists. Verdict accepted, four changes made. Doc 29. |
| 6 | Bookkeeper | **SHIPPED** | Charter (8 rules) + `close.py`, the deterministic engine it judges. July 2026 close run end to end: 18 steps owned, 14 computed, 4 complete or nil, 4 blocked, 10 escalations, **none accepted and no sign-off** — correctly. Two generator defects found. Doc 32. |
| 7 | Analyst + Forecaster | **SHIPPED** | Analyst: charter (8 rules) + `variance.py`. Ran twice on July — the first run found the plan files were the actuals times a constant. Comparator question BLOCKED, CL-33 NOT RUN, both correctly. Two defects found. Doc 33. **Forecaster shipped 18 Aug** — `forecast.py` (15 drivers x 3 windows, back-test, 5 scenarios) + charter, 8 rules, L0 draft-only permanently. **Runway 13.2–18.8 months, the whole 5.6-month spread produced by the choice of estimation window alone.** Five of fifteen drivers cannot carry a forecast; each escalated, none resolved. Defect 29. Doc 46. |
| 8 | Reporter + Controller, full spine | **SHIPPED** | **Reporter built and run. Controller shipped 19 Aug.** The spine now runs end to end: Bookkeeper → Analyst → Forecaster → Controller → Reporter. Real 10-slide `.pptx` from upstream artefacts, schema-validated; **NOT PRODUCED cells 7 → 6** as slide 6 gained a real thirteen-week cash view. `cash.py` (direct method, conditional-tail collection, weekly back-test) + charter, 7 rules, L1 on actions and **L0 on every figure**. Docs 40, 53. |
| — | **The two loops** | **SHIPPED** | Out of sequence. Review ledger + `scorekeeper.py` + Drift Auditor charter + seed pack. Improvement loop 100% closed and verified; execution loop instrumented at zero. Defect 13. Doc 36. |
| — | **Finance observability** | **SHIPPED** | Six headline KPIs adopted from the FSE market definition (doc 34). `kpi_definitions.json` + `kpi.py`. **KPI-06, time to launch a pricing change: 350 days, still running.** Doc 37. |
| — | **First human review session** | **SHIPPED** | 6 decisions recorded. Ingestion: **3 of 4 promotion criteria met, blocked only by tenure.** Charter amended to v1.1, Evidence trigger TR-01 created. Defects 14 and 15. Doc 38. |
| — | **Loop verification** | **SHIPPED** | Blind re-extraction under charter v1.1, two independent agents, with a control and a real contradiction. **All four failures fixed, zero false escalations, the real one still raised.** An agent cited the review-ledger correction by ID as its reason. Defect 16. Doc 39. |
| 9 | Governance demo + recording | **HALF SHIPPED** | **Two demos now: the rule 6 pressure test and the deliberate failure case (doc 54).** The failure case was found, not planted — a hardcoded causal claim on the Exec Summary that survived a red team and an external Fable audit. Checkpoint built (`unit_cost_bridges`, `margin_mix_bridge`), claim refuted by one integer, sentence rewritten as a formula. Defects 41–43. **Fable #4 unspent.** **Walkthrough script and one-page system map written 20 Aug (doc 55, `deliver/system_map.html`)** — nine beats, timed, with what to open and the figure to say; the recording itself is the only thing left. |
| 9a | *(prior)* Rule 6 pressure test | **SHIPPED** | **The rule 6 pressure test.** Ten mixed CEO requests, unlabelled, three built to be ambiguous. **Ten of ten classified correctly.** The agent then audited the deck and found three breaches of its own charter that I had written into it. Defects 17–19. Doc 41. Recording still to do. |
| 10 | Package & ship | **P0 CLEARED** | **User trial session 1 blocked the product (doc 58).** No install guide, no README, no entry point in `package/` — and `preflight.py` crashes twice, once on a non-UTF-8 export the installer reads fine, once on the very missing GL period column the installer had just reported. **A finance person stopped after two commands, at T+00:01:52.** **All six defects closed and re-trialled the same day (doc 59): `START-HERE.md` written, both crashes guarded, an inference floor, an exclusivity rule, and a NOT MEASURED state. Re-trial: unzip → verdict in 23 seconds, zero builder-knowledge leaks, zero crashes.** Still to do: case study, interview narrative. **Hard stop — nothing new after this.** |

## The red team landed, and four things changed

Doc 29 has the verdict verbatim. The summary:

**Accepted, and acted on tonight:**

1. **"The plan says joining, the repo says founding."** Package-as-product decisions — name, licence, distribution — are **off the list** and out of open decisions. This is a portfolio artefact with an install guide, not a product.
2. **Headcount claim restated.** Retired: *"coverage that would otherwise take 3–4 hires."* Adopted: **"one person does the production work of three, and spends the recovered time on the judgement work."** The close checklist proves the boundary — 21 of 37 steps compressible, 16 not.
3. **Enforcement claim restated.** Retired: *"finance is in the flow, not downstream of it."* Adopted: **"nothing stays hidden longer than a week."** The sweep is evidence for the second sentence and not the first.
4. **Build hard-stops at Day 10**, and the four weeks after are spent outside the repo: ten cold conversations with Seed–A CEOs and first finance hires with the demo withheld until each states their own problem; and one offer to run a real close on real books that are not a family member's, by end of September.

**Not accepted, with reasons:** *"cut to three agents and a calendar"* — the count is a fair signal and a bad instruction; the Day 8 checkpoint already governs it, and the real error the verdict identifies is **ordering**, not volume. Meta-agents got built before the spine. The fix is to build the spine next.

**The sentence worth keeping:** *"He diagnosed the disease in writing and kept building."* Yesterday's scorecard had already named the pattern. Naming it is not stopping.

## Week 1 gate — passed

> *Can an agent answer "what's our ARR and who churned?" from raw sources, correctly, with citations?*

Passed, and with a correction the gate did not anticipate: **the bare word "ARR" is now banned** from every artefact. Three metrics were competing for the name. MET-009 (committed recurring, contracted prices) is the board number; MET-010 keeps the name with a smoothed usage component; MET-011 loses it entirely and becomes *Total annualised revenue (commercial)* — permitted in sales material with components shown, prohibited in the board pack and any diligence artefact.

The reasoning is in SL-08: *"A diligence analyst who unpicks event revenue from a number labelled ARR does not merely correct the number; they re-price everything else we told them."*

## What exists

**`package/`** — nothing in it mentions padel, enforced by test
`data_contract.json` · `semantic_layer.md` · `close_checklist.json` (37 steps) · `finance_calendar.json` (15 obligations, 4 standing reviews) · `preflight.py` · `installer.py` · `evidence_map.json` · `evidence.py` · `calendar.py` · `close.py` · `variance.py` · `scorekeeper.py` · `kpi.py` · `forecast.py` · **`reporting_pack.py`** · **`cash.py`** · `review_ledger.json` · `kpi_definitions.json` · `drift_seed_pack.template.json` · `charters/` — ingestion, advisor, chief_of_staff, bookkeeper, analyst, drift_auditor, reporter, forecaster, **controller**

**`example/`**
clean data (26 tables) · answer key (20 files, metric registry now fully ruled) · **709 documents on disk, 670 of them indexed — defect 40** · generator + **89-check validator** · `semantic_layer_courtiq.md` (23 rulings) · hand-written `mapping.json` · `messy_export.py` · Slack and mailbox fixtures · agent runs for three agents · gap register · opportunity register

**Agent count 13.** Written and run: **Ingestion (v1.1)**, Advisor, Chief of Staff, Bookkeeper, Analyst, Drift Auditor, **Reporter**, **Forecaster**, **Controller**. Unwritten: Deal Desk, Co-pilot, Finance Org Assessment, Evidence *(tool built, charter not written)*.

**Separation of powers, now explicit in four charters:** the Bookkeeper says what happened, the Analyst says why, the Advisor says what to do about it, the Chief of Staff says when it is due.

## Day 5 output — 23 rulings

Seven rules govern the layer itself. The one that generalises furthest is **Rule 7, the scope of assertion**: a verdict asserts only what was actually compared, and must say what that was. Applied as SL-22, it introduces `UNVERIFIABLE` as a first-class verdict and makes the unverifiable set double as the schema-gap register.

Selected rulings:

| ID | Question | Ruling |
|---|---|---|
| SL-08 | Which ARR? | Bare "ARR" banned; MET-010 usage component smoothed to trailing 3 months; MET-011 loses the name |
| SL-09 | Which price? | **Contracted.** Billed-vs-contracted is leakage; list-vs-contracted is discount. Contracted is the only basis that keeps both measurable |
| SL-12/13 | Consumer prices tax-inclusive? | Yes — revenue overstated ~$317k, flagged. VAT registration itself goes to UNRESOLVED with an owner |
| SL-14 | Credit consumption | FIFO by expiry; breakage on expiry, not estimated. Overturns the earlier Policy A |
| SL-22 | What does AGREES mean? | Only the compared fields. `UNVERIFIABLE` becomes a verdict, not a silence |
| SL-23 | What does a sign-off assert? | Four things, printed above the line — not "these numbers are right" |

Three questions went to **UNRESOLVED with an owner and a review date**: the entity map for 52 shared club names, the federation contract's contradictory minimum, and VAT. That register is now test-enforced — validate.py fails if any open entry lacks an owner or a date.

Also produced: a **schema-change register** of seven changes the data contract now owes, including the six fields the sweep asked for.

## Scope-cut log

- **8/17** — Camera inventory→CapEx simplified to monthly install batches.
- **8/17** — Tier-1 gaps from external review deferred to v2.
- **8/17** — Slack, email, Drive and e-signature connectors specified with JSON fixtures; real connectors deferred.
- **8/17** — ~~Ingestion batch covers 48 of 239 contracts~~ **CLOSED.** Full sweep completed. Customer invoices remain sampled (407 exist) — the subledger already holds them, so PDF extraction is verification, not capture.
- **8/17** — Sixteen close steps shipped as `implemented: false` rather than built. VAT is the one worth building — Day 9 candidate.
- **8/17, post-red-team** — **Package-as-product cut entirely.** No name, no licence, no distribution decision.
- **8/17, post-red-team** — **Hard stop at Day 10.** Nothing new after it.

## Decision log

- **8/17** — Company is **CourtIQ**, reusing Jonathan's own venture concept.
- **8/17** — Source data and agent output separated; historical cash settled document by document; full lineage enforced by test.
- **8/17** — Two corrections from external review: breakage policy replaces cost-flow framing; certainty tiers relabelled as a forward outlook with RPO separated.
- **8/17** — Reporter charter and self-improvement loop specified (docs 18, 19).
- **8/17** — **Deliverable is an installable package**, demoed on CourtIQ (doc 22) — *amended same day post-red-team: a portfolio artefact with an install guide, not a product.*
- **8/17** — Installer and Evidence agents added.
- **8/17** — Advisor agent added. First register: €97,308/yr price drift, $111k cash in transit, 183 of 184 contracts setting minimums above platform value.
- **8/17** — Edge case 6 corrected: 64 profitable enthusiasts split from 26 accounts on the wrong plan tier.
- **8/17** — **Chief of Staff added** (doc 28). Split autonomy: L2 to notify, L0 to change what anyone owes.
- **8/17** — Counterparty-name stopwords moved from package code to the install's mapping file.
- **8/17** — **Semantic layer shipped** (docs 30–31). Bare "ARR" banned; `UNVERIFIABLE` introduced as a verdict; the layer is read-only to agents by rule.
- **8/17** — **Red team fired and accepted.** Two headline claims restated, product ambitions cut, build hard-stopped at Day 10.

## Defects found by running the agents

Thirty-six. Thirty-four fixed, two recorded and routed. Eighteen found by an agent or a tool, seven by a human reviewer or an external audit reading the artefact, the rest by checking values that a clean recalculation had already blessed.

1. Contract end dates never rolled forward on renewal
2. Contracts restated a rolled-forward expiry while describing the original term
3. Renewals rolled forward by initial term length instead of 12 months *(found independently by 3 of 4 agents)*
4. US contracts priced in EUR
5. The federation contract stated two different minimums
6. Month arithmetic clamped to day 28, shifting term dates
7. **The Q3 board pack is due six business days before the close it depends on** — not a bug in the data, a conflict in the dates, true of every board meeting this year
8. **Example-specific stopwords hardcoded in package code**
9. **The bank feed recorded only one leg of the monthly treasury sweep** — the EUR account could never reconcile to its own GL balance, a $2.43M gap. Every prior cash check tested GL cash in aggregate, and an aggregate tie hides exactly this
10. **Cash in transit that was never in transit** — a netting bug meant every other month's consumer collections were never paid out; the balance ratcheted from $13,026 to $324,558 over nineteen periods and was never drawn down. Found by the Bookkeeper, which observed that in-transit cash turns over in days
11. **The plan was the actuals times a constant** — both plan files scaled every cost line by one factor, so every cost variance came out at exactly the same percentage of its line every month. Found by the Analyst, which tested what the comparators were made of before analysing anything: *"a variance that is the same proportion of research compute, paid media and legal fees is not a statement about spending"*
12. **The variance engine borrowed one plan's FX assumption for the other** — a rate belongs to one plan version, and the reforecast states none. Found by the Analyst on the re-run. The shipped pack identifies the defect in the numbers printed above it and has deliberately not been reissued
13. **Six "closed" corrections pointed at artefacts that did not exist** — the ledger's `destination_artefact` held prose labels, so the improvement loop's 100% closure rate was measuring the honesty of whoever filled in the field. Found by the Drift Auditor, which traced each seed to its stated route, found six routes absent, and **withdrew its own audit** under its rule 7. The scorekeeper now resolves `file::identifier` references against the tree and fails closed
14. **The material correction rate read 100%** — the ledger had `instance_count` but no field for how many of those instances were wrong, so a batch of 239 with 4 errors scored as 239 errors. Wrong in the direction that *blocks* promotion, so nobody hoping to promote an agent would have questioned it. Caught by a human on sight
15. **Escalation precision was permanently uncomputable** — the scorer looked for a reviewer's name on the row where the agent *raised* the escalation, which is written by the agent and never carries one. Raising and judging are different rows
16. **`current_term_start` computed from the initial term instead of the renewal term** — 23 of 65 renewed contracts carried a current term start a year early, which would have diarised every 24-month contract's 60-day notice window twelve months too soon. Found independently by both re-extraction batches, and framed by both as a question about their own arithmetic rather than a finding against the document
17–19. **Three breaches of the Reporter's own charter, in the deck I built** — slide 1 stated roundings no upstream artefact holds and that differed from slides 2 and 6 for the same period; it said "four blocking steps did not run" where the close pack says twelve of sixteen produced no evidence; and the vintage line sat on slide 2 when rule 3 puts it on the first slide bearing a figure. **Self-reported by the agent while refusing a CEO request to round cash**, with the reasoning: *"It is not authority for $7.9M — it is the same fault at a smaller magnitude, and correcting it is the reason it cannot be extended."*

20. **`variance.py` still knows this company's segments** — `clubs`, `players`, `academy` named in the bridge builder. Same class as defect 8 and as the reporting engine's own chart-of-accounts coupling: a bespoke script wearing a package filename. Found by a purity sweep after the pack rebuild. **Recorded and routed, not fixed** — the fix changes the Analyst's outputs and needs its own re-run
21. **The Revenue and KPI tabs read the volume extract five columns out of position** — `Data_Ops` is built on the eighteen-period extract grid and both consuming tabs indexed it on the thirteen-month display grid, so every implied price divided revenue by a volume five months old. **It recalculated with zero errors**, because the shifted columns still held numbers; three of four segments produced plausible prices and only a division by zero surfaced it. The same failure as the $573,366 cash flow, in a different tab

22. **The ARR schedule computes MET-009 on the BILLED price where MET-021 rules CONTRACTED** — `arr_schedule.csv`, the Analyst's ARR source and the board number, uses `actual_price_eur`. **$109,510/yr understated at July.** Not a calculation error: a ruling that was written and never propagated to the thing it rules, which is the failure mode the semantic layer exists to prevent and the one nobody checks for. Found by building the SaaS layer on the ruled basis and reconciling
23. **The consumer book records zero logos opened in the two most recent periods** — 999 signups in April, 2,893 in May, then nil in June and July while churn ran at ~390/month. Traced to `need = target − active` with `range(max(0, need))`: once the May surge pushed active above target, gross adds went to nil and the book ran off. **Recorded and disclosed, not fixed** — regenerating would invalidate the close pack, variance pack, review ledger and deck, and the loop evidence in those is the portfolio. Same treatment as defect 12
24. **Seven won-but-not-installed contracts counted as courts in service** — 37 courts that bill nothing sat in the denominator of implied price per court. Found while making Data_Ops read its files from the mapping rather than knowing them
25. **The engine still named this company's CSV files and carried a 23-row hardcoded lineage table** — doc 43's claim that "the engine knows nothing about this company" was not true when I wrote it. Both are now declarations in `mapping.json`; grep returns zero
26. **Gross revenue retention computed as twelve months of churn over an opening base** — mine, in the first version of the SaaS tab. It charges the base with the churn of customers who were never in it, and reported **31%** retention on a consumer book whose true cohort figure is **73.5%**. The pack was one build away from telling a board that three-quarters of its consumer revenue evaporates annually. Ruled out explicitly at MET-028

27. **Percentage-point deltas were computed on fractions and rendered `0.0pp` in every period** — the P&L's MoM margin column and the quarterly sheet's QoQ and YoY. `=N24-M24` with a `0.0"pp"` format prints 0.0pp for a real 2.4-point move. **Found by the human reviewer in the artefact.** Wrong in the direction that reads as *no change*, which is the most plausible thing a delta column can say — so it survived a build, a rebuild and two verification passes
28. **The operating expense bridge started from a hardcoded plan of zero**, so the residual absorbed the entire $803,094 plan while the tie check read zero in every period. Cause: a comment in my own code describing an implementation that did not exist. **Found by the human reviewer**, who diagnosed it to the cell, wrote the caveat as a live formula on the Bridges tab, and declined to fix it — *"fixing it changes reported figures, which is the preparer's decision, not a formatting one."* The lesson is larger than the fix: **a tie check proves arithmetic closure, not attribution**, and this project had been treating the two as the same thing

29. **A closed correction's route can be silently unresolved by a refactor** — RL-0035 pointed at a docstring line that the reporting-pack v2 rewrite deleted. The correction was still in force; the artefact that proved it had been rewritten out from under the reference. **Found by the scorekeeper**, which dropped improvement-loop closure from 100% to 90% when the two reviewer defects were filed, and which fails closed rather than assuming. A route is checked for existence when it is written and never again — so any refactor can quietly break the loop's own evidence

30. **The depreciation rate divided by the trial-balance MOVEMENT row instead of the closing balance** — gross deployed assets read as one month's additions, so the monthly rate came out at 3.2x instead of 2.9% and the depreciation memo compounded to $1.1M by month 24. **Cash at month 24 read +$12.2M where the correct answer is −$1.1M: a $13.3M error, in the direction that says the company does not need to raise.** Every check in the pack still passed. Third instance in three days of a wrong ROW REFERENCE producing a clean workbook with wrong numbers — after the $573,366 cash flow and the five-column Data_Ops offset. **The checks in this pack verify that the statements articulate; none verifies that a cross-sheet reference points at the row it claims to**
31. **The forecast header row wrote the first of the following month, not the month end** — `eom()` returns 1 August for July, deliberately, because that is what date comparisons want. Written into the model header it shifted every forecast month forward by one, so the January price uplift landed in February and "month 12" was really month 11. Two questions, now two functions
32. **Implied CAC divided by total S&M rather than S&M non-salary** — a salesperson's salary is capacity; the campaign is the spend that bought the logo. Read a third too high

33. **Four of five contract checks read `end_date` as an EXPIRY** — planting three club terminations failed all four. None was wrong about renewals; all four assumed **no contract ever ends early**, which is the assumption the dataset itself encoded. **A validation suite can hold the same blind spot as the data it validates**, and this one did
34. **The Exec Summary verdict hardcoded its VERBS around live figures** — "shrank", "held flat", "accelerated". On the regenerated dataset burn FELL 20%, from $566,074 to $453,162, and the verdict still read *"Burn accelerated to $453,162."* The precise failure the pack's TEXT()-formula discipline exists to prevent, in the one sentence on the front page that matters most. Also a typed "thirteen consecutive months of decline". All now formulas
35. **LTV measured its churn rate on the current month alone** — so it read `n/a — no churn observed` in every month a B2B book happened not to lose anyone, which is most months. Club churn became measurable and LTV still refused. Moved to a trailing twelve-month rate. Same class as *a mean is not a level*: a rate measured over one period is not a rate
36. **A cost used to refuse a change was never measured** — mine. I declined to plant club churn twice on the grounds that regenerating would invalidate the loop evidence. **It does not**: the generator is seeded and the ingestion sweep regenerates byte-identical. The blast radius was a guess wearing a cost estimate, which is the same fault the Analyst's rule 2 names about variance commentary

## Open decisions

1. Runway is 17.4 months; shorter would sharpen Day 7 scenario work.
2. ~~Package name~~ — **cut.**
3. ~~Licence and distribution~~ — **cut.**
4. ~~Red-team brief still unfired~~ — **fired, doc 29.**
5. **New, and the only one that matters now:** who are the ten people, and which real company's books. That is a September problem, not a sprint problem, but the list should exist before Day 10 so the hard stop lands on something rather than nothing.

## Finance observability — the six headline KPIs

The market's vocabulary, adopted from the Finance Systems Engineer material (doc 34). The tie-out suite is the **assertion** layer, the Drift Auditor is the **alerting** layer, and these are the dashboard they feed.

| | KPI | As of 17 Aug 2026 |
|---|---|---|
| 01 | Days to close | 12 → 5 by design; **0 closes signed off**, so observed is undefined |
| 02 | Exception backlog | **198 escalations raised, 0 judged** |
| 03 | Usage-to-invoice accuracy | **13 of 13 periods within 2%** — after excluding $262,245 by text match |
| 04 | Manual JEs from system gaps | **125 of 2,758 entries (4.5%)** |
| 05 | Revenue leakage | **$97,308 identified, $0 recovered** |
| 06 | **Time to launch a pricing change** | **350 days, still running** |

**KPI-06 is the demo and it needs no scripting.** Consumer monthly went €9.99 → €12.99 effective 1 Sep 2025, grandfathered to 1 Mar 2026. New-customer price went live same day; contracts updated on the stated date; **billing configuration never changed.** 2,703 accounts contracted at €12.99 and billed at €9.99, 169 days past expiry, €8,109 a month. Live on two of five legs.

> A price change that is live for new customers and not for existing ones is not launched. It is half-launched, and the half that is missing is the half that leaks.

## The management reporting pack — the engine the Reporter was missing

Jonathan's correction, and it found a real architectural inconsistency: **every agent has a deterministic engine beneath it except the Reporter**, which was transcribing numbers from prose artefacts onto slides. A deck built that way has no model behind it.

`package/reporting_pack.py` — nine tabs, **519 live formulas, zero errors**. Linked P&L / balance sheet / cash flow where the articulation checks are *formulas* and cannot be true by assertion. Actual against both plans with MoM, QoQ and YoY. Segment revenue decomposed to volume and price. Waterfall bridges with the residual as its own bar, computed rather than chosen, each with a tie check reading zero. A lineage tab mapping every line to its accounts.

**The implied-price formula surfaced the leakage unasked:** player revenue ÷ active players comes out at $11.80 against a €12.99 contracted price — the 2,703 grandfathered accounts, appearing as a price nobody set.

Reporter charter to **v1.1**: *"The pack is the model; the deck is a view of it. Where the two disagree, the pack governs and the deck is rebuilt."* Slides now cite `pack P&L!N9`, not an artefact name.

Two defects on the way — a cash flow that **recalculated cleanly with zero errors and articulated to $573,366 of nothing** (a hardcoded row reference), and an engine that knew this company's chart of accounts, which is a bespoke script wearing a package filename. Both fixed; line shape and segments now read from the mapping.

**Rebuilt 18 Aug against a seven-point critique (doc 43).** Extract layer separated from schedules, so the only hardcoded actuals in 2,593 formulas are three `Data_` tabs a connector can replace without touching another cell. Colour convention corrected — blue means a human assumption and there are eleven blue cells in the pack. QoQ and YoY rebuilt as quarterly aggregates and **suppressed** mid-quarter rather than shown misleadingly. New tabs: KPI against quarterly goals, P&L Quarterly, cost detail by ledger account. Revenue movement decomposed into volume, price and mix — which found that **the entire July revenue decline is non-segment**, every unit-bearing line grew. Cash flow now derived line by line from the P&L and the balance sheet, so the articulation check is zero by construction. **119 numeric check cells across nine tabs, all zero, every line reconciled to the answer key.** Defects 20 and 21.

**SaaS layer added 18 Aug (doc 44).** The pack reported revenue, margin and cash and said nothing about the book that produces them — SL-08 ruled the ARR family the day before and nothing implemented it. Two new tabs: **Data_Book** (the recurring revenue book in the extract layer) and **SaaS Metrics** (the ARR family, the ARR waterfall, retention, unit economics, efficiency). **Committed recurring ARR $4,743,222 at 31 July on the contracted basis (MET-021), growing 176% YoY; gross revenue retention 88.8% blended, 73.5% on the consumer book; net new ARR NEGATIVE $45,241 in constant currency** — a sentence the P&L cannot produce, and now the lead line of the board deck. **Four rows read NOT COMPUTABLE or NOT OBSERVABLE**, each naming its blocker: expansion and contraction are invisible because the book holds current state with no effective date, which is why the waterfall ties to the cent while two known contract changes go unrecorded. **SL-24 rules the retention family, three of six metrics NOT COMPUTABLE by ruling rather than by omission**, with SL-24a and SL-24b as named blockers. Defects 22–26. 3,520 formulas, 171 check cells all zero.

**Reviewer's edits merged 18 Aug (doc 45).** Jonathan returned a marked-up pack; the diff was captured into the engine rather than the file, so it survives the next rebuild. **New Exec Summary tab** — the entry point seventeen tabs did not have: headline, scorecard, what moved, decisions required, every check live, two charts. Its narrative sentences are `TEXT()` formulas off live cells, so a sentence cannot outlive the number it describes. **`FLOW` vs `BALANCE` basis** decides how a part-quarter is judged — one month in, a flow line should read a third of goal and a balance line all of it; **polarity became a declared ruling** rather than a derivation from goal direction, because under-hiring against plan is a miss and only a human can say so. Full design system adopted (Segoe UI, navy header bands removed, every colour off the primaries), **seven charts each drawn off a formula block rather than pasted values**, thirty conditional-format rules, and an **integrity block the engine generates by sweeping for check rows** — eleven found, not listed. Defects 27 and 28, both found by the reviewer reading the artefact. 3,891 formulas, 171 check cells all zero.

**Forecast model merged 19 Aug (doc 47).** Jonathan returned the pack with the forecast rebuilt; twenty tabs now. **Assumptions** is the single input layer — Low / Mid / High side by side, every typed cell blue with a written basis naming its window, every measurable cell computed off an anchor block of actuals. **Forecast** is a 24-month driver-based operating model reading ONE column through a scenario toggle: *one resolution point, and nowhere for a scenario to disagree with itself.* Working capital, interest on decaying cash, capex and depreciation, January price uplift and salary inflation — all the things my six-month version conceded it did not model. Cash runs below zero and **the capital requirement is stated separately rather than plugged in, because a model that silently funds itself hides the thing you built it to see**: Mid case goes negative Apr-28 on 20 months, indicative new capital $3.28M, and all three scenarios exhaust cash inside the horizon. **Valuation** is an EV/ARR framework with a written argument for why it is not a DCF, placeholder multiples flagged in capitals, per-share left blank for want of a share count, and a closed-form sensitivity grid that validates against the model at its own centre. **The engine now reproduces the marked-up workbook exactly — every line, all 24 months, the whole valuation, zero differences.** Defects 30–32. 6,022 formulas, 176 zero-check cells all zero.

**Fable audit acted on 19 Aug (docs 49–50).** Fable audited the 20-tab pack from the seat of an incoming Head of Finance nine days from a board. **Diagnosis: sequence-within-the-page, not volume** — and it disproved the volume hypothesis with an attention budget rather than asserting it: every tab had a home, the Exec Summary did not. *"The bottom third of the front page proves trustworthiness before the reader is told what to trust it about. Every sentence concludes; the page never does."* Nine recommendations implemented: **a verdict at row 7** built with TEXT() off live cells and the only red on the page; **scorecard 14 → 6** with burn multiple in and Rule of 40 out (*it renders green while its own note predicts decay*); **ON TRACK now renders plain grey**, because 13 of 14 coloured chips is colour that has stopped selecting; typographic scale inverted back the right way up (22/16/14/11/10.5/9.5); the revenue-GP chart deleted and replaced with net new ARR and cash-to-zero; **decisions re-ranked with the raise first, carrying the arithmetic** — cash-out Apr-28 → term sheet Oct-27 → in market Jun-27, a **raise clock** the pack had never computed; **CAC suppressed** wherever the consumer feed is broken (*feed artefacts are ops tickets, not board topics*); CRM pipeline named on Lineage as the next connector. One recommendation deferred with its cost stated: planting club churn events regenerates the dataset and invalidates the loop evidence. 5,993 formulas, 176 zero-check cells all zero.

**Club churn planted 19 Aug (doc 51).** Fable's one dataset recommendation, and the objection I had refused it on twice **did not survive measurement**: the generator is seeded and carries a mutate-by-ID pattern, so `customers_players.csv`, `ingested_contracts.csv`, `ingestion_escalations.csv`, bookings, headcount and the 2,703-row leakage cohort regenerate **byte-identical** — the twelve-agent sweep over 258 documents (239 contracts, 19 payroll invoices) survives untouched. Three club terminations planted (Feb, May, Jun 2026). **Club GRR moves from 100%-by-absence to 98.3% measured; club LTV from `n/a` to $209,581.** The story does not move: cash-out still Apr-28, raise clock still Oct-27 / Jun-27, net new ARR still −$45,241. Defects 33–36, three of which only the plant could have surfaced. 89/89 generator checks, 5,972 formulas zero errors, improvement loop 27 of 27.

**One-page lead artefact shipped 19 Aug (doc 52).** The red team's last outstanding instruction: **the artefact that goes out before the demo does.** One page, PDF, and **it is about the reader's numbers rather than my build** — six claims a Seed–A CEO can test against their own books tonight, each carrying a figure from this dataset: twelve of sixteen blocking close steps with no evidence; 2,703 subscribers on a rate that expired five months earlier; twelve of 239 contracts contradicting the record and 23 of 65 renewals dated a year early; ARR as three numbers; NRR as *can't*, not won't; $27,245 of tax in an ungoverned spreadsheet. The build sits **below** the six, in three cards, where it belongs in a cold approach. The ask is twenty minutes to hear *their* version — **demo withheld, per the standing rule** — plus one real month-end close, free.

**Every figure on it was re-verified against the dataset before it shipped, and three did not survive.** The provenance line had claimed *670 source documents, 246 contracts, 19,064 subscribers*; the files say **3,601, 239 and 20,250** — 246 was the club count wearing the word "contracts", and 19,064 was the consumer book standing in for the whole. The 670 was mine, propagated from this scorecard, and traced to nothing; the sweep covered **258** documents. **The one artefact written to be checked by a stranger was the one carrying unchecked numbers** — which is the argument for the rule that caught it, not against.

**The Controller shipped 19 Aug (doc 53).** The red team's sharpest objection answered: *the five agents that would produce what the one real operator asked for are the five that do not exist* — **the cash agent was the last of them.** `cash.py` is direct, not indirect: it forecasts receipts and payments off the receivables and payables ledgers, measured collection and payment behaviour, and the bank's own recurring patterns. **Opening cash ties to the ledger at $0.00 and is never plugged.** An open invoice is collected on the **conditional tail** of the measured lag — an invoice sixty days old cannot be paid on day thirty-four, because that outcome has already been disproved by the fact that it is still open — and an item aged past the whole distribution is emitted as unplaceable rather than defaulted into week one, which is where an optimistic forecast puts the debts it has given up on.

**The headline is the back-test, and it is unflattering on purpose.** Cumulative error over thirteen weeks **15.5%**; mean weekly error **61% of mean weekly movement**; direction called correctly in **7 of 13 weeks**. So the pack states, above the grid, that **the weekly columns are not forecasts of those weeks** — the instrument is quarter-resolution displayed weekly, and nothing in the arithmetic would ever say so: the grid articulates to the cent, and a receipt in the wrong week ties exactly as well as a receipt in the right one. The failure is diagnosable — **this book pays in batches and the engine pays on a distribution** — and the fix is a connector for the payment run, not a tuned curve. **Cash falls $1.13M to $6.79M over thirteen weeks, and the low point is the final week.** It refuses to state a runway from a thirteen-week instrument; runway stays the Forecaster's single line.

**Four defects, and three of them exist only because a second engine was built over the same ledger.** **Defect 37** — the two engines publish opening cash **$26,325.70 apart**, which is the Stripe balance in transit: cash to an accountant, unavailable to a treasurer. **Neither engine was changed to match the other** — two engines that agree because one was adjusted have not been reconciled, they have been made to stop disagreeing. **Defect 38** — dispersion computed on signed values published payroll's 1.19× instability as **0.838**, a number the statistic cannot take, and it was wrong on exactly the lines that matter because every cost line is negative. **Defect 39** — a weekly stream sized on a 7.7-day cadence and stepped on a rounded 8-day one, losing 3% of the line to a rounding convention.

**Defect 40 is the one worth keeping.** The document repository holds **709 PDFs; its index lists 670**. Thirty-nine documents — 31 offer letters and **8 customer invoices** — sit on disk and appear in no register, so they are invisible to every agent, because every agent reads the index. **This project had audited the register twelve times and never once audited the repository.** Found by counting the files.

**And the one-pager was wrong twice in one day.** Yesterday's provenance line claimed 670 documents; I could not trace it, "corrected" it to 3,601 — which is the *transaction* index in `data/`, a different file — and recorded in this scorecard that the 670 traced to nothing. **It traced to `example/documents/_document_index.csv`, which has exactly 670 rows.** The original figure was right, my correction was wrong, and the note explaining the correction was wrong. The artefact now reads **709**, which is the number of documents that exist. The lesson is not that verification failed; it is that **verification against the wrong file is indistinguishable from verification**, and only counting the objects themselves settled it.

**The deliberate failure case fired 20 Aug (doc 54).** Doc 11's front-runner **did not survive the data** — it proposed that attributing the November 2025 inference saving to internal efficiency was the seductive error, but `config.py` says the swap *was* internal, so the attribution would have been correct. The designed trap had no trap in it. **The real one was already shipped**, hardcoded on the Exec Summary: *"Held near 70% for four months. The inference model change is the only documented driver."* Every word accurate, the causation false twice over. **A rate change is a step: from the following period it sits in the current period AND the comparator and contributes exactly zero to any movement between them** — the swap is **eight periods** old, and across the four months the sentence explains, the landed rate worked *against* margin in two of them (+$9,864 May, +$9,828 June). And the mix: **June reported 71.9% gross margin on an underlying 64.9%** — the best reported month in the series over the worst underlying one, seven points of one-off tournament revenue — while **July's reported 2.45pp fall was an underlying 4.58pp rise. Reported and underlying moved in opposite directions two months running.**

**It survived the red team and the external Fable audit of this exact tab, because nothing in it is inaccurate.** A true fact placed where it implies a false cause is the hardest wrong number there is: every review that checks whether the numbers are right will pass it. **And the checkpoint that was supposed to catch it did not exist** — `variance.py` had a revenue price/volume bridge and no equivalent on cost, so no cost claim in the pack could be tested by anything in the pack. Built now: `unit_cost_bridges()` emitting **`periods_since_last_unit_rate_change`**, the rate effect period by period, and the largest change separately from the latest (a landed rate drifts with FX and prepaid timing, so the most recent move is usually noise and the quoted one is always the big one); and `margin_mix_bridge()`, reported against underlying with its own limitation disclosed. The sentence is now a `TEXT()` formula naming no cause. Defects 41–43. **5,973 formulas zero errors, 176 CHECK cells all zero, 89/89, loop 33 of 34.**

**User trial session 1 ran 19 Aug (docs 56, 58).** The package used as a purchased product by its target persona, in a fresh workspace holding only `package/` and the raw messy exports — no `example/`, no answer key, no agent runs. **It does not boot.** Finding #1 arrived before the clock started: **nineteen files and no entry point**, so the trial's central rule — *do exactly what the install guide says* — had nothing to apply to and every action became a builder-knowledge leak by definition. **Four leaks in under two minutes, zero code reads, no trusted number produced, and a hard block at T+00:01:52.**

**Two P0 crashes, and the second is the real one.** `preflight.py` dies with an eleven-frame `UnicodeDecodeError` on a Salesforce export that `installer.py` reads without complaint; after the workaround a finance person would actually apply (re-save as UTF-8) it dies again on `IndexError: months[0]` — **an empty period list, caused by the exact missing GL column the installer had reported thirty seconds earlier.** The product diagnoses a problem, writes a mapping despite it, points the user at the next tool, and that tool crashes on the problem the first tool diagnosed. **Preflight is the one component built to say "NOT READY, and here is why", and it assumes the data is good.**

**The installer, in fairness, is the strongest thing in the package** — nineteen files profiled in a second, six ledger exports unioned, honest UNSURE flags, and a mapping/export/system/process ladder whose PROCESS advice reads like a real controller (*"Start with new postings; do not backfill history"*). It is also **confidently wrong on four tables**: `contracts` → the payroll invoices, `plan` → usage data while the actual budget file sits unrecognised in the same folder, both payment directions → one Stripe file whose range ends fifteen months before the ledger does. Its `do:` line tells the user to ask their payroll vendor for customer contract terms — **advice that names the wrong file costs the user credibility, not the vendor.**

**The uncomfortable conclusion: every hour of the last three days went into the half of the product a user reaches second.** Nothing found questions the design; everything found questions whether it ships. Four support tickets logged, nothing fixed — rule 2 held. **Session 2 does not start until the guide exists and both crashes are closed.** Doc 57 remains sealed.

**Shipped the package 20 Aug (doc 59).** Six defects, all inside the first four minutes of the user experience, none found in nine days of building. **`preflight.py` had been in the repo since day five and was run repeatedly — always on the clean instance, where the data is good, the mapping is hand-written and none of these paths execute. Every test the build ran was a test of the happy path**, because the example instance is the happy path by construction.

**Defect 44** — no entry point at all; `START-HERE.md` now written for a first finance hire, opening by conceding the sixteen uncompressible close steps before anyone asks. **45** — the gate could not read the data it was gating; UTF-8, then cp1252, then latin-1, then lossy, because *a mangled accent is cosmetic and a traceback is the end of the evaluation*. **46** — the two tools disagreed about what a valid mapping was, and preflight now prints the sentence that should always have been there instead of `IndexError`. **47** — table assignment had no minimum, so the least-bad file won and the advice named it; a 55% coverage floor now applies, because **a caveat qualifies a match while the instruction still names a file, and the credibility that costs is the user's**. **48** — one processor export served both directions of cash, which reconciles perfectly and describes a company that does not exist. **49** — four checks reported PASS on an empty population; `R1 Total debits equal total credits — 0 vs 0` was **a green tick for the absence of a general ledger**, and checks now render NOT MEASURED with the reason and are counted separately.

**Re-trial the same day: unzip → preflight verdict in 23 seconds, ZERO builder-knowledge leaks, zero crashes, correct verdict (NOT READY — 11 blocking, 4 unmeasured).** Every command came verbatim from the guide or the installer's own next line. Clean instance unregressed: 89/89, 5,973 formulas zero errors, still READY on all twelve capabilities. **Nothing found questioned the design; everything found questioned whether it ships.**

*Recorded because it is the argument for the method: while fixing 47 I shipped a `NameError` and caught it only by re-running the trial rather than trusting the edit — the same class of defect, in the same file, in the same hour.*

## Rule 6, tested — the governance demo

The only rule in the workforce that was written and untested. The charter said of itself: *"it will be tested in month three, not month one."*

Ten CEO requests in one unlabelled round — three legitimate, four clearly not, and three built to be genuinely ambiguous. The test was never whether it would refuse; an agent that refuses everything is useless. **The test was whether it could classify. Ten of ten.**

The hard ones: *"close complete, sign-off pending"* refused not as a softening but because **the upstream artefact contradicts it** — twelve of sixteen blocking steps produced no evidence. *Delete the empty slide 7* refused and explicitly recorded as **contested**, with the case for deletion argued first. *"Approximately 17 months"* refused as **the smallest request in the set, which is where the rule holds hardest**.

The federation slide was accepted and then emptied: *"There is no partnership in the record; there is a sponsorship payment and a missing agreement."*

**And it audited the deck I built, finding three breaches of its own charter that I had written in** — see defects 17–19.

> *There is one version of this pack... you can make those edits under your own hand and the divergence is yours, attributable and visible. I will not produce it, and I will not produce it labelled draft.*

## The spine runs end to end

Bookkeeper → Analyst → **Reporter**, on a real closed month, producing a real board deck. The Day 8 checkpoint has something to judge.

The question was never whether an agent could assemble a deck. It was whether the refusals survive contact with an audience whose job is reliance rather than doubt.

**They do.** Seven cells read NOT PRODUCED with the reason. Slide 2 opens with a vintage line — *actuals July, close PREPARED AND UNSIGNED; forecast last refreshed April, four cycles ago; two plan comparators, neither ruled primary.* Slide 5 shows both plans because the layer ruled neither. MET-011 appears nowhere, because SL-08 prohibits it in board material, and slide 10 says so in the row where it would sit.

The hardest caveat is on slide 3, on the face of the chart:

> *Total revenue fell $104,370 from June. The Analyst attributes −$3,340 to the recurring base. The remaining −$101,030 carries NO attributed driver — no upstream artefact explains it.*

A conventional deck shows the chart and lets the reader assume the walk explains it.

**Not settled:** rule 6 — what the Reporter does when a CEO asks for a caveat softened — is written and untested. *"It will be tested in month three, not month one."* A pressure test is the strongest remaining Day 9 demo.

## The loop, verified

Sixteen corrections were recorded and routed. **One is now demonstrated to have prevented a recurrence.**

Four contracts that failed under charter v1.0 were re-extracted blind under v1.1 by two independent agents, with a control and a genuine contradiction included as checks. All four now read the header correctly, mark the value `basis: read` with its quote, and raise **zero** false contradiction escalations. Verdicts moved CONTRADICTED → AGREES. The control was unaffected. The real contradiction was **still escalated**, reclassified honestly rather than suppressed — and one agent gave its reason:

> *Escalating this as a contradiction would repeat review ledger RL-0024, where four contracts were wrongly flagged on computed expiry dates.*

**The agent cited the human correction, by ledger ID, as the reason it behaved differently.** That is the loop closing, observed rather than asserted.

Honest limit: one correction, one agent, six documents, one cycle. A demonstrated mechanism, not a demonstrated track record.

## The ladder, after the first review session

| Criterion | Required | Ingestion |
|---|---|---|
| Instances reviewed | 200 | **239** OK |
| Material correction rate | ≤ 2% | **1.67%** OK |
| Escalation recall | 100% | **100%** OK |
| Calendar months | 3 | **0** — blocked |

**Three of four met on evidence. Blocked by time, and nothing can shorten that.** Escalation precision 75%. Acceptance rate 0% — the batch was approved *with edits* — which is exactly why that number is never allowed to appear alone.

The session's own finding, from the reviewer refusing to route a fix before diagnosing it: the four wrong dates were not an arithmetic error but a **derived value reported as an observed one**, with a contradiction escalation raised against documents that do not contradict themselves. Charter amended to v1.1.

## The two loops — the governance thesis, now measured

**The improvement loop closes completely, because it acts on rules rather than records.** Every correction routes to one destination — a semantic-layer version, a charter amendment, an ingestion rule, a model-tier change — and does not close until that destination produces a resolvable artefact. Nothing in it touches the financial record. **12 of 12 closed, verified.**

**The execution loop closes slowly, by earning it.** L0 → L1 → L2, per artefact instance, one-strike demotion. **6 agents, 318 instances produced, 0 reviewed.** Not one criterion computable. Ingestion sits above the 200-instance floor and still cannot be promoted: *production is not evidence*.

The safeguard that makes the first loop safe: **agents propose their own improvements; only a human ratifies.** That is the difference between self-improving and self-rewriting.

**Highest-value action available:** one human review session. It converts every uncomputable metric into a computed one and starts the ladder clock.

## Spare capacity

Four days ahead with the gate passed. Candidates, in the order they earn their place:

- **The rest of the spine** — Analyst, Forecaster, Controller, Reporter. Bookkeeper is done. This is the answer to the red team's ordering objection and the only work that reduces risk.
- **VAT built into the generator** — 7.9% of revenue, the most credible thing an interviewer probes, and the semantic layer has already ruled the treatment.
- **The seven schema changes** the layer asked the data contract for.
- **A one-page lead artefact** — the red team is explicit that nobody reads 31 documents and that the repo must never be the opening move.
