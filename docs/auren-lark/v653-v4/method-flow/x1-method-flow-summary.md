# GHC Family Method Flow State

- Phase: v653-gmut-thos-v4-x1-x2
- Owner: Auren Lark
- Methods: 13
- Passing witnesses: 13
- Failed witnesses retained: 13

## Preferred methods

### V6534-METHOD-01 — Bounded recovery for broad_memory_registry_search_timeout

- Trigger: broad_memory_registry_search_timeout
- Method: Use one exact fixed-string phase lookup with a bounded timeout and stop when it returns no relevant entry.
- Recurrence guard: Use one exact fixed-string phase lookup with a bounded timeout and stop when it returns no relevant entry.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-01-F, V6534-WITNESS-01-P

### V6534-METHOD-02 — Bounded recovery for combined_memory_skill_and_drive_probe_timeout

- Trigger: combined_memory_skill_and_drive_probe_timeout
- Method: Split memory, skill, and D-drive inspection into separate bounded literal-path probes.
- Recurrence guard: Split memory, skill, and D-drive inspection into separate bounded literal-path probes.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-02-F, V6534-WITNESS-02-P

### V6534-METHOD-03 — Bounded recovery for exact_blob_aggregate_display_truncated

- Trigger: exact_blob_aggregate_display_truncated
- Method: Read the same immutable blob in bounded, numbered line ranges and verify full first-to-last coverage.
- Recurrence guard: Read the same immutable blob in bounded, numbered line ranges and verify full first-to-last coverage.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-03-F, V6534-WITNESS-03-P

### V6534-METHOD-04 — Bounded recovery for thread_list_limit_schema_rejection

- Trigger: thread_list_limit_schema_rejection
- Method: Use the declared maximum of fifty non-pinned tasks; pinned tasks remain included automatically.
- Recurrence guard: Use the declared maximum of fifty non-pinned tasks; pinned tasks remain included automatically.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-04-F, V6534-WITNESS-04-P

### V6534-METHOD-05 — Bounded recovery for worktree_path_separator_registration_misclassification

- Trigger: worktree_path_separator_registration_misclassification
- Method: Normalize path separators or match the exact registry record before classifying worktree registration.
- Recurrence guard: Normalize path separators or match the exact registry record before classifying worktree registration.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-05-F, V6534-WITNESS-05-P

### V6534-METHOD-06 — Bounded recovery for worktree_add_wrapper_timeout_while_checkout_continued

- Trigger: worktree_add_wrapper_timeout_while_checkout_continued
- Method: Do not retry; inspect relevant processes, wait for completion, then verify registration, branch, head, and clean state.
- Recurrence guard: Do not retry; inspect relevant processes, wait for completion, then verify registration, branch, head, and clean state.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-06-F, V6534-WITNESS-06-P

### V6534-METHOD-07 — Bounded recovery for combined_post_timeout_audit_wrapper_timeout

- Trigger: combined_post_timeout_audit_wrapper_timeout
- Method: Split filesystem, process, registry, Git identity, and clean-state checks into bounded probes.
- Recurrence guard: Split filesystem, process, registry, Git identity, and clean-state checks into bounded probes.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-07-F, V6534-WITNESS-07-P

### V6534-METHOD-08 — Bounded recovery for frozen_chain_index_array_key_assumption

- Trigger: frozen_chain_index_array_key_assumption
- Method: Read top-level keys first, then combine prior_proposals and new_proposals exactly as the schema declares.
- Recurrence guard: Read top-level keys first, then combine prior_proposals and new_proposals exactly as the schema declares.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-08-F, V6534-WITNESS-08-P

### V6534-METHOD-09 — Bounded recovery for overbroad_frozen_chain_projection_truncated

- Trigger: overbroad_frozen_chain_projection_truncated
- Method: Use deterministic all-row novelty scoring plus bounded fixed-term collision summaries rather than displaying the entire chain.
- Recurrence guard: Use deterministic all-row novelty scoring plus bounded fixed-term collision summaries rather than displaying the entire chain.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-09-F, V6534-WITNESS-09-P

### V6534-METHOD-10 — Bounded recovery for multi_range_builder_inspection_exceeded_context

- Trigger: multi_range_builder_inspection_exceeded_context
- Method: Read and review one bounded builder range at a time before applying each exact-context patch.
- Recurrence guard: Read and review one bounded builder range at a time before applying each exact-context patch.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-10-F, V6534-WITNESS-10-P

### V6534-METHOD-11 — Bounded recovery for combined_status_and_search_probe_timed_out

- Trigger: combined_status_and_search_probe_timed_out
- Method: Run one-file, one-purpose status or search probes with bounded output and independently recorded results.
- Recurrence guard: Run one-file, one-purpose status or search probes with bounded output and independently recorded results.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-11-F, V6534-WITNESS-11-P

### V6534-METHOD-12 — Bounded recovery for powershell_search_pattern_unterminated

- Trigger: powershell_search_pattern_unterminated
- Method: Use a literal single-quoted bounded search pattern that contains no shell interpolation.
- Recurrence guard: Use a literal single-quoted bounded search pattern that contains no shell interpolation.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-12-F, V6534-WITNESS-12-P

### V6534-METHOD-13 — Bounded recovery for staged_validator_bootstrap_flag_omitted

- Trigger: staged_validator_bootstrap_flag_omitted
- Method: Regenerate the x1 packet with this retained negative, restage the exact candidate, then invoke the validator once with --write before checking receipt freshness without --write.
- Recurrence guard: Regenerate the x1 packet with this retained negative, restage the exact candidate, then invoke the validator once with --write before checking receipt freshness without --write.
- Rollback: Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6534-WITNESS-13-F, V6534-WITNESS-13-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
