# v469A GMUT v8 x2 F0/F2 Manifest Schema

Classification: `advisory`

Execution status: `schema_materialized_dry_lint_only`

Fixture execution: `not_run`

## Common Schema

Every future F0/F2 fixture manifest must carry fixture ID, fixture family, target gate, metric-signature status, action-sign status, coordinate branch rows, units policy, source-authority rows, claim ceiling, execution status, result status, and gate verdict.

The current schema pins metric signature and action sign to `EXPLICIT_HOLD`, units to `HOLD_OPEN_GAP`, execution to `not_run`, result to `no_result`, and gate verdict to `open_gap`.

## F0 Null Schema

F0 must later define the baseline reference equation, scalar disablement switches, `Psi` background, gradient-zero requirement, `Q_mu` zero requirement, interaction-zero requirement, `B_Psi` quarantine status, expected shape reference, residual tolerance policy, and comparison rule.

Those execution prerequisites are not present yet.

## F2 Exchange Schema

F2 must later define the interaction family, `Q_mu`, matter-coupling map, universal-versus-species-specific status, equivalence guard, fifth-force guard, screening assumption status, and expected non-run reason.

Those execution prerequisites are not present yet.

## Dry-Lint Result

Result: `pass_as_schema_only`

The schema is useful as a blocker ledger. It is not a fixture run.
