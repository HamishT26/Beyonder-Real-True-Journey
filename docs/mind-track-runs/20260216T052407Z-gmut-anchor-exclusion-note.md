# GMUT External-Anchor Numeric Exclusion Note

- generated_utc: `2026-02-16T05:24:07+00:00`
- overall_status: **WARN**
- comparator_status: `PASS`
- comparator_max_abs_deviation: `0.04964`
- required_canonical_fields_present: `True`

## Anchor comparisons
| claim_id | anchor_id | source_tier | confidence | ext_bound | ext_uncertainty | conservative_bound | gmut_working_bound | overhang_factor | ingestion_status | interpretation |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| GMUT-005 | MICROSCOPE_EP_eta | secondary | 0.950 | 1.000000e-14 | 2.000000e-15 | 1.200000e-14 | 1.000000e-06 | 8.333e+07 | pending_primary_ingestion | requires_tighter_parameter_fit |
| GMUT-005 | EOTWASH_scalar_range_bucket | secondary | 0.950 | 5.000000e-13 | 1.000000e-13 | 6.000000e-13 | 1.000000e-06 | 1.667e+06 | pending_primary_ingestion | requires_tighter_parameter_fit |
| GMUT-005 | LLR_long_range_residual | secondary | 0.950 | 1.000000e-11 | 2.000000e-12 | 1.200000e-11 | 1.000000e-06 | 8.333e+04 | pending_primary_ingestion | requires_tighter_parameter_fit |

## Governance note
These comparisons are **parameter-screening signals**. Any anchor flagged as provisional,
secondary-tier, or pending canonical ingestion remains an open evidence gap.
Promotion requires primary-source ingestion with explicit confidence/uncertainty metadata.
