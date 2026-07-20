# GHC Family Method Flow State

- Phase: v650-v6-x2
- Owner: Sylven Arc
- Methods: 3
- Passing witnesses: 3
- Failed witnesses retained: 3

## Preferred methods

### V6506-X2M01 — Recover skill validator help-mode assumption while retaining the failed witness

- Trigger: The v650-v6 x2 lane encounters skill validator help-mode assumption.
- Method: Give the help probe zero validation credit and invoke the validator only with each real phase-local skill directory.
- Recurrence guard: Inspect a validator's interface or call it on a disposable real package instead of assuming it implements help mode.
- Rollback: Give the failed attempt zero evidence credit, retain it, and leave external and sibling state unchanged.
- Witnesses: V6506-X2M01-WFAIL, V6506-X2M01-WPASS

### V6506-X2M02 — Recover reserved-word test syntax while retaining the failed witness

- Trigger: The v650-v6 x2 lane encounters reserved-word test syntax.
- Method: Retain the zero-test import failure and express expected witness counts with an explicit string-key mapping.
- Recurrence guard: Use mappings when expected record labels may collide with Python keywords.
- Rollback: Give the failed attempt zero evidence credit, retain it, and leave external and sibling state unchanged.
- Witnesses: V6506-X2M02-WFAIL, V6506-X2M02-WPASS

### V6506-X2M03 — Recover repository-wide staged-index timeout while retaining the failed witness

- Trigger: The v650-v6 x2 lane encounters repository-wide staged-index timeout.
- Method: Give the timed-out review zero credit and derive staged object identifiers from one phase-scoped temporary tree traversal before one bounded blob batch.
- Recurrence guard: Never enumerate the full repository index when the exact staged path set and phase-scoped tree prefixes are already known.
- Rollback: Give the failed attempt zero evidence credit, retain it, and leave external and sibling state unchanged.
- Witnesses: V6506-X2M03-WFAIL, V6506-X2M03-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
