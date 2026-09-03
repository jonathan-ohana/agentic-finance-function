# Control gates

Apply only the gates relevant to the requested output. A missing optional source should degrade the dependent analysis, not block unrelated work.

## Source inventory

| Output | Normally required | Commonly useful |
|---|---|---|
| Close review | General ledger, chart of accounts, trial balance or control totals, reporting period | Bank, AP, AR, payroll, contracts, fixed assets |
| Variance analysis | Actuals, approved plan or comparator, account and department mappings | Operational drivers, owner map, contracts, CRM |
| Management reporting | Reconciled actuals, approved definitions, comparator, exception register | Billing, CRM, cash forecast, commentary evidence |
| Reforecast | Actuals through the cut-off, approved forecast basis, opening cash | Headcount plan, bookings, billing, collections and payment behavior |
| Recurring-revenue metrics | Billing or contract state, governed definition, effective dates | CRM, product usage, FX policy, cancellation and amendment history |

## Structural checks

- Required columns exist and have unambiguous meanings.
- Entity, currency, period, and basis are present or explicitly supplied.
- Row counts and date ranges are plausible for the stated population.
- Duplicate keys, broken joins, missing mappings, and orphaned records are quantified.
- Opening and closing balances reconcile where the output depends on them.
- Debits and credits are not declared tied when both populations are empty.

## Semantic checks

Raise a decision when any of these can change the answer materially:

- recurring revenue includes or excludes usage, services, credits, or contracted backlog;
- gross margin account scope is contested;
- cash includes funds in transit or restricted cash;
- plan versions or vintages compete;
- FX uses transaction, average, closing, or constant-currency rates;
- churn, expansion, contraction, or renewal dates lack an effective-date rule; or
- a flow metric is compared as if it were a period-end balance, or vice versa.

## Evidence checks

- Observed values carry a source locator.
- Derived values show their inputs and method.
- Inferences are written as hypotheses and include the evidence needed to confirm them.
- “No issue found” states the population and check performed.
- “Not computable” names the missing field, rule, or history.

## Verdict logic

Use **BLOCKED** when the missing input or unresolved contradiction could reverse a material conclusion, prevent reconciliation, or make the stated metric undefined.

Use **DEGRADED** when a useful output remains possible but a named section, slice, driver, or confidence level is impaired.

Use **READY** only when the requested output is supported. READY does not mean the company has no open exceptions.
