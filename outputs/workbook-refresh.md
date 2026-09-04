# Build once, refresh forever — the workbook-refresh pair

*Built 4 Sep 2026 on the Arcline instance. `modelbuild.py` ran once;
`workbook_refresh.py` is the only program that has touched the model since. The
model, its versions and its log live in the private instance; this is the record
of the build and its first session.*

Every other workbook in the instance is rebuilt by its engine each period. This
pair is the opposite experiment: a three-statement model constructed a single time
— plan written at birth, statement tabs formulas-only, five tie-out checks rolled
into a `CHECK_TOTAL` the workbook computes about itself — and then only ever
REFRESHED. The manifest emitted at birth is the contract: which named ranges are
writable, from which sources, under which gate, and which checks must hold after
every write. Which cells are yours to write is a governance artifact, not a
convention.

## The six guarantees, in enforcement order

1. The writable range exists and contains no formula — a formula inside a writable
   range means model and manifest disagree, and the write refuses.
2. The period is closed. A trial balance without closing balances, or carrying an
   open-month note, refuses by name rather than landing provisional numbers that
   look final.
3. Sources bring exactly the keys the model was born with. A new FSLI is a model
   revision, not a refresh.
4. Formulas are fingerprinted before and after. Owner edits are disclosed in the
   log, never silently absorbed and never reverted — it is the owner's model.
5. The write lands on a temp copy, a real spreadsheet engine recalculates it, and
   the workbook's own CHECK_TOTAL must be zero with MONTHS_CLOSED advanced by
   exactly one. Only then does the temp replace the model; a failed check leaves
   the model byte-identical to before.
6. Every refresh and every refusal appends to the log with source-file hashes, and
   every landed version is archived whole. The history is the artifact.

## The first session

Refresh 2026-01 LANDED: v2, 42 cells written, CHECK_TOTAL 0.00, one month closed.
Formula cells across v001 and v002: 653 and 653, zero changed — preservation shown
by diff, not promised. Refresh 2026-02 REFUSED by name: the open month's trial
balance carries no closing balance and says so. Re-refreshing 2026-01 REFUSED: the
months-closed guard will not let an already-closed month land twice.

And the first run's refusal found a data truth before the artifact existed to
protect: CHECK_TOTAL failed at exactly opening cash, which unmasked that the FY2026
trial balance carries year-to-date movements with no opening balances — closing
balance-sheet positions must come from the balance-sheet export, which balances to
the cent once its embedded subtotal rows are excluded. The model was reborn from
the right parent, and nothing ever landed while wrong.

## Honest scope

The mechanism is proven on a model born with a manifest. The customer case — a
workbook this package did not build — needs the retrofit: a manifest authored
against an existing file, agreed with its owner, signed like a ruling. The engine
would not change; the manifest workshop is the work. Guarantee 4's drift
disclosure is coded and fingerprint-verified but not yet exercised in anger; it
waits for a closed March and a deliberate owner edit between refreshes.
