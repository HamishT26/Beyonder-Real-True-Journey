# GHC Family Method Flow State

- Phase: v654-v1
- Owner: Tamar Vey
- Methods: 32
- Passing witnesses: 32
- Failed witnesses retained: 32

## Preferred methods

### V6541-METHOD-01 — Bounded recovery for plan_output_truncated_at_tool_boundary

- Trigger: plan_output_truncated_at_tool_boundary
- Method: Reissue only the compact current plan state and verify the single in-progress step.
- Recurrence guard: Keep plan updates concise and omit inherited narrative.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-01-F, V6541-WITNESS-01-P

### V6541-METHOD-02 — Bounded recovery for skill_read_timed_out

- Trigger: skill_read_timed_out
- Method: Read explicit bounded line windows through the declared final line and verify EOF.
- Recurrence guard: Use bounded line windows for long skill files.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-02-F, V6541-WITNESS-02-P

### V6541-METHOD-03 — Bounded recovery for foreach_pipeline_parser_fault

- Trigger: foreach_pipeline_parser_fault
- Method: Materialize foreach output into an array before piping to JSON serialization.
- Recurrence guard: Never pipe directly from a PowerShell foreach statement.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-03-F, V6541-WITNESS-03-P

### V6541-METHOD-04 — Bounded recovery for manifest_summary_emitted_entries

- Trigger: manifest_summary_emitted_entries
- Method: Project only scalar counts, exclusions, and mismatch totals; verify blobs separately in batch.
- Recurrence guard: Never serialize entry-bearing manifests without an explicit scalar projection.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-04-F, V6541-WITNESS-04-P

### V6541-METHOD-05 — Bounded recovery for combined_ancestry_wrapper_timeout

- Trigger: combined_ancestry_wrapper_timeout
- Method: Split head, parent, ancestry, status, and live-remote checks into bounded isolated probes.
- Recurrence guard: Do not combine cold Git and network checks.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-05-F, V6541-WITNESS-05-P

### V6541-METHOD-06 — Bounded recovery for isolated_parent_probe_timeout

- Trigger: isolated_parent_probe_timeout
- Method: Use git cat-file with a larger bound and parse the direct parent line.
- Recurrence guard: Prefer direct object reads for exact parent checks.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-06-F, V6541-WITNESS-06-P

### V6541-METHOD-07 — Bounded recovery for negative_register_summary_overbroad

- Trigger: negative_register_summary_overbroad
- Method: Read only named scalar properties and mutation counts.
- Recurrence guard: Select scalar properties before serialization.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-07-F, V6541-WITNESS-07-P

### V6541-METHOD-08 — Bounded recovery for fast_forward_output_overlarge

- Trigger: fast_forward_output_overlarge
- Method: Audit exact head, branch, clean state, divergence, and fresh remote separately.
- Recurrence guard: Suppress or bound diffstat-like output for large inherited fast-forwards.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-08-F, V6541-WITNESS-08-P

### V6541-METHOD-09 — Bounded recovery for frozen_corpus_rows_field_assumption

- Trigger: frozen_corpus_rows_field_assumption
- Method: Use the actual prior_proposals and new_proposals arrays and verify their counts.
- Recurrence guard: Inspect exact JSON schema keys before binding a query.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-09-F, V6541-WITNESS-09-P

### V6541-METHOD-10 — Bounded recovery for standards_query_foreach_parser_fault

- Trigger: standards_query_foreach_parser_fault
- Method: Materialize the result array before serialization.
- Recurrence guard: Apply the foreach materialization guard to all inventories.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-10-F, V6541-WITNESS-10-P

### V6541-METHOD-11 — Bounded recovery for source_search_output_exceeded_context

- Trigger: source_search_output_exceeded_context
- Method: Use direct official URLs and one bounded targeted query at a time.
- Recurrence guard: Never combine broad source searches when direct primary URLs are available.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-11-F, V6541-WITNESS-11-P

### V6541-METHOD-12 — Bounded recovery for combined_status_negative_probe_timeout

- Trigger: combined_status_negative_probe_timeout
- Method: Run status/head and register projection as separate bounded probes.
- Recurrence guard: One cold subsystem per bounded probe.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-12-F, V6541-WITNESS-12-P

### V6541-METHOD-13 — Bounded recovery for negative_register_path_assumption

- Trigger: negative_register_path_assumption
- Method: Discover the exact final/retained-negative-register.json path before reading.
- Recurrence guard: Use rg --files before assuming lifecycle receipt locations.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-13-F, V6541-WITNESS-13-P

### V6541-METHOD-14 — Bounded recovery for negative_register_depth_projection_overbroad

- Trigger: negative_register_depth_projection_overbroad
- Method: Project the eight named scalar fields directly and never serialize the source object.
- Recurrence guard: Treat depth as insufficient; construct a new scalar object.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-14-F, V6541-WITNESS-14-P

### V6541-METHOD-15 — Bounded recovery for script_inventory_foreach_parser_fault

- Trigger: script_inventory_foreach_parser_fault
- Method: Materialize the rows, then serialize the array.
- Recurrence guard: Reuse the tested foreach materialization pattern.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-15-F, V6541-WITNESS-15-P

### V6541-METHOD-16 — Bounded recovery for broad_route_search_timeout

- Trigger: broad_route_search_timeout
- Method: Restrict the search to the exact Liora packet and closeout builder.
- Recurrence guard: Scope text searches to the smallest authoritative directory.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-16-F, V6541-WITNESS-16-P

### V6541-METHOD-17 — Bounded recovery for overview_patch_context_mismatch

- Trigger: overview_patch_context_mismatch
- Method: Keep the failed patch as zero credit, add the new function with ASCII context, then remove the legacy block by one bounded mechanical replacement.
- Recurrence guard: Use small ASCII anchors around inherited non-ASCII content.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-17-F, V6541-WITNESS-17-P

### V6541-METHOD-18 — Bounded recovery for method_flow_redundant_validated_transition

- Trigger: method_flow_redundant_validated_transition
- Method: Remove the redundant transition, rebuild the temporary ledger, retain the failed invocation, and promote only validated to preferred.
- Recurrence guard: Inspect runner state effects: a passing witness performs candidate-to-validated promotion automatically.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-18-F, V6541-WITNESS-18-P

### V6541-METHOD-19 — Bounded recovery for workflow_runner_one_off_route_enum_mismatch

- Trigger: workflow_runner_one_off_route_enum_mismatch
- Method: Represent the runner's live-phase no-contact policy with its supported enum, retain the one-off post-closeout creation authority in explicit extension fields, and use a string placeholder in the cycle.
- Recurrence guard: Model special post-closeout task creation as an explicit extension without weakening the runner's live-phase messaging guard.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-19-F, V6541-WITNESS-19-P

### V6541-METHOD-20 — Bounded recovery for privacy_scanner_credential_label_false_positive

- Trigger: privacy_scanner_credential_label_false_positive
- Method: Retain the failed scan, require credential assignments or bearer-shaped values rather than labels alone, and rerun every public x1 path.
- Recurrence guard: Credential scanning must distinguish a protected dependency label from an actual assigned secret while preserving bearer and assignment detection.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-20-F, V6541-WITNESS-20-P

### V6541-METHOD-21 — Bounded recovery for evidence_builder_large_patch_context_mismatch

- Trigger: evidence_builder_large_patch_context_mismatch
- Method: Retain the failed patch, inspect exact bounded line windows, and apply small ASCII-anchored changes.
- Recurrence guard: Patch compact generated builders with exact small contexts and avoid spanning inherited non-ASCII text.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-21-F, V6541-WITNESS-21-P

### V6541-METHOD-22 — Bounded recovery for evidence_manifest_unwritten_blob_lookup

- Trigger: evidence_manifest_unwritten_blob_lookup
- Method: Retain the failed validator, add hash-object -w for owner-local temporary blob materialization, and rerun the full bounded evidence validation.
- Recurrence guard: Any validator that reads a just-computed object through cat-file must write that object or hash the filtered bytes directly.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-22-F, V6541-WITNESS-22-P

### V6541-METHOD-23 — Bounded recovery for porcelain_first_line_leading_space_trim

- Trigger: porcelain_first_line_leading_space_trim
- Method: Retain the 17-of-18 result and read porcelain status directly without global string trimming before fixed-column parsing.
- Recurrence guard: Never apply strip to an entire porcelain status stream; preserve its two status columns exactly.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-23-F, V6541-WITNESS-23-P

### V6541-METHOD-24 — Bounded recovery for inherited_test_symbol_inventory_overbroad

- Trigger: inherited_test_symbol_inventory_overbroad
- Method: Retain the truncated inventory with zero selector credit and count test cases per file with a scalar AST probe before choosing dependency-justified modules.
- Recurrence guard: Inventory inherited tests as per-file scalar counts; never print broad matching source bodies.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-24-F, V6541-WITNESS-24-P

### V6541-METHOD-25 — Bounded recovery for grouped_closeout_status_probe_timeout

- Trigger: grouped_closeout_status_probe_timeout
- Method: Retain the timeout and split status, exact head, and inventories into isolated bounded probes.
- Recurrence guard: Run one cold Git or filesystem subsystem per bounded closeout probe.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-25-F, V6541-WITNESS-25-P

### V6541-METHOD-26 — Bounded recovery for full_untracked_status_inventory_timeout

- Trigger: full_untracked_status_inventory_timeout
- Method: Retain the timeout and inspect tracked status separately from owner-scoped untracked paths before explicit staging.
- Recurrence guard: Do not enumerate the checkout-wide untracked surface during closeout; scope untracked inventory to owner paths.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-26-F, V6541-WITNESS-26-P

### V6541-METHOD-27 — Bounded recovery for per_entry_manifest_replay_timeout

- Trigger: per_entry_manifest_replay_timeout
- Method: Retain the timed-out attempt and replay each commit through one exact tree map plus bounded batch object reads.
- Recurrence guard: Never validate a large commit-local manifest with one Git subprocess per entry.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-27-F, V6541-WITNESS-27-P

### V6541-METHOD-28 — Bounded recovery for batch_cat_file_pipe_deadlock_timeout

- Trigger: batch_cat_file_pipe_deadlock_timeout
- Method: Retain the timeout, terminate only the owned helper processes, use communicate for concurrent pipe handling, and parse the bounded returned byte stream deterministically.
- Recurrence guard: Use subprocess communicate rather than write-then-read for multi-object Git batch protocols on Windows.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-28-F, V6541-WITNESS-28-P

### V6541-METHOD-29 — Bounded recovery for inherited_scanner_definition_false_positive

- Trigger: inherited_scanner_definition_false_positive
- Method: Retain the failed scan and quarantine only the exact earlier scanner-definition files before rescanning the complete owner surface.
- Recurrence guard: Carry every phase-local scanner implementation and its own receipt in an explicit definition allowlist without exempting payload files.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-29-F, V6541-WITNESS-29-P

### V6541-METHOD-30 — Bounded recovery for generated_markdown_trailing_space_diff_hygiene

- Trigger: generated_markdown_trailing_space_diff_hygiene
- Method: Retain the failed hygiene check, remove the hard-break spaces in the generator, rebuild the seal, and regenerate exact manifests.
- Recurrence guard: Generate wrapped proposal bullets with explicit newlines and indentation rather than trailing Markdown spaces.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-30-F, V6541-WITNESS-30-P

### V6541-METHOD-31 — Bounded recovery for checkout_wide_unstaged_name_diff_timeout

- Trigger: checkout_wide_unstaged_name_diff_timeout
- Method: Retain the timeout and prove index-to-worktree equality with git diff-files --quiet plus owner-scoped untracked checks.
- Recurrence guard: Use plumbing-level quiet equality for large worktrees; enumerate only the owner-scoped untracked surface.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-31-F, V6541-WITNESS-31-P

### V6541-METHOD-32 — Bounded recovery for postpush_porcelain_clean_probe_timeout

- Trigger: postpush_porcelain_clean_probe_timeout
- Method: Retain the timeout in one additive terminal correction and use tracked diff-files and diff-index equality plus owner-scoped untracked checks.
- Recurrence guard: Do not use checkout-wide porcelain status as the terminal clean-state primitive on this large Windows worktree.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6541-WITNESS-32-F, V6541-WITNESS-32-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
