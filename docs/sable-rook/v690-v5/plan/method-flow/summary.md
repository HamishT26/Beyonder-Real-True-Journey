# GHC Family Method Flow State

- Phase: v690-v5-planning
- Owner: Sable Rook
- Methods: 3
- Passing witnesses: 3
- Failed witnesses retained: 3

## Preferred methods

### SR6905-START-M001 — Exact global-tool root recovery

- Trigger: current v5 reviewer discovery; broad global-tools inventory
- Method: Use the exact family-settlement-lab root named by current authority and inspect only its bounded files.
- Recurrence guard: Prefer the exact authority-named tool root before any broad recursive catalogue search.
- Rollback: Stop discovery without writing repository or global state.
- Witnesses: SR6905-START-W001-F, SR6905-START-W001-P

### SR6905-PLAN-M002 — Case-token request distinctness recovery

- Trigger: 200 planned operation/input contracts; exact request-digest novelty gate
- Method: Add one explicit case provenance token to each request while keeping the operation semantics and expected output unchanged.
- Recurrence guard: Count canonical request digests before committing the planning root and bind each bounded case to an explicit provenance token.
- Rollback: Retain the 178-distinct failed planning output and stop before any lifecycle commit.
- Witnesses: SR6905-PLAN-W002-F, SR6905-PLAN-W002-P

### SR6905-PLAN-M003 — Exact sparse-stage recovery

- Trigger: parentless Sable worktree; inherited sparse-checkout metadata; exact planning allowlist
- Method: Keep shared sparsity unchanged and use git add --sparse only for the exact Sable planning paths.
- Recurrence guard: Inspect sparse-checkout rules before the first stage in a parentless worktree and use an exact sparse-aware allowlist.
- Rollback: Retain the refused stage, inspect partial index state, and do not reset or rewrite the branch.
- Witnesses: SR6905-PLAN-W003-F, SR6905-PLAN-W003-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
