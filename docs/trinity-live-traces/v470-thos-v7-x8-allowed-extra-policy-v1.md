# v470 THOS v7 x8 Allowed-Extra Policy

The v7 x8 harness enforces reason-code strictness for local THOS publication-guard regressions.

## Enforced Fields

- `expected_reason_codes`
- `allowed_extra_reason_codes`
- `observed_reason_codes`
- `unexpected_extra_reason_codes`
- `expected_dominant_reason_code`
- `observed_dominant_reason_code`
- `matches_expected`

## Rule

A case passes only when every required code is present, the dominant code matches the expected primary code, and no observed code appears outside required plus allowed extras.

## Boundary

This is local harness enforcement only. It does not authorize connector/cloud writes, cleanup, publication, GMUT validation, or GMUT gate movement.
