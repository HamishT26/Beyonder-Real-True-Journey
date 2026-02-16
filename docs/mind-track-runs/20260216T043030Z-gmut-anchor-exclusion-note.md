# GMUT External-Anchor Numeric Exclusion Note

- generated_utc: `2026-02-16T04:30:30+00:00`
- overall_status: **WARN**
- comparator_status: `PASS`
- comparator_max_abs_deviation: `0.04964`

## Anchor comparisons
| claim_id | anchor_id | source_kind | external_upper_bound | gmut_working_bound | overhang_factor | interpretation |
|---|---|---|---:|---:|---:|---|
| GMUT-005 | MICROSCOPE_EP_eta | provisional_public_summary | 1.000000e-14 | 1.000000e-06 | 1.000e+08 | requires_tighter_parameter_fit |

## Governance note
These comparisons are **parameter-screening signals**. Any anchor flagged as
`provisional` must be replaced with a canonical external dataset ingestion step
before scientific claims are promoted.
