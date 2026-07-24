# GHC Family Method Flow State

- Phase: v654-v2
- Owner: Elowen Cairn
- Methods: 17
- Passing witnesses: 17
- Failed witnesses retained: 17

## Preferred methods

### V6542-METHOD-01 — Bounded recovery for committed_validator_proposal_ledger_filename_assumption

- Trigger: committed_validator_proposal_ledger_filename_assumption
- Method: Discover and bind the committed filename before the bounded validator retry.
- Recurrence guard: Resolve exact committed receipt and ledger names from the tree before validation.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-01-F, V6542-WITNESS-01-P

### V6542-METHOD-02 — Bounded recovery for windows_wildcard_path_assumption

- Trigger: windows_wildcard_path_assumption
- Method: Use literal paths and an explicitly materialized bounded file inventory.
- Recurrence guard: Never depend on wildcard expansion for exact Windows validation paths.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-02-F, V6542-WITNESS-02-P

### V6542-METHOD-03 — Bounded recovery for workflow_commit_cap_property_projection_assumptions

- Trigger: workflow_commit_cap_property_projection_assumptions
- Method: Inspect the exact workflow receipt schema and bind only its committed property names.
- Recurrence guard: Discover receipt keys before projecting workflow commit-cap fields.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-03-F, V6542-WITNESS-03-P

### V6542-METHOD-04 — Bounded recovery for external_bridge_repo_import_path_omission

- Trigger: external_bridge_repo_import_path_omission
- Method: Apply the narrow external in-memory import-path correction without changing a repository byte.
- Recurrence guard: Preflight the repository import root in external test bridges before invoking the canonical selector.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-04-F, V6542-WITNESS-04-P

### V6542-METHOD-05 — Bounded recovery for startup_skill_memory_discovery_timeout

- Trigger: startup_skill_memory_discovery_timeout
- Method: Split skill discovery from memory lookup and use exact names or bounded filters.
- Recurrence guard: Use one cold filesystem or memory scan per bounded probe.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-05-F, V6542-WITNESS-05-P

### V6542-METHOD-06 — Bounded recovery for filtered_skill_memory_discovery_timeout

- Trigger: filtered_skill_memory_discovery_timeout
- Method: Probe exact expected skill names first, then use filesystem filters independently.
- Recurrence guard: Do not combine directory enumeration with a large registry search.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-06-F, V6542-WITNESS-06-P

### V6542-METHOD-07 — Bounded recovery for foreach_pipeline_parser_fault

- Trigger: foreach_pipeline_parser_fault
- Method: Materialize foreach output in an array before piping.
- Recurrence guard: Never pipe directly from a PowerShell foreach statement.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-07-F, V6542-WITNESS-07-P

### V6542-METHOD-08 — Bounded recovery for combined_source_probe_timeout

- Trigger: combined_source_probe_timeout
- Method: Split storage, exact head, and cleanliness into isolated bounded probes.
- Recurrence guard: One cold Git or filesystem subsystem per probe.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-08-F, V6542-WITNESS-08-P

### V6542-METHOD-09 — Bounded recovery for validation_record_path_assumption

- Trigger: validation_record_path_assumption
- Method: Discover exact committed filenames before binding blob paths.
- Recurrence guard: Use the exact tree inventory rather than lifecycle filename guesses.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-09-F, V6542-WITNESS-09-P

### V6542-METHOD-10 — Bounded recovery for frozen_proposal_id_field_assumption

- Trigger: frozen_proposal_id_field_assumption
- Method: Inspect top-level and entry keys before binding the query.
- Recurrence guard: Bind proposal_id and title only after schema discovery.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-10-F, V6542-WITNESS-10-P

### V6542-METHOD-11 — Bounded recovery for unavailable_dotnet_hash_helper_assumption

- Trigger: unavailable_dotnet_hash_helper_assumption
- Method: Use the installed SHA256 provider and explicit hexadecimal formatting.
- Recurrence guard: Probe runtime APIs or use the compatible streaming provider.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-11-F, V6542-WITNESS-11-P

### V6542-METHOD-12 — Bounded recovery for proposal_schema_field_name_assumption

- Trigger: proposal_schema_field_name_assumption
- Method: Bind the committed null_or_failure_condition, official_or_primary_source_needs, falsifier_or_acceptance_gate, and rollback_or_recovery names.
- Recurrence guard: Inspect exact proposal keys before validating.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-12-F, V6542-WITNESS-12-P

### V6542-METHOD-13 — Bounded recovery for worktree_add_wrapper_timeout_after_completion

- Trigger: worktree_add_wrapper_timeout_after_completion
- Method: Audit exact path, registration, branch, head, clean state, and running Git processes before any retry.
- Recurrence guard: Never retry a timed-out worktree mutation before a complete state audit.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-13-F, V6542-WITNESS-13-P

### V6542-METHOD-14 — Bounded recovery for large_phase_data_patch_context_mismatch

- Trigger: large_phase_data_patch_context_mismatch
- Method: Replace the new owner-local module as one exact file and retain the failed patch.
- Recurrence guard: Prefer whole-file replacement for a new generated data module when inherited Unicode context is unstable.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-14-F, V6542-WITNESS-14-P

### V6542-METHOD-15 — Bounded recovery for overview_patch_unicode_context_mismatch

- Trigger: overview_patch_unicode_context_mismatch
- Method: Replace only the owner-local function between stable ASCII definition markers.
- Recurrence guard: Use stable ASCII function boundaries instead of inherited mojibake in large generated-text patches.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-15-F, V6542-WITNESS-15-P

### V6542-METHOD-16 — Bounded recovery for windows_rg_wildcard_path_assumption

- Trigger: windows_rg_wildcard_path_assumption
- Method: Enumerate explicit files or search a literal directory with a filename filter.
- Recurrence guard: Do not pass unresolved Windows wildcard paths to ripgrep.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-16-F, V6542-WITNESS-16-P

### V6542-METHOD-17 — Bounded recovery for workflow_single_seat_cycle_rejected

- Trigger: workflow_single_seat_cycle_rejected
- Method: Retain the failed packet and represent the no-successor boundary as a second nonowner route label while normalizing only the one authorized Elowen assignment.
- Recurrence guard: Preflight the current runner's minimum two-label cycle rule without inventing a successor owner or phase.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6542-WITNESS-17-F, V6542-WITNESS-17-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
