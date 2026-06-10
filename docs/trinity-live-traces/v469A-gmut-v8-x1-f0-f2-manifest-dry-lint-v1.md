# v469A GMUT v8 x1 F0/F2 Manifest Dry-Lint

Classification: `advisory`

Execution status: `dry_lint_design_only`

Fixture execution: `not_run`

## Common Required Fields

F0 and F2 manifests must include `fixture_id`, `fixture_family`, `target_gate`, metric signature status, action sign status, coordinate branch rows, units policy, source-authority rows, claim ceiling, execution status, result status, and forbidden claims.

## F0 Null Manifest Fields

F0 must name the baseline reference equation, scalar disablement switches, `Psi` background, gradient-zero requirement, `Q_mu` zero requirement, interaction zero requirement, `B_Psi` status, expected shape reference, residual tolerance policy, comparison rule, and gate verdict.

## F2 Exchange Manifest Fields

F2 must name the interaction family, `Q_mu` definition status, matter-coupling map status, universal-versus-species-specific status, equivalence guard state, fifth-force guard state, screening assumption status, expected non-run reason, and gate verdict.

## Dry-Lint Pass Predicates

The manifest dry-lint can pass only if all required fields exist, execution remains `not_run` or `dry_lint_only`, result status remains `no_result`, all gate verdicts remain open, `B_Psi` is quarantined, `V(Psi)` is symbolic, `T_Psi` is template-only, and the claim ceiling does not exceed `audit_only`.

## Dry-Lint Fail Predicates

The dry-lint must fail if any row uses fixture execution, observed result, matched expectation, recovery, validation, gate closure, dimensional closure, derived EOM, derived `T_Psi`, fifth-force safety, equivalence compatibility, consciousness measurement, final physics, or canon-promotion language.

## Safe Next Step

`v8_x2` may materialize the manifest schema and run dry lint against the schema only.
