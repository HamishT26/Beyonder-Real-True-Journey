# v470 THOS v8 x1 Missing-Required Policy

The local THOS assertion-manifest regression harness now exposes missing required reason codes as first-class evidence.

## Rule

A case passes only when every expected code is present, no missing required code is reported, no unexpected extra code is reported, and the dominant code matches the expected primary code.

## Evidence Fields

- `matched_reason_codes`
- `missing_required_reason_codes`
- `unexpected_extra_reason_codes`
- `expected_dominant_reason_code`
- `observed_dominant_reason_code`
- `matches_expected`

## Boundary

This is local harness behavior only. It does not authorize connector writes, cloud writes, destructive cleanup, publication authority, GMUT validation, or GMUT gate movement.
