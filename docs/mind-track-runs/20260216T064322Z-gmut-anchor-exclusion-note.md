# GMUT External-Anchor Numeric Exclusion Note

- generated_utc: `2026-02-16T06:43:22+00:00`
- overall_status: **WARN**
- comparator_status: `PASS`
- comparator_max_abs_deviation: `0.04964`
- required_canonical_fields_present: `True`
- anchors_with_missing_required_fields: `0`
- anchors_with_missing_trace_or_propagation: `0`

## Anchor comparisons
| claim_id | anchor_id | extraction_trace_id | uncertainty_model | source_tier | confidence | ext_bound | ext_uncertainty | conservative_bound | gmut_working_bound | overhang_factor | ingestion_status | interpretation |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| GMUT-005 | MICROSCOPE_EP_eta_primary | trace:gmut005:microscope:2026-02-16:v1 | linear_bound_addition | primary | 0.950 | 1.000000e-14 | 2.000000e-15 | 1.200000e-14 | 1.000000e-06 | 8.333e+07 | ingested_primary_source | requires_tighter_parameter_fit |
| GMUT-005 | EOTWASH_EP_bucket_primary | trace:gmut005:eotwash:2026-02-16:v1 | linear_bound_addition | primary | 0.950 | 5.000000e-13 | 1.000000e-13 | 6.000000e-13 | 1.000000e-06 | 1.667e+06 | ingested_primary_source | requires_tighter_parameter_fit |
| GMUT-005 | LLR_residual_primary | trace:gmut005:llr:2026-02-16:v1 | linear_bound_addition | primary | 0.950 | 1.000000e-11 | 2.000000e-12 | 1.200000e-11 | 1.000000e-06 | 8.333e+04 | ingested_primary_source | requires_tighter_parameter_fit |

## Governance note
These comparisons are **parameter-screening signals**. Any anchor flagged as provisional,
secondary-tier, or pending canonical ingestion remains an open evidence gap.
Promotion requires primary-source ingestion with explicit confidence/uncertainty metadata.
