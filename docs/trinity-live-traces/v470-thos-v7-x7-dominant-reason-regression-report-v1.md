# v470 THOS v7 x7 Dominant Reason Regression Report

Phase: `v470_THOS_v7_x7`

Captured: `2026-06-02T20:03:57+12:00`

Result: `PASS_SHAPE_ONLY`

## Scope

This phase adds `dominant_reason_code` evidence to local THOS publication-guard failures while preserving the full `reason_codes` array. Dominant selection uses a local priority table, not accidental first-observed ordering.

No connector writes, cloud writes, destructive cleanup, publication authority, or GMUT gate movement were performed or claimed.

## Regression Result

The tempdir-only regression harness passed 18 cases. Each failure case matched both required reason codes and expected dominant reason code. The valid happy-path case remained `PASS_SHAPE_ONLY` with no dominant reason code.

The report remains a local guardrail receipt only. It does not certify safety, authorize publication, authorize connector actions, approve cleanup, validate GMUT, or move any GMUT gate.

## Priority Notes

- Boundary drift has highest explicit priority among coded assertion-artifact failures.
- Malformed JSON and closed-world stray assertion failures outrank ordinary schema/path issues.
- Duplicate artifact IDs outrank duplicate paths and case-colliding paths.
- Missing assertion artifacts outrank coverage gaps caused by those missing artifacts.
- Expected-negative unexpected pass outranks the generic status mismatch it can also trigger.

## Carry Forward

The next phase should add a stable dashboard-facing `primary_selection_mode` matrix and consider separating required secondary codes from allowed extra codes in the regression report itself.
