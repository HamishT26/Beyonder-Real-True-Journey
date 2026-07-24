# GHC Family Method Flow State

- Phase: v653-gmut-thos-v8-x1-x2
- Owner: Liora Venn
- Methods: 12
- Passing witnesses: 12
- Failed witnesses retained: 12

## Preferred methods

### V6538-METHOD-01 — Bounded recovery for activation_read_interrupted_before_eof

- Trigger: activation_read_interrupted_before_eof
- Method: Restart at line one, read every bounded chunk through the declared final line, and verify EOF before mutation.
- Recurrence guard: Restart at line one, read every bounded chunk through the declared final line, and verify EOF before mutation.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-01-F, V6538-WITNESS-01-P

### V6538-METHOD-02 — Bounded recovery for worktree_add_wrapper_timeout

- Trigger: worktree_add_wrapper_timeout
- Method: Do not replay the mutation; inspect processes, path, worktree registration, branch, exact head, and clean state with isolated read-only probes.
- Recurrence guard: Do not replay the mutation; inspect processes, path, worktree registration, branch, exact head, and clean state with isolated read-only probes.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-02-F, V6538-WITNESS-02-P

### V6538-METHOD-03 — Bounded recovery for combined_post_timeout_audit_timeout

- Trigger: combined_post_timeout_audit_timeout
- Method: Split process, path, registration, branch, head, and status checks into bounded isolated probes.
- Recurrence guard: Split process, path, registration, branch, head, and status checks into bounded isolated probes.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-03-F, V6538-WITNESS-03-P

### V6538-METHOD-04 — Bounded recovery for powershell_convertfromjson_depth_unsupported

- Trigger: powershell_convertfromjson_depth_unsupported
- Method: Inspect the installed PowerShell command surface and parse the bounded JSON without the unsupported parameter.
- Recurrence guard: Inspect the installed PowerShell command surface and parse the bounded JSON without the unsupported parameter.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-04-F, V6538-WITNESS-04-P

### V6538-METHOD-05 — Bounded recovery for overbroad_corpus_display_truncated

- Trigger: overbroad_corpus_display_truncated
- Method: Use exact schema counts, bounded recent-title slices, and targeted mechanism-token searches while retaining the complete machine-read audit.
- Recurrence guard: Use exact schema counts, bounded recent-title slices, and targeted mechanism-token searches while retaining the complete machine-read audit.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-05-F, V6538-WITNESS-05-P

### V6538-METHOD-06 — Bounded recovery for powershell_foreach_pipe_parse_failure

- Trigger: powershell_foreach_pipe_parse_failure
- Method: Materialize foreach output in an array before formatting, filtering, or measurement.
- Recurrence guard: Materialize foreach output in an array before formatting, filtering, or measurement.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-06-F, V6538-WITNESS-06-P

### V6538-METHOD-07 — Bounded recovery for x1_workflow_wrapper_self_recursion

- Trigger: x1_workflow_wrapper_self_recursion
- Method: Bind the inherited workflow function before installing the wrapper override, keep the partial packet outcome-free, and rerun the x1-only generator after the narrow repair.
- Recurrence guard: Bind the inherited workflow function before installing the wrapper override, keep the partial packet outcome-free, and rerun the x1-only generator after the narrow repair.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-07-F, V6538-WITNESS-07-P

### V6538-METHOD-08 — Bounded recovery for workflow_messaging_enum_mismatch

- Trigger: workflow_messaging_enum_mismatch
- Method: Use the canonical existing-task-after-terminal-gate and user-mediated-file-relay-only enums while retaining the stricter live prose boundary.
- Recurrence guard: Use the canonical existing-task-after-terminal-gate and user-mediated-file-relay-only enums while retaining the stricter live prose boundary.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6538-WITNESS-08-F, V6538-WITNESS-08-P

### V6538-METHOD-09 — Bounded recovery for combined_post_push_equality_probe_timeout

- Trigger: combined_post_push_equality_probe_timeout
- Method: Preserve the timeout, then run isolated clean-state, upstream, tracking, fresh-live, commit-count, merge-count, and parent probes.
- Recurrence guard: Do not combine potentially cold Git and live-remote checks; each exact witness receives its own bounded probe.
- Rollback: Stop, retain the failed witness with zero credit, and leave all external and protected-gate state unchanged.
- Witnesses: V6538-WITNESS-09-F, V6538-WITNESS-09-P

### V6538-METHOD-10 — Bounded recovery for inherited_validator_filename_assumption

- Trigger: inherited_validator_filename_assumption
- Method: Use rg --files to discover the exact inherited filenames before reading sizes, schemas, or implementation patterns.
- Recurrence guard: Discover exact repository filenames before constructing a bounded inventory; never infer validator or test suffixes.
- Rollback: Stop, retain the failed witness with zero credit, and leave all external and protected-gate state unchanged.
- Witnesses: V6538-WITNESS-10-F, V6538-WITNESS-10-P

### V6538-METHOD-11 — Bounded recovery for combined_tracked_untracked_inventory_timeout

- Trigger: combined_tracked_untracked_inventory_timeout
- Method: Run tracked changes, untracked paths, and scope counts as isolated bounded probes before staging.
- Recurrence guard: Materially enforce isolated Git probes after any cold-worktree timeout; do not combine repository scans for convenience.
- Rollback: Stop, retain the failed witness with zero credit, and leave all external and protected-gate state unchanged.
- Witnesses: V6538-WITNESS-11-F, V6538-WITNESS-11-P

### V6538-METHOD-12 — Bounded recovery for detailed_validator_cp1252_stdout_failure

- Trigger: detailed_validator_cp1252_stdout_failure
- Method: Configure UTF-8 stdout explicitly in the validator and preserve the same validated payload and Māori wording.
- Recurrence guard: Every direct validator and canonical wrapper must set UTF-8 stdout or an equivalent PYTHONIOENCODING before emitting receipts.
- Rollback: Stop, retain the failed witness with zero credit, and leave all external and protected-gate state unchanged.
- Witnesses: V6538-WITNESS-12-F, V6538-WITNESS-12-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
