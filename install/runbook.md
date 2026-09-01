# 85 — The install runbook: implementing the workflow at a new company

*Ruled 23 Aug 2026. The first-finance-hire deployment plan, ~90 days. Sources: docs 22 (package), 65 (onboarding), 81 (day-one protocol), 82/83 (planning ladder), 84 (triggers). PACKAGE artifact.*

## Phase 0 — before day one (negotiated at the offer, maximum leverage)

- **Read-only credentials as standing policy:** "AI connections get read-only roles — worst case is a bad query, never a bad journal entry."
- **Finance-in-the-flow rule agreed with the CEO:** contracts not signed until filed; vendors not paid until the SOW is in the repository. (Red-team enforcement risk neutralized by making it a hiring condition, not a month-two imposition.)
- Company Claude workspace, Team/Enterprise plan (plan hygiene), one project per company, plugin installed.

## Phase 1 — week 1: map and preflight

Inventory systems; export everything as-is; run preflight. The verdict is CEO deliverable #1: data state sorted into mapping / export / system / process gaps. Honest gate: no agent runs on unpassed data.

## Phase 2 — weeks 2–3: foundation (mostly meetings)

Map exports into the data contract. **Semantic-layer workshop with the CEO** — every DECIDE flag answered (ARR definition and who may use the word, comparator, contested allocations, usage treatment). Owner→CC mapping dictated. Lexicon confirmed in the team's vocabulary. Document repository live under the Phase-0 policy.

## Phase 3 — month 1: first supervised close (day-one protocol, doc 81)

All agents L0 draft-only; 100% review; exemplar store fills from accepted wording only; promotion clocks at zero; review ledger from run one. The escalations ARE the findings report ("my first close surfaced N issues"). Red-line cycle on the first variance pack = the calibration deferred from synthetic data; converges in 2–3 closes.

## Phase 4 — month 2: cadence and triggers

Finance calendar → scheduled tasks (close, daily rec monitor, drift auditor). First LBE after M1 close. Owner-question protocol introduced at a team meeting BEFORE the first email: one-minute closed-form questions, stated defaults, silence = default applies. Board pack v1 with the checks page.

## Phase 5 — month 3+: earned autonomy and the planning ladder

Promotions strictly on doc-19 evidence (ledger has data since day one). Budget season → LRP anchors the annual plan (doc 83). The 90-day report writes itself from instrumentation: close time before/after, checks live, escalation stats, new visibility.

## The three don'ts

1. No tool rip-outs in Q1 — the package sits ON the existing stack (extracts/MCP); that is the data contract's whole point.
2. Never promise "no finance hires" — promise "no hires before the evidence says so."
3. No agent touches anything before preflight passes and the semantic layer is signed. Deployments fail on data foundations.

---

## Amendment (23 Aug) — three corrections from Jonathan's review

**1. Finance-in-the-flow, realistic version (replaces the Phase-0 absolute).** Signatures cannot be gated at a startup (invoices precede SOWs; sales signs first; a new hire has no authority to police it). Enforce at the choke points finance controls: **nothing paid without its document** (chase before the payment run, never refuse business) and **nothing billed without its contract** (billing setup requires the paper). Everything else is DETECTION: close flags journals without document references; monthly completeness check surfaces gaps. Intake must be frictionless: contracts@/ap@ aliases auto-ingest into the repository — forwarding an email is realistic; forms are not. CEO ask, final form: "finance pays nothing and bills nothing without the paper; the rest gets caught at close."

**2. Installer access mechanics (all read-only).** One shared "Finance install intake" folder receives the system exports per the mapping worksheet. Access via: Google Drive connector (company Drive) · local folder bridge (Claude desktop "Add folder") · MCP connectors where systems have them (no export needed) · Gmail connector for the invoice inbox. Scope to finance folders only, never the whole Drive. Preflight reads and writes nothing — that sentence is the security answer.

**3. What "supervised" means (kills the manual-first-3-months misreading).** Agents do ALL production from week one; L0 means the human approves output before it counts, not that the human produces it. Timeline: week 1 installer/preflight (agent-run) · weeks 2–3 the human phase — meetings and rulings (the judgment work that IS the job) · week 3–4 first agent-run close, human reviews the finished draft · months 2–3+ autonomy phases in per the doc-19 ladder. The workflow is implemented at the first agent-run close (~week 3). What is earned over months is how little of it you must look at. The judgment layer — decisions, reviews, owner conversations — is never delegated at any stage.

## Amendment 2 (23 Aug) — deployment = ownership, and the graduation triggers

**Mental model:** deployment stopped meaning "our servers" decades ago (payroll runs in Gusto's cloud; the books in QuickBooks'). Deployed-at-the-company = the company's instance of a vendor-hosted service: their account, their data boundary, their users. The Cowork desktop app is a window; the host is Anthropic's cloud — scheduled tasks run with every laptop closed.

**The ownership rule (added to Phase 0):** build in the COMPANY's Claude workspace, never a personal account. Company org and billing; connectors authed with company accounts; project and plugin org-owned; a second person addable to the review role. This is the bus-factor test every CEO applies — org-owned passes it; personal-account-hosted fails it and deserves the "not deployed" critique.

**Graduation triggers (when Cowork-hosting stops being correctly sized → stage 2 / Agent SDK service):** a multi-person finance team needing role-based approvals · auditors requiring a controlled system boundary (typically Series B/C) · non-finance users needing a real UI beyond artifacts · vendor-independence requirements. None holds at Seed–A with finance-of-one. On migration, charters / semantic layer / data contract / ledger port unchanged — the artifacts are the system; the host was always swappable.
