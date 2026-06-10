# v470 THOS v7 x6 Reason-Code Regression Report

Phase: `v470_THOS_v7_x6`

Captured: `2026-06-02T19:51:09+12:00`

Result: `PASS_SHAPE_ONLY`

## Scope

This phase hardens the local THOS publication guard by replacing brittle substring-only regression checks with explicit machine-readable `reason_codes` evidence. The work remains a local, non-mutating guardrail receipt only.

No connector writes, cloud writes, destructive cleanup, publication authority, or GMUT gate movement were performed or claimed.

## Regression Result

The tempdir-only regression harness passed 18 cases.

- `happy_manifest_allows` allowed a valid positive plus expected-negative manifest bundle.
- `missing_manifest_required` denied with `MANIFEST_REQUIRED_MISSING`.
- `malformed_manifest_json` denied with `MANIFEST_JSON_UNREADABLE`.
- `unknown_manifest_schema_rejected` denied with `MANIFEST_SCHEMA_INVALID`.
- `path_list_mismatch` denied with `MANIFEST_PATH_LIST_MISMATCH`.
- `unknown_path_list_schema_rejected` denied with `PATH_LIST_SCHEMA_INVALID`.
- `absolute_path_rejected` denied with `MANIFEST_PATH_INVALID`.
- `traversal_path_rejected` denied with `MANIFEST_PATH_INVALID`.
- `duplicate_normalized_path_rejected` denied with `MANIFEST_PATH_DUPLICATE`.
- `windows_case_collision_path_rejected` denied with `MANIFEST_PATH_CASE_COLLISION`.
- `unexpected_role_enum_rejected` denied with `MANIFEST_ROLE_INVALID`.
- `missing_artifact_rejected` denied with `ASSERTION_ARTIFACT_MISSING`.
- `expectation_status_mismatch` denied with `ASSERTION_STATUS_MISMATCH`.
- `expected_negative_unexpected_pass` denied with `ASSERTION_STATUS_MISMATCH` and `ASSERTION_EXPECTED_NEGATIVE_DID_NOT_FAIL`.
- `boundary_drift_rejected` denied with `ASSERTION_BOUNDARY_INVALID`.
- `coverage_gap_rejected` denied with `ASSERTION_COVERAGE_MISSING`.
- `stray_assertion_rejected` denied with `MANIFEST_CLOSED_WORLD_STRAY`.
- `duplicate_artifact_id_rejected` denied with `MANIFEST_ARTIFACT_ID_DUPLICATE`.

All expected reason-code assertions matched. The harness emitted a curated summary only, verified tempdir cleanup, and recorded `temp_fixture_leakage: false`.

## Boundary

This artifact supports future local THOS report clarity and refusal traceability. It does not certify platform safety, approve connector writes, approve cleanup/deletion, validate GMUT, close any GMUT gate, or promote any Journey/Solas material into canon.

## Carry Forward

The next phase should keep the reason-code layer stable while adding a dominant-reason summary, a compact case-to-code matrix, and optional coverage counters for future dashboards. Renderer migration remains blocked until the manifest-aware assertion lane stays green across broader artifact families.
