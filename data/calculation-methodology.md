# CourtIQ — How Every Metric Is Calculated

*Companion to the Day 2 dataset. This is the calculation methodology behind every number in the review pack. It is also the raw material for the semantic layer on Day 5 — most of what follows is a definition that will need a formal ruling.*

---

## The spine

Everything derives from four driver populations, month by month:

- **Courts in force** — how many club courts are live and billable
- **Active player subscriptions** — split by plan (monthly / annual) and price cohort (legacy / current / Black Friday)
- **Active coach seats**
- **Matches analysed** — the usage volume that drives both overage revenue and inference cost

Every revenue and cost line traces back to one of those four. Nothing is a plug.

---

## Revenue

All prices are set in EUR. Reporting currency is USD. Each month's EUR amounts convert at that month's average EUR/USD rate, which drifts from 1.052 in Feb 2025 to 1.118 by Jul 2026.

### Courts (B2B clubs) — account 4020

Clubs are billed **in advance**: 40% pay annually, 60% quarterly. An invoice equals `courts × €89 × months covered`, and it is booked as a debit to accounts receivable and a credit to deferred revenue — no revenue at billing.

Revenue is then recognised at `courts in force × €89` each month, released out of that deferred balance. A club that prepays twelve months in January carries eleven months of deferred revenue into the following year.

### Player (B2C) — account 4010

**Monthly plans:** billed and recognised in the same month, at the subscriber's actual price. Three prices coexist permanently: €9.99 for anyone who signed up before September 2025 (grandfathered), €12.99 for everyone after, and the Black Friday cohort on annual terms.

**Annual plans:** the full price is billed on the signup anniversary and credited to deferred revenue, then recognised at one twelfth per month.

The distinction matters: 30% of subscribers are on annual plans, so a material part of consumer cash arrives up to twelve months before the revenue does.

### Academy — account 4025

Coach seats bill annually on the signup anniversary and recognise €39 per month.

### Usage overage — account 4030

Each club gets 120 analysed matches per court per month included. Anything above that bills at €1.20 per match.

**Revenue is recognised in the month the matches are consumed.** Invoicing happens quarterly in arrears — January, April, July and October, covering the prior three months. Between the two, unbilled receivable accrues. This is the line that makes the "is usage part of ARR" question real, because it is genuinely recurring and genuinely variable.

### Tournaments — account 4040

Fixed-fee events recognised on completion. Seven events across the window; June 2026 carries $100k of the $144k total.

### Refunds, credits and chargebacks — account 4090

Contra-revenue, running 0.4–0.9% of recognised Player and Courts revenue.

---

## Cost of revenue

Eight lines, each computed from a driver rather than assumed as a percentage.

| Line | Calculation |
|---|---|
| **Inference compute** (5010) | `total matches × €/match`. The rate is €0.420 through Oct 2025 and €0.231 from Nov 2025 — the model swap. From Jan 2026 the cost is drawn against the prepaid commitment at 71% utilisation, with the residual going to accounts payable. |
| **Storage & egress** (5020) | Storage = `matches in the trailing 12 months × 0.30 GB × €0.021 per GB-month`. Older video tiers to archive and leaves the hot window. Egress = `matches × €0.035`. |
| **Baseline hosting** (5030) | Fixed platform floor of €6,500 per month, plus €0.55 per club per court. |
| **Camera depreciation** (5040) | `deployed units × €340 ÷ 36 months`, starting the month of installation, not the month of purchase. |
| **Installation & field service** (5045) | `newly installed courts × €145`. |
| **Payment processing** (5050) | 2.9% of consumer card billings plus 0.8% of club invoice billings. Consumer-heavy revenue mix makes this line larger than a pure B2B company would carry. |
| **Support allocation** (5060) | 35% of Customer Success salaries. The other 65% sits in S&M. This split is a judgment call, not a fact — it is one of the three contested allocations flagged in the chart of accounts. |
| **Club revenue share** (5080) | 5% of court subscription revenue for the 18% of clubs that came through partners. |

**Gross margin** = `(revenue − total COGS) ÷ revenue`.

---

## Operating expenses

### Payroll

EU staff are employed through Deel. The monthly invoice is `base salary ÷ 12 + 31.2% employer burden + $89 per head platform fee`. US staff run through Gusto at `base ÷ 12 + 11.8% burden`.

Total people cost is then allocated to R&D, S&M and G&A in proportion to the salaries sitting in each cost centre, and the Customer Success portion that belongs in COGS is removed from S&M.

### R&D — 6xxx

ML research compute (training and evaluation runs, distinct from per-match inference), contractors, and engineering tooling. The research-versus-inference boundary is the second contested allocation: the vendor bill arrives as a single line and the split is a judgment.

### S&M — 7xxx

Paid acquisition runs at 76–96% of Player revenue — deliberately aggressive, which is what makes the consumer unit economics worth examining. App store fees at 11% of consumer billings, events and sponsorship, partner commissions at 6% of club billings, and travel scaled to sales headcount.

### G&A — 8xxx

EOR platform fees, legal, accounting and audit, insurance, coworking, software, and bank fees.

**Operating income** = `gross profit − total operating expense`.

---

## Cash

Cash is **derived from balance-sheet movements, not assumed**. Each month:

- Collect 94% of the Stripe in-transit balance and 72–86% of outstanding accounts receivable
- Pay 78–90% of accounts payable and 100% of accrued payroll
- Add interest at 3.1% annualised on the cash balance

The closing cash figure is simply the balance of GL account 1010. Days sales outstanding and days payable outstanding fall out of those collection and payment rates rather than being set.

**This is why cash burn runs below P&L burn.** Annual prepayments from clubs and annual player plans arrive as cash long before the revenue is recognised, so the business is partly funded by its own customers. That gap is real, it is a good story for the Controller agent, and it is the reason runway came in at 19 months rather than the ~15 the spec assumed.

---

## ARR — the four definitions

This is where the demo lives, so each one is spelled out precisely.

**1. Committed recurring ARR — $4,673,195 at Jul-26**

```
(courts in force × €89 × 12)
+ (monthly players × their actual price × 12)
+ (annual players × their actual annual price)
+ (coach seats × €39 × 12)
```
converted at the month's FX rate. Note "actual price," not list — the Black Friday cohort contributes at €71.40, not €119.

**2. ARR plus usage run-rate — $5,171,781**

Committed recurring plus `current month's overage revenue × 12`. Defensible because overage is genuinely recurring; problematic because it is seasonal, so annualising a July figure flatters the number.

**3. The sales view — $5,303,903**

Adds trailing twelve-month tournament revenue. Tournaments are one-off by nature, so this is the weakest of the four — and it is the number a VP Sales will quote.

**4. Constant currency — $4,368,403**

The same EUR base held at the opening rate of 1.052 rather than the current 1.118. Strips out the ~6% currency drift and shows what the business did on its own.

The spread from lowest to highest is **$935,500** — about 20% of the company. All four are defensible. Only one belongs in a board pack, and deciding which is exactly the semantic layer's job.

---

## Usage volumes

| Segment | Calculation |
|---|---|
| Clubs | `courts × 112 base matches × seasonality × random ±15%` |
| Players | `3.2 base matches × seasonality`, except the ~90 heavy accounts at 15–25 per month. The May–June 2026 surge cohort runs 1.52× while it is new. |
| Academy | `coach seats × 11 × seasonality` |
| Tournaments | fixed volumes per event |

Seasonality runs from 0.85 in December to 1.24 in July — padel is an outdoor-peak sport in Europe, and it shows up in usage, in overage revenue, and in inference cost simultaneously.

April 2025 is deliberately incomplete: only 42% of that month's logs were retained, with nothing in the data marking it as partial.

---

## What is deliberately unresolved

Six calculations above are conventions rather than truths, and each one moves a headline number:

1. Whether usage revenue belongs in ARR
2. Whether tournament revenue belongs in ARR
3. Whether ARR uses list price or actual price for discounted cohorts
4. Where the line sits between ML research compute (R&D) and inference (COGS)
5. What share of Customer Success is COGS versus S&M
6. Whether reported or constant-currency ARR is the headline

Day 5 turns each of these into a written, versioned rule with a rationale. Until then, every one of them is a place where two competent analysts would produce two different board packs from identical data.
