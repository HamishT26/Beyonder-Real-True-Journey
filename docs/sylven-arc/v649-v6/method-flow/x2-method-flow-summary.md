# GHC Family Method Flow State

- Phase: v649-gmut-thos-v6-x1-x2
- Owner: Sylven Arc
- Methods: 22
- Passing witnesses: 22
- Failed witnesses retained: 12

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

### V6496-M09 — Bind frozen-phase tests to immutable commit-local blobs

- Trigger: A phase-freeze test is selected after the repository has advanced beyond its frozen commit.
- Method: Read frozen JSON through git show at the exact x1 commit while leaving current-phase tests bound to current evidence.
- Recurrence guard: Every successor aggregate must bind historical phase assertions to their immutable commit rather than the mutable working tree.
- Rollback: Give the mutable-loader design no evidence credit, retain the failed inspection witness, and restore the x1 test from its frozen commit if the commit-local loader cannot be demonstrated.
- Witnesses: V6496-M09-WFAIL, V6496-M09-WPASS

### V6496-M10 — Execute and classify V6496-P01 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Disable reclamation, retain the schedule, and fall back to bounded ownership without independent-evidence credit.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Disable reclamation, retain the schedule, and fall back to bounded ownership without independent-evidence credit.
- Witnesses: V6496-M10-WEXEC

### V6496-M11 — Execute and classify V6496-P02 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Withdraw the row, retain the missing obligation, and make no physical, likelihood, constraint, confirmation, quantum-completion, or Theory-of-Everything claim.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Withdraw the row, retain the missing obligation, and make no physical, likelihood, constraint, confirmation, quantum-completion, or Theory-of-Everything claim.
- Witnesses: V6496-M11-WEXEC

### V6496-M12 — Execute and classify V6496-P03 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Retain zero-row refusal and do not infer a force, prediction, fit, constraint, confirmation, or Theory of Everything.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Retain zero-row refusal and do not infer a force, prediction, fit, constraint, confirmation, or Theory of Everything.
- Witnesses: V6496-M12-WEXEC

### V6496-M13 — Execute and classify V6496-P04 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Return to an inert checklist, retain the trace, and issue no real maintenance, stop-use, release, safety, or handover decision.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Return to an inert checklist, retain the trace, and issue no real maintenance, stop-use, release, safety, or handover decision.
- Witnesses: V6496-M13-WEXEC

### V6496-M14 — Execute and classify V6496-P05 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Reject the vector, retain the negative, and make no account, token, key, credential, authorization, or trust decision.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Reject the vector, retain the negative, and make no account, token, key, credential, authorization, or trust decision.
- Witnesses: V6496-M14-WEXEC

### V6496-M15 — Execute and classify V6496-P06 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Remove any accidental disclosure or authority claim, retain the failure, and preserve person, asset, location, land, remedy, and cultural privacy.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Remove any accidental disclosure or authority claim, retain the failure, and preserve person, asset, location, land, remedy, and cultural privacy.
- Witnesses: V6496-M15-WEXEC

### V6496-M16 — Execute and classify V6496-P07 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Disable parsing, retain the fixture, and expose only inert bounded metadata.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Disable parsing, retain the fixture, and expose only inert bounded metadata.
- Witnesses: V6496-M16-WEXEC

### V6496-M17 — Execute and classify V6496-P08 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Publish a non-sticky fallback and retain each structural failure.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Publish a non-sticky fallback and retain each structural failure.
- Witnesses: V6496-M17-WEXEC

### V6496-M18 — Execute and classify V6496-P09 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Remove the analogy, retain the physical statement only, and preserve the rejected conversion.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Remove the analogy, retain the physical statement only, and preserve the rejected conversion.
- Witnesses: V6496-M18-WEXEC

### V6496-M19 — Execute and classify V6496-P10 within its preregistered gate

- Trigger: The dedicated x1 commit is pushed, clean, and four-way equal.; The proposal remains within its declared execution lane.
- Method: Retain the failed fixture and keep causal-effect, participant-effect, deployment, and Stage 20 claims false.
- Recurrence guard: Re-evaluate the exact falsifier, retain rejected mutations, and never promote a bounded disposition beyond its protected gates.
- Rollback: Retain the failed fixture and keep causal-effect, participant-effect, deployment, and Stage 20 claims false.
- Witnesses: V6496-M19-WEXEC

### V6496-M20 — Link bounded execution methods to their retained synthetic negatives

- Trigger: A bounded evidence-builder or validator wrapper fails before evidence credit is assigned.
- Method: Reconstruct x2 Method Flow from the immutable x1 ledger and link each core method and witness to its exact seven executed-and-rejected mutation identifiers.
- Recurrence guard: A Method Flow method must never be recorded without a non-empty retained-negative linkage; successful bounded executions link their rejected falsifiers.
- Rollback: Give the failed attempt zero credit, preserve its receipt or signature, and reconstruct only from the immutable x1 boundary.
- Witnesses: V6496-M20-WFAIL, V6496-M20-WPASS

### V6496-M21 — Separate wrapper deadlines from durable diagnostic receipts

- Trigger: A bounded evidence-builder or validator wrapper fails before evidence credit is assigned.
- Method: Inspect process state and the durable receipt separately, retain the wrapper timeout, and use a longer bounded envelope for the next validator call.
- Recurrence guard: A wrapper timeout receives no pass credit; inspect process and receipt state before any retry and keep the timeout as an operational negative.
- Rollback: Give the failed attempt zero credit, preserve its receipt or signature, and reconstruct only from the immutable x1 boundary.
- Witnesses: V6496-M21-WFAIL, V6496-M21-WPASS

### V6496-M22 — Compare manifests to file-level Git status domains

- Trigger: A bounded evidence-builder or validator wrapper fails before evidence credit is assigned.
- Method: Compose modified, staged, and git ls-files --others results at file granularity before comparing the exact manifest union.
- Recurrence guard: Never compare a file manifest with porcelain output unless untracked-files=all is explicit; prefer exact diff and ls-files composition.
- Rollback: Give the failed attempt zero credit, preserve its receipt or signature, and reconstruct only from the immutable x1 boundary.
- Witnesses: V6496-M22-WFAIL, V6496-M22-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
