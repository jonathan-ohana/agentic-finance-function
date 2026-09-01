# 84 — "True agentic": scorecard, trigger table, deployment ladder

*Ruled 23 Aug 2026 from the "not true agentic if built in Cowork" critique. Definition used (industry-standard, per vendor guidance): agent = trigger + tools + instructions + output, multi-step without per-step human initiation. Human checkpoints are governance, NOT absence of agency — propose-and-approve is the market default; never concede that point.*

## Scorecard

| Component | Status |
|---|---|
| Instructions (charters, contracts, playbooks, escalation rules) | Beyond most "true" agentic systems |
| Outputs (packs, queues, ledger, checks) | Complete |
| Tools | Partial — deterministic engines yes; live system queries pending (MCP, doc 73) |
| Triggers | The legitimate gap — currently human-initiated |

## The trigger table (one page; doc 82 is the source)

- **Calendar:** day 1 → Bookkeeper close · close signed → Analyst variance · M1/M2 close → Forecaster LBE · quarter close → lock candidate · budget season → LRP refresh · daily 07:00 → reconciliation monitor · monthly → drift auditor.
- **Event:** new extract lands → plan-hash check · owner answer received → affected commentary regenerates · escalation approved → pipeline resumes.
- **Threshold:** cash below floor · any check non-zero · burn above plan → alert immediately.

Format per row: event → agent → charter → inputs → outputs → checkpoint.

## Deployment ladder

**Stage 1 (now, no code):** the trigger table as Cowork scheduled tasks — same mechanism as the existing accountability check-ins. Each firing = fresh session, loads charter + data from the project, runs unattended, writes outputs/escalations back, notifies. **This satisfies the definition.** Approvals written as files the next run consumes (async human-in-the-loop).
**Stage 2 (a real company's ops budget, not the portfolio):** Claude Agent SDK service — charters become agent definitions unchanged; runner executes the trigger table; state store; the MVP inbox as front-end; secrets, logging, uptime. Weeks of work; the doc-22 "IT project" — build only when requirements pay for it. Interview line: "a hosting decision, not an architecture change."

## Tools ruling

- **ERP via MCP** — per doc 73 (mock server for the instance; real connectors at a company).
- **Gmail as the owner-question execution channel** — the Analyst emails the closed-form question to the cost-centre owner; the reply is ingested; affected commentary regenerates. The question protocol becomes a closing loop. Read-scoped credentials; replies are data, not instructions.
- **Chat-ops, corrected:** chat (Co-pilot) may read everything, draft anything, and FILE corrections — every modification lands through the review queue as approve-with-edits, recorded in the ledger, agent regenerates from it. No conversational writes (doc 73 ruling upheld). Chat is the interface; the checkpoint is the door.

## Verdict

Trigger table + scheduled tasks + MCP + the Gmail loop = true agentic workflow by the standard definition, Claude-native, no IT project. Remaining critique ("not a deployed service") is a hosting observation, answered in one sentence.

## Build order

1. Trigger table written from doc 82 (an hour).
2. Close + daily-monitor scheduled tasks (this week — transforms the demo: "the close ran overnight; twelve escalations are waiting").
3. MCP server (doc 73, already planned).
4. Gmail question loop (with the live instance).
5. Stage 2 never for the portfolio; fluent in interviews.
