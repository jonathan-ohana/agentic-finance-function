# The pipeline surface — tier 3, first implementation

*Built 4 Sep 2026 on the Arcline instance. `_generator/pipeline.py`; outputs in
`06-forecast/FY2026/`. The artifacts are not published in this repository; this is
the record of the run.*

`forecast-method.md` has specified this engine since it was written: revenue in
three stacks — contracted, renewal-adjusted, and weighted pipeline — never summed
into a single unlabelled figure. Tiers 1 and 2 read the contract book. Nothing read
the pipeline until this run.

## The run

120 open deals, 0 refused, 4/4 checks. Three bands, each with its claim stated on
the artifact: commit 10,010,000 (ACV at stage 5–6 — what sales says will close),
weighted 13,170,850 (probability-weighted — see the findings before believing it),
best case 27,207,000 (every open deal at full ACV — a ceiling, not a forecast).

Against the plan's new-business assumption (850,000/month net new ARR, from
`plan_fy26_assumptions.md`): February–March weighted closes are 2,004,850 against
1,700,000 planned — ahead of plan on gross new ACV, with the stated caveat that the
plan figure is net and churn sits in tier 2.

The engine emits one proposed LBE row — account 4000, 2026-03, −2,788, half
`materializes`, at ratified=N — because a forecast term enters the LBE through
the Analyst's ratification or not at all. Only a February close touches Q1 revenue,
one month at ACV/12, which is why the number is small while the ARR gap is not.
It was ratified in the instance on 4 Sep by the owner, after this run.

## What the first run refused or named

**F1.** Every probability in the export is its stage default. No deal carries
rep-entered judgement, so the weighted band is a stage-mix statistic, not deal
intelligence, and moves only when deals change stage.

**F2.** Staleness is not observable — the export has no last-modified date. A
probability untouched for ninety days and one reviewed yesterday are
indistinguishable. Schema request: `last_activity_date`.

**F3.** The method requires probabilities adjusted for historical stage-to-close
conversion. NOT COMPUTABLE — the export holds open deals only and no closed-deal
history exists. CRM probabilities used, and every weighted figure carries that
basis on its face.

**F4.** Weighted pipeline was not a registered metric when the engine first ran.
It proposed MET-016 and a revenue-conversion DEF (revenue begins the month after
close at ACV/12; services and commissions are separate lines); the owner registered
both as MET-016/MET-017 on ratification. The engine itself registers nothing.

**F5.** The plan comparison reads prose constants. Schema request: the ARR walk as
a plan export, so the constants block can die.

**Back-test: REFUSED.** Scoring the weighted band needs a later snapshot and a
closed-won register; the instance holds one snapshot and no history. The refusal
retires when the second monthly snapshot exists.

The pattern worth keeping: the first run of a forecast engine produced three
numbers and five refusals, and the refusals are the more valuable half — each one
is a claim the surface declines to make until the data can support it. A copilot
pointed at the same file would have summed it and called it a forecast.
