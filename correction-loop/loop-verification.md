# 39 — The loop verified

**Date** 18 August 2026 · **Status** complete

The improvement loop has been instrumented since this morning: sixteen corrections, each routed to one destination, each closed against a resolvable artefact. **None had ever been shown to change an outcome.** A loop that records corrections and a loop that prevents recurrences look identical on a dashboard.

This is the flush.

---

## The test

Yesterday's review session found four contracts where the agent had **derived** a term expiry with the wrong renewal length and then reported the result **as read from the document header**. The header said otherwise. The correction produced Ingestion charter v1.1 and a new rule 3: *a value you derived is not a value you read.*

The four contracts were re-extracted blind, by two independent agents, against the amended charter. Neither was told what the previous run got wrong, and both were forbidden from reading any prior extraction.

Two things were added to make it a real test rather than a demonstration:

- **A control** — CLB-0007, extracted correctly under v1.0. If the amendment broke correct behaviour, it would show here.
- **A genuine contradiction** — CLB-0077, where the document really does contradict itself. An amendment that stops an agent raising false escalations by stopping it raising escalations is worse than the disease.

---

## The result

**All four now read the header and get it right.** 2027-04-14, 2027-01-12, 2027-04-28, 2027-06-10. Every one marked `basis: read`, with the quoted words and their location.

**Zero false contradiction escalations.** All four verdicts moved **CONTRADICTED → AGREES**.

And the reasoning is explicit in the output, unprompted:

> *Clause 1's 28 April 2026 is the expiry of the INITIAL term; the header states the CURRENT term expiry after one renewal. These are two different fields and are not a self-contradiction. Rule 3 applies: no contradiction escalation is raised on the basis of any expiry date I could calculate.*

Where the agents did compute a date, they emitted it as a separate field marked `derived`, listed its inputs, and — as the rule requires — **cited no document location**, because no location contains it:

> *Computed, not read. The document nowhere states a current-term start date. Emitted with no location because no location contains it. Used only as a check against the ledger; may not be, and is not, the basis of any contradiction escalation.*

**The control was unaffected** — and produced a new finding of its own: the ledger flags CLB-0007 as `partner_sourced = True` while the contract contains no partner, referral or commission clause anywhere. Either a partner agreement exists that nobody has indexed, or the flag has no economic effect. Different consequences, and only the partner agreement settles it.

**The real contradiction still escalated.** CLB-0077 was not suppressed. It was reclassified honestly:

> *Rule 3 applies here and I am explicitly not raising a self-contradiction... Both differences are produced by my arithmetic, not by the document. The stated values govern.*
>
> *The doubt sits with my method first — a 28 December date is consistent with a day-count convention the clause does not spell out. Raised as a question, not a defect... **Escalating this as a contradiction would repeat review ledger RL-0024, where four contracts were wrongly flagged on computed expiry dates.***

**The agent cited the correction that produced the rule, by ledger ID, as its reason for behaving differently.**

That is the loop closing, observed rather than asserted. A human correction became a charter amendment, and a later run applied it by name. Sixteen corrections were recorded; this is the first one demonstrated to prevent a recurrence.

---

## Defect 16, found by the re-extraction

Both batches, independently, flagged the same thing — and both got the framing right.

The ledger's `current_term_start` was computed as expiry minus the **initial** term length. On a contract that has renewed, the current term is a *renewal* term, so on every 24-month contract that has renewed the current term started a year earlier than recorded. **23 of 65 renewed contracts.**

Neither agent called it a document defect. Both called it a question about their own arithmetic:

> *The document is silent on current_term_start, so this is not a document/ledger disagreement... My arithmetic is the thing to check first; raised as a question for the ledger owner, not as a finding against the document.*

That is exactly the posture rule 3 was written to produce, applied to a case the rule was not written about. The agents were right and the ledger was wrong.

**What it would have cost:** `current_term_start` feeds renewal-date reporting. Every 24-month contract's 60-day notice window would have been diarised a year early — which is the failure mode the Chief of Staff's calendar exists to prevent, arriving through a field nobody was watching.

Fixed, with a regression check. **89/89 checks pass.**

---

## Where the ladder stands

| | Ingestion |
|---|---|
| Instances reviewed | **245** |
| Material correction rate | **1.63%** (ceiling 2%) |
| Escalation recall | **100%** |
| Escalation precision | **75%** |
| Acceptance rate | **2.45%** |
| Calendar months | **0** of 3 — blocked |

The improvement loop is **16 of 16 closed against resolved artefacts**, and one of those sixteen is now evidenced rather than merely recorded.

Acceptance rate rose from 0% to 2.45% — six instances approved with no edits, out of 245. It remains a number that would be meaningless alone and is honest beside the other four.

---

## What this does to the argument

The claim available this morning was *"the improvement loop is closed and instrumented."* The claim available now is stronger and is the one that matters:

> **A human corrected an agent. The correction became a versioned rule. A later run of that agent applied the rule, cited the correction by ID, and did not repeat the error — while still escalating a real problem it would have been easier to stay quiet about.**

That is the Level 3 answer to *"name the system you built, what it replaced, and what broke when it ran unattended"* — and it is evidence rather than architecture.

The honest limit: one correction, one agent, six documents, one cycle. It is a demonstrated mechanism, not a demonstrated track record. The distinction is the same one the ladder makes, and it should be stated in those terms rather than inflated.

---

## Carried forward

- **Reporter next.** It completes the Bookkeeper → Analyst → Reporter chain the Day 8 checkpoint measures, and it is where every prior agent's caveats either survive or get laundered.
- The `partner_sourced` finding on CLB-0007 is unresolved and is a real question.
- Ingestion remains three months from promotion. Nothing can shorten that.
