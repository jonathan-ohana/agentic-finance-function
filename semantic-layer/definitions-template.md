# The Semantic Layer — template and method

**Version** 1.0 · **Artefact class** governed, human-owned, read-only to agents · **Instance required** one per company, before any agent output leaves draft

---

## What this artefact is

The semantic layer is the one place where a finance leader's judgement is written down, versioned, and made available to every agent, so that a number means the same thing in the board pack as it does in the ledger. Every agent in this package computes. None of them decides what a computation means. That decision is made here, once, by a person, and every agent reads it.

It is not a glossary. A glossary defines the words everyone already agrees on, and agreement is precisely the situation in which a written definition adds nothing. The value of this layer is concentrated entirely in the contested cases: where two reasonable finance people would rule differently, where the ruling changes a reported number, and where the reason for the ruling matters more than the ruling itself.

Three tests for whether something belongs here. All three must hold:

1. Two competent people could rule it differently.
2. The ruling changes a number somebody reports or acts on.
3. An agent, left without the ruling, would have to guess.

If an entry could not plausibly have been ruled the other way, it does not need to be here. If an agent has ever escalated a question and the answer was a judgement rather than a lookup, that answer belongs here.

## How to install it

Copy this template into an instance file. Answer every question in Part 2 using the record format in Part 3. Anything you cannot yet answer goes in as `UNRESOLVED` under the discipline in Rule 4 — an honest gap is usable; a plausible guess is not.

The question set in Part 2 is the minimum, assembled from what breaks in practice. Your business will add questions of its own. An instance that answers every question here is not finished; it is started. The layer accretes a ruling every time an agent escalates something the instance does not cover, and an instance that has not grown in six months means either the business has stopped changing or the escalations have stopped being read.

---

## Part 1 — The rules of the layer itself

These govern the file, whoever fills it in. They are not suggestions and they are not business-specific.

### Rule 1 — Definitions and policies are different things, and every entry says which

A **definition** (`DEF`) states what a number *is*: what a customer is, what counts as recurring revenue, which price a metric uses. Definitions are claims about meaning. Changing one changes every number ever computed under it — history rewrites, whether or not anyone recomputes it.

A **policy** (`POL`) states what the company *does*: how it provides for doubtful debts, whether untaken leave accrues, what it waives as immaterial. Policies are choices with an effective date. Changing one applies prospectively and does not change what past numbers meant.

Every entry is marked `DEF` or `POL`, and the marking decides its change behaviour. Conflating them causes trouble in both directions. Treat a policy change as a definition change and you restate history that was never wrong — after which people stop changing policies, because every change looks like an admission. Treat a definition change as a policy change and comparatives silently break: this year's figure and last year's share a name and nothing else, and the growth rate between them is fiction.

An entry can carry both — a definition of what a liability is, and a policy for how it is estimated. Split them into separately versioned parts rather than blending them.

### Rule 2 — A definition that cannot be computed is a wish

Every `DEF` names its inputs: the tables and fields of the data contract it is computed from. If those inputs do not exist — no field holds the value, no system captures it — the entry may not be written as if it were in force. It is recorded `UNRESOLVED`, with the missing inputs named and a requested schema change attached.

The failure mode this prevents: a definition that exists on paper with no computation behind it will still get asserted in a reporting pack, because the words are available even when the number is not. The figure under it was then produced some other way — a spreadsheet, a memory, a guess — and nobody can say which. A written definition with no data behind it is more dangerous than no definition, because it looks answered.

### Rule 3 — Versioning, and what a change owes the past

Every entry carries a version and an `effective_from` period. Every reported number cites the entry it was computed under, at version: `MET-009@1.0` is a different number from `MET-009@2.0` even when they happen to agree.

Two classes of change:

- **Clarification** — wording improves, no computed value changes anywhere. Minor version. No comparability question arises.
- **Substantive** — any computed value changes. Major version, and the ruling **must** state one of three comparability decisions:
  1. **Restate** — comparatives presented alongside the new number are recomputed under the new version, and the restatement is disclosed once.
  2. **Fork** — both versions are reported side by side for a stated number of periods, then the old one retires.
  3. **Break** — old periods stand as computed; every comparison that crosses the boundary is flagged non-comparable, permanently.

A substantive change with no comparability decision is invalid, and agents must refuse to compute under it. A change landing mid-year defaults to **Restate** within the fiscal year: a trend chart is the artefact most consumed and least questioned, and a definition change without a restatement decision breaks every trend crossing the boundary while leaving it looking intact. That is the failure mode: not a wrong number, but a wrong comparison that no individual number reveals.

No entry is ever deleted. Old versions remain readable, because numbers computed under them remain in circulation.

One timing prohibition: **no substantive change takes effect between a period's cut-off and its sign-off.** A definition changed mid-close means the close both computed the number and moved the target it was computed against, and the sign-off then attests to neither.

### Rule 4 — UNRESOLVED is a legitimate state, with its own discipline

Some questions cannot be answered from the available data, and some should not be answered by finance alone. The layer must be able to say so without the gap becoming either an invisible default or a permanent parking space.

- Only the **owner** (Rule 5) may mark an entry `UNRESOLVED`, or accept an agent's proposal to. Agents may surface the gap; they may not declare it.
- Every `UNRESOLVED` entry carries five things: the **forcing case** (the specific evidence that raised the question), **what blocks resolution** (missing data, missing decision, missing counterparty), the **interim treatment**, the **resolving owner**, and a **review date**.
- The **interim treatment** is mandatory and is the whole point. It states exactly what an agent does on hitting the entry: a stated conservative computation, an exclusion with a label, or a refusal to produce the number. Never a silent guess. An output resting on an `UNRESOLVED` entry carries the entry's ID visibly; it may not be presented clean.
- `UNRESOLVED` ages. An entry past its review date is escalated by the calendar-owning agent as an overdue obligation, exactly like a filing. An entry unresolved for more than two closes appears **by name** in the management reporting pack.

The failure mode without this discipline: `UNRESOLVED` becomes where questions go to look answered. Nothing complains about a parked question, and the numbers computed around the gap acquire a confidence the gap never earned.

### Rule 5 — Who may change what

- The layer has **one named owner**, a senior finance human. Not a role shared by committee, not an agent.
- A `DEF` used in external reporting — board, investors, covenants — is changed only by the owner, in writing, in this file.
- An internal-only `DEF`, or any `POL`, may be changed by a named delegate, with the owner notified in the change record.
- **Agents propose, never enact.** A proposal is a drafted ruling in the record format of Part 3, with the forcing case and evidence attached, filed to the escalation register. The best agent proposals arrive pre-written and get accepted verbatim; they still arrive as proposals.

### Rule 6 — No agent edits this file. Ever.

This is the one artefact in the package that every agent reads and no agent may write, and the reason is structural, not cautionary.

The layer is the measuring stick. An agent that can edit the definition it is measured against can make any output correct by construction — not through malice, but through the ordinary mechanics of optimisation: whatever check an agent faces, the cheapest path to passing it that exists will eventually be taken, and editing the check is the cheapest path there is.

The subtler version is helpfulness. An extraction agent meets a contract term the schema cannot hold, and "fixes" the definition so the term fits. The term is now recorded — and the company's vocabulary has been silently rewritten to match what one document contained rather than what anyone decided. A definition drifted by accretion is worse than one changed by error, because no single edit looks wrong.

Therefore: the file is read-only to every agent at the infrastructure level, not merely by instruction. Proposals go to the separate register. Any diff to this file not traceable to the owner or a named delegate is an incident: the change is reverted, and every output computed since the change is quarantined and re-run.

### Rule 7 — The scope of assertion

This rule governs the vocabulary agents use about their own conclusions, and it is the most general rule in the layer.

**A verdict asserts only what was actually compared, and must say what that was.** When an agent compares a document to a ledger and reports agreement, the agreement covers exactly the fields both sides hold — no more. If the document states six material terms and the ledger stores two of them, "agrees" means "agrees on two", and any consumer who reads it as "the contract is confirmed" has been misled by an accurate statement.

Therefore, in every instance of this layer:

- Every comparison verdict carries its **compared-field list**.
- Every material term with no counterpart on the other side is listed under a distinct verdict — `UNVERIFIABLE` — never silently omitted. Silence and verification must be impossible to confuse.
- No downstream consumer, human or agent, may cite a verdict beyond its field list. "The ledger agrees with the contract" is a permitted sentence only when the field list covers every material term; otherwise the sentence is "the ledger agrees on the terms it stores, and cannot check the rest", and the rest are named.

The same rule governs the close sign-off, which is the largest verdict the function produces. A signature on a close computed by agents cannot assert "these numbers are right" — the signer computed none of them, and pretending otherwise either deters signing or turns the signature into a formality, and both destroy the control. The instance must state exactly what the signature asserts (Part 2, F2), and the stated scope is the entire value of the ritual: a person taking responsibility for a process and its exceptions, knowingly, in writing.

---

## Part 2 — The questions every instance must answer

Grouped by the kind of question, because the kinds fail differently. For each: the question, and what breaks while it is unanswered. The instance answers each one in the record format of Part 3.

### A. Identity — what you are counting

**A1. What identifies a customer?**
A name is a label, not a key. The moment two records share a name — two sites, two entities, one entity re-contracted — every metric with "per customer" in it silently picks a unit nobody chose. There are at least four candidate units: the legal counterparty, the operating site, the agreement, and the billing account. Each metric must name its unit. *Unanswered:* logo count, churn, net revenue retention, concentration and cohort analysis are all computed on an accidental unit, and no two of them necessarily on the same one.

**A2. Two live agreements, one counterparty, no supersession — one line or two?**
When a counterparty holds two concurrent agreements and neither references the other, the data supports both readings: an expansion that should have been an amendment (one customer, and the earlier terms possibly dead), or two genuine sites (two everything). The instance must rule a default treatment for the period before the facts are known, because billing and committed-revenue metrics cannot wait. *Unanswered:* either committed revenue is double-counted, or a live contractual obligation is extinguished by inference — and an agent will pick one of these silently.

**A3. Who keeps derived contract state true?**
Contracts change state without anyone acting: an auto-renewal fires when a notice deadline passes, a quantity clause lets the contracted amount drift from the signed amount. A ledger that only records signatures is wrong by default the day after the first silent transition. The instance names the owner of each transition, the event that triggers the update, and the arithmetic of the update (renewal period is not always the initial term). *Unanswered:* backlog and committed revenue quietly exclude renewed contracts; churn is recorded a year after it was decided; notice windows expire with nobody watching, which converts a decision into an accident.

### B. Fields — what a value may claim

**B1. A field that holds one value for a two-valued fact.**
Systems flatten. When a contract bills one component in advance and another in arrears, and the ledger holds a single cadence field, the field is not wrong — it is incomplete, which is harder to see. The instance must state, for every such field, **which member of the collapsed set the field holds**, and prohibit consumers from treating it as the whole fact. Where the missing member matters — and a cadence's direction decides whether a balance is deferred or accrued — the instance requests the schema change and names the interim treatment. *Unanswered:* cash forecasting, deferred revenue release, and dunning are all built on the assumption that the stored leg is the only leg.

**B2. Absence, zero, and unknown are three different facts.**
A contract that asserts "no minimum applies", a field never populated, and a minimum of zero are indistinguishable once all three are stored as `0` — which means an extraction failure can never again be detected, and every filter, sum, or average over the field treats a contractual absence as a number. The instance adopts an encoding that keeps the three apart (the data contract's convention — empty means unknown, never zero — plus a status marker for asserted absence) and bans zero as an encoding of absence. *Unanswered:* committed-revenue floors, disclosure counts, and data-quality sweeps are all silently wrong, and stay silently wrong.

**B3. When a document contradicts itself, which text governs for computation?**
Real documents disagree with themselves: a header table against an operative clause, a special condition against a standard term. Which reading governs is ultimately a legal question, but the ledger cannot hold two values while lawyers deliberate. The instance sets a **computational precedence rule** (which text the ledger carries in the interim), a **conservatism rule for deadlines** (where the two readings imply different action dates, act on the earlier), and routes the legal question as `UNRESOLVED` with a deadline. *Unanswered:* each agent — or each human — picks a reading ad hoc, the ledger inherits contradictions instead of surfacing them, and the same defect resolves differently on different contracts.

### C. Revenue — what counts, at what price, when

**C1. The recurring-revenue family.**
"ARR" bare is a different number to sales, to the board, and to a diligence analyst, and the gap between their versions is where credibility dies. The instance defines a **named family**: the strictly contracted figure, the figure including annualised consumption (and the annualisation basis — a single spiky month times twelve is a coin flip), and whatever broader commercial figure the go-to-market team uses. Each gets its own ID; the bare word is banned from any artefact; each audience-facing document states which family member it uses. *Unanswered:* the company tells three true stories with one name, and eventually has to explain the differences under time pressure to someone holding a term sheet.

**C2. Price basis: list, contracted, or billed?**
Three prices can exist for one customer — the list price, the contractually agreed price, and what the billing system actually charges — and they genuinely diverge (discount cohorts, expired grandfathering, configuration drift). A recurring-revenue metric must name its basis. The gap between contracted and billed is then a **finding** (leakage, surfaced and fixed), not a definitional ambiguity absorbed into the metric. *Unanswered:* the metric absorbs billing errors as if they were pricing decisions, and the leakage becomes invisible precisely because the headline number moved to cover it.

**C3. Constant currency: which rate, fixed when?**
"Constant currency" is only a defined term once someone says which rate and for how long. The instance rules the rate source (typically the rate the annual plan was struck at), its fixity (for the full plan year), and the requirement that both sides of any growth comparison use the same rate. *Unanswered:* constant-currency growth quietly becomes a choice made per-report, which is to say a lever.

**C4. Recoveries, penalties, and breakage — revenue, and whose line?**
Minimum-commitment shortfalls, unredeemed prepayments, early-termination charges: money that arrives because a customer *did not* consume. Two defensible treatments — fold each into the stream it protects, or give it its own line. The choice changes what the per-unit economics look like and whether a calibration problem (minimums set far above realistic usage, prepayments systematically expiring) stays visible. The instance rules per stream, with recognition timing. *Unanswered:* the underlying stream looks healthier than it is, and the signal that pricing is miscalibrated is consumed by the very line it should be flagging.

**C5. Are consumer prices tax-inclusive?**
Where consumer-facing prices are quoted inclusive of indirect tax — the norm in many jurisdictions — the advertised price is gross, and revenue is the net. This single yes/no changes reported revenue by the full tax margin on every consumer sale. It must be ruled explicitly, because a billing export contains no marker for it and an agent summing receipts will book gross without hesitation. *Unanswered:* revenue is overstated by the tax margin against a liability that has never been recognised, and the error grows with the business.

**C6. Prepaid credits and consumption: which lot's price, and breakage when?**
When customers prepay for units at prices that differ by purchase lot, consumption must be priced by some rule — lot-specific FIFO, weighted average — and unredeemed value must be released by some rule — proportionally as redemption happens (requires a supportable estimate) or only on expiry (requires patience). Both pairs are defensible; the instance rules both, and states what evidence would justify the estimate-based method. *Unanswered:* deferred revenue release is whatever the billing code happens to do, and breakage is recognised on an estimate nobody has examined.

### D. Tax — the treatments that exist whether or not the ledger holds them

**D1. Indirect tax treatment, per supply type.**
One product sold to a domestic business, a foreign business, and a foreign consumer can attract three different indirect-tax treatments, each with its own invoicing requirement, filing, and deadline. The treatments exist as legal fact the moment the sales happen; the only question is whether the ledger represents them. This is the question most likely to be **honestly unanswerable from the data** — no tax fields, no registration facts in any governed system — and it is therefore the flagship application of Rule 4: ruled as `UNRESOLVED`, with an interim treatment that stops agents from inventing tax logic, a schema request naming the missing fields, an external owner, and statutory deadlines that stay on the calendar regardless, because the tax authority does not wait for the schema. *Unanswered silently:* the largest single misstatement a consumer-facing multi-jurisdiction business can carry, growing monthly, discovered in diligence.

### E. Cost boundaries, estimates, and thresholds

**E1. Shared-resource cost boundaries.**
Where one resource serves both delivery and development — compute, support staff, infrastructure — the COGS/opex boundary is a judgement that moves gross margin directly. The instance states the boundary as a **decision rule** ("a cost incurred producing output delivered to a customer is COGS") rather than a percentage wherever possible; where an allocation percentage is unavoidable, it carries a measured basis and a re-measurement cadence, and a movement beyond a stated tolerance is a version change. An allocation with no basis is a plug wearing a percentage. *Unanswered:* gross margin is a negotiable number, and everyone negotiating it is right.

**E2. Expected credit loss: a provision, or a documented nil, on what basis.**
An ageing report is not a provision. The instance rules whether receivables carry an expected-loss provision, the matrix or method, the rates and their basis — including the honest case where there is no loss history yet, which justifies low rates but not the absence of a policy. An allowance account that exists and has never been posted to is a close step that has silently stopped existing. *Unanswered:* receivables are stated at a value nobody has actually asserted, and the first bad debt becomes a surprise with a history.

**E3. Compensation accruals: target, or expected attainment?**
A bonus pool accrued at target is a budget; accrued at expected attainment it is an estimate that needs an assessment process behind it. Either is defensible; the instance picks one, states the assessment cadence and the default before the first assessment exists, and floors the accrual at contractual guarantees. *Unanswered:* the year-end true-up is a shock in whichever direction nobody prepared for.

**E4. Untaken leave: a liability, or a policy — by jurisdiction.**
In some jurisdictions untaken leave is a cash liability on termination as a matter of law; in others it is whatever the company's policy says. This is the exemplar of the `DEF`/`POL` split: the jurisdictional facts are definitions the company does not get to choose; the treatment where law is silent is a policy it must choose. The instance carries the table, per jurisdiction of employment. *Unanswered:* a real liability accrues invisibly in some countries while a phantom one is imagined in others.

**E5. Materiality, written down.**
Every finance function operates thresholds — what adjustment is too small to post, what variance is too small to explain, what purchase is too small to spread. Operating them unwritten means each agent and each human applies their own, and "immaterial" becomes a private judgement invoked after the fact. The instance writes the numbers: posting threshold, aggregate-waived threshold per period, flux-explanation threshold, capitalise-or-spread threshold — with their derivation and review cadence. *Unanswered:* materiality is claimed, never granted, and the claim is unfalsifiable.

### F. The vocabulary of assertion

**F1. What a comparison verdict is entitled to assert.**
Apply Rule 7 concretely: for each reconciliation the agents run, the instance lists the verifiable field set (both sides hold it), the unverifiable set (one side is blind), and the required verdict form. The unverifiable set is also a standing schema-gap register: every field on it is a term a counterparty could change without any system noticing. *Unanswered:* every "agrees" in every report is broader in the reader's mind than in the data, which is the mechanism by which a reconciled ledger and a mispriced contract coexist for years.

**F2. What a close sign-off asserts.**
The instance states the exact text of the attestation a signer makes: which process claims (every blocking step ran and produced evidence or a documented nil), which judgement claims (exceptions reviewed and accepted by name, open items carried knowingly), and which claims it explicitly does not make (personal recomputation, absence of error). *Unanswered:* either nobody signs, or everybody signs, and the two failures are indistinguishable from outside.

---

## Part 3 — The ruling record

Every entry in the instance uses this shape. The shape is the method: a ruling without a forcing case is a glossary entry, a ruling without a cost is advertising, and a ruling without a revisit trigger is dogma.

```
ID          SL-nn (stable, never reused)
Name        what is being defined or decided
Kind        DEF | POL
Status      RULED | UNRESOLVED
Version     n.n        Effective    YYYY-MM       Ruled by    name, date

THE CASE      The specific instance that forces the question — document IDs,
              record counts, amounts. Real evidence, not a hypothetical.
THE ANSWERS   The defensible readings, stated fairly. If only one reading is
              defensible, this entry probably fails the three tests.
THE RULING    Which reading governs. One sentence if possible.
WHY           The reason — the thing a successor needs when the case recurs
              in a form the ruling didn't anticipate.
WHAT IT COSTS What this ruling gives up, misstates, or defers relative to
              the road not taken. Quantified where the data allows.
REVISIT WHEN  The observable condition that reopens the question.
COMPUTED FROM Tables and fields (DEF), or scope and effective date (POL).
              For UNRESOLVED: the interim treatment, the blocker, the
              resolving owner, and the review date.
```

The instance ends with three registers, maintained continuously: the **UNRESOLVED register** (every open entry, with review dates — this is a work list, not an archive), the **schema-change register** (every field a ruling requires that the data contract does not yet hold), and the **change log** (every version bump, with its comparability decision).
