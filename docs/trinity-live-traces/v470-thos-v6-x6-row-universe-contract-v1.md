# v470 THOS v6 x6 Row-Universe Contract

Phase: `v470_THOS_v6_x6`
Created NZ: `2026-06-02T17:13:52+12:00`

## Contract

v6 x6 keeps two separate receipts. `row_identity_digest` detects membership drift over sorted row IDs. `row_content_digest` detects semantic drift over the canonical tuple: `row_id`, `family`, `status`, `surface`, and `source_row_id`.

Rows with missing required fields, unknown status, duplicate identity, or non-object shape are rejected into explicit buckets. Rejected rows are not silently dropped; they remain part of source-side accounting.

## Pass Criteria

- Source rows equal canonical rows plus rejected rows.
- Canonical and rejected rows are disjoint.
- Digest versions are recorded separately.
- Visualization data projects from canonical rows.
- No connector write, external mutation, or GMUT gate movement occurs.

## Boundary

This contract supports local THOS reconciliation only. It does not certify source truth, operational safety, external publication, or GMUT validity.
