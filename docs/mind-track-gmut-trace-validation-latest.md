# GMUT External-Anchor Trace Validation Report

- generated_utc: `2026-02-16T10:32:59+00:00`
- overall_status: **PASS**
- relative_tolerance: `1e-09`
- absolute_tolerance: `0.0`

## Checks
| check | status | detail |
|---|---|---|
| canonical_input_exists | PASS | docs/mind-track-external-anchor-canonical-inputs-v1.json |
| trace_manifest_exists | PASS | docs/mind-track-external-anchor-trace-manifest-v1.json |
| canonical_anchors | PASS | anchors=3 |
| manifest_traces | PASS | traces=3 |
| manifest_unique_trace_ids | PASS | unique_ids=3 |
| anchor_rows_scanned | PASS | rows=3 |
| trace_ids_mapped | PASS | all canonical trace IDs mapped in manifest |
| snapshot_paths_exist | PASS | all snapshot files present |
| snapshot_checksums | PASS | all checksums match manifest |
| numeric_consistency | PASS | canonical/manifest/snapshot values align |

## Anchor trace status
| claim_id | anchor_id | trace_id | status | issues |
|---|---|---|---|---|
| GMUT-005 | MICROSCOPE_EP_eta_primary | trace-gmut005-microscope-eta-v1 | PASS | - |
| GMUT-005 | EOTWASH_EP_bucket_primary | trace-gmut005-eotwash-bucket-v1 | PASS | - |
| GMUT-005 | LLR_residual_primary | trace-gmut005-llr-residual-v1 | PASS | - |
