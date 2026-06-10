# v470 THOS v4 x1 Checker Run

Phase: `v470_THOS_v4_x1`

Checker script: `scripts/thos_publication_guard.py`

## Runs

| Target | Files | Staged Only | Aggregate |
| --- | ---: | --- | --- |
| `v470-thos-v3-x2` | 16 | false | `PASS_SHAPE_ONLY` |
| `v470-thos-v4-x1` | 12 | false | `PASS_SHAPE_ONLY` |

## Row Summary

Both runs reported:

- `artifact_presence PASS_SHAPE_ONLY`
- `path_guard PASS_SHAPE_ONLY`
- `credential_guard PASS_SHAPE_ONLY`
- `forbidden_claim_guard PASS_SHAPE_ONLY`
- `json_parse PASS_SHAPE_ONLY`
- `status_enum PASS_SHAPE_ONLY`
- `trailing_whitespace PASS_SHAPE_ONLY`
- `staged_allowlist NOT_RUN`
- `git_drift PASS_SHAPE_ONLY`

## Claim Ceiling

- The checker run validates publication guard shape only.
- The checker run does not certify workflow safety.
- The checker run does not validate GMUT.
- The checker run does not authorize cleanup or connector writes.
