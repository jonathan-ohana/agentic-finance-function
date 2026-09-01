# 37 — Finance observability: the six KPIs, and the pricing change that took 350 days

**Date** 18 August 2026 · **Status** built and run · **Source** doc 34, the Finance Systems Engineer analysis

Two things to build came out of the FSE reading: **adopt the metric list as the demo's headline KPIs**, including one that wasn't planned, and **adopt the vocabulary** — "finance observability" is the drift auditor and the tie-out suite under the market's own name.

Both are done. The unplanned metric turned out to be the best thing in the set.

*(Housekeeping: doc 34 collided with the two-loops write-up, which has moved to 36.)*

---

## Why "finance observability" is the right borrow

Engineering has had this idea for a decade: you do not find out your system is broken from your customers. You instrument it, you watch the instruments, and you get told before anyone outside notices.

The package already had both halves and no name for them:

- **The tie-out suite is the assertion layer** — 88 checks that must hold.
- **The Drift Auditor is the alerting layer** — the agent that watches whether the checks are still being *evaluated at all*.

And the distinction that makes the word earn its place, already built as the DORMANT/DISCONNECTED split:

> A check that passes and a check that stopped running produce identical green dashboards. Observability is the discipline of making those two states look different.

That is the whole argument for the seed pack too, and it now has a name that a hiring manager recognises.

---

## The six

`package/kpi_definitions.json` holds the definitions and `package/kpi.py` computes them. Same rule as every other engine: it computes, it does not judge. No RAG status, no target evaluation — *a dashboard that grades itself is a dashboard nobody reads twice.*

| | KPI | CourtIQ, as of 17 Aug 2026 |
|---|---|---|
| 01 | Days to close | 12 manual → 5 agentic by design. **0 closes actually signed off**, so the observed value is undefined |
| 02 | Exception backlog | 11 open ledger entries, **198 agent escalations raised, 0 judged**, 3 UNRESOLVED layer entries |
| 03 | Usage-to-invoice accuracy | **13 of 13 periods within 2%** — after excluding $262,245 by text matching |
| 04 | Manual JEs from system gaps | **125 of 2,758 entries (4.5%)**, across seven causes |
| 05 | Revenue leakage | **$97,308 identified, $0 recovered** |
| 06 | Time to launch a pricing change | **350 days, still running** |

Each carries a rule about how it must be read, because every one of them is misleading alone:

- KPI-01 without KPI-02 is a speed claim with the queue hidden.
- KPI-05 identified without KPI-05 recovered is a claim to have *noticed*.
- KPI-03 near 100% between two systems that are both wrong is agreement, not accuracy.

---

## KPI-06 — the one that wasn't planned, and the demo

**Time to launch a pricing change** measures the whole path: decision → contracts → billing configuration → ledger → reported metric. Nobody measures it because no single team owns the whole path. Sales changes the price, Product changes the config, Billing changes the plan, Finance changes the definition, and each hands off assuming the previous one finished.

The data already contained a real one. Consumer monthly went from €9.99 to €12.99 effective **1 September 2025**, with existing accounts grandfathered until **1 March 2026**.

The trace:

| Leg | Elapsed | State |
|---|---|---|
| Decision → new-customer price live | 0 days | done |
| Decision → contracts updated | 181 days | done — the grandfather clause expired on its stated date |
| Contracts updated → **billing configuration updated** | **169 days** | **OPEN** |
| Decision → **fully launched** | **350 days** | **OPEN** |

**2,703 accounts are contracted at €12.99 and billed at €9.99.** The billing configuration was never changed. €8,109 a month, €97,308 a year, running for 169 days past the date the contracts say it should have stopped.

The definition of "launched" is what makes this useful:

> Launched means all five: every affected contract reflects the new price, billing charges it, the ledger recognises it, the recurring-revenue metric is computed on it, and the transition cohorts have either converted or been documented as permanent exceptions. **A price change that is live for new customers and not for existing ones is not launched. It is half-launched, and the half that is missing is the half that leaks.**

This change is live on two of five.

**The demo does not need scripting.** The honest walkthrough is stronger than a synthetic one: here is a real pricing change, here is the stack tracing it across five systems, here is the leg that has been open for 169 days, here is what it costs per month, and here is the lineage from the finding back to the contract clause. The books stayed auditable throughout — the leakage is visible *because* the contracted price and the billed price are both stored, which was a data-contract decision made on Day 2.

---

## What KPI-03 found on the way

The first version scored **46%** and was measuring the wrong thing: it compared periods carrying an invoice *typed* as overage against periods with metered overage. Most overage here is billed inside the subscription invoice and carries no separate type, so that was invoice **labelling**, not billing completeness.

Rewritten as value against value — metered units × contracted rate, against the overage revenue account — it scored **0 of 13 periods**, with gaps from 10% to 163%.

That turned out to be real, and not a defect. Account 4030 carries **both** metered overage *and* minimum-shortfall true-ups. Shortfall is contractual, not metered. They cannot be separated by account, because the separate account does not exist — and it does not exist despite **already being on the semantic layer's schema-change register** as SL-11.

So the engine excludes shortfall by matching text, scores 13 of 13, and says plainly what that costs:

> *This is a workaround for a schema gap already on the semantic layer's change register... Until the account exists, this KPI depends on text matching, which is not a control.*

A KPI reporting 100% and simultaneously explaining why the 100% is provisional is the correct output. $262,245 was excluded to get there.

---

## What this changes about the positioning

Doc 34's judgement holds and the build supports it. The FSE as the labs define it is an engineer who learned finance — 7+ years engineering, production systems, $500–700K. That is not the profile here and pretending otherwise would fail in the first technical screen.

The wedge is the stage where the two roles are still one person:

> **A 30-person Series A cannot hire a $500K systems engineer, but its revenue is already software.** So finance hire #1 has to be the finance systems owner — with agents and semantic rules instead of Python.

What the build now supports, with artefacts rather than assertions:

- Six operating KPIs of the finance machinery, computed from real data, each with the rule for how to read it
- A pricing change traced across five systems with a 350-day answer and a per-month cost
- An observability stack in the market's own vocabulary: assertions, alerting, and the discipline of making a stopped check look different from a passing one

And the Level 3 probe — *"name the system you built, what it replaced, and what broke when it ran unattended"* — now has an unusually strong answer, because thirteen defects were found by the agents themselves, one of them by an audit that **withdrew its own conclusion** rather than report a clean month it could not prove.

The caution from doc 34 stands and should stay in the framing: the source is a vendor naming a category it benefits from, and the six companies cited are the most usage-exposed on the planet. The role is real; the urgency at a subscription-heavy Series A is lower than the whitepaper's tone implies. Vocabulary and framing, not a claim that every startup needs this yesterday.

---

## Carried forward

- **KPI-05 recovered is $0.** Every finding is analysis until someone acts. That number moving is the single best evidence the function pays for itself, and it cannot move without a human decision.
- **KPI-02's 198 unjudged escalations** and **KPI-01's zero signed closes** both resolve with the same action: the human review session.
- The shortfall revenue account (SL-11) would turn KPI-03 from a text-matching workaround into a real control. Small change, already on the register.
