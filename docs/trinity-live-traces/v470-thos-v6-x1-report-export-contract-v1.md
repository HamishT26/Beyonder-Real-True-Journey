# v470 THOS v6 x1 Report Export Contract

`scripts/thos_supervisor_gate.py` now supports optional `--output` for a local JSON report export.

The default mode remains stdout-only. The script still does not execute requested actions, call connectors, perform cleanup, spend externally, or validate GMUT.

## Required Row Fields

- `request_id`
- `rule_map_id`
- `authority_route`
- `status`
- `gate_result`
- `expected_status`
- `expected_failure`
- `matches_expected`
- `expected_interpretation`

The export is a local report artifact only. It is not publication authority.
