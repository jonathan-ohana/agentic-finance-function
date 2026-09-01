# 67 — Five finance agents, and how each one will be confidently wrong

*A FinanceOS playbook.*

*A starter playbook, in the format the market has settled on — trigger, tools, instruction logic, output — with the three things that format leaves out: what it takes for the agent to earn more autonomy, what takes it away, and the specific way it will be wrong while sounding certain.*

---

## Why this document exists

The best lead magnet in this category is an AI-native ERP's *Deploying Your Own Agents*, and it is genuinely good: five deployable agents, each with a trigger, its tools, its instruction logic and its output, plus five questions to ask before deploying any of them. Its doctrine matches the one in this package, arrived at independently — **agents draft, controllers approve, nothing posts without a human decision**, and *"structured, consistent source data… is often the most time-consuming prerequisite."*

Three things are missing from it, and they are the same three things missing from every version of this document I can find.

**There is no semantic layer.** Its variance agent *"retrieves budget from your planning tool"*. Which budget — the board plan or April's reforecast? Both exist, they disagree by design, and the answer changes every number in the report. Nothing in the playbook says who decides.

**The commentary instruction bakes in a causal error.** *"[Account] was [X]% above budget, driven by [top contributing transactions or vendor names]."* A top contributing transaction is not a cause. That template writes a true fact into a sentence shaped like an explanation, and a reader takes the explanation. It is the single most common way a finance narrative misleads, and here it is as a starter template.

**Their own third question has no answer.** *"How do I know if the agent's outputs are accurate?"* is asked, and then the document moves on. Everything after it — back-tests, an answer key, a review ledger, promotion thresholds — is the part that decides whether any of this is safe, and it is not there.

So: same five agents, same format, three added rows. **The claim is not "I can deploy agents." That sentence was commoditised the day that PDF shipped. The claim is: I know exactly how these agents will be confidently wrong, and I have built the thing that catches it.**

---

## The three rows the format is missing

| | |
|---|---|
| **Promotion criteria** | What must be true, measured, for this agent to move up the autonomy ladder — L0 draft-only, L1 execute-with-approval, L2 autonomous-with-audit. Counted in reviewed instances, not in months elapsed. |
| **Demotion trigger** | The specific event that takes autonomy away, and for how long. An agent that can only be promoted is not governed. |
| **Known failure mode** | The way this agent produces a confident, plausible, wrong answer. Not "it might make mistakes" — the actual mechanism, so a reviewer knows what to look at first. |

Autonomy is earned per **workflow**, never per agent, and it is earned on instances reviewed with no material correction. The review ledger is the substrate: every human correction is captured at the moment it is made, routed to exactly one destination — a definition, a charter, an ingestion rule, a check — and closed only when that destination has produced an artefact.

---

## Agent 1 — Daily reconciliation exception monitor

**Trigger.** Daily, 07:00.

**Tools.** Bank statement (read), general ledger (read), a channel to write a digest to.

**Instruction logic.** Match bank lines to ledger entries on amount, date window and counterparty. Surface unmatched items above the materiality floor. For each, retrieve the counterparty's last three transactions and state what the item resembles — *"same vendor and amount as 11/03"* — without asserting that it is a duplicate.

**Output.** A digest of unmatched items, each with its evidence and a proposed resolution, for review.

**Promotion criteria.** L1 (auto-clearing exact matches, review next day) after **200 reviewed matches with zero corrections** and a documented materiality floor. L2 never — an unexplained difference is a judgement.

**Demotion trigger.** One wrongly auto-cleared item returns the workflow to L0 for 200 instances. A cleared item later reversed is the same event.

**Known failure mode.** **A confident duplicate call on a legitimate repeat payment.** Two identical invoices from the same vendor in one month is what a duplicate looks like *and* what a genuine second delivery looks like. The proposed resolution reads as a finding; the reviewer clears it; the payment was real, and the reversal appears next month as a new exception. Guard: the agent may state resemblance, never conclusion, and the digest names the two candidate readings.

---

## Agent 2 — Variance commentary drafter

**Trigger.** Day 3 of the close, or on request.

**Tools.** Ledger (read), plan (read), the semantic layer (read).

**Instruction logic.** Compute variance against **the plan version named in the semantic layer** — not "the budget", which is ambiguous whenever a reforecast exists. Decompose each material variance into rate, volume, mix and timing before writing anything. Then, and only then, draft one sentence per line, where the sentence names a **decomposed driver**, not a large transaction.

**Output.** A variance table with a draft sentence per material line, each carrying the decomposition it was written from.

**Promotion criteria.** **L0 permanently.** A variance narrative is judgement about causation, and causation is not delegable. What may be promoted is the *table*: the arithmetic, once back-tested.

**Demotion trigger.** Not applicable — it starts and stays at the floor. The measured thing here is edit rate: material edits per close, trending down, are the evidence the drafting is worth having at all.

**Known failure mode.** **The true fact in the causal slot.** Given "gross margin fell 4 points" and "the largest cost line was hosting", the sentence writes itself as *"margin fell, driven by hosting"* — and if margin actually fell because a price change landed mid-month while volume mix shifted, the sentence is true in both clauses and false in its implication. This package's own demonstration is exactly this case, caught by requiring a rate/volume/mix bridge before a sentence may be drafted. **A number and a narrative are not the same artefact and are not approved by the same rule.**

---

## Agent 3 — Accrual gap scanner

**Trigger.** Day 28, before the close opens.

**Tools.** AP ledger (read), vendor contracts (read), accruals schedule (read).

**Instruction logic.** Four tests: a vendor billing monthly with no bill this period; a bill dated in the period that arrived after it; a committed contract with no bill against it; a prior-period accrual neither reversed nor billed. Estimate from the vendor's own history, and carry the basis, the number of months it was drawn from, and the spread of what was observed.

**Output.** Observations with estimates and bases. **No verdict field** — nothing says an accrual should be raised.

**Promotion criteria.** **L0 permanently on the estimates.** A new estimate changes a reported number relative to what a human approved, which is what the human is for. The *reversal* of an approved accrual is promotable on the ordinary schedule-continuation test: six closes, zero corrections.

**Demotion trigger.** One corrected reversal returns the class to L0 for six closes.

**Known failure mode.** **A median mistaken for a forecast.** The estimate is the middle of a vendor's history, and a history is only predictive if the arrangement held. A renegotiated contract, a switch to annual billing, or a service quietly cancelled all produce a confident monthly number for a cost that no longer exists — and it will be accrued, and it will sit there. Guard: where the observed spread exceeds half the median the estimate is reported as unusable, where the basis is under three months the shortage is named in the memo, and a vendor whose contract has lapsed is escalated rather than drafted.

**What it cannot see.** Open purchase orders — this package has no PO register. Anything held only in someone's head. Both are stated in the output, because silence about them is what makes a scan look complete.

---

## Agent 4 — Close status digest

**Trigger.** Daily at 08:00 during close week.

**Tools.** Close checklist (read), ledger (read, for period lock), a channel to write to.

**Instruction logic.** Report each open task, its owner, whether it is past its target, and what is blocking it. Distinguish **not started**, **blocked on someone**, and **blocked on data**, because the three have different remedies and only the first is about effort.

**Output.** A morning digest: overdue, due today, completed since yesterday, and blockers with names against them.

**Promotion criteria.** L2 — fully autonomous — after 20 digests with no factual error. It is the one workflow here that can reach the top of the ladder, because **it changes no number.** Reporting status is not an accounting judgement.

**Demotion trigger.** One digest that reports a task complete when it is not. Status that cannot be trusted is worse than no status, because the whole point is that nobody re-checks it.

**Known failure mode.** **Completion inferred rather than evidenced.** If "complete" is derived from a checkbox rather than from the artefact the step was supposed to produce, the digest reports a green close over a step nobody did. Guard: a step is complete when its evidence artefact exists, and the digest names the artefact.

---

## Agent 5 — AP bill coder and router

**Trigger.** A new bill arrives.

**Tools.** AP (read/write), chart of accounts (read), approval workflow (write).

**Instruction logic.** Retrieve the vendor's last five bills, take the account coding used, and apply it — or flag where the vendor is new, the coding was inconsistent, or the description does not match the pattern. Route on amount, against a documented approval matrix.

**Output.** A coded bill routed to an approver, with a note saying whether the coding matched prior treatment or diverged from it.

**Promotion criteria.** L1 (code and route without pre-approval, reviewed after) after **300 bills with zero coding corrections**, and only for vendors with five or more consistently coded prior bills. New vendors are L0 for their first five bills, always.

**Demotion trigger.** Three coding corrections in one month, or one miscoding that crosses a capitalisation boundary — expense treated as asset or the reverse — which returns the workflow to L0 immediately regardless of the count, because that error moves EBITDA.

**Known failure mode.** **Yesterday's coding, faithfully repeated.** The agent's rule is "code it the way this vendor was coded before", so a vendor miscoded once is miscoded forever, and consistency is mistaken for correctness. The check that catches it cannot be inside this agent — it is the quarterly account-level review of vendors by coding, which asks whether the pattern is right rather than whether it was followed.

---

## The five questions, answered

The market's playbook ends with five questions and the instruction to stay in draft mode until you can answer them. That is right, and it is a checklist. Here are the answers this package ships with, as machinery rather than intention.

| Their question | What answers it here |
|---|---|
| Who reviews and approves before it affects the books? | The charter names the reviewer per workflow, and the review ledger records who, when and what they changed. |
| What happens on an exception the agent can't handle? | Each charter carries an escalation clause with a named destination. An agent that flags its own uncertainty and is wrong is behaving correctly; the ledger has a column for exactly that, because an agent that was wrong and *confident* is the dangerous one and the two must be distinguishable in the statistics. |
| How do I know the outputs are accurate? | Back-tests with held-out periods, an answer key on the demonstration instance, and per-agent metrics — edit rate, material-correction rate, instances since last correction. |
| What's the audit trail? | The review ledger, from entry 1, which is the install itself. Every correction is routed to a definition, a charter, an ingestion rule or a check, and closed only when that artefact exists. |
| Who owns the logic and updates it? | The charter is the logic, it is a text file under version control, and a change to it is a ledger entry with a reason. |

---

## The honest caveat about the source

That PDF is a lead magnet for an ERP, and *"five agents you can deploy this month"* is doing sales work. Its own prerequisites list quietly contains months of effort — clean data, consistent coding, permissions, a validation process — acknowledged in a sentence and then stepped over. **The gap between that sentence and the reality is the entire reason this package exists**, and it is why the first thing it produces is not an agent but a verdict on whether your data can support one.

*Recorded 21 Aug. The two workflows this read added — the day-28 accrual scan and audit preparation — are built and shipped in `accrual_scan.py` and `audit_pack.py`, and both are in the Bookkeeper's charter with their promotion criteria, demotion triggers and failure modes.*
