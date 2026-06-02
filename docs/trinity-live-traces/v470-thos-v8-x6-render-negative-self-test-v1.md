# v470 THOS v8 x6 Render Negative Self-Test

Phase: `v470_THOS_v8_x6`

Status: `PASS_SHAPE_ONLY`

## Negative Cases

- `missing_required_label`: failed as expected on `required_labels`.
- `case_count_mismatch`: failed as expected on `case_count_parity`.
- `row_count_mismatch`: failed as expected on `row_count_parity`.

## Boundary

The negative mutations are in-memory checker probes only. No source artifact, rendered artifact, connector, cloud resource, or GMUT gate was mutated by this self-test.
