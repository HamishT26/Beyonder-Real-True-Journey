# v470 THOS v7 x2 Report Assertion Contract

Phase: `v470_THOS_v7_x2`
Created NZ: `2026-06-02T18:15:45+12:00`

## Contract

v7 x2 adds `scripts/thos_visualization_report_assert.py`, a local non-mutating assertion layer over THOS visualization binding reports. It rederives aggregate status, dominant and secondary findings, digest-reference presence, row-to-summary count reconciliation, and explicit no-GMUT-gate-effect boundaries from report details.

## Boundary

This contract validates local report shape and reconciliation only. It does not authorize connector writes, certify security, validate GMUT, close GMUT gates, prove fifth-force safety, or prove consciousness claims.
