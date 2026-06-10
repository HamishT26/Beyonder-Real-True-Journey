# v469A GMUT v7 x2 Signature And Action Source Audit

Classification: `blocker`

## Question

Can the metric signature or action sign move from `EXPLICIT_HOLD` to a rehearsal-only candidate after the v7 x2 source refresh?

## Result

No. Both remain `EXPLICIT_HOLD`.

This is not a failure of the phase. It is the useful result of the audit: the external source refresh confirms that the project must choose and propagate a convention bundle explicitly. The sources do not supply a GMUT-specific convention by inheritance.

## Metric Signature

Prior status: `EXPLICIT_HOLD`

New status: `EXPLICIT_HOLD`

Reason: the current artifacts still do not define a single convention bundle that connects all of these:

- the temporal sign in the Lorentzian metric,
- whether the active rehearsal branch is `x0=ct` or `x0=t`,
- how c powers move between coordinates, derivatives, metric components, and coefficients,
- how the scalar kinetic term is written,
- how the stress-energy tensor is varied from the matter action,
- how the null and baseline fixtures interpret the metric.

The source refresh supports the need for this bundle. It does not complete it.

## Action Sign

Prior status: `EXPLICIT_HOLD`

New status: `EXPLICIT_HOLD`

Reason: action sign is coupled to curvature sign, metric signature, scalar kinetic sign, potential sign, boundary assumptions, and stress-energy definition. A scalar-field note can show one action route; a GR sign-convention note can show that conventions vary. Neither supplies a GMUT-specific lock.

## Promotion Criteria

A later phase may promote a convention to `rehearsal_candidate_not_validation` only after these minimum rows exist:

- selected metric signature,
- selected active coordinate branch,
- gravitational action sign,
- scalar kinetic and potential signs,
- boundary-term policy,
- stress-energy variation definition,
- c-relocation table,
- null and baseline fixture expectations.

## Forbidden Claim

This audit does not validate GMUT, close dimensional consistency, close null recovery, or demonstrate fifth-force/equivalence safety. It only narrows the next admissible convention work.
