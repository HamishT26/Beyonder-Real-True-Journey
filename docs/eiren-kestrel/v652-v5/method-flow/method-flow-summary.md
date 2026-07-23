# GHC Family Method Flow State

- Phase: v652-v5
- Owner: Eiren Kestrel
- Methods: 17
- Passing witnesses: 17
- Failed witnesses retained: 17

## Preferred methods

### V6525-METHOD-01 — Bounded recovery for combined_source_audit_timeout

- Trigger: combined_source_audit_timeout
- Method: Split branch, anchor, manifest, storage, and remote probes into bounded scalar reads.
- Recurrence guard: Do not aggregate large-tree and live-remote checks under one short wrapper deadline.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-01-F, V6525-WITNESS-01-P

### V6525-METHOD-02 — Bounded recovery for powershell_merge_base_expression

- Trigger: powershell_merge_base_expression
- Method: Run the Git command first, capture LASTEXITCODE separately, and then construct the summary.
- Recurrence guard: Keep child command execution outside PowerShell expression and hash-literal values.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-02-F, V6525-WITNESS-02-P

### V6525-METHOD-03 — Bounded recovery for broad_inventory_timeout

- Trigger: broad_inventory_timeout
- Method: Use exact phase-root and filename enumeration with rg and bounded direct reads.
- Recurrence guard: Prefer exact filenames and phase roots over whole-repository content inventories.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-03-F, V6525-WITNESS-03-P

### V6525-METHOD-04 — Bounded recovery for unquoted_revision_suffix

- Trigger: unquoted_revision_suffix
- Method: Quote the complete revision argument literally before passing it to git cat-file.
- Recurrence guard: Quote all Git revision expressions containing braces, carets, or upstream syntax.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-04-F, V6525-WITNESS-04-P

### V6525-METHOD-05 — Bounded recovery for template_line_count_timeout

- Trigger: template_line_count_timeout
- Method: Enumerate exact filenames first, then use bounded direct reads only for selected files.
- Recurrence guard: Do not use repeated Get-Content line counts across large generated builders.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-05-F, V6525-WITNESS-05-P

### V6525-METHOD-06 — Bounded recovery for frozen_index_shape_assumption

- Trigger: frozen_index_shape_assumption
- Method: Inspect the exact schema and concatenate prior_proposals with new_proposals.
- Recurrence guard: Probe machine-ledger keys before iterating a new or inherited schema.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-06-F, V6525-WITNESS-06-P

### V6525-METHOD-07 — Bounded recovery for bulk_clone_wrapper_timeout

- Trigger: bulk_clone_wrapper_timeout
- Method: Do not repeat the write; enumerate every exact destination and inspect their contents read-only.
- Recurrence guard: Separate bulk mechanical generation from expensive status enumeration.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-07-F, V6525-WITNESS-07-P

### V6525-METHOD-08 — Bounded recovery for stale_patch_context

- Trigger: stale_patch_context
- Method: Read the exact current block and apply smaller reviewed hunks.
- Recurrence guard: Refresh mechanically transformed context before applying a large semantic patch.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-08-F, V6525-WITNESS-08-P

### V6525-METHOD-09 — Bounded recovery for powershell_regex_quoting

- Trigger: powershell_regex_quoting
- Method: Use a literal single-quoted PowerShell argument for the complete regex.
- Recurrence guard: Use PowerShell single-quoted literals for regexes containing quotes, commas, or dollar anchors.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-09-F, V6525-WITNESS-09-P

### V6525-METHOD-10 — Bounded recovery for powershell_discovery_quoting

- Trigger: powershell_discovery_quoting
- Method: Reduce the command to one literal pattern per bounded read.
- Recurrence guard: Prefer one single-quoted search literal per PowerShell command when discovery terms contain punctuation.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-10-F, V6525-WITNESS-10-P

### V6525-METHOD-11 — Bounded recovery for multi_pattern_pipeline_timeout

- Trigger: multi_pattern_pipeline_timeout
- Method: Use a simple one-pattern rg invocation against exact files.
- Recurrence guard: Avoid downstream formatting pipelines for large multi-pattern searches.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-11-F, V6525-WITNESS-11-P

### V6525-METHOD-12 — Bounded recovery for combined_status_search_timeout

- Trigger: combined_status_search_timeout
- Method: Split repository state from direct file-bounded searches and use Select-String on exact paths.
- Recurrence guard: Do not combine worktree enumeration with content discovery in one bounded wrapper.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-12-F, V6525-WITNESS-12-P

### V6525-METHOD-13 — Bounded recovery for module_symbol_assumption

- Trigger: module_symbol_assumption
- Method: Enumerate top-level assignment names from the parsed syntax tree before importing the module.
- Recurrence guard: Discover phase-data symbols before reusing count wrappers across generations.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-13-F, V6525-WITNESS-13-P

### V6525-METHOD-14 — Bounded recovery for proposal_source_field_assumption

- Trigger: proposal_source_field_assumption
- Method: Inspect the exact proposal and source keys before testing their relationship.
- Recurrence guard: Bind source-coverage checks to inspected schema keys rather than inherited field names.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-14-F, V6525-WITNESS-14-P

### V6525-METHOD-15 — Bounded recovery for foreground_generator_timeout

- Trigger: foreground_generator_timeout
- Method: Confirm no child remains, preserve the intermediate state as zero-credit evidence, and run the same deterministic builder in one hidden bounded process while polling its explicit exit code and logs.
- Recurrence guard: Run process-heavy Method Flow generation under a pollable bounded process instead of a short foreground wrapper.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-15-F, V6525-WITNESS-15-P

### V6525-METHOD-16 — Bounded recovery for generated_test_count_literal

- Trigger: generated_test_count_literal
- Method: Compare ledger counts to the generated negative-register length instead of freezing a numeric literal in test source.
- Recurrence guard: Use schema relationships rather than lifecycle-sensitive count literals in generated tests.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-16-F, V6525-WITNESS-16-P

### V6525-METHOD-17 — Bounded recovery for background_launch_policy_rejection

- Trigger: background_launch_policy_rejection
- Method: Use unique log filenames and a launch-only Start-Process command with an explicit interpreter and hidden window.
- Recurrence guard: Separate optional log housekeeping from process launch and avoid destructive operations in orchestration wrappers.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6525-WITNESS-17-F, V6525-WITNESS-17-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
