# v496 GMUT/THOS v32 v7 x2 Wait Policy Blocker Repair

- Status: `PASS_WAIT_POLICY_BLOCKER_REPAIRED`
- Blocker: `WEB_SEARCH_COUNT_SCHEMA_MISMATCH`
- Initial status: `FAIL_WAIT_POLICY_BLOCKER`

## Root Cause

The wait-policy guard expected `search_queries_completed` at the top level, while the source ledger stores the count under `prep_window.search_queries_completed`.

## Five Safe Fix Attempts

1. Ran the wait-policy guard and captured the failing row without mutating live skills, plugin cache, lanes, or raw transport. Result: `web_searches_at_least_30` reported `count=None`.
2. Inspected the curated source ledger shape only. Result: `prep_window.search_queries_completed=32`.
3. Patched the wait-policy guard to read top-level `search_queries_completed` first and `prep_window.search_queries_completed` as a safe fallback. Result: guard code compiled.
4. Reran the wait-policy guard against the framework, source ledger, reflection ledger, and cadence gate. Result: `PASS_WAIT_POLICY_GUARD`.
5. Cross-checked all current v7 x2 JSON artifacts and reran the no-overclaim guard over the expanded artifact set. Result: JSON parse passed and no-overclaim reported zero blocker hits.

## Carry Forward

1. Future source-ledger guards should support nested summary counts when receipts keep counts inside a `prep_window` object.
2. A schema mismatch should be treated as a repairable guard adapter issue when source evidence is present and validated.
3. Five safe attempts can complete early when the blocker is repaired and validated without unsafe escalation.

Claim boundary: no raw lane text, raw transport, credentials, local absolute paths, user-skill mutation, plugin-cache mutation, GMUT validation, or canon promotion is claimed.
