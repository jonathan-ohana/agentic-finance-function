# 38 — The first human review session

**Date** 18 August 2026 · **Reviewer** Jonathan · **Status** complete, 6 decisions recorded

The first time a human judged anything this workforce produced. Before it, every trust metric in the system read *not computable* and no agent could move.

---

## What it changed

**Ingestion, before and after:**

| Criterion | Required | Before | After |
|---|---|---|---|
| Instances reviewed | 200 | 0 | **239** |
| Material correction rate | ≤ 2% | not computable | **1.67%** |
| Escalation recall | 100% | not computable | **100%** |
| Calendar months | 3 | 0 | 0 |

**Three of four criteria met on evidence. Blocked by time.**

That is the asymmetry working as designed. Accuracy can be demonstrated in an afternoon; tenure cannot be bought. Escalation precision is now computable too, at **75%** — three of four judged escalation classes were warranted.

The improvement loop went from 12 corrections to **15, all closed against resolved artefacts.**

---

## The reviewer refused to route before diagnosing, and was right

Presented with five wrong dates and asked where the fix should go, the answer was:

> *"I think we need to understand why the agent got it wrong so that it can learn from it, no?"*

And again, on routing: *"I need to understand the root for the mistake to understand where the errors needs to be routed."*

That is the `root_cause` field doing its job, and it is the difference between a ledger that compounds and one that accumulates. **I had already proposed a route before diagnosing, and my proposed route was wrong.**

### What the diagnosis found

Four contracts had a term expiry a year late. My first reading — reported to the reviewer — was that the agent had repeated the same renewal-arithmetic bug the agents had earlier found in the generator. Plausible, and false.

The agent's escalation said:

> *"The header summary states 'Current term expires: 28 April 2028 (renewed 1x)'."*

**The header says 28 April 2027.** All four do. And the documents are internally consistent: clause 1 gives a 24-month initial term expiring 2026, renewing in successive **twelve**-month terms. 2026 + 12 = 2027. Header agrees. Ledger agrees.

2028 is 2026 + 24. The agent **computed** the date using the initial term length instead of the renewal length, and then **reported the result as something it had read in the header.**

That is not an arithmetic error. It is a **derived value presented as an observed one**, and a self-contradiction escalation raised against a document that does not contradict itself. The agent manufactured the conflict and cited a source that says otherwise.

The Ingestion charter already named this failure mode in its first rule — *"an agent that quietly makes the document agree with the data it was also given"* — but the rule was written about the ledger. Here the agent made the document agree with **its own arithmetic**, which the rule did not cover.

### The fifth case went the other way

CLB-0077 looked like a two-day extraction error. It was not. The header says 30 December 2026; clause 1 says a 12-month term from 30 December 2024 expiring **28 December 2025**. That document genuinely contradicts itself — the day-28 clamping defect surviving in the paper. The agent followed the clause, flagged it, and escalated correctly.

The reviewer had already ruled "a date is a date — material." The ruling stands as a materiality principle; the case it was applied to turned out to be the agent being right.

**Net: four material errors in 239 instances, not five. 1.67%, not 2.09%.** The difference between promotion blocked and promotion earned came down to diagnosing one case properly.

---

## The artefacts the session produced

Every correction routed to exactly one destination and produced something.

**1. Ingestion charter v1.1 — a new rule 3, *A value you derived is not a value you read.***

> An extracted field must be **quotable**. If you cannot point at the words in the document that contain it, you did not extract it — you computed it.
>
> - A derived value may never be the basis of a contradiction escalation. If your arithmetic disagrees with a stated value, the stated value governs and your arithmetic is the thing in doubt.
> - Reporting a computed number as a reading is worse than reporting it wrongly, because it launders an inference into an observation and every downstream reader treats it as fact.

**2. Evidence trigger TR-01 — the first improvement-loop entry originating from a human rather than a defect.**

On the federation contract's conflicting minimums, the reviewer's instinct went further than the escalation:

> *"Maybe the next step would be to look for an email, video chat transcript, some form of communication that would explain the gap between S1 and clause 3."*

Nothing triggered that search. Now something does: when Ingestion escalates a document contradicting itself on a material term, Evidence sweeps every connected source for the communication that resolves it. The rationale is sound and nobody had written it down — *a contract that contradicts itself was drafted by people who were talking to each other at the time, and the resolving sentence usually exists outside the contract repository.*

**3. A standing ruling on escalation posture**, from the reviewer:

> *"Escalation is good as a first principle. As we refine the framework, we'll learn better what needs escalation and what doesn't."*

Recorded as applying to every agent, not just Ingestion.

**4. Counting rule for repeated escalations.** Four false escalations, one root cause, recorded as **one** unwarranted escalation. Precision should measure judgement quality, not blast radius — counting four would punish the agent for the size of the corpus, and if the same bug had touched forty contracts a single root cause would destroy the metric. That creates a quiet incentive to escalate less on large batches, which is backwards.

The legitimacy of that rule rests entirely on the diagnosis having been done. Skip it and *count as one* becomes a way to shrink any number.

---

## Two defects in my own instrumentation, both caught by the session

**Defect 14 — the correction rate read 100%.** The ledger had `instance_count` but no field for *how many of those instances were in error*. A batch of 239 with 4 wrong dates scored as 239 errors. Added `instances_corrected`; the rate now reads 1.67%.

The failure mode is worth naming: the metric was wrong in the direction that **blocks** promotion, so it would never have been questioned by anyone hoping to promote an agent. It was caught because the number was absurd on sight, not because anything tested it.

**Defect 15 — escalation precision was permanently uncomputable.** The scorer looked for a reviewer's name on the row where the agent *raised* the escalation. That row is written by the agent and never carries a reviewer, so precision could never be computed no matter how many escalations were judged. Raising and judging are different rows and the scorer now pairs them. Precision: **75%**.

---

## What is still not measured

Five of six agents have **zero reviewed instances**. The close pack, the variance pack, the opportunity register and the standup were all put in front of the reviewer and none was ruled on — the session went deep on Ingestion instead, which was the right trade for a first sitting but leaves four artefacts unjudged.

Acceptance rate for Ingestion is **0%** — the batch was approved *with edits*, so nothing was approved clean. That is correct and it is the number that should never be shown alone: 0% acceptance alongside 100% recall and 1.67% correction rate describes an agent that is accurate, honest about its uncertainty, and had one genuine flaw. A single figure would have described none of that.

---

## Carried forward

- **Ingestion is three months from promotion and nothing can shorten that.** The only remaining criterion is tenure.
- Four artefacts still unreviewed. Each is one decision.
- The four contracts with wrong extracted dates should be re-extracted under charter v1.1 — the test of whether the amendment works.
- KPI-05 recovered is still **$0**. Every finding remains analysis until someone acts on it.
