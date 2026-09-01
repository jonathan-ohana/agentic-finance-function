# 10 — CourtIQ: Company Design Spec

*Day 1 deliverable of the Aug 17–28 sprint. This is the specification the Day 2–3 data generators read from. Every number here is a **target** for the generator, not a fact — Day 2 reconciles them to the penny. Last updated Mon 8/17, 2026.*

> **Edge cases: see `12-edge-case-design.md`.** The twelve-candidate list originally in this doc was cut to ten and reworked in Fable session #1. Doc 12 is authoritative for what gets planted; the summary below is retained only for context.

---

## Decisions locked

| Decision | Answer |
|---|---|
| Company | **CourtIQ** — padel-specific AI coaching and match intelligence |
| Fidelity | **Flat files** (CSV/JSON) standing in for GL, billing, CRM, HRIS, bank, and inference-usage logs. Real third-party sandboxes explicitly deferred per the sprint plan. |
| Anchor workflow | **Close July 2026 → variance vs. plan → rolling forecast refresh → board pack** |
| Geography | EU-first (Spain, France, Italy, Portugal), young US business. Delaware parent, USD functional currency, EUR primary billing currency |
| Hardware | Club cameras owned and installed by CourtIQ; consumers self-film on a phone with a court mount |
| History window | **Feb 2025 – Jul 2026** (18 months). Jul 2026 is the last closed month and the close-demo month. Aug 2026 is open. |

---

## The company

CourtIQ sells padel match intelligence. Computer vision analyses match video and returns telemetry — unforced errors, shot distribution, court positioning, rally length, pair coordination — plus coaching recommendations on what to correct. Two capture paths: clubs get fixed cameras installed above the court, consumers film themselves on a phone in a court mount.

Series A, closed April 2025. **33 FTE** as of Jul 2026, up from 18 in Feb 2025. HQ Madrid; Delaware parent (CourtIQ Inc.) with EU staff employed through an EOR (Deel) — no EU legal entity yet, which is deliberate: it makes the payroll source data EOR invoices rather than clean payroll registers, and that mess is realistic.

Padel is the point. It's the fastest-growing racquet sport in Europe, the clubs are small businesses with 4–12 courts, and the sport is seasonal in a way that shows up hard in the numbers.

## Revenue model — four streams, on purpose

| Stream | Motion | Pricing | Contract | Billing |
|---|---|---|---|---|
| **Player** (B2C) | Self-serve, freemium | Free: 1 match/mo. Pro €12.99/mo or €119/yr | Monthly or annual, no commitment | Card (Stripe), in advance |
| **Courts** (B2B club) | Sales-led | €89/court/month, 4-court minimum, includes camera hardware and 120 analysed matches/court/month | 12–36 months, annual prepay or quarterly | Invoice, EUR, net 30 |
| **Academy** (B2B2C) | Inside sales | €39/coach/month, up to 25 managed players | Annual | Card or invoice |
| **Usage & events** | — | Overage €1.20/match above allowance; tournament packages €2,500–8,000 fixed | None (arrears / one-off) | Quarterly in arrears; events on completion |

This mix is the reason the company was chosen. It forces every hard definition question at once, and it makes the semantic layer a necessity rather than a nicety.

### Target scale at Jul 2026

| Metric | Target |
|---|---|
| Paying Player subs | 14,200 (blended €11.20/mo — annual-plan discounting drags it below list) |
| Clubs / courts | 238 clubs, 1,560 courts |
| Academy coaches | 940 |
| Committed recurring ARR | **$4.30M** (Courts $1.80M, Player $2.05M, Academy $0.45M) |
| Usage overage, annualised | $0.38M |
| Tournament revenue, TTM | $0.24M |
| Jul 2026 revenue | ~$400k |
| Blended gross margin | ~68% |
| Net burn | ~$395k/month |
| Cash at Jul 31 | $6.1M → **~15 months runway** |

**The number the board sees depends on who assembles it.** Committed recurring is $4.30M. Add usage at run-rate and it's $4.68M. Add trailing tournament revenue the way the VP Sales does and it's $4.92M. All three are defensible; only one belongs in a board pack; the semantic layer is where that gets decided and versioned. This gap is the single most important artefact in the whole build.

---

## Chart of accounts

Four-digit, designed so the contested allocations are visible rather than buried.

**Assets (1xxx)** — 1010 Cash operating USD · 1015 Cash EUR · 1020 Stripe balance in transit · 1100 Accounts receivable · 1150 Allowance for doubtful accounts · 1200 Prepaid expenses · 1210 Prepaid compute commitment · 1300 Camera inventory (uninstalled) · 1500 Deployed camera assets · 1590 Accumulated depreciation

**Liabilities & equity (2xxx–3xxx)** — 2010 Accounts payable · 2020 Accrued expenses · 2030 Accrued payroll & EOR · 2050 Deferred revenue current · 2055 Deferred revenue non-current · 2060 Unused match-allowance liability · 2100 Venture debt · 3010 Preferred stock · 3020 Common stock · 3030 APIC · 3090 Accumulated deficit

**Revenue (4xxx)** — 4010 Player subscription · 4020 Courts subscription · 4025 Academy subscription · 4030 Usage overage · 4040 Tournament & events · 4090 Refunds, credits & chargebacks (contra)

**COGS (5xxx)** — 5010 GPU inference compute · 5020 Video storage & egress · 5030 Baseline hosting & CDN · 5040 Depreciation — deployed cameras · 5045 Installation & field service · 5050 Payment processing fees · 5060 Customer support allocation · 5080 Club revenue share

**Operating expense (6xxx–8xxx)** — 6xxx R&D (salaries, ML research compute, contractors, tooling) · 7xxx S&M (salaries, paid acquisition, app-store fees, events, partner commissions, travel) · 8xxx G&A (salaries, EOR fees, legal, accounting, insurance, coworking, software, bank fees)

**Below the line (9xxx)** — 9010 FX gain/loss · 9020 Interest income · 9030 Interest expense · 9090 Income tax

**Three allocation calls the CoA deliberately exposes** — each one a decision the semantic layer must record with a rationale, because each one moves gross margin by points:

1. **ML research compute: R&D or COGS?** Training and evaluation runs go to 6xxx; per-match inference goes to 5010. The boundary is genuinely fuzzy and the engineering team's cloud bill arrives as one line.
2. **Customer support: COGS or S&M?** Split by segment — club onboarding support is COGS, consumer growth-driven support is S&M.
3. **Cameras: inventory, CapEx, or COGS?** Purchased into 1300, transferred to 1500 on installation, depreciated over 36 months into 5040. Installs are batched monthly (simplified per doc 12).

---

## Rosters (generator inputs)

**Headcount — 33 FTE at Jul 2026, from 18 at Feb 2025.** Engineering & ML 12 (4 CV/ML) · Product & Design 3 · Club Sales 6 · Growth/consumer marketing 3 · Customer Success & field ops 4 · Executive 3 (CEO, CTO, COO) · G&A 2 (People/Ops, and the finance seat). Roughly 70% EU via EOR, 30% US direct. Average fully-loaded cost ~$130k.

**Customers — ~15,300 records across three very different shapes.** 14,200 Player subs (high volume, low value, monthly churn 3.4%, no contracts, card data only). 238 clubs (named accounts, signed contracts, 4–24 courts, concentrated in Spain 44% / France 18% / Italy 16% / Portugal 9% / US 8% / other 5%). 940 Academy coaches. Plus 2 federation-level accounts with bespoke terms.

**Vendors — ~55 records.** GPU/inference provider (the largest single vendor), cloud hosting, video storage/CDN, camera manufacturer, EU logistics and installation partners, Deel, Stripe, HubSpot, standard SaaS stack, legal, accounting, insurance, Madrid coworking.

---

## 18-month event timeline

| When | Event | Why it's in |
|---|---|---|
| Feb 2025 | History opens. 18 FTE, ARR ~$1.9M | Baseline |
| Apr 2025 | Series A closes, $12M | Cash step-change, preferred stock, plan reset |
| Apr 2025 | **Usage logs partial for the month** | Data gap — does the agent flag it or interpolate? |
| May–Aug 2025 | Hiring ramp, 18 → 27 FTE | Plan-vs-actual hiring drift |
| Jul–Aug 2025 | European outdoor peak | Seasonality: usage, inference COGS, consumer signups all peak |
| Sep 2025 | Player Pro €9.99 → €12.99, existing users grandfathered | Two price cohorts forever |
| Sep→Nov 2025 | Planned Sept hire actually starts in November | Plan-vs-actual on the largest cost driver |
| Nov 2025 | Model swap cuts inference cost per match 45% | Gross margin improves for reasons unrelated to operations |
| Dec 2025 | Black Friday annual plans at 40% off; winter usage trough | Deferred revenue + discounted-ARR question + seasonal low |
| Q4 2025 | Bulk purchase, 1,000 cameras | Inventory build, working capital, cash |
| Jan 2026 | $480k/yr prepaid GPU compute commitment signed | Prepaid asset, amortisation, utilisation risk |
| Jan 2026 | **Board plan set** | Baseline #1 |
| Feb 2026 | Federation deal signed, non-standard terms | The messy enterprise contract |
| Q1–Q2 2026 | Cameras installed from inventory, monthly batches | Inventory → CapEx transfer |
| Mar 2026 | Duplicate vendor invoice paid | Routine Bookkeeper catch |
| Apr 2026 | Italian club chain renews 8 courts → 5 | Contraction, mislabelled in CRM |
| Apr 2026 | **Reforecast issued** | Baseline #2 — "vs. plan" now has two answers |
| ~Q1–Q2 2026 | Termination fee buried in a routine monthly EOR invoice | Does the Bookkeeper read invoices or patterns? |
| May 2026 | App-store feature drives consumer signup surge | Inference spike; partially offsets the Nov margin gain to net +6pts |
| Jun 2026 | Two tournament events | One-off revenue that must not enter run-rate |
| **Jul 2026** | **Close-demo month** | The month the agents actually close |
| Aug 2026 | Open month | Current-period cash and forecast work |

---

## Planted edge cases

**Superseded by `12-edge-case-design.md`.** Ten designed cases, each testing a distinct failure mode, plus three demoted to ambient conditions (FX, camera CapEx mechanics, duplicate invoice) and three new generator-level traps (hire-date drift, EOR termination fee, Apr 2025 usage gap). Doc 12 is what the generator builds against.

---

## Open items

- Exact monthly P&L reconciliation — Day 2, in the generator, not by hand.
- Whether the Feb 2026 federation deal is EUR or USD denominated (leaning EUR, to load the FX case).
- ~~Board plan versions~~ — **resolved**: Jan 2026 plan and Apr 2026 reforecast, both retained, neither labelled canonical. Promoted to edge case #10.
