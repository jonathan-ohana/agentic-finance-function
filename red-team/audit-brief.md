# Fable brief — audit the reporting and forecasting package

**Attach:** `mgmt_reporting_pack_2026-07.xlsx` · **Optional:** docs 44 (SaaS layer) and 47 (forecast model), only if Fable asks for the rulings behind a refusal.

---

You are auditing a management reporting and forecasting package built for a Series A B2B/B2C SaaS company. Twenty tabs, 6,020 formulas. **The workbook is attached — open it and cite cells.** Do not ask me for extracts; do not reconstruct what you can read.

## Your standing

You are **not a reviewer giving feedback.** Choose the harder of these two seats and say which you took:

- the **incoming Head of Finance** who inherits this pack and must present it to the board in nine days, or
- the **Series B partner** who has ninety minutes with it before an IC meeting.

Both have the same problem: **finite attention and a decision to reach.** Judge every tab against that, not against completeness.

## The brief in one line

The person who built this says: *"The design and visuals are not crisp. The data feels messy. If I were the CEO, I would feel overwhelmed."* **Assume that verdict is correct and find out why.** Your job is not to confirm it.

## The four questions

1. **Does the key message land?** What is the *one* thing this month says, is it findable in under sixty seconds, and does the pack lead with it or bury it?
2. **What does a Series A SaaS CEO actually need to know — and does this answer it?** Name what is missing that matters, and name what is present that does not.
3. **How does this pack help a CEO steer?** It currently reports and refuses. Where should it move from *reporting* to *insight to decision* — and where must it not, because the inference would exceed the evidence?
4. **Is it auditable without being exhausting?** The audit trail is the pack's differentiator. Right now it may also be its burden.

## Diagnose before you prescribe

**I do not know what is wrong, and neither should you until you have looked.** "Overwhelming" is a symptom with at least five different diseases, and the fix for each is incompatible with the fix for the others. **Name the disease first, with evidence, then prescribe.**

The candidates — falsify the ones that do not fit:

- **Volume.** There is genuinely too much here. Fix: delete or merge.
- **Sequence.** The right amount, in the wrong order. Twenty tabs where three are the front and seventeen are an appendix is not a smaller pack, it is a *sequenced* one — and it may be the whole answer. Fix: re-order and re-label, delete nothing.
- **Hierarchy.** Everything is the same size, so nothing is emphasised. Fix: typography, weight, whitespace, ruthless de-emphasis of the secondary.
- **Voice.** The pack reports where it should conclude. Every line is true and none of them says *therefore*. Fix: rewrite the sentences, not the structure.
- **Content.** The wrong things are measured, so no amount of presentation saves it. Fix: change what is computed.

**Say which it is, and how confident you are.** If it is more than one, rank them by how much of the symptom each explains. If you think it is mostly presentation, say so plainly — the person who built this suspects the same and has not been able to prove it.

**Then, and only then:** an addition must be paid for. If you propose new content, name what it displaces from the reader's attention — not necessarily from the file. Demoting to an appendix counts as payment; making the CEO read one more thing does not.

Deliver an explicit attention budget either way: what the CEO reads in 2 minutes, in 15, and what exists only for audit. **That budget is itself diagnostic** — if every tab has a legitimate home in it, the problem was never volume.

**Be specific or say nothing.** Every criticism names a tab and a cell or quotes a sentence. *"Improve the visual hierarchy"* is worthless; *"Exec Summary rows 21–34 give fourteen KPIs equal weight, so the one BEHIND line is invisible — cut to five and move the rest"* is the standard.

**Rewrite, don't describe.** For the three highest-impact fixes, produce the actual replacement: the literal sentences, the row order, the number formats, the chart type and what it plots. I will implement what you write verbatim.

**Separate the two "messy" complaints.** Distinguish *the data is presented badly* from *the underlying dataset is unconvincing*. Different fixes, and I need to know which you mean each time.

**Rank by impact on a decision.** Order every recommendation by how much it changes what the CEO does on Monday. Anything that changes nothing goes at the bottom, labelled cosmetic.

## What this pack does deliberately, so you critique the choice and not the accident

These are rulings, not oversights. Attack them if they are wrong — but attack them as choices.

- **Metrics that cannot be measured are refused, not estimated.** `LTV : CAC` and `Net revenue retention` read `n/a` with a stated blocker. NRR is unavailable because the subscription book holds current state with no dated change log, so expansion and contraction are unobservable.
- **Colour is a claim about provenance.** Blue = a human input. Amber = an extract from a system of record. Black = computed on this sheet. Green = a link to another tab. 127 blue cells, nearly all on Assumptions.
- **Every check is a formula reading zero**, and the Exec Summary carries all fourteen live.
- **The forecast has one scenario toggle**, not three parallel projections, so a scenario cannot disagree with itself.
- **The cash line runs below zero and is not plugged**; the capital requirement is stated separately.
- **The valuation is EV/ARR and deliberately not a DCF**, with placeholder multiples flagged as such.

## The numbers, so you spend no tokens finding them

July 2026 actual · close **PREPARED AND UNSIGNED** · no management forecast since April 2026.

| | |
|---|---|
| Total revenue | $457,459 (−18.6% MoM; June carried $111,850 of one-off event revenue) |
| Gross margin | 69.5% |
| Operating loss | $452,315 |
| Cash | $7,874,975 · runway 16.1 months on trailing burn |
| Committed recurring ARR (MET-009) | $4,743,222 |
| **Net new ARR** | **−$45,241** — churn exceeded new business in June and July |
| Gross revenue retention, 12m cohort | 88.8% blended · 100% B2B · **73.5% consumer** |
| Logo churn | 2.40%/month |
| Rule of 40 | 76.7% |
| Forecast, Mid case | cash negative **Apr-28**, 20 months, peak shortfall $1.15M, **indicative raise $3.28M** |
| **Burn multiple, month 24** | **27.6×** |

Two facts about the data you should know before judging it. It is **synthetic**, built to carry deliberate defects. And one of those defects is live and disclosed: **the consumer book records zero new logos in June and July** against ~390 monthly churn, which is a data-feed artefact, not a business event. Do not spend tokens rediscovering it — tell me whether disclosing it on the face of the pack is right, or whether it should be fixed in the data before a CEO ever sees it.

## Tab inventory

| Tab | Rows | Formulas | Holds |
|---|---|---|---|
| Cover | 63 | 0 | Close parameters, colour legend, contents, checks, caveats |
| **Exec Summary** | 87 | 204 | Headline 6, scorecard of 14 KPIs with FLOW/BALANCE signal, 5 findings, 5 CEO decisions, 14 live checks, 2 charts |
| KPI | 40 | 263 | 14 KPIs × 13 months vs quarterly goal |
| P&L | 34 | 432 | 13 months, both plans |
| P&L Quarterly | 64 | 181 | QoQ and YoY, complete quarters only |
| Revenue | 60 | 329 | Segments, volume/price/mix decomposition |
| **SaaS Metrics** | 111 | 713 | ARR family, waterfall, retention, unit economics, efficiency |
| COGS / Opex | 16 / 37 | 503 | By ledger account |
| Balance Sheet / Cash Flow | 33 / 46 | 568 | Linked; nothing typed |
| **Assumptions** | 88 | 45 | Low/Mid/High driver set, every input with a written basis |
| **Forecast** | 164 | 1,904 | 24-month model, scenario toggle, capital requirement |
| **Valuation** | 76 | 174 | EV/ARR, two sensitivity grids |
| Bridges / Lineage | 34 / 37 | 39 | Plan-to-actual waterfalls; connector status and line lineage |
| Data_TB / Ops / Book / Plan | 180 | 665 | The extract layer — the only hardcoded actuals |

## Deliver

1. **The diagnosis**, ≤150 words. Which disease, how confident, and the evidence that rules the others out.
2. **The verdict**, ≤80 words. Would you present this pack as it stands? If not, the single reason.
3. **The attention budget** — 2 minutes / 15 minutes / audit-only. Every tab assigned. Say whether the exercise found a volume problem or disproved one.
4. **The five things that change what the CEO does**, ranked, each with the cell it lives in and the rewrite.
5. **Design**: the three rules this pack breaks, each with the specific instance and the fix. Hierarchy, density, colour, chart choice. If the diagnosis was presentation, this is the longest section.
6. **Data**: presentation faults and dataset faults, separately. What would make it convincing.
7. **The strategic gap** — what a Series A SaaS CEO needs that is absent, and what it displaces.
8. **The line you would not cross** — where recommendation would exceed evidence, and how the pack should say so.

Skip anything you would only say to be encouraging. If a section has nothing worth saying, write "nothing" and move on.
