# The workflow lifecycle: explore, operate, compile

*Written 9 Sep 2026, after this repository was published. It is doctrine informed by field
research — operating the system described here, and conversations with practitioners running
finance work at volumes I have not run. The lifecycle below has not been run end to end. What
was demonstrated is linked; everything else is stated as a position, and should be read as one.*

---

## The question

The sharpest argument against an agentic finance function does not come from people who think
the models are weak. It comes from people who build deterministic workflow platforms, and it is
a good argument:

- A coded workflow executes identically on run one and on run one million.
- It emits a log. When it fails, the failure is visible, located, and reproducible.
- It leaves proof, rather than asking for trust.

An agent decides at runtime. Two runs over the same inputs can differ, and the difference is not
always visible in the output. Everything this repository builds — definitions, contracts, checks,
a review ledger — is machinery for containing a property a coded pipeline does not have.

One practitioner put both halves of the argument to me at once: they run 200+ client books on an
AI harness, and separately built a deterministic workflow platform because the harness alone
would not hold at that volume. Their critique sharpened this page and one of its rules.

If the critique is right, an agentic finance function is a mistake — an expensive, drifting
substitute for code that somebody should have written. I do not think it is a mistake. I think
it is a phase, and the critique and this repository are both right about different ones.

## Workflows have a lifecycle

**A workflow is born agentic.** Not because agents are better, but because on day one nobody
knows what the rules are. Agents are cheap to create, tolerate messy inputs, and handle the case
nobody anticipated — and the first closes are almost entirely cases nobody anticipated. You
cannot write the deterministic spec at the start, because writing it requires the knowledge the
first runs produce. A platform that demands the spec up front demands the output of the phase it
would replace.

**It operates agentically under governance.** Contracts, definitions, human review, and the
correction loop hold it while the rulings accumulate. This is the phase this repository is in.

**It is compiled when the corrections converge.** When several consecutive runs produce no new
rulings, the workflow has stopped discovering and has revealed its own stable structure. That is
the point to write it down as code: a deterministic pipeline for the mechanics, with the model
retained only at the nodes where judgment is required.

| Phase | What it is | What holds it | Exit condition |
|---|---|---|---|
| **Explore** | Discovering what the workflow actually is | Draft-only autonomy, everything reviewed | The workflow runs the same way twice |
| **Operate** | Running it under governance while rulings accumulate | Definitions, contracts, review ledger, correction routing | Corrections converge — consecutive runs, no new rulings |
| **Compile** | Deterministic code for the pipeline, model at the judgment nodes | Execution logs, the same definitions, the same approvals | None. A material change to an input system sends it back to Explore |

The last cell keeps this honest. New pricing, a new billing system, a new entity — the events that
demote a workflow down the [autonomy ladder](../correction-loop/self-improvement-loop.md) also
decompile it, because the spec was true about data that no longer exists.

## The correction ledger is the promotion gate

This repository built the correction loop as a learning mechanism: a human correction becomes a
versioned rule, and a later run applies the rule and cites it by ID. That is the demonstration in
[loop verification](../correction-loop/loop-verification.md).

The ledger has a second role I did not see when I built it. It is the instrument that tells you,
empirically, when a workflow has earned compilation. A deterministic platform requires that a
human already know the spec before anything runs. A governed agentic phase *discovers* the spec —
each correction routed to a destination, each ruling written down with the case that forced it —
and the rulebook that comes out the other end is the compilation input. The ledger going quiet is
not the absence of a signal. It is the signal.

## What never compiles

The test is two controllers. Give the same data, definitions, and question to two competent
controllers. If they would produce the same answer, the output is mechanical and the task is on
the conveyor toward code; the only question is when. If they could legitimately produce different
answers and both defend them, the output is judgment, and it stays probabilistic and
human-governed permanently — not until the technology improves.

Judgment, by this test: the causal story behind a variance, the interpretation of an anomaly,
definitional rulings, and the adjudication of an exception — whether this one is material, this
month, to this reader.

Variance analysis splits exactly along that line, which is why it is the useful example. The
arithmetic and the ledger attribution compile: actual minus plan, by account, by entity, ranked.
The causal story never does, because the *why* is not in the ledger — it is in the pipeline
review, the hiring decision, and the contract nobody has read. Compiling the first half is what
buys attention for the second.

## Silence is a failure state

A practitioner's critique of this design, which I adopt in full: a scheduled agentic workflow
whose failure is silent is ungoverned, no matter how good its outputs are when it works. A run
that did not happen and a run that happened cleanly produce identical evidence, which is none.
This is the DORMANT/DISCONNECTED distinction from
[finance observability](../correction-loop/observability.md), applied to the agent rather than
to the check.

The rule: **any workflow granted scheduled autonomy must emit a run status — that it ran, when,
what failed, and who approved the output — and silence is itself a failure state that triggers
demotion**, on the same one-strike basis as a missed material error. It joins the demotion
triggers in the [autonomy ladder](../correction-loop/self-improvement-loop.md) and the earned-autonomy
phase of the [install runbook](../install/runbook.md).

Honestly, this requirement favours the compile step. A coded workflow gets execution logging
nearly free — it is a property of the runtime. An agent has to be instrumented deliberately, and
the instrumentation is a thing that can itself stop running. That asymmetry is a real cost of
staying agentic, and it belongs on the same page as the argument for it.

## What this changes about the thesis

The thesis was *buy the ledger, build the judgment layer*. It gains a third clause: **compile
workflows as they stabilize.**

The durable asset is unchanged, which is why the third clause costs nothing. Definitions, rulings,
contracts, and the correction log are execution-substrate-agnostic: they govern an agent today and
a compiled workflow tomorrow, and they survive a platform change either way. Nothing in this
repository's semantic layer knows what executes the run.

So the market layers rather than competes. Ledger platforms own the books. Deterministic platforms
own the execution rail for stabilized workflows. The judgment layer — and the migration path
between exploration and compilation — belongs to the finance function itself, because it is the
only party that can rule on what a number means.

## The limit

What was demonstrated here is one correction, one rule, and one later run that cited it. The
lifecycle above was not run through to compilation: no workflow in this repository has reached
convergence, been compiled, and then been operated as code under the same governance. The
convergence threshold — how many consecutive quiet runs earn compilation — is an untested design
parameter.

This page is the design that operating experience and field conversations point to. It is not a
result and should not be cited as one.
