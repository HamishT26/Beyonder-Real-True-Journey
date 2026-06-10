# v463A GMUT Deep Remaster v5 Scalar-Only Route Decision

Generated: 2026-05-29T14:12:43Z / 2026-05-30T02:12:43+12:00

Status: `scalar_only_route_selected_for_readiness_scaffold`

## Decision

v5 selects `scalar_only_derivation_readiness` and does not select full `AB -> mu-nu` projection-map construction.

Reason: scalar-only readiness has a bounded candidate action route and can demote `B_Psi` while preserving evidence hygiene. Full `AB -> mu-nu` projection remains underdefined and would risk canon promotion or tensor-equivalence overclaim.

Claim limit: readiness scaffold only. No `T_Psi_mu_nu` derivation completion, GMUT validation, or physical promotion is claimed.

## Scalar-Only Fixture

Candidate action context:

```text
S_Psi = integral d4x sqrt(-g) [
  -1/2 g^mu_nu partial_mu Psi partial_nu Psi
  - V(Psi)
  + L_int
]
```

v5 active simplification:

- `L_int = 0` for the first scalar-only readiness pass.
- `lambda_T = 0` for the first scalar-only readiness pass.
- `alpha_B = 0` by `B_Psi` demotion.
- Mandala/meta terms are out of physical derivation scope.

Status: `ready_to_attempt_derivation_under_declared_fixture_assumptions_only`.

## B_Psi Disposition

Decision: demote `B_Psi` to quarantined dependency.

Reason: `B_Psi_mu_nu` lacks tensor definition, action support, units, divergence behavior, observables, null recovery, and external constraints. Removing it entirely would discard a future research option; defining it now would overclaim.

Allowed use: roadmap context and blocker ledger. Not allowed: active derivation term or physical stress-energy term.

## Projection Map Disposition

Decision: scaffold only, not active route.

Allowed use: future comparison scaffold between v13 `AB` and v462A `mu-nu` surfaces.

Not allowed: canon promotion, tensor equivalence, or physical stress-energy derivation.

## Blockers

- Metric signature and action sign are not fixed for derivation completion.
- `V(Psi)` is not chosen or parameterized.
- `T_Psi_mu_nu` metric variation has not been carried out.
- Conservation or exchange current has not been selected.
- Scalar couplings are not mapped to external fifth-force/equivalence constraints.

## Classification

Evidence: v462A requires scalar source definitions, null recovery, conservation/exchange behavior, fifth-force/equivalence routing, projection discipline, and consciousness measurement boundaries.

Hypothesis: a scalar-only fixture with `L_int=0`, `lambda_T=0`, and `alpha_B=0` is the safest next derivation-attempt route.

Advisory: v6 should attempt scalar-only derivation under declared assumptions or produce an explicit hold if metric/sign/potential conventions remain unresolved.
