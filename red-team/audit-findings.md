# 49 — Fable audit: the July 2026 reporting and forecasting pack

**Fable session output, 19 Aug 2026**, against `mgmt_reporting_pack_2026-07.xlsx` (20 tabs, 6,020 formulas) and the brief in doc 48. **Seat taken: incoming Head of Finance, nine days from the board.**

---

## 1. Diagnosis (disease ranking)

**Primary: sequence-within-the-page. Secondary: page-level voice.** Volume across tabs is **disproved** by the attention budget — every tab has a home.

The Exec Summary alone carries **44 competing elements across 87 rows**: 6 headline lines, a 14-row scorecard duplicating the KPI tab verbatim, 5 findings, 5 decisions, 14 live checks, and two charts anchored rows 79–86 — floating over the audit-trail text at B82:B85, with their caption (B87) underneath them.

**The bottom third of the front page proves trustworthiness before the reader is told what to trust it about.** Every sentence concludes; the page never does — no verdict exists.

Hierarchy machinery exists (CF chips on F21:F34) but is **un-ranked**: 13 of 14 scorecard rows carry a coloured chip, so colour no longer selects.

## 2. Verdict

**Not presentable as it stands.** Single reason: the page buries the emergency (book shrinking + raise clock) under its own audit trail. The model beneath **is** presentable. Nine days is enough — **the fix is one page, not the pack.**

## 3. Attention budget

- **2 min:** Exec Summary rows 1–35 as rebuilt (verdict, 6 headline lines, 6-row scorecard, 2 charts).
- **15 min:** rest of Exec Summary, KPI, SaaS Metrics, Forecast rows 1–41 + 135–164, Assumptions, P&L; Valuation when the raise is on the agenda.
- **Audit-only:** Cover, P&L Quarterly, Revenue, COGS, Opex, Balance Sheet, Cash Flow, Bridges, Lineage, Data_TB/Ops/Book/Plan.

**Volume disproved at pack level, confirmed at page level.**

## 4. Five changes, ranked by Monday impact

1. **Verdict sentence at new row 7** (14pt bold, only red on page): *"The recurring book shrank for a second month — churn removed $60,947 against $15,706 of new business; only $29,359 of FX held headline ARR flat. Burn accelerated to $582k. On the only forward view that exists (MID, unratified), cash runs out Apr-28 and every scenario exhausts cash inside 24 months. The decision this month is the raise timeline."* (Sources: SaaS Metrics N88/N47/N46, Exec C13, Forecast D19/B58.)
2. **Re-rank decisions** (B52 block): raise first with calendar arithmetic (cash-out Apr-28 → term sheet by Oct-27 → process in market ~Q2-27); then feed verification; VAT; sign the close; comparator ruling last.
3. **Suppress computed-through-defect CAC.** SaaS Metrics M70:N70 ($17,483.50 / $43,342.09) → `FEED DEFECT — SUPPRESSED (defect 23)`. **Ruling on the disclosure question:** disclose the gap on the face — yes; print arithmetic built on it — never; in a real company, verify the feed before the CEO sees the pack. **Feed artefacts are ops tickets, not board topics.**
4. **Burn multiple onto the front page** (new scorecard row after B31: *"n/a — net new ARR negative"*, BEHIND, note the month-24 model value 27.6×). **Rule of 40 off the front page** — F34 renders green ON TRACK while its own note predicts decay.
5. **Scorecard 14 → 6** (ARR, net new ARR [new row, `=SaaS Metrics N77`], burn multiple, churn, gross margin, cash+runway; the other 8 already live on KPI rows 5–18). **Charts to rows 18–32:** delete revenue/GP bars (finding 1's misleading headline as a picture); plot (a) Net new committed ARR 13-month bars (SaaS Metrics D87:F99), (b) Cash actual + MID forecast line to zero with an Apr-28 marker (Exec R10:S22 + Forecast C121:Z121).

## 5. Design rules broken

1. **Inverted header hierarchy** — section heads 9pt gray caps under 10.5pt body (B8, B18, B36, B52, B64); DECISIONS header smaller than its paragraphs. **Fix:** 16/11/9.5 scale; red reserved for verdict + BEHIND only.
2. **Signal saturation** — 13 of 14 scorecard rows coloured (6 green, 7 amber, 1 red); the lone BEHIND (F33) is camouflage. **Fix:** ON TRACK renders plain gray; fills only for WATCH/BEHIND.
3. **Orphaned numbers** — D16 ($488,588 burn mean rendered under the 2026-06 column of the runway row; move into the G16 sentence); N9:T22 raw chart-source block on the visible page (move below row 100, as KPI already does); chart-anchor collision over B82:B85. **Compliment:** the `+0.0"pp"` margin-delta format (E11, P&L O24) is exactly right.

## 6. Data: presentation vs dataset

**Presentation faults:** all of §5 — the "messy" feeling is **misfiled numbers and one drowned signal, not wrong numbers.**

**Dataset conviction faults:** (a) zero churn events in Club and Academy over 18 months / 239 logos — **plant 2–3 club churn events in the generator** (also unlocks LTV-Club and de-absurdifies HIGH's observed zero); (b) May surge → two exact-zero months is deliberate and disclosed, **leave**; (c) ARPA drifts too smoothly (Club 612→681 monotone) — optional noise.

## 7. Strategic gap

**The raise deadline as arithmetic.** The pack computes cash-out, buffer and capital requirement but never the **process-start date** (≈ Q2-27). One formula row on the Forecast headline block, echoed in decision 1; pays for itself by demoting the comparator ruling from the CEO list.

**Forward revenue indicators** (bookings, pipeline coverage) absent because CRM pipeline is not in the extract layer — **name it on Lineage as the next connector; do not estimate it.**

## 8. Lines not to cross

(a) **Which scenario is true** — unknowable from this data; the Assumptions written scenario definitions are the best-argued refusal in the file. (b) **The raise amount as "the ask"** — scenario output on placeholder multiples. (c) **NRR** — the row-62 proxy discipline must survive every edit. (d) **Business interpretation of the consumer zeros before feed verification** — LOW may model the trough; nothing may attribute it. **State the refusals once, in the caveat banner, not three times per page.**

---

## Summary for the nine days

> **Re-sequence one page, suppress two numbers, plant three churn events, add one date. The audit trail is the moat — it just has to stop standing in front of the message.**
