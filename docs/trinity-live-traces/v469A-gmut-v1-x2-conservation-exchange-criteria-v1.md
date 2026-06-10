# v469A GMUT v1 x2 Conservation/Exchange Criteria

Classification: `blocker`
Status: `decision_criteria_only`

## Decision Lanes

### Lane 1: Minimal Uncoupled Scalar

Use this lane only if:

- `S_m` is independent of `Psi`.
- Matter is minimally coupled to `g_mu_nu`.
- The scalar equation of motion has been derived.
- The stress-energy tensor has been derived.

Expected shape:

```text
nabla_mu T_m^{mu nu} = 0
nabla_mu T_Psi^{mu nu} = 0
nabla_mu T_total^{mu nu} = 0
```

This lane is not accepted yet.

### Lane 2: Explicit Exchange Current

Use this lane only if:

- matter depends on `Psi`, or
- a coupling function is declared, or
- a source term is declared.

Expected shape:

```text
nabla_mu T_m^{mu nu} = Q^nu
nabla_mu T_Psi^{mu nu} = -Q^nu
nabla_mu T_total^{mu nu} = 0
```

This lane is blocked because no coupling or source term is currently defined.

### Lane 3: Explicit Hold

Use this lane when convention, coupling, potential, or variation is incomplete.

This is the current safe lane.

## Rejection Conditions

The next phases must reject any conservation/exchange claim if it:

- chooses exchange without a coupling;
- chooses separate conservation while matter depends on `Psi`;
- treats fixture existence as physical proof;
- imports Journey/Solas language as physics evidence;
- treats THOS schema validation as conservation validation.

## Result

The conservation/exchange law gate remains open. The useful progress is that v469A v2 x1 now has accept/reject criteria instead of a vague conservation request.
