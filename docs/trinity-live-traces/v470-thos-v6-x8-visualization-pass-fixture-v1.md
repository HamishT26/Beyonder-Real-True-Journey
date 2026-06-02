# v470 THOS v6 x8 Visualization Pass Fixture

Phase: `v470_THOS_v6_x8`
Created NZ: `2026-06-02T17:32:47+12:00`

## Fixture

The pass fixture copies the v6 x5 visualization row universe and adds matching `row_identity_digest`, `row_content_digest`, and `derived_from_canonical` fields to each row.

## Boundary

This is a local fixture, not a renderer migration. It proves the checker can recognize a clean digest-reference shape; it does not prove dashboard readiness, publication, safety, connector authority, or GMUT validation.
