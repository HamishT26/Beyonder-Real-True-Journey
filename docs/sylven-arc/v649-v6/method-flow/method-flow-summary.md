# GHC Family Method Flow State

- Phase: v649-gmut-thos-v6-x1-x2
- Owner: Sylven Arc
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 8

## Preferred methods

### V6496-M01 — Recover powershell_foreach_formatter_parse_fault while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes powershell_foreach_formatter_parse_fault.
- Method: Emit scalar path results directly without a formatter pipeline.
- Recurrence guard: Do not pipe directly from a PowerShell foreach statement; assign or emit scalar rows first.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M01-WFAIL, V6496-M01-WPASS

### V6496-M02 — Recover manifest_byte_domain_conflation while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes manifest_byte_domain_conflation.
- Method: Verify path-filtered Git blob identity separately from checkout-byte receipts.
- Recurrence guard: Keep raw blob, path-filtered blob, and checkout-byte domains explicit in every manifest replay.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M02-WFAIL, V6496-M02-WPASS

### V6496-M03 — Recover mixed_line_ending_filter_replay_mismatch while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes mixed_line_ending_filter_replay_mismatch.
- Method: Use the clean canonical working-tree byte receipt for the nonreconstructable mixed-line-ending domain and require its path-filtered object to equal the commit tree.
- Recurrence guard: Never infer historical mixed checkout bytes solely from a normalized Git blob and current smudge filter.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M03-WFAIL, V6496-M03-WPASS

### V6496-M04 — Recover narrow_source_probe_timeout while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes narrow_source_probe_timeout.
- Method: Rerun only the scalar checks under a bounded sixty-second envelope.
- Recurrence guard: Use realistic Windows Git wrapper budgets and give timed-out attempts no credit.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M04-WFAIL, V6496-M04-WPASS

### V6496-M05 — Recover git_object_path_separator_fault while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes git_object_path_separator_fault.
- Method: Use repository-relative forward slashes and check each Git child exit code.
- Recurrence guard: Normalize Git object paths to forward slashes and fail on every nonzero child exit.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M05-WFAIL, V6496-M05-WPASS

### V6496-M06 — Recover expected_no_match_exit_misclassified while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes expected_no_match_exit_misclassified.
- Method: Use explicit no-match-aware structured term counts.
- Recurrence guard: Distinguish expected search absence from execution failure before assigning evidence credit.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M06-WFAIL, V6496-M06-WPASS

### V6496-M07 — Recover semantic_seed_collisions while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes semantic_seed_collisions.
- Method: Withdraw every collision and replace them with RGS product semantics, RFC 9701 introspection JWTs, and Focus Not Obscured without lowering the threshold.
- Recurrence guard: A new dataset, standard number, profession, or label does not establish a distinct mechanism.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M07-WFAIL, V6496-M07-WPASS

### V6496-M08 — Recover memory_registry_current_phase_absence while retaining the failed witness

- Trigger: A bounded v649-v6 workflow exposes memory_registry_current_phase_absence.
- Method: Retain the absence and use the live verified baton, committed pointer, and exact Git proof for current truth.
- Recurrence guard: Treat absent current memory as absence, never as proof or route authority.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6496-M08-WFAIL, V6496-M08-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
