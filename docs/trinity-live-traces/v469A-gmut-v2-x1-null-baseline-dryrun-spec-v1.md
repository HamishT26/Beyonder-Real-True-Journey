# v469A GMUT v2 x1 Null/Baseline Dry-Run Spec

Classification: `open_gap`

## Null Switch

The null switch should eventually set:

- `Psi` to zero or a declared constant;
- `nabla_mu Psi` to zero;
- `V(Psi)` to a declared null value;
- scalar-matter coupling to absent;
- `B_Psi` to absent because it is quarantined.

Expected target:

```text
G_mu_nu + Lambda g_mu_nu = (8*pi*G/c^4) T_m_mu_nu
```

This is not executed in v2 x1.

## Baseline Ladder

Rungs:

1. GR vacuum or matter baseline.
2. Lambda-retained baseline.
3. Cosmology baseline only if FLRW assumptions are declared.

## Blocked Execution Reasons

- `V(Psi)` null value is undefined.
- `Psi` units are undefined.
- `T_Psi_mu_nu` is not derived.
- Conservation/exchange is held.
- Fixture code cannot substitute for missing physics assumptions.

## Result

Null recovery and baseline recovery remain open.
