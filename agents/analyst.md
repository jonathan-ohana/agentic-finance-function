# 33 — The Analyst, the variance engine, and the plan that was not a plan

**Date** 18 August 2026, morning · **Sprint** plan-day 7 (first half), on calendar day 2 · **Status** built and run twice

Second agent of the spine. Same architecture as the Bookkeeper: `package/variance.py` computes, `package/charters/analyst.md` attributes.

The separation of powers is now explicit in all four charters. **The Bookkeeper says what happened. The Analyst says why. The Advisor says what to do about it. The Chief of Staff says when it is due.** The Analyst is the only one permitted to assign a cause, and its charter is eight rules about why that permission is dangerous.

---

## The rule that took the most thinking

Rule 3, the residual.

Every bridge the engine produces carries an `unexplained_residual` computed as total variance less attributed components. It ties by construction and is never chosen. The charter forbids distributing it, folding it into the largest driver, or sizing a soft driver to absorb it:

> *A residual distributed to complete the bridge is the analytic form of the Bookkeeper's plug — same motive, same concealment, and harder to detect, because afterwards nothing is out of balance.*

That sentence is the whole design. The Bookkeeper's plug shows up as a reconciliation that ties when it should not. The Analyst's plug shows up as nothing at all, because a bridge with a distributed residual looks *better* than an honest one.

The demotion trigger matches the Bookkeeper's: a distributed residual found anywhere returns the agent to L0 and requires every bridge since the last clean close to be re-run.

## The autonomy split

L0 permanently for any sentence that assigns a cause. The reasoning is the sharpest argument in the charter for why a causal claim is different in kind from a numerical one:

> *A wrong number is caught by the next reconciliation; a wrong cause is caught by nothing downstream of the human who reads it, is repeated to a board, and shapes decisions until someone disproves it. Attribution also seals itself: once a cause is accepted, the following periods are read in its light, and the evidence that would overturn it stops being looked for.*

One class may ever be promoted — the metric pack, where values come from registry definitions a human already approved and no causal sentence appears.

---

## Defect 11 — the plan was the actuals times a constant

The Analyst ran, and instead of analysing the variances it tested the comparators first. Rule 4 requires knowing a comparator's vintage; the agent decided vintage was not sufficient and checked what the plan files were made of.

> *Both plans' cost lines are the ledger's actuals multiplied by a constant.*

Against the board plan the ratio was 0.95694 on COGS, R&D, S&M and G&A, in every month. Against the reforecast, 0.98814 on all four from April onward.

The verdict:

> *A variance that is the same proportion of research compute, paid media and legal fees is not a statement about spending. It is the plan's construction re-expressed.*
>
> *No driver may be attributed to any cost-line variance under either comparator, in this period or in the persistence series, because the variance is determined by the comparator's construction before any cost is incurred.*

It was right, and it is my defect. `make_plan()` took one growth factor and one cost factor and applied the cost factor to all four expense lines. Every "variance analysis" the dataset could support was arithmetic about a scalar.

**Fixed.** Plans are now built line by line, each line carrying its own base assumption, its own monthly drift and its own month-to-month error. The board plan is optimistic on revenue and assumes a compute efficiency that never arrived; the reforecast corrects revenue but leaves the sales ramp uncorrected. July now shows S&M $29,880 *under* plan while COGS runs $4,095 *over* it — different lines moving in different directions, which is the minimum condition for a variance to carry information.

New check: *plan lines are assumptions, not the actuals times a constant.* **83/83 checks pass.**

The agent also caught, in the same pass, that the reforecast restates January to March cost actuals to the cent — so two of any six-month persistence series are zero by construction, and a run counted through them is four months, not six. It reported four of the engine's twelve persistence flags as failing rule 7's test on exactly that ground.

## Defect 12 — my engine borrowed one plan's FX assumption for the other

On the re-run, with plans fixed, the Analyst found a defect in `variance.py` itself:

> *The engine applies a plan rate of 1.0520 to the FX component of both revenue bridges. That rate is the FY26 board plan's. The Apr-26 Reforecast states no FX assumption anywhere in its file... the component as published rests on an assumption imported from the other plan.*

Correct. The rate was a single engine-level parameter. A rate assumption belongs to one plan version, and attributing an FX driver on a bridge whose plan never stated a rate manufactures a driver out of the analyst's own choice.

**Fixed.** Rates are now per version, and a version that states none gets no FX component — the engine emits `FX UNAVAILABLE as a driver` and the effect stays in the residual where it belongs. The reforecast revenue bridge went from an attributed +$27,154 with a −$35,720 residual to an honest −$8,566 residual and nothing attributed.

**The shipped pack is the run that found it, and it has not been reissued.** Its section 2.3 identifies the defect in the numbers printed above it. That is what a finance function actually does with an error found after a pack is out: correct forward, say so, and do not quietly restate. Reissuing would have destroyed the evidence that the control worked.

---

## What the July analysis actually concluded

**Almost nothing, and correctly.**

The comparator question is **BLOCKED**. Two plan versions are live, the semantic layer has ruled neither primary, and the choice changes the *sign* of the COGS variance and moves revenue and gross profit across the flux threshold. Rule 4 forbids choosing. The agent filed a drafted ruling and showed both comparators on every line.

CL-33, the metric refresh, is **NOT RUN** — the engine reports registry definitions but computes no values, and the agent declined to compute them itself rather than breaching rule 1.

CL-13 and CL-15 are **BLOCKED** on prerequisites the Bookkeeper could not complete. CL-16 delivered the ageing and blocked the provision, because no provision matrix is in force.

The caveat block is the first section and states that twelve of sixteen blocking steps have no evidence, that thirteen escalations are open, and which of them touch each line analysed — by ID.

This is the second consecutive agent to produce an artefact whose main content is what it refuses to assert. That is either the most valuable property of this architecture or the least marketable one, and it is probably both.

---

## Carried forward

- **The primary comparator ruling** is now blocking two agents. It is the highest-value open item in the semantic layer.
- The reforecast plans headcount equal to actual headcount in every forward month, so no personnel driver is observable against it. Realistic for a reforecast, but worth stating in the plan file rather than leaving to be discovered.
- CL-33 needs the engine to compute metric values, not just report definitions. That is the next engine increment and it is small.
- Next: the Forecaster, then the Reporter — at which point the spine runs end to end and the Day 8 checkpoint has something to judge.
