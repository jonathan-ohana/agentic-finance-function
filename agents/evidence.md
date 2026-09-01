# 24 — The Evidence agent: for every number, where is the paper?

*18 Aug 2026. The ninth agent, and the one that answers the question a finance person actually asks forty times a month.*

---

## The question

> *"I can see revenue for customer X. Where's the contract?"*

That is not schema validation. The pre-flight asks whether a file is well formed. This asks something harder and more useful: **for every entity that appears in the financial record, does the evidence that authorises it exist — and can I find it, anywhere?**

A number without evidence is not wrong. It is *unsupported*, which is worse, because nobody can tell which numbers are which until someone asks.

## Why sources are plural

Evidence lives in a governed repository if you are lucky and in Slack, an inbox, a personal drive, or an unfinished e-signature envelope if you are normal. Scanning one folder answers the wrong question.

So the agent takes any number of sources: file trees, Slack exports, mailboxes, Drive, DocuSign, the CRM, Notion. The filesystem connector is implemented; the rest are specified in `evidence_map.json` with the note that matters most — *personal drives count, because that is where the unfiled version usually is.*

**Finding evidence in the wrong place is a different finding from not finding it**, and the register says which. That distinction is the entire value.

## Six verdicts

| Verdict | Meaning |
|---|---|
| **FILED** | In a governed repository. Nothing to do. |
| **FOUND_UNFILED** | Exists, but in Slack or an inbox. The information is there; the process is not. |
| **STALE** | Exists but predates a change. Contract says one thing, billing does another, no amendment found. |
| **CONTRADICTED** | Exists and disagrees with the ledger on a material term. |
| **INCOMPLETE** | Exists but is not binding — no countersignature, no date, a missing schedule. |
| **MISSING** | Nothing, in any connected source. |

`FOUND_UNFILED` is the one that changes behaviour. "You have no contract" gets argued with. "Your contract is in Diego's Slack DM from March, here is the message" does not.

## Twelve requirements

Written as finance rules, not technical checks. Each says what triggers it, what must exist, and *why it matters*, because a gap register nobody believes is a gap register nobody acts on.

Customers with revenue need a contract. Any change in quantity, price or term needs an amendment. Closed Won needs both a contract and a billing record. Vendors above materiality need an agreement. Everyone on payroll needs an offer letter. An end date or a one-off payroll charge needs a separation agreement. Manual journals above threshold need a supporting schedule. A billed price differing from a contracted price needs something authorising it. A non-standard cadence needs a clause.

**Exemptions are written down, not coded away.** Self-serve vendors — ad platforms, app stores, cloud marketplaces — have click-through terms rather than negotiated contracts. That is a judgement, so it lives in `evidence_map.json` where it can be argued with, and the register still reports the spend so nobody forgets it is uncontracted. In the CourtIQ run that is $2.9M of ad spend correctly exempted rather than silently ignored.

## What it found on CourtIQ

Run across 703 documents and three sources:

**INCOMPLETE — the federation contract.** $40,125 invoiced. The agreement is on file, in the right place, with all its non-standard terms. It has no countersignature date. *Obtain the client signature before the next invoice; escalate if the client is disputing.* The trap planted on Day 1 was found by reading the paper rather than the data.

**FOUND_UNFILED — seven Closed Won opportunities that were never billed.** Four of them resolve to a Slack message in `#deals`: *"verbal yes from Padel Arena Madrid, paperwork to follow, marking closed won so it lands this quarter."* That single line explains a pipeline conversion problem, a revenue gap and a forecasting distortion at once, and it was sitting in a channel nobody in finance reads.

**MISSING — $1.17M of activity with no usable evidence.** Three employees with no offer letter. Eleven vendors above the $25k threshold with no agreement, including two contractors at $90k and $71k.

**FILED, with an action anyway — the arrears-cadence contract.** The clause is documented, so no control gap; but the register still says *confirm treasury has modelled the cash timing, and add it to the deal-desk exception list.*

The closing summary is the line worth quoting:

> $1,174,579 of financial activity has no usable evidence. $33,108 has evidence sitting outside any governed repository — the information exists, the process does not.

## Why this is the strongest piece in the package

**Every line is actionable by a named person this week.** The design rule in `evidence_map.json` is explicit: *a gap register that says "improve document management" is a failure.*

**It measures the thesis.** Doc 03 claims finance should be *in the flow, not downstream of it*. The `FOUND_UNFILED` total is literally a measure of how downstream you are — evidence that exists but never reached finance. It turns a slogan into a number that can be tracked month over month.

**It needs an agent, not a script.** Matching *"Padel Zone Milano contract v3 FINAL.pdf"* in someone's Drive to `CLB-0088` is fuzzy work across unstructured text. The deterministic version here does the mechanical part; a Claude-native agent does it properly, and can read the document to check whether the terms match the ledger — which is what turns `FILED` into `CONTRADICTED`.

**It sells itself.** A CFO who runs this learns something uncomfortable about their own company in ten minutes, before adopting anything. That is a better opening than any deck.

## The three discovery agents, in order

The package now has three, and they answer different questions:

1. **Finance Organization Assessment** — how is the function set up? Systems, owners, process, where finance sits relative to the business. An interview.
2. **The Installer** — what data do you have, what does it mean, and what is it missing? A scan of files.
3. **Evidence** — for what you do have, where is the paper? A search across every source.

The Installer tells you a column is missing. Evidence tells you a *contract* is missing, and names the customer, the amount, and where to look first.

## Still to build

Verdicts `STALE` and `CONTRADICTED` are specified and only partly implemented — they need the agent to read a document and compare its terms to the ledger, which is Day 4's ingestion work. The upsell case is the natural first test: the contract says four courts, billing says ten, and the order form exists. If it were unfiled, that becomes `STALE`. If it said something different, `CONTRADICTED`.

Slack, email, Drive and e-signature connectors are specified with JSON fixtures standing in. Real connectors are a day of work each and belong after the sprint.
