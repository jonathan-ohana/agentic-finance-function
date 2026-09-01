# Semantic Layer — CourtIQ instance

**Instance of** `package/semantic_layer.md` v1.0 · **Owner** Head of Finance · **Ruled** 2026-08-18 · **Effective** period 2026-08 unless stated
**Status** 20 ruled, 3 unresolved · every ruling below cites its forcing evidence

This file resolves the fourteen questions raised by the contract sweep of all 239 club contracts (`ingestion_escalations.csv`), the close-coverage audit (doc 28, `close_checklist.json`), and the eight metrics flagged `UNRESOLVED — Day 5` in `metric_registry.csv`. Agents read this file; no agent writes it (template Rule 6).

---

## A. Identity — what we are counting

### SL-01 · What identifies a customer

**Kind** DEF · **Status** RULED (entity map UNRESOLVED as SL-01a) · **v1.0** · effective 2026-08

**The case.** `customers_clubs.csv` holds 246 club records. 52 club names are shared across 2–5 records each — Padel House Bordeaux appears four times, Padel House Madrid, Racket Center Valencia, Padel Indoor Braga, Set Point Lyon and Padel Indoor Valencia three times each. The contracts name the client by trading name only, with no registration number, address, or parent key. `club_name` reads like a key and is not one.

**The answers.** (a) A name identifies a customer — simple, and demonstrably false 52 times over. (b) The agreement identifies the customer — correct for billing, but then "customers" equals "contracts" and every retention metric is a contract-survival metric. (c) The legal entity identifies the customer — correct, and not derivable from any field we hold.

**The ruling.** No single unit. Three units, each named, and every per-customer metric must state which it uses:
- **Billing unit** = the agreement (`club_id` / contract). Invoicing, minimums, shortfall tests, and dunning run at this grain and nowhere else.
- **Operating unit** = the site. Interim proxy: one `club_id` = one site, unless SL-01a resolves a pair into one site.
- **Counting unit** for logo count, churn, NRR, and concentration = the legal entity. Until SL-01a delivers an entity key, these metrics are computed on sites **and say so**, with the standing disclosure: *"customer counts are site counts; entity-level counts are lower by an unknown amount bounded by the 52 shared-name groups."*

`club_name` is a display label. No agent may join, aggregate, or deduplicate on it. The failure this prevents: a cohort analysis that merges two unrelated Valencia clubs, or splits one Madrid operator into three customers, and does either silently.

**What it costs.** NRR and churn are wrong at the entity level until SL-01a lands — an expansion at a second site of an existing operator currently reads as a new logo. We accept overstated logo count over silently merged records, because the overstatement is disclosed and the merge would not be.

**Revisit when.** SL-01a resolves; or any new contract arrives without an entity identifier — at which point intake, not finance, has the defect.

**SL-01a (UNRESOLVED).** Entity map for the 52 shared-name groups. *Blocker:* facts we do not hold — which names are multi-site operators, which are re-contracted single sites. *Resolving owner:* commercial team, with the account managers. *Interim treatment:* as ruled above. *Review* 2026-09-30. The five pairs escalated by ingestion (Racket Center Valencia CLB-0073/0085, Sport Club Madrid CLB-0086/+, Set Point Valencia CLB-0104/0110, Padel Arena Madrid CLB-0098/0124, Padel Indoor Valencia CLB-0226/0232, and the three-way Padel Zone Madrid CLB-0193/0201/0212) go first.

### SL-02 · Two concurrent agreements, one counterparty, no supersession

**Kind** DEF · **Status** RULED · **v1.0** · effective 2026-08

**The case.** Set Point Valencia holds CLB-0104 (effective 2025-07-04, 8 courts, EUR 10,300 minimum) and CLB-0110 (effective 2025-07-15, 4 courts, EUR 5,000 minimum), eleven days apart, overlapping terms, neither referencing the other. Padel Indoor Valencia holds CLB-0226 and CLB-0232 nine days apart. Neither document contains supersession, novation, or amendment language.

**The answers.** (a) The later agreement supersedes — treat the earlier as dead, one ARR line. Plausible commercially; extinguishes EUR 10,300 of contracted minimum by inference. (b) Both are live — two sites or a deliberate second agreement; two ARR lines, both minimums bite.

**The ruling.** **Both agreements are live until a signed instrument or the counterparty says otherwise.** Both bill, both count in committed revenue and ARR, both minimums are tested. For counting-unit metrics they are one customer once SL-01a confirms one entity. Every such pair carries a flag in the committed-revenue lineage naming the double-count risk and its amount.

**Why.** The asymmetry of errors. If we double-count and the truth is supersession, we overstate committed revenue by a disclosed, flagged amount and the error dies the day commercial answers. If we extinguish by inference and the truth is two sites, we have stopped invoicing a live contract and waived a minimum nobody agreed to waive — an error that loses real money and surfaces, if ever, as a customer noticing they stopped being billed. The ledger must never extinguish an obligation on inference; that is a human decision with a signature on it.

**What it costs.** Committed recurring revenue may be overstated by up to the sum of the flagged smaller agreements (currently the five pairs above). The amount is disclosed on MET-009 and MET-024 lineage until each pair resolves.

**Revisit when.** Any pair resolves; or the count of unresolved pairs grows, which is a contracting-process defect to escalate, not a definitions problem.

### SL-03 · Renewal state and the notice window

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08

**The case.** CLB-0113 expired 2026-08-18 — today — with its 60-day non-renewal notice deadline passed on 2026-06-19 and the ledger still showing `renewals_to_date = 0`: the contract has, as a matter of law, either auto-renewed or terminated, and the ledger records neither. Ten further contracts in sweep 5 have lapsed notice windows with unexpired terms. Separately, every renewed 24- or 36-month contract in the book shows an end date advanced by the *initial term* instead of the twelve months clause 1 actually grants (CLB-0046, CLB-0014, CLB-0028, CLB-0022, CLB-0017) — the ledger shows zero renewals recorded correctly anywhere.

**The ruling.**
1. **The renewal notice deadline is a contractual calendar obligation.** Every active contract's deadline (expiry minus notice days) enters `finance_calendar.json` with authority `contractual`. The Chief of Staff's renewal watch owns it. Passing a notice deadline is a *decision* — renew by default or serve notice — and a decision requires that someone was told the date existed.
2. **The ledger end date rolls the day after an unexercised deadline**, not at expiry. Once notice can no longer be served, renewal is certain and committed revenue must reflect it; waiting until expiry understates backlog by up to the notice period on every contract.
3. **The roll is +12 months** — the renewal period per clause 1 — never `+term_months`. The renewal period becomes a stored field (schema register). The five contracts carrying the 24-month-advance defect are corrected under the SL-05 precedence rule, and the population is swept for the pattern.
4. CLB-0113 and CLB-0030 are recorded as renewed to 2027, effective their anniversary dates, today.

**What it costs.** Committed revenue now includes contracts a customer might still dispute renewing (notice served but not recorded reaches us late). Accepted: the contract says what it says, and a late-arriving notice is an exception to process, not a reason to hold the whole book at understatement.

**Revisit when.** Any counterparty disputes an auto-renewal we recorded; or e-signature/notice tracking gives us actual notice events to consume.

---

## B. Fields — what a value may claim

### SL-04 · What `billing_frequency` means

**Kind** DEF · **Status** RULED · **v1.0** · effective 2026-08

**The case.** Every one of the 239 contracts bills twice, in opposite directions: platform fees in advance (annually in some, quarterly in others — clause 6) and overage quarterly in arrears (clause 4, all contracts). The ledger's single `billing_frequency` holds the platform-fee leg in every case and has no room for the other. As the sweep put it: for contracts marked `annual_prepay`, a quarterly in-arrears billing obligation exists that the ledger does not show.

**The answers.** (a) The field means "the contract's cadence" — false for 239 of 239 contracts. (b) The field means the platform-fee (advance) leg only, and the arrears leg lives elsewhere.

**The ruling.** `billing_frequency` is defined as **the platform-fee cadence, direction: in advance.** Nothing else. Two fields join the contract record (schema register): `platform_fee_cadence` (value + direction, migrating the old field) and `overage_cadence` (value + direction; currently "quarterly, arrears" for the whole book — a template constant today, a field tomorrow, because template constants are what change without telling anyone). Ingestion already extracts both; the ledger now has somewhere to put them.

**Prohibition.** No cash forecast, deferred-revenue schedule, unbilled-receivable computation, or dunning rule may consume `billing_frequency` as if it described the whole contract. Deferred revenue arises from the advance leg; unbilled receivable from the arrears leg; a model driven off one field treats 100% of contract value as prepaid and misses the accrued asset entirely — which is precisely what the current dataset does.

**What it costs.** Every consumer of the old field must be found and re-pointed; until the schema lands, the interim treatment is that agents computing cash or deferred revenue read overage cadence from `ingested_contracts.csv`, with lineage saying so.

**Revisit when.** Any contract's overage cadence deviates from quarterly-arrears — the day the constant becomes a variable is the day this ruling earns its keep.

### SL-05 · When a document contradicts itself

**Kind** DEF · **Status** RULED (one instance UNRESOLVED as SL-05a) · **v1.0** · effective 2026-08

**The case.** Three shapes, all real. (1) Header term tables contradict clause 1 on renewed contracts — "expires 2028 (renewed 1x)" where clause 1's twelve-month renewals give 2027 (CLB-0046, CLB-0014, CLB-0028, CLB-0022, CLB-0017); the ledger adopted the header every time. (2) CLB-0239: special condition S1 states a EUR 96,000 minimum invoiced in advance; standard clause 3 states EUR 40,000 with an arrears shortfall; S3 uses express "notwithstanding clause 6" language, S1 uses none. Also S4 says 90 days' notice where clause 1 says 60. (3) Six contracts whose clause 3 says "no minimum" carry clause 7 boilerplate referencing "any minimum shortfall" on termination (ruled separately, SL-07).

**The ruling — three rules, in order.**
1. **The operative clause governs over the header.** Cover tables and header summaries are derived text — somebody's arithmetic about the clauses, not the agreement itself. Where they disagree, the ledger carries the clause reading, at reduced confidence, and the contradiction is logged. This resolves shape (1): the five contracts' end dates are corrected to clause-1 arithmetic, and the renewal-recording process that generated the pattern is the defect to fix.
2. **A special condition overrides a standard clause only where it says so.** S3's "notwithstanding" language governs payment terms (Net 60 stands). S1 carries no override language against clause 3's EUR 40,000, so finance cannot rule which minimum governs — that is a legal reading with EUR 56,000 per contract year on it. It goes to SL-05a.
3. **For deadlines, the conservative reading acts.** Where two readings imply different action dates, the calendar carries the *earlier* deadline: CLB-0239's notice window is computed at 90 days, because serving notice 30 days early under the 60-day reading costs nothing and missing it under the 90-day reading forfeits the option. Money follows evidence; deadlines follow caution.

**SL-05a (UNRESOLVED).** CLB-0239 minimum: EUR 96,000 (S1) or EUR 40,000 (clause 3). *Blocker:* legal reading. *Owner:* external counsel via Head of Finance. *Interim treatment:* the ledger continues at 40,000 — the basis the customer has actually been billed on, because invoicing an additional EUR 56,000 without a settled reading manufactures a dispute with the largest club in the batch — and MET-024 committed revenue carries a flagged range of +56,000/year. *Review* 2026-09-15.

**What it costs.** Rule 1 assumes headers are wrong and clauses right; if a header ever reflects a genuine side agreement, we under-record until the amendment surfaces. Accepted: an unrecorded side agreement is a document-management failure that no precedence rule can absorb safely.

**Revisit when.** Legal returns on SL-05a; or the contract template is fixed so headers are generated from clauses, at which point rule 1 becomes a consistency check instead of a tiebreaker.

### SL-06 · Absence, zero, and unknown

**Kind** DEF · **Status** RULED · **v1.0** · effective 2026-08

**The case.** Roughly forty contracts across the sweeps state "No minimum commitment. No annual minimum applies to this Agreement." The ledger records `annual_minimum_eur = 0` for every one — indistinguishable from a minimum that was never captured, and countable, summable, and filterable as if it were a number. Ingestion has been emitting `annual_minimum_status = asserted_none` with nowhere for it to land. Compounding it: eleven-plus USD-denominated contracts (CLB-0136 USD 10,000; CLB-0199 USD 12,500; others) carry unconverted USD values in the EUR-named field.

**The ruling.** Three facts, three encodings, per the data contract's convention (empty means unknown, never a placeholder):
- **Asserted absence** — companion field `annual_minimum_status = asserted_none`, value field empty. There is no minimum and no shortfall test exists for this contract.
- **Stated value** — `annual_minimum_status = stated`, value populated, **and a currency column beside it**. `annual_minimum_eur` is renamed `annual_minimum` + `annual_minimum_currency` (schema register); a field name is not metadata, and this one has been lying about eleven contracts. Until the rename, no agent may sum the column without joining the contract currency and converting.
- **Unknown** — status empty, value empty. This is an extraction gap and escalates; it is never zero.

Zero is banned as an encoding of absence. A true zero minimum, should one ever be written, is a `stated` value of 0 — a test that always passes, which is a different fact from no test.

**What it costs.** Every query in circulation that filters `annual_minimum_eur > 0` must be rewritten. Cheap, once, against the alternative: a genuinely missing minimum that can never again be detected.

**Revisit when.** Never expected to reverse; extend the tri-state pattern to the next field that collapses absence into a value (the sweep nominates `countersigned_date` next).

### SL-07 · "No minimum" versus the termination-shortfall boilerplate

**Kind** DEF · **Status** RULED · **v1.0** · effective 2026-08

**The case.** In at least fifteen contracts (six in sweep 1, nine in sweep 6), clause 3 asserts no annual minimum while clause 7 requires, on termination, payment of "any minimum shortfall calculated on a pro rata basis." The document does not say which governs.

**The answers.** (a) Clause 7 creates an enforceable termination charge — with no stated amount, on a contract that defines no minimum to calculate from. (b) Clause 7 is dead boilerplate, unconformed to the no-minimum variant of the template.

**The ruling.** **Clause 3 governs. No shortfall receivable, contingent asset, or committed-revenue amount is ever recognised from clause 7 on a no-minimum contract.** The clause fails the computability test twice over: there is no minimum to pro-rate and no amount to state. A definition that cannot be computed is a wish, and a receivable that cannot be computed is not even that. Legal is asked to conform the template so the contradiction stops shipping.

**What it costs.** If a court ever reads clause 7 as enforceable, we will have foregone termination charges we never billed. Sized at nil to date — no no-minimum contract has terminated.

**Revisit when.** Any no-minimum contract terminates (the question becomes live, escalate before settlement); or legal opines either way.

---

## C. Revenue — what counts, at what price, when

### SL-08 · The ARR family *(resolves MET-010, MET-011)*

**Kind** DEF · **Status** RULED · **v2.0 of MET-010/011** · effective 2026-08 · comparability: **Restate** (all periods presented, from `arr_schedule.csv` inputs)

**The case.** The registry carries three ARRs. MET-009 (contracted recurring, ruled) is $1.0M growing to $1.3M+ across the dataset. MET-010 adds current-month overage annualised (`4030 × 12`): overage is seasonal and lumpy — the schedule shows months of $0 against months of $75k of annualised usage — so the metric whipsaws with no change in the business. MET-011 adds trailing-twelve-month tournament revenue (`TTM 4040`) and calls the result ARR: one-off event revenue inside a metric whose name promises recurrence.

**The ruling.**
- **The bare word "ARR" is banned** from every artefact. Every use cites a registry ID.
- **MET-009, Committed recurring ARR**, stands as ruled: contracted recurring only, at actual contracted prices. This is the board and investor number.
- **MET-010, ARR including usage run-rate**, v2.0: the usage component is the **trailing three-month average of 4030, annualised** — not the current month × 12. A single month of a seasonal series times twelve is a coin flip wearing a formula. Cost of the smoothing: genuine inflections appear two months late; that is what MET-009's movement analysis is for.
- **MET-011 is stripped of the name.** Renamed **Total annualised revenue (commercial)** — MET-010 plus TTM event revenue — permitted in sales and partnership material with its components shown, **prohibited** in the board pack, investor updates, and any diligence artefact. A diligence analyst who unpicks event revenue from a number labelled ARR does not merely correct the number; they re-price everything else we told them.

**Revisit when.** Overage minimums convert usage into contracted amounts (moves it into MET-009); or event revenue becomes genuinely recurring under contract, in which case it earns its way in by the definition, not the label.

### SL-09 · Price basis for recurring metrics *(resolves MET-021)*

**Kind** DEF · **Status** RULED · **v1.0** · effective 2025-02 (ratifies existing practice)

**The case.** `customers_players.csv` carries three prices per player: `list_price_eur` (12.99), `contracted_price_eur`, and `actual_price_eur` — what billing actually charges. They diverge: a legacy cohort's grandfathered 9.99 expired 2026-03-01 and billing was never updated, so dozens of players are contracted at 12.99 and billed at 9.99, €3.00/month of leakage each (`pricing_configuration_drift.csv`).

**The answers.** List price (overstates — discount cohorts are real commitments at real prices); billed price (imports billing bugs into the definition of revenue); contracted price.

**The ruling.** **ARR uses contracted price** — what the customer has agreed to pay, per the current governing document or plan terms. The contracted-vs-billed gap is **leakage**: a quantified Advisor finding with `pricing_configuration_drift.csv` as standing lineage, fixed in the billing system, never absorbed into the metric. The contracted-vs-list gap is **discount**: disclosed in cohort analysis, not hidden by defining it away.

**Why.** Each candidate basis makes a different error invisible. Contracted price is the only basis under which both the discounting decision and the billing defect stay measurable, because it sits between them.

**What it costs.** ARR exceeds the cash run-rate by current drift. Disclosed monthly beside MET-009 until drift is zero.

**Revisit when.** Drift is fixed and stays at zero for two quarters — the disclosure can then retire; the definition does not change.

### SL-10 · Constant currency *(resolves MET-012)*

**Kind** DEF · **Status** RULED · **v1.0** · effective 2025-02

**The case.** 810 of 869 invoices are euro-denominated; reporting is USD; EUR/USD moved from 1.052 to 1.118 across the dataset. MET-012's draft formula said "EUR base × 1.052" without saying what 1.052 was or when it stops being the rate.

**The ruling.** Constant-currency figures translate all periods at **the plan rate — the rate the board plan for the fiscal year was struck at** (FY26: 1.052, per `plan_fy26_board.csv` assumptions). Fixed for the entire plan year; re-set once when the next plan is approved; never re-picked mid-year, never chosen per report. Both sides of any growth comparison use the same rate — a "constant currency" comparison at two rates is the ordinary kind with extra steps. Constant-currency numbers never appear without the as-reported number beside them.

**What it costs.** As the spot rate drifts from 1.052, the constant-currency figure diverges from economic reality by design; that divergence *is* the FX effect being isolated. The cost is a rate that is arbitrary by mid-year; the alternative — a rate someone picks each month — is a lever, and levers get pulled.

**Revisit when.** FY27 plan approval (mechanical re-set); or reporting currency changes.

### SL-11 · Minimum shortfall: revenue, and whose line

**Kind** DEF · **Status** RULED · **v1.0** · effective 2026-08 · comparability: **Restate** revenue-by-stream for periods presented (totals unchanged)

**The case.** Shortfall billing is running at $262,245, and 91 of the 184 minimum-bearing clubs were shortfall-billed. This is not an edge case; it is half the committed book paying for usage that did not happen.

**The answers.** (a) Fold it into platform subscription revenue (4020) — it is the minimum being enforced, part of the committed fee. (b) Fold it into usage revenue (4030) — it prices the same unit. (c) Its own line.

**The ruling.** **Its own line: account 4032, Minimum shortfall revenue** (schema register). Recognised as it accrues over the contract year per the monthly CL-13 assessment — the shortfall becomes both probable and computable progressively, not suddenly at the anniversary — and billed at contract-year end.

**Why.** Merging it anywhere destroys the one signal it carries. Inside 4030, usage economics look healthier than they are and the per-match figures (MET-018 divides by matches analysed) silently improve as clubs use the product *less*. Inside 4020, the committed base looks like willing subscription. On its own line, the number says what it is: 49% of the minimum-bearing book is committed above its realistic usage, which is either a pricing miscalibration or a sales-incentive artefact, and either way a decision — the Advisor's register, not the ledger, is where it goes next.

**What it costs.** A restatement of stream-level history and one more line to explain. Cheap against the alternative, which is a revenue mix that looks like product engagement and is actually its absence.

**Revisit when.** Shortfall falls below 10% of club revenue for two consecutive quarters — at that point it is noise and may be folded into 4020 under a v2.0 with a Restate decision.

### SL-12 · Consumer prices are tax-inclusive *(with SL-13)*

**Kind** DEF · **Status** RULED · **v2.0 of MET-001 measurement for consumer streams** · effective 2026-08 · comparability: **Restate all periods presented**, executed when SL-13 confirms rates and registration state

**The case.** €12.99 is what a player pays. Twelve months of consumer revenue: $1,828,527. If the price is tax-inclusive, roughly $317,000 of that — 7.9% of total revenue — is VAT collected and booked as revenue, against a liability never recognised.

**The answers.** (a) Prices are exclusive; €12.99 is net. (b) Prices are inclusive; €12.99 is gross.

**The ruling.** **Inclusive.** EU consumer-protection law requires B2C advertised prices to include VAT; €12.99 is the gross amount in every jurisdiction we sell to, and the checkout flow adds nothing. Consumer revenue = collected amount ÷ (1 + standard rate of the subscriber's country): ES 21%, FR 20%, PT 23%, IT 22%. The measurement rule is ruled and computable today from `customers_players.csv.country`; the *postings* — liability accounts, filings, the restatement itself — land with SL-13, because booking a liability to a registration state we have not confirmed manufactures precision. Until then, every consumer-revenue figure carries the flag: *"gross of VAT, overstated ~7.9% at total-revenue level; see SL-13."*

**Why ruled now rather than held with SL-13.** The inclusivity question is answerable and the overstatement is the single largest known misstatement in the ledger. Leaving the measurement ruling inside the tax UNRESOLVED would let the biggest number hide behind the hardest process.

**What it costs.** Revenue, gross margin, and every growth rate over consumer streams restate downward ~7.9% of total. It costs a hard conversation once, versus the same conversation in a data room with a penalty attached.

**Revisit when.** Never on inclusivity; rates table maintained per SL-13.

### SL-13 · VAT treatments

**Kind** DEF+POL · **Status** UNRESOLVED · owner Head of Finance + external VAT advisor · review 2026-09-30

**The forcing case.** One product, three treatments, none represented. (1) Domestic Spanish supply — Spanish VAT at 21%. (2) Cross-border B2B — club contracts in FR/PT/IT/US: intra-EU reverse charge (zero-rated to us, customer self-accounts, invoice must say so; ours don't) and a US question of its own. (3) B2C cross-border — players in FR/PT/IT under One-Stop-Shop, output VAT at destination rates through a single quarterly OSS return. No invoice carries tax; no account in the chart of accounts holds it. And the Evidence agent's sweep found `2025 VAT returns summary` — a spreadsheet outside every governed system, netting $27,245 payable for 2025, no 2026 equivalent — which means filings may exist that the ledger has never heard of. That is worse than an omission, because it looks like a process.

**What blocks resolution.** Facts, not judgement: registration status per jurisdiction, whether OSS registration exists, whether the 2025 filings were made and paid, US nexus analysis. None of this is in any system an agent reads. **A treatment that cannot be computed from the data is a wish** — this entry stays UNRESOLVED rather than pretending, and the pretence it refuses is specific: an agent-invented VAT schedule would net confidently to a number, and confident wrong tax is strictly worse than absent tax, because absent tax still looks like a gap.

**Interim treatment (binding on all agents).**
- No agent computes, nets, accrues, or files VAT. Any tax-shaped number an agent encounters (including the found spreadsheet) is evidence to escalate, never input to consume.
- Every invoice and consumer receipt is treated as tax-status-unknown; SL-12's disclosure rides on every consumer-revenue figure.
- The Chief of Staff carries VAT/OSS filing deadlines as **statutory** calendar obligations regardless of this entry's state. The tax authority is not waiting for our schema.
- Escalation standing per the four-line format: WHAT — VAT position, all jurisdictions, WHO — Head of Finance with external advisor, WHEN — before 2026-09-30, IF NOT — accreting liability ~7.9% of consumer revenue plus penalties, surfacing in diligence.

**Schema requested.** `tax_amount` and `tax_treatment` on `ar_invoices`; accounts 2070 VAT output / 2075 VAT input / 2078 OSS payable; jurisdiction registration register in `document_index`.

### SL-14 · Credit pack recognition *(resolves MET-023)*

**Kind** DEF (lot rule) + POL (breakage) · **Status** RULED · **v1.0** · effective 2026-08 · comparability: **Restate** (breakage recognised to date reverses into deferred)

**The case.** Clubs prepay for credits in lots at different prices — CLB-0018 bought at €0.72/credit and €0.95/credit within a fortnight — with twelve-month expiry per lot. Consumption draws from a pooled balance. Which lot's price is recognised per credit consumed, and when is unredeemed value (breakage) released? `credit_recognition_methods.csv` shows the ledger currently releasing breakage proportionally as credits burn (Policy A), €222–€1,570/month recognised ahead of expiry, on the rationale that "redemption behaviour is predictable."

**The ruling — two parts.**
1. **Lot pricing: FIFO by expiry date** (equal to purchase order here, since expiry = purchase + 12 months). Each credit consumed relieves the earliest-expiring lot at that lot's per-credit price. Weighted average is rejected because it dissolves the lot structure the expiry mechanics depend on — when a lot expires you must know what that lot's unredeemed credits are worth, and an averaged pool cannot say. LIFO is rejected without discussion; it matches nothing about how entitlement works.
2. **Breakage: recognised on expiry only (Policy B), overturning current ledger practice.** Proportional release is the better answer *when the breakage estimate is supportable* — and ours is not. We have nineteen months of history, growing cohorts, and not one full annual cycle of stabilised behaviour; "predictable" is asserted, not demonstrated. Until the estimate earns support, breakage waits for the fact.

**What it costs.** Revenue recognised to date under Policy A reverses into deferred revenue (the cumulative `difference_eur` column of `credit_recognition_methods.csv`), and future revenue arrives later and lumpier — expiry-month spikes instead of a smooth accrual. That lumpiness is honest: it is when the entitlement actually dies.

**Revisit when.** 24 months of completed expiry cohorts exist and redemption rates are stable within a stated band — then Policy A returns as a v2.0 proposal with the cohort evidence attached.

### SL-15 · Expected revenue tier *(resolves MET-026)*

**Kind** DEF · **Status** RULED · **v1.0** · effective 2025-02

**The case.** The revenue-certainty tiers separate cash-certain, contracted, and expected amounts. Tier 3 — usage and credit consumption above minimums — needs a stated forecast basis or it is a mood.

**The ruling.** Tier-3 expected revenue = trailing-twelve-month 4030 plus 4035, explicitly labelled an assumption, with the `forecast_confidence` column bound to history length (below 12 months of usage history the label is Low, and the tier is presented as such). **Prohibition:** tier 3 is never summed with tiers 1–2 into a single unlabelled "revenue" figure. A certainty tiering that gets re-aggregated has communicated nothing and laundered an assumption into a fact on the way through.

**Revisit when.** Usage minimums or committed consumption contracts move amounts from tier 3 to tier 2 — the definition holds; the amounts migrate.

---

## D–E. Cost boundaries, estimates, thresholds

### SL-16 · The compute boundary: COGS or R&D *(resolves MET-019)*

**Kind** DEF · **Status** RULED · **v1.0** · effective 2025-02 (ratifies split; rules the edge)

**The case.** The same GPU pipeline serves paying customers and the ML team. 5010 (COGS, inference) versus 6020 (R&D, research compute) needs a boundary that survives the hard case: re-processing historical matches to evaluate a new model runs customer data through production infrastructure and delivers nothing to anyone.

**The ruling.** The boundary is the **deliverable**, not the infrastructure: *a run whose output is delivered to a customer is COGS; every other run is R&D.* Applied to the edges: live match analysis — COGS. Training, experimentation, internal benchmarks and evaluation runs on historical footage — R&D, whatever hardware they share. Re-processing a customer's history because a shipped model upgrade re-delivers improved output to that customer — COGS, because the customer receives the result. The tag travels with the workload (job-level attribution in the compute logs), not with the cluster.

**Why.** Any infrastructure-based rule reclassifies costs whenever the platform team moves workloads, which hands gross margin to a deployment decision. The deliverable test is stable under refactoring and auditable from job metadata.

**What it costs.** Job-level tagging discipline from the ML team, permanently. **Revisit when** re-processing-as-delivery exceeds 10% of inference spend — at that scale it deserves its own account, not a bigger bucket.

### SL-17 · Customer Success allocation *(resolves MET-020)*

**Kind** DEF · **Status** RULED · **v1.0** · effective 2025-02 (ratifies, with conditions)

**The case.** 35% of Customer Success payroll sits in COGS (5060) as support cost; 65% in S&M. The percentage predates anyone measuring anything.

**The ruling.** 35% stands for v1.0, with its basis written down for the first time: management estimate of CS time on retained-customer support (COGS) versus onboarding, expansion, and renewal work (S&M). Conditions: the estimate is **re-measured by a time study within twelve months** and annually thereafter; a measured movement beyond ±5 points forces a version change with a Restate decision; the basis line appears in the metric lineage. An allocation with no basis is a plug wearing a percentage, and a plug that moves gross margin is a plug in the board deck.

**Revisit when.** The time study lands; or CS headcount doubles (mix shifts invalidate old measurement).

### SL-18 · Expected credit loss *(implements CL-16)*

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08

**The case.** 393 of 760 collections in the period settled late, averaging fifteen days past due. Account 1150 (allowance for doubtful accounts) exists and has never been posted to. There is ageing and no provision — an assertion about receivable value that nobody has actually made.

**The answers.** (a) No provision: there is no observed default history — every late invoice has eventually paid — so any rate is invented. (b) A provision matrix with modest rates: expected loss does not wait for the first loss, and a book of small-business counterparties paying fifteen days late on average is not a zero-loss book, it is a book whose first loss hasn't landed yet.

**The ruling.** Matrix, posted monthly to 1150 per CL-16, by ageing bucket at rates set as a floor judgement — current 0.3%, 1–30 days 1%, 31–60 days 3%, 61–90 days 10%, over 90 days 30% — stated openly as judgement benchmarked on comparable SMB receivables books, **not** derived from our own loss history, because we have none. The basis column in the provision schedule says exactly that. Delay is not loss, and the matrix does not pretend the 393 late payers are defaulting; it prices the tail the delay implies.

**What it costs.** A first-month catch-up charge against a receivables book that has so far always paid, disclosed as policy adoption, not deterioration. **Revisit** quarterly against actual write-offs; rates re-set annually or on the first real default, whichever comes first.

### SL-19 · Bonus accrual basis *(implements CL-25)*

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08

**The ruling.** Accrue at **expected attainment**, assessed semi-annually by management; **default to 100% of target until the first assessment exists**; never accrue below contractually guaranteed amounts. Target-basis was the alternative — simpler, and it hard-codes a fiction in any year attainment diverges, delivering the difference as a Q4 surprise in whichever direction nobody planned. Changes in expected attainment apply prospectively (this is a POL; no restatement). The accrual has never been posted in eighteen closed months; the first posting is a catch-up, disclosed.

**Revisit when.** A bonus plan changes shape (commission-like plans accrue on the driver, not on attainment estimates).

### SL-20 · Untaken leave, by jurisdiction *(implements CL-25)*

**Kind** DEF (jurisdictional facts) + POL (where law is silent) · **Status** RULED · **v1.0** · effective 2026-08

**The case.** Headcount sits in Spain (Madrid, Barcelona), France (Paris), Portugal (Lisbon), Italy (Milan), and the US (Austin, New York, remote). In the EU jurisdictions, untaken statutory leave is a cash liability on termination as a matter of law. In the US it depends on state and on our policy. No leave accrual has ever been posted.

**The ruling.**

| Jurisdiction | Untaken leave is | Treatment |
|---|---|---|
| ES, FR, PT, IT | A liability — law, not our choice | Accrue monthly: untaken days × daily cost including employer burden, from EOR leave balances |
| US — NY | Payable on termination only if policy provides | Policy set below |
| US — TX, remote | Policy-driven | Policy set below |

**Policy (US):** PTO does not pay out on termination, wherever that is lawful, and the written HR policy must say so — the accounting position is only as good as the policy document behind it. Therefore no US leave accrual, and this line is the exemplar the template promised: the EU rows are definitions we do not get to choose; the US row is a choice, changeable prospectively, that changes no past number.

**What it costs.** EOR leave-balance data becomes a close input (schema register); the first EU accrual is a catch-up. **Revisit when** headcount enters a new jurisdiction — the table gets a row before the first hire's first close, not after.

### SL-21 · Materiality, written down *(implements the CL-20 judgement, and others)*

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08

**The case.** Annual insurance and annual software subscriptions are expensed as paid — "a materiality judgement nobody has written down" (CL-20). Flux review, adjustment posting, and vendor-statement scope all run on thresholds that exist only as habits.

**The ruling.** Derived from roughly 0.5% of TTM revenue and reviewed annually:

| Threshold | Amount | Meaning |
|---|---|---|
| Individual adjustment | $2,500 | Below this, an identified adjustment may be waived — logged, never silently dropped |
| Aggregate waived per period | $15,000 | Waivers stop when the pile reaches this; the pile is on the sign-off |
| Flux explanation | greater of $10,000 or 15% of the line | CL-31 explains every movement above; below is noise by policy, not by fatigue |
| Capitalise / spread | $5,000 and benefit spanning >2 periods | Annual insurance and software now spread; the CL-20 habit is reversed above this line |
| Vendor statement scope (CL-21) | vendors >$10,000/period | The reconciliation population is now defined |

A waived item is a decision with a record; the aggregate of waived items appears on the close sign-off, because ten immaterial items in the same direction are one material item wearing camouflage.

**Revisit when.** Revenue doubles, or an auditor sets planning materiality that should supersede these.

---

## F. The vocabulary of assertion

### SL-22 · What a verdict asserts *(template Rule 7, applied)*

**Kind** DEF · **Status** RULED · **v1.0** · effective 2026-08

**The case.** The sharpest finding in the sweep, verbatim in spirit: *an AGREES verdict on these records means the document agrees with the five ledger fields that exist — not that the price is confirmed.* The charter names six material terms: price, quantity, term dates, minimum, billing cadence, payment terms. The club ledger stores no field for unit price, payment terms, overage cadence, included allowance, or notice period. Every AGREES verdict issued over this book asserted less than every reader assumed, and a mispriced contract would have surfaced not as a contradiction but as nothing.

**The ruling.** Effective immediately, for every reconciliation in the workforce:
- Every verdict carries its **compared-field list**. A verdict without one is invalid output and is treated as not run.
- Every material term absent from one side is listed under **`UNVERIFIABLE`** — a first-class verdict, never an omission. For club contracts today: verifiable = {term dates, quantity, minimum (with SL-06 status), platform-fee cadence, currency}; unverifiable = {unit price, payment terms, overage rate and cadence, included allowance, renewal notice period} — until the schema register lands, at which point the sets are re-drawn and this entry is versioned.
- **No consumer, human or agent, may cite a verdict beyond its list.** The sentence "the ledger agrees with the contract" is permitted only when the list covers all six material terms; otherwise the required sentence is "the ledger agrees on the terms it stores; it cannot check price, payment terms, or overage, and here is what that leaves exposed."
- The `UNVERIFIABLE` set doubles as the standing schema-gap register: every field on it is a term a counterparty could change tomorrow without any system noticing, which is the strongest possible priority signal for the data contract.

**Why this generalises.** This is not a rule about contracts. It is a rule about the grammar of agent output: an assertion's scope is the intersection of what both sides could hold, and any wider reading is manufactured by the reader. Writing the scope into the assertion is the only defence, because readers cannot be fixed.

**What it costs.** Verdicts get longer and reconciliation reports less reassuring. That is the reassurance being repriced to what it was actually worth.

**Revisit when.** Schema changes move fields between sets — mechanical re-versioning, each time.

### SL-23 · What the close sign-off asserts *(implements CL-34)*

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08

**The case.** Eighteen closed months, no signature on any of them. And the honest obstacle: the signer computed none of it — agents did — so what could a signature possibly mean that is neither a lie ("I verified these numbers") nor a formality (a name on a page)?

**The ruling.** The sign-off (CL-34, human, never an agent) asserts exactly four things, printed above the signature line:

1. **Every blocking step ran** and produced its evidence — or a documented nil. A nil result is a completed step; a skipped step is not a nil result, and this signature is the only place in the financial statements where that difference is visible.
2. **Every open exception was reviewed**, and each was accepted or actioned **by a named person** — including the aggregate of materiality waivers under SL-21.
3. **The open items carried into next period are listed here**, and the signer accepts the carry knowingly.
4. **Deviations from this semantic layer are listed here**, including every number computed under an UNRESOLVED entry's interim treatment, by entry ID.

And it asserts nothing else. Explicitly not: that the signer recomputed anything; that the numbers contain no error. The signature is the transfer of responsibility from a process to a person — the person attests to the process and to the exceptions, because that is what a person reviewing an agentic close can honestly attest to, and an attestation calibrated to what is honest is the only kind that will keep being made. Demanding more produces either refusal or ritual, and a control that is a ritual is a control that has stopped existing.

**What it costs.** The sign-off document grows a page of lists. Those lists are the close's memory; without them, month twelve inherits month one's accepted risks with nobody left who accepted them.

**Revisit when.** An auditor or board requires a different attestation form — theirs supersedes, and this entry versions to match.

---

## Registers

### UNRESOLVED register

| ID | Question | Interim treatment | Owner | Review |
|---|---|---|---|---|
| SL-01a | Entity map for 52 shared-name groups | Count sites, disclose the band | Commercial | 2026-09-30 |
| SL-05a | CLB-0239 minimum: EUR 96,000 or 40,000 | Ledger at 40,000; +56,000/yr flagged on MET-024 | External counsel | 2026-09-15 |
| SL-13 | VAT: registration, OSS, US nexus, 2025 filings | No agent touches tax; deadlines statutory; SL-12 flag on consumer revenue | Head of Finance + advisor | 2026-09-30 |

Any entry past review escalates via the Chief of Staff as an overdue statutory-class obligation. Any entry older than two closes appears by name in the reporting pack.

### Schema-change register

| Requested by | Change |
|---|---|
| SL-03 | `renewal_period_months` and `renewal_notice_days` on contracts; notice deadlines into `finance_calendar.json` |
| SL-04 | `platform_fee_cadence` (+direction), `overage_cadence` (+direction); retire bare `billing_frequency` |
| SL-06 | `annual_minimum` + `annual_minimum_currency` + `annual_minimum_status`; retire `annual_minimum_eur` |
| SL-11 | Account 4032, Minimum shortfall revenue |
| SL-13 | `tax_amount`, `tax_treatment` on `ar_invoices`; accounts 2070/2075/2078; registration register |
| SL-20 | EOR leave balances as a monthly close input |
| SL-22 | Unit price, payment terms, included allowance, overage rate, notice period on the contract record — the entire `UNVERIFIABLE` set |
| SL-24 | Effective-dated change history on the subscription record (quantity, price, effective date); a segment and acquisition/retention dimension on S&M |

---

### SL-27 · Payment processor fees, and where they clear *(implements CL-38, rules MET-001)*

**Kind** DEF + POL · **Status** RULED · **v1.0** · effective 2026-08 · comparability: **Restate** (balance sheet only; the P&L is unaffected)

**The case.** The consumer book settles through a payment processor. The processor charges the customer the gross amount, deducts its fee, and remits the balance in a batched payout — so the money that reaches the bank is never the money the customer paid, and the difference is a real cost of collecting.

The ledger currently books the fee as a monthly bulk accrual, `Dr COGS — payment processing fees / Cr Accounts payable`, and records the payout as the **gross** clearing balance moving into the bank. Both halves are internally consistent and both are wrong about the world: the processor is never invoiced and never paid, so the payable is never settled. **$77,931 at 31 July 2026** — 9% of the accounts payable balance — sits against a counterparty who will never send a bill. Fees run **2.52% of gross billings through the processor** ($83,727 on $3.33m), which is large enough to move gross margin.

**The candidate answers.** Net the fee against revenue (recognise 12.66 on a 12.99 charge); book the fee to payables and settle it (what the ledger does, minus the settlement); clear the fee through the processor clearing account.

**The ruling.**

- **Revenue is recognised gross of processor fees.** The customer's promised consideration is the full charge. The processor is not the customer and its fee is not a discount granted to the customer, so under IFRS 15 and ASC 606 the fee is a cost of collecting rather than a reduction of the transaction price. Netting leaves net income unchanged and understates both revenue and cost — which silently corrupts gross margin, MET-009, ARPU and every per-customer metric while leaving the bottom line looking correct. **That is precisely why it survives: the P&L is fine.**
- **The fee clears through the processor clearing account (1020), never through payables.** A processor settles itself by deduction. A payable represents an obligation that will be discharged by payment, and this one never will be; recording it as one puts a permanent, growing, unclearable balance into the AP ageing.
- **Three entries, in this order:** charge captured — `Dr 1020 / Cr deferred revenue or revenue`, gross; fee incurred at capture — `Dr 5050 / Cr 1020`; payout received — `Dr bank / Cr 1020`, **net**.
- **Revenue and bank receipts are not expected to agree, and the bridge is a named artefact.** Gross charges less refunds and chargebacks less processor fees less charges captured but not yet paid out, plus payouts of prior-period charges, equals bank credits. That bridge is CL-38 and it is blocking.
- **The accumulated $77,931 is reclassified** from accounts payable to the clearing account. Balance-sheet restatement only; no period's reported profit changes.

**Why.** Each wrong answer hides a different thing. Netting hides the cost and the revenue together, so no ratio built on either is trustworthy. Payables hides the fact that nothing will ever be paid, so the AP ageing degrades a little every month and the reconciliation that would catch it does not exist. The clearing account is the only treatment under which the gap between what the customer paid and what the bank received is a number somebody has to explain.

**What it costs.** A close step that did not exist, run per payout rather than per month, and one restatement of the payables balance. The gross-versus-net question also has to be asked of every future settlement counterparty — app stores, marketplaces, embedded finance — because each one settles net and each one will arrive with the same error attached.

**Revisit when.** A processor changes to invoiced billing rather than deduction — in which case the fee genuinely is a payable, and this entry versions rather than being overridden case by case.

### SL-28 · Which file is the answer *(implements CL-01, governs every ingested role)*

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08 · comparability: **Prospective**, except where an adopted restatement moves a reported figure, which restates

**The case.** Every export folder holds them. `General Ledger 2026Q2.CSV` beside `General Ledger 2026Q2 FINAL.CSV`. `FY26 Budget v7 FINAL (2).csv`. Three headcount trackers with three dates in the name. The installer's first rule decided by **table type** — transactional tables union, everything else is a version, plans keep all — which is a guess about the files made without reading them. It handles two situations and silently mishandles two more.

**The distinction that matters: this is four problems wearing one costume.**

| | |
|---|---|
| **Fragments** | Slices of one population — a ledger exported one quarter per file. Not versions. Union them, and prove it: disjoint keys, contiguous coverage. The two failure modes are overlap, which double-counts, and a gap, which understates. Both are testable. |
| **Restatement** | The same population exported again. The later file governs — but **if two exports of one period disagree, that is a finding, not a preference.** Compute the difference, disclose it, then adopt. |
| **Coexisting** | Both remain true and which governs depends on the question — a board plan and a reforecast. Never supersede. This entry names which version governs which artefact, per artefact, because the board pack and the cash forecast may legitimately answer to different plans (SL-08). |
| **Snapshots** | Photographs of something that changes — a headcount tracker exported monthly. October's file is not a correction of September's. **Read the version governing the period being reported, not the newest.** Reporting June off the newest roster is wrong in a way that never raises an error. |

**The ruling.**

- **Coverage decides what is a fragment; only files covering the same ground can be versions of each other.** Classification runs period-first: bucket by period coverage, union across buckets, and resolve versions only inside a bucket. A role can be both at once — six clean quarters and one restated quarter — and the verdict says so.
- **Four measurements settle the case**: key overlap, period coverage, row equality on shared keys, column shape. Each of the four situations has its own signature.
- **The machine classifies. The machine does not choose.** Where the signature is unambiguous it acts and discloses, per rule 1 of the Systems Engineer charter. Where it is ambiguous it asks exactly one question — **and the question carries the diff**: *"1,168 of 1,170 shared rows are identical; 2 differ and the value moves by $2,500. Correction, or a different scenario?"* Someone asked *which file is right* guesses; someone shown the two rows answers.
- **Never union files whose keys overlap.** Overlapping keys with differing values is a restatement or a coexisting version, never a fragment. A silent union of overlapping keys is the worst outcome available, because nothing downstream notices.
- **The filename is a hint and never evidence.** Ranked: an export stamp inside the file, then modification time, then filename convention, then listing order. *FINAL (2) v3* correlates with recency; it does not establish it.
- **Retain everything, adopt one, log which.** Every adoption is a review-ledger entry naming what was adopted, what was shelved and on what evidence. Nothing is deleted, so the diff can be re-run when someone asks why July moved.
- **A version choice that moves a reported number is a ruling, not a setting**, and carries a comparability note here.
- **Refuse rather than pick.** Where no ruling names the governing version, the dependent output does not run — which OUT-13 already requires of variance analysis.

**Why.** The alternative rules all fail the same way. Deciding by table type is a guess made without reading the files. Newest-wins deletes evidence and hides restatements. Asking the user for every folder is the tool performing diligence rather than doing it. Measuring first is the only rule under which *the tool found something* is a possible outcome.

**What it costs.** A comparison pass over every duplicated role at install, and one question in the genuinely ambiguous case. On the demonstration folder that is eight ledger files: seven quarters unioned to a contiguous nineteen-month coverage, and one restated quarter caught — 2 rows differing by $2,500, 3 rows re-coded out of `8030` into `8040`, disclosed rather than absorbed.

**Revisit when.** A source system starts stamping its exports with a generation timestamp, which promotes the recency evidence a rank and removes most of the ambiguity this entry exists to handle.

### SL-30 · Internal-use software: what is an asset, and where the amortisation goes *(ASC 350-40, IAS 38)*

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08 · comparability: **Restates** — every prior period moves, on the P&L and on the balance sheet

**The case.** Engineering payroll was expensed in full to R&D. Nothing in the ledger recognised that a material part of it builds durable features the platform then uses to deliver the service for years. Two things followed: **cost of revenue was understated**, because the asset that delivers the service was not being consumed anywhere in the accounts; and **R&D was overstated**, because it carried the cost of building things that are not research.

**The classification, and it is not the obvious one.** This is a hosted service the customer never takes possession of, so the software is **internal-use software under ASC 350-40** — not software to be sold, leased or marketed under ASC 985-20, and not a research cost. Under IFRS the same spend is development cost under IAS 38 once the six criteria are met. The two frameworks agree on the outcome here and differ on the trigger, which is worth knowing before anybody asks.

**The ruling.**

1. **Only the application development stage is capitalised.** Three stages, and the middle one is the only asset: *preliminary project* — scoping, evaluating alternatives, selecting a design — is expensed; *application development* — coding, configuration, testing, installation — is capitalised; *post-implementation* — training, maintenance, bug fixes, production support — is expensed. Capitalisation stops when the asset is **ready for its intended use**, not when the team stops working on it.
2. **Not all of a person's month qualifies.** Standups, planning, interviews, on-call and production support are not development. The capitalisable share is agreed per person per project between engineering and finance, recorded in the allocation, and is a **judgement on the face of the artefact** — never a plug and never a company-wide percentage.
3. **The rate is the fully charged cost of the person doing the work** — base plus the employer burden that goes with their contract. Base pay alone understates the asset by the burden, which here is 31.2% on an EOR contract and 11.8% on US payroll.
4. **The amortisation is a cost of revenue, not an operating expense.** The asset is what delivers the service. Putting it in R&D would flatter gross margin by the same amount every month and put the cost of delivery in a line nobody reads as delivery.
5. **Amortisation begins in the month the asset is placed in service** and runs straight-line over the useful life. A project in development is an asset earning nothing, and that is disclosed rather than smoothed.
6. **The useful life is set per project and carried on the register, not applied as a policy.** A ranking model is superseded faster than a booking engine: 24 months on IUS-003, 48 on IUS-002, 36 on the other two. One number applied to all four is a policy standing in for an estimate, and it is a misstatement the moment two projects obviously differ.
7. **The capitalisation credit goes against the expense line it came from**, so R&D salaries carry the net. It is expense that became an asset, not new spend, and a cash flow statement that shows it as investing must show the same amount inside operating.

**Why.** A SaaS company that expenses all engineering reports a gross margin that has never been charged for the thing delivering the service, and an R&D line that mixes building with maintaining. Both numbers are used — gross margin by every investor, R&D by every board — and both are wrong in the same direction at the same time.

**What it costs.** A judgement per person per project that nobody can audit from a system, because no system holds it. Mitigated three ways: the allocation is an exported file with a stage on every row, so a post-implementation line is visible without opening the schedule; the schedule reconciles to the asset and the charge in the ledger every month; and the capitalised total is priced off the roster rather than typed, so a salary change flows through without anybody restating anything.

**What it found.** USD 591k capitalised across four projects and **USD 24,633 capitalised on IUS-001 in the three months after it was placed in service**, which is post-implementation cost and is not capitalisable. On the demonstration instance the amortisation is USD 148k of FY26 cost of revenue and **2.7 points of gross margin** that were not being charged anywhere.

**Where it lives.** The schedule is `capex_FY26.xlsx` — the project register, the time allocation, the per-project lives and the amortisation build, alongside the other two asset classes. The cost of revenue line in the revenue model reads the same fixed asset register rather than a second copy of the answer, and the two are checked against each other every month.

**Revisit when.** A project is abandoned before it goes live, at which point the carrying amount is written off immediately and this entry needs an impairment limb; or a feature is retired early, at which point the single 36-month life stops being defensible.

### SL-29 · An account that carries two economics *(extends SL-11, governs every model built on the ledger)*

**Kind** POL · **Status** RULED · **v1.0** · effective 2026-08 · comparability: **Restates** — prior-period usage economics move

**The case.** SL-11 ruled minimum shortfall true-ups onto their own account, 4032. The account was never built (ESC-12), so the ledger posts two economically opposite things to 4030: metered overage, which a club pays for using the product **more**, and minimum true-ups, which a club pays for using it **less**. The close pack and the variance pack both disclose this. The revenue model then read 4030 as one stream and inherited the defect in a new place — implied overage rate of EUR 1.41 against a contracted 1.20, and a per-match economic that improves as consumption falls.

**The distinction that matters.** A disclosure stops the number being *believed*. It does not stop it being *used*. Every artefact built downstream of a known-contaminated account re-commits the same error unless the split is made somewhere. The question is where.

**The ruling.**

- **Where an account is known to carry two economics and the separating account does not exist, the split is made on entry-level evidence, at the point of use, and stated on the face of the artefact.** Here: the true-up entries carry their own invoice and a memo that names them. The model separates on that, shows the two as adjacent sections, and prints the reason where the reader meets the line.
- **The split must reconcile to the account.** Overage plus true-ups equals 4030, every period, or the artefact does not ship. A split that loses money is a worse defect than the merge it replaced.
- **It is a workaround with an expiry, not a design.** The split moves to the account the day 4032 exists, and the artefact says so. Nothing here reduces the pressure to build the account — the split is what the business does while it waits, and the disclosure is what stops the wait becoming permanent.
- **A split made this way is never silent.** It is a ruling with a comparability note, because it moves reported usage economics in every prior period.
- **The reverse case is barred.** Two streams already separated in the ledger are never merged into one modelled line for tidiness. Separation is cheap to keep and expensive to recover.

**Why.** The merged line was not merely imprecise, it pointed the wrong way: it made consumption look healthier as consumption fell, which is the one thing a usage model exists to detect. The evidence to separate them was in the ledger the whole time, in the memo field, unread. A finance function that discloses a contaminated account and then keeps building on it has documented its problem rather than handled it.

**What it costs.** A text test on a memo field, which is exactly the fragile kind of rule this layer is otherwise built to eliminate — the memo convention could change and the split would fail quietly. Mitigated by the reconciliation above, which fails loudly instead: if the memo test stops matching, overage plus true-ups stops equalling 4030. Accepted as the price of not waiting for a schema change to make the model right.

**What it found.** Split on the demonstration instance, every month with overage recomputes to the contracted EUR 1.20 to the cent, in eight separate periods — which is also the evidence that the split is the right one. FY26 metered overage is USD 327k against USD 51k last year, growing 547%; true-ups are USD 55k against USD 224k, down 75%. Merged, those two facts read as one flat line. They are the clearest signal in the revenue model and the merge destroyed both.

**Revisit when.** Account 4032 is built, at which point this entry is superseded by SL-11 in force and the split moves to the chart of accounts.


### SL-24 · The retention family *(rules MET-027 to MET-032)*

**Kind** DEF · **Status** RULED with two components UNRESOLVED · **v1.0** · effective 2026-08 · comparability: **Prospective**

**The case.** The board pack reported revenue, margin and cash and said nothing about the book that produces them — no ARR line, no retention, no churn, no acquisition cost. The gap was not that the metrics were unruled; SL-08 ruled the ARR family a day earlier. The gap was that nothing implemented them, so a subscription business was reporting itself as a manufacturer.

Building them surfaced the real question, which is not *what is NRR* but *what can this book support*. The subscription files hold **one row of current state per customer** — today's court count, today's price — with no effective date on a change. Two contract changes are known to exist in the population (CLB-0042's upsell from 4 to 10 courts in January, and one downgrade). Both are invisible: the book reports the post-change value in every historical period, so the change never happened and the periods before it are misstated.

**The answers.** (a) Report NRR using a plug for expansion — the market expects the number, and every competitor produces one. (b) Report a proxy and call it NRR. (c) Report what the book supports, name what it does not, and say what would fix it.

**The ruling.**

1. **MET-027 Committed recurring ARR waterfall.** Opening, FX translation, new logos, churned logos, unattributed, closing — and it ties. FX is separated onto its own line so the commercial movement is constant-currency; a book movement that includes translation is not a statement about customers.
2. **MET-028 Gross revenue retention** is a **twelve-month cohort** measure: of the value live twelve months ago, how much is still live. Twelve months of churn over an opening base is prohibited — it charges the base with the churn of customers who were never in it and understates retention in any book that grew. Reported as an **UPPER BOUND**, with the word on the metric, because contraction inside a surviving logo is not observable.
3. **MET-029 Net revenue retention is NOT COMPUTABLE** and is reported as such. It requires expansion and contraction. A monthly proxy — unattributed movement treated as expansion and contraction — may be shown on its own row, labelled a proxy, and **may not be quoted as NRR**.
4. **MET-030 Customer acquisition cost** is **fully loaded and blended**: all S&M over all logos opened. Fully loaded because no ruling exists on which part of S&M is acquisition and which is retention; blended because S&M carries no segment. It is therefore **not comparable to any published benchmark**, and that sentence travels with the metric.
5. **MET-031 CAC payback and MET-032 LTV:CAC are NOT COMPUTABLE.** The numerator is a cost incurred overwhelmingly to win B2B contracts; the denominator is drawn from a book that is 94% consumer subscribers by count. Two populations in one fraction is not a ratio. **LTV for a segment with no observed churn event is emitted as `n/a — no churn observed`, never as a large number**: an unmeasured life is not a long one.
6. **Counting unit** is the site, per SL-01, and the standing disclosure travels with every retention figure.

**SL-24a (UNRESOLVED).** Effective-dated change history on the subscription record — quantity, price, effective date. *Blocker:* the billing system holds it and does not export it. *Owner:* Head of Finance with RevOps. *Interim treatment:* expansion and contraction reported NOT OBSERVABLE; GRR reported as an upper bound. *Unblocks:* MET-029, and the lower bound on MET-028. *Review* 2026-09-30.

**SL-24b (UNRESOLVED).** S&M segmentation between the B2B and consumer motions, and between acquisition and retention. *Blocker:* no cost-centre or campaign dimension on accounts 7010–7060. *Owner:* Head of Finance with the S&M lead. *Interim treatment:* CAC fully loaded and blended with the non-comparability stated on the metric; payback and LTV:CAC not computed. *Unblocks:* MET-030 at segment level, MET-031, MET-032. *Review* 2026-09-30.

**What it costs.** The pack reports fewer SaaS metrics than a competitor's, and two of the four an investor asks for first read NOT COMPUTABLE. Accepted: a diligence analyst who finds that our NRR was a proxy does not merely discount NRR — they re-price every other number we gave them. The disclosure is cheaper than the discovery.

**Revisit when.** SL-24a or SL-24b resolves; or the first churn event lands in a B2B segment, at which point MET-032 becomes computable on one leg and the other blocker becomes the binding one.


### Metric registry deltas (to `metric_registry.csv`)

| Metric | Was | Now |
|---|---|---|
| MET-010 | UNRESOLVED | Ruled v2.0 — trailing-3-month usage basis (SL-08) |
| MET-011 | UNRESOLVED | Ruled v2.0 — renamed Total annualised revenue (commercial); barred from board material (SL-08) |
| MET-012 | UNRESOLVED | Ruled v1.0 — plan-rate constant currency (SL-10) |
| MET-019 | UNRESOLVED | Ruled v1.0 — deliverable test (SL-16) |
| MET-020 | UNRESOLVED | Ruled v1.0 — 35% ratified with basis and re-measurement (SL-17) |
| MET-021 | UNRESOLVED | Ruled v1.0 — contracted price; drift is leakage (SL-09) |
| MET-023 | UNRESOLVED | Ruled v1.0 — FIFO by expiry; breakage on expiry, overturning Policy A (SL-14) |
| MET-026 | UNRESOLVED | Ruled v1.0 — TTM basis, labelled assumption, never re-aggregated (SL-15) |
| MET-027 | NEW | Ruled v1.0 — ARR waterfall, FX on its own line, ties (SL-24) |
| MET-028 | NEW | Ruled v1.0 — GRR on a twelve-month cohort, reported as an upper bound (SL-24) |
| MET-029 | NEW | **NOT COMPUTABLE** — NRR needs expansion and contraction; proxy permitted, labelled (SL-24) |
| MET-030 | NEW | Ruled v1.0 — CAC fully loaded and blended, non-comparability stated on the metric (SL-24) |
| MET-031 | NEW | **NOT COMPUTABLE** — CAC payback; blocked on SL-24b (SL-24) |
| MET-032 | NEW | **NOT COMPUTABLE** — LTV:CAC; blocked on SL-24a and SL-24b (SL-24) |

### Change log

| Date | Entry | Change | Comparability |
|---|---|---|---|
| 2026-08-22 | SL-30 | Internal-use software capitalised under ASC 350-40 / IAS 38; amortisation ruled into cost of revenue; useful life set per project | **Restates.** Every prior period moves: FY26 cost of revenue up USD 148k, gross margin 69.1% to 66.2%, R&D down by the capitalised labour, and net book value appears on the balance sheet. |
| 2026-08-21 | SL-29 | An account carrying two economics is split on entry-level evidence at the point of use, pending the schema change | **Restates.** Usage economics move in every prior period: FY26 metered overage USD 327k, not USD 383k; true-ups shown separately at USD 55k. |
| 2026-08-18 | SL-24 | The retention family ruled; MET-027 to MET-032 added, three of six NOT COMPUTABLE by ruling rather than by omission | Prospective. |
| 2026-08-18 | All | Instance v1.0 — initial rulings | Restate: SL-08, SL-11, SL-12 (pending SL-13), SL-14. All others ratify existing practice or apply prospectively. No changes take effect between cut-off and sign-off of any period. |
