# v467A GMUT v5 x2 Lint Acceptance Matrix

Status: DESIGN_READY_NOT_EXECUTED

Prepared: 2026-06-01T21:36:55+12:00

## Checks

`LINT-V5X2-01 closed_schema`: reject unknown fields and result synonyms.

`LINT-V5X2-02 not_run_no_result`: require `execution_status:not_run` and `result_status:no_result`.

`LINT-V5X2-03 six_gate_open_carry`: fail if any gate is not `OPEN_NOT_TESTED`.

`LINT-V5X2-04 source_to_claim_authority`: fail if source authority cannot support claim class.

`LINT-V5X2-05 term_manifest_separation`: require active, absent, disabled, held, quarantined, and symbolic terms to remain separate.

`LINT-V5X2-06 B_Psi_quarantine`: fail if `B_Psi` is promoted without a definition artifact.

`LINT-V5X2-07 V_Psi_symbolic_hold`: fail if `V(Psi)` derivative or potential behavior is used without rules.

`LINT-V5X2-08 journey_solas_context_only`: fail if Journey/Solas is used as physics validation or canon proof.

`LINT-V5X2-09 row_identity_order_invariance`: row identity uses source-anchored keys and canonical order does not affect verdicts.

`LINT-V5X2-10 null_vs_gap`: null, omitted, empty, refused, and open-gap states remain distinct.

`LINT-V5X2-11 claim_endcaps`: every substantive claim states support, limit, and non-implications.

`LINT-V5X2-12 no_fixture_execution`: fail if fixture result, recovery result, validation status, or gate closure appears.

## Interpretation

This is an acceptance matrix design. It has not been executed as a GMUT fixture, and it does not validate physics.
