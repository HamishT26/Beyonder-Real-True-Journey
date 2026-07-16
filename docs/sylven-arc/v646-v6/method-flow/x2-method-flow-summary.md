# GHC Family Method Flow State

- Phase: v646-gmut-thos-v6-x1-x2-x2
- Owner: Sylven Arc
- Methods: 9
- Passing witnesses: 9
- Failed witnesses retained: 9

## Preferred methods

### V6466-X2-M01 — Read generic evidence envelopes through their declared surface summary

- Trigger: generic evidence envelope; surface-specific source gate; zero-row receipt; schema traversal
- Method: Persist the bounded surface summary inside the receipt and make the gate traverse that explicit field.
- Recurrence guard: Validators must read the declared schema shape and never infer top-level placement from a filename.
- Rollback: Retain the original failure and award no affected credit until the bounded recovery passes.
- Witnesses: V6466-X2-M01-W-F, V6466-X2-M01-W-P

### V6466-X2-M02 — Separate UTF-8 evidence files from narrow Windows console summaries

- Trigger: Windows console; CP1252; UTF-8 repository receipt; Māori boundary text
- Method: Write the canonical receipt as UTF-8 and serialize only the console copy with ensure_ascii enabled.
- Recurrence guard: Console compatibility must not strip or alter Māori text in repository evidence.
- Rollback: Retain the original failure and award no affected credit until the bounded recovery passes.
- Witnesses: V6466-X2-M02-W-F, V6466-X2-M02-W-P

### V6466-X2-M03 — Invoke the family Method Flow runner in UTF-8 console mode

- Trigger: family Method Flow runner; Windows CP1252 console; Māori boundary text; summary command
- Method: Set PYTHONUTF8 for the child process without changing the ledger, summary content, or repository encoding.
- Recurrence guard: Family runner subprocesses that can emit Māori text use UTF-8 console mode; repository files remain UTF-8.
- Rollback: Retain the original failure and award no affected credit until the bounded recovery passes.
- Witnesses: V6466-X2-M03-W-F, V6466-X2-M03-W-P

### V6466-X2-M04 — Distinguish browser evaluation labels from private browser callable identifiers

- Trigger: five-class privacy scan; accessibility receipt; browser-prefixed field; private callable class
- Method: Constrain the browser callable branch to send, probe, route, callable, or message semantics and retain all other pattern classes and candidates.
- Recurrence guard: Generic browser evaluation vocabulary is not a callable ID; any callable-semantic browser identifier remains confirmed unless explicitly dispositioned.
- Rollback: Retain the original failure and award no affected credit until the bounded recovery passes.
- Witnesses: V6466-X2-M04-W-F, V6466-X2-M04-W-P

### V6466-X2-M05 — Classify both privacy scanner implementations as scanner-definition candidates

- Trigger: exact staged Git-blob scan; validation runner source; scanner regex literals; candidate-confirmed split
- Method: Disposition only callable and session matches in the two known scanner implementations as scanner-definition candidates; keep all files and classes in coverage.
- Recurrence guard: The exception is path- and class-specific; any nondefinition match remains confirmed.
- Rollback: Retain the original failure and award no affected credit until the bounded recovery passes.
- Witnesses: V6466-X2-M05-W-F, V6466-X2-M05-W-P

### V6466-X2-M06 — Keep closeout replay labels stable across records and tests

- Trigger: generated closeout record; machine substring assertion; named local-only replay; precommit validation
- Method: Use one stable contiguous named-replay phrase in the closeout record while preserving the local-only lane qualifier.
- Recurrence guard: Machine checks and generated receipts share one stable label; scope qualifiers remain explicit elsewhere in the same phrase.
- Rollback: Retain the 23-of-24 failed run and award no closeout-test credit until the bounded rerun passes.
- Witnesses: V6466-X2-M06-W-F, V6466-X2-M06-W-P

### V6466-X2-M07 — Quote PowerShell ripgrep alternations as literal arguments

- Trigger: PowerShell shell; ripgrep alternation; embedded quote character; bounded cross-reference search
- Method: Pass the ripgrep alternation as one PowerShell single-quoted literal so embedded double quotes remain data rather than shell syntax.
- Recurrence guard: PowerShell search expressions containing alternation or quote characters use literal-safe single-quoted arguments and are retried without broadening scope.
- Rollback: Retain the parser failure and do not treat it as search evidence; use only the successful literal-safe rerun.
- Witnesses: V6466-X2-M07-W-F, V6466-X2-M07-W-P

### V6466-X2-M08 — Refresh coupled lifecycle-count assertions after retained failures

- Trigger: append-only Method Flow growth; authoritative retained-negative register; evidence-stage historical receipts; current validation assertions
- Method: Update all final count-dependent assertions together after appending closeout Method Flow failures, while retaining evidence-stage receipts as historical snapshots.
- Recurrence guard: After any retained lifecycle failure, update the authoritative negative register, current tests, minimal validator, closeout checks, and Method Flow count assertions in one review set; historical evidence receipts keep their stage label.
- Rollback: Retain the 22-of-24 failed current bundle and do not claim final count parity until the complete bounded bundle passes.
- Witnesses: V6466-X2-M08-W-F, V6466-X2-M08-W-P

### V6466-X2-M09 — Allow only the explicit phase closeout test in staged-surface review

- Trigger: exact staged-file review; phase-local closeout test; owner-scoped allowlist; precommit inspection
- Method: Extend only the v646-v6 phase-local test allowlist to the explicit closeout suffix; keep all other out-of-scope paths rejected.
- Recurrence guard: When a phase adds an explicitly named closeout test, review the exact staged allowlist before invocation and add only that phase-local suffix.
- Rollback: Retain the inspection finding; if the exact staged review does not pass, restore the narrow allowlist and award no staged-review credit.
- Witnesses: V6466-X2-M09-W-F, V6466-X2-M09-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
