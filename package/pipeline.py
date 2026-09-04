"""
Tier 3 of the rolling forecast: the weighted pipeline surface.

forecast-method.md has promised this engine since it was written: revenue is built from
three stacks - contracted, renewal-adjusted, and "weighted pipeline from
pipeline_2026-01.csv" - and the three are never summed into a single unlabelled figure.
Tiers 1 and 2 read the contract book. Nothing read the pipeline. This does.

What it emits, into 06-forecast/FY2026/:

  pipeline_surface_<p>.csv    every open deal: band, close month, revenue phasing, flags
  pipeline_by_month_<p>.csv   close month x {commit, weighted, best_case}, deal counts,
                              and the subscription-revenue phasing of each band
  pipeline_vs_plan_<p>.csv    the quarter's open months against the plan's new-business
                              assumption, and the proposed LBE materializes row -
                              emitted with ratified=N, because a forecast term enters
                              the LBE through the Analyst's ratification or not at all
  pipeline_notes_<p>.md       bands, findings, refusals, and the proposed rulings

The three bands, and what each may claim:
  commit    ACV of deals at stage 5-Negotiation or later. What sales says will close.
  weighted  sum of probability x ACV over all open deals. See finding F1 before
            believing it.
  best_case ACV of every open deal. A ceiling, not a forecast.

The bands are never summed with tier 1 or tier 2, and no total in these files mixes
bands. A certainty tiering that gets re-aggregated has communicated nothing.

Doctrine carried over from the LBE build: nothing here posts anywhere, nothing here is
ratified by being computed, and a question the data cannot answer is emitted as a named
refusal rather than a plausible number.

    python3 pipeline.py [instance folder] [period]      period defaults to 2026-01
"""
import os, csv, sys, datetime as dt
from collections import defaultdict


def quarter_open_months(period):
    """The remaining months of this period's calendar quarter, after the period itself."""
    y, m = int(period[:4]), int(period[5:7])
    q_end = ((m - 1) // 3 + 1) * 3
    return [f"{y}-{mm:02d}" for mm in range(m + 1, q_end + 1)]


PERIOD = sys.argv[2] if len(sys.argv) > 2 else "2026-01"
Q_OPEN = quarter_open_months(PERIOD)     # open months of the quarter at this snapshot

# The plan's new-business assumption. Machine-readable source does not exist: these
# figures are prose in plan_fy26_assumptions.md ("Net new ARR USD 10.20m, phased at
# roughly USD 850k per month"; "average new-logo ACV USD 168,000"). Constants block
# per doc 75; finding F5 requests the ARR walk as a plan export so this block can die.
PLAN_NET_NEW_ARR_MONTHLY = 850_000.0
PLAN_SOURCE = "plan_fy26_assumptions.md (FY26 Plan v3, locked 2025-12-11)"

COMMIT_STAGES = {"5 - Negotiation", "6 - Verbal"}

def read(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def month_of(datestr):
    return datestr[:7]

def add_month(period):
    y, m = int(period[:4]), int(period[5:7])
    m += 1
    if m == 13: y, m = y + 1, 1
    return f"{y}-{m:02d}"

def build(folder):
    P = lambda *a: os.path.join(folder, *a)
    src = P("06-forecast", "FY2026", f"pipeline_{PERIOD}.csv")
    deals = read(src)
    checks, findings, refused = [], [], []

    # ---- integrity of the export itself
    bad_weight = [d for d in deals
                  if abs(float(d["probability"]) * float(d["acv_usd"]) - float(d["weighted_acv_usd"])) > 0.5]
    checks.append(("weighted_acv_usd equals probability x acv_usd on every row", not bad_weight,
                   f"{len(bad_weight)} rows disagree" if bad_weight else f"{len(deals)} rows"))
    closed_stages = [d for d in deals if d["stage"].startswith(("Closed", "7"))]
    checks.append(("export contains open deals only", not closed_stages,
                   f"{len(closed_stages)} closed rows present" if closed_stages else ""))

    # rows the surface refuses rather than repairs
    kept = []
    for d in deals:
        why = None
        if not d["expected_close_date"]:
            why = "no expected close date - a deal with no date is not in any month's forecast"
        elif month_of(d["expected_close_date"]) <= PERIOD:
            why = ("expected close in or before the closed month - a deal that should have closed "
                   "is a pipeline-hygiene escalation, not a forecast input")
        if why:
            refused.append((d["opportunity_id"], why))
        else:
            kept.append(d)
    checks.append(("every kept row carries a future-dated close", True, f"{len(kept)} kept, {len(refused)} refused"))

    # ---- findings the reader must have before the numbers
    probs_by_stage = defaultdict(set)
    for d in kept:
        probs_by_stage[d["stage"]].add(d["probability"])
    all_default = all(len(v) == 1 for v in probs_by_stage.values())
    if all_default:
        findings.append(("F1", "Every probability in the export is its stage default - no deal "
                         "carries rep-entered judgement. The weighted band is therefore a "
                         "stage-mix statistic, not deal-level intelligence, and moves only when "
                         "deals change stage."))
    findings.append(("F2", "Staleness is not observable: the export carries no last-modified "
                     "date, so a probability untouched for ninety days and one reviewed "
                     "yesterday are indistinguishable. Schema request: last_activity_date on "
                     "the CRM export."))
    findings.append(("F3", "forecast-method.md requires stage probabilities 'adjusted for the "
                     "historical stage-to-close conversion rather than the CRM's stated "
                     "probability'. That adjustment is NOT COMPUTABLE: the export holds open "
                     "deals only, and no closed-deal history ships with the instance. CRM "
                     "stated probabilities are used, and every weighted figure in these files "
                     "carries that basis."))
    findings.append(("F4", "Weighted pipeline is not a registered metric. Proposed registry "
                     "entry (not registered by this engine): MET-016, weighted pipeline by "
                     "close month, basis = CRM stage probability pending F3's history. "
                     "Proposed DEF: a closed deal's subscription revenue begins the month "
                     "after close at ACV/12; services attach and commissions are separate "
                     "lines, not modelled here."))
    findings.append(("F5", f"The plan comparison reads its new-business figures from prose "
                     f"({PLAN_SOURCE}). Schema request: the ARR walk as a plan export, so the "
                     f"constants block in this engine can be deleted."))

    # ---- deal surface with bands and phasing
    surface = []
    for d in kept:
        cm = month_of(d["expected_close_date"])
        acv, p = float(d["acv_usd"]), float(d["probability"])
        surface.append({
            "opportunity_id": d["opportunity_id"], "account_name": d["account_name"],
            "segment": d["segment"], "stage": d["stage"], "probability": f"{p:.2f}",
            "acv_usd": f"{acv:.2f}", "weighted_acv_usd": f"{p*acv:.2f}",
            "close_month": cm, "revenue_starts": add_month(cm),
            "in_commit": "Y" if d["stage"] in COMMIT_STAGES else "N",
            "basis": "CRM stage probability (F3)",
        })

    by_month = defaultdict(lambda: {"deals": 0, "commit_usd": 0.0, "weighted_usd": 0.0, "best_case_usd": 0.0})
    for r in surface:
        b = by_month[r["close_month"]]
        b["deals"] += 1
        b["weighted_usd"] += float(r["weighted_acv_usd"])
        b["best_case_usd"] += float(r["acv_usd"])
        if r["in_commit"] == "Y":
            b["commit_usd"] += float(r["acv_usd"])

    tie = abs(sum(b["weighted_usd"] for b in by_month.values()) - sum(float(r["weighted_acv_usd"]) for r in surface))
    checks.append(("by-month weighted ties to the deal surface", tie < 0.01, f"residual {tie:.2f}"))

    # ---- the quarter against the plan
    # ARR grain: what the plan assumes closes in the open months vs what the pipeline holds.
    # Revenue grain: only a February close touches Q1 revenue (one month, March, at ACV/12).
    vs_plan_rows, lbe_feed = [], None
    for band in ("commit_usd", "weighted_usd", "best_case_usd"):
        arr_open = sum(by_month[m][band] for m in Q_OPEN if m in by_month)
        plan_arr = PLAN_NET_NEW_ARR_MONTHLY * len(Q_OPEN)
        gap = arr_open - plan_arr
        rev_q1 = (by_month[Q_OPEN[0]][band] if Q_OPEN[0] in by_month else 0.0) / 12.0
        plan_rev_q1 = PLAN_NET_NEW_ARR_MONTHLY / 12.0
        vs_plan_rows.append({
            "band": band.replace("_usd", ""),
            "new_acv_closing_feb_mar_usd": f"{arr_open:.2f}",
            "plan_net_new_arr_feb_mar_usd": f"{plan_arr:.2f}",
            "arr_gap_usd": f"{gap:.2f}",
            "q1_revenue_effect_usd": f"{rev_q1 - plan_rev_q1:.2f}",
            "note": "gross new business only; plan figure is NET new ARR - churn sits in tier 2, "
                    "so a fair gap needs the renewal-adjusted tier beside this one",
        })
        if band == "weighted_usd":
            lbe_feed = {
                "period": "2026-03", "account": "4000",
                "account_name": "Subscription revenue - platform",
                "proposed_effect_usd": f"{rev_q1 - plan_rev_q1:.2f}",
                "half": "materializes",
                "basis": "tier-3 weighted pipeline vs plan new-business assumption; one month of "
                         "revenue on February closes at ACV/12 (F4 conversion DEF, proposed)",
                "ratified": "N",
            }

    # ---- write everything
    out = P("06-forecast", "FY2026")
    def dump(name, rows, fieldnames):
        with open(os.path.join(out, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

    dump(f"pipeline_surface_{PERIOD}.csv", surface, list(surface[0].keys()))
    month_rows = [{"close_month": m, "deals": b["deals"],
                   "commit_usd": f"{b['commit_usd']:.2f}", "weighted_usd": f"{b['weighted_usd']:.2f}",
                   "best_case_usd": f"{b['best_case_usd']:.2f}",
                   "revenue_starts": add_month(m)}
                  for m, b in sorted(by_month.items())]
    dump(f"pipeline_by_month_{PERIOD}.csv", month_rows, list(month_rows[0].keys()))
    dump(f"pipeline_vs_plan_{PERIOD}.csv", vs_plan_rows, list(vs_plan_rows[0].keys()))
    dump(f"pipeline_lbe_feed_{PERIOD}.csv", [lbe_feed], list(lbe_feed.keys()))

    with open(os.path.join(out, f"pipeline_notes_{PERIOD}.md"), "w", encoding="utf-8") as f:
        f.write(f"# Pipeline surface - {PERIOD} snapshot\n\n")
        f.write("Tier 3 of forecast-method.md, first implementation. Bands are never summed "
                "with tier 1 or 2, and the LBE feed row is a proposal at ratified=N.\n\n")
        f.write("## Bands (all open deals, all close months)\n\n")
        tw = sum(b["weighted_usd"] for b in by_month.values())
        tc = sum(b["commit_usd"] for b in by_month.values())
        tb = sum(b["best_case_usd"] for b in by_month.values())
        f.write(f"| Band | USD | May claim |\n|---|---:|---|\n")
        f.write(f"| Commit | {tc:,.0f} | what sales says will close (stages 5-6) |\n")
        f.write(f"| Weighted | {tw:,.0f} | stage-mix expectation - see F1 and F3 |\n")
        f.write(f"| Best case | {tb:,.0f} | ceiling: every open deal at full ACV |\n\n")
        f.write("## Findings\n\n")
        for fid, txt in findings:
            f.write(f"**{fid}.** {txt}\n\n")
        if refused:
            f.write("## Refused rows\n\n")
            for oid, why in refused:
                f.write(f"- {oid}: {why}\n")
        f.write("\n## Back-test\n\nREFUSED - scoring the weighted band requires a later "
                "snapshot and a closed-won register; this instance holds one snapshot and no "
                "closed-deal history. The refusal retires when a second monthly snapshot exists.\n")
        f.write("\n## Checks\n\n")
        for name, ok, detail in checks:
            f.write(f"- {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else "") + "\n")

    for name, ok, detail in checks:
        print(("PASS  " if ok else "FAIL  ") + name + ("  " + detail if detail else ""))
    print(f"\n{len(surface)} deals on the surface, {len(refused)} refused, "
          f"{len(findings)} findings, LBE feed at ratified=N")
    return all(ok for _, ok, _ in checks)

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
    sys.exit(0 if build(folder) else 1)
