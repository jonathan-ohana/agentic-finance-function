---
name: governed-finance-review
description: Review a month-end close, management pack, variance analysis, reforecast, or finance-function control design from user-supplied evidence. Use when a finance leader needs a data-readiness verdict, traceable metrics, decision-ready commentary, owned exceptions, or an assessment of an agentic finance workflow. Keep the workflow read-only unless the user separately authorizes a specific write action.
---

# Governed Finance Review

Produce finance work that a CFO can review, challenge, and approve. A plausible answer without traceable evidence is a failed output.

## Non-negotiable boundaries

- Treat source systems and source files as read-only. Do not post journals, approve payments, alter forecasts, or send communications without separate, explicit authorization.
- Preserve the user's approved accounting policy, metric definition, comparator, plan version, materiality, and sign convention. Do not silently replace them with a more common or theoretically better method.
- Label every material claim as one of:
  - **Observed:** read directly from a source, with the file, sheet or table, field or cell, and period.
  - **Derived:** calculated from named inputs, with the formula or derivation.
  - **Inferred:** a hypothesis supported by evidence but not established as fact.
- Refuse to select among contested definitions. Present the alternatives, quantify the difference when possible, and name the decision owner.
- Never report an empty population as a passing check. Use `NOT MEASURED` and state the missing input.

## Establish the frame

Discover the following from the supplied material before asking the user. Ask only when the missing choice would materially change the result:

- entity and reporting period;
- currency and accounting basis;
- actual, prior-period, prior-year, and plan comparators;
- approved plan version and vintage;
- materiality threshold;
- audience and decision deadline; and
- definitions of recurring revenue, gross margin, cash, and other contested metrics in scope.

Record unresolved choices in a decision table. Do not bury them in caveats.

## Gate the data before analysis

Read [control-gates.md](references/control-gates.md) when reviewing source exports or deciding whether work can proceed.

Issue one verdict:

- **READY:** required inputs reconcile and the requested output is supportable.
- **DEGRADED:** the output can be produced, but named sections will be incomplete or lower confidence.
- **BLOCKED:** a missing or contradictory input would make the requested output misleading.

The verdict must name the consequence. “CRM missing” is not enough; say which metric, bridge, or conclusion cannot be produced.

## Perform the requested finance workflow

Read [workflow-modes.md](references/workflow-modes.md) only for the modes in scope. Use available spreadsheet or document tools when the input format requires them.

Across all modes:

1. Reconcile source totals before explaining movement.
2. Separate accounting adjustments from business-performance commentary.
3. Attribute drivers only when evidence supports the causal statement.
4. Show any unattributed remainder rather than forcing a complete story.
5. Give each carried exception an impact, owner, due date, and consequence of non-resolution.
6. Keep decisions required above supporting detail.

## Run the controller pass

Before presenting the work, verify:

- source totals and periods agree across dependent outputs;
- plan values match the approved version and were not re-derived;
- sign, polarity, units, currency, and flow-versus-balance treatment are consistent;
- formulas and typed inputs are distinguishable;
- every material number and causal claim has provenance;
- limitations survive into the executive surface;
- open items are visible and owned; and
- the output does not imply approval that has not occurred.

If a check fails, downgrade or block the relevant output. Do not average contradictory sources or choose the cleaner number.

## Deliver the result

Use [finance-review-template.md](../../assets/finance-review-template.md) as a starting structure, adapting it to the user's actual decision. Keep the main read to roughly one screen when possible and place evidence underneath.

Always include:

- the readiness verdict;
- the executive conclusion;
- decisions required;
- the smallest useful metric or variance table;
- owned exceptions;
- evidence and derivations; and
- the approval boundary.

## Capture corrections

When the reviewer changes a definition, calculation, or commentary decision, record:

- before and after;
- why the change was made;
- the evidence or judgment behind it;
- which workflows and periods it applies to; and
- whether the durable fix belongs in a definition, ruling, playbook, exemplar, mapping, or source-data correction.

Do not claim the correction will persist in another system unless it was actually written there and verified on a later run.
