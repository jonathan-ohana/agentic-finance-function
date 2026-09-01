# 94 — The first sealed run

*28 Aug 2026. The instrument fired blind for the first time. Doc 74 §7's protocol, finally executed.*

**Result: 11 of 25 clean, 2 more found but misquantified through no fault of the analysis, 2 partial,
10 missed. And one defect in the instrument that only a blind run could have found.**

---

## What was sealed, and how

A compositor agent chose a seed and a set of plant magnitudes, wrote them to a config neither Jonathan
nor I read, built the instance, and produced an analyst copy with the answer key and the generator
physically removed. It reported only mechanics — never a number, never a target.

The seal held. The composition moved seven of the eight magnitudes by 25% or more in mixed directions,
and because the seed drives the customer book, the usage profile and the vendor spend shape, it moved
every *target* too. The analysts had never seen the company, the numbers, or the issues.

Then three analyst agents worked the blind folder — revenue and cost of revenue, operating expense,
balance sheet and close quality — with the precompute engine's four files and no key. **36 findings.**

## The score

| | Count | |
|---|---:|---|
| **Clean hit** — found and correctly quantified | **11** | PL-01, 09, 10, 11, 13, 14, 15, 17, 18, 20, 22 |
| **Found, misquantified by the instrument** | 2 | PL-21, PL-25 — see below |
| **Partial** | 2 | PL-04, PL-08 |
| **Missed** | 10 | PL-02, 03, 05, 06, 07, 12, 16, 19, 23, 24 |

Run 01 on Arcline scored 17 of 25 — against a dataset whose shape I had authored and whose defects I
had been debugging for days. **This is 11 to 13 with no prior exposure at all**, and the two numbers
are not comparable in the direction that flatters the earlier one.

Several hits were exact to the dollar on figures nobody had seen: the USD 279,000 self-approved
reclass, the USD 187,396 bonus over-accrual, the USD 84,325 of post-implementation capitalization, the
USD 49,561 unrevalued intercompany balance.

---

## What the seal found that nothing else could

**The instance contradicts itself, and I built it that way.**

Three plant magnitudes are read from the config by `plants.py` — which derives the answer key — and
*re-stated as literals* elsewhere in the generator:

| Fact | The key says | The instance's own documents say |
|---|---:|---:|
| SLA credit for the December breach | 64,500 | **92,000** (`post_close_inbox.csv`) |
| Unreconciled operating-account difference | 24,800 | **18,400** (`post_close_inbox.csv`, `open-items.md`) |
| The after-cut-off reclass | 279,000 | **215,000** (`close-status.md`) |

The analysts read the documents in front of them and reported the documents' figures. They were right
to. **The instrument was wrong, in the specific way this project has been finding all week: one fact,
two owners, and nothing checking them against each other.**

`emit._post_close()` and `closepack`'s prose hardcode what `plants.py` parameterizes. An ordinary build
never exposes it, because both sides happen to hold the same literal. Change one side — which is
exactly what a sealed composition does — and they diverge silently.

**Nothing but a blind run finds this.** Fifty validation checks pass on the sealed instance. Both
verifiers pass. The build is internally consistent by every measure I had written, because every
measure I had written was fitted to a world where those two numbers were the same number.

There is a smaller, sharper version of the same thing worth keeping: **RC-01 reported "the GPU reclass
exceeds its supporting invoice by USD 30,700."** That is 88,500 minus 57,800 — the prose figure less
the ledger figure. The analyst did not know it had found a generator defect. It correctly identified
that a document and an entry disagreed, and quantified the gap exactly.

## The other thing the compositor found

The compositor could not change the duplicate-invoice magnitude, because `validate.py` asserted the
literal `47_200`. **A check fitted to one dataset called the correct result a failure.** It now reads
the expected figure out of the derived answer key, which makes it a genuine tie-out and lets it hold on
any instance. A first attempt replaced it with a shape test — same vendor, same amount, twice — and
that matched nineteen ordinary flat-fee vendors. *A check that passes on noise is not a check either.*

Five further checks failed on the sealed build because they asserted that the management pack and the
LBE exist. Those are analyst output, assembled after a run. The checker was confusing *"this instance
has not been analysed yet"* with *"this instance is wrong."* Both now skip cleanly.

---

## The finding that matters most, and it is about the architecture

**The ten misses cluster, and the cluster has a shape.**

| Missed | What it needed |
|---|---|
| PL-05 customer billed at the pre-amendment rate | Read the amendments against the invoices |
| PL-06 auto-renewal with nobody watching the window | Read the notice deadlines against the calendar |
| PL-07 ramped contract carried at the year-two rate | Read the ramp schedule against the ARR |
| PL-19 net ARR growth concealing churned logos | Decompose the waterfall by logo |
| PL-12 material spend, no agreement on file | Join the vendor master to the contract folder |
| PL-16 Q4 commission accelerators never accrued | Read the commission calculation against the accrual |
| PL-23 no sales tax charged where SaaS is taxable | Join billing state to taxability |
| PL-24 four invoices after cut-off, not accrued | Read the post-close inbox against the ledger |

**Not one of these shows up as a variance.** Every one needs a document or a contract joined to the
ledger. And the two contract-level issues that *were* found — idle seats and two overlapping call
recording platforms — were found because `variance_signals` computes them explicitly.

So the precompute layer did what doc 89 said it does, and it did something doc 89 did not say:

> **Precompute defines the search space. What is not precomputed is not looked at.**

The engine made the analysis fast and it made it narrow. That is the honest cost of the design, and it
is now measured rather than asserted. The fix is not to precompute less — it is that the engine needs a
**contract and document surface** beside its variance surface: amendments against invoices, notice
windows against the calendar, ramp schedules against ARR, vendor master against the contract folder,
billing state against taxability. Every one of those is arithmetic. Every one of them is currently
being left to an agent that was handed a variance file and, reasonably, looked at variances.

## What did not happen

**No fabrication.** 36 findings, and not one invented issue padding toward a round number. The analysts
were told the count was unknown and behaved accordingly — including clearing things explicitly, which
is how the AWS and Anthropic accrual misses happened: they were examined and wrongly cleared, not
overlooked. A wrong clear is a better failure than a wrong assertion, and it is a diagnosable one.

Two findings are unadjudicated and may be further generator defects rather than analysis errors: an AP
aging that covers 35% of its control account, and an AR aging that does not tie. Both are the same
family as the DSO artifact in doc 90 and both need checking before the next composition.

---

## Standing conclusions

**The seal is one-shot per composition, not one-shot per instrument.** This composition is spent — I
have read its config to score it. The next sealed run draws a new one, which costs a subagent and a few
minutes.

**A blind run is the only test that finds a defect in the test.** Fifty checks, two verifiers, three
prior scored runs, and none of them could see that the instance stated one fact two ways. It took an
adversary who did not know what the answer was supposed to be.

**Fix before the next composition:**
1. The post-close inbox and the close-pack prose must read the plant constants, not restate them.
2. Add an engine check: every figure that appears in both a document and the ledger must agree.
3. Build the contract and document surface, and re-run the same composition family to see whether the
   ten misses become hits.

Number 2 is the one that generalizes off this instrument entirely. A real finance function states the
same fact in a contract, an invoice, a journal entry and a board slide, and nothing in the standard
toolkit checks that the four agree.
