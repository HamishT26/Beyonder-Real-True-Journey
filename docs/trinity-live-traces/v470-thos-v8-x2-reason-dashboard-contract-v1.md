# v470 THOS v8 x2 Reason Dashboard Contract

The compact fixture must preserve the full reason-code evidence needed by a future renderer.

## Required Row Fields

- `case_id`
- `expected_reason_codes`
- `matched_reason_codes`
- `missing_required_reason_codes`
- `allowed_extra_reason_codes`
- `unexpected_extra_reason_codes`
- `reason_codes`
- `expected_dominant_reason_code`
- `observed_dominant_reason_code`
- `primary_selection_mode`
- `matches_expected`
- `row_status`

## Boundary

This is a local fixture contract. It does not authorize connector writes, cloud writes, destructive cleanup, publication authority, renderer migration, or GMUT gate movement.
