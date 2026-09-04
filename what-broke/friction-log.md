# 60 — Friction log: user trial, live

*Trial 2 onward. Jonathan in the finance-hire seat; observations recorded as they happen, in his words where possible. Protocol: doc 56, **as amended below on 20 Aug**.*

**Severity key** — **P0** blocks a user entirely · **P1** costs real time or credibility · **P2** cosmetic or a nice-to-have.

**Protocol amended mid-trial, 20 Aug, at the user's instruction.** Doc 56 rule 2 held every finding to session 5. Split in two:

> **Correctness defects are fixed at the step boundary. Experience defects are logged and held to the retro.** The test: *does continuing produce observations that are still true?* If the product has stated something false, stop and fix — every downstream observation inherits the lie. If it merely wasted the user's time, log it and carry on, because the count and the sequence of those **are** the finding and fixing them destroys the measurement.

**One guard, non-negotiable, and it is FL-08's lesson:** after a fix, re-run the whole step from a clean workspace **on the platform it failed on**. FL-08 exists because a line was fixed, verified in the environment it was written in, and shipped still broken.

The amendment also settles an inconsistency: this project's entire thesis is an improvement loop that closes corrections immediately and measures the closure rate. Batching them to a retro was the one process in the build that did not run its own loop.

**Status column added below.**

---

| # | Where | What happened | Severity | Class | Status |
|---|---|---|---|---|---|
| **FL-01** | `START-HERE.md`, "Before you start" | *"How do I check I have Python?"* The guide says **run** `python3 --version` and never says **where**. It assumes the reader has a terminal open, knows what one is, and knows that "run this" means "type it at a prompt". A finance person has no reason to know any of that. | **P0** | **Unstated prerequisite** | held — experience |
| **FL-01b** | same | The guide gives `python3` throughout. **On Windows the command is `python`** — `python3` fails. Found while answering FL-01, before the user hit it. | P1 | Wrong instruction | **FIXED** 20 Aug — pending Windows verification |
| **FL-02** | The premise | *"I shouldn't have to install Python on my computer to start using the tool. Any other software doesn't require you to check if you have Python before you start."* | **P0 — and it is not a documentation defect** | **Wrong container** | held — retro decision |
| **FL-03** | Python install, before the package is ever opened | The installer stopped on a system prompt: *"Windows is not configured to allow paths longer than 260 characters… requires changing a system-wide setting, which may need an administrator to approve, and will require a reboot. Update setting now? [y/N]"* The user is being asked to change a **Windows registry-level setting and reboot their machine**, with a default of **N**, before this package has shown them a single number. | **P0 — evidence for FL-02** | **Wrong container** | held — evidence for FL-02 |
| **FL-04** | Environment | Machine is **Windows on ARM64**, and the runtime installed is **Python 3.14** — very new. Not all third-party packages publish builds for that combination yet, and this package needs at least one (`openpyxl`). The guide names no supported platforms and no supported Python versions beyond "3.9 or later", which is a floor with no ceiling. **Watch item for the first `pip install`.** | P1 | Unstated prerequisite | held — watch item |
| **FL-05** | Python install, still before the package | A **second** system-configuration prompt immediately after the first: *"The global shortcuts directory is not configured… Add commands directory to your PATH now? [y/N]"* — again defaulting to N, again requiring the user to judge something with no finance content. | **P0 — evidence for FL-02** | Wrong container | held — evidence for FL-02 |
| **FL-06** | Python install, still before the package | A **third** prompt — and the reveal: *"You do not have the latest Python runtime. Install CPython now? [Y/n]"*. **What the user downloaded from python.org was not Python. It was an install manager, which then asks whether to install Python.** Answer `n` here and the user has completed the entire documented install and still has no runtime. Note also that the default flips to **`Y`** after two prompts that defaulted to `N` — the muscle memory built over the previous ninety seconds is now wrong. | **P0 — evidence for FL-02** | Wrong container | held — evidence for FL-02 |
| **FL-07** | Getting to a prompt | *"In the finalized product, the user shouldn't have to do that."* — on having to open a terminal inside the extracted folder and type a command with a file path in it. Same root as FL-02: the interaction model is a developer's, not a finance person's. | **P0 — evidence for FL-02** | Wrong container | held — retro decision |
| **FL-08** | `installer.py`, final line | **The printed next command still says `python3`** — which does not exist on Windows. Yesterday's fix (defect 44 family) corrected the *path* and left the *interpreter name* hardcoded. **The single line the user is most likely to copy still fails on their machine.** Same defect, same line, fixed once already. | **P0** | Wrong instruction | **FIXED** 20 Aug — **only the user can verify this one** |
| **FL-09** | `installer.py`, MAPPING section | **The same locale-date finding printed 16 times**, once per file, each with the identical three-line why/do. It occupies more of the report than every other finding combined and pushes the four genuinely different problems out of view. **The product's own lesson, unlearned:** the Fable audit killed the pack's colour chips for exactly this — *thirteen of fourteen coloured means colour has stopped selecting.* | **P1** | Signal saturation | held — experience |
| **FL-10** | `installer.py`, file listing | **`Copy of Book1.csv` is silently dropped.** It is scanned (the header says 19 files), it is not mapped, and it is **not listed as unrecognised**. 19 in, 18 accounted for. It is an empty file with blank headers — which is exactly the kind of thing a finance person needs told, because it is usually the remains of something that mattered. For a package whose thesis is *say what you do not know*, a file that vanishes without comment is the worst available failure. | **P1** | Silent omission | **FIXED** 20 Aug — verified |
| **FL-11** | Every command in the guide | **The guide never names a working directory.** Every command is relative (`package\...`, `--data exports`), so it only works from inside the extracted folder — and a newly opened PowerShell starts in `C:\Windows\system32`. The user opened a fresh window, pasted the next command, and got `can't open file 'C:\Windows\system32\package\preflight.py'`: **an error naming a path they never typed, from a program that is not this product.** The guide's Step-2 instruction says "run these from the folder that contains the `package` folder" in prose, once, and never repeats it or shows how. | **P0** | Unstated prerequisite | held — experience |
| **FL-11b** | Same, one hour later | **It recurred.** After a clean re-download and unzip, the user opened a fresh PowerShell and pasted the commands again — same `C:\Windows\system32` error, twice in a row, for both commands. **This is not a user slip; it is the default path.** Opening a terminal and typing the command is what everyone does, and the guide's single prose mention of a working directory does not survive contact with it. | **P0** | Unstated prerequisite | held — but the recurrence upgrades the fix from "clarify the sentence" to "remove the requirement" |
| **FL-12** | Unzipping | Extraction produced `Agentic Finance\agentic-finance\agentic-finance` — the folder nested inside a folder of the same name, because Windows' Extract All creates a container and the zip already had one. Harmless, but it makes every path longer and more confusing, and it is the vendor's fault for zipping with a top-level directory. | P2 | Packaging | held — packaging |
| **FL-13** | `preflight.py` §7 vs §2 and §4 | **The report contradicts itself on one page.** §2: `gl_journal — missing: entry_id, date, period, account, debit, credit, description` — **all seven required columns**. §4: every accounting check NOT MEASURED. §7: **`READY close`**, and *"Agents supported: Bookkeeper"*. Readiness is computed as `all(tables.get(t) …)` — **whether a file was found and had rows, nothing more.** It never asks whether the table has its columns or whether a single integrity check passed. | **P0 — the worst one yet** | **False green** | **FIXED** 20 Aug — verified both directions |
| **FL-16** | `preflight.py` — the root cause of half this log | **The general ledger export has a title banner above the real header row** (`CourtIQ Inc.`, then a subtitle, then a blank, then the column names). `installer.py` detects this and reads the right header; **`preflight.py` never did.** So the installer wrote a correct mapping and the gate then read line 1 as the header, found none of the mapped columns, and reported `gl_journal — missing: entry_id, date, period, account, debit, credit, description` — **all seven.** The ledger was fine the whole time. Two components of one product disagreed about where the data starts. | **P0 — the largest finding of the trial** | Silent misread |
| **FL-17** | Both tools | Row counts differed between the two reports for the same files — gl_journal 6,074 vs 6,067. Neither was right: the installer counted physical lines (so a quoted memo containing a line break invented a row) and both counted a **TOTAL summary row** at the foot of each ledger extract as a journal line. | **P1** | Miscount |
| **FL-18** | `installer.py` inference | `stripe_customers_export.csv` — a customer list with **no amount column at all** — was mapped to `payments_received`. The 55% floor let it through because the columns it *did* match scored well. A table can clear a coverage threshold and still be the wrong file. | **P1** | False match | **FIXED** 20 Aug — `setup.py` now challenges any table whose missing fields have no plausible candidate: *"is this really your money received?"* |
| **FL-19** | The whole NOT READY → READY path | *"the tool should guide you through the process… it needs to make it very easy for the finance person to set up."* The gate said **NOT READY, 14 blocking** and left the user to hand-edit JSON. | **P0** | No path forward | **FIXED** 20 Aug — `setup.py` built |
| **FL-20** | The setup conversation | *"Once the tool asks me a question, I should be able to start a discussion. To make sure I understand the question and I give the right answer."* And then: *"I think it should be a conversation with an agent."* | **P0** | No way to ask back | **PARTLY FIXED** 20 Aug — `?` explains any question (why it matters / how to tell / what to do if unsure), `s` shows more data, `k` skips. **The agent is the real answer** — charter written, see below |
| **FL-07b** | The setup surface | Follow-through on FL-07 and FL-20: the conversation moved out of the terminal. `wizard.py` serves a local page — one question at a time, *"why are you asking?"* and *"show me my data"* on every one, back/skip, and a closing screen with the email to send. No paths, no flags, no JSON. **The runtime is still required to start it, so FL-02 is untouched.** | — | Built 20 Aug | **BUILT** — surface only; the container question stays open |
| **FL-21** | The chart-of-accounts question | *"Not sure this is the right question. The ask should be to download the chart of accounts for your company. From there the agent should be able to map each account. I would create a chart of accounts sheet — something to upload here."* The tool asked permission to **guess each account's type from its number** — a fact that is written down in every accounting system on earth. And the table it was guessing about **did not exist**: the installer had matched the general ledger to `chart_of_accounts` and manufactured one. | **P0** | Inferring a fact that exists | **FIXED** 20 Aug — see below |
| **FL-22** | The date question, framing | *"Not the right question. It should be about the date format in general, not one date in particular."* The question shows `06/02/2025` and asks **"which is it?"** — which invites the user to reason about one value, when the answer is a property of the whole export. The right question is **what date format does this system write**, with the example as evidence rather than as the subject. | P1 | Wrong frame | **FIXED** 20 Aug — asked once per file, about the format, and **only when the file cannot settle it itself**: 3,344 values in the ledger have a number above 12 in the first position, which proves DD/MM/YYYY and removes the question |
| **FL-23** | `wizard.py`, every pick question | *"I can't click on any of the first two answers."* `JSON.stringify` emits the value **with double quotes**, and inside `onclick="ans(...)"` the first quote terminates the attribute -- so every option carrying a string value lost its click handler. "None of these" kept working because it passes `null`. **Every pick question in the wizard was unusable.** | **P0** | Shipped untested | **FIXED** 20 Aug -- verified by simulating a click |
| **FL-24** | Question wording throughout | *"I feel accountants and finance people don't talk like: 'the journal or voucher number that groups a transaction's lines'. You're a top finance expert. You need to talk like a finance expert using the right terms."* Every field label was a **definition** rather than a **term of art**. | **P1** | Wrong register | **FIXED** 20 Aug -- rewritten in trade terms; definitions moved behind "why are you asking?" |
| **FL-25** | The `Num` question | Asked openly which column was the journal entry ID, offering `Num` (JE-000001) against `Split` (account descriptions). `num` was absent from the synonym list, so a certainty scored as a guess. | **P1** | Asked what it knew | **FIXED** 20 Aug -- recognised automatically; question removed |
| **FL-26** | The accounting-period question | *"Is this question necessary? Yes it's obvious. If the JE is June 2nd, let's assume it belongs to June."* Plus a factual challenge: do ERPs carry a separate period column? **Validated: NetSuite yes and they may differ; QuickBooks Online no -- the date is the period and a closing-date lock is the control.** At Seed-Series A the ledger is QuickBooks or Xero, so there is no period field to find and deriving it is the only option available. | **P1** | Asked the unanswerable | **FIXED** 20 Aug -- derived automatically and disclosed; **and turned into check R8b** |
| **FL-15** | `installer.py` §2 vs §3 | **FL-13 again, in the other file.** Twenty minutes after the false green was fixed in `preflight.py`, the installer printed `READY close` and *Agents supported today: Bookkeeper* on the same page as its own §3 reporting `gl_journal: required field(s) not found — entry_id, period`. Same rule, same violation, second location. Its readiness test used **mapping confidence** — how sure we are about the columns we found — which says nothing about whether the required ones are there at all. | **P0** | False green | **FIXED** 20 Aug — verified on Windows |
| **FL-14** | `preflight.py` §3 | `[PASS] ar_invoices — conforms` on a table §2 reports as missing **every** required column. Type conformance passes because there are no typed columns left to check. **The same "a check that ran on nothing did not pass" defect I fixed in §4 yesterday and did not look for in §3.** | **P0** | False green | **FIXED** 20 Aug — verified |
| **FL-27** | The wrong-file question | *"The Stripe customer file doesn't have any numbers in there. The question seems irrelevant and also not professional. 'Is the file your money received?' Is that how finance professionals talk? No."* Two defects in one sentence: FL-18's fix turned a bad match into a **question**, when a file with no amount column cannot be a receipts file whatever the answer; and `payments_received` was rendered as *money received*, which is nobody's vocabulary. | **P1** | Asked what it knew · wrong register | **FIXED** 20 Aug — rejected automatically with the reason stated; every table name rewritten in trade terms (cash receipts, payment run, AR/AP ledger, payroll register, customer master) |
| **FL-28** | The revenue-stream question | *"You ask for revenue stream and as answer options you put the created date and the number of courts. This is unacceptable and completely irrelevant. Your revenue stream has to be found in your ledger under series 4xxx accounts."* The question was asked of the customer master, which does not hold the answer, so every offered option was wrong by construction. | **P0** | Question with no correct answer | **FIXED** 20 Aug — question deleted; revenue splits by 4-series account from the ledger, stated in the summary |
| **FL-29** | The start-date question | *"Also irrelevant. Created Date is obviously the right column."* It was, and the tool could see it: a column named for it, containing dates, and the only one. | **P1** | Asked what it could read | **FIXED** 20 Aug — adopted automatically and disclosed; `created_date` and four other names added to the synonyms |
| **FL-30** | The cost-centre question | *"Again the cost centre question — the answer can't be the name of the employee. You have the department name but no cost centre. It would make sense to ask for the cost centre attached to each employee, but let's not do it during onboarding."* | **P1** | Question with no correct answer | **FIXED** 20 Aug — deferred out of the install; payroll splits by department, and the real ask (a cost-centre code per employee) is named as an export change |
| **FL-31** | Chart-of-accounts wording | *"Why would you say 'I won't guess one'? Who talks like that? Just say I couldn't find a chart of accounts."* Plus: cut the paragraph explaining where to find one in the accounting system. | **P2** | Wrong register | **FIXED** 20 Aug — title is the plain sentence; the how-to moved behind *why are you asking?* |
| **FL-32** | The six missing-file questions | *"What do you mean by contracts or subscriptions? You need to be much more precise. Is it customer contracts, SaaS agreements?"* · *"What is a sales pipeline? Is it relevant to finance?"* · *"Document index? What is it?"* · and on all of them: *"the options should be upload file/folder, we don't have it, or remind me later."* Six near-identical yes/no cards, each naming a file too vaguely to answer and offering no way to supply it. | **P0** | Imprecise ask · no way to act | **FIXED** 20 Aug — one card, seven rows, each with what the file is and where it comes from, **what it switches on**, and **what happens if it never arrives**; three actions per row including a real upload that writes into the exports folder, and a re-read without relaunching |
| **FL-33** | `wizard.py` / `setup.py` planner | Found while fixing FL-32, not reported by the user. The installer records only the columns it had to **rename** — a file already headed `contract_id, customer_id, term_months` produces no `columns` entry at all, and every reader falls back to the contract name. Every reader except the question planner, which read the mapping alone, concluded the file had no recognised columns, and **asked five questions about a file that was already perfect**. A clean export earned the longest interrogation in the product. | **P1** | False gap | **FIXED** 20 Aug — the planner now reads the file's own header too |
| **FL-34** | The shape of the flow | Review of build 8: *"The wizard asks before it gives. Run with what you have first, then present the questions next to a live first output."* Time-to-first-trusted-number is the trial's own metric, and the wizard was architected against it — the aha landed after the chase list, if at all. | **P1** | Wrong order | **FIXED** 20 Aug — three screens: what each file is → **your own numbers** → what is left. On the messy folder the second screen opens with 6,053 journal lines and a trial balance out by $4,506, before a single question |
| **FL-35** | The mapping itself | Same review: file-to-role assignment is the **highest-risk inference in the flow** and build 8 handled it inside a disclosure box the user read at the end. A wrong role poisons everything downstream while every check passes — the *"invisible to every check"* argument applies to it more than to dates. | **P0** | Unconfirmed high-risk inference | **FIXED** 20 Aug — one screen, every file with its role, confidence and row count, least-certain first, approved as a set in about ninety seconds. **Charter rule 1 amended** to draw the line: roles confirmed, provable facts decided and disclosed |
| **FL-36** | The chase list | *"Route the chase list to people, not just to a list… if the user can only chase one file this week, the wizard should say which one buys the most capability."* Seven rows of equal weight, addressed to nobody, with generic advice. | **P1** | Unactionable output | **FIXED** 20 Aug — ranked by capabilities unlocked, and grouped into **a drafted email per person**, each carrying the exact export path where the system is identifiable from the file names (Stripe, QuickBooks, Xero, Salesforce, HubSpot, Mercury, Deel) |
| **FL-37** | The missing-file answers | *"The three answer buttons are missing a state your own NRR case proves exists — the system holds it but doesn't export it."* That is EXPORT on the installer's own four-way ladder, and its fix (an export request) is nothing like the fix for absence. | **P1** | Answer set too coarse | **FIXED** 20 Aug — fourth answer added and reported as an EXPORT gap |
| **FL-38** | The close of the install | *"An agentic product's onboarding has one job a normal SaaS wizard doesn't: setting expectations about what will happen without the user."* And: the approval of the setup is itself a review, so it belongs in the ledger from run one. | **P1** | Missing contract · missing audit trail | **FIXED** 20 Aug — closing screen states what runs alone (nothing), what arrives as drafts, what is never touched and what would have to change; approval is signed and written as **RL-0001** in `review_ledger.csv` |
| **FL-39** | `plan` matching | Found while building FL-35, not reported. The budget in the trial folder — months down, P&L lines across, the way every company keeps one — matched nothing, so the tool reported *"no plan or budget found"* while the plan sat in the folder. Assigning it by hand then made things **worse**, because the contract wants one row per line per month. | **P1** | Silent shape mismatch | **FIXED** 20 Aug — wide files are detected and the reshape is offered as a question; on yes, plan version comes from the file's own name and plan date from its timestamp, both disclosed. **Variance vs plan went from BLOCKED to READY on a file that was already there** |
| **FL-40** | The approval screen, copy | *"This is way too wordy. Short impactful explanation is all we need."* Four sentences where one would do, on the screen whose whole promise is ninety seconds. | P2 | Wordy | **FIXED** 20 Aug — one sentence: *"A wrong role is the one mistake nothing downstream catches — every total still foots, and every number is about the wrong thing."* |
| **FL-41** | `installer.py` matching | *"We already discussed that. The Stripe customer export doesn't include any $ amount. How can this be the cash receipts? Use common sense!"* Build 9 caught it downstream — rejected it after the fact, with an explanation. **He is right that catching it downstream is the wrong place.** A money table without an amount column is not that table, and coverage scoring cannot see it. | **P1** | Matcher blind spot | **FIXED** 20 Aug — `DEFINING` extended: receipts, payments, bank, AR and AP all require an amount; the ledger requires an account. The Stripe file no longer reaches the screen as a receipts file at all |
| **FL-42** | Rejecting a row | *"If I click 'not the right file', an option to share a link to the right file should appear."* Rejecting only switched a capability off — correct, and a dead end. | **P1** | No path forward | **FIXED** 20 Aug — rejecting opens a picker **of the files it could not identify** (the right one is usually already in the folder) plus an upload button |
| **FL-43** | Multiple versions | *"How do we handle files with multiple versions?"* | P1 | Unanswered case | **FIXED** 20 Aug — a role with several files shows *+N more files*, expandable; and assigning a file to a role already filled **appends it as a further version** rather than replacing, which is what R12 wants for plans |
| **FL-44** | Role names | *"Not sure what a payroll register is. Is it the right term?"* · *"What is AP ledger?"* · *"What does the aged receivables file consist of — does it match what you call AR ledger?"* Three questions, one defect: the screen showed labels and expected the user to approve claims. **And payroll register was simply the wrong term** — that is the per-period record of gross, deductions and net, not a roster of people and salaries. | **P1** | Wrong term · unstated claim | **FIXED** 20 Aug — renamed (*headcount and salaries*, *supplier bills (AP)*, *customer invoices (AR)*) and every row now carries the claim under the name: *"what you owe — every bill received, unpaid and paid"* |
| **FL-45** | The unmatched list | *"Instead of 'files I am not using' I would have 'files I was not able to identify'."* · *"Remove the unreadable section."* · *"Why are the Deel invoices or the FY26 budget not being used? It doesn't make sense."* The third is the real one: **"not used" reads as an oversight when it is a finding.** | **P1** | Unexplained omission | **FIXED** 20 Aug — renamed, unreadable folded in as a greyed row rather than its own section, and **every row now says why**: *"closest to your customer receipts (75% of it), but it has no amount"*, *"months down the side and amounts across — the shape of a budget, but with no version on it"* |
| **FL-46** | The button | *"Rename 'That is all correct — continue'."* | P2 | Copy | **FIXED** 20 Aug — `Continue →` |
| **FL-47** | The whole screen, conceptually | *"Define clearly what files and data are needed to generate an output, then scan all available files against that mapping table."* The contract already existed in `data_contract.json` and was never shown: rows displayed a file and a confidence, not what the role is supposed to carry. | **P1** | Requirements invisible | **FIXED** 20 Aug — every row shows **N of M data points captured**; the ? beside each role lists what it must carry and what was not found; and `WHAT-IT-NEEDS.md` is generated from the contract so it cannot drift — every output, the files it needs, and every field of every file |
| **FL-48** | The second section | *"'7 files I couldn't identify' is not about existing files — we're not going to name files we're not using. It's about the files we NEED and don't have. If the annual plan is missing, the annual plan belongs in that section."* The section was a list about the folder where it should have been the other half of the requirements table. | **P0** | Wrong object | **FIXED** 20 Aug — section two is now **"N I have not found a file for"**: one row per role with no file, ranked by what it unlocks, each with upload / remind me later / not exported / we don't have it. The old missing-files card at step 3 is gone — it was always this list, shown too late |
| **FL-49** | The budget, again | *"You have identified FY26 Budget v7 as the annual plan. And yet it's still in the second section. Doesn't make sense."* Build 9 could only identify a wide budget **after** the user assigned it by hand. | **P1** | Matcher blind spot | **FIXED** 20 Aug — the matcher now recognises the shape itself: a month column plus two or more P&L captions across the top is a budget, whatever the columns are called. `FY26 Budget v7 FINAL (2).csv → budget or plan` with no human involved; the reshape is still offered rather than assumed |
| **FL-50** | Definitions on the row | *"The definition for what each file is should be under a question mark — hover and it appears."* | P2 | Layout | **FIXED** 20 Aug — `?` beside every role, hover for the meaning plus the data points it must carry and the ones missing from your file. The row itself is back to one line |
| **FL-51** | Screen 1, the header | *"'A wrong role is one mistake…' is bad. It's confusing. It needs to be about: we scanned your files, please help the agent match them to the right roles."* The heading led with the risk instead of the task. Sections were named after the tool's state, not the user's job. | P1 | Wrong frame | **FIXED** 21 Aug — *"I have scanned your files. Help me match them to the right roles."* Sections are **N matches to confirm** and **N roles without a match** |
| **FL-52** | The roles-without-a-match rows | *"Remove the explanation of why we need it, where to find it, who owns it. The what-is-it should be under the question mark. Keep the unlocks — that's a good find."* Five lines of prose per row, fifteen rows. | P1 | Wordy | **FIXED** 21 Aug — row is now the name, the ?, and what it unlocks. Everything else moved behind the ? |
| **FL-53** | Its options | *"The options should be: something about sharing a link (we don't need an upload), we do not have it, remind me later. Remove all other options."* Five buttons where three would do. | P1 | Too many actions | **FIXED** 21 Aug — three. The starting sheet is no longer a button: **saying you do not have a chart of accounts is what builds it**, from your own ledger, and the closing screen says so. A link is recorded and carried into the chase email so nobody has to find it twice |
| **FL-54** | *"1 of 5 data points"* | *"What do you mean?"* A ratio invented for the screen, meaningless without the contract next to it. | P2 | Jargon | **FIXED** 21 Aug — the row names what is absent instead: *"no plan version, no date this plan version was set"*. The counts live behind the ? with the full list |
| **FL-55** | *"Also read, and not needed"* | *"Remove it. We won't list 1,000 unnecessary files."* Correct, and it exposed the better answer: an unrecognised file is only interesting **next to the role it nearly filled**. | P1 | Noise | **FIXED** 21 Aug — section gone. A near-miss now appears on the row of the role it missed: *"Closest thing in your folder: stripe_customers_export.csv — 75% of it, but no amount in your functional currency — use it anyway"* |
| **FL-56** | The suggestion on an unmatched role | *"Deel invoices is about payroll, right? Why do you have it under customer contract?"* and *"Don't suggest a file there. Otherwise it should be in the first section."* A 43% name overlap was offered as a candidate; the file is contractor payroll. | **P1** | Bad suggestion | **FIXED** 21 Aug — suggestions removed entirely. The rule is now binary: confident enough to match it, or say nothing. A near-miss is a fact for the report, not an offer on the install screen |
| **FL-57** | Two roles on the list | *"Remove document index. Remove FX rates."* Neither exists at Seed to Series A, and putting them on the first screen turns a short chase list into an unattainable one. | P2 | Wrong audience | **FIXED** 21 Aug — `HIDE_AT_INSTALL`. Both stay in the contract and in the pre-flight; the document index reappears once, at the close, as the reason nothing can leave draft-only |
| **FL-58** | `data_contract.json` | *"Why would there be a revenue stream in a customer master file?"* The contract had `segment` as REQUIRED on customers, so a complete customer file was reported as incomplete — while `DEFER` already said revenue splits by 4-series account. The tool disagreed with itself. | **P1** | Contract wrong | **FIXED** 21 Aug — `segment` is now optional, with the reason written into the contract. Recurring revenue no longer waits on a column nobody has |
| **FL-59** | The budget question | *"Remove the budget question on page."* The matcher identifies a wide budget **by its shape** — and then asked the user to confirm the very observation it had matched on. | **P1** | Circular question | **FIXED** 21 Aug — reshaped automatically, disclosed at the close. The row says what it did: *"months down, 6 lines across — I read it as one row per line per month"* |
| **FL-60** | Screen 2 | *"The dashboard on page 2 should be the result of onboarding, so I would exclude it from the onboarding process."* Correct, and it resolves the tension in doc 65: the aha does not have to interrupt the flow to land, it has to be the thing waiting at the end. | **P1** | Wrong place | **FIXED** 21 Aug — the numbers moved to the closing screen. **Onboarding is now one screen and a result** |
| **FL-61** | The verbose sub-heading and the missing-field list | *"Remove 'everything I produce…'"* · *"Keep only the first."* | P2 | Wordy | **FIXED** 21 Aug — sub is *"Least certain first."*; the row shows the first missing data point with a count of the rest behind the ? |
| **FL-62** | The mapping table | *"I like that view. Instead of saying what's missing, there can be a missing link for each item — click it and a small window appears with the card for that role."* Plus: *"Remove the also-read category, replace it with missing, keep the grey format."* | P1 | Built out | **BUILT** 21 Aug — `mapping_table.py`. Required data points only; a missing one carries a grey **missing** tag that opens the role's own card. It is a program in the package now, linked from the closing screen, not a one-off page |
| **FL-63** | The same table, without a company in it | *"I want to see what the table looks like without the matching — how many roles we have and how many data points per role."* | P1 | Missing view | **BUILT** 21 Aug — a second tab, **The model**: 15 roles, 73 required data points, an overview table of role → data points → what it feeds, then one card per role. The requirements with nothing of yours in them |
| **FL-64** | The data contract itself | *"Do we have everything we need? A commission plan is missing. Employee benefits is missing. I don't see an internal-use software capitalisation plan or any capitalisation plan with the amortisation schedule. This needs to be exhaustive."* Fifteen roles covered a close, a pack and a forecast — and stopped at the point where most of the judgement lives. | **P0** | Model incomplete | **FIXED** 21 Aug — **contract 1.1: 29 roles, 138 required data points, 24 capabilities.** Fourteen added: commission plan, employee benefits, hiring plan, fixed assets and capitalised software, prepayments, accruals, deferred revenue, debt, leases, equity grants, expenses and card spend, vendor contracts, tax returns, marketing spend |
| **FL-65** | The consequence of FL-64 | Adding fourteen roles nobody at Seed to Series A has would have turned a clean install into *"10 of 24"* and read as failure. | P1 | Signal saturation | **FIXED** 21 Aug — every role and capability carries a **tier**. Core is what a close needs; extended does not block a close and decides whether it is *right*. Reported and counted separately everywhere, and extended roles are not chased during an install |
| **FL-66** | Duplicate files | *"What do we do with duplicates — multiple versions of the same file? The user will check-mark the source of truth."* | P1 | Unhandled case | **FIXED** 21 Aug — a role with more than one file says which kind it is. **Transactional tables are a union** (a ledger by quarter: all true, read together). **Everything else is versions**: radio buttons, one source of truth, the rest set aside — except plans, where every version is kept on purpose and the current one is marked |
| **FL-67** | Several files, one role | *"We should be able to add multiple files for the same role."* | P1 | Missing capability | **FIXED** 21 Aug — *+ another file for this role* on every matched row. And the substantive half of the answer is FL-64: a commission plan and a hiring plan are not versions of a headcount file, they are **their own roles**, which is why they now exist |
| **FL-68** | The unmatched cards | *"Add back the background colour for each role without a match card."* | P2 | Layout | **FIXED** 21 Aug |
| **FL-69** | The install screen | *"The user should also be able to share the link to a file he deems important, with a description bar to explain what it is."* Every path in was a path the tool had asked for. Nothing let the customer volunteer something. | **P1** | One-way conversation | **FIXED** 21 Aug — *Something else that matters*: a link and a description, added as often as you like. Recorded in the mapping under `_flagged`, disclosed at the close, and carried into the chase list. **A flagged file the model has no role for is the more useful finding**, and it lands where the model gets extended |
| **FL-70** | The `missing` tag | *"The missing is way too big. Please resize just like required."* | P2 | CSS collision | **FIXED** 21 Aug — the pill carried `class="tag miss"` and `.miss` is also the class on the roles-with-no-file **card**: 20px of card padding applied to a pill. Renamed to `tag gap`. Two components, one class name, and the one that loaded second won |
| **FL-71** | The install screen | *"You should add all missing roles under the missing roles section."* Contract 1.1 added fourteen roles and `HIDE_AT_INSTALL` kept every one of them off the install screen — so the model doubled and the screen showed the same six. Then, on the first attempt at the fix: *"No need to add '16 more beyond the close' — it's the same section."* | **P1** | Hidden model | **FIXED** 21 Aug — **all 22 unmatched roles, one flat section**, ordered by what each unlocks. A role with no file is a role with no file, whether or not a close can be signed without it; tiering belongs in how capabilities are *counted*, not in whether a role is *shown* |
| **FL-72** | The build stamp | *"Ah show me, I didn't see."* Investigating produced a defect in my own process, not the product: **three consecutive builds all reported `build 15`.** Each bump was written into a patch script that asserted its way to a different anchor first and aborted before writing, so the version string never moved while the code did. The page's whole reason for carrying a build number — *"am I running the version you were sent?"* — was quietly false. | **P1** | Version lied | **FIXED** 21 Aug — stamped 17 and verified in the served page rather than in the source |

---

## FL-26 — a question deleted, and a check gained

The user's instinct was right and the reason is a fact worth having checked rather than assumed.

**A real ERP keeps posting date and posting period apart on purpose.** NetSuite has a setting called *Allow Transaction Date Outside Of Posting Period*, precisely so a vendor bill dated 28 June can post to July when June has closed. Its own documentation warns that *"financial reports are built on the transaction's posting period; all other reports are based on the transaction date"* — which is why an AP ageing can disagree with the accounts and nobody can work out why.

**QuickBooks Online has no such field.** The transaction date *is* the period, and the control is a closing-date lock instead.

**So the question was unanswerable in the case that matters.** A Seed–Series A company is on QuickBooks or Xero. There is no period column to point at, deriving the month from the date is not a shortcut but the only thing available, and asking permission for the only possible answer is theatre. It is now derived automatically and disclosed in the summary, with the cut-off check left open — because what the derivation cannot see is exactly the entries booked after a month closed.

**And the deleted question became a better check.** Where a ledger *does* carry both fields, the difference between them is not noise — it is the list of post-close entries, and nobody exports it. **R8b** compares them, groups them by which month was booked into which, and where there is no period field says so plainly rather than passing:

> `[ -- ] R8b Every line is posted in the month it is dated — this ledger has no separate posting period, so the date is the period by definition and there is nothing to compare. Normal for QuickBooks and Xero; a real ERP would let these differ.`

Two columns most systems already have, compared. It is the closest thing to a cut-off test that can be run on an extract alone.

---

## FL-23 -- I verified that it rendered, not that it worked

Three screenshots were taken of that wizard before it shipped. All three looked right. **Not one of them clicked anything.**

The bug is trivial. The pattern is not, because it is the third instance of the same error in two days:

- **FL-08** -- a fix verified on the platform it was written on, shipped broken on the platform it was for.
- **FL-13 / FL-15** -- a rule fixed in the instance it was reported in, left standing in the other file.
- **FL-23** -- a surface verified by looking at it, shipped with no working controls.

Each time the verification was real, and each time it tested the wrong property. **Rendering is not working, one platform is not all platforms, and one instance is not the rule.** The user found all three, which is the argument for the trial and an uncomfortable one for the builder.

---

## FL-22 — the format is the question, not the date

Held at the user's instruction; recorded now so the reasoning survives.

**What it asks:** *"Dates in your general ledger look like 06/02/2025. Which is it? — 6 February 2025 / 2 June 2025."*

**What it should ask:** *"What date format does this system export?"* — naming the conventions, with the example underneath as evidence. The three that exist, and a finance person will recognise all of them:

| | | |
|---|---|---|
| `DD/MM/YYYY` | day first | most of the world, including the UK and Europe |
| `MM/DD/YYYY` | month first | essentially only the United States |
| `YYYY-MM-DD` | ISO 8601 | unambiguous, which is why it is the right answer to the underlying problem |

**Why the framing matters and is not cosmetic.** Asking about one value invites the user to reason about that value — and `06/02/2025` is exactly the case where reasoning about the value cannot help, because both readings are valid. Asking about the *format* points them at the thing that can actually settle it: what system produced the file, and what its regional setting is. The evidence row already shows six dates; it should be illustrating an answer, not asking for one.

**And a real consequence hiding behind the wording.** The format is a property of the FILE, not of a column — but the question is currently asked once per table, on the `date` column alone. The customer-invoice export has `Invoice Date` **and** `Due`; the supplier-bill export has `Bill date` **and** `Due date`. One answer should settle every date column in that file, and probably every file out of the same system. As built, it settles one column and leaves the others to be guessed at or reported as unresolved.

**The fix, when it comes:** ask about the file's convention once, apply it to every date column in that file, and offer ISO as a third option — both because some systems already emit it and because naming it is the shortest route to the advice the installer already gives, which is to re-export as ISO and stop having the problem.

---

## FL-21 — do not infer what exists as fact somewhere

The question was wrong, and it was wrong twice over.

**It proposed inferring something the customer's own system states.** A chart of accounts is not a judgement call — every accounting package exports one, and it says in writing whether 4030 is revenue or a cost. Guessing that from a leading digit is the tool preferring its own cleverness to the customer's records.

**And the table it was guessing about had been invented.** There is no chart of accounts in those exports. The installer matched the general ledger to `chart_of_accounts` — the same file it had already matched to `gl_journal` — then handed the manufactured table downstream, where setup dutifully asked how to fill in the one column that would have made it real.

Three fixes, and the third is the one worth keeping:

**A ledger is not a chart of accounts.** Added to the exclusivity rules. The first attempt blocked only the primary file and the matcher promptly took a different quarter of the same ledger — *the rule defeated by arithmetic rather than by argument* — so it now blocks every file in the partner's union.

**A table has defining fields.** Coverage thresholds measure how MUCH of a table a file supplies; they cannot see that one field is the whole point. Blocked from the ledger, the matcher went looking for the next-best thing and offered **the bank statement**. `DEFINING` now records that a chart of accounts without a `type` column is a list of accounts, which is a different object.

**And the part that came straight from the user: make asking cheap.** "Go and get a file" is a dead end if the customer must then build it from nothing. The tool already knows **all 51 account codes in their ledger**, so it now writes them into a sheet with the type column blank and a suggestion beside it to correct. The work left is reading down one column.

> *I couldn't find a chart of accounts, and I won't guess one.*
> *Every accounting system exports this… **Or take a head start** — I already know every account code in your ledger, so I can write them into a sheet with the type column left for you.*

**The general rule, now in the code:** where a table is missing but its content is partly recoverable from data already in hand, offer the half-filled sheet as well as the request.

---

## FL-20 — the missing agent, and it was the one the project is about

The user's proposal, and it exposed a structural gap rather than a usability one.

**Setup was the only place in this package where a judgement gets made with no agent and no charter over it.** *Is `Num` your journal number? Is this really your payments file?* Those are judgements — they are exactly the kind of question this whole architecture says a written agent should own and a deterministic engine should merely inform. Everything else in the workforce has that split. Setup did not.

And the role was already defined, in this project's own positioning. Doc 34 named the **Finance Systems Engineer**: the person who owns *"the revenue data model, integrations, usage-to-cash reconciliation"* — and argued that at Seed–Series A, **finance hire #1 must be the finance systems owner, executed with agents and semantic rules instead of Python and BigQuery.** That is the pitch the entire project rests on, and it had no charter.

`charters/systems_engineer.md` now exists. The rule that matters most in it is the one explaining why it is **L0 permanently, with no promotion path ever**:

> *"Every other agent here can earn promotion, because something downstream refuses to balance when it is wrong. Nothing refuses to balance when you are wrong — that is the definition of the harm you cause. A ledger whose debit column is pointed at the wrong field balances perfectly, reconciles perfectly, and reports numbers that are entirely fictional. Every check passes. The pack builds. The board reads it."*

**The honest limit, recorded now rather than discovered later:** `setup.py` running standalone answers `?` from explanations written in advance, so it answers anticipated questions and no others. A genuine conversation the customer can interrupt needs a model at their end — which is FL-02's container question again, arriving from a third direction. Charter written; the surface it runs on is still undecided.

---

## FL-16 — the finding that reframes the whole trial

For four hours this trial believed the demo ledger was unusable. Preflight said so plainly and repeatedly: *"gl_journal — missing: entry_id, date, period, account, debit, credit, description."* All seven required fields. Every downstream conclusion — `BLOCKED close`, four accounting checks unmeasurable, *Agents supported: Controller* — followed correctly from that.

**It was wrong, and the ledger was fine.**

The export begins with a title banner: the company name on line 1, a subtitle, a blank line, and the real column headers on line 4. Every accounting system on earth does this. `installer.py` already had a `find_header()` for exactly this reason, used it, and wrote a perfectly good mapping. **`preflight.py` had no equivalent**, read line 1 as the header, and therefore could not find a single column the mapping named.

So the pair behaved like this: one tool understood the file, wrote down what it found, handed the note to the second tool — **and the second tool could not read the file the note described.**

With header detection added to the gate, on the same data, unchanged:

| | before | after |
|---|---|---|
| `ar_invoices` | missing 9 columns | **PASS** |
| `gl_journal` | missing 7 columns | missing 2 (`entry_id`, `period`) |
| Checks that could not be measured | 7 | **2** |
| R1 trial balance | not measurable | **runs — and fails** |

And the first genuine accounting finding of the entire trial appears:

> `[FAIL] R1  Total debits equal total credits — 65,570,417 vs 65,574,923 over 6,053 posted lines`
> `[FAIL] R3  Every account exists in the chart of accounts — 48 accounts; unknown: ['1210', '1300', '4040']`

**The trial balance is out by $4,506, and three accounts are posting to a chart that does not contain them.** That is what this product is for, and it took until hour four to say it — not because the analysis was wrong, but because the file was being opened at the wrong line.

**The lesson, third time of asking:** the two programs do not share a reader. They do not share a readiness rule (FL-13/15) and they do not share a row count (FL-17) either. Every one of those defects is the same defect — *two implementations of one idea, corrected one at a time.*

---

## FL-13 / FL-15 — the same rule broken in three places, fixed one at a time

The rule is one sentence, written into `Report.item` on 19 August: **a check that ran on nothing did not pass.** Its readiness corollary: **ready means usable, not present.**

It has now been violated and fixed in three separate locations, on three separate occasions, each found by the user rather than by me:

1. `preflight.py` §4 — accounting checks reporting PASS on an empty ledger *(fixed 19 Aug)*
2. `preflight.py` §3 and §7 — type conformance and capability readiness *(fixed 20 Aug, after FL-13/14)*
3. `installer.py` §2 — the same readiness test again, twenty minutes later *(FL-15)*

**The pattern is not that the rule is hard. It is that I fix the instance I am shown.** Each fix was verified, each verification passed, and each left the next copy of the same defect standing. The third one was found because a user re-ran a step I had declared closed.

For the retro: the fix that would have prevented all three is not a better guard clause. It is a single shared function that answers *"is this capability ready?"*, called from both files — so the rule lives in one place and cannot be half-corrected. **A rule enforced by discipline in four locations is a rule that will be broken in the fifth.**

---

## FL-13 — the product failing its own thesis

Everything logged before this was about getting *to* the software. This one is about what the software says, and it is the most serious entry in the log.

On a single page, the report states:

- the general ledger is **missing all seven of its required columns**
- **no** accounting-integrity check could be measured
- **`READY close`** — and the Bookkeeper is listed as a supported agent

A user who reads only section 7 — which is the section written to be read, titled *"What the agents can do with this"* — will conclude they can run a month-end close. They cannot. There is no account, no debit, no credit, no period. **The green light is computed from the existence of a file with rows in it.**

This is precisely the failure the whole package is built to prevent, committed by the component built to prevent it:

> *"A tie check proves arithmetic closure, not attribution."* — learned at defect 28
> *"A check that ran on nothing did not pass."* — written into this very file yesterday, in `Report.item`

**I wrote that rule into section 4 and did not carry it into section 7.** The rule is now in the codebase in one place and violated three sections below it.

The fix is small and the lesson is not: a capability is ready when its tables are present **and** their required columns are mapped **and** the integrity checks that govern them have actually run and passed. Anything less is a green tick for the existence of a filename.

---

## FL-08 — the one I should be most uncomfortable about

Yesterday's trial found that the installer's printed next command omitted the `package/` prefix, so the line a new user copies failed. I fixed it, verified it, wrote it up in doc 59 as closed, and re-ran the trial to prove it.

**I fixed it on Linux.** The path is now correct and the interpreter name is still `python3`, which does not exist on this user's machine. The line still fails, for a different reason, in the same place.

That is the second time this exact line has been wrong and the second time it was found by a user rather than by me — because the verification re-ran the trial **in the environment the fix was written in.** Doc 59 said the build's tests were all tests of the happy path. This is the same error one level up: **the fix's test was a test of the happy platform.**

---

## The install-day tally, before the product has run once

**Six entries. Four of them P0. Not one of them is about finance, and not one is a defect in anything this project built.**

The user has answered **three consecutive prompts about the operating system**, agreed to a **registry change requiring a reboot**, edited their **PATH**, and discovered that the thing they downloaded **was not the thing they wanted** but a manager that installs it. Two prompts defaulted to `N`; the third defaults to `Y`, so the habit formed in the previous ninety seconds is now the wrong answer.

At no point has `START-HERE.md` been wrong. **That is the point.** The guide is accurate and the experience is still this, which is the cleanest possible demonstration that FL-02 is a container problem and not a documentation one.

**One line for the diary chapter:** *the product's first user spent his first ten minutes not on his employer's books but on his own laptop's registry.*

---

## FL-03 — the cost of FL-02, made concrete within two minutes

FL-02 was an argument. This is the receipt.

The user has not opened the package, has not seen the installer, has not been shown one figure. What they have seen is a **black window asking permission to change a system-wide Windows setting, warning that an administrator may be required and that the machine will need a reboot** — and the safe-looking default is `N`, which is the answer that causes a confusing package failure twenty minutes later.

Three separate things a finance person must now judge, none of which is about finance:

1. whether a registry-level path-length change is safe on a work laptop
2. whether they have the admin rights, or must ask IT and wait
3. whether `N` is the cautious answer *(it looks like it and it is not)*

**On a managed corporate laptop this is where the evaluation ends**, not because the product failed but because it never got the chance to run. That is the whole of FL-02 expressed as a single screen.

**For triage: this is not a documentation fix.** No sentence in `START-HERE.md` makes this acceptable. It is the strongest available evidence that the runtime has to move off the user's machine, or the audience has to be restated.

---

## FL-02 — the one that questions the shape of the thing

Every previous finding, including yesterday's six, was a defect *inside* the product. This one says the product is in the wrong box.

**It is right on the merits.** No software a finance person uses asks them to install a language runtime first. Excel does not. Their ERP does not. A hosted tool does not. "Check you have Python 3.9+" is not a prerequisite, it is a **request that the user do part of the vendor's job**, and it lands on page one, before any value has been delivered. Everything the package does well — the installer's four-way gap ladder, preflight's honest verdict, the agents' refusals — sits behind a step that a large share of the intended audience will not complete.

Worse, it is the step most likely to fail *invisibly*. A wrong ERP export produces an error message. A missing runtime produces a person who quietly closes the folder.

### The tension this creates, which is the reason to record it carefully

The red team (doc 29) explicitly **cut** package-as-product decisions — name, licence, distribution — on the grounds that this is *a portfolio artefact with an install guide, not a product*. That ruling stands and it was right.

But FL-02 exposes a seam in it. **The moment the artefact carries an install guide addressed to a finance person, it has made a claim about who can install it** — and Python-at-a-terminal falsifies that claim. There are only two coherent positions:

1. **It is a portfolio artefact.** Then the reader is a technically comfortable hiring manager or a founder, the runtime is not a barrier, and the guide should say so plainly at the top — *"you will need to be comfortable running a command"* — rather than implying a finance-hire audience it cannot serve.
2. **It is aimed at a finance person.** Then the container is wrong and no amount of guide-writing fixes it. The runtime has to disappear: a hosted version, a packaged executable, or running it where the data already lives.

**The current artefact claims (2) in its prose and delivers (1) in its packaging.** That is the actual defect, and it is a positioning defect, not an engineering one.

### Not to be fixed during the trial

Under rule 2 this is logged and worked around. It is also **the single highest-value entry the trial can produce**, because it is the kind of finding that only exists when someone who is not the builder reads page one — and because it costs nothing to state and would have cost weeks to discover after shipping.

For session 5 triage, the question is not *"how do we remove Python?"* It is: **who is this for, and does the packaging agree with the prose?**

---

## FL-01 — the note for triage

This is the first instruction in the guide and it fails for the reader it was written for. Worse, it fails *silently*: someone who does not know what a terminal is does not get an error message, they get stuck with no signal, and the most likely next action is to close the folder.

It is also a class, not an instance. The guide says "run" four more times and never once says where. **Every command in `START-HERE.md` inherits this defect.**

The fix at triage is not a longer sentence. It is a short, illustrated *"Step 0 — open a terminal"* section, per operating system, and a plain statement of what a terminal is and that nothing typed into it can damage anything. Possibly also a one-click check script.

**Note the pattern against doc 59.** Yesterday's six defects were all found by pointing the tools at unprepared *data*. This one was found by pointing the guide at an unprepared *reader*. The build has now failed the same way twice: it tested the happy path, and the happy path assumed a user who already knew.

---

---

## FL-27 to FL-33 — twelve questions became two, and the rule that did it

The user reviewed all twelve setup questions in one pass and rejected, in some form, **nine of them**. Read together the objections are not nine separate complaints. They are two rules the product was breaking.

**Rule one: if the file settles it, the file settles it.**

The date question is the clean case. It asked *"dates look like 06/02/2025 — which is it?"* and the honest answer was that **the ledger already knows**: 3,344 of its values carry a number above 12 in the first position, and only day-first allows that. The tool was holding up one ambiguous value and asking the user to reason about it while sitting on three thousand proofs. Same class: a start date column named `Created Date` containing dates; an accounting period that can only be the month of the posting date; a journal number column called `Num`.

Asking anyway is not caution. **It is a tool declining to read its own input**, and it costs the user's attention at exactly the moment they are deciding whether this thing knows anything.

The scan now runs over every date column of every file behind a table, and produces one of four outcomes: proved day-first, proved month-first, **two conventions in one file** (a broken export, reported as such and never averaged), or genuinely undecidable — which is the only case that becomes a question, framed as the file's format rather than as one value.

**Rule two: do not ask a question whose only available answers are wrong.**

Revenue stream, offered against the columns of a customer master, could only be answered with a created date or a court count. Cost centre, offered against a payroll file that carries departments, could only be answered with an employee's name. The user's word was *unacceptable*, and it is the right word, because the failure is not that the guess was poor — **it is that no correct option was on the screen.** A user who is offered an absurd suggestion learns that the suggestions are worthless, and from that point answers no to everything, which is a worse state than never having asked.

Both of those are now out of the install. Revenue splits by 4-series account, from the ledger, where it lives. Payroll splits by department, which is what the file has, and the real ask — a cost-centre code per employee — is named as a change to the export rather than smuggled in as a question.

### What the count actually measures

**Twelve questions to two.** But the number that matters is what happened to the other ten: **six became sentences on the closing screen** — each saying what was decided and what proves it — and four disappeared because they were wrong to ask. Nothing was hidden to make the number smaller. The disclosure got longer while the interrogation got shorter, which is the trade the whole package is built on.

### FL-32 in particular: what a missing file is worth

The six *"do you have one somewhere?"* cards were the least defensible thing in the wizard. Each named a file too vaguely to identify — *contracts or subscriptions* to a finance person means their customers' contracts or their own SaaS agreements, and the tool never said which — and then offered yes or no, where **yes did nothing but add a line to an email**.

They are now one card, and each row carries four things: what the file is and which system it comes from, **what it switches on**, **what happens if it never arrives**, and three actions — upload it now, remind me later, we don't have it. *We don't have it* is a real answer with a stated consequence, not a failure to comply.

The upload is real: the file is written into the exports folder, and the closing screen offers to read the folder again without relaunching anything. On the document index, the consequence sentence is the one that matters most — *everything stays draft-only, permanently; an agent that cannot show its evidence never earns autonomy* — and it is the first time the autonomy ladder appears in the install rather than in a charter.

### FL-33: the defect the user could not have found

While rewriting the missing-file card, an uploaded contracts file with perfectly clean headers produced **five questions**. The installer records only the columns it had to rename; a file already headed `contract_id` produces no entry, because every reader falls back to the contract name. Every reader except the one that generates the questions.

So **the cleanest possible export earned the longest interrogation**, and the messy one did better. It had been true since the wizard was written, and no user would ever have diagnosed it — they would have concluded the tool could not read a normal file, which, on the evidence in front of them, would have been the reasonable conclusion.

---

## FL-34 to FL-39 — the second review, and the number that justifies it

A reviewer read the twelve-to-two rewrite and returned seven ranked gaps. Doc 65 holds the review in full and the triage against it. Two things are worth recording here rather than there.

**The order of the first two was wrong as given, and both were right.** Gap 1 said show a number before question 1. Gap 2 said the file-to-role assignment is the one inference every downstream check is blind to. Put together as stated, they produce a first number computed from an unapproved role assignment — the exact failure gap 2 exists to prevent, delivered at the moment of maximum trust. The order that satisfies both is **approve the roles, then show the numbers**, and the approval is itself the first thing of value the user sees: for most of them it will be the first time every export they own has appeared, named, in one list.

**And the screen paid for itself on the first run.** The trial folder contains `FY26 Budget v7 FINAL (2).csv`. It had matched nothing, so every version of this tool up to build 8 reported *"No plan or budget found — without a plan there is no variance analysis"* while the plan sat four inches away in the same folder. On the approval screen it appears under *five files I am not using*, one dropdown assigns it, and the wizard then notices it is wide and offers to read it as one row per line per month.

**Variance versus plan went from BLOCKED to READY, on a file that was already there.** Blocking issues 14 → 11, capabilities ready 1 → 2. Nothing was fetched, nobody was emailed, and the only new information came from the user glancing at a list.

That is the argument for the screen, and it is a better one than the risk argument: the mapping table is not merely the place a dangerous error gets caught, it is the place the tool finds out what it already had.

---

## FL-40 to FL-46 — the terminology round, and the one that was not about terminology

Eleven comments on the approval screen. Seven were copy and layout; three were terminology; one was a matcher defect wearing a terminology costume.

**The matcher defect (FL-41) is the one worth keeping.** The Stripe customer export had already been caught in build 9 — but *downstream*, by a rule that rejects a table whose missing fields have no plausible candidate, and it produced a paragraph of explanation on the closing screen. The user's response was not that the explanation was wrong. It was: *use common sense*, meaning **catch it in the matcher, where a person would have caught it, and never show me the paragraph.**

He is right, and the rule is one line: a money table without an amount column is not a money table. Coverage scoring cannot see that — a customer export shares half its columns with a receipts file, and the ledger shares most of its columns with a chart of accounts — which is why `DEFINING` already existed for three tables. It now covers six more. The file never reaches the approval screen as receipts; it appears among the unidentified, saying *closest to your customer receipts (75% of it), but it has no amount in your functional currency.*

**The three terminology questions have one answer, and it is not a better word.** *Is "AP ledger" the right term? What does the aged receivables file consist of? Is a payroll register the headcount tracker?* Each asks the user to approve a claim while showing them only a label. The fix is to state the claim: **supplier bills (AP) — what you owe: every bill received, unpaid and paid.** Now the row can be approved or rejected on its meaning rather than on whether two people use a word the same way.

One of the three was also just wrong. A payroll register is the per-period record of gross, deductions and net; the file is a roster of people and salaries. Renamed to *headcount and salaries*. The Deel invoices are contractor invoices — payables, not payroll — and they now say so on the screen instead of sitting silently in a list.

**And "not used" was the wrong frame entirely (FL-45).** A finance person reading *five files I am not using* asks, correctly, why their budget is one of them. Renamed to **files I could not identify**, with the reason on every row: the near-miss table, how much of it the file covered, and the field it lacked. On this folder that turns a list of five shrugs into five findings — including two the user could act on immediately, and did: assigning the budget and the usage file took ready capabilities from **one to three** without a single new export.

---

## FL-47 to FL-50 — the requirements table, and the section that was pointing the wrong way

Three comments, one structural idea underneath all of them: **the screen should be the requirements table, checked against the folder — not a report on the folder.**

That distinction sounds academic until you look at what it changes. A list about the folder has two sections: files I used, files I did not. A list about the requirements has two sections: **roles I found a file for, roles I did not** — and the second one is the useful one, because it is the same list whether or not the file exists anywhere. *"You haven't given me a budget"* is actionable. *"I'm not using these five files"* is a shrug with names in it.

So section two is now the roles with no file, ranked by what each unlocks, each with the four answers. The missing-files card that used to appear at step 3 is gone: it was always this list, shown after the user had already been asked to approve a mapping with holes in it.

What is genuinely unrecognised is now a **footnote** — one line of file names, expandable, each saying why and offering a role. It keeps FL-10's rule (a file that vanishes without comment is the worst available failure) without spending a section on it.

### The budget, and why it took two rounds

The sharpest of the three: *"you have identified FY26 Budget v7 as the annual plan, and yet it is still in the second section."* Both halves were true in build 9, and together they were incoherent — the tool could only see the budget **after** the user pointed at it.

The fix is that the shape is the identification. A month column down the side and two or more P&L captions across the top — revenue, COGS, R&D, S&M, G&A, EBIT — is a budget, whatever any individual column is called, and no amount of column-name matching will ever find it because the contract wants one row per line per month and the file has none of those columns. It is now matched on shape, and the reshape is still put as a question rather than assumed.

### And the data points

The contract has always specified every field of every table; it had simply never been shown to anyone. Each row now reports **N of M data points captured**, the ? lists what the role must carry and what your file lacks, and `WHAT-IT-NEEDS.md` is generated from `data_contract.json` at build time — the requirements table the user asked for, guaranteed to match what the programs actually read because it is written from the file they read.

---

## FL-51 to FL-55 — the same screen, a third of the words

Five comments, all subtractive, and the product is better for every one of them. What is worth recording is not the edits but the pattern in them: **three of the five removed something this build had added for a defensible reason.**

The five-button row existed because a reviewer was right that *"we don't have it"* and *"the system holds it and nobody exports it"* are different states with different fixes (FL-37), and because a starting sheet is genuinely useful (FL-21). Both true. Both wrong on the screen, because a person scanning fifteen rows does not read five buttons — they read the first two and stop.

The resolution was not to drop the ideas but to move them out of the way. **Saying you do not have a chart of accounts is now what builds the starting sheet** — the action became a consequence of an answer rather than a fifth option next to it. That is a better design than the one that was cut, and it only appeared because the button had to go.

**The near-miss is the same move.** *"Files I could not identify"* was cut as noise, correctly — nobody wants a list of files they are not using. But the information inside it was real: `stripe_customers_export.csv` is 75% of a receipts file. It now appears on the row of the role it nearly filled, where it is not a list at all but an offer: *use it anyway*. Deleting the section is what forced the information to find its right place.

The header change is the smallest and possibly the most important. *"A wrong role is the one mistake nothing downstream catches"* is true, and it is the reason the screen exists, and it is **the builder's reason, not the user's**. What the user needs at the top of a screen is the job: *I have scanned your files. Help me match them to the right roles.* The risk argument still exists, one hover away, for the person who wants to know why they are being asked.

---

## FL-56 to FL-61 — onboarding becomes one screen

Six comments, and between them they removed the last two questions in the flow. On the trial folder, setup is now **one screen and a result**: confirm seven matches, tell it about six roles it has no file for, and the next thing you see is your own trial balance.

**The two questions that died were both circular.** The wide-budget question asked the user to confirm the shape the matcher had just used to identify the file. The date question had already gone the same way for the same reason. There is a general rule underneath both, and it is worth stating: **if an observation is good enough to act on for matching, it is good enough to act on for reading — and if it is not, the match should not have been made.** A tool that matches on evidence and then asks permission for the evidence is performing diligence rather than doing it.

**The dashboard moving to the end resolves a tension in doc 65.** Gap 1 of that review said *show value before asking for anything*, and I built it as screen 2, between the approval and the questions. The user's correction is better: onboarding is not where the numbers belong, **the numbers are what onboarding produces.** The aha does not need to interrupt the flow to land — it needs to be waiting at the end of it. Interrupting also cost something real: a second screen to click past, which is exactly what the last four rounds have been removing.

**And the contract was wrong, not just the screen (FL-58).** `segment` was required on the customer master, so a perfectly complete customer file was reported incomplete — while `DEFER` in the same codebase said revenue is split by 4-series account and the customer-master question should never be asked. Two parts of the product held opposite positions on the same field, and only the user asking *"why would there be a revenue stream in a customer master?"* surfaced it. The contract now says what the rest of the package already believed.

---

## FL-62 and FL-63 — the requirements, with and without you

Two requests, and together they turned a throwaway page into the third program in the package.

**What the second view is really for.** *"Show me the table without the matching"* sounds like a documentation request and is not one. Every screen built so far answers *have I got what this needs?* — which cannot be judged without first seeing *what does it need at all*, and that question has never had an answer anywhere except inside `data_contract.json`. **15 roles, 73 required data points**, one overview table, and nothing about the reader's company in it. It is the same list the install screen checks against, which means the two views cannot disagree: they are generated from the same file.

**And the missing tag.** A missing data point named on its own — *no billable metric* — is information only to someone who already knows what the role is for. Clicking it now opens the same card a role with no file at all gets: what it is, what it unlocks, what happens without it. One component, two places, and the second one costs nothing because the first already existed.

Optional fields are gone from the page. They doubled its length to answer a question nobody asks — an optional field is by definition neither needed nor missing. They are still read where present, and they are still in `WHAT-IT-NEEDS.md`.

---

## FL-64 — the model was not exhaustive, and that was the largest gap left

Three examples, and each one is a different kind of hole.

**The commission plan** is a cost the ledger records and nothing explains. It is also, at this stage, the most commonly wrong accrual in the book — computed in a spreadsheet, reconciled by nobody, and material the moment a rep beats quota. There was no role for it.

**Employee benefits** is worse, because the contract already knew: `headcount.annual_cost` carried the note *"Base, excluding employer burden"*. The model documented the omission and then did nothing about it. Base pay is 70–80% of the true cost of a person, so a plan built on the roster alone is wrong by the burden, every month, in the largest line in the P&L.

**Capitalised software** is the one with the most at stake. Whether engineering payroll is an expense or an asset moves EBITDA, gross margin and the R&D line, and it is decided by a policy plus a schedule with in-service dates and useful lives. The package had neither.

The pattern across all three: **the model covered what a close needs and stopped where the judgement starts.** Fourteen roles now cover the rest — including deferred revenue (billings are not revenue, and the difference is the first thing diligence asks about), leases, debt with its covenant written down, equity grants for share-based compensation, tax returns, card spend, and committed vendor spend with the notice date, which is earlier than the renewal date and is what anyone actually has to diary.

**Tiering was not optional once the count doubled.** Fourteen roles no company at this stage has, reported in one list with the ten that matter, would tell somebody whose close is clean that they had failed at twenty-two things. Core and extended are counted separately in the pre-flight, on the closing screen and in the mapping table; extended roles are not chased during an install at all.

**What is still open.** The user's next sentence was the right one: *"then I envision a feature where Claude is embedded in the product and we can ask to add the missing elements — or manually add."* The manual path exists and is documented at the end of `WHAT-IT-NEEDS.md`: the contract is a JSON file, a role is one entry, and everything downstream follows from it. The conversational path — *"we also track deferred COGS, add it"* — is the natural next build, and it is genuinely small, because the contract is already the single source every other component reads.

---

## FL-73 — a card that opens a card is a dashboard explaining itself

*"On clicking the metric card, I didn't mean for another card to open. The clicking card should open the excel spreadsheet."*

The drawer was the wrong artefact and it took one sentence to see why. A drawer restates the number with a derivation next to it, which is the same claim in longer form; it asks to be believed twice. **A finance person clicking a figure is not asking for an explanation, they are asking to see the rows.** So the click now opens the sheet: a grid, with column letters, row numbers, a green title bar carrying the file name and the engine that produced it, sheet tabs across the bottom, and the actual lines the number was built from.

The change is cosmetic for about ten seconds and then it is not, because a grid has to contain something. Building four of them forced four numbers to be recomputed from the example ledger rather than carried forward, and **three of the four were wrong.**

---

## FL-74 — the numbers that did not survive being opened

**Gross burn was overstated by 24%.** The card had a revenue figure on it, which the user replaced with gross burn. The obvious computation — credits on the cash accounts — gives $1,094,912 for July. It is wrong: $214,185 of it is the month-end sweep from the EUR operating account to the USD one, which is one company moving its own money and appears as both a receipt and a payment. True gross burn is **$880,727**, and the sheet now carries the transfer as its own column with the total nil.

**Runway had three answers and the card was showing the fourth.** It said 17.3 months. Tracing it: `validate.py` computes cash divided by **July's operating loss** — an accrual figure, one period, $459,357 — as a story sanity check, and the number leaked out of the generator onto the front page. MET-008 rules runway as closing cash over trailing three-month *net cash burn*, which gives **19.9**. The Forecaster, the only instrument allowed to produce months-to-zero, gives **13.8 to 19.0** across its scenarios. So a package whose stated doctrine is *the runway figure appears once in this whole system* was carrying three definitions, and displaying the one that agreed with none of the others.

It survived because nobody could open it. That is the entire argument for making every card open its sheet, and the sheet now carries all three bases with the 17.3 line marked as not a runway. The card now reads **13.8 – 19.0 mo** with *window unruled, FC-01 open*, and the sheet shows five scenarios with what each assumes. **A range on the card is not indecision — the spread is 5.2 months and every bit of it comes from a choice nobody has made.** Under the Forecaster's rule 2 that choice is not the agent's, so the card does not make it either.

**ARR could be computed and had been refusing for the wrong reason.** *"Let's figure the rule for ARR/MRR and let's calculate something."* SL-08 rules three metrics: MET-009 committed recurring ARR is v1.0, effective from the start of the dataset, and computes cleanly — **$4,608,471**, MRR $384,039. It was MET-010 (ARR including usage run-rate) whose v2.0 does not take effect until August, and MET-011 that is barred from board material. The card was refusing a metric it could have produced, because the refusal had been written before the registry was read carefully. **The honest version is stronger than the refusal was:** a number, on the ruled definition, with the ruling cited, next to two named siblings that do not have one.

**And the disclosure SL-09 requires is on the sheet.** 2,703 players are contracted at €12.99 and billed €9.99 — a grandfathered price that expired on 1 March and a billing system nobody updated. €8,109 a month, about $109,510 a year, sits inside the ARR above and is not being collected. It stays in the metric, because the definition uses contracted price, and it is disclosed every month until the drift is zero. Defining it away would make the billing defect invisible, which is the whole argument for the basis.

> **Superseded 18 Aug by defect 22 — and not by a restatement.** The paragraph above says the
> €8,109 a month sits *inside* the figure, because the definition uses contracted price. The
> definition does; `arr_schedule.csv` did not — it computed MET-009 on `actual_price_eur`, so the
> leakage was missing from the number rather than disclosed inside it, and the figure above is
> the billed-price book.
> Rebuilt on the ruled basis, MET-009 committed recurring ARR is $4,743,222 at 31 July.
> SL-09 has been effective since 2025-02 and ratifies existing practice, so nothing here was
> restated: a ruling was written and never propagated to the schedule it rules. Both figures stay
> on this page — what the card showed, and what it should have shown — because the distance
> between them is the finding.

---

## FL-75 — the sheet said something the card could not

Gross burn fell 13.7% month on month. On a card that is good news with a green arrow.

On the sheet it is not news at all. **Cost incurred fell 4.0%. Paid-acquisition spend was flat to within $349 — and $314,137 less of it was paid.** Accounts payable rose $93,261 in the month, which is two-thirds of the entire improvement. Every other cash line went up.

The sheet has no verdict field, so it does not say "this is a timing effect". It reports cash paid, cost incurred, and the payable balance on the same page and lets the three of them argue. That is the difference between a metric and an instrument, and it is the reason the arrow on the burn card is grey rather than green: **a fall in gross burn is not automatically good, and colouring it good is the dashboard telling you what to think about your own company.**

---

## FL-76 — the queue came off the home page, and the Chief of Staff earned its place

*"Remove the queue."*

Ten escalations under three columns of counts made the page end in a list, which is a page that has stopped prioritising. The queue is now its own screen, one click away and reachable from the count that names it.

What replaces it is the part the page was missing. The three columns are lists — *ten escalations, four blocked steps, four dates* — and a list asserts that everything on it is equally the reader's to sort. **The Chief of Staff ranks, and the user's instruction was precise about where the right to rank comes from:** *"It's also linked to your email or any meeting transcript so it would know if there's anything not in that page worth your attention."*

That is the correct architecture, and it is not a feature request about email. Everything else in this system reads the ledger, and the ledger is a record of what has already happened. **The inbox and the calendar are where the things that have not happened yet live** — a vendor saying an invoice will be late, an EOR moving a cut-off, a CEO asking for a number before Thursday. Two of the three items in the digest change something on the page above them: the payroll deadline is a day earlier than the finance calendar thinks, and the accrual the day-28 scan reported as *unusable, spread too wide* has just been confirmed by the vendor at €8,900.

The limitation is stated on the page rather than in a footnote: **it reads, ranks and links. It cannot send, reply or act, and the connector is read-only by design.** An agent with write access to the inbox of the person who signs the accounts is a different risk conversation, and it is not one this package needs to have to be useful.

---

## FL-77 — three statement models, and nobody had written down what the system produces

*"Maybe first thing we need to understand is what are the key calculated sheets the agents produce once they have scanned all documents. We have a list of required documents with required inputs. We need now a list of required calculated sheets with the required output."*

This is the largest structural gap found in weeks, and it had been invisible because the half that existed was good. `data_contract.json` describes 29 input roles and 138 data points in detail. **Nothing described the other end.** Every engine knew what it produced; no artefact said what the system produced, which meant there was no way to answer the most obvious question a buyer or a CEO asks — *what do I actually get* — except by reading five programs.

`output_contract.json` is the answer: **22 calculated sheets**, in five families — the three statements plus their articulation, the reconciliations, the schedules behind the balance sheet, the analysis, and the governance packs. Each carries five things:

| | |
|---|---|
| **requires** | the input roles without which it cannot be produced at all |
| **uses** | the roles that make it complete, absent which it publishes with a stated gap |
| **outputs** | the lines it must contain — not a description, a checklist |
| **ties to** | the sheets it must agree with, with the residual reported in currency rather than a tick |
| **refuses when** | the single condition under which it declines to produce a number |

**The refusal row is the one that took the longest and matters most.** A sheet that always produces something cannot be trusted, because you can never distinguish *this reconciles* from *this was rendered*. A cash flow statement that does not articulate is not a draft, it is a defect. A P&L with an account the chart does not contain has wrong subtotals rather than incomplete ones. A variance report against an unnamed budget is a lever. Writing 22 of these down was the exercise that proved the contract was real.

**And the third view is the one that will get used.** *What a gap costs* prices every missing input role in the sheets it blocks rather than in capabilities. "We don't have a fixed-asset register" is an easy sentence at install and an expensive discovery at audit; on that page it costs a named schedule, a supported balance-sheet line, and the capital expenditure line of the cash flow statement. On the demonstration instance, **20 of the 22 sheets are producible today and two are not**, and the page says which two and why.

Every one of the 29 input roles feeds at least one sheet. That was worth checking: a role that fed nothing would be a question asked at install for no reason, and the grid is what makes that impossible to hide.

---

## FL-78 — what is still wrong

**`variance.py` and `kpi.py` still name this company's segments.** Thirty-odd occurrences of terms that belong to the demonstration instance, in files that ship. It is defect 20, it has been open since the sweep, and it is the one standing constraint on this package that is currently being broken. Nothing else in `package/` mentions the example company; these two do, and until they stop, "ships to any company" is a claim with an exception in it.

**The output contract is written and not yet wired.** The 22 sheets describe what the engines do; the engines do not yet read the contract to decide what to produce or to publish their own refusal reasons from it. That is the difference between documentation and machinery, and the mapping table crossed it months earlier by being generated from `data_contract.json`. The same move is available here and has not been made.

---

## FL-79 — ten edits to the dashboard, and one of them was a doctrine question

Nine were presentation and took an hour. *Remove the company and the date from the header. Remove the close status from under the greeting. The tab is a Dashboard, not a Monday. `As of 08/17/2026`, and say what the arrow compares to. Cut the tooltips — "bank position from yesterday midnight" is enough. Drop "open the sheet"; a card that highlights on hover has already said it. Millions on the cards.*

All correct, and the common thread is worth naming: **every one of them removes a word that was doing the job of a smaller word.** "Ledger cash on accounts 1010 and 1015, the bank position, not liquidity, nothing here nets off the payment run" became "the bank position at yesterday's midnight". The longer version was not more honest — it was the same claim, taking four times as long to read, on a card whose entire purpose is to be read in under a second.

**The tenth was not presentation.** *"Whose job is it to calculate cash runway? The forecaster should take the controller hypothesis for the first 13 weeks. Their estimates shouldn't vary."*

That is a ruling, and the package needed it. The Controller runs a 13-week direct grid from contractual detail: open invoices, open bills, payroll dates. The Forecaster runs a six-month model from drivers. **They overlap for thirteen weeks and nothing said what happens in the overlap.** Measured: from the same July close of $7,911,301, the Controller reaches $6,785,821 at the end of week 13 and the Forecaster reaches $6,611,113 at the end of October. **$174,708 apart, with no rule saying which governs.**

SL-26 now says it: inside thirteen weeks the Forecaster adopts the Controller's committed receipts and payments unchanged and models nothing of its own; beyond week 13 it forecasts. The Controller holds the detail, the Forecaster holds the horizon, and the handover is at week 13 and nowhere else. The ruling is written and `forecast.py` does not yet implement it, so the workbook states the divergence rather than resolving it by presenting whichever number is more convenient.

---

## FL-80 — the cards now open real workbooks

*"Let's create real excel sheets to click on from the metrics cards. I need to verify how everything is being calculated."*

The HTML grid was a picture of a spreadsheet. This is the spreadsheet: four `.xlsx` files, built by `tools/build_sheets.py`, linked from the title bar of each sheet view.

**The rule they were built under: no number is typed where a formula can compute it.** Each workbook carries the source rows on their own tabs — 1,805 general ledger lines that touch cash, 1,677 bank statement lines, the payment file, the ARR schedule, the pricing-drift register, the 13-week grid, the forecaster's scenarios — and every figure on the front tab is a `SUMIFS` or an `INDEX/MATCH` over them. The as-of date is one blue cell; change it and all seven months move.

| | |
|---|---|
| `cash_reconciliation_2026-08.xlsx` | seven months, opening to closing, with own-account transfers separated; ledger against bank, difference computed **0.00**; funds in transit; the runway numerator |
| `gross_burn_2026-07.xlsx` | 36 categories July against June, then the bridge: cost incurred, cash paid, payables. **67% of the fall in cash burn is the rise in payables** — a computed cell, not a claim |
| `runway_2026-07.xlsx` | MET-008 arithmetic, five scenarios, the SL-26 reconciliation, and the three competing numbers with **17.3 recomputed from the operating loss** so the reader can see exactly where it came from |
| `arr_schedule_2026-07.xlsx` | the MET-009 build with **two tie cells that must be nil**, the SL-09 leakage disclosure summed from 2,703 rows, the three other ARRs, and a cross-check that rebuilds courts ARR from the customer file and lands **0.19%** from the engine |

Zero formula errors across 273 formulas. Every figure on the home page now ties to a cell somebody else can open.

**What this changes about the demonstration.** The strongest objection to the whole artefact was always *how do I know any of this is real* — and until today the answer was "read the Python". A CFO does not read Python and should not have to. **Four workbooks, live formulas, source rows attached, is the form of proof this audience already trusts**, and building them found three more things: a transfers column mislabelled as netting to zero, a constant-currency tie that is a rounding difference and now says so, and a cross-check that does not tie exactly and now names why rather than being quietly dropped.

---

## FL-81 — an escalation was a memo, and a memo is what you write when you have not decided what you want

*"This needs to be much clearer. Concise, clear, with action points. What is the situation, what is the risk, what do we need the Finance hire to do. Is this something you would prepare yourself? What do you need to prep for this?"*

Every escalation opened with four paragraphs of argument and closed with a question. The argument was good — E-03 is the best thing in the package — and it was in the wrong place. **A finance lead reading this at 08:40 wants three things in one order: what is happening, what does it cost, what do I do today.** The reasoning matters only if they disagree with the conclusion, and putting it first makes every reader earn the conclusion before they can act on it.

All ten now open with **the situation** and **the risk** side by side, then **what I need you to do** as a numbered table — action, who, how long, what it unblocks. The full argument is folded underneath, one click, labelled with its paragraph count.

**The time estimate is not decoration.** An action without one is a request to be ignored, because the reader cannot tell whether it costs ten minutes or a fortnight and defaults to assuming the worst. E-01's first action is ten minutes: *ask whoever built the 2025 spreadsheet whether the Q2 return was submitted.* Everything else in that item branches on the answer, and nothing in any system can produce it.

**And the question underneath the question was the important one.** *Is this something you would prepare yourself?* Each item now answers it explicitly, in two blocks that face each other:

**What I will do once you have** — for the VAT item: compute output VAT by member state and quarter from the 4010 and 4035 lines at each country's standard rate, produce the OSS working, draft the recognition journal unposted, reconcile the 2025 spreadsheet against what the ledger implies, and diary all four deadlines with a latest-safe-start on each.

**What I cannot do** — file the return, and know whether the 2025 one was filed. There is no tax data in any governed system, so the first fact has to come from a person.

That pair is the honest version of the whole product claim. Without it, "agentic finance" quietly means *it will sort itself out*; with it, the reader knows exactly which half is theirs. The `cannot` line is also the one place in the artefact where the system says something against its own interest, and it is the line most likely to be believed.

---

## FL-82 — "Stripe takes a fee. Where is it in this sheet?"

One question, asked of a finished cash reconciliation, and the answer was **nowhere** — which turned out to be the finding rather than an omission.

**What the ledger does.** The processor fee is accrued monthly, `Dr COGS — payment processing fees / Cr Accounts payable`, and the payout is recorded as the **gross** clearing balance moving into the bank. Both halves are internally consistent. Both are wrong about the world: a processor settles itself by deduction, so it is never invoiced and never paid. **$77,931 at 31 July sits in accounts payable — 9% of the balance — against a counterparty that will never send a bill**, and it grows every month. Fees run **2.52% of gross billings through the processor**, $83,727 on $3.33m.

**What the correct treatment is.** Revenue gross — the customer's promised consideration is the full charge, the processor is not the customer, and its fee is a cost of collecting rather than a reduction of the transaction price, under both IFRS 15 and ASC 606. The fee clears through the **processor clearing account at the point of capture**, so the payout settles to the net amount that actually reached the bank. Three entries, and the middle one is the whole argument: `Dr 5050 / Cr 1020`, not `Cr 2010`.

**Why nobody had caught it in eighteen months, and this is the part worth keeping.** *The P&L is fine.* Revenue gross, fee expensed, net income exactly right. Every review that reads an income statement passes it. Only the balance sheet and the composition of cash are wrong — and the reconciliation that would catch it, a per-payout bridge from gross charges to the net bank credit, **did not exist as a close step.**

**The dataset had its own tell.** The synthetic bank file records the payout gross, identical to the ledger, which is why the reconciliation ties to $0.00. A real processor statement would not: it would disagree by exactly the fee, every payout. The generator reproduced the company's error faithfully enough that the bank side agreed with it — which is a good argument for testing an engine against a statement it did not produce.

**What shipped:** **SL-27** in the semantic layer (revenue gross, fee clears through 1020 and never through payables, and the ruling extends to every future settlement counterparty — app stores, marketplaces, embedded finance, each of which settles net and arrives with the same error attached); **CL-38**, the processor clearing reconciliation, blocking, owned by the Bookkeeper; **E-11** in the queue with the reclassification as a five-minute approval; and a payment-processor block on the cash workbook showing charged, settled and carried-in-payables, with a Processor fees tab behind it.

**The general lesson.** The question that found this was not sophisticated. It was *where is the thing I know exists?* asked of a sheet that looked complete. A finance function's real defects are rarely in the numbers that are present; they are in the ones nobody expected to see and therefore nobody missed. **A sheet is not finished when every figure ties — it is finished when a knowledgeable person cannot name something that should be on it and is not.** That is a better completion test than any check in this package currently implements, and it is not automatable, which is exactly why the review ledger exists.

---

## FL-83 — the dataset was told to break, and the engine found it unassisted

*"Wait, so we need to modify the bank statement to not be gross right?"* — and then, looking at a competitor's Stripe integration: *"we should be able to understand the fee portion."*

Both are right, and the second is the one that turned a disclosure into a control.

**The bank statement is the one document in a dataset that cannot be wrong.** It is external. If the processor deducts its fee before remitting, the bank line is net, and a synthetic bank file that records the payout gross is not modelling a bank — it is modelling the company's own error twice, on both sides, so the reconciliation ties and nothing is learnable.

**The rule that made this work: fix one side only.** Netting the bank *and* correcting the ledger would have restored the tie and destroyed the finding. So the bank went net, the ledger kept its error, and the two now disagree by exactly the cumulative fee.

**Then the engine found it with no code change.** `CL-05` on the July close: `account 1010: bank minus GL [-77,930.76]`. An hour earlier that number had been produced by a human reading a spreadsheet and asking where the fees were. This is the difference between a package that documents a defect and one that catches it, and it was one file away the whole time.

**The fee portion is the part that had to become a source.** A monthly bulk accrual cannot be reconciled against anything — you can tie a total to a total and learn nothing about which payout it belongs to. So `stripe_payouts.csv` now carries **one row per settlement: gross charges, refunds settled, processor fee, net to bank, effective rate**, and it earned a role in the data contract (`processor_settlements`, extended tier) with its own capability. **The contract is now 30 roles.** The note on the role says why it exists: *the bank line is net and can never be tied to revenue without this file.*

**CL-38 is now implemented rather than declared.** On July: gross $201,235 less fees $5,790 equals $195,445, which is exactly what the bank received — and exactly $5,790 less than the ledger recorded as a payout. Four separate assertions, each computed: the processor's own arithmetic, the bank against the processor, the fee charged against the fee deducted, and the ledger's payout against the net received. The last one is the finding, and the step names SL-27 as the ruling that fixes it.

**What moved.** The close is now **15 of 19** rather than 14 of 18. The cash card shows **$7.0M — the bank's number, not the ledger's** — because a cash balance the bank will not confirm is not a cash balance, and you cannot spend ledger cash. E-07 changed shape entirely: it used to say *the reconciliation ties and part of it is unverifiable*, and now says *there is one difference and it is explained to the dollar, and separately there is a component nobody can verify.* **An explained difference is a reconciliation. An unexplained one is a finding. A reconciliation with neither is a summary.**

**And the generator check was inverted rather than deleted.** *Every bank account reconciles to its own GL account* now fails by design, so it became *bank and GL disagree by exactly the processor fees never cleared* — which asserts the gap equals the cumulative fee to within a dollar. 89/89 again. A check that would have to be satisfied by breaking the dataset is a check pointing the wrong way, and rewriting it is cheaper than losing the demonstration.

---

## FL-84 — four problems wearing one costume

*"How should we handle multiple versions for the same file? How does the AI know which one to use? We need to come up with some rules."*

What the installer did was decide by **table type**: transactional tables union, everything else is a version, plans keep all. That is a guess about the files made without opening them, and it covers two situations out of four.

**Fragments** are slices of one population — a ledger exported one quarter per file. Not versions at all. **Restatements** are the same population exported again. **Coexisting versions** are both true, with which one governs depending on the question. **Snapshots** are photographs of something that changes, where the rule is to read the version governing the period being reported rather than the newest — and reporting June off the newest headcount file is wrong in a way that never raises an error.

**The rule that makes it decidable: the machine classifies, the machine does not choose.** Four measurements settle which situation it is — key overlap, period coverage, row equality on shared keys, column shape — and each situation has its own signature. Where the signature is unambiguous the tool acts and discloses, which is rule 1 of the charter. Where it is ambiguous it asks one question, and **the question carries the diff**. Someone asked *which file is right* guesses. Someone shown *1,168 of 1,170 rows are identical, 2 differ, the value moves by $2,500* answers correctly. That is the whole design.

---

## FL-85 — the classifier compared the wrong pairs, and said everything was fine

The first implementation sorted a role's files by date and compared adjacent pairs. On the demonstration folder — seven quarterly ledger exports plus a restated Q2 — it compared Q3 against `2026Q2 FINAL`, found nothing in common, and reported **eight files, clean union, contiguous coverage**. A confident, well-evidenced, wrong answer, produced by a tool built specifically to catch confident wrong answers.

The fix is a rule worth keeping: **coverage decides what is a fragment; only files covering the same ground can be versions of each other.** Bucket by period first, union across buckets, resolve versions only inside one. A role can be both at once, and the verdict now says so:

    [FRAGMENTS]   across periods
       7 distinct period coverages
       -> Union. Coverage: 2025-02 to 2026-08, 19 periods, contiguous

    [RESTATEMENT] 2026-04 to 2026-06
       1,170 shared rows, 1,168 identical, 2 differing, 3 only in the
       earlier file, value moves by 2,500.00
       -> Adopt the later file. That difference is a finding, raised
          rather than absorbed.
       SHELVE  General Ledger 2026Q2.CSV  (retained, never deleted)

The three rows that exist only in the earlier file are a re-coding — `8030` legal reclassified into `8040` audit — which the key treats as a delete and an add rather than a change. That is a limitation of keying a ledger line on entry, date and account, and it is disclosed in the evidence rather than smoothed over: **three rows present in one export and not the other is itself something a reviewer should see.**

**And one small thing that would have broken it in every real folder.** The first run called the quarterly ledgers snapshots rather than fragments, because two files shared exactly one key. The shared key was the report footer — `TOTAL`, with the number split across three columns by an unquoted comma, so every field the key reads was blank. Two blank-keyed footers from different quarters look like the same row restated. Rows that cannot identify themselves are now excluded, and the count of keyed rows is reported rather than the count of lines.

**What shipped:** `package/versions.py`, and **SL-28** — *which file is the answer* — carrying the four cases, the classification rules, and the five supporting rules: never union overlapping keys; the filename is a hint and never evidence; retain everything and log the adoption; a version choice that moves a reported number is a ruling, not a setting; refuse rather than pick.

---

## FL-86 · The disclosure that kept being inherited

I was fixing three things the reviewer named — hardcoded dates, actuals reading their prices off the assumptions tab, and missing sources — and the fix surfaced a fourth that nobody had asked about.

Deriving the actuals is what found it. While the price came from the assumptions tab, the usage section multiplied out perfectly, because it was multiplying an assumption by itself. The moment the rate had to be *recomputed from the book* — revenue over matches over FX — it came out at EUR 1.41 against a contracted 1.20, in every single closed month. A rate that is wrong by the same 17% for eight months running is not noise.

Account 4030 carries metered overage **and** minimum shortfall true-ups. A club pays overage for using the product more and pays a true-up for using it less. Merged, the per-match economics improve as clubs play less.

**None of this was new.** SL-11 ruled the true-ups onto their own account 4032 in the very first pass. ESC-12 escalated that 4032 was never built. The close pack names it, the variance pack names it, KPI-03 already works around it by text-matching, and doc 42 says in writing that the overage implied price sits above the rate *because* of this. Four artefacts disclosed the defect and the fifth quietly inherited it.

**That is the friction worth logging.** A disclosure stops a number being believed. It does not stop it being used. Every new artefact built on a contaminated account re-commits the error unless something splits it, and "it is already on the register" reads like handling when it is only documentation. The register had been doing its job for weeks; nothing downstream was reading it.

**What shipped:** the model splits on the evidence that was in the ledger the whole time — the true-up entries carry their own invoice and memo — shows the two as adjacent sections, reconciles the split back to 4030 every period, and prints the reason on the line. **SL-29** rules the general case: where an account is known to carry two economics and the separating account does not exist, split on entry-level evidence at the point of use, reconcile to the account, and state it as a workaround with an expiry.

Split, every month with overage recomputes to the contracted EUR 1.20 to the cent. FY26 metered overage is USD 327k against USD 51k last year, up 547%; true-ups are USD 55k against USD 224k, down 75%. Those are the two clearest facts in the revenue model, they point in opposite directions, and the merged line was showing neither.

**Two more things the derivation caught**, both invisible while the actuals were assumptions:

The club count was computed from *today's* active clubs, which silently rewrote every prior month — a club that churned in May was absent from January too — so the roll-forward drifted against the register and the derived price per court wobbled between 88.5 and 91.0. Corrected to a period-end count that includes a club in every month it traded, the derived price lands on 89.17 against a contracted 89.00.

And blended ARPU derives to 10.76 across the closed months while the forecast was reading 12.20 off the drivers tab. The gap is 2,703 grandfathered accounts still billing at 9.99. Holding the derived actual instead of the list price took USD 141k out of the forecast — revenue that was only there on the assumption that someone had already decided to reprice that cohort and absorbed the churn. Nobody had. **A model that reads its prices from the assumptions tab does not just agree with itself; it books decisions that have never been taken.**

Total FY26 revenue is now USD 5.36m against a board plan of USD 5.52m — USD 160k behind, where the model previously showed USD 4k ahead.

---

## FL-87 · The tab that no system produces

The reviewer asked a question I should have asked myself: *no ERP would generate that history page in an early-stage startup — is that a fair assessment?*

It is, and it was the weakest thing in the file. The History tab was a clean nineteen-by-twenty grid of clubs, courts, subscribers, coach seats, matches, FX and revenue by stream, sitting there with the quiet authority of an export. It was a paste. Every figure had been computed in Python and typed into a cell, and nothing on the face of the workbook said so.

**Why it matters more than it looks.** Half the argument of this whole system is *show your working*. A model whose actuals arrive as an unexplained block has moved the unexamined step one tab to the left, not removed it. And the tab was load-bearing: eleven derived rates on the model divide by figures that only existed there.

**What a company this size actually has.** Six extracts, and the shape of the problem is that not one of them is a list of months:

| | |
|---|---|
| **General ledger** | revenue by account. Knows nothing about courts. |
| **Club register** (CRM) | one row per club, with dates and court counts. Knows nothing about matches. |
| **Subscriber list** (billing) | 19,064 rows, one per subscription, with the price actually billed. |
| **Coach list** | 940 rows. |
| **Usage log** (product) | one row per club per month: courts metered, matches, entitlement. Has never heard of euros. |
| **FX table** | 19 rows. |

Each is a list of *things*. The monthly grid is a list of *months*. Nothing bridges them until somebody in finance does, and that assembly is not a preliminary to the work — **it is the work**, and it is the part of the job that never appears in a job description.

**What shipped.** The six extracts are now six source tabs, and History is calculated: `COUNTIFS` and `SUMIFS` against dates and periods, one formula per figure, twenty-two columns by nineteen months. The revenue columns sum off a `Stream` column on the ledger tab which is itself a formula, so the SL-29 split is visible at the point it is made rather than asserted upstream. I rebuilt every figure independently from the raw CSVs and checked it cell for cell against the recalculated workbook.

**Three things the rebuild caught that the paste had hidden:**

**The allowance was 120.5, not 120.** Deriving entitlement per court as total allowance over month-end courts gives 120.2 to 120.6 depending on the month. The numerator comes from the meter and the denominator from the register, and they are different populations — a club metered in the month it terminated is not in the month-end count. Both halves now come from the meter and it recomputes to exactly 120. **A ratio whose numerator and denominator come from different systems is wrong in a way that looks like rounding.**

**Counting conventions have to agree across registers or the roll-forward drifts.** Clubs and subscribers are now struck on one rule — count in every month you traded, leave the count in the month you terminate — which is what makes opening plus additions less churn equal closing on both. It had not, and the drift was showing up as a derived price per court that wobbled between 88.5 and 91.0 against a contracted 89.00.

**The seven clubs that signed and never installed are an exclusion someone has to make.** They sit in the register with a status and no other flag. Counted, they inflate the base and depress every per-club rate. That exclusion is now a criterion in a visible formula rather than a filter in a script, which is the difference between a judgement and a secret.

**And three smaller corrections from the same review.** The pipeline's stage weightings were typed into the tab — they now look up the Drivers tab by stage name, so changing a probability there changes the forecast. The close-date column was unlabelled: it is the owner's committed signature date from the CRM, not an installation or a cash date, and it now says so. The ACV column was unexplained and unused; it now carries a derived neighbour, ACV over courts over twelve, which reads 89.00 on all 64 open opportunities — **the pipeline confirming it is priced at the contracted rate, and a column that would light up the day somebody discounted without recording it.**

---

## FL-88 · "Weighted courts is wrong? Did you mean weighted revenue?"

The reviewer's instinct was that weighting a physical unit is a strange thing to do, and that the pipeline should be weighted in money. The right answer turned out to be *neither and both*, and chasing it down found something worse.

**They cannot disagree here.** Every open opportunity is priced at the contracted EUR 89 per court per month, so ACV is courts times 89 times twelve, exactly, on all 64 rows. Weight the money and weight the units and you get the same statement in two denominations: both blend to 44.5% of the whole, and weighted ACV over weighted courts over twelve recovers 89.00. All three figures are now on the tab as a visible tie-out.

**The model consumes courts, and that is deliberate.** Courts carry forward — they earn again next month, they are metered for usage, and they set the included allowance. Money does not carry forward; it is the output. But the reviewer was right that the money column had to be there, because everyone outside finance discusses pipeline in euros, and **a number that cannot be checked against the CRM's own report is a number nobody trusts.**

**The thing worth saying plainly.** A weighted count is an expectation, not a forecast of any one deal. 7.4 clubs in September means the stage mix is worth seven and a bit. No club signs 40% of a contract. That is fine across a portfolio, and this portfolio is 64 opportunities — large enough to average, small enough that one 16-court club landing or slipping moves the month.

**And then the calibration question, which is where it got interesting.** If the four stage probabilities are the load-bearing assumption, what are they calibrated against? So I went to look.

**The CRM records 246 opportunities Closed Won against 1 Closed Lost.** A 99.6% win rate. That is not a win rate — it is a CRM where lost deals are deleted rather than marked lost. And closed records do not retain the stage they were in, so stage-by-stage conversion cannot be measured either. **The four probabilities driving the entire courts forecast are convention, and the data that would evidence them has been destroyed by ordinary CRM housekeeping.**

They are now labelled as convention on the Drivers tab rather than dressed up with a basis, which is the honest treatment: the alternative is a "basis" column that reads *standard first-stage conversion* and means nothing.

**What it is worth, which is the part that makes it useful rather than alarming.** Weighted, the pipeline contributes USD 850,263 of FY26 courts revenue. If every open deal closed on its committed date it would contribute USD 906,654. The whole weighting decision is worth **USD 56,390 — about 1% of total revenue.** So: the assumption is unevidenced, and it is also not where this forecast's risk lives. Both facts go on the tab. A finding that turns out to be immaterial is still worth sizing, because the sizing is what stops the next person re-opening it.

**What it should become.** The win-rate defect is a data-quality escalation in its own right — it is not a modelling choice, it is a system that has been quietly deleting the evidence a forecast needs. It belongs on the escalation list beside ESC-05, not only in a footnote on a source tab.

---

## FL-89 · Four questions that were all the same question

*"Do I need to remind you you're a top 1% investment banker building the revenue model?"* Four challenges followed. Each was a place where I had made something look finished instead of making it right.

### The tab was called History and coloured like a calculation

It is **Actuals**. That is what it is and that is what a banker calls it. And it should not be navy, because navy in this file means the model. The colour scheme now carries meaning rather than decoration: **navy the model, blue the assumptions — the only tab anyone types on, grey a supporting schedule built here, gold source data exactly as received.** Actuals is grey. It holds no judgement, takes no view, and should never be overwritten by hand. The legend is on the model.

### "Why is the price per court not exactly 89 in the actuals?"

Because the denominator was wrong, not the price.

The register said 1,602 courts in July. The meter billed 1,605. **Two clubs changed their court count mid-term and nobody wrote it back to the CRM** — Padel Zone Valencia went from 4 courts to 10 in January 2026, and Racket Center Miami ran 5 of its contracted 8 until April. Dividing revenue by the register gave 89.17 against a contracted 89.00, and 0.19% reads like rounding.

On the courts the meter actually billed, courts revenue is **courts x EUR 89.00 x FX, to the cent, every month from March 2026.** The 0.19% was two unmaintained contracts.

The model now carries both bases and reconciles them, which is what the question deserved: *Courts per the club register* — the commercial base — then *Contract amendments not written back*, then *Courts billed*, which is what revenue answers to. The reconciling line is 3 courts and it closes when someone maintains the register.

**And then January and February would not tie either**, at 88.86 and 88.36. Different cause, larger consequence. Courts were metered that had no billing to recognise against, so revenue was recognised **below service delivered**. Running it back: FY25 booked USD 645k of courts revenue against roughly **USD 803k metered at the contracted rate** — a gap that starts at 387 courts a month in February 2025 and closes to nil by March 2026. Courts revenue grows 191% on the reported basis and **34% on a service-delivered basis.** The reported figure is what the ledger says and is what the model compares against; the growth rate should never be quoted without the other. It also implies unbilled revenue that was never accrued, which is a question for the ledger owner, not a modelling adjustment. It sits on the FY25A cell as a comment and in note (8).

### "The plan should be as detailed as the revenue model"

It was one number a month, and I had written a note explaining that no segment plan existed — which is documenting a problem rather than fixing it. **No board plan is ever built as one number a month.** A plan is built stream by stream and the total is the *output* of that build. The single line is what survived the trip into the reporting pack.

So the plan now exists at the grain it was built at: eight streams, twelve months, footing to the published board file exactly in every month — the published total stays authoritative and is never restated. Every segment now carries Plan, Variance and Variance %, and prior year and growth beside them.

**The decomposition is the whole argument.** Total revenue is 3% behind plan, which reads as roughly on track. Underneath it: courts 4% behind, usage overage 15% behind, minimum true-ups 46% behind, events 25% behind — and player subscription 5% *ahead*. One number turned four different problems and one success into a rounding error.

### "Are we using best practice on the SaaS drivers?"

No, in two places, and both were material.

**ARPU was an assumption. It is now an output.** I had held blended ARPU flat at the July actual of EUR 10.76 and called it conservative. It is not conservative, it is wrong in a direction nobody chose: **every new subscriber arrives at 11.98 while the 9.34 and 5.95 cohorts churn away underneath.** Holding the blend flat assumes a mix that is demonstrably moving — and the actuals show it moving, 10.13 to 10.76 across seven months, which I had looked at and not seen.

The player section is now a three-cohort build: current price 9,481 accounts at EUR 11.98, legacy 4,477 at 9.34, promotional 1,070 at 5.95, each with its own churn rate measured from the roster (2.85%, 2.69%, 1.35% monthly). All additions land in the current cohort, because all of them do. Blended ARPU is calculated in both halves — derived from revenue in a closed month, weighted from the mix in a forecast month — **and the two meet at 10.76 in July**, which is the test that the cohort build is the same population the ledger billed. ARPU now rises to 11.11 by December because the mix says so.

**Club churn was a percentage that rounded to zero.** 0.15% a month on a base of 236 clubs is 0.35 clubs, which ROUND turns into nothing, every month, forever. B2B contract churn does not work like that: **a three-year contract cannot churn until it reaches renewal.** The driver is now a non-renewal rate applied to contracts *reaching renewal*, and the renewal calendar is a fact the register already holds — for forecast months as much as closed ones.

It changes what the model can see. **56 contracts carrying 371 courts reach renewal between August and December — 23% of the installed base up for decision inside five months.** A flat monthly percentage is structurally incapable of showing that. The rate itself, 4.4%, is 3 losses against 68 observed renewal decisions, which is thin and is labelled thin.

**And a key metrics block**, because a revenue model without one is a schedule. Recurring revenue in the month, ARR on the MET-009 basis with the exclusions named, month-on-month growth, net new subscribers, logo churn monthly and annualised — compounded, not multiplied by twelve — blended ARPU, clubs, courts billed, and revenue per court. The July ARR computes to USD 4,608,471.36, which is MET-009 to the cent: **the model and the metric registry agree without either being told to.**

> **Also superseded 18 Aug by defect 22.** The revenue model and `arr_schedule.csv` agreed to the
> cent because both read `actual_price_eur`, which SL-09 does not rule. Two instruments agreeing
> on the same wrong basis is not corroboration, and *the model and the metric registry agree
> without either being told to* is the sharpest example on this page of stopping at plausible.
> On the basis SL-09 rules, MET-009 committed recurring ARR is $4,743,222 at 31 July.

### What the four had in common

Every one was a place where I had stopped at plausible. A tab named for what it looked like instead of what it was. A price that was close enough. A comparison at a grain that made the variance unanswerable. And drivers that were conventional rather than measured, on a dataset where the measurement was sitting one tab away the entire time.

---

## FL-90 · "If you don't renew, you churn"

The reviewer's objection to splitting churn from non-renewal: they are the same thing. He is right about the outcome, and pressing on it exposed that my driver was built on the wrong numerator.

**The distinction is not the event. It is the population at risk and the month it can happen in.**

- *Mid-term termination* — a club walks away before the term ends. Can happen in any month. Population at risk: the whole in-term base.
- *Non-renewal* — a contract reaches its end and is not signed again. Can only happen at renewal. Population at risk: that month's renewal cohort.

Same customer, equally gone. Different hazard. A single monthly percentage on the whole base gets both wrong at once: **it spreads churn across months where the contract forbids it, and it thins out the months where the entire decision actually lands.** In a book of 12-, 24- and 36-month terms, churn is lumpy and scheduled, and the schedule is a fact the register already holds.

That is the defence of the split. Then I went to check the rate, and the rate was indefensible.

### All three losses were mid-term. There has never been a non-renewal.

| Club | Term | Ended | Natural expiry | |
|---|---|---|---|---|
| Racket Center Barcelona | 24m | 2026-02-28 | 2028-05-22 | 27 months early |
| Set Point Lyon | 24m | 2026-06-30 | 2027-08-16 | 14 months early |
| Break Point Madrid | 12m | 2026-05-31 | 2026-12-30 | 7 months early |

I had written a non-renewal rate of 4.4% as "3 losses against 68 renewal decisions". **Not one of those 3 was a renewal decision.** I had divided one quantity by an unrelated other and put the result on the assumptions tab with a basis that read like evidence. The correct count of observed non-renewals is **zero, in 93 recorded renewals.**

Which is a better modelling problem than the one I thought I had: **what do you assume for an event that has never happened?**

Not zero. An unobserved event is not an impossible one, and a forecast that books nil churn because none has occurred yet is asserting something the evidence cannot support. The answer is the **rule of three**: zero events in 93 trials puts the 95% upper bound at 3/93 = 3.2%. That is what the model carries — not measured, *bounded*, and labelled as bounded.

### Mid-term breaks are now nil by instruction, and the nil is visible

The reviewer's call: assume nobody breaks mid-term. Defensible — the contracts bind, and a model that forecasts contract breaches is forecasting counterparties behaving badly.

But it has a sharp edge worth stating: **it assumes away the only churn this book has ever taken, and forecasts the only kind it has never seen.** So the line stays on the model reading zero, directly beneath the actual months where it happened three times. A zero you can see is a decision. A line that was never drawn is an oversight, and they look identical in the output.

Both hazards then roll up into **club logo churn, annualised**, in the key metrics block — the single rate a board would be shown. Which is the reviewer's point, honoured where it belongs: one number for reporting, two drivers for forecasting.

### And the rounding absurdity that fell out of it

With ROUND on the formulas, the forecast showed **nil clubs lost beside twelve courts lost.** 0.32 clubs rounds to nothing; 2.03 courts does not.

The rule is now explicit: **round in the number format, never in the formula.** A weighted pipeline of 7.4 clubs and an expected 0.3 non-renewals are expectations, and rounding an expectation to a whole unit every month accumulates bias in whichever direction the rounding happened to fall — as well as producing that contradiction on the face of the sheet. Club and court lines carry a decimal; subscriber lines do not, because at fifteen thousand accounts the fraction is invisible. The arithmetic underneath is unrounded on both.

### One more thing the renewal calendar surfaced

Building the calendar meant computing each contract's term end from its current term start and term length, and comparing it to the end date the CRM holds. **They disagree on 22 active clubs** — all 24-month terms carrying one renewal, whose recorded end date sits exactly twelve months after the current term start. Either they renewed onto a 12-month term and the term field is stale, or the end date was never updated. Eight of them, 51 courts, fall inside the August-to-December renewal window.

It is disclosed on the Club register tab and it is not adjusted for. A question for whoever maintains the CRM, and the sort of thing that only becomes visible when you make the model recompute something the system already claims to know.

---

## FL-91 · "Even if they churn before the end, what do we care? We still get the money."

The commercial correction that collapsed a whole block of machinery.

I had built two churn hazards and defended the distinction. The reviewer accepted the distinction and then removed the reason for one of them: **a mid-term break does not reduce contracted revenue.** The contract is committed and the money is still earned. An early exit is a *collection* question — receivables, bad debt, the cash model — and it has no business in a revenue line at all.

That is not a simplification of my model. It is a correction of what my model was measuring. I had been treating a contracted B2B book like a consumer subscription, where leaving and stopping paying are the same act. In a contracted book they are two different events on two different statements.

So mid-term termination is gone entirely — not held at nil, gone. One line remains: **clubs lost at non-renewal.**

### And the renewal line stopped being overhead the moment it earned a second job

The reviewer's instruction on the renewal cohort was *remove it, it is over-complicated for no good reason* — followed immediately by *then having a different price for renewal would make sense. Having an upsell assumption would make sense.*

Which is the real point, and it is about **whether a line pays for itself**, not about complexity in the abstract. The renewal cohort was over-complicated when all it produced was 0.32 phantom club losses a month. The same line, doing two jobs, is the spine of the section:

- it is the **only population that can produce a loss**, because a club eleven months into a three-year term cannot leave in a way that costs revenue; and
- it is the **population that reprices**, because a rate changes when the contract is signed again and not before.

So the uplift phases through the calendar instead of stepping on a date somebody picked. 63 courts reprice in August, 359 of 1,766 by December, and the rest of the base stays on EUR 89.00 because that is what its contracts say. Blended price walks 89.00 to 89.54. **A model that steps the whole book at once is pricing contracts that are contractually fixed — the same error I had just been corrected for making with churn.**

The uplift is 3.0% and it is labelled as what it is: **a planned action, not an observed rate.** No price has moved in nineteen months and all 64 open opportunities are priced at 89.00, so this company is not pricing up today. Set the driver to nil and every price row reads 89.00 again, which is what they should read until somebody actually takes the decision.

### Upsell — the expansion line the company cannot see

Added as the reviewer asked, and it is the thinnest driver in the file, honestly labelled. **One upsell in nineteen months**: Padel Zone Valencia, 4 courts to 10. And the only reason anybody can see it is that **the meter disagreed with the CRM**, because nobody wrote the amendment back.

That is worth stating plainly rather than burying in a rate. A company that cannot see its own expansion cannot forecast it. The lever is there, held small, held visible — and the fact that its evidence had to be recovered from a reconciliation difference is itself the finding.

### What I keep learning from this reviewer

Three times now the correction has not been *your number is wrong* but **your line is measuring something that does not matter, or is measured against the wrong population.** Mid-term churn was arithmetically fine and commercially irrelevant. The 4.4% non-renewal rate was computed correctly from the wrong numerator. Blended ARPU held flat was internally consistent and directionally false.

None of those would fail a formula audit. All three would fail a conversation with someone who knows the business.

---

## FL-92 · "What does 'contract reaching renewal' even mean?"

The reviewer sent two reference models — a the reference take-home and a SaaS three-statement model — and one instruction: **new, expansion, churn. That's the right terms.**

He was right twice over, and the second one is the more useful lesson.

### First: those are the terms

Both reference models present recurring revenue the same way, and it is the way the entire industry does. The SaaS model's retention block is literally *Starting MRR / Less: Downgrades and Churn / Plus: Expansion / Final MRR*. The reference model is segments times ARPU with churn applied per segment. Neither contains a row called "contracts reaching renewal", because **that is a mechanism, not a movement.**

I had put my plumbing on the face of the model. A reader opening it saw the renewal calendar, the non-renewal rate, courts repriced cumulative — the machinery — and had to reverse-engineer new/expansion/churn out of it. The machinery was correct. It was also not what anybody wants to look at.

All three recurring segments are now MRR bridges:

    MRR, opening, EUR
      New
      Expansion — courts added at existing clubs
      Expansion — repricing on renewal
      Contraction — courts removed
      Churned
    MRR, closing, EUR

The renewal calendar still drives churn and repricing. It is now **inside the formulas**, with the explanation in a cell comment. Same arithmetic, and the reader sees the five things that moved.

### Second, and this is the real one: the residual found what no system records

Building the bridge meant deriving expansion in the closed months. There is no source for it — the billing system does not record an upgrade as an upgrade, which is exactly the gap SL-24 names when it rules NRR NOT COMPUTABLE. So expansion has to be a **residual**: the court movement the meter shows, less commissions, plus terminations.

Backed out that way it is **zero in seventeen of nineteen months, and non-zero in exactly two**:

- **January 2026: +6 courts.** Padel Zone Valencia, 4 to 10. **EUR 533 a month of recurring revenue that appears in no system as expansion.**
- **April 2026: −3 courts.** Racket Center Miami, 8 down to 5. A downgrade nobody recorded as one.

These are the same two clubs whose stale CRM records I had already found by reconciling the register to the meter. What is new is the *reading*. I had filed them as a data-hygiene defect: two records nobody updated. They are not that. **They are this company's entire expansion and contraction history, and the only reason anyone can see either is that a reconciliation difference refused to go away.**

A company that cannot see its own expansion cannot forecast it, cannot price for it, and cannot tell an investor what its net revenue retention is.

### Which makes the NDR number worth putting on the page

Net dollar retention on the courts book computes to **essentially 100%** — no meaningful expansion, no meaningful churn. That is not a disappointing number to be buried. It is the finding: **every dollar of growth in this book comes from new logos.** The SaaS companies quoting 120% are quoting an expansion motion this company does not have and, on the evidence of the expansion line, could not currently measure if it did.

It is stated on courts, where expansion and contraction can be recovered from the court movement, and **withheld on player subscription**, where SL-24 rules it not computable. A blended NDR across both would launder the gap into a number that looks measured.

### And the academy section grew a trend nobody has explained

Rebuilding academy on the same shape needed gross adds and churn, which meant looking at them for the first time. Adds run **57, 50, 42, 32, 21, 7** from February to July. Monotonic decay, no explanation. A twelve-month mean of 35 would forecast a level of demand the last two months contradict, so the driver is the trailing three. Churn is zero in 5,082 opening-months — the rule of three again, 0.06% a month.

Both are labelled for what they are. **The decaying adds line is the one driver in this model with a trend and no story, and it is worth a question before it is worth a better number.**

### The pattern, again

Three sessions running, the correction has not been about arithmetic. Here it was presentation — but presentation in the strong sense: **the model was arranged around how it was built rather than around what it means**, and rearranging it around the standard movements is what made a finding fall out that had been sitting in the file all along, filed under the wrong heading.

---

*Entries continue below as the trial proceeds.*

---

## FL-93 · "I feel pretty much everything is variable. What cost is really fixed in this?"

I had split cost of revenue into *variable with volume*, *variable with revenue and new business*, and *capacity and contractual*, then published a **contribution margin of 74.9%** against a gross margin of 69.1% and wrote a note calling the 5.7-point gap "the operating leverage in this business".

He read it and asked one question: *why is customer service not variable? The more clubs you have, the more support agents you have.*

He was right and the note was wrong. Contribution margin was excluding customer support **and camera depreciation** as if both were fixed. Depreciation is not remotely fixed — it is a straight function of the court estate, and the estate is the business. Taking those two back out:

| | |
|---|---|
| Gross margin | **69.1%** |
| Gross margin before platform hosting only | **71.0%** |
| Gross margin before hosting *and* support | **71.9%** |

**Operating leverage in cost of revenue is worth 2.8 points, not 5.7.** This business's cost of delivery scales with volume close to one for one, which is the truth about it, and the number I published said otherwise.

### But the interesting part was what "fixed" turned out to mean

Only one line is fixed by nature. **Platform hosting moved from USD 8,196 to USD 8,707 over nineteen months while the court estate went from 486 to 1,605** — 6% of cost for 230% of volume.

The support line looked fixed too. It is **USD 3,908.33 every single month, to the cent, for nineteen months.** A number that steady is either a fixed cost or a stale allocation, and the two look identical in a ledger.

It is neither, quite. Going to the headcount file: **customer success has been two people the entire time.** 3,908 is 35% of their payroll (MET-016), and the allocation is correct. What has changed is what those two people carry — **78 clubs when the line was struck, 236 now.** Support cost per club has fallen from USD 50 to USD 16.56 not because the company got efficient but because it has not hired.

So the line is flat, and its flatness is not an economic property. **It is a capacity limit that has not broken yet**, sitting in the accounts wearing the costume of a fixed cost. The regrouping now says *flat in the ledger* rather than *fixed*, and the note says why.

### The lesson

Variable-versus-fixed is not a category you can assign from the account name. It is a claim about behaviour, and behaviour is testable against the ledger in about four lines of arithmetic. I asserted the split instead of measuring it, and a CFO caught it by asking about the one line where the assertion was obviously wrong.

---

## FL-94 · "This retention window is complicated and not needed, correct me if I'm wrong"

Storage was the one cost line not forecast per match analysed. It is driven by the *stock* of video still under the twelve-month retention window, which needs a rolling add-this-month-drop-the-twelfth calculation on the face of the model. He wanted it gone.

The test is whether the two bases behave differently. They do, and it is not close:

| | Jan 26 | Dec 26 | drift |
|---|---|---|---|
| Storage per **match analysed**, USD | 0.1232 | 0.1550 | **+26%** |
| Storage per **match still stored**, EUR | 0.0134 | 0.0142 | +6% |

The price list has not moved. What moves is the ratio of stored stock to monthly flow — **8.0x today, climbing toward 12x at steady state as the estate matures.** A cost-per-match-analysed forecast either holds the rate and understates storage by a quarter, or grows the rate with an assumption nobody can defend.

So the window stays — but he was right about where it was. It was sitting in the middle of the cost lines making the reader do the mechanism before they got the margin. It now lives in **section III, Cost drivers**, and section II makes the case for it visibly: storage is the one line whose cost per match analysed climbs while every other line holds or falls.

**The challenge was worth taking even though the answer was no.** It moved the mechanism out of the reader's way and produced the one exhibit that justifies it.

---

## FL-95 · "One thing missing from cost of revenue is internal-use software"

He was right, and the gap was larger than a missing line.

Every dollar of engineering payroll was expensed to R&D. Nothing in the ledger recognised that a material part of it builds durable features the platform then uses to deliver the service for years. Two errors, pointing in opposite directions, in the two numbers investors and boards actually read:

- **Cost of revenue was understated**, because the asset that delivers the service was not being consumed anywhere in the accounts.
- **R&D was overstated**, because it carried the cost of building things that are not research.

### The classification is not the obvious one

This is the part worth writing down. Instinct says software a SaaS company sells is **ASC 985-20** — software to be sold, leased or marketed. It is not. The customer never takes possession of it; they access a hosted service. That makes it **internal-use software under ASC 350-40**, which is the standard treatment across SaaS and the reason SaaS gross margins carry a software amortisation line at all. Under IFRS the same spend is development cost under **IAS 38** once the six criteria are met — same outcome, different trigger.

### Three stages, and only the middle one is an asset

| | |
|---|---|
| **Preliminary project** — scoping, evaluating alternatives, selecting a design | expense |
| **Application development** — coding, configuration, testing, installation | **capitalise** |
| **Post-implementation** — training, maintenance, bug fixes, production support | expense |

Capitalisation stops when the asset is **ready for its intended use**, which is also when amortisation starts — not when the team stops working on it. That distinction is where most companies get it wrong, and it is the defect the demonstration instance now carries.

### And not all of a person's month qualifies

His instruction: *not all of one employee's hours is capitalisable — he goes to meetings, not capitalisable; he's coding or designing, capitalisable.* Exactly so, and it is the judgement the whole standard turns on. Standups, planning, interviews, on-call and production support are not development.

So the capitalisable share is a per-person, per-project assumption agreed between engineering and finance, and it sits on the face of the artefact rather than inside a script. The rate it is applied to is the **fully charged** cost — base plus the employer burden that goes with the contract, 31.2% on an EOR contract and 11.8% on US payroll. Base pay alone understates the asset by the burden, which is a third of it.

### What got built

Four projects, four new accounts, two new source exports, three new tabs.

| | |
|---|---|
| **IUS-001 Match highlight reels** | in service Sep 2025 · USD 129,506 |
| **IUS-002 Club booking and court scheduling** | in service Jan 2026 · USD 107,735 |
| **IUS-003 Player ranking engine v2** | in service Apr 2026 · USD 125,875 |
| **IUS-004 Coach analytics workspace** | in development, expected Sep 2026 · USD 203,281 |

The ledger now carries `Dr 1550 Capitalised software / Cr 6010 R&D salaries` monthly, and `Dr 5070 Amortisation / Cr 1595 Accumulated amortisation`. The **Employees** tab prices the roster fully charged from two burden assumptions. The **Software projects** tab holds the register and the allocation, with the fully charged rate green-linked per row to Employees. The **Capitalised software** tab is the schedule: capitalised by project by month, amortisation by project, and the asset roll-forward.

Nothing on the schedule is typed. Cost comes from the allocation, the allocation is priced off the roster, and the life and the in-service date come from the register.

### What it does to the numbers

**FY26 gross margin falls from 69.1% to 66.5%.** Software amortisation is USD 141k of cost of revenue — 2.6 points of margin that were not being charged anywhere. USD 434k of net book value appears on the balance sheet. R&D falls by the capitalised labour.

That is the honest version, and it is worse-looking than the one I had published. It is also the version that survives a diligence question, which the other one would not have.

### The defect it plants

**IUS-001 carries USD 24,633 capitalised in the three months after it was placed in service.** Post-implementation cost, capitalised. It is the single most common IUS error in practice, it is invisible in the ledger — the entries are identical to development-stage entries — and it is visible on the allocation the moment the stage column is read against the in-service date.

That is the whole argument for the tab. The GL cannot tell you this. The register and the in-service date can, and nobody looks at them because they live in engineering's spreadsheet.

### One thing I decided rather than assumed

The project register stops at IUS-004, so on the register alone capitalisation falls to zero from September and the asset stops growing. That would read as a forecast, and it is not one — engineering does not stop when the last scoped project ships. The forecast carries the run rate on a row called **Projects not yet scoped**, and it amortises nothing, because an unscoped project has no in-service date. A visible assumption beats an invisible cliff.

**SL-30** now rules the whole thing: what qualifies, whose time, at what rate, where the amortisation goes, and why one 36-month life applied to every project is a policy rather than an estimate.

---

## FL-96 · The capex schedule, and the asset class nobody had bought

*"Now let's move on to the capex sheet. Pretty straightforward."*

It was, except for one thing found on the way in.

### A 33-person company with no computers on the balance sheet

Before building the schedule I listed what this company owns. Cameras, and capitalised software. That is the whole fixed asset book — and it cannot be, because thirty-three people are working on something.

**Nothing in the ledger buys a laptop.** Not capitalised, not expensed, not anywhere. That is a generator gap dressed as an accounting fact, and it is exactly the FL-82 failure: *a sheet is finished when a knowledgeable person cannot name something that should be on it and is not.* A capex schedule for a Series A software company with no IT equipment on it would have been the first thing anyone asked about.

So IT equipment is now real: a workstation per person at USD 2,400 on their start date, 36-month life, with an opening balance for everyone who joined before the ledger opens. **Accounts 1510 and 1591, and the charge goes to 8090 — G&A, not cost of revenue.** Workstations are issued to everybody, not to the service, so the line never touches gross margin. That distinction is the one thing on this schedule somebody could get wrong in a way that moves a headline number.

### Then the schedule found its own answer

**No camera is bought in FY26.**

That is not a modelling shortcut, it is what the book says. Camera capex is nil in every closed month of 2026 — because the November 2025 bulk purchase left **USD 127k of cameras in inventory**, and every court the pipeline delivers between August and December costs **USD 65k** of stock. An install is a transfer from inventory to the depreciating asset, not capital expenditure.

Which is why section I is titled *capital expenditure* and reads nil on the largest hardware class, while the asset class table underneath shows inventory drawing down from 127k to 62k. A capex sheet that showed "camera capex" equal to installs would have reported USD 65k of spend that is not going to happen.

### The forecast comes from the same places everything else does

| | |
|---|---|
| Cameras | the weighted sales pipeline — a list of named clubs, not a growth rate |
| IT equipment | one workstation per new starter, on the hiring run rate |
| Software | the run rate, because the register carries nothing past IUS-004 |

And the software amortisation is built **per project off the fixed asset register**, so it steps in September when IUS-004 goes live. That is the same USD 16,418 the revenue model's Gross margin tab carries, reached from the same register by a different formula in a different workbook — and the verifier now checks the two agree, month by month, along with camera depreciation.

### One design decision worth recording

The capitalised software rows appear in `fixed_assets.csv` as one asset per project at total cost. That works because a project's cost pool is complete before it is placed in service — every project except IUS-001, whose post-implementation tail is the planted defect, and whose extra cost landed in 2025, outside this schedule's window. Inside FY26 the static register and the month-by-month build agree to the cent, which is why one file can drive both workbooks. **State that limit rather than discover it later:** the day a project capitalises after going live *inside* the reporting window, the register stops being sufficient and the capex sheet has to read the allocation like the revenue model does.

### What it looks like

FY26 capital expenditure **USD 438k**, of which software is 94%. Depreciation and amortisation **USD 310k**, of which **USD 282k is cost of revenue** and USD 27k is G&A. Net book value closes at **USD 977k**, against USD 849k opening.

**A hardware company that has stopped buying hardware and spends 94% of its capex on engineering time is a software company.** The schedule says that in four lines, and nothing else in the pack said it at all.

---

## FL-97 · "This is not good at all. And frankly lazy."

Four corrections, and he was right on all four. The one that stings is that three of them are the same mistake: **I put an assumption where a schedule belonged.**

| what I did | what it should have been |
|---|---|
| One 36-month life for every software project | A life per project, on the register |
| `New starters a month, forecast = 1` | The hiring plan — named roles, planned start dates |
| The IUS build in the revenue model, a second copy in capex | One build, in capex, read by both |

The camera line survived, because it was built the way the others should have been: a driver (courts commissioned) times a rate, with the driver coming from the pipeline.

### The pattern

A run-rate assumption is what you write when you have not gone to look for the schedule. It is cheap, it is defensible in a sentence, and it is **exactly what a model is supposed to replace.** "One a month" is not a hiring forecast; it is a refusal to open the requisition list. "36 months for everything" is not a useful life; it is a refusal to ask engineering how long a ranking model lasts.

Both were on the assumptions tab in blue, labelled with a basis, looking like decisions. That is what made it lazy rather than merely incomplete — **the presentation gave them the authority of a judgement when nobody had made one.**

### What moved

**All internal-use software is now in `capex_FY26.xlsx`.** The project register, the time allocation, the roster it is priced off, and the per-project amortisation — section IV of the capex schedule. The revenue model lost three tabs and gained one: the fixed asset register, which its Gross margin tab now reads for the software amortisation forecast.

**Useful lives vary and the variation matters.** 24 months on the player ranking model — models get superseded — 48 on the booking engine, 36 on the other two. That is a USD 148k FY26 charge against USD 141k on the flat-36 version, and the monthly shape is different: IUS-003 amortises at USD 5,245 rather than 3,497.

**Workstations come off the hiring plan.** Eight approved requisitions with roles, locations, salaries, planned start dates and a reason each. One in August, two in September, and so on — the forecast steps, because hiring steps.

### And the headcount model, which is the one he actually asked for

`headcount_plan_FY26.xlsx`. Four sections: how many people and where they sit, what they cost fully charged, **where that cost lands in the P&L**, and the tie to the ledger.

Section III is the one worth defending. A payroll report tells you what people cost. It does not tell you that **USD 411k of it is capitalised to an asset** and **USD 70k is allocated into cost of revenue** — two decisions that move gross margin and appear in no payroll system. Both now sit on one page and foot to the total.

Two of the eight open requisitions are customer success, and the model shows what that does: the cost-of-revenue allocation steps from USD 3,908 to 7,745 in August and 9,811 by December. **The line that has been flat for nineteen months because two people covered a trebling club count stops being flat the moment the plan lands.** That is the first time that finding has had a number attached to the other side of it.

### The bug the reconciliation found on its first run

Section IV compares people cost per the roster against people cost per the ledger. It came out USD 1,958 apart in January — and USD 1,958 was exactly that month's EOR platform fee.

**The generator was charging the EOR's platform fee twice**: once inside the salary pot it allocates across R&D, S&M and G&A, and again on its own line to account 8020. About USD 2k a month, USD 40k over the dataset. Not a planted defect — a real arithmetic error that had been in the book since the first build and that nothing else in the pack could see, because every statement still balanced.

Fixed. The reconciliation now reads **nil in every closed month but one**: April, USD 8,400 — the separation charge buried inside the EOR invoice, which is not a cost of anybody who works here. That is the edge case the dataset plants, surfaced as a single number by a check that exists for a different reason.

**A reconciliation you build because it ought to be there finds things you were not looking for.** That is the second time this week — the processor fee was the first.

---

## FL-98 · "So we start having different FX assumptions in each spreadsheet. It's not gonna work."

Seven corrections on the two new workbooks, and one of them is architectural.

### The FX rate was in three files

`EUR/USD forecast = 1.1254` was typed on the revenue model's Assumptions tab, again on the capex Assumptions tab, and would have been typed a third time the moment any other model needed it. Same for the employer burden, the camera cost, the stage probabilities.

**The second time a number is typed, one of the copies is already wrong and nobody knows which.** It is the single most common way a pack of models stops agreeing with itself, and it never shows up as an error — every workbook still recalculates cleanly.

`global_assumptions.csv` now holds thirteen shared parameters, each with a **named owner**: FX and the two lives sit with Finance, both employer burdens and the EOR fee with People & Ops, the camera cost with Field Operations, the four stage probabilities with Club Sales. Every workbook carries the file on a **Global assumptions** tab and links to it. On the revenue model's Assumptions tab those rows are now **green rather than blue** — which is the convention doing exactly what it exists for: green means the number came from somewhere else, so you can see at a glance which assumptions this model owns and which it inherits.

A verifier now reads all three workbooks and asserts every shared parameter is the same number in each. It is the cheapest check in the pack and it protects the thing hardest to spot by eye.

### "The master headcount lives with HR"

His framing, and it is the right one. The capex schedule had a full **Employees** tab — a copy of the roster, salary by salary. That is not a model reading another model, it is one model owning a second copy of somebody else's master file.

It is replaced by **From HR**: an extract, not a copy. Two small blocks — starters by month, and the fully charged monthly cost of only the eleven people who appear on a capitalised project — stamped with the source files, the owning function, and the model that maintains them. The headcount workbook gets the symmetric **From capex** tab for the capitalised-software line.

**An extract carries values, the way the ledger tab does.** The formulas live in the model that owns the data; what crosses the boundary is a summary with its provenance on it. That is also how it works in a real company, where finance does not get write access to the HRIS.

### The other five

**The 32k flat capitalisation is gone from both files.** It was a run-rate standing in for a plan, twice — exactly the thing corrected in FL-97, left in two places. Capitalisation now stops after August because the project register stops at IUS-004, and the tab says so: *nothing beyond it has been scoped, and a run rate here would put an asset on the balance sheet nobody approved.* A visible nil beats an invented number.

**"Pipeline, stage weighting" was a label nobody could parse.** He guessed it meant a capitalisation rate per stage. It is the probability a deal at that stage closes, and it is now called that — **Probability of close — Discovery**, and so on — with the honest basis attached: convention, not calibrated, because the CRM holds 246 won against 1 lost and stage conversion cannot be measured from it.

**The employer burden cell was green and should not have been.** It is `IF(contract = EOR, x, y)` — a formula, not a link. Green means *this figure came from another tab, unchanged*. An IF that chooses between two links is a calculation and reads black. Small, and it matters: a convention that is nearly followed carries no information at all.

### What this round was really about

Four of the seven corrections are the same class as FL-97's: **a value living in two places, or a value standing in for a schedule.** The difference is that this time the duplication was between workbooks rather than inside one, which is harder to see and much harder to fix later.

The rule that came out of it, and it is now enforced by a check rather than by discipline: **a number is typed once, in the file whose owner is accountable for it, and every other model links to it or receives it as a stamped extract.**

---

## FL-99 · "The one who's hiring these people should know what project they'll be working on"

Four comments on the capex workbook. Three are tidying. The fourth is a design idea better than the one it replaced.

### The comment that was not critical

*"Typed here and nowhere else — a green cell in any workbook is reading one of these."* True, and nobody needs telling. It was a sentence explaining a convention to a reader who can see the convention working. Deleted, along with the tab's footer to a single line.

**The rule, again:** a note earns its place by carrying something the sheet cannot show. Explaining how the sheet works is not that.

### One Assumptions tab, in the model's colour, holding only what the model uses

The tab was called *Global assumptions* and listed all thirteen shared parameters in every workbook — including the ones that workbook never touches. His correction is right on both counts: it is the **Assumptions** tab, it is part of the model rather than a source, so it carries the model's colour, and it shows the parameters this workbook actually uses and nothing else.

Capex shows eleven, headcount shows four, the revenue model folds its seven into the single tab it already had. Every one still comes from `global_assumptions.csv`, and every one carries the function that owns it.

### The roster and the hiring plan were the same list

*"I think the Hiring plan tab should be the headcount tab including existing headcount, people already hired, and future hired."*

Correct, and it removes an abstraction I had invented one round earlier. **From HR** — my extract tab — is gone. There is one **Headcount** tab: everybody on the payroll and every approved requisition, on one list, with the same columns, distinguished by a status column. Both workbooks render it from the same module, so they cannot disagree about who is on the payroll in November.

A roster and a hiring plan are the same list at two points in time. Splitting them makes every model that needs people do the union itself, and the two halves drift.

### And the idea that was better than mine

*"In the SW projects tab, we should have included future hires as well. The one who's hiring these people should know what project they will be working on and their cap assumptions for each."*

This is the answer to something I had got wrong twice. First I put a **USD 32k a month run rate** on the capitalisation forecast — corrected in FL-97 as an assumption standing in for a schedule. Then I removed the run rate entirely, and capitalisation fell to nil from September, which is not right either: engineering does not stop.

The right answer is neither. **A requisition is approved for a reason, and the reason is a project.** So the time allocation now carries open requisitions alongside employees — REQ-043 Backend Engineer at 70% from September, REQ-044 ML Engineer at 75% from October, REQ-048 Product Designer at 60% from December — on **IUS-005 Club performance benchmarking**, staffed alongside the two engineers who come free when IUS-004 ships in August.

That produces a capitalisation forecast that is a **plan with names on it**: USD 118k in FY26, rising as each hire lands, with nothing amortising because IUS-005 does not go into service until March 2027. Three attempts, and the third one is the only one that could survive somebody asking *who is doing this work?*

**The general lesson, and it is the one this whole trial keeps teaching:** when a forecast needs a number nobody has, the answer is almost never a rate. It is a list somebody in the business is already keeping — a requisition list, a project register, a renewal calendar, a pipeline — and finance's job is to find it and join it to the ledger.

---

## FL-100 · "The headcount sheet is missing a lot of elements"

Commission, benefits and stock comp. He is right that a headcount model without them is a salary schedule, and the three of them together are **USD 584k of FY26 people cost** that was not on the page.

### What the model was measuring, and what it should have been

| | |
|---|---|
| **was** | base salary × (1 + employer burden) |
| **now** | salaries and burden · benefits · sales commission · employer platform fees = **cash people cost** · plus share-based compensation = **total people cost** |

FY26: salaries USD 4.64m, benefits 189k, commission 58k, platform fees 28k, and **share-based compensation 353k**. Four new tabs behind them — Commission, Benefits, Equity, Cap table — plus a Pipeline tab, because the commission forecast needed one.

### The instrument question, which he asked and which changed the build

*"RSU with vesting period, PRSU with vesting period and goal attached to it — or maybe stock option for startup. I'm just not sure how it works exactly."*

At Seed to Series A it is **options**, and it is not close. An option carries a strike set to the 409A fair market value on the grant date, so it is worth nothing unless the company is worth more later. An RSU has no strike, so it has value the day it vests — which on an illiquid private share creates a tax bill on paper nobody can sell. That is why RSUs start around Series D and are almost always double-trigger.

The accounting distinction is the one that matters for the model: the charge is the **grant-date fair value of the option**, not the share price. Black-Scholes at 55% volatility and a six-year expected term values an at-the-money grant at about **56% of the strike**. A 35,000-share grant at USD 2.60 is a USD 51,121 charge, not USD 91,000.

And **the PRSU idea earned its place**, because the accounting is genuinely different: a performance award is expensed only while the outcome is judged **probable**, and the whole cumulative catch-up lands in one month when that judgement flips. So there is exactly one in the book — 120,000 options to the CEO on reaching USD 6.0m committed ARR by end-2027, assessed **not probable**, recognising nothing. It is in no account and on no statement, and it is real dilution.

### And the cap table he suspected was needed

*"It means we might need a cap table sheet somewhere as well."*

He was right, and for the reason that makes it worth building: the only question anyone asks about an option plan is **how much pool is left**. Building it answered that immediately.

**1,928,000 options granted against a 1,600,000 authorised pool. Over by 328,000 shares.**

Granting past the pool is one of the commonest things a company discovers in its next round's diligence, and **nothing in a payroll report, a P&L or a balance sheet would ever show it** — the expense is right, the equity is right, the pool is a board authorisation that lives in a minute book. It took a cap table with one subtraction on it.

### The bug the commission plan found

A commission plan needs to know who sold the deal. **The CRM records the owner of all 311 opportunities as "Club Sales"** — the department. Not one names a person.

That is not a modelling inconvenience, it is a system that cannot run the compensation plan built on it. Ownership is now assigned to the rep who was live on the signature date, and the assignment is stated as an assignment rather than smuggled in as data. It also fixed the revenue model's pipeline tab, where "owner" had been a column with one value in it for four reviews and nobody — me included — had asked what it was for.

### The one that will move gross margin

The 35% customer support allocation is struck on **base salary only**. It excludes the employer burden, benefits and share-based compensation — so the cost of revenue is understated by the support team's burden and benefits on 35% of their time, and gross margin is overstated by the same. Small today at two people. Not small when the plan's two customer success hires land, which is why the allocation has to be re-struck on a fully charged basis rather than re-struck on the same wrong base.

---

## FL-101 · One alias out of thirty-two, and the two rungs that were rejected

Doc 71 asked for alias lists on registry entries so free-form phrasing reaches a
registered metric. The obvious build derives them mechanically from the ruled
name. I built that, ran it over 32 entries, and it put an alias on 29 of them in
about a second.

Then I read them.

`AIURR`. `RVCCS`. `CRAW`. Nobody has ever said those out loud. That was the
harmless failure. The dangerous ones were `CR` for *Committed revenue*, `ER` for
*Expected revenue*, and `LC` for *LTV : CAC* — because **`CR` is credit in most
of finance before it is anything else, and `ER` is an exchange rate.** An alias
that is a common abbreviation for a different thing does not fail to resolve. It
resolves, confidently, to the wrong entry — which is precisely the error the
resolver was built to prevent, arriving through the resolver's own front door.

The second rung looked safer and was not. Stripping a unit suffix turns "Runway
months" into "Runway", which is fine, and turns **"Deferred revenue days" into
"Deferred revenue", which is a balance-sheet line** — a completely different
object that anyone asking for it would cheerfully accept as an answer.

Nothing mechanical separates those two cases. So the initialism rung was deleted
outright, and the word-removing rung was demoted from *written* to *proposed*.

What survives writes exactly one alias across the whole registry, and the rest
of the output is a confirm list. Three word-removing candidates: two ruled in,
one ruled out, by a person, in about four seconds — which is the correct cost of
that decision and it was never the tool's to make.

**The generalisable bit:** an alias is a pointer with no meaning of its own, so
it *looks* like the kind of thing a machine can generate. What it actually is,
is a claim about what people in this company say when they mean this metric. The
package can restate a ruled name. It cannot know a vocabulary, and a
manufactured one is worse than an empty column because an empty column refuses.

---

## FL-102 · Two engines that only run on one company

The standing check is a grep: `package/` must contain no trace of the
demonstration company, because `package/` is what ships. It has passed every
time it has been run.

It passed on vocabulary. It has never been run against *behaviour*.

`variance.py` reads `customers_clubs.csv`, `customers_players.csv` and
`customers_academy.csv` **by literal filename**, bypassing `mapping.json`
entirely, and hardcodes those three as the segment list. `kpi.py` reads
`customers_players.csv` the same way. Every other engine in the package goes
through the mapping.

On any other company those two engines find no files and produce nothing —
**silently**, because a missing optional file is a legitimate state everywhere
else in the package. The install would look successful. Two outputs would simply
never appear, and the one person who would notice is the one who does not yet
know what they were supposed to see.

Two things worth keeping from this.

**A portability check that only reads strings is checking the wrong layer.** The
company's name is not in those files. The company's *file names* are, which is
the same dependency wearing a costume that greps do not catch.

**The failure is silent because of a good rule.** Optional inputs degrade
gracefully rather than crashing — correct, and the reason a hardcoded path
inside a graceful degradation produces nothing instead of an error.

Filed rather than patched: the fix is that segments come from the mapping as a
declared block, and that changes a contract. A contract change gets its own
ruling, not a commit at the end of an unrelated build.

---

## FL-103 · A hundred and forty-nine months of runway

The portability harness was built to prove the package installs at a company it
was not written for. It did that. It also found two numbers that have been wrong
on the demonstration company since they were first produced, and the second one
is the kind you do not want found in a diligence room.

**The forecast's plan-headcount scenario reported 149 months of runway. The real
answer is 20.4.**

The mechanism is three lines long. Planned headcount was assembled by walking
the data directory for every file whose name began with `plan_`, reading each
into one dictionary keyed on version and period. Six files match that prefix.
Two are plans. The other four are the cost-centre split, the COGS detail, the
line detail and the driver file — and every one of them carries a `plan_version`
and a `period` column, so every one was swept in and treated as a plan.

Last file to mention a period wins. Sorted alphabetically that is the driver
detail: 456 rows, one per driver per period. The headcount the forecast planned
against was whichever driver row happened to sort last. Salary cost came out
near zero. Cash lasted twelve years.

Two more from the same idiom, which appears three times in the package: the
board pack cover printed its plan comparator as **"FY26 Board Plan ()"** with a
blank vintage, because it took the version from the cost-centre split, which has
no plan date. And `plan_reconciliation.csv` carried 150 rows across three
phantom plan versions, one of them the same plan twice with different dates.

### Why nothing caught it

Every check in the project was pointed somewhere else, and each one was pointed
there for a good reason.

The **tie-out suite** checks that outputs agree with the ledger. A forecast is
not in the ledger; there is nothing for it to disagree with.

The **answer key** covers the close, the statements and the schedules. It does
not cover a scenario projection, because a scenario is a judgement about the
future and an answer key is a record of the past.

The **portability grep** looked for the company's name. `plan_` is not the
company's name.

And the number itself never looked wrong in the one place a person would see it,
because nobody reads a scenario table looking for an implausible runway — they
read it looking for the runway. **149 is not a number you check. It is a number
you are relieved by.**

### The bit worth keeping

The harness that found it was not looking for it. It was looking for filename
dependencies, and a filename dependency is what this was — the plan was
identified by a naming convention rather than by a declaration, and a naming
convention is a rule with nothing enforcing it.

Which generalises: **discovery by convention is the same bug as a hardcoded
path, one level of indirection later.** `"plan_fy26_board.csv"` is obviously
unportable. `startswith("plan_")` looks like flexibility and is the same
dependency with a wildcard on the end — it is unportable *and* it is
unpredictable, because now any file anyone drops in that directory becomes an
input. The hardcoded version at least fails loudly at the next company. This one
produced a number every month.

---

## FL-104 · Three false positives, and one thing the harness still cannot see

Three of the harness's early findings were the harness's own fault. Recording
them because a check with a standing false positive gets switched off faster
than a check that misses things.

**It rewrote its own scrambled names inside SHA-256 digests.** Directories were
named `d01`, `d02`; `d02` occurs inside hex. Two identical workbooks came back
different. Every generated name now begins with `z`, which is not a hex digit.

**It rewrote the word "data" inside prose.** The mapping was scrambled by blind
text replacement, and the data directory is called `data` — so every occurrence
of that word in the mapping's own comments was rewritten. One of those comments
is quoted verbatim onto a worksheet, which is where it surfaced: a board pack
driver note reading *"the consequence of believing the zdir19"*. The harness had
corrupted the instance and then reported the engine for it.

**It could not tell a declared filename from a held one.** An engine reading a
name the *instance* wrote in its mapping is behaving correctly; a different
company writes a different mapping and it finds their file. Only a name the
*engine* holds is a bug. Until the harness learned that distinction it was
reporting correct behaviour as failure — which is the fastest possible way to
make a portability check worthless, because the first three things you look at
are all fine and you stop looking.

### And the limit, which is structural

**The harness compares the scrambled run against the control run, so a fault
present in both is invisible to it.**

This is not hypothetical. Midway through the conversion I rewrote the
`customers` block in `mapping.json` and dropped its column renames, breaking the
contract's `customer_id` and `name` fields. The harness reported PASS. Both
sides were equally broken, and equal is all it measures. What caught it was the
before-and-after snapshot against the original outputs — a different check,
answering a different question.

Two checks, two questions, and neither substitutes for the other:

- *Does it find my files?* — the harness, control against scrambled.
- *Did the numbers move?* — the snapshot, before against after.

A refactor needs both, and I would not have known that this morning.
