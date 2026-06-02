# v470 THOS v6 x6 Run Status

Phase: `v470_THOS_v6_x6`
Created NZ: `2026-06-02T17:13:52+12:00`

## Status

v6 x6 enhanced the THOS row-universe checker with two digest surfaces: legacy membership identity and richer canonical tuple content. It also added first-class rejected-row accounting and a tempdir-only mixed-invalid payload rehearsal.

## Validation So Far

- Python compile passed for `scripts/thos_row_universe_check.py`.
- Positive row-universe check returned `PASS_SHAPE_ONLY`.
- Mixed-invalid payload rehearsal returned `FAIL_BLOCKER` with exit code `1`.

Local pre-stage publication validation passed. Staged allowlist, diff, commit, push, and remote equality checks are still required before publication can be claimed.

## Boundary

No connector writes or external mutations were performed. All six GMUT gates remain open.
