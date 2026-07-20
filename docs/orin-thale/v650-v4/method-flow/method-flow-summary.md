# GHC Family Method Flow State

- Phase: v650-v4
- Owner: Orin Thale
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
