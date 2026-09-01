# 26 — Ingestion at volume: 48 contracts, four independent agents

*18 Aug 2026. The batch test that Day 4 needed. Four agents, twelve contracts each, working independently from the same charter with no coordination. The result validates the charter approach and condemns the generator.*

---

## Setup

48 club agreements — the four planted traps plus 44 chosen at random, spanning all three contract templates. Four agents, each given only the charter, its twelve PDFs, and the ledger record for each. No shared context, no cross-talk.

## Verdicts

| | Batch 1 | Batch 2 | Batch 3 | Batch 4 | Total |
|---|---|---|---|---|---|
| AGREES | 11 | 11 | 10 | 9 | **41** |
| CONTRADICTED | 0 | 1 | 2 | 3 | **6** |
| INCOMPLETE | 1 | 0 | 0 | 0 | **1** |
| Escalations | 8 | 4 | 6 | 5 | **23** |

**Not one agent, in 48 documents, made a document agree with the ledger.** That was the failure mode the charter was written to prevent, and it did not occur once.

## What the agents found

They caught the planted traps: the federation's blank countersignature date, its unrepresentable revenue share and volume cap, the arrears cadence. Expected.

Then they found **four defects nobody had planted**, three of which I introduced myself the previous day while fixing something else.

**Renewals rolled forward by the wrong period.** Clause 1 says agreements renew in "successive twelve (12) month terms." The generator rolled expiry forward by the *initial* term length. On a 12-month contract the two are identical, which is why it went unnoticed — it is only visible on 24- and 36-month agreements. Three of the four agents found it independently, and batch 3 went further: *"only visible on contracts whose initial term is not 12 months, so it needs a population-level sweep."*

**Currency contradicted itself.** US clubs carry USD in the ledger and in the contract header, while clauses 2 and 4 priced in EUR, with no FX basis stated. Two agents flagged it. One noticed the ledger field is named `annual_minimum_eur` on a USD contract — a data-contract naming defect, not just a rendering one.

**The federation contract stated two different minimums.** Special condition S1 said €96,000; the standard clause 3 said €40,000. Batch 1 caught it and quantified the exposure: *"EUR 56,000/yr may be understated on the largest club in the batch."*

**Month arithmetic clamped to day 28.** Batch 4: *"stated term dates are two days short of the 12 months the same document specifies, shifting the minimum measurement period and the 60-day notice deadline."*

All four are fixed. Renewals now roll in 12-month terms, clause text follows the contract's own currency, the federation carries one minimum, and month arithmetic respects real month lengths. 78/78 validation checks still pass.

## Findings nobody asked for

Three observations came back that were outside the task and are better than the task.

Batch 2, unprompted, on the whole population: *"in four contracts the stated annual minimum exceeds the stated annual platform value, so those minimums can only be met with match-analysis consumption."* That is a genuine commercial insight — those accounts are structurally dependent on usage to avoid a shortfall invoice, and nobody had looked.

Batch 3 spotted a contract expiring **the following day** with its 60-day notice window already closed, so it auto-renews, while the ledger still shows zero renewals.

Batch 2 questioned the evidence of execution itself: signature blocks carry typed names and dates, but the signature lines are blank rules with no e-signature certificate in the text layer. *"Dates are high confidence; execution status is medium, and it determines whether any of these should instead be INCOMPLETE."* That is the right question and I had not thought to ask it.

## What this settles

**The charter approach works.** Four agents, no coordination, converged on the same defects and used the verdict vocabulary consistently. The behaviour that mattered came from the prohibitions, exactly as the first run suggested.

**Escalation recall is the metric that earns its place.** Doc 19 argued that escalation recall — what the agent missed — matters more than acceptance rate. This run inverts the usual worry: the agents did not miss things, they found things nobody was looking for. Twenty-three escalations against four planted traps.

**"A term I cannot represent" was the highest-yield escalation category.** Every batch raised it. Clause 5's equipment obligation — one camera per court, title retained, removal within thirty days of termination, 82 units in batch 4 alone — has no field anywhere in the data contract. It is an asset-recovery obligation that currently exists only in prose. That category did not exist in doc 03 and now justifies itself.

**Material correction rate: zero.** Not one extraction had to be corrected. The corrections all landed on the *documents*, not the agents. On doc 19's promotion criteria that is 48 of the 200 instances needed, with escalation recall at 100% so far.

## The honest caveat

These are synthetic contracts generated from three templates. Real agreements are negotiated, redlined, scanned, and occasionally photographed. The 48 here are far more uniform than any real corpus, so a zero correction rate proves the charter is sound, not that extraction is solved.

The next real test is documents nobody generated — which is why the messy fixture and, eventually, actual contracts matter more than another 200 of these.

## Where this leaves Day 4

Complete. The document repository exists, the ingestion charter is written and validated at volume, and the STALE/CONTRADICTED verdicts that doc 24 left unbuilt are now demonstrated on real documents.

Day 5 is the semantic layer — and it now inherits three new open questions from this run: how to represent revenue share, volume caps and equipment obligations; whether "no minimum" and "minimum of zero" are the same thing (four agents flagged the difference, and they are right that it matters); and what counts as evidence of execution.
