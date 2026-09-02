# GHC Family Method Flow State

- Phase: v684-v5-x2
- Owner: Sable Rook
- Methods: 3
- Passing witnesses: 3
- Failed witnesses retained: 5

## Preferred methods

### SR6845-M008 — Pin UTF-8 for Unicode-emitting skill validation

- Trigger: A Unicode-emitting phase-local skill is validated by a script using process-default text decoding.
- Method: Set PYTHONUTF8 and PYTHONIOENCODING to UTF-8 for the validator subprocess and retain the failed attempt separately.
- Recurrence guard: Pin UTF-8 before every Unicode-emitting validation process and refuse replay after a successful receipt.
- Rollback: Remove only incomplete current receipts, retain failed receipts, and return to the immutable x1 parent if the corrected attempt fails.
- Witnesses: SR6845-M008-WF01, SR6845-M008-WF02, SR6845-M008-WF03, SR6845-M008-WP01

### SR6845-M009 — Pin UTF-8 for Unicode Method Flow summary projection

- Trigger: A validated Method Flow summary includes Unicode text and is projected to a legacy Windows console.
- Method: Verify persisted files before retry, then set PYTHONUTF8 and PYTHONIOENCODING to UTF-8 for the summary command.
- Recurrence guard: Pin UTF-8 before Unicode-emitting Method Flow commands and never infer failure of persisted evidence from a console-only encoding fault.
- Rollback: Keep the previously validated ledger and persisted files; do not rebuild or delete evidence.
- Witnesses: SR6845-M009-WF01, SR6845-M009-WP01

### SR6845-M010 — Inspect persisted staged-review state before retry

- Trigger: A bounded validation wrapper is unattributable but may have completed and written deterministic receipts.
- Method: Inspect the persisted review, exact staged and unstaged counts, mismatch arrays, and diff hygiene before any retry.
- Recurrence guard: Never replay a potentially successful deterministic review solely because its presentation wrapper is empty.
- Rollback: Keep the exact staged index unchanged and stop if persisted state is incomplete or contradictory.
- Witnesses: SR6845-M010-WF01, SR6845-M010-WP01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
