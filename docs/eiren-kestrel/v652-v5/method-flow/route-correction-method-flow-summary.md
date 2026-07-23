# GHC Family Method Flow State

- Phase: v652-v5-route-correction
- Owner: Eiren Kestrel
- Methods: 6
- Passing witnesses: 6
- Failed witnesses retained: 6

## Preferred methods

### V6525-ROUTE-METHOD-01 — Bounded recovery for combined_syntax_status_wrapper_timeout

- Trigger: combined_syntax_status_wrapper_timeout
- Method: Split syntax compilation and Git-state inspection into separate bounded probes, crediting each only after its own successful result.
- Recurrence guard: Do not combine Python compilation and broad Windows Git status in one short wrapper; use separate bounds and outputs.
- Rollback: Stop, retain the failed wrapper, and leave repository history and external state unchanged.
- Witnesses: V6525-ROUTE-WITNESS-01-F, V6525-ROUTE-WITNESS-01-P

### V6525-ROUTE-METHOD-02 — Bounded recovery for porcelain_leading_column_trim

- Trigger: porcelain_leading_column_trim
- Method: Read git status --porcelain=v1 as raw captured output, preserve both status columns, and slice the path only after the fixed prefix.
- Recurrence guard: Never apply whole-output strip operations before parsing fixed-column Git porcelain records.
- Rollback: Stop, retain the failed wrapper, and leave repository history and external state unchanged.
- Witnesses: V6525-ROUTE-WITNESS-02-F, V6525-ROUTE-WITNESS-02-P

### V6525-ROUTE-METHOD-03 — Bounded recovery for route_correction_allowlist_omission

- Trigger: route_correction_allowlist_omission
- Method: Declare the closeout compatibility test as a route-correction path and permit only the builder's own phase artifacts during an idempotent retry from the unchanged closeout head.
- Recurrence guard: When a route correction changes a historical compatibility assertion, include that exact test in both starting and final path allowlists.
- Rollback: Stop, retain the failed wrapper, and leave repository history and external state unchanged.
- Witnesses: V6525-ROUTE-WITNESS-03-F, V6525-ROUTE-WITNESS-03-P

### V6525-ROUTE-METHOD-04 — Bounded recovery for mutable_predecessor_route_read

- Trigger: mutable_predecessor_route_read
- Method: Read predecessor route truth from the immutable closeout Git blob rather than from the mutable working tree.
- Recurrence guard: Bind every predecessor lifecycle read to its declared immutable commit whenever an additive correction may rerun.
- Rollback: Stop, retain the failed wrapper, and leave repository history and external state unchanged.
- Witnesses: V6525-ROUTE-WITNESS-04-F, V6525-ROUTE-WITNESS-04-P

### V6525-ROUTE-METHOD-05 — Bounded recovery for route_method_flow_frozen_scope_misclassification

- Trigger: route_method_flow_frozen_scope_misclassification
- Method: Freeze inherited, evidence, and closeout Method Flow paths while explicitly admitting only route-correction-prefixed Method Flow artifacts in the additive correction.
- Recurrence guard: Define freeze domains by lifecycle ownership, not by a broad top-level directory prefix.
- Rollback: Stop, retain the failed wrapper, and leave repository history and external state unchanged.
- Witnesses: V6525-ROUTE-WITNESS-05-F, V6525-ROUTE-WITNESS-05-P

### V6525-ROUTE-METHOD-06 — Bounded recovery for unavailable_pytest_entrypoint

- Trigger: unavailable_pytest_entrypoint
- Method: Use the repository-native unittest module entrypoints already declared by the phase tests and final validator.
- Recurrence guard: Probe runner availability or use the repository-declared unittest entrypoint instead of assuming an optional pytest installation.
- Rollback: Stop, retain the failed wrapper, and leave repository history and external state unchanged.
- Witnesses: V6525-ROUTE-WITNESS-06-F, V6525-ROUTE-WITNESS-06-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
