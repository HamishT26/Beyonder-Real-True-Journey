# GHC Family Method Flow State

- Phase: v654-v4
- Owner: Caelen Morrow
- Methods: 59
- Passing witnesses: 59
- Failed witnesses retained: 59

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
