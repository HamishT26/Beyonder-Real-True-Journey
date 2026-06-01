# v469A GMUT v4 x1 Forbidden-Claim Lint

Classification: `blocker`

This lint prevents accidental validation or gate closure language.

## Forbidden Phrases

Do not use: `dimensionally consistent`, `covariant proof`, `scalar EOM derived`, `T_Psi derived`, `source-backed validation`, `fixture recovery`, `fifth-force safe`, `consciousness measured`, `gate-ready`, `ready to close`, `validated route`, or `physics confirmed`.

## Lint Rows

1. `lint_c_factor_placement_missing`: refuse Route A if `x0=t` versus `x0=ct`, metric component units, and c placement are not explicit.
2. `lint_dt_d3x_bookkeeping_overclaim`: allow `dt d3x` as bookkeeping candidate only.
3. `lint_d4x_sqrt_g_equivalence_overclaim`: refuse equivalence to `d4x sqrt(-g)` without an exact local derivation artifact.
4. `lint_source_role_ceiling`: refreshed sources support context or constraints only.
5. `lint_journey_solas_noncanon`: Journey/Solas remain `journey_context_not_canon` with local path/line references before use.
6. `lint_consciousness_proxy_false_positive`: proxy rows require false-positive controls and no measurement claim.
7. `lint_B_Psi_quarantine`: `B_Psi` remains quarantined unless separately defined.
8. `lint_V_Psi_symbolic_hold`: symbolic `V(Psi)` cannot support derivative, EOM, stress-energy, or conservation claims.
9. `lint_scalar_EOM_not_derived`: refuse EOM-derived language without explicit local variation.
10. `lint_T_Psi_not_derived`: refuse stress-energy-derived language without explicit metric variation.
11. `lint_fixture_recovery_synonym`: refuse recovery synonyms without execution artifacts.
12. `lint_all_six_gates_open`: all six gates remain open.
