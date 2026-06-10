# v470 THOS v6 x5 Row-Universe Invariants

This invariant sheet freezes the local row-universe rules used by v6 x5.

## Core Rule

For this phase, visualization JSON and the row-universe digest are two views of the same canonical local row set. Bad rows must be counted and classified, not silently dropped.

## Required Fields

- `row_id`.
- `family`.
- `status`.

## Digest Rule

The digest is SHA-256 over sorted `row_id` values with LF separators. This is intentionally simple and reproducible. v6 x6 can expand it to include status and provenance fields if needed.

## Boundary

All invariants are THOS infrastructure invariants. They do not close GMUT gates.
