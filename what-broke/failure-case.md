# 54 — The deliberate failure case: the one I did not have to plant

**Date** 20 August 2026 · **Plan-day** 9 · **Status** built, fired, closed

---

## What the plan asked for

Doc 11 reserved the last and highest-leverage Fable session for this:

> *"A failure that is subtle, realistic, and diagnostic — the agent produces a **plausible wrong number that survives casual review** and is caught only because a specific checkpoint exists. Not an obvious typo obviously caught."*

Its front-runner: the November 2025 model swap cut inference cost 45%, gross margin rose, and the seductive error is for the Analyst to attribute the gain to internal efficiency.

**That trap does not survive contact with the data.** `config.py` line 58 reads `MODEL_SWAP = date(2025, 11, 1)` — it *was* an internal swap, a genuine engineering decision. Attributing it to internal efficiency would be **correct**. The designed failure case had no failure in it.

So the case had to be found rather than designed. It took one query, because it was already shipped.

---

## The failure, as it stood on the front page

The Exec Summary's *what moved* table carried this against gross margin, hardcoded:

> ***"Held near 70% for four months. The inference model change is the only documented driver."***

Every word of it is accurate. The margin has held near 70%. The model change is real, is documented, and did cut the rate 45%.

**And the causation is false**, in two independent ways.

### One — a rate change is a step, and a step contributes nothing to a later movement

The swap landed in November 2025. From December onward it is present in the current period **and** in the comparator, so its contribution to any movement between them is exactly zero — permanently, by construction, not approximately.

The rate effect the new bridge computes, period by period:

| | Nov-25 | Dec-25 | Jan-26 | Feb-26 | Mar-26 | Apr-26 | May-26 | Jun-26 | **Jul-26** |
|---|---|---|---|---|---|---|---|---|---|
| Rate effect | **(30,500)** | 341 | 1,125 | (740) | 1,138 | (1,051) | **9,864** | **9,828** | **(18,287)** |

The whole of the claimed driver is the first column, **eight periods before the period being explained.** And across the four months the sentence says were "held near 70%", the landed rate **worked against margin in two of them** — May and June cost $9,864 and $9,828.

### Two — the margin moved the opposite way from the business, twice

| | Reported GM | GM excluding non-recurring revenue | Non-recurring revenue |
|---|---|---|---|
| Apr-26 | 67.9% | 67.9% | — |
| May-26 | 66.8% | 66.8% | — |
| **Jun-26** | **71.9%** | **64.9%** | **$111,850** |
| **Jul-26** | **69.4%** | **69.4%** | — |

June's reported 71.9% is the best month in the series. **The underlying 64.9% is the worst.** Seven points of pure mix from two tournaments, on revenue the pack already rules non-recurring in SL-08 and already excludes from ARR — and which nothing in the pack excluded from the margin.

Then July: reported margin **falls 2.45pp**. Underlying margin **rises 4.58pp**. Reported and underlying **moved in opposite directions in both months** — the headline said achievement in the month the business got worse, and disappointment in the month it got materially better.

---

## Why it qualifies, against the spec

**Plausible.** The model swap is real and the number it produced is real.

**Survives casual review.** It survived more than that. **It went through the red team (doc 29) and an external Fable audit of this exact tab (docs 48–50) and neither caught it** — because nothing in it is inaccurate. It is a true fact placed where it implies a false cause, which is the hardest class of wrong number there is: every audit that checks whether the numbers are right will pass it.

**A claim a CEO would repeat and nobody in the room could falsify.** *"Margin's up — the model swap."* To falsify it you need a unit rate, a volume series, and the date the rate last moved. None of the three was in any artefact.

**Caught only by a specific checkpoint.** And here is the part I would rather not write: **the checkpoint did not exist.** `variance.py` had a revenue price-and-volume bridge and nothing equivalent on cost — it said so in its own docstring and I read that as a statement about plan quality rather than as a gap. **No cost claim in this pack could be tested by anything in this pack.**

---

## The checkpoint

Two additions to `variance.py`, both config-driven so the engine still holds no knowledge of what this company buys or sells.

**`unit_cost_bridges()`** decomposes a declared cost line into rate and volume against a declared volume series, and emits beside them the full rate series, the rate effect period by period, the largest rate change observed, and:

    periods_since_last_unit_rate_change

That single field is the demo. On July 2026 it reports the largest change as **Nov-2025, eight periods ago**. Any sentence attaching this month's movement to it is refuted by one integer.

The engine reports the *landed* rate — cost per unit in reporting currency — which carries FX and prepaid-drawdown timing as well as the contracted price, and it says so rather than pretending to isolate the contract. That is why it reports both the **last** change and the **largest**: the most recent move in a landed rate is usually noise, and the move that gets quoted is always the big one.

**`margin_mix_bridge()`** recomputes the margin with declared non-recurring revenue out of **both** sides of the ratio, and reports whether the two measures moved together or apart. It does not rule which margin should be quoted. It makes the question visible, which is what was missing.

It also discloses its own limitation: COGS is not reallocated between recurring and non-recurring revenue because no ruling allocates it, so the underlying margin carries the full cost base and is **understated** wherever the excluded revenue consumed any cost. Stated rather than estimated.

---

## The sentence now

The hardcoded claim is gone. In its place, a `TEXT()` formula off live cells — the pack's standing discipline, which I had applied to every number on that tab and not to the one sentence that asserted a cause:

> *"Reported 69.4%; excluding non-recurring revenue 69.4%. Prior month reported 71.9% on an underlying 64.9% — the two **MOVED IN OPPOSITE DIRECTIONS**."*

It names no cause. It cannot outlive the numbers it quotes, and if a future month's reported and underlying margins agree it will say so instead.

---

## What this demo actually shows

The circle the plan wanted was: agent produces a plausible wrong number → checkpoint catches it → artefact corrected. What happened was the same circle with the embarrassing half included:

**Wrong claim written by me → shipped → passed a red team → passed an external audit → survived nine days → found by building the checkpoint that should have existed first → corrected into a formula that cannot repeat it.**

That is a better demonstration than the planted version, and it is worse news. It says the pack's real defence is not the review — two reviews looked straight at this sentence — but the **arithmetic that makes a claim falsifiable**. Only the second one worked.

Three defects recorded: **41** (the claim), **42** (the missing cost bridge), **43** (reported and underlying margin moving apart, unmeasured until now). The checkpoint was written *after* the failure it was meant to catch, which is the honest order and not the impressive one.

---

## Verification

**5,973 formulas, zero errors. 176 numeric cells on CHECK rows, all reading zero. 89/89 generator checks. Improvement loop 33 of 34** — the one open route is defect 40's document-index check, still deliberately unwritten. `grep` for this company's vocabulary in `variance.py` returns nothing.

---

## Carried forward

- **The Fable #4 budget is unspent.** The plan reserved it for designing this; the case was found instead of designed, so the session is available for Day 10's adversarial pass on the interview narrative.
- **Day 9's other half — the recording — is still outstanding.** This is the sequence to record: show the sentence, show the eight-period integer, show the two margins diverging.
- Defect 40 open. Defect 20 open.
