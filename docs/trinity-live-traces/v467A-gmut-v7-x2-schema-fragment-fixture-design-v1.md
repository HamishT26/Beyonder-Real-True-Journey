# v467A GMUT v7 x2 Schema Fragment and Fixture Design

Prepared: 2026-06-01T22:23:17+12:00

This artifact designs future schema fragments and fixture bundles. It does not execute them.

## Schema Fragments

Planned fragments include manifest envelope, literal input row, derived lint report, identity record, reference handle, coefficient/unit quantity, residual adjudication, provenance triple, gate-carry report, and no-result envelope.

## Fixture States

- `clean`: schema fields complete and no conflicts, but still `not_run/no_result`.
- `conflicted`: required rows exist but conflict.
- `quarantined`: row family blocked by definition or overclaim risk.
- `no_result_heavy`: rows are structurally present but lack exact artifacts, comparison rules, or measurement inputs.

## Test Designs Not Run

Future designs include canonicalization golden tests, cross-manifest reference integrity tests, identity ambiguity tests, diff/merge conflict fixtures, coefficient/SI failure fixtures, residual adjudication fixtures, conservation/exchange tables, overhang/proxy/falsifier lint cases, and readiness memo generation cases.

No fixture state validates GMUT or closes a gate.
