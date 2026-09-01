# 35 — Plain-language glossary

*Every term this project uses that isn't ordinary English, explained with an CourtIQ example. Written 18 August 2026, after the vocabulary had grown faster than the definitions.*

---

## 1. The agents — who does what

An **agent** here is not a chatbot and not a script. It is a written set of instructions and prohibitions — a **charter** — that Claude follows when doing one job. The charter is the agent. Change the charter and you have changed the employee.

Thirteen exist. Six have been written and run.

| Agent | Its one sentence |
|---|---|
| **Ingestion** | Reads documents and turns them into data |
| **Evidence** | Asks "for this number, where is the paper?" across every connected source |
| **Bookkeeper** | Performs the close: reconciliations, tie-outs, draft journal entries |
| **Analyst** | Explains *why* the numbers moved |
| **Advisor** | Finds things worth acting on and presents options |
| **Chief of Staff** | Owns the finance calendar and says what is due, late or at risk |
| **Drift Auditor** | Audits the other agents and the rules they run on |
| **Forecaster** | Not yet built — the rolling forecast |
| **Controller** | Not yet built — cash view and 13-week forecast |
| **Reporter** | Not yet built — the board pack |
| **Deal Desk**, **Co-pilot**, **Org Assessment** | Specified, not built |

**Separation of powers** is the phrase for how they divide up:

> The Bookkeeper says **what happened**. The Analyst says **why**. The Advisor says **what to do about it**. The Chief of Staff says **when it is due**.

Each is forbidden from doing the next one's job. The Analyst may write *"gross margin fell four points because compute cost per match rose 11%"*. It may **not** write *"we should renegotiate the compute contract"* — that sentence belongs to the Advisor, and the reason is that a recommendation arriving inside a numbers document borrows authority the numbers give it.

### Ingestion, specifically

The word means "taking things in." The Ingestion agent's job is the least glamorous and the most load-bearing: a signed PDF contract says *"€89 per court per month, 120 matches included, 60 days' renewal notice."* None of that is data until something reads the PDF and writes those values into a table.

It has read **239 contracts** and **19 payroll invoices** in this project. Its most important rule is not about accuracy:

> **Absence is a finding, never a value.** A missing countersignature date is not "probably the same as the signature date." A missing minimum is not zero.

Because inferring a plausible value *converts a visible gap into an invisible error*, which is worse than being wrong loudly.

---

## 2. The vocabulary of trust

### Artefact

The word that trips everyone, and it is deliberately boring. **An artefact is a thing the system produced that you can point at.** A close pack. A reconciliation. A journal entry. A drift report. A spreadsheet.

It matters because of one rule repeated in several charters: **completion is evidence, not inference.** You may not say a step was done because the steps around it were done. There must be an artefact, and if there is no artefact the step did not happen — regardless of anyone's memory.

So when the Bookkeeper reports "fourteen of eighteen steps produced an artefact," it is not being pedantic. It is saying four steps have no evidence they occurred.

### Artefact instance

The **counting unit** for trust. One decision can cover many instances.

If a human reviews a batch of 48 contract extractions in one sitting and approves them, that is **one decision** and **48 instances**.

This distinction is what makes the whole trust ladder workable. A monthly close happens twelve times a year, so measuring trust per close would take twenty months to earn anything. But a close *contains* hundreds of reconciliation lines and categorisations. Counting instances rather than cycles is what lets a high-volume workflow earn trust in months instead of years — and it is also why the board deck, which genuinely happens four times a year, should probably never earn autonomy at all.

### Autonomy, L0 / L1 / L2

How much the agent is allowed to do without a human in front of it. The names come from a ladder:

- **L0 — draft only.** The agent produces; a human reads everything before it goes anywhere. Every agent starts here.
- **L1 — execute with approval.** The agent acts once approved, reviewed in batches rather than line by line.
- **L2 — autonomous with audit.** The agent acts without prior review; a sample is checked afterwards.

Three things stay human **forever**, at any level, whatever the track record: **money movement**, **external communication**, and **anything entering the signed financial record**.

### Promotion and demotion

The words are borrowed from employment on purpose. An agent is treated like a junior hire: it starts supervised and earns responsibility by demonstrating it.

**Promotion** from L0 to L1 requires, all at once:

- 200+ artefact instances **reviewed** (not produced — reviewed)
- material correction rate under 2%
- escalation recall of 100%
- at least three calendar months

**Demotion** takes **one strike**. One missed material error and the agent goes back to L0.

> *Promotion takes hundreds of instances and months. Demotion takes a single missed error. That asymmetry is the point, and it is what makes the ladder credible to an auditor rather than a marketing device.*

There is also **automatic demotion**: any material change to a source system — new pricing, a new billing platform, a new entity — sends every affected agent back to L0 immediately, because *the track record was earned on data that no longer exists*.

Right now **no agent has been promoted, and none can be**, because nobody has reviewed anything. Ingestion has produced 258 instances, above the 200 floor, and the scorekeeper still blocks it with four words: **production is not evidence.**

---

## 3. The vocabulary of output

### Escalation

The agent stops and hands something to a human rather than deciding it. Not a failure — the opposite. An agent that escalates the right things is working; one that never escalates has either been given easy work or has learned to go quiet.

**198 escalations** have been raised so far. None has been judged, which is why one of the trust metrics can't yet be computed.

### Verdict

A short label the agent attaches to a comparison. The Ingestion agent compares a contract to what the systems hold and returns one of:

`AGREES` · `STALE` · `CONTRADICTED` · `INCOMPLETE` · `UNSUPPORTED` · `UNVERIFIABLE`

The last one was added late and is the most interesting. It means: *I could not check this, and I am telling you rather than staying silent.* It exists because of a finding from the contract sweep:

> An `AGREES` verdict meant the document agreed with the **five fields the ledger stores** — not that the price was confirmed, because the ledger has no field for price. Two of six material terms were untested and the verdict didn't say so.

That produced a general rule: **a verdict asserts only what was actually compared, and must say what that was.** Anything one side is blind to is listed as `UNVERIFIABLE`, never left as silence.

### Nil result

**The agent looked and found nothing.** Recorded as a full result with the population it examined — which accounts, how many rows, which fields.

The rule that makes this matter:

> **A nil result is a completed step. A skipped step is not a nil result** — and the difference is invisible in every financial statement ever produced.

The steps that find nothing for eleven months are exactly the ones people quietly stop doing, and month twelve is when they'd have caught something.

Concretely: the FX revaluation nobody performs turned out to be worth $6,499 across the whole ledger. Immaterial. **That is the point** — nobody knew it was immaterial, because nobody computed it.

### BLOCKED vs NOT RUN

Two different failures, kept apart:

- **BLOCKED** — the agent could have done it but a *decision doesn't exist*. The FX revaluation is blocked because nobody has ruled how to treat eighteen prior unrevalued periods.
- **NOT RUN** — the agent *couldn't* do it. No corporate card feed is connected, so the card reconciliation didn't happen.

The first needs a human to make a ruling. The second needs a system connected. Collapsing them into "incomplete" hides which.

---

## 4. The vocabulary of the loop

### The two loops

The core idea, and the one worth keeping:

- **The execution loop** — the agent doing the work. Closes **slowly**, workflow by workflow, only where autonomy has been earned.
- **The improvement loop** — the system getting better at the work. Closes **completely and immediately**.

Why the asymmetry: the improvement loop **acts on rules, not records**. It never touches a number in the books; it changes how the system will behave next month, with a changelog, after a human ratifies it. That is safe to close fully. The execution loop touches the actual financial record, so it crawls.

> **Agents propose their own improvements; only a human ratifies.** That is the difference between self-improving and self-rewriting.

### Review ledger

The file where every human correction of an agent gets written down — what was wrong, how big, whether the agent had flagged its own uncertainty. Without it there is no history, and without history nothing can be measured.

Its most important column is **`agent_flagged_uncertainty`**:

> An agent that was wrong **and said it might be** is behaving correctly. An agent that was wrong **and confident** is the dangerous one — and without this column the two are indistinguishable in the statistics.

### Routing and destination

Every correction goes to exactly **one** place:

| What went wrong | Where the fix lives |
|---|---|
| A **definition** was unclear | A new semantic-layer version |
| A **process** was wrong | A charter amendment |
| The **data** was bad | An ingestion rule or a test |
| The **model** got it wrong | A model-tier change |

And the rule that makes it real: **a correction is not closed until it has a destination and an artefact.** A correction that was only fixed in this month's output will recur next month.

This is where the audit caught me. Six corrections were logged as closed against artefacts that turned out to be **prose labels naming nothing** — so the "100% closed" figure was measuring my honesty, not reality. The scorekeeper now opens the named file and checks the thing is actually in it.

### Drift

The slow rot of a governance system. A review that stopped happening. A rule that stopped firing. A definition that changed with no record of why.

Its defining property is that **it is silent**. All of those produce exactly the records a healthy month produces — none. Worse, drift often looks like improvement: acceptance rises when the reviewer stops reading, escalations fall when an agent learns to stay quiet.

### DORMANT vs DISCONNECTED

Two readings of the same silence, and the auditor must say which it can prove:

- **DORMANT** — the rule was checked, never triggered, and the log was demonstrably working. Possibly too loose to be a real control.
- **DISCONNECTED** — no evidence the rule was ever checked. The control isn't wired up. Much worse.

> *An absence asserted over a dead log is not a finding; it is a guess wearing one.*

Current state: 1 FIRED, 20 DORMANT, 16 DISCONNECTED — the sixteen being the close steps named in the checklist and never implemented.

### Seed pack

A set of known problems with known correct answers, kept by a human, that the Drift Auditor must re-detect every time it runs.

The reason: **a clean month and a broken audit produce identical reports.** If the auditor finds nothing, is everything fine, or has it stopped working? The seeds are the only place those two states produce different evidence.

This is what caused the first audit to withdraw itself: six seeds failed to reproduce, so under its own rule the month is **not audited** — even though its findings still stand on the register.

---

## 5. The vocabulary of the data

### Semantic layer

The written-down answers to every question where two sensible finance people would disagree. Not a glossary — nobody needs "ARR" spelled out. It holds the **contested** cases.

Example: three different numbers were all being called ARR. The layer ruled that **the bare word is banned**; every use cites a specific definition. The most valuable one loses the name entirely, because event revenue isn't recurring, and:

> *A diligence analyst who unpicks event revenue from a number labelled ARR does not merely correct the number; they re-price everything else we told them.*

It is **read-only to agents**, permanently and at the infrastructure level. An agent that could edit the definition of the number it reports would be a control failure, not a feature.

### UNRESOLVED

A question the layer has **not** answered, recorded openly with an owner and a review date rather than quietly guessed at. Three are open: the customer-name problem, a contract with two different stated minimums, and VAT.

### Data contract

The shape the data must be in for agents to work — 15 tables, what each must contain, and the rules that must hold. The thing the installer checks a new company's exports against.

### Lineage

Every number traces to the journal line, to the document, to the clause. Enforced by test: the build fails if any journal line has no supporting document. 6,052 lines, 0 unsupported.

### Materiality

The size below which a difference isn't worth correcting. The subtle rule:

> The threshold licenses **not posting a correction** for a difference you understand. It does not license **not understanding**.

---

## 6. The two forbidden acts

Each has a name, and each carries the harshest penalty in its charter.

### The plug (the Bookkeeper)

Making a reconciliation balance **by force**. The crude version is a balancing entry. The versions that actually happen are quieter: rounding a difference away, reclassifying it to "sundry," burying it in the largest line, or choosing the cut-off date that makes it vanish.

> *An unexplained difference, reported, is the control working. The same difference, absorbed, is a control that has stopped existing — and the mechanics of absorption are indistinguishable from the mechanics of concealment.*

### The distributed residual (the Analyst)

When explaining why a number moved, the pieces you can name rarely add up to the whole. The gap is the **residual**, and it must be reported under its own name.

Spreading it across the named causes so the explanation looks complete is:

> *the analytic form of the Bookkeeper's plug — same motive, same concealment, and harder to detect, because afterwards nothing is out of balance.*

Both carry the same penalty: everything back to L0, and every piece of work since the last clean month re-run.

---

## 7. The measurements

| Metric | What it means | Why it exists |
|---|---|---|
| **Acceptance rate** | Approved with no edits ÷ total | The headline, and misleading on its own |
| **Material correction rate** | Real errors ÷ total | The one that decides trust |
| **Mean materiality** | Average size of a real error | Separates rounding from damage |
| **Escalation precision** | Escalations the reviewer agreed were warranted | Catches an agent escalating everything to look safe |
| **Escalation recall** | The share of real errors the agent **did** flag | **The dangerous one** |

The rule that ties them together, and the sentence worth remembering:

> An agent at **95% acceptance and 60% recall** is more dangerous than one at **70% acceptance and 100% recall** — because the first one is quietly wrong and the second one asks.

Which is why acceptance rate is never allowed to appear on its own.

### Not computable ≠ zero, and ≠ perfect

The scorekeeper returns a metric as **null with a reason** rather than a number when it can't be measured. A workforce with no reviews has an **undefined** acceptance rate, not a perfect one. Reporting 100% there would be the single most dangerous number the system could produce, because it would unlock promotion on no evidence at all.

---

## 8. The engine / agent split

Recurring architecture: for every agent that handles a lot of numbers, there is a **deterministic tool** that computes and an **agent** that judges.

| Tool | Agent | The split |
|---|---|---|
| `close.py` | Bookkeeper | Computes balances and differences; the agent decides what each difference *is* |
| `variance.py` | Analyst | Computes the bridges; the agent decides what *caused* each movement |
| `scorekeeper.py` | Drift Auditor | Computes the metrics; the agent decides what they *mean* |

Two reasons. Arithmetic across thousands of rows is exactly where a language model is confidently wrong. And the tools contain **no verdict field anywhere** — deliberately — because giving the agent a pre-formed judgement lets it inherit one and present it as its own.

---

## 9. Package vs example

- **`package/`** — ships to any company. Nothing in it mentions padel, clubs or courts, and that is enforced by a test.
- **`example/`** — CourtIQ, the worked demonstration. The data, the 673 documents, the agent runs.

The same split runs through everything: the semantic layer has a **template** (the questions) and an **instance** (this company's answers). So does the seed pack, and so does the mapping file.
