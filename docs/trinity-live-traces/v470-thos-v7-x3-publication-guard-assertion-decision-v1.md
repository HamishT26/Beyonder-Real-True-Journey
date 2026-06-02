# v470 THOS v7 x3 Publication Guard Assertion Decision

Phase: `v470_THOS_v7_x3`
Created NZ: `2026-06-02T18:37:36+12:00`

## Decision

`scripts/thos_publication_guard.py` now has an explicit assertion-artifact requirement path. It is not silently enabled for every phase. A phase or caller must request it with `--require-assertion-artifacts`, and it can require named fixture coverage with repeated `--require-assertion-coverage` flags.

## Boundary

This is local THOS readiness evidence only. It does not authorize connector writes, certify security, validate GMUT, close GMUT gates, prove fifth-force safety, or prove consciousness claims.
