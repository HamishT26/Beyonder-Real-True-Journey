# v470 THOS v7 x7 Case-To-Code Matrix

This matrix summarizes the 18 tempdir-only regression cases for `v470_THOS_v7_x7`.

## Matrix Rule

Each expected-negative case must fail closed, include all required reason codes, and expose the expected `dominant_reason_code`. Extra reason codes are tolerated only as local secondary codes when listed in the matrix.

## Result

All 18 cases matched expected behavior. The happy-path case remained `PASS_SHAPE_ONLY`; all malformed or unsafe cases produced expected local refusal evidence.

## Boundary

The matrix is fixture coverage, not platform-wide safety coverage. It does not authorize connector writes, cloud writes, cleanup, publication, GMUT validation, or GMUT gate movement.
