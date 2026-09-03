"""Tie-out suite. Reads the OUTPUT files, never the generator's working numbers."""
import csv, os, json, glob, sys, re
from collections import defaultdict

# The instance folder. Taken from argv so the checker runs wherever the instance lives -
# on the build machine, or on the laptop that holds the delivered copy. A hardcoded path is
# a portability claim that has never been tested.
OUT = (sys.argv[1] if len(sys.argv) > 1 else
       os.environ.get("ARCLINE_FOLDER", "/home/claude/out/Arcline-Finance"))
P = lambda *a: os.path.join(OUT, *a)
FAIL, PASS = [], []


def chk(name, cond, detail=""):
    (PASS if cond else FAIL).append(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")


def rd(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def f(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


gl = rd(P("03-actuals", "FY2025", "gl_journal_2025.csv")) + rd(P("03-actuals", "FY2026", "gl_journal_2026-01.csv"))
chk("GL has rows", len(gl) > 8000, f"{len(gl):,} lines")

# 1 every entry balances
byid = defaultdict(float)
for l in gl:
    byid[l["entry_id"]] += f(l["amount_usd"])
bad = {k: v for k, v in byid.items() if abs(v) > 0.011}
chk("Every journal entry balances", not bad, f"{len(byid):,} entries, {len(bad)} unbalanced")

# 2 debits equal credits
d = sum(f(l["debit"]) for l in gl); c = sum(f(l["credit"]) for l in gl)
chk("Total debits equal total credits", abs(d - c) < 0.05, f"{d:,.2f} vs {c:,.2f}")

# 3 trial balance nets to zero every period
tb = rd(P("03-actuals", "FY2025", "trial_balance_2025_monthly.csv")) + rd(P("03-actuals", "FY2026", "trial_balance_2026-01.csv"))
per_mv = defaultdict(float)
for r in tb:
    per_mv[r["period"]] += f(r["period_movement"])
chk("Trial balance movement nets to zero in every period",
    all(abs(v) < 0.05 for v in per_mv.values()), f"{len(per_mv)} periods, max {max(abs(v) for v in per_mv.values()):.4f}")

# 4 TB movements agree to the GL
glmv = defaultdict(float)
for l in gl:
    glmv[(l["period"], l["account"])] += f(l["amount_usd"])
tbmv = {(r["period"], r["account"]): f(r["period_movement"]) for r in tb}
diff = [k for k in glmv if abs(glmv[k] - tbmv.get(k, 0.0)) > 0.02]
chk("Trial balance ties to the general ledger", not diff, f"{len(diff)} account-periods differ")

# 5 balance sheet balances every period
bs = rd(P("03-actuals", "FY2025", "balance_sheet_2025_monthly.csv")) + rd(P("03-actuals", "FY2026", "balance_sheet_2026-01.csv"))
checks = [r for r in bs if r["account_name"].startswith("CHECK")]
chk("Balance sheet balances in every period",
    all(abs(f(r["closing_balance_usd"])) < 0.05 for r in checks),
    f"{len(checks)} periods, max {max(abs(f(r['closing_balance_usd'])) for r in checks):.4f}")

# 6 P&L subtotals internally consistent, and tie to the GL
pl = rd(P("03-actuals", "FY2025", "pnl_2025_monthly.csv")) + rd(P("03-actuals", "FY2026", "pnl_2026-01.csv"))
sub = defaultdict(dict)
for r in pl:
    if r["fsli"] == "Subtotal":
        sub[r["period"]][r["account_name"]] = f(r["amount_usd"])
ok = True
for p, s in sub.items():
    if abs((s["SUBTOTAL Total revenue"] - s["SUBTOTAL Cost of revenue"]) - s["SUBTOTAL Gross profit"]) > 0.05:
        ok = False
    if abs((s["SUBTOTAL Research and development"] + s["SUBTOTAL Sales and marketing"] +
            s["SUBTOTAL General and administrative"]) - s["SUBTOTAL Total operating expense"]) > 0.05:
        ok = False
chk("P&L subtotals foot", ok, f"{len(sub)} periods")

glrev = defaultdict(float)
for l in gl:
    if l["account"][0] == "4":
        glrev[l["period"]] -= f(l["amount_usd"])
chk("P&L revenue ties to the GL",
    all(abs(glrev[p] - sub[p]["SUBTOTAL Total revenue"]) < 0.05 for p in sub),
    f"max {max(abs(glrev[p]-sub[p]['SUBTOTAL Total revenue']) for p in sub):.4f}")

# 7 ARR waterfall ties
w = rd(P("03-actuals", "FY2025", "arr_waterfall_2025.csv"))
chk("ARR waterfall ties in every period", all(abs(f(r["check"])) < 0.05 for r in w), f"{len(w)} periods")

arr = rd(P("03-actuals", "FY2025", "arr_schedule_2025.csv"))
chk("Closing ARR at Dec-25 is 17.6m", abs(f(arr[-1]["committed_arr_usd"]) - 17_600_000) < 60_000,
    f"{f(arr[-1]['committed_arr_usd']):,.0f}")

# 8 subledgers foot to their control accounts
ap = rd(P("03-actuals", "FY2025", "ap_bills_2025.csv")) + rd(P("03-actuals", "FY2026", "ap_bills_2026-01.csv"))
ar = rd(P("03-actuals", "FY2025", "ar_invoices_2025.csv")) + rd(P("03-actuals", "FY2026", "ar_invoices_2026-01.csv"))
chk("AP subledger has vendor-level detail", len({r["vendor_name"] for r in ap}) > 60,
    f"{len(ap):,} bills across {len({r['vendor_name'] for r in ap})} vendors")
chk("AR subledger has customer-level detail", len({r["customer_name"] for r in ar}) > 100,
    f"{len(ar):,} invoices across {len({r['customer_name'] for r in ar})} customers")

open_ar = sum(f(r["amount_usd"]) for r in ar if r["status"] != "Paid")
bs_ar = [r for r in bs if r["period"] == "2026-01" and r["account"] == "1100"]
chk("Open AR is within a reasonable band of the AR control account",
    abs(open_ar - f(bs_ar[0]["closing_balance_usd"])) / max(open_ar, 1) < 0.35,
    f"subledger {open_ar:,.0f} vs GL {f(bs_ar[0]['closing_balance_usd']):,.0f}")

# 9 every JE type in the ledger is defined
types = {r["je_type"] for r in rd(P("00-company", "je_types.csv"))}
used = {l["je_type"] for l in gl}
chk("Every JE type used is defined", used <= types, f"{len(used)} used, undefined: {used - types}")

# 10 every account used is in the chart of accounts
coa = {r["account"] for r in rd(P("00-company", "chart_of_accounts.csv"))}
chk("Every account used is in the chart of accounts", {l["account"] for l in gl} <= coa, "")

# 11 every cost centre used is defined
ccs = {r["cost_center"] for r in rd(P("00-company", "cost_centers.csv"))}
used_cc = {l["cost_center"] for l in gl if l["cost_center"]}
chk("Every cost centre used is defined", used_cc <= ccs, f"{used_cc - ccs}")

# 12 plan exists for every FY26 month and every FY25 month
p26 = rd(P("02-budget", "FY2026", "plan_fy26_pnl_monthly.csv"))
chk("FY2026 plan covers twelve months", len({r["period"] for r in p26}) == 12, "")
p25 = rd(P("02-budget", "FY2025", "plan_fy25_pnl_monthly.csv"))
chk("FY2025 plan covers twelve months", len({r["period"] for r in p25}) == 12, "")

# 13 January variance is computable and non-trivial
jan_a = {r["account"]: f(r["amount_usd"]) for r in pl if r["period"] == "2026-01" and r["account"]}
jan_p = {r["account"]: f(r["amount_usd"]) for r in p26 if r["period"] == "2026-01" and r["account"]}
var = {a: jan_p.get(a, 0) - jan_a.get(a, 0) for a in set(jan_a) | set(jan_p)}
big = {a: v for a, v in var.items() if abs(v) > 40_000}
chk("January carries material variances to explain", len(big) >= 5,
    f"{len(big)} lines over USD 40k: {sorted(big, key=lambda a: -abs(big[a]))[:6]}")

# 14 the planted issues are all present in the manifest
man = rd(P("99-answer-key", "planted_issues.csv"))
chk("Answer key lists 25 planted issues", len(man) == 25, f"{len(man)}")

# 15 spot-check three plants in the data
# The duplicate is checked by its SHAPE, not by its amount. This check used to assert the
# literal 47,200, which meant it could only ever pass on one instance: the first sealed build
# changed the magnitude, as a sealed build is supposed to, and the checker called the correct
# result a failure. A check that hardcodes what it is looking for is a check that has been
# fitted to one dataset.
# The expected amount is read from the DERIVED answer key, not typed here. That makes this a
# genuine tie-out - the key is computed from the finished ledger, so agreeing with it proves
# the two agree - and it holds on any instance, which a literal cannot. A first attempt
# checked the duplicate by shape instead and matched nineteen ordinary flat-fee vendors: a
# check that passes on noise is not a check either.
_k = {r["issue_id"]: r for r in rd(P("99-answer-key", "planted_issues.csv"))}
_m = re.search(r"USD ([\d,]+)", _k["PL-01"]["expected_finding"]) if "PL-01" in _k else None
_want = float(_m.group(1).replace(",", "")) if _m else None
_ref = re.search(r"(BILL-\S+)", _k["PL-01"]["where_it_lives"]) if "PL-01" in _k else None
hit = [l for l in gl if l["period"] == "2026-01" and abs(f(l["debit"]) - (_want or -1)) < 1]
chk("PL-01 the duplicate bill the key names is in the ledger", bool(_want) and bool(hit),
    f"key says USD {_want:,.0f}; {len(hit)} matching debit(s), ref {_ref.group(1) if _ref else '?'}"
    if _want else "no amount in the key")
# the plant is the ABSENCE of the routine 1-January reversal. The close then posted a
# correcting entry, which does not un-plant it: the evidence of both is in the ledger.
routine = [l for l in gl if l["period"] == "2026-01" and l["vendor_name"] == "Anthropic PBC"
           and l["document_ref"].startswith("REV-2025-12")]
chk("PL-03 the routine January reversal of the Anthropic accrual is still absent",
    not routine, f"{len(routine)} found")
correction = {l["document_ref"] for l in gl if l["document_ref"] == "ADJ-2026-01-001"}
chk("PL-03 the close posted a correcting entry for it", bool(correction), f"{correction}")
rcl = [l for l in gl if l["document_ref"] == "RCL-2026-011"]
chk("PL-13 unsupported reclass is present and self-approved",
    rcl and rcl[0]["attachment_ref"] == "" and rcl[0]["entry_date"] > "2026-02-01", "")

# 15b usage overage foots to the revenue account it drives
u = rd(P("03-actuals", "FY2025", "usage_2025_monthly.csv")) + rd(P("03-actuals", "FY2026", "usage_2026-01.csv"))
uo = defaultdict(float)
for r in u:
    uo[r["period"]] += f(r["overage_amount_usd"])
gl4010 = defaultdict(float)
for l in gl:
    if l["account"] == "4010":
        gl4010[l["period"]] -= f(l["amount_usd"])
worst = max(abs(uo[p] - gl4010[p]) for p in uo)
chk("Usage overage foots to account 4010 in every period", worst < 0.05, f"max {worst:.4f}")

# 15c one customer_id, one name, everywhere
names = defaultdict(set)
for path, idc, namec in [
    (P("07-contracts", "customers", "customer_agreements.csv"), "customer_id", "customer_name"),
    (P("07-contracts", "customers", "customer_mrr_changes.csv"), "customer_id", "customer_name"),
    (P("07-contracts", "customers", "amendments.csv"), "customer_id", "customer_name"),
    (P("03-actuals", "FY2025", "usage_2025_monthly.csv"), "customer_id", "customer_name"),
    (P("03-actuals", "FY2026", "usage_2026-01.csv"), "customer_id", "customer_name"),
    (P("03-actuals", "FY2025", "ar_invoices_2025.csv"), "customer_id", "customer_name"),
    (P("03-actuals", "FY2026", "ar_invoices_2026-01.csv"), "customer_id", "customer_name")]:
    for r in rd(path):
        if r[idc]:
            names[r[idc]].add(r[namec])
split = {k: v for k, v in names.items() if len(v) > 1}
chk("Every customer_id carries one name in every file", not split, f"{len(split)} split identities")

# 15d every preparer and approver exists on the headcount register
roster = {r["name"] for r in rd(P("03-actuals", "FY2025", "headcount_2025.csv"))}
def initialled(n):
    n = n.split(" (")[0]
    return n
people_refs = set()
for l in gl:
    for who in (l["preparer"], l["approver"]):
        w = initialled(who)
        if w and "(auto)" not in w and w not in ("Armanino LLP",):
            people_refs.add(w)
def matches(ref):
    parts = ref.replace(".", "").split()
    if len(parts) < 2:
        return True
    ini, last = parts[0], parts[-1]
    return any(p.split()[-1] == last and p[0] == ini[0] for p in roster)
orphan = sorted(x for x in people_refs if not matches(x))
chk("Every named preparer and approver is on the headcount register", not orphan, f"{orphan}")

# 15e the answer key is derived, not typed: every amount must appear in the data
man = rd(P("99-answer-key", "planted_issues.csv"))
blank = [r["issue_id"] for r in man if not r["expected_finding"].strip()]
chk("Every manifest entry states an expected finding", not blank, f"{blank}")

# 15f the vendor build IS the budget: it must foot to the P&L plan in every period
vp = rd(P("02-budget", "FY2026", "plan_fy26_by_vendor.csv"))
roll = defaultdict(float)
for r in vp:
    roll[(r["period"], r["account"])] += f(r["plan_usd"])
plnacc = {(r["period"], r["account"]): f(r["amount_usd"]) for r in p26 if r["account"]}
off = [k for k in roll if abs(roll[k] - plnacc.get(k, 0.0)) > 0.05]
chk("Bottom-up vendor budget foots to the P&L plan in every period", not off,
    f"{len(roll)} account-periods, {len(off)} off")

# 15g every planned vendor is a real vendor
vm = {r["vendor_name"] for r in rd(P("07-contracts", "vendors", "vendor_master.csv"))}
vm |= {"(no vendor - internal entry)", "(customer billing)", "Miscellaneous suppliers (under $5k)"}
ghosts = {r["vendor_name"] for r in vp} - vm
chk("Every vendor in the budget exists in the vendor master", not ghosts, f"{sorted(ghosts)[:4]}")

# 15h every planned line carries a written basis and an owner
nobasis = [r for r in vp if not r["basis"].strip() or not r["owner"].strip()]
chk("Every budget line carries a basis and a named owner", not nobasis, f"{len(nobasis)} without")

# 15i the generator must be reproducible: no randomised hashing, no set iteration into RNG
import re as _re
gen = [g for g in glob.glob(P("_generator", "*.py"))
       if os.path.basename(g) != "validate.py"]   # the checker is not the generator
# An empty glob makes every scan below pass on nothing. That is how this check once
# reported clean against a mirror the build had stopped writing.
chk("Generator source is mirrored into the instance", len(gen) >= 10, f"{len(gen)} modules")
offenders = []
for gpath in gen:
    src = open(gpath, encoding="utf-8").read()
    for i, line in enumerate(src.splitlines(), 1):
        if line.strip().startswith("#"):
            continue
        if _re.search(r"(?<![_\w])hash\(", line) and "stable_hash" not in line:
            offenders.append(f"{os.path.basename(gpath)}:{i} bare hash()")
        # A set iterated into output ordering or an RNG is the defect. sorted() around it
        # is the remedy, so a line that already has one is not an offender - the first
        # version of this rule fired on the fix as loudly as on the fault.
        if _re.search(r"for\s+\w+\s+in\s+set\(", line) and "sorted(" not in line:
            offenders.append(f"{os.path.basename(gpath)}:{i} iterating a set")
chk("Generator contains nothing that varies between processes", not offenders, f"{offenders[:3]}")

# 15j the house lexicon, enforced on every generated artifact
sys.path.insert(0, P("_generator"))
import lexicon as _lex
lexhits = defaultdict(int)
for pth in glob.glob(P("**", "*"), recursive=True):
    if not os.path.isfile(pth) or pth.rsplit(".", 1)[-1] not in ("md", "csv", "json"):
        continue
    if os.sep + "_generator" + os.sep in pth:
        continue
    if os.path.basename(pth) == "reporting-standards.md":
        continue      # the register has to name what it bans; the rule book is not the rule
    for hit in _lex.violations(open(pth, encoding="utf-8", errors="ignore").read()):
        lexhits[hit.lower()] += 1
chk("House lexicon clean across every generated artifact", not lexhits,
    f"{sum(lexhits.values())} hits: {dict(list(lexhits.items())[:5])}")

# 15k-pre every operating expense line names an owner
# Payroll used to post with no cost center, so the budget had owners and the ledger did
# not, and opex-by-owner - the only cut a cost center owner is managed on - could not be
# struck from the actuals at all. 9xxx is below the line and correctly carries none.
no_cc = [l for l in gl if l["account"][0] in "678" and not l["cost_center"]]
chk("Every operating expense line carries a cost center", not no_cc,
    f"{len(no_cc)} lines, {sorted({l['account'] for l in no_cc})[:6]}")

# 15k cost center is an opex dimension only
cogs_cc = [l for l in gl if l["account"][0] == "5" and l["cost_center"]]
chk("No cost of revenue line carries a cost center", not cogs_cc, f"{len(cogs_cc)} lines")
vp_cc = [r for r in vp if r["account"][0] == "5" and r["cost_center"]]
chk("No cost of revenue budget line carries a cost center", not vp_cc, f"{len(vp_cc)} lines")

# 16 folder completeness
need = ["README.md", "00-company/chart_of_accounts.csv", "01-lrp/LRP-FY26-FY30.xlsx",
        "02-budget/FY2026/FY26-annual-plan.xlsx", "03-actuals/FY2026/gl_journal_2026-01.csv",
        "04-month-end-close/FY2026/2026-01/close_checklist.csv",
        "04-month-end-close/FY2026/2026-01/reconciliations/bank-reconciliation-2026-01.csv",
        "05-lbe/FY2026/lbe_q1_2026_input.csv", "06-forecast/FY2026/pipeline_2026-01.csv",
        "02-budget/FY2026/plan_fy26_by_vendor.csv",
        "07-contracts/customers/customer_mrr_changes.csv",
        "07-contracts/vendors/software_agreements.csv", "09-metrics/mapping.json",
        "99-answer-key/SEALED-answer-key.md"]
missing = [n for n in need if not os.path.exists(P(*n.split("/")))]
chk("Every expected artefact exists", not missing, f"missing: {missing}")

# The January variance analysis is ONE file. The engine's working CSVs are agent input
# and belong in the work directory; shipping them beside the workbook put six files named
# variance_* in one folder and buried the only one anybody opens.
vfiles = sorted(os.path.basename(p) for p in glob.glob(P("03-actuals", "FY2026", "variance*")))
if vfiles:
    chk("January variance analysis is a single deliverable",
        vfiles == ["variance_analysis_2026-01.xlsx"], f"{len(vfiles)}: {vfiles}")
else:
    chk("Variance analysis not yet produced for this instance", True,
        "this is a generated instance, not an analysed one")

# The indirect cash walk is a partition of every non-cash account, so it reaches the ledger
# cash balance by construction and `unexplained` is nil. It is printed anyway: a future
# account that lands in no bucket must announce itself rather than be absorbed.
for cf_path, label in ((P("03-actuals", "FY2025", "cash_flow_2025_monthly.csv"), "FY2025"),
                       (P("03-actuals", "FY2026", "cash_flow_2026-01.csv"), "January 2026")):
    # the first period on file has no opening balance sheet to move from, so every movement
    # in it is zero by construction and there is nothing to check
    cf = rd(cf_path)[1:] if label == "FY2025" else rd(cf_path)
    bad = [r for r in cf if abs(float(r["unexplained"])) > 0.5]
    chk(f"Cash walk reaches the ledger, {label}", not bad,
        f"{len(bad)} periods unexplained")
    off = [r for r in cf if abs(float(r["depreciation_and_amortization"])
                                - float(r["da_per_pnl"])) > 0.5]
    chk(f"Depreciation add-back agrees with the P&L, {label}", not off, f"{len(off)} periods")

# the cash flow's net result is the P&L's. Getting this sign wrong once made the cash flow
# report the SUM of revenue and cost - out by twice revenue, on every month of the year.
pl25 = {r["period"]: float(r["amount_usd"]) for r in rd(P("03-actuals", "FY2025", "pnl_2025_monthly.csv"))
        if r["account_name"] == "SUBTOTAL Net result"}
cf25 = rd(P("03-actuals", "FY2025", "cash_flow_2025_monthly.csv"))
off = [r["period"] for r in cf25 if abs(float(r["net_result"]) - pl25.get(r["period"], 0)) > 0.5]
chk("Cash flow net result ties to the P&L, every month", not off, f"{off[:4]}")

# Both January deliverables are single workbooks. Their contents are checked independently by
# packverify.py, which recomputes from the CSVs and reads the RECALCULATED workbook rather
# than the formulas the builder wrote.
# The pack and the LBE are ANALYST output, assembled by a later pipeline from a completed
# run. A freshly generated instance cannot have them yet, and asserting their existence
# unconditionally made a correct build report five failures - the checker was confusing
# "this instance has not been analysed yet" with "this instance is wrong".
PACK = P("08-reporting", "FY2026", "FY2026-01-management-pack.xlsx")
LBEF = P("05-lbe", "FY2026", "LBE_Q1_2026_M1.xlsx")
if os.path.exists(PACK) or os.path.exists(LBEF):
    for pth, label in ((PACK, "management pack"), (LBEF, "Q1 LBE")):
        chk(f"The January {label} exists", os.path.exists(pth), os.path.basename(pth))
    rep = sorted(os.path.basename(x) for x in glob.glob(P("08-reporting", "FY2026", "*.xlsx")))
    chk("The reporting pack is a single deliverable",
        rep == ["FY2026-01-management-pack.xlsx"], f"{len(rep)}: {rep}")
    lbes = sorted(os.path.basename(x) for x in glob.glob(P("05-lbe", "FY2026", "*.xlsx")))
    chk("One LBE artifact per build, stamped and never overwritten",
        lbes == ["LBE_Q1_2026_M1.xlsx"], f"{len(lbes)}: {lbes}")
else:
    chk("Analyst deliverables not yet produced for this instance", True,
        "pack and LBE checks skipped - this is a generated instance, not an analysed one")

# The monthly release of an annually-billed subscription is its CONTRACT value over twelve
# months. It used to be a share of the account's spend target, with the renewal back-derived
# as twelve times that share - so eight G&A subscriptions each released at 59.03% of ACV/12
# and eight R&D ones at 120.77%, to five decimal places. Eight vendors agreeing to the same
# fraction are not eight numbers; they are one number.
swa = {r["vendor_name"]: r for r in rd(P("07-contracts", "vendors", "software_agreements.csv"))}
rel = defaultdict(float)
for l in rd(P("03-actuals", "FY2026", "gl_journal_2026-01.csv")):
    if l["je_type"] == "PREPAID_AMORT" and f(l["amount_usd"]) > 0 and l["vendor_name"]:
        rel[l["vendor_name"]] += f(l["amount_usd"])
off = []
for v, amt in sorted(rel.items()):
    if v not in swa:
        continue
    # the release runs at the PRIOR term until a renewal is applied; PL-07 is the one that
    # was never applied, and the close's correcting entry brings it to the new contract
    expect = f(swa[v]["renewal_acv_usd"]) / 12.0
    if expect and abs(amt - expect) / expect > 0.02:
        off.append((v, round(amt), round(expect)))
chk("Every prepaid release ties to its contracted ACV", not off, f"{len(off)} off contract: {off[:3]}")

# Every precomputed input must be named in the runbook with the question it answers. PL-19
# was missed because arr_movement_gross.csv was handed over and nothing pointed at it - a
# file in the inputs that no instruction names is a file nobody opens.
rb_path = P("04-month-end-close", "analyst-runbook.md")
rb = open(rb_path, encoding="utf-8").read() if os.path.exists(rb_path) else ""
desk = P("04-month-end-close", "analyst-inputs")
work = (os.environ.get("ARCLINE_WORK")
        or (desk if glob.glob(os.path.join(desk, "*.csv")) else None)
        or os.path.join("/home/claude/work", os.path.basename(OUT.rstrip("/"))))
inputs = sorted(os.path.basename(x) for x in glob.glob(os.path.join(work, "*.csv")))
unnamed = [i for i in inputs
           if i.replace("2026-01", "<period>").rsplit(".", 1)[0] not in rb
           and i.rsplit(".", 1)[0] not in rb]
# An empty work directory must NOT pass this check. A test whose subject is missing has not
# been satisfied, it has been skipped - and the determinism check already taught us once that
# a green light on an empty glob is worse than a red one, because nobody investigates green.
chk("Every precomputed input is named in the analyst runbook",
    bool(inputs) and not unnamed,
    f"{len(inputs)} inputs, unnamed: {unnamed}" if inputs
    else f"NO INPUTS FOUND in {work} - check not exercised, so it fails")

n_files = sum(len(fs) for _, _, fs in os.walk(OUT))
# The code beside the data must be the code that produced it - or the difference must be
# named. A mismatch is not automatically wrong: the generator may have moved on deliberately
# while a signed period is left standing. What is not acceptable is that it happens silently.
import buildstamp as _bs
_state, _detail = _bs.compare(OUT)
chk("The instance names the generator that built it", _state == "match", f"{_state}: {_detail}")

chk("Folder has substance", n_files > 60, f"{n_files} files")

for line in PASS + FAIL:
    print(line)
print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
