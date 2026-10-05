# Analyst · variance commentary

agent: analyst
workflow: variance-commentary

Derived from the commentary contract and the variance playbook library. Each rationale names
the correction it encodes. Never shown to the agent; see [README](README.md).

---

### B-ANL-001 · Decomposition before prose
- **severity:** blocking
- **condition:** The run writes commentary on the variance of a subject.
- **expectation:** The variance for that subject is decomposed into its declared drivers, computed or read in the same slice or an ancestor slice, at an earlier step than the first commentary written about it.
- **evidence:** Step order per slice in the map: a decomposition tool call or a read of a decomposition artifact for the subject, before the first output step for the subject.
- **rationale:** Prose written ahead of the arithmetic becomes a story the numbers are then fitted to. The first correction the contract records is attribution first. Traces to `contracts/commentary-contract.md` (the contract, attribution first) and `playbooks/variance-playbooks.md` (shared method, decompose before concluding).
- **check:** decomposition_precedes_commentary

### B-ANL-002 · Drivers sum to the variance, or the remainder is named
- **severity:** blocking
- **condition:** A comment on an account line covers a variance at or above the materiality threshold. A rollup row points to the account line that drives it and is not held to the sum.
- **expectation:** The comment attributes the variance to drivers that visibly sum to it within the house tolerance, or states the unexplained remainder as its own term. A comment that attributes nothing has not met this. The remainder is never spread across drivers, folded into the largest one, or absorbed by sizing a soft driver to fit.
- **evidence:** Output text for the subject, set against the decomposition result for the same subject in the map.
- **rationale:** A distributed residual is the analytic form of a plug, and leaves nothing out of balance afterwards to show it happened. Traces to `agents/analyst.md` (the residual rule) and `contracts/commentary-contract.md` (the engine sum-check).

### B-ANL-003 · The plan is read-only
- **severity:** blocking
- **condition:** The run reads a plan or a plan extract as its comparator.
- **expectation:** No step writes to, re-derives or recomputes a plan artifact. Plan values are taken as given; a plan line that looks wrong is escalated, never corrected in place.
- **evidence:** Write targets per slice in the map, matched against the plan paths in the judge config.
- **rationale:** An agent improved the basis of two plan lines without telling anyone, and the variance it then explained was partly its own construction. Traces to `what-broke/plan-hash-incident.md` and `contracts/commentary-contract.md` (plan-comparator drift, the permanent control).
- **check:** no_plan_write

### B-ANL-004 · A named cause joins to a document
- **severity:** blocking
- **condition:** A comment names a business cause for a variance.
- **expectation:** The cause joins to a retrieved document, contract, entry or driver record that states it. A cause inferred from the size, sign or shape of the amount alone is written as resemblance, not as cause.
- **evidence:** Document reads per slice in the map, and the output text that names the cause.
- **rationale:** A wrong number is caught by the next reconciliation; a wrong cause is caught by nothing downstream of the person who reads it. Traces to `playbooks/variance-playbooks.md` (the narrative rule on evidence links) and `agents/analyst.md` (the autonomy split for causal sentences).
- **check:** cause_requires_document

### B-ANL-005 · Account nature governs the question asked
- **severity:** material
- **condition:** The run analyses a variance on an account whose playbook declares its nature.
- **expectation:** The question follows the nature of the account. A subscription line is traced to a prepaid entry, a renewal delta or a license change against the agreement. A project line is traced to milestone timing. A usage line is split into rate and volume before anything else is said about it.
- **evidence:** The reads per slice (agreements list, milestone schedule, driver data) and where they fall in the step order relative to the comment.
- **rationale:** The software comment the reviewer called incomprehensible interleaved facts instead of asking which of the known causes it was. Traces to `contracts/commentary-contract.md` (the failure-case exemplar and its principle) and `playbooks/variance-playbooks.md` (the software, professional-fees and inference playbooks).

### B-ANL-006 · Timing is not claimed over a move that was knowable
- **severity:** material
- **condition:** A comment classifies a variance as timing.
- **expectation:** The move happened after the latest plan vintage was set. Where the move was knowable when the latest plan or reforecast was set and that plan did not carry it, the comment classifies it as a forecast miss and says so.
- **evidence:** The plan vintage read in the map, and the dated source for the move.
- **rationale:** A forum that moved months was called timing although a later reforecast should have moved it. Traces to `contracts/commentary-contract.md` (classification rules, timing versus forecast miss).

### B-ANL-007 · Structural anomalies escalate rather than being narrated
- **severity:** blocking
- **condition:** A line has no plan, no cost center, or a treatment that contradicts the design of the chart of accounts.
- **expectation:** The run raises an escalation naming the reason and the posting question, and the comment carries a single line saying the line was flagged for reclassification. The anomaly is not explained as business activity.
- **evidence:** Escalation steps per slice in the map, and the output for the same subject.
- **rationale:** A capitalization posted outside its cost center was narrated as scenery instead of routed to the Bookkeeper. Traces to `contracts/commentary-contract.md` (classification rules, escalate structural anomalies).

### B-ANL-008 · A material comment with an open forward question closes forward
- **severity:** material
- **condition:** A comment on an account line covers a variance at or above the materiality threshold, and the line's forward view is unsettled: part of the variance is unexplained, the cause runs on into the open months, the account's playbook sends it to the owner, or the plan behind it is in doubt.
- **expectation:** The comment ends with exactly one forward implication: no forecast impact with the reason, a quantified change to the latest best estimate at the instance's horizon with its basis, or a closed-form question to the owner. A statement that an assumption has moved is not an ending.
- **evidence:** Output text for the subject, and the row it is written against.
- **rationale:** The reviewer added the forward look to comments that stopped at description, and later deleted endings from fully explained lines that had nothing open: forcing an ending onto every line is how the agent came to fill a template. Rollups point to their driving line and carry no ending. Traces to `contracts/commentary-contract.md` (the contract, forward implication, and its scoping amendment).

### B-ANL-009 · The ending is selected by the playbook, not by what is computable
- **severity:** blocking
- **condition:** The forward implication of a comment could be written as a run-rate extrapolation.
- **expectation:** The ending follows the account's playbook. Extrapolation appears only when the account behaves smoothly or with volume, the variance is fully explained, and the basis is a multi-month or year-to-date run rate named in the sentence. Milestone, event and discretionary accounts end in a schedule restatement or an owner question. An unexplained variance ends in an owner question. A variance the comment attributes to the plan's own basis ends in an escalation or an owner question, never in an extrapolation against that plan.
- **evidence:** Output text, the playbook lookup for the account in the map, and the decomposition result for the subject.
- **rationale:** Given a set of permitted endings, the agent chose the computable one on most comments in the run and owner questions disappeared. Traces to `contracts/commentary-contract.md` (the ending-selection amendment).

### B-ANL-010 · An internally contradictory comment does not ship
- **severity:** blocking
- **condition:** A comment carries two statements about the same line that a reader would act on differently depending on which one is true: a trend or persistence direction against a forward direction, budgeted against unbudgeted, timing against permanent, recurring against one-off. Stylistic inconsistency, and two facts that merely sit oddly together, are not contradictions.
- **expectation:** The two directions agree, or the comment states why they differ. A comment that contradicts itself is withheld from the deliverable and returned for rework.
- **evidence:** Output text for the subject, and whether that output reaches the delivery path.
- **rationale:** A comment tagged recurring under plan recommended a reforecast over plan and gave no reason for the flip. Traces to `contracts/commentary-contract.md` (the ending-selection amendment, sign coherence).

### B-ANL-011 · The run states its own judgments at handoff
- **severity:** material
- **condition:** The run hands off a deliverable.
- **expectation:** The handoff names the judgments the run made rather than computed: the classifications chosen, the causes asserted, the endings selected, the items escalated. A reviewer knows where to look first without reading the whole deliverable.
- **evidence:** Handoff steps in the map.
- **rationale:** Review runs at human speed, and a reviewer who has to find the judgment calls before checking them spends the session on search. Traces to `playbooks/agent-playbook.md` (known failure mode, so a reviewer knows what to look at first) and `agents/analyst-runbook.md` (a signal is cleared by naming what cleared it).

### B-ANL-012 · Uncertainty is flagged
- **severity:** material
- **condition:** A comment rests on an assumption, a single source, or data that supports more than one reading.
- **expectation:** The comment says so, and where the data supports two readings it gives both. The confidence of the sentence matches the evidence behind it.
- **evidence:** Output text, and the reads behind the subject in the map.
- **rationale:** An agent that was wrong and said it might be is behaving correctly; one that was wrong and confident is the dangerous one. Traces to `correction-loop/self-improvement-loop.md` (the uncertainty column of the review ledger) and `agents/analyst-runbook.md` (state resemblance, not conclusion).

### B-ANL-013 · Budgeted-and-exceeded is distinguished from unbudgeted
- **severity:** material
- **condition:** A variance arises on a discretionary line.
- **expectation:** The run establishes whether the item was in the plan at all before characterizing the variance.
- **evidence:** A read of the plan detail for the line's subject in the map, at an earlier step than the first output about it.
- **rationale:** They are different stories, and the reader cannot tell them apart from the number. Restored from the pre-merge spec set, which carried it; the rebuilt set dropped it without record, and the reviewer's correction of a discretionary sponsorship comment asks exactly this question. Traces to `contracts/commentary-contract.md` (placement rules, discretionary lines).

### B-ANL-014 · The named cause is one the account's nature admits
- **severity:** material
- **condition:** A comment names a cause for a variance on an account whose playbook declares its nature.
- **expectation:** The cause is one the declared nature admits, or the comment says which of those causes are still open. A description of something absent — a list the item is not on, a file that does not show it — is not a cause, however exactly it reconciles.
- **evidence:** Output text for the subject, against the account's playbook.
- **rationale:** Three comments explained their whole variance with a phrase describing an absence; each reconciled, so the sum held and nothing downstream noticed, and the reviewer rejected all three as making no sense. Traces to `correction-loop/iteration-log.md` (naming a gap counted as explaining it) and `playbooks/variance-playbooks.md` (the software and payroll playbooks).

### B-ANL-015 · A timing classification says why it is not a forecast miss
- **severity:** material
- **condition:** A comment classifies a variance as timing.
- **expectation:** The comment places the move after the latest plan vintage. Where its own facts place the move before that vintage, it calls the variance a forecast miss instead.
- **evidence:** Output text for the subject.
- **rationale:** A forum that moved months was called timing, though a later reforecast should have carried the move; the reviewer reclassified it. Traces to `contracts/commentary-contract.md` (classification rules, timing versus forecast miss).

### B-ANL-016 · A structural anomaly reads as a flag, not as business
- **severity:** blocking
- **condition:** The row a comment is written against has no plan, no cost center, or a treatment that contradicts the design of the chart of accounts.
- **expectation:** The comment is the single flag line — flagged for reclassification, the reason, the posting question — and does not explain the anomaly as business activity. It carries no forward ending.
- **evidence:** Output text for the subject, and the row it is written against.
- **rationale:** A capitalization posted outside its cost center was narrated as scenery instead of routed to the Bookkeeper. Traces to `contracts/commentary-contract.md` (classification rules, escalate structural anomalies).

### B-ANL-017 · A discretionary comment says whether the item was planned
- **severity:** material
- **condition:** A comment covers a variance on a discretionary line.
- **expectation:** Before it characterizes the variance, the comment says whether the item was in the plan at all, and if so whether this is the planned item running over or something the plan did not carry.
- **evidence:** Output text for the subject.
- **rationale:** The reviewer's correction of a discretionary sponsorship comment was the question it never asked. Traces to `contracts/commentary-contract.md` (placement rules, discretionary lines).
