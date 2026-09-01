# 78 — Variance analysis playbook library (v0.2 — red-lined)

*v0.1 drafted 20 Aug 2026 (Fable). v0.2 incorporates Jonathan's red-line of 20 Aug — eleven corrections, logged at the foot of this doc. Sections 3, 4, 5, 9, 10 and the shared method received no red-line: treated as accepted, revisit after the first live month. READY FOR WIRING into the Analyst charter.*

## Shared method (applies to every account)

**Ladder, cheapest evidence first — elimination, not confirmation:** (1) Accrual artifact? — reversal pairs, prior accrual vs landed invoice. (2) Timing? — entry dates, vendor cadence, the account's trend test. (3) Volume/rate? — decompose against the account's declared driver before concluding. (4) One-off? — entry scan: new vendors, odd amounts, memo text. (5) Only survivors may be called run-rate.

**Taxonomy (one tag per variance):** Timing · One-time · Run-rate · Accrual artifact · Volume-driven · Rate-driven · FX. Consequences: Timing nets over the quarter; One-time leaves baselines; Run-rate changes the forecast.

**Narrative rule:** rank materiality × permanence × surprise; top 2–3 as prose; rest to the table. Timing and Accrual-artifact may never lead. "Driven by" requires an entry- or driver-level evidence link; otherwise "coincides with."

**Owner questions:** closed-form, evidence attached, default stated ("no reply by close+2 → treated as timing"), answer recorded as next month's prior.

---

## 1 · T&E (in 7xxx travel / 8xxx)

**Benchmark:** budget per head × **budgeted** headcount — so the total variance decomposes cleanly into a **headcount effect** (actual vs budgeted heads at budget rate) and a **spend-per-head effect** (actual vs budget rate at actual heads). Never benchmark against actual headcount alone: it silently absorbs the headcount variance. **Behavior:** bumpy per person, smoother in aggregate; **event-driven** — conferences and major sales events dominate the bumps, so check the events calendar before calling anything a trend. **Trend test:** trailing-6M CV; <0.15 smooth, >0.3 bumpy/event-driven. **Failure modes:** late expense reports (timing), accrual not released, new-hire ramp misbudgeted, an event moving months. **Depth rule:** **>5% variance** → pull entries; missing regular submitters = timing signal; uniformly lower spend = savings signal; a single event explaining the bump = calendar check. **Owner Qs:** smooth+under → "Real behavior change to carry into forecast, or catch-up coming?" · bumpy+under → "Was [event] moved or cancelled? If moved, which month absorbs it? Default: timing, catch-up expected."

## 2 · Payroll & benefits via EOR (6/7/8xxx salaries; 2030)

**Benchmark:** the employee-level roster — budgeted cost per named current AND planned future employee. The variance then attributes to one of five known drivers: **base salary change · hire timing (early/late vs plan) · attrition · hire-at-a-rate-different-from-budget · accrual/benefits assumptions.** **Behavior:** stepped, moves only on roster and comp events; the largest cost line, so small % = large $. **Failure modes:** **bonus accrual basis** — budget may accrue 100% of planned bonus while actuals accrue 90%; a variance with zero roster movement behind it. **Benefits election (PEPM)** — budget assumes a plan-election mix; actual elections produce a different per-employee-per-month cost. EOR invoice lags start dates ~1 month; one-time fees (termination, onboarding) buried in routine invoices; EUR salaries at moving FX; jurisdiction accruals (13th month, vacation). **Depth rule:** ANY variance not explained by a roster delta → attribute against the five drivers, then read the EOR invoice line by line; never accept "payroll is just up." **Owner Qs (to People/Ops), plain form:** "Payroll came in $X above plan. We matched every person to the plan and the difference isn't headcount. Two checks: (1) did anyone's pay or bonus accrual change this month? (2) does the EOR invoice include any one-off charge — an exit payment, a signing cost? Default: hold as unexplained accrual, escalated to close."

## 3 · GPU inference compute (5010) — the margin driver *(v0.1 — accepted)*

**Benchmark:** matches analysed × contracted rate per match; NEVER prior month alone. **Behavior:** volume-driven with strong seasonality (summer peak); rate is a step function that moves only on vendor/model changes. **Trend test:** decompose rate × volume FIRST — check `periods_since_last_unit_rate_change` before any narrative (the Day-9 failure lives here). **Failure modes:** prepaid-commitment amortisation masking cash rate; utilisation drift on the commitment (~71%); free/tournament matches consuming paid inference; misattributing rate steps to "efficiency." **Depth rule:** always split rate/volume/mix vs both benchmark and prior month; tie volume to Data_Ops match counts. **Owner Qs (to CTO):** "Volume +18% vs revenue-driving matches +9% — what's the non-billable inference (testing, tournaments, free tier)? Default: flag margin-dilutive usage, no forecast change."

## 4 · Storage, egress & hosting (5020/5030) *(v0.1 — accepted)*

**Benchmark:** per-match storage cost trailing-3M × current matches; hosting = near-fixed floor + small variable. **Behavior:** storage follows CUMULATIVE video retained with ~1-month lag; egress follows viewing, not capture. **Failure modes:** retention-policy changes (step), tier-pricing cliffs, one-time backfills/migrations. **Depth rule:** separate the growing-archive component from the activity component before judging. **Owner Qs:** "Storage/match up 12% with no rate change — retention or resolution change? Default: one-time until a second month confirms run-rate."

## 5 · Paid acquisition (7xxx non-salary, ~$294k/mo) *(v0.1 — accepted)*

**Benchmark:** plan by channel; sanity-check vs signups but never "explain" via CAC alone. **Behavior:** lumpy by design — campaigns, seasonality, app-store billing thresholds; spend is DISCRETIONARY, so variance is often a decision, not an anomaly. **Failure modes:** platform threshold billing, agency fees mixed with media, events prepaid months ahead, spend continuing against a broken acquisition feed (SL-24b). **Depth rule:** split media / agency / events / app-store fees before analysing; match campaign dates to entry dates. **Owner Qs (to Growth):** "Spend at plan while recorded signups were nil — paused, or running against a broken feed? Default: escalate to the feed-defect register, not the forecast."

## 6 · Professional fees & outside services (8xxx)

**Not one class — four sub-classes, each with its own benchmark and behavior:**

- **Temps/contractors:** can be RECURRING — benchmark like a headcount line (rate × utilisation vs plan), not like project spend.
- **Consulting:** project-based and bumpy, correlated to **milestones** — benchmark against the project/milestone schedule; a variance is a milestone moving, hit early, or missed.
- **Accounting:** SEASONAL — audit, annual close, tax deadlines; the spike belongs in the calendar, not the surprise column.
- **Legal:** unpredictable, litigation especially — which is the argument for **negotiated flat-rate arrangements with firms**; where a flat rate exists, benchmark against it and treat any excess as scope change requiring explanation.

**Failure modes:** unaccrued WIP (bills arrive quarters late), matter-level creep, deal/fundraise costs needing separate treatment. **Depth rule:** every entry **>$5k or >5% of the line** gets matter/project identification; maintain a rolling known-matters list as the accrual basis. **Owner Qs:** "Two invoices from [firm], no matter reference — which project, is more coming, and is this inside the flat-fee arrangement? Default: accrue at invoice level, matter unknown flagged."

## 7 · Software & tooling (6xxx tooling / 8xxx software)

**Benchmark:** the **subscription schedule** (vendor × seats × rate × renewal date) — and tie license counts to the **hiring plan**: more people generally means more licenses, EXCEPT tiered contracts priced "up to X employees," which carry headroom — growth inside the tier is free and must not be forecast as cost growth. **Behavior:** stepped on seats and tiers; renewals land in single months. **Failure modes:** **missed prepaid entry** — above ~$50k annual contract value the amount should spread over 12 months; if budget assumed the spread and the actual hit one month (or vice versa), the variance is an accounting-treatment artifact, not spend. Auto-renewal uplifts; duplicate tools; seats not reclaimed after departures. **Depth rule:** new vendor name → immediate schedule add + owner; contracts >$50k → verify prepaid treatment matches budget's assumption before analysing anything. **Owner Qs (reframed to renewal cost):** "[Vendor] renews [month] at +$X vs current — **is that uplift in the budget?** If not: absorb within your envelope, negotiate, or flag for reforecast — which? Default: flagged as unbudgeted run-rate pending your call."

## 8 · Camera depreciation & installation (5040/5045)

**Two components, opposite treatments.** The **rate** is deterministic — the depreciation schedule; a variance at constant install volume is a DATA-INTEGRITY signal (missed batch transfer, schedule error, unrecorded disposal), never a business story. The **volume** is a business story: installs follow club openings, so depreciation and installation cost vs BUDGET legitimately vary with **expansion pace** — installs ahead of plan is real news (growth, and future COGS), behind plan likewise. **Depth rule:** first split schedule-rate vs install-volume; rate variance → reconcile to 1500/1590 as a close item; volume variance → narrate as expansion pace, tied to club openings in Data_Ops. **Owner Qs (to Field Ops):** rate side → "Installs recorded 10, installation cost implies ~16 — batches transferred late? Default: escalate to Bookkeeper." · volume side → "Install pace is 20% ahead of plan — does the pipeline support holding this rate (with the COGS that follows), or is this a pull-forward?"

## 9 · Payment processing fees (5050) *(v0.1 — accepted)*

**Benchmark:** blended expected rate × card-collected revenue — pure rate × volume × MIX. **Behavior:** tracks collections, not revenue; card-vs-invoice mix does most of the moving. **Failure modes:** processor rate changes, cross-border surcharges, chargeback spikes, annual-prepay months inflating collections. **Depth rule:** compute effective rate (fees ÷ card collections) monthly; investigate the RATE, not the dollars. **Owner Qs:** rarely needed; rate move >10bps → "processor pricing notice? Default: rate-driven run-rate, update driver."

## 10 · EOR fees, insurance & G&A admin (8xxx) *(v0.1 — accepted)*

**Benchmark:** EOR fee = per-head rate × EU headcount; insurance = policy schedule; bank fees = activity + FX spread. **Behavior:** per-head lines step with headcount; insurance annual with mid-year true-ups; bank fees FX-sensitive. **Failure modes:** EOR rate tiers, unaccrued insurance true-ups, FX spread widening on EUR payroll funding. **Depth rule:** per-head lines reconcile to roster; insurance → policy schedule first. **Owner Qs:** "EOR fee per head rose €12 — tier change or rate increase? Default: rate-driven, check contract before forecast update."

---

## Red-line correction log (v0.1 → v0.2) — review-ledger entries

| # | Playbook | Correction | Root cause |
|---|---|---|---|
| 1 | T&E benchmark | Budget/head × BUDGETED headcount, preserving headcount-vs-rate decomposition (draft used actual HC, absorbing the volume effect) | definition — design error |
| 2 | T&E depth | Threshold 30% → **5%** | calibration |
| 3 | T&E behavior | Bumpy = event-driven (conferences, sales events); calendar check added | missing driver |
| 4 | Payroll benchmark | Employee-level roster incl. future hires; five named drivers (salary change, hire timing, attrition, off-budget hire rate, accrual basis) | definition — enrichment |
| 5 | Payroll failure modes | **Bonus accrual basis** (100% plan vs 90% actual) and **benefits PEPM election mix** added — variances with zero roster movement | missing drivers |
| 6 | Payroll owner Q | Rewritten in plain language ("I don't understand the question") | process — question clarity standard |
| 7 | Prof fees | Split into four sub-classes (temps recurring / consulting milestone-driven / accounting seasonal / legal unpredictable → flat-fee mitigation) | definition — design error (one class treated uniformly) |
| 8 | Prof fees depth | Threshold: $5k **or 5%** | calibration |
| 9 | Software | "Register" → "subscription schedule" (US usage); license counts tied to hiring plan; tiered-contract headroom noted | vocabulary + missing driver |
| 10 | Software failure modes | Missed prepaid entry (>$50k annual → 12-month spread); treatment-vs-budget mismatch is an artifact, not spend | missing failure mode |
| 11 | Software owner Q | Reframed to renewal cost: uplift budgeted? absorb / negotiate / reforecast | process — decision-forcing question |
| 12 | Depreciation | Rate deterministic BUT volume is a business story (install pace = expansion pace); draft's "never narrate" rule was too absolute | definition — design error |

## Wiring instructions (cheap-model session)

1. Merge this v0.2 into the Analyst charter as a retrievable library (one lookup per account class before analysis).
2. Build TWO gold exemplars from a real closed month (trace → classified table → story → owner questions); Jonathan reviews both; they enter the charter as worked examples.
3. Add scorecard line: classification accuracy vs sealed-month answer key.
4. Future edits route via the review ledger → playbook version bump. Sections marked *(v0.1 — accepted)* get priority re-review after the first live month.

---

## Wiring status — which corrections are enforced in code

See `agentic-fpa/79-playbook-wiring.md` for the line-by-line map of red-line item → engine test. Corrections 1, 4, 5, 7, 8, 10 and 12 change how `tools/drivers.py` computes a decomposition and are enforced. Corrections 2 and 8 were already the calibration in force. Corrections 3, 6, 9 and 11 are process and vocabulary standards with no computable test; they bind the Analyst's writing, not the engine's arithmetic.
