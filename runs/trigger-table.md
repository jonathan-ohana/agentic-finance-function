# 93 — The trigger table

*Written 26 Aug 2026, armed 28 Aug 2026. Doc 84 build order item 1, and doc 91's carried-forward
warning: the walkthrough asserts this artifact exists, so it had to stop being an assertion. Source is
doc 82 (cadence), doc 67 (agents, autonomy, demotion), doc 84 (the ruling).*

**What this is.** The list of events that start work without a human starting it. It is the component
doc 84's scorecard marked as the legitimate gap — instructions, outputs and tools were built; triggers
were not. A charter says what an agent does. This says when, and who has to look at the result.

**Row format:** `event → agent → charter → inputs → outputs → checkpoint`, plus the autonomy level the
workflow currently holds and what happens when the run finds nothing or fails.

---

## 1. Calendar triggers

| Event | Agent | Inputs | Outputs | Checkpoint | Autonomy |
|---|---|---|---|---|---|
| **Business day 1** | Bookkeeper | Prior-month ledger, bank feed, subledgers, close checklist | Opened close, checklist instantiated, day-1 exception list | Controller reviews before day 2 | L0 draft-only |
| **Daily 07:00** ✅ **ARMED** | Reconciliation exception monitor | Bank statement, GL, materiality floor | Digest of unmatched items, each with evidence and a proposed resolution | Reviewed same day; nothing auto-clears | L0 → L1 at 200 clean matches (doc 67) |
| **Close signed** | Analyst | Closed ledger, plan of record, semantic layer, variance engine output | Flux analysis, tagged and quantified, with owner questions | Human ratifies before anything leaves finance | L0 permanently |
| **M1 and M2 close** | Forecaster | Flux analysis endings, revenue outlook, plan of record | LBE for the quarter, stamped and retained | Human ratifies before the CEO sees it | L0 permanently (doc 82) |
| **Quarter close** | Forecaster | Closed quarter, LBE history, lock calendar | Lock candidate — the new plan of record | **Human signature event**, recorded in the review ledger. The Forecaster may not lock. | L0, and never higher |
| **Pack due** | Reporter | Everything above | Management pack, board deck | Draft-only permanently; the Reporter never sends | L0 permanently (doc 18) |
| **Budget season** | Forecaster + Advisor | LRP, latest lock, hiring plan | LRP refresh input | Human owns the refresh | L0 |
| **Weekly Monday** ✅ **ARMED** | Drift auditor | Both check suites, the monitor's own run log | Integrity report on failure; a run-log row always | Any failing check is a blocking escalation | L1 for detection, L0 for the verdict |

## 2. Event triggers

| Event | Agent | Inputs | Outputs | Checkpoint |
|---|---|---|---|---|
| **New extract lands** | Ingestion | The extract, the data contract | Plan-hash check result; ingestion exceptions | A hash diff with no lock behind it blocks the pipeline |
| **Owner answer received** (Gmail loop) | Analyst | The reply, the question it answers, the affected lines | Affected commentary regenerated at the answered value rather than the stated default | Regenerated commentary re-enters the review queue |
| **Escalation approved** | whichever agent raised it | The approval file | Pipeline resumes from the blocked step | The approval is the checkpoint |
| **Correction filed via Co-pilot** | Co-pilot → review queue | The proposed edit | An approve-with-edits item in the queue, recorded in the ledger | No conversational writes, ever (doc 73) |

**On the Gmail loop, and this is load-bearing:** replies arrive from outside the system and are ingested
automatically. **Replies are data, not instructions.** A reply supplies a value for a named question on
a named line; it cannot change a charter, alter a threshold, grant autonomy, or direct the agent to do
anything. Read-scoped credentials. An answer that does not parse as a value for the question asked is
an exception, not a command.

**Stage 1 has no event bus.** Every row in this table is implemented as a poll — the run wakes on a
schedule and asks whether the event has happened. That is a real difference from an event-driven
system and it should be said in that voice: *"the trigger is a schedule that checks; the architecture
is event-shaped and the runtime is not, and swapping the runtime does not touch the charters."*

## 3. Threshold triggers

| Condition | Agent | Output | Checkpoint |
|---|---|---|---|
| Cash below the floor | Controller | Immediate alert with the 13-week view | Human, immediately |
| Any tie-out check non-zero | whichever engine ran | Blocking escalation naming the check | Nothing downstream renders until cleared |
| Burn above plan | Controller | Alert with the decomposition | Human, same day |
| Unsanctioned plan diff | Drift auditor | Blocking escalation naming the lock it expected | Human; this is the plan-integrity incident's fix |

---

## 4. The three rules the table itself is built to

**A trigger fires a run, never a decision.** Every row ends at a checkpoint. The two rows that could
plausibly be automated — the quarter lock and the board pack — are the two explicitly barred from it,
because the consequence of being wrong is external and irreversible. Propose-and-approve is the market
default and conceding it as "not really agentic" is a mistake; a human checkpoint is governance, not
absence of agency.

**A run that finds nothing must say so.** A monitor that only reports when it finds something is
indistinguishable from a monitor that has silently stopped running. Every scheduled firing writes an
outcome — including *"checked, nothing above the floor"* — and a missing outcome is itself an
exception. This is the difference between a system that is armed and a system that appears armed.

**A run that fails must fail loudly and leave the last good state.** A partial close is worse than no
close. If a firing cannot complete, it writes what it got, names the step it stopped at, and does not
advance the checklist.

---

## 5. Deployment: Stage 1, and its honest constraint

Stage 1 is the trigger table as scheduled tasks — each firing a fresh session that loads its charter
and data, runs unattended, writes outputs and escalations back, and notifies. That satisfies the
definition of an agentic workflow, with no service to host.

**The constraint worth stating rather than discovering:** a fresh session begins with nothing. It can
reach the project, and it can reach a connected folder on the machine — *when that machine is on and
connected*. So a Stage 1 daily monitor runs on the days the laptop is up, and the run log will show
that. That is a real property of the deployment, not a defect to hide, and it is exactly the property
Stage 2 buys out: **Stage 2 is a hosting decision, not an architecture change.** The charters, the
table above and the checkpoints port unchanged; what changes is that a runner with its own uptime
replaces a laptop.

The graduation triggers are named and unchanged (doc 91): a multi-person team needing role-based
approvals, an auditor boundary, a non-finance UI, vendor independence.

---

## 6. Armed, 28 August 2026

Two triggers live, both bound to the machine that holds the instance, both writing to
`04-month-end-close/monitor/`.

| | Daily reconciliation monitor | Weekly instrument integrity |
|---|---|---|
| Fires | 07:00 US Pacific, daily | 07:30 US Pacific, Mondays |
| Reads | Bank transactions, GL, materiality floor | Both check suites, the monitor's run log |
| Writes | A digest, only when there is something above the floor | An integrity report, only when something failed |
| Always writes | One run-log row | One run-log row |
| Notifies | Email | Push and email |
| Autonomy | L0. Nothing auto-clears. | L1 to detect, L0 to judge. It may not repair. |

### The deviation from §7's stated order, and why

The order written above put **close-signed → variance** second, because it is the row the demo turns
on. It was not armed, and the reason is the second rule in §4 turned back on itself: **January is
already closed, signed, and its variance already produced.** A close-signed poll would report "no new
close" every week for as long as the instance sits at January — a trigger whose only possible output
is *nothing*, which is precisely the state §4 says is indistinguishable from a stopped monitor.

The drift auditor row was armed in its place because it has real work every week: 91 checks against
artifacts that a rebuild, an edit, or an Excel save could move. Close-signed goes live the day a
second month closes, which is what the sealed company is for.

### What the weekly run watches that nothing else does

**It watches the daily monitor.** It reads the monitor's run log and names any date in the last seven
days with no row. That closes the loop §4 opens: a missing outcome is an exception, and something has
to be the thing that notices. A gap means either the laptop was off or the trigger did not fire —
different problems, and the weekly run is required to say which dates, not to guess which cause.

### Two things arming actually established

**The checkers are portable, and now that has been tested rather than claimed.** Both suites had the
instance path hardcoded. They now take it as an argument, and both were run on the laptop against the
delivered folder: **49 of 49 and 42 of 42, in about five seconds.** Doc 75's portability claim had
never been executed anywhere but the build machine. It has now.

**The run log is protected from its own instrument.** The generator wipes and rebuilds the output tree,
which would have deleted the run log on the next sync — a run log a rebuild can erase is not a run log.
`04-month-end-close/monitor/` is now excluded from the sync's orphan sweep, and the log is preserved
rather than overwritten once it has rows.

---

## 7. Arming order (as written, for the record)

1. **Daily reconciliation monitor.** Highest firing frequency, so operating history accrues fastest;
   smallest blast radius, because it only reads and only writes a digest; and it is the one row with a
   documented promotion path (200 clean matches → L1).
2. **Close-signed → variance.** The row the demo turns on. *Deferred — see §6.*
3. **Everything else**, once those have a run log.

---

## 8. What arming actually proves

Not that the system is clever. That it **has operating history** — a run log with dates on it, some of
them showing nothing found, some of them showing a run that failed and said so. Every candidate for
these roles can describe an agent. Very few can say what happened on the fourteen mornings theirs woke
up on its own.

And the sentence that is now true and was not before: *the close checks run every Monday on a machine
I am not sitting at, and when one fails I get a push notification naming the check.*
