# v470 THOS v6 x2 Unreconciled Exception Export

This artifact defines the current v6 x2 unreconciled-exception export shape and records that no unreconciled exception rows were produced in this dry-run pass.

## Required Shape

Each future row must include a stable exception ID, source artifact, source row ID, rule-map ID, expected status, actual status, reconciliation status, owner, next required artifact, and explicit GMUT gate effect.

## Current Result

- Unreconciled exception count: `0`.
- Connector writes performed: `false`.
- External mutations performed: `false`.
- GMUT gate effect: `none_open_not_tested`.

## Boundary

An empty exception export is not a validation claim. It only says the current local dry-run exports did not produce an unmapped mismatch.
