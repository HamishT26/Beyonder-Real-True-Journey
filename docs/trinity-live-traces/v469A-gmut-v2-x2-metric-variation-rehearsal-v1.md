# v469A GMUT v2 x2 Metric Variation Rehearsal

Classification: `hypothesis`
Status: `formal_rehearsal_not_acceptance`

## Candidate Definition

```text
T_mu_nu = -2/sqrt(-g) delta S_matter_like / delta g^{mu nu}
```

## Rehearsal

Hold `Psi` fixed while varying `g^{mu nu}`.

Track:

```text
delta sqrt(-g) = -1/2 sqrt(-g) g_mu_nu delta g^{mu nu}
```

and the metric contraction in the scalar kinetic term.

The candidate shape is:

```text
T_Psi_mu_nu =
  nabla_mu Psi nabla_nu Psi
  - g_mu_nu [1/2 nabla_alpha Psi nabla^alpha Psi + V(Psi)]
```

## Decision

The metric variation shape is rehearsed but not accepted. A proof artifact still needs to declare the stress-energy sign convention, check local energy density, and close field/potential units.
