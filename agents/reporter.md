# 18 — The Reporter: charter, standard board deck, and CEO briefing

*Written 17 Aug 2026. Closes a gap in doc 03, where the Reporter's deliverable was named ("board pack") but never specified. Input to Fable session #3 on Day 6, and the build target for Day 8.*

---

## Why this needed writing

Doc 03 gave the Reporter one line: *"assembles the monthly investor update and quarterly board pack from the other agents' outputs, drafts commentary in the company's voice, maintains an always-current data room."*

Three things were missing, and each one matters:

**No output artefact.** "Board pack" could mean a memo. Nobody presents a memo to a board. The deliverable is a slide deck, and it has to be named as one.

**No standard structure.** The point of a repeatable board process is that the deck looks the same every month, so the board learns where to look and the meeting argues about the business rather than the format. Without a fixed slide set the agent improvises — which reintroduces exactly the instability the field input identified as the core anxiety: *"reporting different numbers to investors each time without a clear explanation."*

**Nothing about preparing the CEO.** This is the real job. Getting a CEO ready for a board meeting is not producing slides; it is producing slides *plus* a briefing — what changed, what they will be asked, what they should not promise, and the backup detail behind each likely challenge. A good finance lead does this. A bad one hands over a deck.

---

## Revised charter

**The Reporter (board, investor and CEO readiness).**

*Inputs:* the closed trial balance and statements from the Bookkeeper; the variance analysis and metric outputs from the Analyst; the rolling forecast and scenarios from the Forecaster; the cash view and 13-week forecast from the Controller; the semantic layer; the decision log.

*Outputs, monthly:*
1. **Board deck** (`.pptx`) — fixed ten-slide structure, below
2. **CEO briefing note** (1–2 pages) — not for the board
3. **Investor update** (email/memo, monthly) — narrative version for the cap table
4. **Data room refresh** — statements, metric definitions, cap table, contracts index

*Cadence:* deck and briefing five business days after close; investor update the same day; data room continuous.

*Autonomy:* **draft-only, permanently.** External communication is a hard human line under the governance model. The Reporter never sends; it prepares.

*Escalation:* any metric whose definition changed version since the last deck; any figure the Analyst flagged as low-confidence; any variance above threshold with no attributed driver.

---

## The standard board deck

Ten slides, same every month. The board learns the shape; deviations become signal.

| # | Slide | Contents | Source |
|---|---|---|---|
| 1 | **TL;DR** | Three to five bullets, the month in the CEO's voice. What happened, what it means, what's being asked | Reporter, from all agents |
| 2 | **KPI dashboard** | ARR, NRR, gross margin, net burn, runway, headcount — each with prior month, plan, and direction | Analyst |
| 3 | **Revenue** | By stream, plus the movement walk: opening, new, expansion, contraction, churn, closing. Subscription and usage split | Analyst |
| 4 | **Unit economics** | CAC, payback, LTV:CAC, gross margin by segment. Benchmarks differ by motion — self-serve and sales-led are not compared on the same line | Analyst |
| 5 | **P&L vs plan** | Variance with driver attribution, and an explicit statement of *which* plan | Analyst |
| 6 | **Cash and runway** | 13-week detail, 12-month view, scenario range | Controller |
| 7 | **Forecast** | Current reforecast against the previous one — what changed and why | Forecaster |
| 8 | **Hiring plan vs actual** | By function, with start-date drift called out. People are 60–70% of cost | Analyst |
| 9 | **Decisions and asks** | What the board is being asked to approve, each with the analysis behind it | Reporter, from the decision log |
| 10 | **Appendix: definitions and lineage** | Every metric on slides 2–8 with its registry ID, definition, version number, and what changed since last month | Semantic layer |

### Slide 10 is the differentiating one

A board deck that carries its own versioned metric definitions is the direct, physical answer to *"the numbers are different every time and nobody can explain why."* When ARR moves because the definition changed rather than because the business changed, the deck says so, on the page, with a version number.

Effectively no startup board deck does this. It costs one slide, and it is the single most visible expression of the whole thesis: **the semantic layer is not internal plumbing, it is a board-facing artefact.**

### Formatting rules

Every number on every slide carries its registry ID in the speaker notes. Any figure that is an assumption rather than an actual is labelled as one on the slide, not in a footnote. Forecast ranges are shown as ranges. No metric appears without a prior-period comparison. If a definition changed, the affected slide gets a marker and slide 10 explains it.

---

## The CEO briefing note

One to two pages, produced with the deck, **for the CEO only**. Five sections:

1. **What changed** — the three things materially different from last month, in plain language
2. **The three questions you will be asked** — with the answer, and the number behind it
3. **What not to commit to** — where the data is soft, where a forecast is one customer away from being wrong, what would be dangerous to promise in the room
4. **Backup** — the detail behind each likely challenge, so the CEO can go one level deeper without turning to finance
5. **Where I could be wrong** — the Reporter's own uncertainty, stated. Which figures rest on unresolved definitions, which on estimates, which on incomplete data

Section 5 is the governance layer showing up in the deliverable. An agent that states where it might be wrong is the opposite of the failure mode a skeptical CFO expects.

---

## What this means for the sprint

**Day 6 (Fable #3, charters).** The Reporter charter above is an input, not an output — Fable's job is to attack the autonomy boundary and the escalation rules, not to redesign the deck.

**Day 8.** The Reporter builds a real `.pptx` for July 2026 using the pptx skill, from the other agents' outputs, plus the briefing note. Not a mockup — the actual artefact a CEO would carry into a board meeting.

**Day 9.** The failure demo becomes sharper with a deck in play: the wrong margin narrative from the Nov-25 model swap would have gone onto slide 5 and into the CEO's mouth. The governance checkpoint catching it *before* the deck is assembled is a far more legible save than catching it in a spreadsheet.

**Day 10.** The deck is the single best artefact for demonstrating the system. A reader can evaluate a board deck in ninety seconds; they cannot evaluate a data pipeline.

---

## Open question for Day 6

Whether the Reporter should also produce the **quarterly** board pack as a distinct, longer artefact, or whether the monthly deck plus a quarterly appendix is sufficient at this stage. Doc 03 assumed monthly investor updates and quarterly board packs; the field input suggests monthly board contact is the reality at Series A. Leaning towards one monthly deck with a quarterly deep-dive appendix, which avoids maintaining two formats.
