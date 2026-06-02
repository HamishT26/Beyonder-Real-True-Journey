# v470 THOS v8 x3 Reason Dashboard Assertion Contract

The compact reason dashboard fixture now has a local assertion script: `scripts/thos_reason_dashboard_fixture_assert.py`.

## Asserted Rules

- Top-level fixture fields are present and type constrained.
- Rows contain required reason-code fields.
- Missing required codes rederive from expected reason codes minus observed reason codes.
- Unexpected extra codes rederive from observed reason codes outside expected plus allowed extras.
- A row with missing, unexpected, dominant mismatch, or nonmatching status must be `FAIL_BLOCKER`.
- Summary case-id lists rederive from rows.
- Aggregate status rederives from summary.

## Boundary

This is local assertion coverage only. It does not authorize connector writes, cloud writes, destructive cleanup, renderer migration, publication authority, or GMUT gate movement.
