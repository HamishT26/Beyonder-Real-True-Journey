# GHC Family Method Flow State

- Phase: v644-gmut-thos-v6-x1-x2
- Owner: Ilyra Fen
- Methods: 9
- Passing witnesses: 8
- Failed witnesses retained: 0

## Preferred methods

### V6446-M02 — Bounded command envelopes for large repository inspection

- Trigger: large D-first working tree; Git status or Python startup; multiple inspections sharing one short envelope
- Method: Split inspections by purpose, suppress unnecessary untracked enumeration where appropriate, and use a measured sixty-second ceiling without weakening the underlying check.
- Recurrence guard: Use single-purpose commands and an envelope above the observed scan duration; never promote a timed-out batch as evidence.
- Rollback: Discard only the incomplete command result, retain its negative receipt, and reread authoritative Git or runner state directly.
- Witnesses: V6446-M02-W01

### V6446-M03 — Literal PowerShell patterns for bounded ripgrep inspection

- Trigger: PowerShell command composition; regular expression with quote-like JSON syntax; multiple patterns embedded in one shell string
- Method: Use a literal single-quoted ripgrep pattern and one bounded target file per structural inspection.
- Recurrence guard: Keep regular expressions literal in PowerShell and avoid nested JSON quotation in composite commands.
- Rollback: Retain the parse failure, make no file change, and retry the read-only query with literal quoting.
- Witnesses: V6446-M03-W01

### V6446-M04 — State-aware Method Flow witness promotion

- Trigger: Method Flow candidate method; passing witness registration; caller assumes witness and validated transition are separate; state operations batched before returned state is inspected
- Method: Record one witness, inspect its returned method_state, and request preferred only when the witness has already produced validated.
- Recurrence guard: Do not batch witness and redundant validated transitions; branch the next operation on the runner's returned state.
- Rollback: Retain the rejected transition, leave the witness and current valid state intact, and issue no compensating edit to the append-only ledger.
- Witnesses: V6446-M04-W01

### V6446-M05 — Dual-key inherited source-ledger deduplication

- Trigger: recursive inherited source ledger; official specification with multiple stable URLs; candidate comparison limited to URL identity
- Method: Recursively decode the full inherited ledger and compare both normalized titles and canonicalized URLs before assigning a new source ID; reuse the inherited ID when either identifies the same source.
- Recurrence guard: Require zero duplicate normalized titles and zero duplicate canonical URLs for every added source slate.
- Rollback: Remove only the uncommitted duplicate additions, preserve the failed builder receipt as a negative, and keep inherited ledger rows unchanged.
- Witnesses: V6446-M05-W01

### V6446-M06 — Direct writer map and deferred self-output gate

- Trigger: generated exact-file list; terminal validation writes after presence calculation; expected receipt names inherited without direct writers
- Method: Give every expected non-self artifact a direct writer and exclude only the explicitly named terminal validation JSON and Markdown outputs from the prewrite presence gate.
- Recurrence guard: Require a writer-or-input map for expected files and keep the deferred self-output set minimal, named, and verified after process completion.
- Rollback: Retain the incomplete build receipt, revert only the unpromoted builder correction if it hides a real missing file, and never weaken privacy or exact-file review.
- Witnesses: V6446-M06-W01

### V6446-M07 — Exact boundary vocabulary in generated validation receipts

- Trigger: user boundary uses a term of art; generated receipt uses a near-synonym; validator asserts the explicit frozen role
- Method: Carry exact boundary vocabulary into generated receipts and tests for canonical role, named lane, same-owner replay, and independent-reproduction limits.
- Recurrence guard: Treat frozen role labels as schema values rather than prose synonyms and mutation-test their presence.
- Rollback: Restore the prior receipt only if the exact term misstates evidence; otherwise retain the failed test and regenerate the bounded receipt.
- Witnesses: V6446-M07-W01

### V6446-M08 — Exact Git-blob hash domain for committed content seals

- Trigger: Windows working tree; text generated with platform newlines; Git attributes or clean filters; manifest intended to attest committed bytes
- Method: Generate the committed-byte seal from exact Git blob bytes after repository attributes and clean filters, and name that domain explicitly.
- Recurrence guard: Every hash receipt must declare Git-blob, normalized logical-text, or raw working-tree domain; staged parity may compare only the Git-blob domain.
- Rollback: Retain the mismatching review, restore the previous seal only as an explicitly raw-working-tree receipt if needed, and never relabel one hash domain as another.
- Witnesses: V6446-M08-W01

### V6446-M09 — PowerShell here-string transport for inline Python

- Trigger: PowerShell host; multi-line inline Python; POSIX heredoc syntax
- Method: Pipe a literal PowerShell here-string to python standard input for multi-line read-only queries.
- Recurrence guard: Select shell-native multi-line transport before composing inline code and keep the query read-only.
- Rollback: Retain the parser failure, make no file change, and rerun only through the host shell's supported literal transport.
- Witnesses: V6446-M09-W01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
