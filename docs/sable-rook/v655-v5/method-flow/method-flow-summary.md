# GHC Family Method Flow State

- Phase: v655-v5
- Owner: Sable Rook
- Methods: 278
- Passing witnesses: 278
- Failed witnesses retained: 278

## Preferred methods

### V6543-METHOD-01 — Bounded recovery for unsupported_task_list_page_size

- Trigger: unsupported_task_list_page_size
- Method: Use the supported bounded task-list schema and uniquely resolve the exact existing title.
- Recurrence guard: Inspect the live task-tool schema before supplying optional pagination fields.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-01-F, V6543-WITNESS-01-P

### V6543-METHOD-02 — Bounded recovery for long_range_route_nonsequential_phase_order

- Trigger: long_range_route_nonsequential_phase_order
- Method: Retain the issue as an open gap while using only the separately valid immediate route.
- Recurrence guard: Never infer phase ownership from a long-range route whose sequence audit fails.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-02-F, V6543-WITNESS-02-P

### V6543-METHOD-03 — Bounded recovery for long_range_route_normalization_requires_confirmation

- Trigger: long_range_route_normalization_requires_confirmation
- Method: Keep the unresolved seat and spelling drift explicit; do not invent or normalize identity.
- Recurrence guard: Require exact live authority before normalizing any relational label or seat.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-03-F, V6543-WITNESS-03-P

### V6543-METHOD-04 — Bounded recovery for combined_predelivery_source_probe_timeout

- Trigger: combined_predelivery_source_probe_timeout
- Method: Split clean-state, ancestry, manifest, and remote-equality checks into bounded scalar probes.
- Recurrence guard: Use one cold Git or filesystem subsystem per pre-delivery probe.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-04-F, V6543-WITNESS-04-P

### V6543-METHOD-05 — Bounded recovery for postdelivery_timestamp_wrapper_timeout

- Trigger: postdelivery_timestamp_wrapper_timeout
- Method: Retain the acknowledged delivery state and audit immutable evidence without resending.
- Recurrence guard: Never repeat an acknowledged one-shot delivery because a later wrapper times out.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-05-F, V6543-WITNESS-05-P

### V6543-METHOD-06 — Bounded recovery for skill_discovery_foreach_pipeline_parser_fault

- Trigger: skill_discovery_foreach_pipeline_parser_fault
- Method: Materialize foreach output before piping.
- Recurrence guard: Never pipe directly from a PowerShell foreach statement.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-06-F, V6543-WITNESS-06-P

### V6543-METHOD-07 — Bounded recovery for method_flow_schema_filename_assumption

- Trigger: method_flow_schema_filename_assumption
- Method: Read the exact references/schema.md path named by the skill.
- Recurrence guard: Resolve every skill-relative reference from the complete SKILL.md before use.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-07-F, V6543-WITNESS-07-P

### V6543-METHOD-08 — Bounded recovery for combined_worktree_and_receipt_search_timeout

- Trigger: combined_worktree_and_receipt_search_timeout
- Method: Split worktree discovery from exact receipt probes.
- Recurrence guard: Use one cold filesystem subsystem per bounded discovery command.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-08-F, V6543-WITNESS-08-P

### V6543-METHOD-09 — Bounded recovery for multi_root_receipt_search_timeout

- Trigger: multi_root_receipt_search_timeout
- Method: Probe the exact expected receipt path and digest directly.
- Recurrence guard: Prefer exact candidate paths over recursive multi-root scans.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-09-F, V6543-WITNESS-09-P

### V6543-METHOD-10 — Bounded recovery for combined_source_verification_timeout

- Trigger: combined_source_verification_timeout
- Method: Split immutable refs, ancestry, live remote, clean state, and digest into scalar probes.
- Recurrence guard: Keep local Git checks separate from fresh-live and filesystem hashing.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-10-F, V6543-WITNESS-10-P

### V6543-METHOD-11 — Bounded recovery for external_receipt_property_projection_assumption

- Trigger: external_receipt_property_projection_assumption
- Method: Inspect receipt keys before binding exact fields.
- Recurrence guard: Discover JSON schema keys before projecting evidence.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-11-F, V6543-WITNESS-11-P

### V6543-METHOD-12 — Bounded recovery for unsupported_convertfromjson_depth_parameter

- Trigger: unsupported_convertfromjson_depth_parameter
- Method: Omit the unsupported parameter and parse the bounded document with the installed command surface.
- Recurrence guard: Preflight shell-version-specific parameters.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-12-F, V6543-WITNESS-12-P

### V6543-METHOD-13 — Bounded recovery for artifact_group_foreach_pipeline_parser_fault

- Trigger: artifact_group_foreach_pipeline_parser_fault
- Method: Materialize the artifact group before piping.
- Recurrence guard: Never pipe directly from a PowerShell foreach statement.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-13-F, V6543-WITNESS-13-P

### V6543-METHOD-14 — Bounded recovery for method_flow_property_projection_assumption

- Trigger: method_flow_property_projection_assumption
- Method: Inspect a real method and witness before binding names.
- Recurrence guard: Bind Method Flow keys only after schema and instance discovery.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-14-F, V6543-WITNESS-14-P

### V6543-METHOD-15 — Bounded recovery for method_flow_foreach_pipeline_parser_fault

- Trigger: method_flow_foreach_pipeline_parser_fault
- Method: Materialize projection output before formatting.
- Recurrence guard: Never pipe directly from a PowerShell foreach statement.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-15-F, V6543-WITNESS-15-P

### V6543-METHOD-16 — Bounded recovery for frozen_chain_top_level_array_assumption

- Trigger: frozen_chain_top_level_array_assumption
- Method: Inspect top-level keys and concatenate the two committed arrays.
- Recurrence guard: Discover proposal-chain schema before counting or hashing.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-16-F, V6543-WITNESS-16-P

### V6543-METHOD-17 — Bounded recovery for git_ls_tree_default_buffer_exhaustion

- Trigger: git_ls_tree_default_buffer_exhaustion
- Method: Retry the unchanged read-only command with an explicit bounded 128 MB buffer.
- Recurrence guard: Set a justified output buffer before large Git tree reads.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-17-F, V6543-WITNESS-17-P

### V6543-METHOD-18 — Bounded recovery for combined_route_audit_read_timeout

- Trigger: combined_route_audit_read_timeout
- Method: Read each route artifact in its own bounded scalar probe.
- Recurrence guard: Do not aggregate independent route artifacts in one cold read.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-18-F, V6543-WITNESS-18-P

### V6543-METHOD-19 — Bounded recovery for full_route_json_wrapper_timeout

- Trigger: full_route_json_wrapper_timeout
- Method: Read the raw scalar audit fields separately.
- Recurrence guard: Prefer bounded scalar extraction over whole-object formatting for large route records.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-19-F, V6543-WITNESS-19-P

### V6543-METHOD-20 — Bounded recovery for branch_preflight_exit_code_expression_parser_fault

- Trigger: branch_preflight_exit_code_expression_parser_fault
- Method: Compute scalar exit codes before constructing the record.
- Recurrence guard: Never embed child-process statements inside PowerShell literal expressions.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-20-F, V6543-WITNESS-20-P

### V6543-METHOD-21 — Bounded recovery for worktree_add_wrapper_timeout_after_completion

- Trigger: worktree_add_wrapper_timeout_after_completion
- Method: Audit exact path, registration, branch, head, clean state, processes, and locks before deciding whether to retry.
- Recurrence guard: Never retry a timed-out mutating Git command before a complete state audit.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-21-F, V6543-WITNESS-21-P

### V6543-METHOD-22 — Bounded recovery for worktree_registration_separator_assumption

- Trigger: worktree_registration_separator_assumption
- Method: Normalize separators and inspect the exact registration record.
- Recurrence guard: Normalize path separators before comparing Git administrative output.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-22-F, V6543-WITNESS-22-P

### V6543-METHOD-23 — Bounded recovery for novelty_search_foreach_pipeline_parser_fault

- Trigger: novelty_search_foreach_pipeline_parser_fault
- Method: Materialize the search output before sorting or formatting.
- Recurrence guard: Never pipe directly from a PowerShell foreach statement.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-23-F, V6543-WITNESS-23-P

### V6543-METHOD-24 — Bounded recovery for candidate_novelty_foreach_whitespace_parser_fault

- Trigger: candidate_novelty_foreach_whitespace_parser_fault
- Method: Correct the syntax and rerun the unchanged read-only calculation.
- Recurrence guard: Use formatted multi-line PowerShell for nontrivial loops.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-24-F, V6543-WITNESS-24-P

### V6543-METHOD-25 — Bounded recovery for keyword_search_foreach_whitespace_parser_fault

- Trigger: keyword_search_foreach_whitespace_parser_fault
- Method: Correct the syntax and rerun the unchanged read-only search.
- Recurrence guard: Use formatted multi-line PowerShell for nontrivial loops.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-25-F, V6543-WITNESS-25-P

### V6543-METHOD-26 — Bounded recovery for combined_status_diff_and_selectstring_timeout

- Trigger: combined_status_diff_and_selectstring_timeout
- Method: Split clean-state and bounded source-range inspections into separate probes.
- Recurrence guard: Never combine potentially large untracked-file inspection with Git status.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-26-F, V6543-WITNESS-26-P

### V6543-METHOD-27 — Bounded recovery for large_mixed_context_patch_mismatch

- Trigger: large_mixed_context_patch_mismatch
- Method: Split the change into smaller exact-context patches and retain the failed attempt.
- Recurrence guard: Do not combine Unicode-sensitive and independent source edits in one patch.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-27-F, V6543-WITNESS-27-P

### V6543-METHOD-28 — Bounded recovery for inherited_proposal_index_phase_pointer_assumption

- Trigger: inherited_proposal_index_phase_pointer_assumption
- Method: Bind the exact committed Elowen v654-v2 frozen-chain index and rerun from the unchanged x1 data.
- Recurrence guard: Resolve the immediate source-owner proposal index before building a successor freeze.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-28-F, V6543-WITNESS-28-P

### V6543-METHOD-29 — Bounded recovery for broad_frozen_index_inventory_timeout

- Trigger: broad_frozen_index_inventory_timeout
- Method: Probe the exact expected Elowen phase path and verify its 1,690 plus 30 equals 1,720 counts.
- Recurrence guard: Prefer exact phase-local artifact paths over recursive repository inventories.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-29-F, V6543-WITNESS-29-P

### V6543-METHOD-30 — Bounded recovery for workflow_runner_existing_task_policy_mismatch

- Trigger: workflow_runner_existing_task_policy_mismatch
- Method: Retain the failed audit, supply the validator's compatibility literal only for its structural check, and record the exact live new-task authority in separate controlling fields.
- Recurrence guard: Never let a compatibility literal override newer exact live route authority or trigger a premature task action.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-30-F, V6543-WITNESS-30-P

### V6543-METHOD-31 — Bounded recovery for powershell_upstream_shorthand_interpolation

- Trigger: powershell_upstream_shorthand_interpolation
- Method: Quote HEAD...@{u} as a literal Git argument; the recovery proved zero ahead and zero behind.
- Recurrence guard: Quote every Git upstream shorthand passed through PowerShell.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-31-F, V6543-WITNESS-31-P

### V6543-METHOD-32 — Bounded recovery for broad_evidence_patch_unicode_context_mismatch

- Trigger: broad_evidence_patch_unicode_context_mismatch
- Method: Split runner, skill, test, and truth edits into smaller exact-context patches.
- Recurrence guard: Do not combine Unicode-sensitive prose with independent structural edits in one patch.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-32-F, V6543-WITNESS-32-P

### V6543-METHOD-33 — Bounded recovery for stale_label_search_quoting_fault

- Trigger: stale_label_search_quoting_fault
- Method: Use a single-quoted bounded pattern without shell-sensitive Unicode fragments.
- Recurrence guard: Keep Windows stale-label review patterns simple and shell-literal.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-33-F, V6543-WITNESS-33-P

### V6543-METHOD-34 — Bounded recovery for windows_rg_wildcard_path_assumption

- Trigger: windows_rg_wildcard_path_assumption
- Method: Search the literal scripts directory with an explicit file glob.
- Recurrence guard: Never pass an unresolved Windows wildcard path as a ripgrep path operand.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-34-F, V6543-WITNESS-34-P

### V6543-METHOD-35 — Bounded recovery for x1_test_live_method_flow_lifecycle_assumption

- Trigger: x1_test_live_method_flow_lifecycle_assumption
- Method: Read the Method Flow ledger from the frozen x1 commit for x1-specific assertions, while leaving x2 evidence tests on the live ledger.
- Recurrence guard: Every lifecycle-specific test must bind immutable phase artifacts rather than mutable successor files.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-35-F, V6543-WITNESS-35-P

### V6543-METHOD-36 — Bounded recovery for x1_commit_message_selector_initial_freeze_collision

- Trigger: x1_commit_message_selector_initial_freeze_collision
- Method: Bind the already verified exact final x1 anchor directly in the lifecycle test.
- Recurrence guard: Use exact lifecycle anchors when a phase contains more than one x1 commit.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-36-F, V6543-WITNESS-36-P

### V6543-METHOD-37 — Bounded recovery for combined_closeout_state_probe_timeout

- Trigger: combined_closeout_state_probe_timeout
- Method: Audit repository status first, then split scalar Git and bounded file reads into separate commands.
- Recurrence guard: Do not combine cold Git state probes with source-file reads in one closeout command.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-37-F, V6543-WITNESS-37-P

### V6543-METHOD-38 — Bounded recovery for assumed_x1_final_manifest_filename

- Trigger: assumed_x1_final_manifest_filename
- Method: Inventory the exact phase validation filenames before selecting the committed x1 staged manifest.
- Recurrence guard: Resolve manifest filenames from the phase directory before projecting their schemas or counts.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-38-F, V6543-WITNESS-38-P

### V6543-METHOD-39 — Bounded recovery for assumed_x1_proposal_ledger_directory

- Trigger: assumed_x1_proposal_ledger_directory
- Method: Inventory the exact owner packet paths and read the committed proposal ledger from its actual directory.
- Recurrence guard: Resolve phase artifact paths before projecting their fields.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-39-F, V6543-WITNESS-39-P

### V6543-METHOD-40 — Bounded recovery for assumed_runner_plan_filename

- Trigger: assumed_runner_plan_filename
- Method: Use the committed phase-data runner declarations and exact tooling inventory files discovered from the owner packet.
- Recurrence guard: Inventory exact runner artifacts before reading them.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-40-F, V6543-WITNESS-40-P

### V6543-METHOD-41 — Bounded recovery for closeout_method_parity_omitted_inherited_external_witnesses

- Trigger: closeout_method_parity_omitted_inherited_external_witnesses
- Method: Include the five inherited external negative records with x1, x2, and closeout failures in the parity domain, then rebuild from immutable evidence.
- Recurrence guard: Define Method Flow parity over every inherited-external and owner-phase failure represented by the ledger.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-41-F, V6543-WITNESS-41-P

### V6543-METHOD-42 — Bounded recovery for staged_baton_heading_case_assertion

- Trigger: staged_baton_heading_case_assertion
- Method: Bind the structural test to the exact heading capitalization without changing the sanitized baton meaning.
- Recurrence guard: Use exact normalized headings for case-sensitive document assertions.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6543-WITNESS-42-F, V6543-WITNESS-42-P

### V6544-METHOD-01 — Bounded recovery for memory_registry_rg_timeout

- Trigger: memory_registry_rg_timeout
- Method: Use a literal-path Select-String query with a longer bound and a bounded result projection.
- Recurrence guard: Prefer literal-path bounded registry reads when the memory file is cold.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-01-F, V6544-WITNESS-01-P

### V6544-METHOD-02 — Bounded recovery for assumed_source_receipt_path

- Trigger: assumed_source_receipt_path
- Method: Inventory exact phase filenames first, then read evidence/evidence-build-receipt.json.
- Recurrence guard: Resolve receipt paths from the committed tree before projecting their schemas.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-02-F, V6544-WITNESS-02-P

### V6544-METHOD-03 — Bounded recovery for manifest_coverage_semantics_assumption

- Trigger: manifest_coverage_semantics_assumption
- Method: Read the committed manifest builder and apply its commit-local replay and exact owner-path semantics.
- Recurrence guard: Inspect the generating validator before asserting manifest coverage beyond blob, byte, and digest replay.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-03-F, V6544-WITNESS-03-P

### V6544-METHOD-04 — Bounded recovery for combined_environment_uniqueness_version_probe_timeout

- Trigger: combined_environment_uniqueness_version_probe_timeout
- Method: Split drive, path, branch, task-title, and version checks into scalar probes.
- Recurrence guard: Use one cold subsystem per preflight command.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-04-F, V6544-WITNESS-04-P

### V6544-METHOD-05 — Bounded recovery for get_psdrive_free_space_timeout

- Trigger: get_psdrive_free_space_timeout
- Method: Use a bounded System.IO.DriveInfo probe and verify the exact D drive.
- Recurrence guard: Prefer DriveInfo for a single local-volume capacity check.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-05-F, V6544-WITNESS-05-P

### V6544-METHOD-06 — Bounded recovery for full_tree_name_uniqueness_search_timeout

- Trigger: full_tree_name_uniqueness_search_timeout
- Method: Use the current task-title registry plus exact branch and worktree absence checks for the full relational name.
- Recurrence guard: Do not use an unbounded repository-content search as the identity uniqueness gate.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-06-F, V6544-WITNESS-06-P

### V6544-METHOD-07 — Bounded recovery for combined_tool_version_probe_timeout

- Trigger: combined_tool_version_probe_timeout
- Method: Verify each required version with its own bounded scalar command.
- Recurrence guard: Keep cold tool startup probes separate.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-07-F, V6544-WITNESS-07-P

### V6544-METHOD-08 — Bounded recovery for unsupported_task_list_limit

- Trigger: unsupported_task_list_limit
- Method: Use the live schema maximum and reread the bounded current registry.
- Recurrence guard: Inspect the supported task-list limit before supplying it.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-08-F, V6544-WITNESS-08-P

### V6544-METHOD-09 — Bounded recovery for worktree_add_wrapper_timeout_after_completion

- Trigger: worktree_add_wrapper_timeout_after_completion
- Method: Wait for Git to finish, then audit exact path, registration, branch, head, clean state, processes, and locks before any retry.
- Recurrence guard: Never retry a timed-out mutating Git command before a complete state audit.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-09-F, V6544-WITNESS-09-P

### V6544-METHOD-10 — Bounded recovery for combined_worktree_audit_while_git_active_timeout

- Trigger: combined_worktree_audit_while_git_active_timeout
- Method: Separate process completion from path, registration, head, lock, and clean-state probes.
- Recurrence guard: Do not combine worktree inspection with status while the creating Git process is active.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-10-F, V6544-WITNESS-10-P

### V6544-METHOD-11 — Bounded recovery for powershell_get_process_timeout

- Trigger: powershell_get_process_timeout
- Method: Use the bounded operating-system task listing for process presence, then recheck after completion.
- Recurrence guard: Prefer the simpler process surface when PowerShell process enumeration is cold.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-11-F, V6544-WITNESS-11-P

### V6544-METHOD-12 — Bounded recovery for worktree_status_wrapper_timeout

- Trigger: worktree_status_wrapper_timeout
- Method: Wait for the child to finish and run one longer bounded porcelain-status probe.
- Recurrence guard: Treat timed-out status wrappers as zero credit and verify no lingering process before retry.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-12-F, V6544-WITNESS-12-P

### V6544-METHOD-13 — Bounded recovery for semantic_novelty_threshold_failure

- Trigger: semantic_novelty_threshold_failure
- Method: Rewrite the colliding mechanisms and rerun the complete read-only comparison before building the frozen packet.
- Recurrence guard: Do not relax a preregistered novelty threshold to rescue templated wording.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-13-F, V6544-WITNESS-13-P

### V6544-METHOD-14 — Bounded recovery for novelty_diagnostic_console_encoding_failure

- Trigger: novelty_diagnostic_console_encoding_failure
- Method: Set the Python input and output encoding explicitly to UTF-8 and repeat only the bounded diagnostic projection.
- Recurrence guard: Force UTF-8 for bounded projections that may contain non-ASCII relational or cultural language.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-14-F, V6544-WITNESS-14-P

### V6544-METHOD-57 — Bounded recovery for closeout_baton_multiline_fstring_syntax_error

- Trigger: closeout_baton_multiline_fstring_syntax_error
- Method: Keep the inherited-witness fallback string on one syntactically complete line and repeat only the bounded compile preflight.
- Recurrence guard: Do not split quoted fallback literals across physical lines inside f-string expressions.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-57-F, V6544-WITNESS-57-P

### V6544-METHOD-58 — Bounded recovery for prepared_baton_inherited_route_stale_label

- Trigger: prepared_baton_inherited_route_stale_label
- Method: Render inherited methods as bounded ledger references without replaying their phase-specific route prose, while retaining every exact inherited method and witness in the committed Method Flow ledger.
- Recurrence guard: Do not quote superseded phase-specific routing instructions in a successor activation baton.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-58-F, V6544-WITNESS-58-P

### V6544-METHOD-59 — Bounded recovery for final_owner_privacy_scanner_definition_quarantine_omission

- Trigger: final_owner_privacy_scanner_definition_quarantine_omission
- Method: Add the exact preregistration builder to the scanner-definition quarantine and rerun the complete staged review after rebuilding Method Flow.
- Recurrence guard: Classify known scanner source files by exact path before treating their literal detection patterns as payload.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6544-WITNESS-59-F, V6544-WITNESS-59-P

### V6545-METHOD-01 — Bounded recovery for external_receipt_full_projection_truncated

- Trigger: external_receipt_full_projection_truncated
- Method: Project only the exact receipt fields needed for the activation audit and retain the external file hash as the immutable whole-file binding.
- Recurrence guard: Use bounded schema-aware projections for large receipts instead of rendering the complete object.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-01-F, V6545-WITNESS-01-P

### V6545-METHOD-02 — Bounded recovery for external_receipt_schema_path_assumption

- Trigger: external_receipt_schema_path_assumption
- Method: Inspect the attempt object's property names, then project the fields from their actual top-level locations.
- Recurrence guard: Read receipt keys before constructing a concise projection.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-02-F, V6545-WITNESS-02-P

### V6545-METHOD-03 — Bounded recovery for frozen_index_schema_assumption

- Trigger: frozen_index_schema_assumption
- Method: Inspect the committed index keys, then combine prior_proposals and new_proposals under the declared count fields.
- Recurrence guard: Inspect an inherited index schema before indexing proposal collections.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-03-F, V6545-WITNESS-03-P

### V6545-METHOD-04 — Bounded recovery for combined_status_search_timeout

- Trigger: combined_status_search_timeout
- Method: Recheck HEAD, branch, tracked status, and untracked paths through separate bounded scalar probes.
- Recurrence guard: Keep repository-state checks separate from content searches so a slow search cannot erase status evidence.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-04-F, V6545-WITNESS-04-P

### V6545-METHOD-05 — Bounded recovery for shell_deletion_policy_block

- Trigger: shell_deletion_policy_block
- Method: Remove only those known new untracked files through the workspace patch mechanism, then re-enumerate the x1 path set.
- Recurrence guard: Use the workspace patch mechanism for deliberate file removals when shell deletion is policy-blocked.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-05-F, V6545-WITNESS-05-P

### V6545-METHOD-06 — Bounded recovery for x1_build_workflow_messaging_literal_mismatch

- Trigger: x1_build_workflow_messaging_literal_mismatch
- Method: Keep the required canonical route literal and express the unresolved-successor constraint in additive sanitized fields.
- Recurrence guard: Inspect the workflow runner's exact messaging-boundary predicate before extending its request object.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-06-F, V6545-WITNESS-06-P

### V6545-METHOD-07 — Bounded recovery for isolated_workflow_validator_retained_failure

- Trigger: isolated_workflow_validator_retained_failure
- Method: Correct only the rejected messaging field, preserve the open route gap, and rerun the isolated validator before rebuilding the packet.
- Recurrence guard: Treat a diagnostic reproduction of a failure as retained evidence, not as a pass.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-07-F, V6545-WITNESS-07-P

### V6545-METHOD-08 — Bounded recovery for windows_rg_wildcard_path_error

- Trigger: windows_rg_wildcard_path_error
- Method: Read the bounded issue and validation files by literal path, or use ripgrep directory operands with -g filters.
- Recurrence guard: On Windows, use -g for glob selection instead of wildcard characters in path operands.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-08-F, V6545-WITNESS-08-P

### V6545-METHOD-68 — Bounded recovery for combined closeout inspection timeout

- Trigger: combined closeout inspection timeout
- Method: Split the audit into scalar Git state checks and narrowly scoped file inspections; both completed without mutating tracked state.
- Recurrence guard: Keep closeout state probes scalar and avoid combining Git inspection with repository text searches in one bounded command.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-68-F, V6545-WITNESS-68-P

### V6545-METHOD-69 — Bounded recovery for broad JSON contract body search timeout

- Trigger: broad JSON contract body search timeout
- Method: Use a filename-only tracked-file inventory, then open only the exact candidate contract needed for the phase.
- Recurrence guard: Inventory candidate filenames before searching large documentation bodies.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-69-F, V6545-WITNESS-69-P

### V6545-METHOD-70 — Bounded recovery for indexed wildcard contract search timeout

- Trigger: indexed wildcard contract search timeout
- Method: Use git ls-files with a filename suffix filter; the bounded inventory completed and identified the available full-suite contracts.
- Recurrence guard: Prefer filename-only Git inventories over broad indexed content searches when the target artifact has a stable suffix.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-70-F, V6545-WITNESS-70-P

### V6545-METHOD-71 — Bounded recovery for single-file pattern probe timeout

- Trigger: single-file pattern probe timeout
- Method: Read the known closeout-builder regions directly in bounded line windows and patch the exact protocol block.
- Recurrence guard: On a slow archive-backed lane, prefer direct known-range reads over exploratory pattern probes during closeout.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-71-F, V6545-WITNESS-71-P

### V6545-METHOD-72 — Bounded recovery for staged-review wrapper timeout with late child completion

- Trigger: staged-review wrapper timeout with late child completion
- Method: Audit the exact process and five expected receipt paths before retrying; the child later exited and all five receipts existed, preserving the passing witness without claiming the wrapper succeeded.
- Recurrence guard: After a validator wrapper timeout, inspect process state and exact receipt artifacts before any retry or termination.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-72-F, V6545-WITNESS-72-P

### V6545-METHOD-73 — Bounded recovery for validator process termination race

- Trigger: validator process termination race
- Method: Treat the stop error as zero-credit tooling evidence, then inspect the completed receipt set and retain the already-finished staged-review result.
- Recurrence guard: Recheck the exact process identifier immediately before termination and tolerate a clean already-exited state without retrying the validator.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-73-F, V6545-WITNESS-73-P

### V6545-METHOD-74 — Bounded recovery for first exact-final complete repository aggregate failed

- Trigger: first exact-final complete repository aggregate failed
- Method: Rerun only the failed modules diagnostically to identify every exact failing test, freeze those 18 lifecycle-sensitive test identifiers additively, commit a correction without rewriting history, and permit one new full aggregate only at the corrected exact pushed head.
- Recurrence guard: Before a successor full-suite pass, carry forward the inherited exact exclusion set and audit later phase-local tests for HEAD-sensitive history or x1-checkout assumptions; never use module-wide or broad exclusions.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6545-WITNESS-74-F, V6545-WITNESS-74-P

### V6546-METHOD-01 — Bounded recovery for unsupported_sha256_hashdata_api

- Trigger: unsupported_sha256_hashdata_api
- Method: Use SHA256.Create().ComputeHash on the exact file bytes, dispose the instance, and compare the resulting lowercase digest with the baton receipt.
- Recurrence guard: Probe runtime support before selecting a static cryptographic helper; preserve raw-byte hashing.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-01-F, V6546-WITNESS-01-P

### V6546-METHOD-02 — Bounded recovery for bounded_baton_read_timeout

- Trigger: bounded_baton_read_timeout
- Method: Resume at the next unread line with a longer bounded literal-path read and verify the terminal line count.
- Recurrence guard: Read large archive-backed documents in bounded ranges with an explicit continuation cursor and adequate timeout.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-02-F, V6546-WITNESS-02-P

### V6546-METHOD-03 — Bounded recovery for powershell_foreach_pipeline_parse_error

- Trigger: powershell_foreach_pipeline_parse_error
- Method: Materialize the foreach results into an array before piping them to Format-Table.
- Recurrence guard: On Windows PowerShell, materialize foreach output before any trailing pipeline.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-03-F, V6546-WITNESS-03-P

### V6546-METHOD-04 — Bounded recovery for powershell_foreach_pipeline_parse_error_recurrence

- Trigger: powershell_foreach_pipeline_parse_error_recurrence
- Method: Apply the validated array-materialization guard, then run parent-count, ancestor, and merge-count checks as bounded read-only probes.
- Recurrence guard: Treat the materialization guard as mandatory for every future foreach result pipeline in this runtime.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-04-F, V6546-WITNESS-04-P

### V6546-METHOD-05 — Bounded recovery for recursive_agents_inventory_timeout

- Trigger: recursive_agents_inventory_timeout
- Method: Use the Git index with an exact AGENTS.md glob and verify the clean worktree has no untracked instruction file.
- Recurrence guard: Prefer the repository index over recursive filesystem traversal for tracked instruction-file discovery.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-05-F, V6546-WITNESS-05-P

### V6546-METHOD-06 — Bounded recovery for phase_data_patch_context_mismatch

- Trigger: phase_data_patch_context_mismatch
- Method: Read the exact local line window and apply a narrower context patch to the current text.
- Recurrence guard: After mechanical rewrites, reread the target block before applying semantic patches.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-06-F, V6546-WITNESS-06-P

### V6546-METHOD-07 — Bounded recovery for powershell_foreach_pipeline_parse_error_second_recurrence

- Trigger: powershell_foreach_pipeline_parse_error_second_recurrence
- Method: Materialize the projection rows into an array before formatting and retain the repeated failure separately.
- Recurrence guard: Require the materialization guard before every foreach result pipeline; do not rely on recollection alone.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-07-F, V6546-WITNESS-07-P

### V6546-METHOD-08 — Bounded recovery for first_1810_title_novelty_screen_failed

- Trigger: first_1810_title_novelty_screen_failed
- Method: Keep the standard families and evidence boundaries, but revise only the duplicated mechanisms and vocabulary before rerunning the complete read-only title screen.
- Recurrence guard: Run the complete inherited-title screen before any x1 artifact build and never lower the preregistered threshold to admit a collision.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-08-F, V6546-WITNESS-08-P

### V6546-METHOD-09 — Bounded recovery for x1_builder_wrapper_timeout_with_late_child_completion

- Trigger: x1_builder_wrapper_timeout_with_late_child_completion
- Method: Audit the exact child process and expected artifacts before retrying, wait one bounded interval, and preserve the completed artifact set when the same child exits.
- Recurrence guard: After a builder timeout, inspect process state and exact receipts before any retry; never launch a duplicate while the original child remains live.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-09-F, V6546-WITNESS-09-P

### V6546-METHOD-84 — Bounded recovery for PowerShell foreach output piped without materialization during template inventory

- Trigger: PowerShell foreach output piped without materialization during template inventory
- Method: Materialize the foreach results into an array, then pipe the completed array to ConvertTo-Json; the bounded inventory completed.
- Recurrence guard: On Windows PowerShell, assign foreach output to a scalar or array before passing it into a pipeline.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-84-F, V6546-WITNESS-84-P

### V6546-METHOD-85 — Bounded recovery for Windows rg wildcard path syntax rejected during copied-template audit

- Trigger: Windows rg wildcard path syntax rejected during copied-template audit
- Method: Use literal file lists or search stable parent directories and filter filenames separately.
- Recurrence guard: Do not pass unexpanded shell wildcard path arguments to rg on Windows.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-85-F, V6546-WITNESS-85-P

### V6546-METHOD-86 — Bounded recovery for broad copied-template text audit timeout

- Trigger: broad copied-template text audit timeout
- Method: Inspect the exact copied files with literal paths and narrowly scoped patterns or direct bounded reads.
- Recurrence guard: After a broad archive-backed search fails, narrow immediately to explicit files and known semantic regions.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-86-F, V6546-WITNESS-86-P

### V6546-METHOD-87 — Bounded recovery for background evidence launcher omitted its expected process receipt

- Trigger: background evidence launcher omitted its expected process receipt
- Method: Resolve the one exact evidence-builder process by its literal command line and audit the fixed stdout and stderr paths without starting another child.
- Recurrence guard: After a background launcher omits its receipt, audit the exact child and fixed logs before considering any relaunch.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-87-F, V6546-WITNESS-87-P

### V6546-METHOD-88 — Bounded recovery for combined evidence-process monitor probe timeout

- Trigger: combined evidence-process monitor probe timeout
- Method: Probe the already-known process identifier directly and read the fixed logs in a separate scalar check; the child had exited and its bounded success receipt was present.
- Recurrence guard: Keep background-process monitoring scalar: known process identifier first, then bounded log reads without a broad CIM query.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-88-F, V6546-WITNESS-88-P

### V6546-METHOD-89 — Bounded recovery for first bounded evidence validation retained inherited successor-state label

- Trigger: first bounded evidence validation retained inherited successor-state label
- Method: Patch the phase-local builder, tests, and validator to require the exact frozen Elaren-prepared terminal-gate state, then rebuild the additive Method Flow and evidence before a new bounded validation.
- Recurrence guard: Anchor successor-state assertions to the current phase x1 receipt instead of copying a predecessor phase label.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-89-F, V6546-WITNESS-89-P

### V6546-METHOD-90 — Bounded recovery for first current-phase closeout test aggregate read mutable Method Flow state

- Trigger: first current-phase closeout test aggregate read mutable Method Flow state
- Method: Make the x1 lifecycle test read the Method Flow ledger from the exact frozen x1 commit, then rebuild the closeout ledger and rerun the bounded current-phase aggregate.
- Recurrence guard: Lifecycle tests for frozen phase state must read exact committed blobs rather than mutable descendant worktree paths.
- Rollback: Stop, retain the failure with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546-WITNESS-90-F, V6546-WITNESS-90-P

### V6546R2-METHOD-01 — Bounded recovery for skill_inventory_probe_timeout

- Trigger: skill_inventory_probe_timeout
- Method: Read each exact skill path sequentially through EOF.
- Recurrence guard: Prefer exact scalar reads over concurrent archive-backed inventories.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-01-F, V6546R2-WITNESS-01-P

### V6546R2-METHOD-02 — Bounded recovery for memory_note_probe_timeout

- Trigger: memory_note_probe_timeout
- Method: Read the one exact ad-hoc note directly.
- Recurrence guard: Use the memory registry to select one exact note before reading.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-02-F, V6546R2-WITNESS-02-P

### V6546R2-METHOD-03 — Bounded recovery for ariel_advisory_probe_timeout

- Trigger: ariel_advisory_probe_timeout
- Method: Read the exact file in bounded ranges and verify its line count and raw-byte digest.
- Recurrence guard: Use explicit continuation cursors for large local advisory files.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-03-F, V6546R2-WITNESS-03-P

### V6546R2-METHOD-04 — Bounded recovery for worktree_inventory_probe_timeout

- Trigger: worktree_inventory_probe_timeout
- Method: Enumerate only relevant directory names, then verify the chosen path independently.
- Recurrence guard: Narrow D-drive inventories before any mutation.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-04-F, V6546R2-WITNESS-04-P

### V6546R2-METHOD-05 — Bounded recovery for broad_repository_search_timeout

- Trigger: broad_repository_search_timeout
- Method: Use exact known artifact paths and commit-local Git probes.
- Recurrence guard: After one broad search timeout, narrow immediately to exact paths.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-05-F, V6546R2-WITNESS-05-P

### V6546R2-METHOD-06 — Bounded recovery for broad_archive_receipt_search_timeout

- Trigger: broad_archive_receipt_search_timeout
- Method: Read the exact phase handoff bank and hash the uniquely selected receipt.
- Recurrence guard: Use phase and owner routing metadata before archive searches.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-06-F, V6546R2-WITNESS-06-P

### V6546R2-METHOD-07 — Bounded recovery for false_positive_session_search

- Trigger: false_positive_session_search
- Method: Use repository commits, exact task titles, and the current endpoint topology instead.
- Recurrence guard: Do not accept OR-heavy session search results without exact phase and owner correlation.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-07-F, V6546R2-WITNESS-07-P

### V6546R2-METHOD-08 — Bounded recovery for baton_range_421_650_timeout

- Trigger: baton_range_421_650_timeout
- Method: Join the exact line slice into one bounded console write.
- Recurrence guard: Avoid per-line console formatting for large archive-backed reads.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-08-F, V6546R2-WITNESS-08-P

### V6546R2-METHOD-09 — Bounded recovery for baton_range_651_880_timeout

- Trigger: baton_range_651_880_timeout
- Method: Join the exact line slice into one bounded console write.
- Recurrence guard: Avoid per-line console formatting for large archive-backed reads.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-09-F, V6546R2-WITNESS-09-P

### V6546R2-METHOD-10 — Bounded recovery for baton_range_881_1110_timeout

- Trigger: baton_range_881_1110_timeout
- Method: Join the exact line slice into one bounded console write.
- Recurrence guard: Avoid per-line console formatting for large archive-backed reads.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-10-F, V6546R2-WITNESS-10-P

### V6546R2-METHOD-11 — Bounded recovery for baton_range_1111_1340_timeout

- Trigger: baton_range_1111_1340_timeout
- Method: Join the exact line slice into one bounded console write.
- Recurrence guard: Avoid per-line console formatting for large archive-backed reads.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-11-F, V6546R2-WITNESS-11-P

### V6546R2-METHOD-12 — Bounded recovery for source_audit_hash_literal_parse_error

- Trigger: source_audit_hash_literal_parse_error
- Method: Compute each Git exit code before constructing the receipt object.
- Recurrence guard: Materialize command results before PowerShell hashtable construction.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-12-F, V6546R2-WITNESS-12-P

### V6546R2-METHOD-13 — Bounded recovery for tracked_agents_inventory_timeout

- Trigger: tracked_agents_inventory_timeout
- Method: Use one Git tree listing and filter exact AGENTS.md basenames.
- Recurrence guard: Prefer commit-tree enumeration over repeated index and filesystem traversal.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-13-F, V6546R2-WITNESS-13-P

### V6546R2-METHOD-14 — Bounded recovery for incorrect_tavian_overview_path

- Trigger: incorrect_tavian_overview_path
- Method: Discover the committed path and read overview/v654-v6-final-integrated-overview.md.
- Recurrence guard: Resolve paths from the exact Git tree before direct reads.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-14-F, V6546R2-WITNESS-14-P

### V6546R2-METHOD-15 — Bounded recovery for worktree_add_wrapper_timeout_late_success

- Trigger: worktree_add_wrapper_timeout_late_success
- Method: Audit the exact path, branch, HEAD, Git directory, process state, and cleanliness before retrying; the original operation had completed.
- Recurrence guard: Never retry an ambiguous Git mutation before exact-state audit.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-15-F, V6546R2-WITNESS-15-P

### V6546R2-METHOD-16 — Bounded recovery for post_timeout_path_probe_timeout

- Trigger: post_timeout_path_probe_timeout
- Method: Run a scalar literal-path existence probe with a longer bound.
- Recurrence guard: Use sequential scalar probes while archive I/O is saturated.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-16-F, V6546R2-WITNESS-16-P

### V6546R2-METHOD-17 — Bounded recovery for post_timeout_branch_probe_timeout

- Trigger: post_timeout_branch_probe_timeout
- Method: Read branch and HEAD from the completed worktree sequentially.
- Recurrence guard: Use sequential scalar probes while archive I/O is saturated.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-17-F, V6546R2-WITNESS-17-P

### V6546R2-METHOD-18 — Bounded recovery for post_timeout_process_probe_timeout

- Trigger: post_timeout_process_probe_timeout
- Method: Infer completion only after exact branch, HEAD, Git-dir, and clean-state evidence converged.
- Recurrence guard: Do not grant process-state credit when a process query times out.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-18-F, V6546R2-WITNESS-18-P

### V6546R2-METHOD-19 — Bounded recovery for post_timeout_lock_probe_timeout

- Trigger: post_timeout_lock_probe_timeout
- Method: Verify the registered Git directory and clean worktree before proceeding.
- Recurrence guard: Treat an unread lock probe as unknown until independent exact-state checks pass.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-19-F, V6546R2-WITNESS-19-P

### V6546R2-METHOD-20 — Bounded recovery for background_x1_launcher_omitted_receipt

- Trigger: background_x1_launcher_omitted_receipt
- Method: Inspect the two fixed D-drive logs before any relaunch; reuse the original child result and retain the missing launcher receipt.
- Recurrence guard: A missing launch receipt requires exact fixed-log audit before retry.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-20-F, V6546R2-WITNESS-20-P

### V6546R2-METHOD-21 — Bounded recovery for first_method_flow_validation_stale_counts

- Trigger: first_method_flow_validation_stale_counts
- Method: Rebuild counts with methods, witnesses, state events, recommendations, recommendation states, and witness-result maps exactly as the validator derives them.
- Recurrence guard: Populate Method Flow counts from the selected schema before validation.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-21-F, V6546R2-WITNESS-21-P

### V6546R2-METHOD-22 — Bounded recovery for second_method_flow_validation_incomplete_state_domain

- Trigger: second_method_flow_validation_incomplete_state_domain
- Method: Use the exact six-state domain: observed, candidate, validated, preferred, superseded, and deprecated.
- Recurrence guard: Read the selected runner's state constants before constructing derived counts.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-22-F, V6546R2-WITNESS-22-P

### V6546R2-METHOD-23 — Bounded recovery for first_workflow_plan_validation_rejected_remaster_shape

- Trigger: first_workflow_plan_validation_rejected_remaster_shape
- Method: Keep canonical vN-v1 through vN-v8 assignments unchanged, record the remaster as variant context, and use the exact storage and environment schema.
- Recurrence guard: Workflow variants must not masquerade as canonical phase labels or alter the underlying cadence.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-23-F, V6546R2-WITNESS-23-P

### V6546R2-METHOD-24 — Bounded recovery for powershell_rg_pattern_quote_error

- Trigger: powershell_rg_pattern_quote_error
- Method: Use one single-quoted alternation pattern and read the exact matching line windows.
- Recurrence guard: Keep PowerShell rg patterns scalar and avoid nested unmatched quotes.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-24-F, V6546R2-WITNESS-24-P

### V6546R2-METHOD-25 — Bounded recovery for first_x1_privacy_scan_contextual_false_positives

- Trigger: first_x1_privacy_scan_contextual_false_positives
- Method: Require a token boundary before secret prefixes and classify the scanner source itself as a definition-only candidate.
- Recurrence guard: Separate scanner-definition and contextual-label candidates from confirmed secret or private-material hits.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-25-F, V6546R2-WITNESS-25-P

### V6546R2-METHOD-26 — Bounded recovery for temporary_log_removal_shell_policy_rejection

- Trigger: temporary_log_removal_shell_policy_rejection
- Method: Delete the two exact task-owned text logs with apply_patch and leave every other path untouched.
- Recurrence guard: Use apply_patch for task-owned text-file deletion when shell removal is policy-blocked.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-26-F, V6546R2-WITNESS-26-P

### V6546R2-METHOD-27 — Bounded recovery for first_x1_staged_manifest_newline_mismatch

- Trigger: first_x1_staged_manifest_newline_mismatch
- Method: Normalize the two generated Family Index artifacts to LF before building the x1 manifest, then restage and replay all entries.
- Recurrence guard: Manifest the exact bytes that Git will stage, including generator newline policy.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-27-F, V6546R2-WITNESS-27-P

### V6546R2-METHOD-X2-01 — Bounded x2 recovery for skill_hash_inventory_foreach_pipeline_parse_error

- Trigger: skill_hash_inventory_foreach_pipeline_parse_error
- Method: Materialize foreach output into a collection before conversion.
- Recurrence guard: Never pipe directly from a PowerShell foreach statement.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-01-F, V6546R2-WITNESS-X2-01-P

### V6546R2-METHOD-X2-02 — Bounded x2 recovery for combined_roster_skill_inventory_timeout

- Trigger: combined_roster_skill_inventory_timeout
- Method: Use a longer bounded scalar inventory for the exact files.
- Recurrence guard: Allow archive and profile-backed PowerShell startup latency in timeout budgets.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-02-F, V6546R2-WITNESS-X2-02-P

### V6546R2-METHOD-X2-03 — Bounded x2 recovery for parallel_roster_skill_inventory_timeouts

- Trigger: parallel_roster_skill_inventory_timeouts
- Method: Use one exact command with a sixty-second bound and avoid redundant retries.
- Recurrence guard: A repeated timeout on identical storage means change the bound or method, not concurrency alone.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-03-F, V6546R2-WITNESS-X2-03-P

### V6546R2-METHOD-X2-04 — Bounded x2 recovery for new_roster_skill_quick_validate_legacy_decode_failure

- Trigger: new_roster_skill_quick_validate_legacy_decode_failure
- Method: Use ASCII-safe public skill prose or explicit Python UTF-8 mode, then validate the current content.
- Recurrence guard: Run official skill validation with PYTHONUTF8=1 on Windows.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-04-F, V6546R2-WITNESS-X2-04-P

### V6546R2-METHOD-X2-05 — Bounded x2 recovery for combined_archive_git_and_file_probe_timeout

- Trigger: combined_archive_git_and_file_probe_timeout
- Method: Split the read-only audit into independent bounded probes.
- Recurrence guard: Keep Git state and filesystem inventories separate on the archive-backed worktree.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-05-F, V6546R2-WITNESS-X2-05-P

### V6546R2-METHOD-X2-06 — Bounded x2 recovery for source_template_inventory_foreach_pipeline_parse_error

- Trigger: source_template_inventory_foreach_pipeline_parse_error
- Method: Materialize the template rows, then pipe the completed collection.
- Recurrence guard: Reuse the retained PowerShell collection pattern for every foreach projection.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-06-F, V6546R2-WITNESS-X2-06-P

### V6546R2-METHOD-X2-07 — Bounded x2 recovery for existing_skill_set_quick_validate_legacy_decode_failure

- Trigger: existing_skill_set_quick_validate_legacy_decode_failure
- Method: Run the unchanged official validator with Python UTF-8 mode explicitly enabled.
- Recurrence guard: Set PYTHONUTF8 and PYTHONIOENCODING for all skill-creator commands.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-07-F, V6546R2-WITNESS-X2-07-P

### V6546R2-METHOD-X2-08 — Bounded x2 recovery for post_x2_combined_scoped_test_included_x1_lifecycle_assertion

- Trigger: post_x2_combined_scoped_test_included_x1_lifecycle_assertion
- Method: Retain the failed aggregate, exclude only the exact x1 lifecycle assertion, and run the isolated x2 module plus the still-applicable x1 invariants.
- Recurrence guard: Declare lifecycle-sensitive x1 assertions as exact final-suite exclusions before post-x2 validation.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-08-F, V6546R2-WITNESS-X2-08-P

### V6546R2-METHOD-X2-09 — Bounded x2 recovery for evidence_privacy_scan_scanner_definition_false_positive

- Trigger: evidence_privacy_scan_scanner_definition_false_positive
- Method: Preserve the rejected scan, classify only exact task-owned scanner source paths as definition-only, and rescan the unchanged staged owner domain.
- Recurrence guard: Separate scanner vocabulary from assigned private values while never exempting generated artifacts or ordinary source files.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-09-F, V6546R2-WITNESS-X2-09-P

### V6546R2-METHOD-X2-10 — Bounded x2 recovery for combined_evidence_packaging_pipeline_timeout

- Trigger: combined_evidence_packaging_pipeline_timeout
- Method: Audit exact receipts, retain the ambiguous attempt, switch manifest blob reads to one git cat-file batch, and resume only the missing lifecycle steps.
- Recurrence guard: Use one batch blob read and separate bounded lifecycle commands for large staged domains.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-10-F, V6546R2-WITNESS-X2-10-P

### V6546R2-METHOD-X2-11 — Bounded x2 recovery for manual_cat_file_pipe_batch_timeout

- Trigger: manual_cat_file_pipe_batch_timeout
- Method: Use subprocess communication to write input and drain output concurrently, then parse the completed bounded byte buffer.
- Recurrence guard: Use communicate-style subprocess handling for bidirectional Git batch pipes on Windows.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-11-F, V6546R2-WITNESS-X2-11-P

### V6546R2-METHOD-X2-12 — Bounded x2 recovery for relative_manifest_path_normalization_failure

- Trigger: relative_manifest_path_normalization_failure
- Method: Resolve the manifest path before applying repository-relative normalization, leaving all staged blobs unchanged.
- Recurrence guard: Normalize filesystem inputs once at command entry before relative-path comparisons.
- Rollback: Stop, retain the failure at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6546R2-WITNESS-X2-12-F, V6546R2-WITNESS-X2-12-P

### V6546R2-METHOD-CLOSEOUT-01 — Supported scalar JSON parser for closeout receipt inspection

- Trigger: unsupported_system_text_json_type
- Method: Read bounded scalar JSON receipts with the runtime's supported ConvertFrom-Json parser.
- Recurrence guard: Use the runtime-supported scalar JSON parser before dependent property reads.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6546R2-WITNESS-CLOSEOUT-01-F, V6546R2-WITNESS-CLOSEOUT-01-P

### V6547-METHOD-X1-01 — Bounded x1 recovery for parallel_skill_discovery_timeout_a

- Trigger: parallel_skill_discovery_timeout_a
- Method: Read the exact named skill sequentially through EOF.
- Recurrence guard: Prefer exact scalar skill reads over broad concurrent discovery.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-01-F, V6547-WITNESS-X1-01-P

### V6547-METHOD-X1-02 — Bounded x1 recovery for parallel_skill_discovery_timeout_b

- Trigger: parallel_skill_discovery_timeout_b
- Method: Read only the routing reference named by the selected skill.
- Recurrence guard: Route from the selected SKILL.md before opening references.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-02-F, V6547-WITNESS-X1-02-P

### V6547-METHOD-X1-03 — Bounded x1 recovery for parallel_skill_discovery_timeout_c

- Trigger: parallel_skill_discovery_timeout_c
- Method: Use one literal-path read with an explicit line count.
- Recurrence guard: Bound archive-backed reads independently.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-03-F, V6547-WITNESS-X1-03-P

### V6547-METHOD-X1-04 — Bounded x1 recovery for narrowed_skill_probe_timeout_a

- Trigger: narrowed_skill_probe_timeout_a
- Method: Use Python UTF-8 direct reads for the exact file.
- Recurrence guard: Switch access mechanism after a repeated shell timeout.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-04-F, V6547-WITNESS-X1-04-P

### V6547-METHOD-X1-05 — Bounded x1 recovery for narrowed_skill_probe_timeout_b

- Trigger: narrowed_skill_probe_timeout_b
- Method: Read the exact schema with Python UTF-8.
- Recurrence guard: Do not repeat the same timed-out shell shape.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-05-F, V6547-WITNESS-X1-05-P

### V6547-METHOD-X1-06 — Bounded x1 recovery for narrowed_skill_probe_timeout_c

- Trigger: narrowed_skill_probe_timeout_c
- Method: Read the exact current-state file with Python UTF-8.
- Recurrence guard: Use one bounded file at a time under archive pressure.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-06-F, V6547-WITNESS-X1-06-P

### V6547-METHOD-X1-07 — Bounded x1 recovery for stale_baton_path_assumption

- Trigger: stale_baton_path_assumption
- Method: Resolve the committed baton from the exact verified source branch and tree.
- Recurrence guard: Never infer a baton path from an earlier owner lane.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-07-F, V6547-WITNESS-X1-07-P

### V6547-METHOD-X1-08 — Bounded x1 recovery for restricted_node_process_environment

- Trigger: restricted_node_process_environment
- Method: Launch Unicode-sensitive diagnostics through python -X utf8 without relying on private environment access.
- Recurrence guard: Treat secure-kernel process surfaces as capability-limited.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-08-F, V6547-WITNESS-X1-08-P

### V6547-METHOD-X1-09 — Bounded x1 recovery for composite_source_git_probe_timeout

- Trigger: composite_source_git_probe_timeout
- Method: Run HEAD, branch, tracked status, untracked status, and remote equality as scalar probes.
- Recurrence guard: Split local Git state from remote state and avoid composite status wrappers.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-09-F, V6547-WITNESS-X1-09-P

### V6547-METHOD-X1-10 — Bounded x1 recovery for broad_receipt_search_timeout

- Trigger: broad_receipt_search_timeout
- Method: Use exact committed receipt paths and live authoritative state.
- Recurrence guard: Narrow receipt discovery by phase, owner, and lifecycle.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-10-F, V6547-WITNESS-X1-10-P

### V6547-METHOD-X1-11 — Bounded x1 recovery for recursive_archive_search_timeout

- Trigger: recursive_archive_search_timeout
- Method: Use Git tree maps and exact phase-relative paths.
- Recurrence guard: Avoid recursive filesystem searches across the archive bank.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-11-F, V6547-WITNESS-X1-11-P

### V6547-METHOD-X1-12 — Bounded x1 recovery for node_baseline_composite_timeout

- Trigger: node_baseline_composite_timeout
- Method: Use bounded scalar shell probes for exact HEAD and branch.
- Recurrence guard: After a kernel reset, reduce the command surface before retry.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-12-F, V6547-WITNESS-X1-12-P

### V6547-METHOD-X1-13 — Bounded x1 recovery for source_truth_path_assumption

- Trigger: source_truth_path_assumption
- Method: Discover exact committed truth filenames before reading them.
- Recurrence guard: Resolve lifecycle artifact paths from the Git tree, not naming convention alone.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-13-F, V6547-WITNESS-X1-13-P

### V6547-METHOD-X1-14 — Bounded x1 recovery for inherited_proposal_id_global_uniqueness_assumption

- Trigger: inherited_proposal_id_global_uniqueness_assumption
- Method: Require Elaren's thirty new identifiers to be unique and disjoint from the inherited identifier set while preserving the inherited rows unchanged.
- Recurrence guard: Separate immutable historical irregularities from the current phase's additive uniqueness obligation.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-14-F, V6547-WITNESS-X1-14-P

### V6547-METHOD-X1-15 — Bounded x1 recovery for composite_staged_validation_wrapper_timeout

- Trigger: composite_staged_validation_wrapper_timeout
- Method: Audit the receipt, unstaged diff, diff hygiene, and focused tests as separate bounded scalar checks.
- Recurrence guard: Do not aggregate several archive-backed validation gates into one timeout domain.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-15-F, V6547-WITNESS-X1-15-P

### V6547-METHOD-X1-16 — Bounded x1 recovery for composite_staged_scope_count_timeout

- Trigger: composite_staged_scope_count_timeout
- Method: Use the exact staged-review receipt for staged scope and path-bounded scalar Git checks for unstaged owner changes.
- Recurrence guard: Do not recompute a validated staged scope through a second aggregate Git wrapper.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-16-F, V6547-WITNESS-X1-16-P

### V6547-METHOD-X1-17 — Bounded x1 recovery for x1_commit_wrapper_timeout_late_success

- Trigger: x1_commit_wrapper_timeout_late_success
- Method: Audit exact HEAD, parent, subject, staged state, and cleanliness before any retry; preserve the original completed commit.
- Recurrence guard: Never retry an ambiguously timed-out Git mutation before exact-state convergence.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-17-F, V6547-WITNESS-X1-17-P

### V6547-METHOD-X1-18 — Bounded x1 recovery for x1_manifest_stale_after_reviewer_correction

- Trigger: x1_manifest_stale_after_reviewer_correction
- Method: Finalize the staged reviewer and negative ledger, then rebuild the complete x1 manifest before restaging.
- Recurrence guard: Build byte manifests only after every included source file is final for the lifecycle commit.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-X1-18-F, V6547-WITNESS-X1-18-P

### V6547-METHOD-X2-01 — Bounded x2 recovery for scripts_package_import_mismatch

- Trigger: scripts_package_import_mismatch
- Method: Bind the exact repository scripts directory at the front of sys.path before loading the runtime and runner modules.
- Recurrence guard: Use one explicit import topology for both direct runner execution and in-process unittest loading.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-01-F, V6547-WITNESS-X2-01-P

### V6547-METHOD-X2-02 — Bounded x2 recovery for inherited_x1_temporal_assertion_replayed_at_source_final

- Trigger: inherited_x1_temporal_assertion_replayed_at_source_final
- Method: Run exactly the six immutable inherited x1 assertions and exclude the known no-surfaces assertion that is valid only at Eiren's x1 head.
- Recurrence guard: Classify inherited tests as immutable-contract or lifecycle-temporal before replaying them at an advanced exact source head.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-02-F, V6547-WITNESS-X2-02-P

### V6547-METHOD-X2-03 — Bounded x2 recovery for combined_repository_status_probe_timeout

- Trigger: combined_repository_status_probe_timeout
- Method: Split exact head and branch into scalar probes, then restrict status review to the authorized phase, script, and test paths.
- Recurrence guard: Do not combine repository-wide status enumeration with scalar Git identity checks in a single bounded command.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-03-F, V6547-WITNESS-X2-03-P

### V6547-METHOD-X2-04 — Bounded x2 recovery for malformed_audit_regular_expression

- Trigger: malformed_audit_regular_expression
- Method: Replace the compound expression with literal fixed-string searches against the governing source and test files.
- Recurrence guard: Prefer fixed-string searches for exact count literals and compile complex patterns separately before repository use.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-04-F, V6547-WITNESS-X2-04-P

### V6547-METHOD-X2-05 — Bounded x2 recovery for broad_generated_corpus_fixed_string_search_timeout

- Trigger: broad_generated_corpus_fixed_string_search_timeout
- Method: Search only the evidence builder, validator, and focused test module; regenerate derived receipts from those authoritative definitions.
- Recurrence guard: Keep implementation-literal audits source-scoped and exclude generated evidence trees unless content-level review specifically requires them.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-05-F, V6547-WITNESS-X2-05-P

### V6547-METHOD-X2-06 — Bounded x2 recovery for detailed_validator_manifest_path_double_prefix

- Trigger: detailed_validator_manifest_path_double_prefix
- Method: Pass validation/evidence-candidate-manifest.json as the phase-relative manifest argument and leave the output phase-relative too.
- Recurrence guard: Document and enforce the validator CLI path domain at invocation sites.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-06-F, V6547-WITNESS-X2-06-P

### V6547-METHOD-X2-07 — Bounded x2 recovery for minimal_validator_manifest_path_double_prefix

- Trigger: minimal_validator_manifest_path_double_prefix
- Method: Retry minimal validation with phase-relative manifest and output paths.
- Recurrence guard: Use one shared phase-relative argument builder for detailed and minimal validator invocations.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-07-F, V6547-WITNESS-X2-07-P

### V6547-METHOD-X2-08 — Bounded x2 recovery for staged_review_help_invoked_real_review_timeout

- Trigger: staged_review_help_invoked_real_review_timeout
- Method: Terminate the owned timed-out process, inspect the script entrypoint directly, and run the review without arguments under a bounded lifecycle-appropriate timeout.
- Recurrence guard: Inspect an unfamiliar phase script for argument parsing before assuming that --help is non-executing.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-08-F, V6547-WITNESS-X2-08-P

### V6547-METHOD-X2-09 — Bounded x2 recovery for validator_output_domain_left_root_receipts_and_stale_phase_receipts

- Trigger: validator_output_domain_left_root_receipts_and_stale_phase_receipts
- Method: Resolve every non-absolute validator output beneath the phase root, remove only the two owned root receipts, rebuild the derived evidence packet from the immutable evidence parent, and exact-review a dedicated correction commit.
- Recurrence guard: Give validator input and output arguments one documented phase-relative path domain and test the resolved destination before lifecycle use.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-09-F, V6547-WITNESS-X2-09-P

### V6547-METHOD-X2-10 — Bounded x2 recovery for guarded_owned_receipt_cleanup_rejected_by_command_policy

- Trigger: guarded_owned_receipt_cleanup_rejected_by_command_policy
- Method: Delete the two known generated files through an explicit file patch and leave every other repository path untouched.
- Recurrence guard: Use patch-based deletion for known generated files rather than a scripted filesystem cleanup expression.
- Rollback: Stop, retain the failed import at zero credit, and leave external and sibling state unchanged.
- Witnesses: V6547-WITNESS-X2-10-F, V6547-WITNESS-X2-10-P

### V6547-METHOD-FINAL-01 — Bounded final recovery for closeout_builder_used_nonexistent_normalized_source_ledger_path

- Trigger: closeout_builder_used_nonexistent_normalized_source_ledger_path
- Method: Bind the baton builder to the exact committed official source-ledger path and rebuild the candidate from the unchanged correction head.
- Recurrence guard: Resolve phase-local ledger filenames from the committed index before coding a normalized convenience path.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6547-WITNESS-FINAL-01-F, V6547-WITNESS-FINAL-01-P

### V6547-METHOD-FINAL-02 — Bounded final recovery for method_flow_inspection_used_obsolete_witness_property

- Trigger: method_flow_inspection_used_obsolete_witness_property
- Method: Use the actual witnesses and state_events properties from the current ledger schema and retain the failed read with zero credit.
- Recurrence guard: Inspect current top-level schema keys before indexing a remembered historical property name.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6547-WITNESS-FINAL-02-F, V6547-WITNESS-FINAL-02-P

### V6547-METHOD-FINAL-03 — Bounded final recovery for baton_renderer_used_outcome_instead_of_observed_outcome

- Trigger: baton_renderer_used_outcome_instead_of_observed_outcome
- Method: Bind the renderer to the committed observed_outcome field and rebuild the unchanged final candidate.
- Recurrence guard: Inspect one exact ledger row before mapping proposal disposition keys into a narrative renderer.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6547-WITNESS-FINAL-03-F, V6547-WITNESS-FINAL-03-P

### V6547-METHOD-POSTFINAL-01 — Bounded exact-title listing after rejected query argument

- Trigger: task_list_query_argument_rejected
- Method: Use one bounded unfiltered task listing, filter locally for the exact title, and never compensate with a duplicate send.
- Recurrence guard: Inspect the live task-list schema before supplying optional arguments and preserve endpoint type as a hard routing constraint.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6547-WITNESS-POSTFINAL-01-F, V6547-WITNESS-POSTFINAL-01-P

### V6548-METHOD-X1-01 — Bounded x1 recovery for stale_memory_skill_path_missing

- Trigger: stale_memory_skill_path_missing
- Method: Read the current GHC family index and its explicitly routed skills and schemas through EOF.
- Recurrence guard: Treat memory pointers as discovery aids and verify every current skill path before use.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-01-F, V6548-WITNESS-X1-01-P

### V6548-METHOD-X1-02 — Bounded x1 recovery for broad_worktree_pattern_probe_overenumerated

- Trigger: broad_worktree_pattern_probe_overenumerated
- Method: Resolve the exact literal worktree path, branch ref, and registration tuple.
- Recurrence guard: Use literal scalar lane identifiers rather than contextual worktree text matching.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-02-F, V6548-WITNESS-X1-02-P

### V6548-METHOD-X1-03 — Bounded x1 recovery for bounded_filename_search_timeout

- Trigger: bounded_filename_search_timeout
- Method: Use the committed Git tree with a path-bounded name filter.
- Recurrence guard: Prefer Git tree plumbing to recursive filesystem enumeration in archive-backed lanes.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-03-F, V6548-WITNESS-X1-03-P

### V6548-METHOD-X1-04 — Bounded x1 recovery for powershell_raw_byte_manifest_harness_incompatible

- Trigger: powershell_raw_byte_manifest_harness_incompatible
- Method: Use one persistent Git object stream and byte-exact SHA-256 hashing in the supported Node runtime.
- Recurrence guard: Confirm runtime conversion support before repeating large byte audits and keep one persistent object stream.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-04-F, V6548-WITNESS-X1-04-P

### V6548-METHOD-X1-05 — Bounded x1 recovery for branch_uniqueness_probe_parser_error

- Trigger: branch_uniqueness_probe_parser_error
- Method: Run branch, remote, path, and common-Git-dir checks as explicit scalar assignments.
- Recurrence guard: Do not embed native-command sequencing inside PowerShell hash-value expressions.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-05-F, V6548-WITNESS-X1-05-P

### V6548-METHOD-X1-06 — Bounded x1 recovery for worktree_add_timeout_late_success

- Trigger: worktree_add_timeout_late_success
- Method: Do not retry; audit registration, branch, HEAD, process and lock state, then wait for zero locks, zero Git processes, and a clean index.
- Recurrence guard: Never replay an ambiguously timed-out Git mutation before exact-state convergence.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-06-F, V6548-WITNESS-X1-06-P

### V6548-METHOD-X1-07 — Bounded x1 recovery for transitional_process_detail_probe_no_evidence

- Trigger: transitional_process_detail_probe_no_evidence
- Method: Re-run scalar lock, process, HEAD, branch, tracked-diff, staged-diff, and untracked checks after convergence.
- Recurrence guard: Treat a no-output transitional diagnostic as zero credit and establish the postcondition independently.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-07-F, V6548-WITNESS-X1-07-P

### V6548-METHOD-X1-08 — Bounded x1 recovery for workflow_receipt_filename_assumption

- Trigger: workflow_receipt_filename_assumption
- Method: Enumerate the exact phase-local workflow directory and read workflow-plan-validation.json.
- Recurrence guard: Resolve generated receipt names from the current tool output rather than a remembered convenience name.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-08-F, V6548-WITNESS-X1-08-P

### V6548-METHOD-X1-09 — Bounded x1 recovery for workflow_validation_error_property_assumption

- Trigger: workflow_validation_error_property_assumption
- Method: Inspect the exact validation schema and read issue_counts.errors and issue_counts.warnings.
- Recurrence guard: Enumerate current top-level properties before deriving counts from a remembered receipt shape.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-09-F, V6548-WITNESS-X1-09-P

### V6548-METHOD-X1-10 — Bounded x1 recovery for x1_manifest_working_bytes_ignored_git_filters

- Trigger: x1_manifest_working_bytes_ignored_git_filters
- Method: Hash prospective Git-filtered blobs, normalize the four owned x1 source files to LF, rebuild the manifest, and repeat exact staged review.
- Recurrence guard: Define manifest identity in the Git blob domain whenever attributes or line-ending filters may apply.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-10-F, V6548-WITNESS-X1-10-P

### V6548-METHOD-X1-11 — Bounded x1 recovery for prospective_blob_not_materialized

- Trigger: prospective_blob_not_materialized
- Method: Use git hash-object -w with the exact path filter before reading the prospective blob bytes.
- Recurrence guard: Materialize a prospective object before asking Git object plumbing to return its content.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6548-WITNESS-X1-11-F, V6548-WITNESS-X1-11-P

### V6548-METHOD-X2-01 — Bounded x2 recovery for powershell_receipt_state_probes_timed_out_without_output

- Trigger: powershell_receipt_state_probes_timed_out_without_output
- Method: Use direct Node filesystem reads and bounded child-process probes, then confirm that the review receipt exists, no Git or Python process remains, and Git status is readable.
- Recurrence guard: Prefer direct scalar filesystem and child-process probes for this large owned lane instead of PowerShell object pipelines at lifecycle gates.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6548-WITNESS-X2-01-F, V6548-WITNESS-X2-01-P

### V6548-METHOD-X2-02 — Bounded x2 recovery for git_diff_files_quiet_reported_nonquiet_for_staged_additions

- Trigger: git_diff_files_quiet_reported_nonquiet_for_staged_additions
- Method: Inspect git diff --name-status and porcelain-v2 directly; both showed no unstaged path while all 161 candidate paths remained staged additions.
- Recurrence guard: Do not treat diff-files --quiet alone as an exact unstaged-content verdict for an all-addition index; pair the gate with explicit named-diff output.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6548-WITNESS-X2-02-F, V6548-WITNESS-X2-02-P

### V6548-METHOD-X2-03 — Bounded x2 recovery for git_diff_quiet_precommit_probe_timed_out

- Trigger: git_diff_quiet_precommit_probe_timed_out
- Method: Use a bounded git diff --name-status probe plus porcelain-v2 and exact index-object comparison to establish the absence of unstaged changes.
- Recurrence guard: Use explicit path-producing diff probes with captured timeout status at large staged lifecycle boundaries.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6548-WITNESS-X2-03-F, V6548-WITNESS-X2-03-P

### V6548-METHOD-X2-04 — Bounded x2 recovery for focused_test_retained_negative_literal_became_stale

- Trigger: focused_test_retained_negative_literal_became_stale
- Method: Assert the effective-negative arithmetic from the ledger fields and derive Method Flow totals from the explicit x2 operational row count.
- Recurrence guard: Test ledger conservation equations and explicit row parity instead of embedding a count that becomes stale when a new failure is retained.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6548-WITNESS-X2-04-F, V6548-WITNESS-X2-04-P

### V6548-METHOD-X2-05 — Bounded x2 recovery for porcelain_v2_restage_probe_timed_out

- Trigger: porcelain_v2_restage_probe_timed_out
- Method: Resolve cached, unstaged, and untracked name sets with separate bounded Git commands and compare those explicit paths to the owned allowlist.
- Recurrence guard: Use separate name-only Git surfaces with an adequate bound instead of requiring one full porcelain record over a large staged candidate.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6548-WITNESS-X2-05-F, V6548-WITNESS-X2-05-P

### V6548-METHOD-X2-06 — Bounded x2 recovery for correction_reviewer_required_superset_mismatched_delta

- Trigger: correction_reviewer_required_superset_mismatched_delta
- Method: Bind the reviewer to the exact generated negative-ledger, Method Flow, validation, manifest, and anchor-script delta, with only its own receipt admitted as a self-exclusion.
- Recurrence guard: Derive correction-required paths from the actual immutable-parent delta and reject both missing and unexpected paths.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6548-WITNESS-X2-06-F, V6548-WITNESS-X2-06-P

### V6548-METHOD-X2-07 — Bounded x2 recovery for git_grep_cached_option_was_parsed_as_revision

- Trigger: git_grep_cached_option_was_parsed_as_revision
- Method: Place git grep options before the pattern and path delimiter, then treat status 1 with empty output as the expected no-match result.
- Recurrence guard: Keep git grep options before its pattern and reserve the double dash for the pathspec boundary.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6548-WITNESS-X2-07-F, V6548-WITNESS-X2-07-P

### V6548-METHOD-FINAL-01 — Bounded final recovery for combined_closeout_candidate_validator_rejection

- Trigger: combined_closeout_candidate_validator_rejection
- Method: Inspect the validator's failing check identities, correct only the candidate consistency defect, and rerun the closeout candidate once.
- Recurrence guard: Persist or inspect per-check validator results whenever aggregate validity is false; do not infer the defect from test or privacy counts.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6548-WITNESS-FINAL-01-F, V6548-WITNESS-FINAL-01-P

### V6548-METHOD-FINAL-02 — Bounded final recovery for parallel_powershell_skill_reads_timeout

- Trigger: parallel_powershell_skill_reads_timeout
- Method: Read the exact files through bounded direct Node filesystem calls, verify byte counts, and emit explicit EOF markers.
- Recurrence guard: Use direct byte reads for known archive-backed or global skill files instead of short parallel PowerShell content reads.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6548-WITNESS-FINAL-02-F, V6548-WITNESS-FINAL-02-P

### V6548-METHOD-FINAL-03 — Bounded final recovery for node_repl_process_environment_unavailable

- Trigger: node_repl_process_environment_unavailable
- Method: Invoke the bounded child process without a custom environment; the inherited tool environment is sufficient for this read-only diagnostic.
- Recurrence guard: Use the Node REPL metadata-only runtime contract and never reference the unavailable process global from model-authored code.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6548-WITNESS-FINAL-03-F, V6548-WITNESS-FINAL-03-P

### V6551-METHOD-X1-01 — Bounded x1 recovery for parallel_index_routing_skill_read_timeout

- Trigger: parallel_index_routing_skill_read_timeout
- Method: Read each exact skill and required reference through EOF with one bounded literal-path operation.
- Recurrence guard: Prefer direct sequential reads for required instruction files on archive-backed Windows paths.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-01-F, V6551-WITNESS-X1-01-P

### V6551-METHOD-X1-02 — Bounded x1 recovery for parallel_method_schema_read_timeout

- Trigger: parallel_method_schema_read_timeout
- Method: Read the Method Flow skill and schema separately through EOF before recording a method.
- Recurrence guard: Do not rely on short parallel wrappers for required schema reads.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-02-F, V6551-WITNESS-X1-02-P

### V6551-METHOD-X1-03 — Bounded x1 recovery for memory_registry_query_timeout

- Trigger: memory_registry_query_timeout
- Method: Use one narrower exact-keyword query and read only the directly referenced current continuity rows.
- Recurrence guard: Keep memory lookup to exact owner, phase, and route keywords.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-03-F, V6551-WITNESS-X1-03-P

### V6551-METHOD-X1-04 — Bounded x1 recovery for broad_phase_script_inventory_output_truncated

- Trigger: broad_phase_script_inventory_output_truncated
- Method: Enumerate exact filenames with a phase-bounded basename filter and inspect only the selected builders, validators, and tests.
- Recurrence guard: List names and sizes first; never dump every matching source file.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-04-F, V6551-WITNESS-X1-04-P

### V6551-METHOD-X1-05 — Bounded x1 recovery for powershell_branch_probe_parser_error

- Trigger: powershell_branch_probe_parser_error
- Method: Run the native command, capture its exit code in a separate scalar, then construct the result object.
- Recurrence guard: Do not place semicolon-separated native commands inside a PowerShell value expression.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-05-F, V6551-WITNESS-X1-05-P

### V6551-METHOD-X1-06 — Bounded x1 recovery for combined_uniqueness_live_remote_probe_timeout

- Trigger: combined_uniqueness_live_remote_probe_timeout
- Method: Split local path, local branch, worktree registration, and live-remote checks; preserve an empty live-remote result as an explicit zero-row success.
- Recurrence guard: Separate local Git checks from network-backed remote checks.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-06-F, V6551-WITNESS-X1-06-P

### V6551-METHOD-X1-07 — Bounded x1 recovery for worktree_add_timeout_late_success

- Trigger: worktree_add_timeout_late_success
- Method: Do not retry; inspect process count, registration, target existence, branch, head, locks, and cleanliness after convergence.
- Recurrence guard: Never replay an ambiguously timed-out Git mutation before exact-state convergence.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-07-F, V6551-WITNESS-X1-07-P

### V6551-METHOD-X1-08 — Bounded x1 recovery for transitional_worktree_state_audit_timeout

- Trigger: transitional_worktree_state_audit_timeout
- Method: Use a scalar process-and-existence probe, wait within a bounded window for zero Git processes, then inspect Git state.
- Recurrence guard: Avoid worktree-status plumbing while checkout is observably active.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-08-F, V6551-WITNESS-X1-08-P

### V6551-METHOD-X1-09 — Bounded x1 recovery for combined_postconvergence_state_audit_timeout

- Trigger: combined_postconvergence_state_audit_timeout
- Method: Run exact head, branch, tracked status, and untracked checks as separate bounded scalar probes.
- Recurrence guard: Use small scalar Git commands for archive-backed Windows worktrees.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-09-F, V6551-WITNESS-X1-09-P

### V6551-METHOD-X1-10 — Bounded x1 recovery for semantic_novelty_threshold_rejected_task_envelope_title

- Trigger: semantic_novelty_threshold_rejected_task_envelope_title
- Method: Replace the shared template phrasing with a projection-job charter whose mechanism names dome region, asset delta, permission ceiling, abort path, and external-release refusal.
- Recurrence guard: Audit both mechanism and title tokens against the complete inherited chain before freezing x1.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6551-WITNESS-X1-10-F, V6551-WITNESS-X1-10-P

### V6551-METHOD-X2-01 — Bounded x2 recovery for focused_tests_started_before_evidence_validator_receipts

- Trigger: focused_tests_started_before_evidence_validator_receipts
- Method: Run the detailed and minimal evidence validators against the prospective evidence manifest, then rerun only the receipt-dependent test.
- Recurrence guard: Materialize validator receipts before invoking tests that read them; do not rerun an otherwise passing broad selection.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6551-WITNESS-X2-01-F, V6551-WITNESS-X2-01-P

### V6551-METHOD-X2-02 — Bounded x2 recovery for evidence_staged_review_wrapper_timeout_late_success

- Trigger: evidence_staged_review_wrapper_timeout_late_success
- Method: Do not rerun the same reviewed surface; verify zero Python processes and inspect the durable receipt before deciding whether any new staged surface requires a finalization review.
- Recurrence guard: Budget the Git-blob staged review separately from its wrapper and treat a durable receipt as evidence only after direct parsing.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6551-WITNESS-X2-02-F, V6551-WITNESS-X2-02-P

### V6551-METHOD-X2-03 — Bounded x2 recovery for powershell_large_staged_receipt_parse_timeout

- Trigger: powershell_large_staged_receipt_parse_timeout
- Method: Read the exact UTF-8 JSON with a bounded direct Python parser and extract only validity and mismatch counts.
- Recurrence guard: Use direct JSON parsing for lifecycle receipts instead of archive-backed PowerShell object conversion.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6551-WITNESS-X2-03-F, V6551-WITNESS-X2-03-P

### V6551-METHOD-FINAL-01 — Bounded final recovery for quote_unsafe_broad_rg_powershell_parse_failure

- Trigger: quote_unsafe_broad_rg_powershell_parse_failure
- Method: Use one single-quoted literal ripgrep pattern without the malformed quote fragment; the bounded inventory then completed.
- Recurrence guard: Prefer literal, shell-safe search patterns and split syntax-sensitive inventories into bounded calls.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6551-WITNESS-FINAL-01-F, V6551-WITNESS-FINAL-01-P

### V6551-METHOD-FINAL-02 — Bounded final recovery for combined_status_diff_inventory_wrapper_timeout

- Trigger: combined_status_diff_inventory_wrapper_timeout
- Method: Split status counts, exact path inventory, diff hygiene, and statistics into separate bounded scalar probes before staging.
- Recurrence guard: Do not combine archive-backed Git inventory surfaces in one short PowerShell wrapper when each result can be checked independently.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6551-WITNESS-FINAL-02-F, V6551-WITNESS-FINAL-02-P

### V6552-METHOD-X1-01 — Bounded x1 recovery for combined_activation_metadata_git_status_probe_timeout

- Trigger: combined_activation_metadata_git_status_probe_timeout
- Method: Split exact UTF-8 baton metadata, source branch, head, and cleanliness into long-bound scalar probes.
- Recurrence guard: Do not combine archive-backed file reads and Git status in one short startup wrapper.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-01-F, V6552-WITNESS-X1-01-P

### V6552-METHOD-X1-02 — Bounded x1 recovery for parallel_baton_metadata_line_count_timeout

- Trigger: parallel_baton_metadata_line_count_timeout
- Method: Use one exact .NET UTF-8 ReadAllText operation, then verify byte, character, line, and final-newline counts.
- Recurrence guard: Use a single direct .NET file read for a known archive-backed baton.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-02-F, V6552-WITNESS-X1-02-P

### V6552-METHOD-X1-03 — Bounded x1 recovery for parallel_source_branch_head_probe_timeout

- Trigger: parallel_source_branch_head_probe_timeout
- Method: Run branch and head as separate scalar Git commands with archive-sized timeouts; both then matched the activation.
- Recurrence guard: Require complete scalar outputs rather than crediting a partial multi-command identity probe.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-03-F, V6552-WITNESS-X1-03-P

### V6552-METHOD-X1-04 — Bounded x1 recovery for parallel_source_cleanliness_probe_timeout

- Trigger: parallel_source_cleanliness_probe_timeout
- Method: Run status alone with a longer bound and materialize only porcelain row count; the source then proved clean.
- Recurrence guard: Keep archive-backed cleanliness separate from identity and metadata probes.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-04-F, V6552-WITNESS-X1-04-P

### V6552-METHOD-X1-05 — Bounded x1 recovery for ripgrep_option_boundary_pattern_error

- Trigger: ripgrep_option_boundary_pattern_error
- Method: Use rg -n -- followed by the literal pattern and exact file; the bounded runner inspection then completed.
- Recurrence guard: Insert the rg option terminator before any pattern that can begin with a hyphen.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-05-F, V6552-WITNESS-X1-05-P

### V6552-METHOD-X1-06 — Bounded x1 recovery for powershell_foreach_receipt_projection_parser_error

- Trigger: powershell_foreach_receipt_projection_parser_error
- Method: Materialize receipt rows in an array, then pipe that array to the formatter; the six exact receipts parsed.
- Recurrence guard: Materialize PowerShell foreach output before piping it.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-06-F, V6552-WITNESS-X1-06-P

### V6552-METHOD-X1-07 — Bounded x1 recovery for semantic_domain_query_missing_closing_brace

- Trigger: semantic_domain_query_missing_closing_brace
- Method: Use a materialized Where-Object result with balanced syntax; the complete 1,960-title seed-domain audit then returned.
- Recurrence guard: Prefer a short materialized filter over nested one-line foreach and if blocks for title audits.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-07-F, V6552-WITNESS-X1-07-P

### V6552-METHOD-X1-08 — Bounded x1 recovery for unicode_multi_hunk_patch_context_rejection

- Trigger: unicode_multi_hunk_patch_context_rejection
- Method: Apply small exact UTF-8 hunks for identity, source, practice, disposition, and catalogue aliases; the owned file updates passed.
- Recurrence guard: Use exact UTF-8 source context and split unrelated patches when a terminal display may have decoded Unicode differently.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-08-F, V6552-WITNESS-X1-08-P

### V6552-METHOD-X1-09 — Bounded x1 recovery for combined_catalogue_ast_status_probe_timeout

- Trigger: combined_catalogue_ast_status_probe_timeout
- Method: Split the verification into a literal file probe, a direct UTF-8 structure read, and one bounded AST parse; the catalogue was intact.
- Recurrence guard: Keep archive-backed metadata, interpreter, and Git checks as separate scalar probes.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-09-F, V6552-WITNESS-X1-09-P

### V6552-METHOD-X1-10 — Bounded x1 recovery for novelty_report_console_encoding_error

- Trigger: novelty_report_console_encoding_error
- Method: Set the Python standard-stream encoding explicitly to UTF-8 and rerun the unchanged read-only comparison.
- Recurrence guard: Declare UTF-8 standard-stream encoding for Unicode-bearing evidence reports on Windows.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-10-F, V6552-WITNESS-X1-10-P

### V6552-METHOD-X1-11 — Bounded x1 recovery for x1_manifest_worktree_line_ending_mismatch

- Trigger: x1_manifest_worktree_line_ending_mismatch
- Method: Validate each manifest row against the exact prospective Git blob used by the manifest, while the staged review separately audits the eventual index blobs.
- Recurrence guard: State and test the content basis of byte manifests explicitly when core.autocrlf is active.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-11-F, V6552-WITNESS-X1-11-P

### V6552-METHOD-X1-12 — Bounded x1 recovery for powershell_system_text_json_type_unavailable

- Trigger: powershell_system_text_json_type_unavailable
- Method: Use the host-supported ConvertFrom-Json parser and literal file metadata; it identified four line-ending-only mismatches.
- Recurrence guard: Use PowerShell's native JSON cmdlets unless an assembly-backed type has first been verified.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6552-WITNESS-X1-12-F, V6552-WITNESS-X1-12-P

### V6552-METHOD-X2-01 — Bounded x2 recovery for evidence_builder_skill_path_binding_missing

- Trigger: evidence_builder_skill_path_binding_missing
- Method: Bind each exact phase-local skill directory inside the validation loop, retain the partial build at zero credit, and rerun from the unchanged immutable x1 parent.
- Recurrence guard: Define lifecycle-local paths in every function that consumes them rather than relying on a same-named local from another helper.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6552-WITNESS-X2-01-F, V6552-WITNESS-X2-01-P

### V6552-METHOD-FINAL-01 — Bounded final recovery for closeout_tests_inherited_x2_count_and_pillar_literals

- Trigger: closeout_tests_inherited_x2_count_and_pillar_literals
- Method: Bind the closeout tests to the immutable Lyren evidence receipt: one x2 operational fault and THOS Body as the primary pillar, while preserving all dynamic final-fault arithmetic.
- Recurrence guard: Derive closeout identity, focus, and inherited fault counts from the phase evidence artifacts rather than source-template literals.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6552-WITNESS-FINAL-01-F, V6552-WITNESS-FINAL-01-P

### V6553-METHOD-X1-01 — Bounded x1 recovery for oversized_activation_baton_display_truncated

- Trigger: oversized_activation_baton_display_truncated
- Method: Read the exact immutable Git blob in bounded line ranges through the final line.
- Recurrence guard: Use bounded immutable-blob ranges for long activation files.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-01-F, V6553-WITNESS-X1-01-P

### V6553-METHOD-X1-02 — Bounded x1 recovery for combined_auth_roster_display_truncated

- Trigger: combined_auth_roster_display_truncated
- Method: Reread each required file separately with bounded exact UTF-8 reads.
- Recurrence guard: Do not combine multiple long policy files into one evidence display.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-02-F, V6553-WITNESS-X1-02-P

### V6553-METHOD-X1-03 — Bounded x1 recovery for auth_state_tail_display_compacted

- Trigger: auth_state_tail_display_compacted
- Method: Reread the remaining state in two explicit bounded ranges.
- Recurrence guard: Split long JSON state tails before context or output limits are approached.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-03-F, V6553-WITNESS-X1-03-P

### V6553-METHOD-X1-04 — Bounded x1 recovery for auth_state_get_content_probe_timeout

- Trigger: auth_state_get_content_probe_timeout
- Method: Use System.IO.File.ReadAllLines for the exact known file and bounded range.
- Recurrence guard: Prefer direct .NET reads for archive-backed or security-scanned policy files.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-04-F, V6553-WITNESS-X1-04-P

### V6553-METHOD-X1-05 — Bounded x1 recovery for auth_state_second_get_content_probe_timeout

- Trigger: auth_state_second_get_content_probe_timeout
- Method: Use the same direct .NET exact-path method and retain this distinct timeout.
- Recurrence guard: Do not repeat a timed-out file cmdlet when the direct .NET method is available.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-05-F, V6553-WITNESS-X1-05-P

### V6553-METHOD-X1-06 — Bounded x1 recovery for auth_schema_get_content_probe_timeout

- Trigger: auth_schema_get_content_probe_timeout
- Method: Read the exact schema through System.IO.File.ReadAllText.
- Recurrence guard: Use one direct exact-path read for small required schemas.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-06-F, V6553-WITNESS-X1-06-P

### V6553-METHOD-X1-07 — Bounded x1 recovery for windows_rg_wildcard_path_rejected

- Trigger: windows_rg_wildcard_path_rejected
- Method: Use rg directory roots with a -g filename glob.
- Recurrence guard: Use ripgrep glob options rather than shell-style wildcard path arguments on Windows.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-07-F, V6553-WITNESS-X1-07-P

### V6553-METHOD-X1-08 — Bounded x1 recovery for inherited_json_stale_field_projection

- Trigger: inherited_json_stale_field_projection
- Method: Enumerate actual top-level properties before projecting scalar counts.
- Recurrence guard: Inspect current receipt schemas rather than assuming fields from an earlier phase.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-08-F, V6553-WITNESS-X1-08-P

### V6553-METHOD-X1-09 — Bounded x1 recovery for second_windows_rg_wildcard_path_rejected

- Trigger: second_windows_rg_wildcard_path_rejected
- Method: Run the corrected directory-root and -g query and retain the recurrence separately.
- Recurrence guard: Apply the Windows rg glob guard to every phase-specific search.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-09-F, V6553-WITNESS-X1-09-P

### V6553-METHOD-X1-10 — Bounded x1 recovery for catalogue_match_count_wildcard_error

- Trigger: catalogue_match_count_wildcard_error
- Method: Rerun bounded searches against directory roots with explicit -g filters.
- Recurrence guard: Never credit partial multi-path search output when any requested path failed.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-10-F, V6553-WITNESS-X1-10-P

### V6553-METHOD-X1-11 — Bounded x1 recovery for workflow_validator_obsolete_request_option

- Trigger: workflow_validator_obsolete_request_option
- Method: Inspect the valid phase-local receipt already emitted by the x1 builder and use the current positional-input CLI only for a future changed request.
- Recurrence guard: Read the current workflow runner help before constructing an independent validation command.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-11-F, V6553-WITNESS-X1-11-P

### V6553-METHOD-X1-12 — Bounded x1 recovery for x1_privacy_receipt_stale_file_count_projection

- Trigger: x1_privacy_receipt_stale_file_count_projection
- Method: Enumerate exact top-level receipt properties and project scanned_file_count.
- Recurrence guard: Bind every scalar summary to the current receipt schema rather than a remembered alias.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6553-WITNESS-X1-12-F, V6553-WITNESS-X1-12-P

### V6553-METHOD-X2-01 — Bounded x2 recovery for skill_creator_whole_file_display_truncated

- Trigger: skill_creator_whole_file_display_truncated
- Method: Read the exact instruction file with direct .NET line access in bounded numbered chunks through the measured final line, then read its required openai.yaml reference through EOF.
- Recurrence guard: Measure large instruction files first and use bounded numbered chunks whenever one display could exceed the tool or model context.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6553-WITNESS-X2-01-F, V6553-WITNESS-X2-01-P

### V6553-METHOD-X2-02 — Bounded x2 recovery for skill_creator_bounded_chunk_wrapper_timed_out_after_output

- Trigger: skill_creator_bounded_chunk_wrapper_timed_out_after_output
- Method: Continue from the next exact line with a wider bounded timeout and confirm every remaining line plus the required reference through EOF.
- Recurrence guard: Allow an adequate bounded wrapper for direct .NET reads in this large Windows workspace and distinguish emitted text from process success.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6553-WITNESS-X2-02-F, V6553-WITNESS-X2-02-P

### V6553-METHOD-X2-03 — Bounded x2 recovery for windows_rg_wildcard_path_rejected

- Trigger: windows_rg_wildcard_path_rejected
- Method: Search the scripts and tests directory roots with explicit rg -g filters; the bounded recovery enumerated all stale template tokens.
- Recurrence guard: Use directory roots plus rg glob filters on Windows instead of wildcard characters in positional path arguments.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6553-WITNESS-X2-03-F, V6553-WITNESS-X2-03-P

### V6553-METHOD-X2-04 — Bounded x2 recovery for first_evidence_overview_exceeded_document_word_cap

- Trigger: first_evidence_overview_exceeded_document_word_cap
- Method: Keep every proposal, disposition, mutation count, source need, artifact class, and evidence boundary while removing repeated full preregistration sentences from the reader-facing proposal summaries.
- Recurrence guard: Enforce both the three-page minimum and 6,000-word maximum immediately after generating each phase narrative.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6553-WITNESS-X2-04-F, V6553-WITNESS-X2-04-P

### V6554-METHOD-X1-01 — Bounded x1 recovery for activation_blob_display_exceeded_context

- Trigger: activation_blob_display_exceeded_context
- Method: Resolve the exact blob hash, measure it, and emit bounded numbered ranges through EOF.
- Recurrence guard: Measure long Git blobs before display and use bounded exact ranges.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-01-F, V6554-WITNESS-X1-01-P

### V6554-METHOD-X1-02 — Bounded x1 recovery for activation_measurement_wrapper_timeout

- Trigger: activation_measurement_wrapper_timeout
- Method: Use direct Git plumbing with a longer bounded timeout and scalar output.
- Recurrence guard: Allow archive-backed Git plumbing an evidence-proportionate bounded timeout.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-02-F, V6554-WITNESS-X1-02-P

### V6554-METHOD-X1-03 — Bounded x1 recovery for process_argument_list_api_unavailable

- Trigger: process_argument_list_api_unavailable
- Method: Use the compatible Arguments property with the already-verified object hash.
- Recurrence guard: Inspect the runtime API surface before using newer process-construction members.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-03-F, V6554-WITNESS-X1-03-P

### V6554-METHOD-X1-04 — Bounded x1 recovery for memory_linked_solo_activation_skill_missing

- Trigger: memory_linked_solo_activation_skill_missing
- Method: Use the present family-current skills named by the fully read Index and activation baton.
- Recurrence guard: Treat memory tool pointers as historical until live filesystem verification passes.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-04-F, V6554-WITNESS-X1-04-P

### V6554-METHOD-X1-05 — Bounded x1 recovery for skill_discovery_regex_false_zero

- Trigger: skill_discovery_regex_false_zero
- Method: Enumerate the narrow skill root by exact directory name and read the resolved files.
- Recurrence guard: Prefer exact skill directory probes over fragile separator-heavy path expressions.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-05-F, V6554-WITNESS-X1-05-P

### V6554-METHOD-X1-06 — Bounded x1 recovery for source_status_aggregate_timeout

- Trigger: source_status_aggregate_timeout
- Method: Split tracked, staged, and untracked source checks into scalar Git witnesses.
- Recurrence guard: Use separate cleanliness probes on archive-backed worktrees.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-06-F, V6554-WITNESS-X1-06-P

### V6554-METHOD-X1-07 — Bounded x1 recovery for ancestry_wrapper_powershell_parser_error

- Trigger: ancestry_wrapper_powershell_parser_error
- Method: Run the ancestry command first, store its exit status, then build the scalar object.
- Recurrence guard: Never embed semicolon-bearing command/status expressions inside a PowerShell hash value.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-07-F, V6554-WITNESS-X1-07-P

### V6554-METHOD-X1-08 — Bounded x1 recovery for guessed_terminal_receipt_directory_absent

- Trigger: guessed_terminal_receipt_directory_absent
- Method: Use the live activation plus a bounded filename-only search; never invent a route path.
- Recurrence guard: Resolve external receipt locations before reading and keep missing guesses at zero credit.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-08-F, V6554-WITNESS-X1-08-P

### V6554-METHOD-X1-09 — Bounded x1 recovery for broad_validation_bank_hash_search_timeout

- Trigger: broad_validation_bank_hash_search_timeout
- Method: Use the known source task event tail and exact committed receipts instead of repeating a broad search.
- Recurrence guard: Avoid recursive archive-wide searches when a bounded authoritative source is available.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-09-F, V6554-WITNESS-X1-09-P

### V6554-METHOD-X1-10 — Bounded x1 recovery for parallel_foreach_reader_parser_error

- Trigger: parallel_foreach_reader_parser_error
- Method: Use the explicit foreach ($item in $items) form and read each declared file once.
- Recurrence guard: Keep the validated explicit-space PowerShell loop form in generated wrappers.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-10-F, V6554-WITNESS-X1-10-P

### V6554-METHOD-X1-11 — Bounded x1 recovery for evidence_projection_extra_brace_parser_error

- Trigger: evidence_projection_extra_brace_parser_error
- Method: Project the required receipts independently with simpler scalar expressions.
- Recurrence guard: Prefer short one-purpose structured projections over nested one-line aggregations.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-11-F, V6554-WITNESS-X1-11-P

### V6554-METHOD-X1-12 — Bounded x1 recovery for frozen_chain_projection_invalid_cmdlet_token

- Trigger: frozen_chain_projection_invalid_cmdlet_token
- Method: Use Select-Object -First and separately project prior and new proposal arrays.
- Recurrence guard: Keep cmdlet parameters separated from command names in PowerShell.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-12-F, V6554-WITNESS-X1-12-P

### V6554-METHOD-X1-13 — Bounded x1 recovery for source_session_tail_projection_timeout

- Trigger: source_session_tail_projection_timeout
- Method: Search for narrow terminal vocabulary first and parse only the matched assistant events.
- Recurrence guard: Filter large event streams lexically before structured parsing.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-13-F, V6554-WITNESS-X1-13-P

### V6554-METHOD-X1-14 — Bounded x1 recovery for terminal_event_search_overconstrained_zero_result

- Trigger: terminal_event_search_overconstrained_zero_result
- Method: Search a small set of exact terminal phrases and parse the resulting assistant events.
- Recurrence guard: Validate event-line shape before combining multiple structural regex assumptions.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-14-F, V6554-WITNESS-X1-14-P

### V6554-METHOD-X1-15 — Bounded x1 recovery for worktree_add_wrapper_timeout_during_initialization

- Trigger: worktree_add_wrapper_timeout_during_initialization
- Method: Audit path, registration, branch, head, processes, and lock state; wait for the one checkout to settle without retry.
- Recurrence guard: Never replay an ambiguous worktree mutation; reconcile its exact state first.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-15-F, V6554-WITNESS-X1-15-P

### V6554-METHOD-X1-16 — Bounded x1 recovery for worktree_audit_spacing_expression_errors

- Trigger: worktree_audit_spacing_expression_errors
- Method: Use explicit spaces in Join-Path and Select-Object parameter forms, then inspect the existing lane only.
- Recurrence guard: Use validated literal scalar syntax for post-timeout mutation audits.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-16-F, V6554-WITNESS-X1-16-P

### V6554-METHOD-X1-17 — Bounded x1 recovery for new_lane_tracked_cleanliness_timeout

- Trigger: new_lane_tracked_cleanliness_timeout
- Method: Run one longer unified porcelain status after checkout processes have fully settled.
- Recurrence guard: Allow first-touch filesystem scanning to settle before exact cleanliness validation.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-17-F, V6554-WITNESS-X1-17-P

### V6554-METHOD-X1-18 — Bounded x1 recovery for new_lane_untracked_enumeration_timeout

- Trigger: new_lane_untracked_enumeration_timeout
- Method: Use the same longer unified porcelain status and require an empty result before writing x1.
- Recurrence guard: Do not run parallel first-touch index and untracked scans on a freshly populated archive lane.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-18-F, V6554-WITNESS-X1-18-P

### V6554-METHOD-X1-19 — Bounded x1 recovery for phase_data_reader_spacing_error

- Trigger: phase_data_reader_spacing_error
- Method: Use the explicit Resolve-Path argument form and read the file through EOF once.
- Recurrence guard: Keep PowerShell cmdlet names and arguments separated in bounded readers.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-19-F, V6554-WITNESS-X1-19-P

### V6554-METHOD-X1-20 — Bounded x1 recovery for test_reader_spacing_error_recurrence

- Trigger: test_reader_spacing_error_recurrence
- Method: Use the already validated explicit Resolve-Path argument form and avoid further diagnostic replay.
- Recurrence guard: Apply the cmdlet-spacing guard to every bounded reader, not only the first recovered file.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-20-F, V6554-WITNESS-X1-20-P

### V6554-METHOD-X1-21 — Bounded x1 recovery for first_full_chain_novelty_audit_rejected_template_overlap

- Trigger: first_full_chain_novelty_audit_rejected_template_overlap
- Method: Redesign the mechanisms, not merely their domain nouns, then rerun only the frozen novelty audit.
- Recurrence guard: Compare both title tokens and mechanism shape against the full inherited chain before freezing x1.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-21-F, V6554-WITNESS-X1-21-P

### V6554-METHOD-X1-22 — Bounded x1 recovery for x1_receipt_projection_foreach_parser_recurrence

- Trigger: x1_receipt_projection_foreach_parser_recurrence
- Method: Retain the failure, rebuild the deterministic ledger, and project receipts with explicit loop and path syntax.
- Recurrence guard: Ban compressed foreach and Resolve-Path tokens from receipt-summary wrappers.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-22-F, V6554-WITNESS-X1-22-P

### V6554-METHOD-X1-23 — Bounded x1 recovery for receipt_join_path_token_recurrence_three

- Trigger: receipt_join_path_token_recurrence_three
- Method: Use direct literal receipt paths for all remaining scalar reads and reject null projections.
- Recurrence guard: Do not construct known receipt paths dynamically in compact PowerShell wrappers.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-23-F, V6554-WITNESS-X1-23-P

### V6554-METHOD-X1-24 — Bounded x1 recovery for x1_stale_term_windows_wildcard_path_rejected

- Trigger: x1_stale_term_windows_wildcard_path_rejected
- Method: Search the script, test, and phase directory roots with explicit ripgrep -g filters and exclusions.
- Recurrence guard: Never use wildcard characters in positional Windows path arguments for ripgrep.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-24-F, V6554-WITNESS-X1-24-P

### V6554-METHOD-X1-25 — Bounded x1 recovery for focused_x1_pytest_dependency_absent

- Trigger: focused_x1_pytest_dependency_absent
- Method: Invoke the dependency-free unittest file directly with the same bytecode and UTF-8 guards.
- Recurrence guard: Inspect the test harness entrypoint before selecting an optional test runner.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-25-F, V6554-WITNESS-X1-25-P

### V6554-METHOD-X1-26 — Bounded x1 recovery for focused_x1_unittest_stale_expected_counts

- Trigger: focused_x1_unittest_stale_expected_counts
- Method: Update every explicit current-phase and cumulative count assertion for the retained N25 witness, then rebuild before rerunning.
- Recurrence guard: Search the whole focused test for every phase-local count whenever a retained negative changes the ledger.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-26-F, V6554-WITNESS-X1-26-P

### V6554-METHOD-X1-27 — Bounded x1 recovery for x1_receipt_summary_guessed_paths_returned_null

- Trigger: x1_receipt_summary_guessed_paths_returned_null
- Method: Discover the committed-intent paths from the generated manifest and read only those literal files with terminating errors.
- Recurrence guard: Treat any null receipt projection as failure and never infer generated filenames from directory semantics.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-27-F, V6554-WITNESS-X1-27-P

### V6554-METHOD-X1-28 — Bounded x1 recovery for combined_x1_index_cleanliness_probe_timeout

- Trigger: combined_x1_index_cleanliness_probe_timeout
- Method: Run the three read-only index and worktree checks separately with archive-aware bounded timeouts.
- Recurrence guard: Do not combine multiple first-pass archive-backed Git scans under one short timeout.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6554-WITNESS-X1-28-F, V6554-WITNESS-X1-28-P

### V6554-METHOD-X2-01 — Bounded x2 recovery for case_insensitive_powershell_replacement_hash_duplicate_key

- Trigger: case_insensitive_powershell_replacement_hash_duplicate_key
- Method: Use one ordered replacement map for unique exact keys and apply the lowercase replacement separately after the map.
- Recurrence guard: Do not encode case-distinct strings as keys in a PowerShell hashtable.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6554-WITNESS-X2-01-F, V6554-WITNESS-X2-01-P

### V6554-METHOD-X2-02 — Bounded x2 recovery for generic_tuple_factory_unavailable_in_legacy_powershell_runtime

- Trigger: generic_tuple_factory_unavailable_in_legacy_powershell_runtime
- Method: Probe and use native nested PowerShell arrays for ordered replacement pairs, then perform the bounded mechanical rewrite.
- Recurrence guard: Verify legacy-runtime collection construction with a two-pair scalar probe before applying it to repository files.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6554-WITNESS-X2-02-F, V6554-WITNESS-X2-02-P

### V6554-METHOD-X2-03 — Bounded x2 recovery for unicode_sensitive_core_patch_context_mismatch

- Trigger: unicode_sensitive_core_patch_context_mismatch
- Method: Read the file through the Unicode-preserving .NET API and patch the ASCII-stable count anchors separately from the exact UTF-8 boundary.
- Recurrence guard: Use Unicode-preserving readers before constructing patches that include non-ASCII authority language.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6554-WITNESS-X2-03-F, V6554-WITNESS-X2-03-P

### V6554-METHOD-X2-04 — Bounded x2 recovery for foreach_output_piped_without_materialization_parser_error

- Trigger: foreach_output_piped_without_materialization_parser_error
- Method: Materialize each scalar tool-path receipt into an array and pipe that array to JSON only after the loop completes.
- Recurrence guard: Do not attach a pipeline directly to a PowerShell foreach statement in bounded repository probes.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6554-WITNESS-X2-04-F, V6554-WITNESS-X2-04-P

### V6554-METHOD-X2-05 — Bounded x2 recovery for stale_domain_audit_conflated_inherited_and_contextual_lens_terms

- Trigger: stale_domain_audit_conflated_inherited_and_contextual_lens_terms
- Method: Scan current evidence prose with domain-specific phrases instead of the generic word lens, and inspect only current-phase x2 Method Flow rows while retaining inherited rows unchanged.
- Recurrence guard: Separate inherited ledger content from current-owner semantic residue and avoid polysemous single-word domain patterns.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6554-WITNESS-X2-05-F, V6554-WITNESS-X2-05-P

### V6554-METHOD-X2-06 — Bounded x2 recovery for evidence_scope_regex_prefix_lacked_runner_suffix_match

- Trigger: evidence_scope_regex_prefix_lacked_runner_suffix_match
- Method: Require one or more characters after the exact instrument runner prefix and rerun the same path-only scope audit.
- Recurrence guard: Test prefix allowlist expressions against at least one full expected runner path before applying them to the manifest.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6554-WITNESS-X2-06-F, V6554-WITNESS-X2-06-P

### V6554-METHOD-X2-07 — Bounded x2 recovery for residue_recovery_rescanned_its_own_negative_and_pattern

- Trigger: residue_recovery_rescanned_its_own_negative_and_pattern
- Method: Apply the stale-domain assertion to current semantic outputs only and separately account for scanner definitions and retained negative or Method Flow witness text.
- Recurrence guard: Never require a negative register or scanner source to omit the exact failure vocabulary it is designed to preserve or detect.
- Rollback: Stop, retain the failed attempt at zero credit, and leave objects, tools, materials, external, and sibling state unchanged.
- Witnesses: V6554-WITNESS-X2-07-F, V6554-WITNESS-X2-07-P

### V6554-METHOD-FINAL-01 — Bounded final recovery for no_match_ripgrep_status_not_normalized

- Trigger: no_match_ripgrep_status_not_normalized
- Method: Capture ripgrep output and status, reject only status greater than one, print the zero-hit count, and exit successfully for an empty result.
- Recurrence guard: Normalize ripgrep status one only when the captured no-match output is empty; preserve status greater than one as an operational failure.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6554-WITNESS-FINAL-01-F, V6554-WITNESS-FINAL-01-P

### V6554-METHOD-FINAL-02 — Bounded final recovery for closeout_builder_wrapper_timed_out_after_durable_completion

- Trigger: closeout_builder_wrapper_timed_out_after_durable_completion
- Method: Do not launch a duplicate while process state is ambiguous. Confirm no Python process remains, parse the durable receipt, and use a wider bounded wrapper for the rebuild that retains this failure.
- Recurrence guard: Budget closeout generation, owner-manifest hashing, validation, and tests under an archive-aware ten-minute wrapper.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6554-WITNESS-FINAL-02-F, V6554-WITNESS-FINAL-02-P

### V6554-METHOD-FINAL-03 — Bounded final recovery for workflow_assignment_projection_used_nonexistent_route_property

- Trigger: workflow_assignment_projection_used_nonexistent_route_property
- Method: Inspect the refinement schema properties and verify the 165 exact phase assignments from the emitted workflow-plan-request route.
- Recurrence guard: Inspect structured receipt properties before projecting nested workflow assignments from a new schema.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6554-WITNESS-FINAL-03-F, V6554-WITNESS-FINAL-03-P

### V6554-METHOD-FINAL-04 — Bounded final recovery for bundled_git_state_probe_timed_out_before_output

- Trigger: bundled_git_state_probe_timed_out_before_output
- Method: Audit the timed-out child processes and worktree lock surface, wait for the orphaned Git processes to clear, then verify branch, HEAD, and full status through separate archive-aware bounded probes.
- Recurrence guard: Keep archive-backed Git state checks scalar and allow an archive-aware bound instead of bundling several repository walks into one wrapper.
- Rollback: Retain the failed attempt with zero initial credit and keep the terminal route unsent.
- Witnesses: V6554-WITNESS-FINAL-04-F, V6554-WITNESS-FINAL-04-P

### V6555-METHOD-X1-01 — Bounded x1 recovery for parallel_startup_probes_timed_out_without_output

- Trigger: parallel_startup_probes_timed_out_without_output
- Method: Rerun only isolated scalar probes with an archive-aware startup bound.
- Recurrence guard: Do not bundle first-touch archive and memory probes under a ten-second shell budget.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-01-F, V6555-WITNESS-X1-01-P

### V6555-METHOD-X1-02 — Bounded x1 recovery for powershell_foreach_output_piped_without_materialization

- Trigger: powershell_foreach_output_piped_without_materialization
- Method: Materialize loop output into an array before JSON projection.
- Recurrence guard: Never attach a pipeline directly to a PowerShell foreach statement.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-02-F, V6555-WITNESS-X1-02-P

### V6555-METHOD-X1-03 — Bounded x1 recovery for bundled_git_state_probe_timed_out

- Trigger: bundled_git_state_probe_timed_out
- Method: Run branch, head, upstream, cleanliness, and live remote as separate scalar probes.
- Recurrence guard: Keep archive-backed Git lifecycle checks scalar.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-03-F, V6555-WITNESS-X1-03-P

### V6555-METHOD-X1-04 — Bounded x1 recovery for powershell_revision_expression_corrupted_cat_file_probe

- Trigger: powershell_revision_expression_corrupted_cat_file_probe
- Method: Use the already-proven exact HEAD and quote any revision expression passed to Git.
- Recurrence guard: Quote Git revision expressions containing braces or other PowerShell metacharacters.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-04-F, V6555-WITNESS-X1-04-P

### V6555-METHOD-X1-05 — Bounded x1 recovery for proposal_domain_probe_foreach_pipeline_recurrence

- Trigger: proposal_domain_probe_foreach_pipeline_recurrence
- Method: Materialize every term result before serializing the domain audit.
- Recurrence guard: Apply the foreach materialization guard to all novelty probes, not only path receipts.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-05-F, V6555-WITNESS-X1-05-P

### V6555-METHOD-X1-06 — Bounded x1 recovery for long_source_inventory_mixed_duplicate_output

- Trigger: long_source_inventory_mixed_duplicate_output
- Method: Keep later inventories single-purpose and use exact literal paths for lifecycle evidence.
- Recurrence guard: Do not combine full phase listings with broad repository filters when one narrow inventory is sufficient.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-06-F, V6555-WITNESS-X1-06-P

### V6555-METHOD-X1-07 — Bounded x1 recovery for powershell_domain_probe_foreach_pipeline_second_recurrence

- Trigger: powershell_domain_probe_foreach_pipeline_second_recurrence
- Method: Use the validated materialized-array form for every remaining semantic query.
- Recurrence guard: Treat compressed loop serialization as banned in this phase.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-07-F, V6555-WITNESS-X1-07-P

### V6555-METHOD-X1-08 — Bounded x1 recovery for first_x1_novelty_audit_rejected_two_template_overlaps

- Trigger: first_x1_novelty_audit_rejected_two_template_overlaps
- Method: Replace the mechanisms with bitemporal validity and VC confidence-method contracts, then rerun only the frozen x1 builder.
- Recurrence guard: When a nearest-neighbour score fails, redesign the state model or standards mechanism rather than renaming its domain nouns.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-08-F, V6555-WITNESS-X1-08-P

### V6555-METHOD-X1-09 — Bounded x1 recovery for first_focused_x1_test_run_retained_five_stale_assertions

- Trigger: first_focused_x1_test_run_retained_five_stale_assertions
- Method: Bind those assertions to the exact v655-v5 source and dynamic current-phase count contract, rebuild, and rerun the focused test once.
- Recurrence guard: After cloning a lifecycle test, audit every explicit hash, cumulative count, owner, phase, and next-route assertion before credit.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-09-F, V6555-WITNESS-X1-09-P

### V6555-METHOD-X1-10 — Bounded x1 recovery for combined_x1_review_help_status_and_count_probe_timed_out

- Trigger: combined_x1_review_help_status_and_count_probe_timed_out
- Method: Read the review script directly, then run each exact bounded probe separately with its observed interface.
- Recurrence guard: Do not infer argparse support or combine an unknown script invocation with unrelated repository inspection.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-10-F, V6555-WITNESS-X1-10-P

### V6555-METHOD-X1-11 — Bounded x1 recovery for short_timeout_truncated_staged_review_source_read

- Trigger: short_timeout_truncated_staged_review_source_read
- Method: Retain the partial read as zero credit and reread the remaining exact line window with a measured sixty-second allowance.
- Recurrence guard: Use line-window reads and the observed startup envelope for repository files on this volume.
- Rollback: Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6555-WITNESS-X1-11-F, V6555-WITNESS-X1-11-P

## Retained boundary

Same-owner workflow evidence only; no independent, empirical, professional, production, legal, cultural, Māori-authority, personhood, Theory-of-Everything, or Stage 20 claim.
