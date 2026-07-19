# GHC Family Method Flow State

- Phase: v649-gmut-thos-v4-x1-x2
- Owner: Orin Thale
- Methods: 17
- Passing witnesses: 17
- Failed witnesses retained: 17

## Preferred methods

### V6494-M01 — Windows ripgrep include-pattern recovery

- Trigger: Windows filesystem; multiple Python filenames selected by wildcard
- Method: Pass explicit directories to ripgrep and constrain filenames with -g patterns rather than shell wildcards.
- Recurrence guard: On Windows, use rg explicit directories with -g include patterns; never pass unexpanded wildcard paths.
- Rollback: Stop the search and leave repository content unchanged.
- Witnesses: V6494-M01-WFAIL, V6494-M01-WPASS

### V6494-M02 — Method Flow auto-promotion state inspection

- Trigger: candidate method; new passing witness; subsequent promotion request
- Method: After adding a passing witness, inspect the ledger state and request only the next legal transition.
- Recurrence guard: Inspect method state after every witness operation before issuing a state transition.
- Rollback: Leave the auto-promoted validated state unchanged and do not rewrite ledger history.
- Witnesses: V6494-M02-WFAIL, V6494-M02-WPASS

### V6494-M09 — Native Git output parse separation

- Trigger: PowerShell native command; git ls-remote output; hash parsing
- Method: Capture native git output first, verify its exit status, and split the captured line in a separate statement.
- Recurrence guard: Evaluate native commands and parse captured output in separate statements.
- Rollback: Discard the malformed equality result and leave repository state unchanged.
- Witnesses: V6494-M09-WFAIL, V6494-M09-WPASS

### V6494-M10 — Isolated no-profile lifecycle probes

- Trigger: Windows shell startup; grouped read-only checks; bounded timeout
- Method: Run unrelated read-only checks as isolated no-profile commands with bounded timeouts.
- Recurrence guard: Use no-profile isolated probes for bounded Windows lifecycle checks instead of grouping unrelated startup-sensitive commands.
- Rollback: Terminate the timed-out wrapper and leave repository content unchanged.
- Witnesses: V6494-M10-WFAIL, V6494-M10-WPASS

### V6494-M11 — Split local and live-remote equality probes

- Trigger: four-way Git equality; live network lookup; combined-probe timeout
- Method: Separate local Git evidence from the live network lookup and give the latter its own bounded window.
- Recurrence guard: Isolate live network lookups from local Git checks and assign them an explicit bounded network timeout.
- Rollback: Terminate the timed-out probe and leave repository and refs unchanged.
- Witnesses: V6494-M11-WFAIL, V6494-M11-WPASS

### V6494-M12 — Measured large-checkout status window

- Trigger: large inherited checkout; git status enumeration; short-bound timeout
- Method: Rerun unchanged local equality criteria under a measured longer timeout reserved for large-checkout status enumeration.
- Recurrence guard: Budget status enumeration separately for inherited large checkouts and do not infer cleanliness from a timed-out probe.
- Rollback: Terminate the short probe and leave repository state unchanged.
- Witnesses: V6494-M12-WFAIL, V6494-M12-WPASS

### V6494-M13 — Substantive mechanism replacement after frozen collision

- Trigger: frozen proposal corpus; lexical collision threshold; same-mechanism seed
- Method: Withdraw the colliding catalogue-adapter seed and substitute a distinct numerical-implementation protocol under the unchanged threshold.
- Recurrence guard: Treat a different instrument or catalogue as insufficient novelty when the evidence mechanism and prerequisite shape collide.
- Rollback: Abort preregistration before packet writes and preserve the frozen corpus unchanged.
- Witnesses: V6494-M13-WFAIL, V6494-M13-WPASS

### V6494-M14 — Practice mechanism replacement after threshold collision

- Trigger: new practice lens; repeated workflow mechanism; frozen semantic audit
- Method: Replace the repeated intake-hold-handover mechanism with a distinct assay sampling and result-custody mechanism.
- Recurrence guard: A new practice domain does not make a repeated intake-hold-handover mechanism novel; change the operational hypothesis and falsifier.
- Rollback: Abort the freeze, remove the repeated seed, and preserve the prior phase's credit and frozen title unchanged.
- Witnesses: V6494-M14-WFAIL, V6494-M14-WPASS

### V6494-M15 — Authority mechanism replacement after frozen collision

- Trigger: authority matrix; new domain; frozen threshold collision
- Method: Replace the inherited-shaped authority matrix with a seed-specific sensitive-knowledge metadata and withdrawal reservation.
- Recurrence guard: Do not treat a new beneficiary domain as novelty when the authority-matrix fields and completion gate are inherited.
- Rollback: Abort the freeze and preserve both the prior proposal and every authority gate unchanged.
- Witnesses: V6494-M15-WFAIL, V6494-M15-WPASS

### V6494-M16 — UTF-8-pinned frozen-title diagnostic

- Trigger: PowerShell host; Python diagnostic; Unicode frozen title
- Method: Pin Python UTF-8 mode before rerunning the exact frozen-title diagnostic.
- Recurrence guard: Pin UTF-8 before any diagnostic that may emit Māori or other non-CP1252 text.
- Rollback: Discard the incomplete diagnostic output and leave repository content unchanged.
- Witnesses: V6494-M16-WFAIL, V6494-M16-WPASS

### V6494-M03 — Recover memory_registry_no_current_match without erasing its failed witness

- Trigger: A bounded v649-v4 workflow exposes memory_registry_no_current_match.
- Method: Retain the no-match and use the live activation plus exact Git evidence as current authority.
- Recurrence guard: Treat exact-current memory absence as absence, not proof or contradiction.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6494-M03-WFAIL, V6494-M03-WPASS

### V6494-M04 — Recover overbroad_worktree_inventory without erasing its failed witness

- Trigger: A bounded v649-v4 workflow exposes overbroad_worktree_inventory.
- Method: Use compact exact-repository probes for named owner and source worktrees after locating them.
- Recurrence guard: Use the global worktree list only for discovery, then switch to exact named probes.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6494-M04-WFAIL, V6494-M04-WPASS

### V6494-M05 — Recover schema_probe_overoutput without erasing its failed witness

- Trigger: A bounded v649-v4 workflow exposes schema_probe_overoutput.
- Method: Query only top-level keys, counts, targeted titles, or exact semantic-neighbor terms.
- Recurrence guard: Never serialize the full frozen index when only schema fields or neighbors are needed.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6494-M05-WFAIL, V6494-M05-WPASS

### V6494-M07 — Recover fast_forward_summary_truncation without erasing its failed witness

- Trigger: A bounded v649-v4 workflow exposes fast_forward_summary_truncation.
- Method: Run exact head, branch, clean, divergence, tracking, and live-remote probes after the fast-forward.
- Recurrence guard: Validate a large fast-forward with separate compact exact probes.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6494-M07-WFAIL, V6494-M07-WPASS

### V6494-M08 — Recover token_inventory_output_truncation without erasing its failed witness

- Trigger: A bounded v649-v4 workflow exposes token_inventory_output_truncation.
- Method: Use narrower exact-token and file-specific searches for each substantive replacement.
- Recurrence guard: Use broad searches only for discovery and narrow them before awarding completeness credit.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6494-M08-WFAIL, V6494-M08-WPASS

### V6494-M17 — Idempotent x1-output allowlist with x2 marker rejection

- Trigger: existing generated x1 packet; receipt refresh; strict x1-before-x2
- Method: Allow existing phase-owned x1 outputs on rerun while rejecting explicit x2 lifecycle names and observed-outcome keys.
- Recurrence guard: Separate first-run seed allowlists from idempotent x1-output allowlists and keep explicit x2 marker rejection in both.
- Rollback: Abort the rebuild before writes and preserve the already-generated x1 tree.
- Witnesses: V6494-M17-WFAIL, V6494-M17-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
