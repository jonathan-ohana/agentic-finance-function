# 23 — The Installer, the messy-export test, and the Finance Organization Assessment

*18 Aug 2026. Day 4 of the sprint, first day of the package build. Two agents, one of which did not exist in the blueprint.*

---

## Why an installer at all

Handing a finance person a data contract and asking them to write a mapping file is a specification, not a product. The install has to be: point the tool at your finance folder, and it works out the rest.

The Installer does four things.

1. **Profiles** every file — columns, inferred types, keys, date ranges, null rates, row counts.
2. **Infers** which contract table each file is and which column is which, scoring every file against every table.
3. **Proposes** a mapping file, flagging anything it is not confident about.
4. **Tells you what to do** about what is missing, sorted by how hard it is to fix.

That fourth step is the one with judgement in it. Every gap is classified:

| | Meaning | Effort |
|---|---|---|
| **MAPPING** | You have it, it just needs pointing at | Minutes |
| **EXPORT** | You have it, you are not exporting it | Hours |
| **SYSTEM** | Your tools do not capture it | A change request |
| **PROCESS** | Your people do not do it | A behaviour change |

The PROCESS category is the honest one, and it is where the blueprint's central claim shows up in a tool. Told that no journal line carries a document reference, the Installer does not offer to fix it:

> This is not a mapping fix. Either your bookkeeper posts summary journals without attaching support, or your GL does not carry the field. Ask for one reference per line — invoice number, bill number, or a named schedule for accruals. Start with new postings; do not backfill history.

That is doc 03's *"finance is in the flow, not downstream of it"* rendered as an install step.

## The synonym table is the product

The Installer maps `Num` to `entry_id`, `Split` to `account_name`, `Ref` to `bill_id`, `Dept` to `function`, `Net` to `amount`, `Base salary` to `annual_cost`. Roughly seventy contract fields, each with the eight or ten things different finance systems call them.

Nobody without years of looking at other people's exports can write that table. It is the least glamorous file in the package and probably the most defensible.

## The messy-export test

The clean `example/data` folder is a fiction — it is what you get *after* a competent person has structured everything. Testing an installer against it proves nothing.

So `example/messy_export.py` degrades the same company into what a real Series A folder looks like, with thirteen specific ailments:

- The general ledger split across **seven quarterly exports**, with QuickBooks column names, DD/MM/YYYY dates, a three-line title block above the header, a TOTAL row at the bottom, **no accounting period column** and **no document reference**
- Customers spread across Salesforce, Stripe and a spreadsheet, with three incompatible ID formats and no common key
- Receivables with `$` signs and thousands separators inside the amount column
- **No cash application file at all** — only a bank feed, so no receipt can be tied to an invoice
- Only the current plan version surviving; the January board plan overwritten
- Usage with no allowance and no completeness flag, keyed on Salesforce IDs rather than billing IDs
- Latin-1 encoding on the file with European club names
- Contracts existing **only as signed PDFs** — no structured contract table, so terms, minimums and cadences are invisible to any query
- And a folder containing a blank workbook, a VAT summary, a board deck and someone's close-call notes

### What the first run found

Badly. Title rows made the general ledger and receivables parse as single-column files; both were unrecognised. Amounts with currency symbols failed the numeric test. And most dangerously, **capabilities were reported READY on the strength of low-confidence false matches** — a usage file had been read as the plan, and the tool said planning was ready.

Three fixes, all of which are now permanent parts of the package:

**Header detection.** Scan the first twelve rows and pick the one that actually looks like a header — most distinct non-empty cells, consistent with the rows beneath, penalised for looking numeric. This single change took the general ledger from unreadable to correctly recognised and unioned across all seven quarterly files, 6,074 lines.

**Tolerant number parsing.** Strip currency symbols and separators before deciding whether a column is numeric.

**Confidence gating.** A capability is only READY when every table it needs is mapped with high coverage. Otherwise it reports **UNSURE**, with the reason. The footer says it plainly: *READY means confidently mapped. UNSURE means it parsed, but a human must confirm the mapping before any number is believed.*

That last one matters more than the other two. An installer that silently guesses is worse than no installer, because it produces exactly the confident nonsense the whole project exists to prevent.

### Where it still fails, deliberately

The budget file is not recognised, because it is a wide sheet with no version column — which is correct, since it genuinely lacks the structure. The Stripe export gets read as a payments file. One general-ledger file also scores as a chart of accounts. These are now surfaced rather than hidden: any file being read as two tables raises a MAPPING flag saying *"sometimes right, often a false match, confirm each one."*

Perfect inference is not the goal and is not achievable. Proposing confidently, flagging honestly, and refusing to mark something ready when it is not — that is the goal.

## The second agent: Finance Organization Assessment

The Installer reads files. It can say a column is missing. It cannot say **why**, and the why is where the real remediation lives.

It cannot know that the plan is a Google Sheet the CEO overwrites each quarter. That contracts are signed in DocuSign and then emailed to nobody in particular. That the close takes three weeks because one person does bank reconciliation by hand. That two people both maintain an ARR number and neither knows the other exists.

That is a different job — an **assessment of the finance function**, and it is an interview, not a scan. It is the eighth agent, and it runs once, before anything else.

**What it produces**

- **A systems map.** For each of GL, billing, banking, spend, payroll, HRIS, CRM, cap table and document storage: what tool, who owns it, who can export, and whether it is connected or manual.
- **A process map.** The close calendar and its actual duration. Who approves what. Which steps are manual. Where the single points of failure are — usually one spreadsheet and one person.
- **A flow assessment.** Where finance sits relative to the business. Does the contract reach finance before or after signature? Does the vendor get paid before or after the SOW is filed? Every "after" is a place the architecture will degrade.
- **A definitions inventory.** Who currently produces each headline metric, from what, and whether two people produce the same one differently. This is the input the semantic layer needs and cannot infer.
- **A readiness score with a sequenced roadmap** — what to fix first, and what to leave alone.

**Why it must be separate from the Installer.** Different input (people, not files), different output (a roadmap, not a mapping), different cadence (once at the start, then annually). Merging them would produce a tool that does neither well.

**Why it belongs in the package.** It is the artefact a CFO reads before deciding to adopt anything, and the one a first finance hire would produce in week one of a new job regardless. It is also, bluntly, the most saleable single piece here.

## Demo-day plan

The sequence to record, in this order:

1. **The assessment** — five minutes, the finance function as it actually is.
2. **The Installer against `example/messy`** — the honest folder, with all thirteen ailments. It finds the ledger across seven files, tells the truth about what it cannot do, and refuses to mark the plan ready.
3. **Fix two things live** — confirm a flagged mapping, add the missing document reference — and re-run to show the readiness change.
4. **The Installer against `example/data`** — the same company after remediation. Everything READY, lineage at 100%, autonomy unlocked.
5. **Then the agents run.**

Step 2 is the one that earns trust, because everybody watching has a folder that looks like that.

## Status

`package/` now holds `data_contract.json`, `preflight.py` and `installer.py`. `example/` holds the clean data, the answer key, the documents, the generator, a hand-written `mapping.json` and now `messy_export.py`. Nothing in `package/` mentions padel.

Next: the ingestion charter — the first agent written to be portable.
