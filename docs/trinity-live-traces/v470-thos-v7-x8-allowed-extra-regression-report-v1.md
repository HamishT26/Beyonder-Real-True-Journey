# v470 THOS v7 x8 Allowed-Extra Regression Report

Phase: `v470_THOS_v7_x8`

Captured: `2026-06-02T20:14:04+12:00`

Result: `PASS_SHAPE_ONLY`

## Scope

This phase moves allowed-extra reason-code policy into the executable tempdir-only regression harness. Each case now checks required reason codes, expected dominant reason code, and unexpected extra reason codes.

No connector writes, cloud writes, destructive cleanup, publication authority, or GMUT gate movement were performed or claimed.

## Regression Result

The harness passed 18 cases. Every case recorded `unexpected_extra_reason_codes: []`.

The valid happy-path case remained `PASS_SHAPE_ONLY`. Every malformed or expected-negative case failed closed with the expected dominant reason code and all required reason codes present.

## Policy

- Required reason codes must all be present.
- Allowed extra reason codes may be present.
- Any unlisted extra reason code fails the case.
- Dominant reason code must equal the expected primary code.
- Full `reason_codes` remain preserved.

## Boundary

This validates local harness behavior only. It does not certify safety, authorize publication, permit connector/cloud writes or cleanup, validate GMUT, or move any GMUT gate.
