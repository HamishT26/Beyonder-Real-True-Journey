# v469A GMUT v2 x2 Scalar Variation Rehearsal

Classification: `hypothesis`
Status: `formal_rehearsal_not_acceptance`

## Starting Point

```text
S_Psi = integral d4x sqrt(-g)
  [-1/2 g^{mu nu} nabla_mu Psi nabla_nu Psi - V(Psi)]
```

## Rehearsal

Vary `Psi` while holding the metric fixed.

The kinetic term contributes a term proportional to:

```text
-g^{mu nu} nabla_mu Psi nabla_nu delta Psi
```

The potential contributes:

```text
-dV/dPsi delta Psi
```

but only if `V(Psi)` has a derivative rule.

After integration by parts, with boundary behavior declared, the candidate interior term has shape:

```text
Box Psi - dV/dPsi
```

## Decision

The shape is rehearsed, not accepted. The blocked slots are boundary behavior, `dV/dPsi`, `Psi` dimensions, and `x0`/`c` convention.
