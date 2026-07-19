# GHC Family Method Flow State

- Phase: v649-gmut-thos-v4-closeout
- Owner: Orin Thale
- Methods: 5
- Passing witnesses: 6
- Failed witnesses retained: 6

## Preferred methods

### V6494-CLOSE-M01 — Isolated no-login post-commit Git verification

- Trigger: large inherited checkout; post-commit verification; grouped wrapper timeout
- Method: Run each post-commit Git probe separately with login-shell initialization disabled.
- Recurrence guard: Run large-checkout post-commit Git probes as isolated no-login commands and preserve each native exit status.
- Rollback: Discard the incomplete grouped result and leave repository and remote state unchanged.
- Witnesses: V6494-CLOSE-M01-WFAIL, V6494-CLOSE-M01-WPASS

### V6494-CLOSE-M02 — Explicit-root Windows ripgrep inventories

- Trigger: Windows filesystem; multiple source or test files; pattern-filtered inventory
- Method: Use explicit directory roots and ripgrep -g filters instead of wildcard path operands.
- Recurrence guard: Use explicit Windows roots with ripgrep -g filters and retain every recurrence as a separate failed witness.
- Rollback: Discard literal-wildcard results and leave repository content unchanged.
- Witnesses: V6494-CLOSE-M02-WFAIL1, V6494-CLOSE-M02-WFAIL2, V6494-CLOSE-M02-WPASS1, V6494-CLOSE-M02-WPASS2

### V6494-CLOSE-M03 — Explicit generated Method Flow filename discovery

- Trigger: generated Method Flow artifacts; unknown filename convention; read-only inspection
- Method: Inventory generated files explicitly before selecting record and witness paths.
- Recurrence guard: Inventory generated filenames explicitly before reading them; do not infer prefixes from method identifiers.
- Rollback: Treat all missing-path reads as failed assumptions and leave repository content unchanged.
- Witnesses: V6494-CLOSE-M03-WFAIL, V6494-CLOSE-M03-WPASS

### V6494-CLOSE-M04 — Repository-root-bound unittest discovery

- Trigger: named repository test modules; script executed from scripts directory; canonical pass budget not yet used
- Method: Bind the repository root in sys.path before loading named repository test modules.
- Recurrence guard: Bind in-process test discovery to the repository root and reject placeholder-only module counts before consuming a pass budget.
- Rollback: Treat the provisional count as invalid, run no tests, and leave the canonical pass budget unused.
- Witnesses: V6494-CLOSE-M04-WFAIL, V6494-CLOSE-M04-WPASS

### V6494-CLOSE-M05 — Import-complete inherited scoped-test selection

- Trigger: failed loader selectors; successful pass counter still zero; immutable inherited test inventory available
- Method: Import every named test module explicitly and select the actual inherited x1 and x2 modules from the immutable test-file inventory.
- Recurrence guard: Explicitly import every named module before suite construction and reject any inferred selector absent from the exact test-file inventory.
- Rollback: Give the failed attempt zero canonical-pass credit, preserve its receipt, and keep successful_passes_used at zero.
- Witnesses: V6494-CLOSE-M05-WFAIL, V6494-CLOSE-M05-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
