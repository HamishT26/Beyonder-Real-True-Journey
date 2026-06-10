# v470 THOS v2 x2 Fail-Blocker Fixtures

The fail-blocker fixtures define conditions that must stop publication or prevent a validator result from being elevated beyond advisory/shape status.

## Blocker Catalog

- `FB-001`: missing command registry.
- `FB-002`: mutating command row in advisory/read-only context.
- `FB-003`: dirty-worktree cookbook performs cleanup instead of classifying.
- `FB-004`: publication overclaim without staged diff and remote equality evidence.
- `FB-005`: advisory receipt omits authority, mutation, cleanup, connector, or GMUT boundaries.
- `FB-006`: shape fixture claims runtime success.
- `FB-007`: THOS artifact implies GMUT gate movement.
- `FB-008`: source contamination or fabricated app-lane response.
- `FB-009`: boundary card missing explicit write policy.
- `FB-010`: broad connector approval instead of scoped single operation.
- `FB-011`: merged plugin/MCP/skill boundary scope.
- `FB-012`: cleanup manifest claims action was applied.
- `FB-013`: retention template lacks secret-redaction handling.
- `FB-014`: consent is assumed or inherited.
- `FB-015`: raw logs, session JSONL, screenshots, or credential-bearing material staged or marked publishable.
- `FB-016`: Journey/Solas material promoted beyond `journey_context_not_canon`.

## Non-Negotiable Result

Any of these cases is `FAIL_BLOCKER`. The safe replacement is to narrow the claim, add missing source/retention/approval evidence, or mark the target `OPEN_GAP`.
