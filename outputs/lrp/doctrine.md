# 83 — The 5-year LRP: doctrine and build brief

*Ruled 22 Aug 2026 (Fable, granularity corrected by Jonathan). Top rung of the benchmark ladder (doc 82): LRP (annual vintage) → budget → quarterly locks → LBE. The Y1 envelope anchors the bottom-up annual plan.*

## Granularity (Jonathan's ruling — uniform, declared on the face)

- **Y1: quarterly, at BUSINESS-OWNER level** (an owner may span multiple cost centres).
- **Y2–Y5: annual, at business-owner level.**
- Account-level detail appears NOWHERE in the LRP — the bottom-up budget supplies precision and ROLLS UP to the LRP for reconciliation. The LRP is never more precise than its knowledge.
- **New semantic-layer artifact: the owner → cost-centre mapping**, declared once, shared by LRP, LBE (doc 82 layout), and the Co-pilot dimensional model.

## Principles

1. **Drivers, not line extrapolation.** Per segment: adds, churn, ARPA, pricing actions. Costs: headcount envelopes by function × per-head; COGS as rate × volume with an explicit learning-curve assumption (inference cost per match declines — one observed 45% step exists); opex as ratios CONVERGING to declared at-scale targets (S&M/R&D/G&A % of revenue). The convergence targets are the strategic statement — "what this company becomes" — sourced from stage benchmarks and owned by the human.
2. **Three-statement integrity at pack standard.** BS on drivers (DSO, deferred-rev months, capex per court, depreciation schedules); CF derived; articulation checks as formulas; **cash never plugged** — financing rounds are discrete modeled events with required size and timing stated when cash breaches the floor.
3. **Waypoints are the deliverable; the grid is the engine.** One page: the path through fundable states — GM crossing points, per-segment contribution-margin turns, the Series B metrics gate (ARR/NRR/burn multiple by when), default-alive date. Mechanical rule: if year N's end-state cannot raise the round year N+1 spends, the model flags the plan as unfunded — fundability gates discipline the growth assumptions.
4. **Scenarios are strategic worlds, written in prose first** (Assumptions-tab discipline; no scenario scales another's output). Low/Mid/High as narratives, plus one reverse pass: work backwards from the Y5 Series-C-ready state — "what must be true each year."
5. **Uncertainty on the face.** Y2+ carries no accuracy evidence and says so; the three dominant assumptions for Y5 cash are named with sensitivities (expect: churn, adds ramp, inference cost curve). No fifty-bar tornado.

## The anchor mechanic

LRP Y1 issues the **envelope**: revenue floor, opex ceiling by business owner (quarterly), headcount cap, ending-cash floor. The annual plan builds bottom-up from cost-centre owners (monthly, account level) and ROLLS UP to the envelope. Mandatory artifact: the **reconciliation bridge** (budget vs LRP-Y1 at owner/quarter level). Two legal outcomes: budget conforms, or the LRP is formally restated with rationale (change control, versioned, disclosed). Silent divergence is illegal — it is what turns LRPs into shelf-ware.

## Governance

Permanently L0 (doc 19: lowest frequency, highest stakes, small N forever). Forecaster runs mechanics; the human owns convergence targets, waypoints, scenario narratives, and the CEO negotiation. Rebuilt annually at budget season, versioned with the plan-hash discipline; never touched intra-year — an anchor that moves when the year gets hard is not an anchor.

## Build sequence (CourtIQ instance; one Opus session per step)

1. Scenario narratives (Jonathan drafts, Opus pressure-tests).
2. Driver tree extended to 20 quarters/5 years with the declared granularity + owner→CC mapping.
3. Convergence targets from stage benchmarks (human ratifies).
4. Three statements + checks.
5. Capital plan (rounds as events, dilution math).
6. Waypoint page with fundability gates.
7. Y1 envelope extraction → handed to the budget process (the doc-82 ladder closes).
