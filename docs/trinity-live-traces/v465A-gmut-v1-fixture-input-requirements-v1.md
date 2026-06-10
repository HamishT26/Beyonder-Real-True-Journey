# v465A GMUT v1 Fixture Input Requirements

Status: `requirements_recorded_not_satisfied`

This artifact lists the minimum inputs required before a null/baseline fixture can move from hold to attempt-ready. It does not execute the fixture.

## Not Ready

The fixture needs exact baseline equations or a reference state, a selected null switch target, disabled/held term lists, expected recovery behavior, `EOM_Psi`/`T_Psi_mu_nu` dependency status, and a pass/fail comparison rule.

Allowed result labels for a future attempt: `not_attempted`, `ready_to_attempt`, `blocked`, `fixture_design_only`, `observed_for_this_fixture_only`.

Forbidden without exact artifact: `recovered`, `passed`, `validated`, or `baseline_proven`.
