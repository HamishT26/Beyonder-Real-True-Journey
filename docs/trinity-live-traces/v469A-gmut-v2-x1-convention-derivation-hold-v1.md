# v469A GMUT v2 x1 Convention Derivation Hold

Classification: `hypothesis`

## Candidate Under Audit

This phase continues the v1 x2 mostly-plus candidate as a single audit lane:

```text
metric signature: (-,+,+,+)
```

The candidate action shapes are:

```text
S_g = integral d4x sqrt(-g) [c^4/(16*pi*G)] (R - 2*Lambda)
S_Psi = integral d4x sqrt(-g) [-1/2 g^{mu nu} nabla_mu Psi nabla_nu Psi - V(Psi)]
```

If every missing assumption closed, the formal route would target:

```text
Box Psi - dV/dPsi = 0
```

and:

```text
T_Psi_mu_nu =
  nabla_mu Psi nabla_nu Psi
  - g_mu_nu [1/2 nabla_alpha Psi nabla^alpha Psi + V(Psi)]
```

## Why The Route Is Held

The candidate is useful because it removes one axis of sign ambiguity. It is still not accepted.

The hold reasons are concrete:

- `x0` is not declared as `t` or `c t`.
- Temporal derivative dimensions and `c` factors are not checked.
- The SI dimension of `Psi` is open.
- `V(Psi)` has no potential rule.
- `dV/dPsi` has no derivative rule.
- The scalar EOM lacks a proof artifact with boundary terms.
- `T_Psi_mu_nu` lacks a metric-variation proof artifact.
- No null-switch fixture has run.
- No baseline-recovery fixture has run.
- No scalar-matter coupling exists for fifth-force comparison.

## Decision

Continue with the mostly-plus candidate as the single route for v469A v2 x2, but keep every GMUT gate open.
