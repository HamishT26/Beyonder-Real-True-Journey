# v470 THOS v8 x1 Regression Report

Regression suite: `thos_assertion_manifest_regression_v1`

Status: `PASS_SHAPE_ONLY`

Case count: `18`

## Result

All existing manifest, path-list, assertion-boundary, expected-negative, duplicate, coverage, and stray-artifact cases still match their expected outcomes after the missing-required evaluator was added.

Every passing case reports an empty `missing_required_reason_codes` list and an empty `unexpected_extra_reason_codes` list.

## Boundary

The regression is tempdir-only and curated-summary-only. It does not perform connector writes, cloud writes, destructive cleanup, publication authority changes, or GMUT gate movement.
