# v553-gmut-thos-v3-x1 Cleanup Tier Board

Status: `PASS_CLEANUP_PROPOSALS_TIERED_NON_DESTRUCTIVE`

## Cleanup Proposals

- CLEANUP-01: verify v553 v2 x2 closeout is direct-listed - inspect_or_index - destructive: `false`
- CLEANUP-02: verify v553 v3 x1 active status across current-state and beacon - inspect_or_index - destructive: `false`
- CLEANUP-03: reconcile Goal Mode status mismatch - inspect_or_index - destructive: `false`
- CLEANUP-04: direct-list v553 v3 x1 files after publication - inspect_or_index - destructive: `false`
- CLEANUP-05: direct-list v553 v3 x2 closeout after publication - inspect_or_index - destructive: `false`
- CLEANUP-06: normalize next-lane wording to triad after v3 x2 - inspect_or_index - destructive: `false`
- CLEANUP-07: mark omega-mini-2 primary in all new artifacts - inspect_or_index - destructive: `false`
- CLEANUP-08: mark omega-mini historical baseline - inspect_or_index - destructive: `false`
- CLEANUP-09: mark full omega exact fallback only - inspect_or_index - destructive: `false`
- CLEANUP-10: quarantine stale historical labels unless explicitly referenced as historical - inspect_or_index - destructive: `false`
- CLEANUP-11: deduplicate lookup lists - inspect_or_index - destructive: `false`
- CLEANUP-12: create v553 source index - inspect_or_index - destructive: `false`
- CLEANUP-13: create v553 Journey reflection index - inspect_or_index - destructive: `false`
- CLEANUP-14: create v553 approval index - inspect_or_index - destructive: `false`
- CLEANUP-15: create v553 Eureka index - inspect_or_index - destructive: `false`
- CLEANUP-16: create v553 skill index - inspect_or_index - destructive: `false`
- CLEANUP-17: create v553 runner index - inspect_or_index - destructive: `false`
- CLEANUP-18: create v553 cleanup index - inspect_or_index - destructive: `false`
- CLEANUP-19: validate all new JSON - validation_or_guard - destructive: `false`
- CLEANUP-20: compile all new scripts - validation_or_guard - destructive: `false`
- CLEANUP-21: run whitespace checks - validation_or_guard - destructive: `false`
- CLEANUP-22: run staged-diff review - validation_or_guard - destructive: `false`
- CLEANUP-23: run credential-pattern guard - validation_or_guard - destructive: `false`
- CLEANUP-24: run local-path redaction guard - validation_or_guard - destructive: `false`
- CLEANUP-25: run raw-route/raw-transcript guard - validation_or_guard - destructive: `false`
- CLEANUP-26: run screenshot/session/private-dump guard - validation_or_guard - destructive: `false`
- CLEANUP-27: exact-stage only curated files - validation_or_guard - destructive: `false`
- CLEANUP-28: record unrelated dirty/untracked files as held - publication_gate - destructive: `false`
- CLEANUP-29: build remote-equals-local verification receipt - publication_gate - destructive: `false`
- CLEANUP-30: publish only after phase truth and goal-mode status are consistent - publication_gate - destructive: `false`

## Forbidden Without Fresh Exact Approval

- deletion
- cache purge
- plugin-cache mutation
- external account mutation
- deployment
- purchase
- API-key creation
- global hook install
- reset/rebase/force-push
