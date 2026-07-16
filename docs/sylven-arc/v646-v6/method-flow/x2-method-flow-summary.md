# GHC Family Method Flow State

- Phase: v646-gmut-thos-v6-x1-x2-x2
- Owner: Sylven Arc
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
