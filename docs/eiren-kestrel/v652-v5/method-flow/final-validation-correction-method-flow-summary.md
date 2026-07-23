# GHC Family Method Flow State

- Phase: v652-v5-final-validation-correction
- Owner: Eiren Kestrel
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

## Preferred methods

### V6525-FINAL-METHOD-01 — Bounded recovery for exact_final_full_suite_failed_attempt

- Trigger: exact_final_full_suite_failed_attempt
- Method: Retain the complete failed attempt, diagnose only its four failed modules, and permit one corrected retry before any successful pass.
- Recurrence guard: Never convert a failed aggregate into a pass or launch a blind full suite replay without first classifying every failed test.
- Rollback: Stop, retain the failed validation attempt, and leave sibling state and external authority unchanged.
- Witnesses: V6525-FINAL-WITNESS-01-F, V6525-FINAL-WITNESS-01-P

### V6525-FINAL-METHOD-02 — Bounded recovery for historical_delta_manifest_reads_successor_head

- Trigger: historical_delta_manifest_reads_successor_head
- Method: The historical remaster test computes its phase-local evidence-to-HEAD delta against the current successor head, so every later sibling and phase path becomes an expected member of the old frozen manifest.
- Recurrence guard: Bind historical delta-manifest assertions to their immutable final commit instead of a moving successor HEAD.
- Rollback: Stop, retain the failed validation attempt, and leave sibling state and external authority unchanged.
- Witnesses: V6525-FINAL-WITNESS-02-F, V6525-FINAL-WITNESS-02-P

### V6525-FINAL-METHOD-03 — Bounded recovery for historical_commit_count_reads_successor_head

- Trigger: historical_commit_count_reads_successor_head
- Method: The historical closeout test counts its source-to-current-HEAD commits and therefore cannot preserve its own two-or-three-commit lifecycle assertion after additive successor phases.
- Recurrence guard: Resolve lifecycle commit-count assertions against the phase's sealed final anchor, never a moving successor HEAD.
- Rollback: Stop, retain the failed validation attempt, and leave sibling state and external authority unchanged.
- Witnesses: V6525-FINAL-WITNESS-03-F, V6525-FINAL-WITNESS-03-P

### V6525-FINAL-METHOD-04 — Bounded recovery for historical_x1_filename_absence_reads_x2_tree

- Trigger: historical_x1_filename_absence_reads_x2_tree
- Method: The historical x1 test scans the mutable phase directory and requires later x2 outcome and seal filenames to remain absent.
- Recurrence guard: Evaluate x1-only filename absence from the immutable x1 tree rather than a later working-tree phase directory.
- Rollback: Stop, retain the failed validation attempt, and leave sibling state and external authority unchanged.
- Witnesses: V6525-FINAL-WITNESS-04-F, V6525-FINAL-WITNESS-04-P

### V6525-FINAL-METHOD-05 — Bounded recovery for historical_x1_directory_absence_reads_x2_tree

- Trigger: historical_x1_directory_absence_reads_x2_tree
- Method: The historical x1 test reads the mutable phase directory and requires the later evidence surfaces directory to remain absent.
- Recurrence guard: Evaluate x1-only directory absence from the immutable x1 tree rather than a later working-tree phase directory.
- Rollback: Stop, retain the failed validation attempt, and leave sibling state and external authority unchanged.
- Witnesses: V6525-FINAL-WITNESS-05-F, V6525-FINAL-WITNESS-05-P

### V6525-FINAL-METHOD-06 — Bounded recovery for route_correction_test_fixed_final_contract

- Trigger: route_correction_test_fixed_final_contract
- Method: Make the owner-controlled compatibility test distinguish the exact route-correction v2 contract from the additive final-correction v3 contract while preserving the six-commit cap and exact scoped counts.
- Recurrence guard: Successor-compatible tests must bind lifecycle assertions to their schema boundary instead of treating an additive final correction as a mutation of the earlier route receipt.
- Rollback: Stop, retain the failed validation attempt, and leave sibling state and external authority unchanged.
- Witnesses: V6525-FINAL-WITNESS-06-F, V6525-FINAL-WITNESS-06-P

### V6525-FINAL-METHOD-07 — Bounded recovery for final_correction_allowlist_omitted_route_test

- Trigger: final_correction_allowlist_omitted_route_test
- Method: Admit that one exact owner-controlled route test in the final-validation correction allowlist while keeping every other root and predecessor path fail-closed.
- Recurrence guard: Whenever a correction updates a predecessor compatibility assertion, declare that exact test in the correction's root-path allowlist.
- Rollback: Stop, retain the failed validation attempt, and leave sibling state and external authority unchanged.
- Witnesses: V6525-FINAL-WITNESS-07-F, V6525-FINAL-WITNESS-07-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
