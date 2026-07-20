# GHC Family Method Flow State

- Phase: v650-v4
- Owner: Orin Thale
- Methods: 14
- Passing witnesses: 14
- Failed witnesses retained: 14

## Preferred methods

### V6504-M01 — Recover broad_worktree_listing without erasing its failed witness

- Trigger: A bounded v650-v4 workflow exposes broad_worktree_listing.
- Method: Use exact named-path and branch probes for source and owner lanes.
- Recurrence guard: Do not use an unbounded worktree inventory as proof of one named lane.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6504-M01-WFAIL, V6504-M01-WPASS

### V6504-M02 — Recover baton_read_budget without erasing its failed witness

- Trigger: A bounded v650-v4 workflow exposes baton_read_budget.
- Method: Read the committed baton in bounded line-addressed chunks through the exact final line.
- Recurrence guard: Chunk long authoritative files and record explicit end-of-file coverage.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6504-M02-WFAIL, V6504-M02-WPASS

### V6504-M03 — Recover fast_forward_summary_budget without erasing its failed witness

- Trigger: A bounded v650-v4 workflow exposes fast_forward_summary_budget.
- Method: Verify exact head, ancestry, status, and remote equality with bounded post-operation probes.
- Recurrence guard: Treat verbose Git summaries as diagnostics, never as exact state receipts.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6504-M03-WFAIL, V6504-M03-WPASS

### V6504-M04 — Recover frozen_index_schema without erasing its failed witness

- Trigger: A bounded v650-v4 workflow exposes frozen_index_schema.
- Method: Decode and concatenate prior_proposals with new_proposals, then assert the combined count is 800.
- Recurrence guard: Inspect exact JSON keys and assert corpus cardinality before semantic screening.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6504-M04-WFAIL, V6504-M04-WPASS

### V6504-M05 — Recover similarity_sweep_timeout without erasing its failed witness

- Trigger: A bounded v650-v4 workflow exposes similarity_sweep_timeout.
- Method: Run bounded candidate batches and preserve the same tokenization and threshold.
- Recurrence guard: Batch quadratic lexical scans and require an exact candidate count in the receipt.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6504-M05-WFAIL, V6504-M05-WPASS

### V6504-M06 — Recover the skill-creator helper contract without erasing the failed probe

- Trigger: A phase-local skill build needs the official initializer, metadata generator, and quick validator.
- Method: Invoke the initializer and metadata generator with their documented arguments, then call quick_validate only with an actual initialized skill directory.
- Recurrence guard: Do not assume sibling helper scripts expose a uniform argparse help surface; use each documented invocation contract.
- Rollback: Give the failed probe zero validation credit, retain it, and do not modify global skills.
- Witnesses: V6504-M06-WFAIL, V6504-M06-WPASS

### V6504-M07 — Bind historical x1 assertions to immutable Git blobs

- Trigger: A successor phase mutates lifecycle companions that had earlier x1 states.
- Method: Bind lifecycle-specific x1 assertions to exact Git blobs from the immutable x1 commit while leaving successor-state assertions on the current tree.
- Recurrence guard: Historical lifecycle assertions must name the immutable commit and path; never infer x1 state from a successor working tree.
- Rollback: Give the failed aggregate zero pass credit, preserve its three failures, and do not broaden the test selection.
- Witnesses: V6504-M07-WFAIL, V6504-M07-WPASS

### V6504-M08 — Replace lifecycle-fragile Method Flow totals with append-only invariants

- Trigger: A retained recovery appends a method after an earlier evidence-boundary count was asserted.
- Method: Assert Method Flow schema invariants, matching fail/pass totals after recovery, required method IDs, and preferred states instead of freezing a mutable lifecycle count in a successor test.
- Recurrence guard: Use append-only ledger invariants and required identifiers for successor tests; bind exact historical counts only to immutable commit blobs.
- Rollback: Give the second failed aggregate zero pass credit, retain its one failure, and do not delete a method to satisfy the old assertion.
- Witnesses: V6504-M08-WFAIL, V6504-M08-WPASS

### V6504-M09 — Bind Method Flow validation to the documented ledger option

- Trigger: A Method Flow validate or summarize invocation is being composed from memory rather than current help output.
- Method: Use the runner's documented --ledger option for validate and summarize, and supply explicit receipt paths where required.
- Recurrence guard: Read the exact subcommand help and use --ledger rather than transferring option names from another runner.
- Rollback: Give the rejected invocation zero validation credit and retain its parser output before retrying with the documented option.
- Witnesses: V6504-M09-WFAIL, V6504-M09-WPASS

### V6504-M10 — Discover Method Flow mutation subcommands from current help

- Trigger: A Method Flow mutation command is being composed without current subcommand help.
- Method: Use the advertised record and witness subcommands after reading their exact help, instead of assuming add-method and add-witness aliases.
- Recurrence guard: Use the top-level advertised command list, then read help for record and witness before composing a mutation command.
- Rollback: Give both rejected subcommand probes zero workflow credit and retain them before using the advertised commands.
- Witnesses: V6504-M10-WFAIL, V6504-M10-WPASS

### V6504-M11 — Bind manifest inventory to the phase-declared validation directory

- Trigger: A phase-local staged review writes manifests to a declared directory that differs from a generic convention.
- Method: List the phase validation directory directly and treat manifest location as schema data rather than a conventional folder name.
- Recurrence guard: Read exact output paths from the phase review runner or list the existing validation directory; do not assume a generic manifests directory.
- Rollback: Give the failed directory probe zero inventory credit while preserving the already completed staged-review result separately.
- Witnesses: V6504-M11-WFAIL, V6504-M11-WPASS

### V6504-M12 — Resolve inherited test modules from exact inventory

- Trigger: A predecessor validator names a Python module whose source filename has not been verified in the current tree.
- Method: Resolve inherited test modules from the exact repository inventory and Python import discovery rather than inferring a filesystem filename from a module string.
- Recurrence guard: Use rg --files and unittest loader-error inspection before declaring an inherited module present or absent.
- Rollback: Give the failed literal read zero module-inventory credit and do not broaden or silently drop the inherited selection.
- Witnesses: V6504-M12-WFAIL, V6504-M12-WPASS

### V6504-M13 — Bound inherited module searches to relevant source roots

- Trigger: A module-reference search would otherwise traverse the full inherited checkout.
- Method: Restrict module-reference searches to scripts and tests, then use importlib spec discovery for the exact module name.
- Recurrence guard: Search only relevant source roots and use import-spec inspection; never treat a timed-out broad search as absence evidence.
- Rollback: Give the timed-out search zero absence or inventory credit and preserve its timeout before the bounded replacement.
- Witnesses: V6504-M13-WFAIL, V6504-M13-WPASS

### V6504-M14 — Isolate inherited module existence and import probes

- Trigger: A grouped module-resolution diagnostic has timed out or obscured which component completed.
- Method: Use one exact Test-Path check and one isolated importlib spec probe; do not combine them with recursive search or ledger mutations.
- Recurrence guard: Isolate exact existence and import-spec probes so each result is attributable and bounded.
- Rollback: Give the grouped timeout zero selection credit and retain it before isolated probes.
- Witnesses: V6504-M14-WFAIL, V6504-M14-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
