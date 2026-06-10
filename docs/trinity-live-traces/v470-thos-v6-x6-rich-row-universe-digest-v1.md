# v470 THOS v6 x6 Rich Row-Universe Digest

Phase: `v470_THOS_v6_x6`
Created NZ: `2026-06-02T17:13:52+12:00`

## Result

- Source artifact: `docs/trinity-live-traces/v470-thos-v6-x5-visualization-row-data-v1.json`
- Validator: `scripts/thos_row_universe_check.py`
- Aggregate status: `PASS_SHAPE_ONLY`
- Source rows: `12`
- Canonical rows: `12`
- Rejected rows: `0`
- Identity digest: `1619e43eaa70f03bafda0864ce9f5b3672a3edae0e0e84cee64c6db9e727eedb`
- Content digest: `d609913bcbb812bf51f3b796b0347b7c5d6d12ddcdac8646d5c767eec68d7ab0`

## Meaning

The identity digest remains the legacy row-membership receipt over sorted `row_id` values. The content digest is the v6 x6 tuple receipt over `row_id`, `family`, `status`, `surface`, and `source_row_id`. A content digest change now records semantic row drift even when the row-id universe is unchanged.

## Boundary

This is a local THOS infrastructure receipt. It does not certify truth, safety, publication, connector approval, GMUT validation, or closure of any GMUT gate.
