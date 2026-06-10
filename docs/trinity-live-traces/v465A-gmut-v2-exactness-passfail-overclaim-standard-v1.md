# v465A GMUT v2 Exactness, Pass/Fail, And Overclaim Standard

Status: `standard_recorded_not_satisfied`

This artifact records standards for future fixture attempts. It does not satisfy those standards or close any GMUT gate.

## Exact Enough

A row is exact enough only when switch values, reduced equations, surviving terms, dropped terms, conventions, comparator, order of limits, and expected recovery behavior are all explicit.

Not exact enough: `small`, `negligible`, `approximately zero`, `vanishes in practice`, `can be chosen`, known-limit language without exact equations, or clean output without residual-term audit.

## Pass/Fail Labels

- `not_run`: design or hold only.
- `ready_to_attempt`: inputs present, no result.
- `pass_for_fixture_only`: exact comparison succeeds inside a declared fixture and scope only.
- `fail_for_fixture`: residual term, mismatch, unit issue, exchange issue, or force-response issue contradicts expected behavior.
- `blocked`: required inputs remain missing.

## Guard

Held terms are not disabled. Full scalar disablement can support a baseline-comparator design, but it does not validate the scalar route. Coupling-to-zero can support an interaction diagnostic, but it does not prove baseline recovery. All six gates remain open.
