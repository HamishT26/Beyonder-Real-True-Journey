# v462A_GMUT_v3 Null-Recovery Fixture v1

Generated UTC: 2026-05-29T08:50:45Z
Generated NZ: 2026-05-29T20:50:45+12:00

## Scope

This is a bounded P2 symbolic fixture over the declared v462A candidate equation scaffold. It is not GMUT validation, not external GR/LambdaCDM/SM validation, and not final physics.

## Fixture A: Hard Null Spacetime Extension

- evidence: Candidate expression was `G + Lambda_g = kappa*(T_SM + T_DM + alpha_Psi*T_Psi) + alpha_B*B_Psi`.
- evidence: Declared baseline expression was `G + Lambda_g = kappa*(T_SM + T_DM)`.
- evidence: With `alpha_Psi = 0` and `alpha_B = 0`, disabled extension source terms reduce to the declared baseline expression in this string-level scaffold fixture.
- advisory: Safe label is `pass_candidate_null_recovery_observed_for_declared_string_fixture_only`.
- blocker: This does not close physical null recovery because full tensor derivation, conservation accounting, external baseline comparators, and fifth-force/equivalence mapping are not executed.

## Fixture B: Decoupled Scalar Limit

- blocker: Setting `alpha_B = 0` is insufficient by itself.
- blocker: `Psi`, `V(Psi)`, scalar source behavior, `T_Psi_mu_nu`, and conservation or exchange accounting remain underdefined.
- advisory: Safe label is `blocker_missing_scalar_definition_and_exchange_accounting`.

## Gate Status

- blocker: Null recovery remains open with one scaffold-level observation.
- blocker: Dimensional consistency remains open.
- blocker: Conservation or exchange law remains open.
- blocker: Baseline recovery remains open.
- blocker: Fifth-force/equivalence constraints remain open.
- blocker: Consciousness measurement bridge remains open and is not advanced by this fixture.

## Handoff

v462A_GMUT_v4 should upgrade from string-level fixture receipts to tensor/formal derivation and conservation accounting before broader null-recovery language is used.
