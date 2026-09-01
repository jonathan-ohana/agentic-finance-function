# 25 — The first agent run

*18 Aug 2026. The Ingestion charter, written portable and executed against real documents. The point of this run was not extraction — it was to find out whether the Claude-native charter approach committed to in doc 22 actually works before six more agents are built on top of it.*

---

## What was tested

`package/charters/ingestion.md`, version 1.0, run at L0 draft-only against three documents: a club master agreement, its amendment, and the federation contract. Output at `example/agent_runs/ingestion/run_2026-08-18.json`.

The charter has four rules, and each was deliberately put under pressure.

**Extract what is written, not what is expected.** The master agreement says 4 courts; usage records say 10. The agent extracted **4**, flagged the disagreement, and did not reconcile. This is the failure mode that matters most in document extraction — an agent quietly making the document agree with the data it was also shown — and the rule held.

**Absence is a finding, never a value.** The federation contract's countersignature date came back `null`, with a location ("signature block, right column"), a reason ("date line blank"), and an escalation. It did not become the signature date.

**Every field carries provenance.** Every extracted value names its clause.

**Say how confident you are, per field.** One field came back `low` — and produced the most interesting result of the run.

## Four exceptions, and none of them resolved

**EXC-001, HIGH.** A signed order form dated 2026-01-15 authorises 10 courts. The customer master records 4. Usage already meters 10. So the company is delivering against ten courts and billing against four. Exposure: roughly €3,738 unbilled to date, plus an allowance understated by 720 matches a month, which suppresses overage revenue on top.

**EXC-002, HIGH.** €40,125 invoiced against a contract that may not be binding, carrying a €96,000 minimum, a 12% revenue share and a 180,000-match cap.

**EXC-003, MEDIUM — and the one I did not anticipate.** The federation contract's revenue share and volume cap **have no field in the data contract**. The agent recorded them as free text and escalated, because a term you cannot represent is more dangerous than a term you get wrong: it disappears entirely. The revenue share is an unrecognised liability; the volume cap is an unmonitored obligation. This is the charter's escalation rule doing exactly what it was written for, and it produced a change request against the data contract rather than a silently dropped clause.

**EXC-004, MEDIUM — the agent found a bug in the generator.** The master agreement stated an initial term of 12 months from March 2024 *and* an expiry of March 2027. Both cannot be true. The expiry had been restated on renewal without amending the term language — which real agreements do not do.

The agent's confidence on that field was `low`, and under rule 2 it declined to emit a value it would defend. It reported the contradiction instead.

That defect is now fixed: contracts state the initial term expiry correctly and carry a separate "current term expires" line showing renewals. All 78 validation checks still pass, and the document set was regenerated.

**This is the third time producing or reading the paper has caught something the numbers alone did not.** First the contract end dates that never rolled forward, then the arrears cadence, now this.

## What this tells us about the implementation decision

The charter approach works, with three qualifications worth recording before Day 6 builds five more.

**Charters must forbid, not just instruct.** The valuable behaviour in this run came from the prohibitions — do not reconcile, do not infer, do not normalise, do not skip the unusual document. An instruction-only charter would have produced a tidier and less useful result.

**Confidence must be per field, not per document.** A document can be 95% unambiguous and contain one field that decides a revenue classification. Document-level confidence would have averaged EXC-004 away.

**The escalation categories need one that did not exist in doc 03.** "A term I cannot represent" is different from "a term I cannot read." The first is a data contract gap; the second is an extraction failure. Only the second is the agent's fault, and conflating them would have hidden EXC-003 entirely. This should go into Fable #3's charter design for all six agents.

**And one honest limitation.** Three documents were processed here, carefully. The promotion criteria in doc 19 require 200+ with a material correction rate under 2%. Nothing about this run says the charter holds at volume — it says the charter is worth running at volume, which is a different and weaker claim. The batch run over all 239 contracts is Day 4's remaining work.

## The field worth the whole exercise

> "This Order Form co-terminates with the master agreement on 13 March 2027. It does not extend the initial term."

That sentence decides whether €6,408 of annual value is **expansion** or **new business** in the ARR movement. It exists nowhere in any system. It exists only in the paper, in a sentence a person had to read.

That is the argument for the document layer, for the ingestion agent, and for the whole thesis, in one line.
