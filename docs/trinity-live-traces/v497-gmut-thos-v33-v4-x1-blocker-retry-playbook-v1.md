# v497 GMUT/THOS v33 v4 x1 Blocker Retry Playbook

- overall_status: `PASS_BLOCKER_RETRY_PLAYBOOK_READY`
- generated_utc: `2026-06-06T18:14:17Z`
- retry_limit_per_blocker: `5`

## Blocker Classes

- BLOCKER-CLI-HEADING-SHAPE: use the standalone heading template, dry prompt checks, numbered placeholders, status-only quality gates, then exact approval if still open.
- BLOCKER-CLI-MARKER-REVIEW: split generic sensitive vocabulary from strict path/key/private-material markers, publish counts only, and block summaries if strict markers appear.
- BLOCKER-APP-WATCHER-WAIT: cadence gate first, gate-only app notifier second, stale-flow refresh third, blocker receipt if route remains unavailable.
- BLOCKER-SOURCE-DRIFT: fetch, inspect drift, avoid reset/rebase, and publish only after drift returns to zero or an approved resolution exists.
- BLOCKER-OVERCLAIM: run no-overclaim guard, replace closure claims with open-gate wording, add claim boundaries, then rerun guard.
- BLOCKER-PROVENANCE-GAP: run the provenance helper with repo-relative subjects and material hashes; block if subjects are missing.
- BLOCKER-SKILL-MUTATION-SCOPE: downgrade to repo-scoped candidates unless exact live skill/plugin-cache approval exists.

## x2 Use

Use this playbook during v497 v4 x2 build/run/test/use work and future v497 v5-v8 x1/x2 phases. It does not publish raw lane text, raw transport, destructive cleanup, plugin-cache/user-skill mutation, or GMUT gate closure.
