# v470 THOS v7 x5 Manifest Regression Report

Status: `PASS_SHAPE_ONLY`

## Scope

This report records a tempdir-only, local, non-mutating regression harness for the THOS assertion manifest guard. The harness materializes synthetic candidate artifacts in OS temp roots, invokes the real `thos_publication_guard.py` entrypoint, verifies expected allow/deny behavior, and preserves only this curated summary.

## Coverage

- Positive permit rehearsal: `happy_manifest_allows`.
- Missing manifest refusal: `missing_manifest_required`.
- Malformed JSON refusal: `malformed_manifest_json`.
- Path-list mismatch refusal: `path_list_mismatch`.
- Absolute path refusal: `absolute_path_rejected`.
- Traversal path refusal: `traversal_path_rejected`.
- Missing artifact refusal: `missing_artifact_rejected`.
- Expectation/status mismatch refusal: `expectation_status_mismatch`.
- Boundary drift refusal: `boundary_drift_rejected`.
- Coverage gap refusal: `coverage_gap_rejected`.
- Stray assertion refusal: `stray_assertion_rejected`.
- Duplicate artifact ID refusal: `duplicate_artifact_id_rejected`.

## Boundary

The harness provides local guardrail evidence only. It does not grant connector authority, cleanup authority, platform safety certification, remote publication authority, GMUT validation, or GMUT gate closure.

## Result

All 12 cases matched their expected outcomes. Temp roots were cleaned up, and no synthetic temp fixture was curated.
