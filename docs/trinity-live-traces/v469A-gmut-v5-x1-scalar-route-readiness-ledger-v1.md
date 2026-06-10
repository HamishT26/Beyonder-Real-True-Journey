# v469A GMUT v5 x1 Scalar Route Readiness Ledger

Classification: `open_gap`

This ledger keeps the scalar route useful without letting placeholders turn into derivations.

## Scalar Kinetic Split

For the selected `x0=ct` rehearsal branch:

```text
L_Psi =
  N sqrt(h) [
    1/(2 N^2) (partial_0 Psi - beta^i partial_i Psi)^2
    - 1/2 h^ij partial_i Psi partial_j Psi
    - V(Psi)
  ]
```

with:

```text
partial_0 Psi = (1/c) partial_t Psi
```

Status: `template_ready_not_eom`.

## V(Psi) Hold

`V(Psi)` remains symbolic.

Blocked promotions:

- No `dV/dPsi` row.
- No mass-term assumption.
- No self-interaction assumption.
- No vacuum-energy assumption.
- No consciousness or proxy semantics.

## T_Psi Readiness

`T_Psi_mu_nu` remains `template_ready_not_derived`.

Required before promotion:

- Metric variation under the selected branch.
- Action sign convention.
- Scalar field dimension card.
- Boundary policy.
- Source-authority binding.
- Coefficient normalization.

## B_Psi Quarantine

`B_Psi` remains quarantined. No scalar boundary term is promoted until a separate definition artifact names the boundary class and variation condition.

Candidate boundary classes are Dirichlet, Neumann/Robin, asymptotic falloff, periodic box, finite timelike wall, initial/final Cauchy slices, and null/corner segments.

Forbidden promotions: scalar EOM derived, `T_Psi` accepted, boundary terms vanish without conditions, `V(Psi)` specified, `B_Psi` defined, or conservation law closed.
