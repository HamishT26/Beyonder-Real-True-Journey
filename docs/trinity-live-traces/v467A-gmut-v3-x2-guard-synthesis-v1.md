# v467A GMUT v3 x2 Guard Synthesis

Status: MACHINE_CHECKABLE_GUARD_PLAN_READY_NO_FIXTURE_EXECUTION

Prepared: 2026-06-01T20:43:29+12:00

v467A_GMUT_v3_x2 synthesizes the v3 x1 schema, refusal lints, sibling advisory synthesis, 120-task roadmap, 20-search source refresh, and P1 guard probe into a machine-checkable guard plan.

## Guard Layers

Closed shape: all required fields must be present, and forbidden fields must not appear.

Hard locks: `execution_status` must be `not_run`, `result_status` must be `no_result`, and `claim_ceiling` must be `fixture_precondition_only`.

Open gates: all six GMUT gates must remain `OPEN_NOT_TESTED` in this phase.

Source authority: each claim must map to an allowed source authority class.

Term inventory: active, explicitly absent, disabled, and held terms must be separated without conflict.

Comparison boundary: `comparison_rule_ref` can describe a future comparison, but it cannot imply execution.

Potential and auxiliary terms: `B_Psi` remains demoted, and `V(Psi)` remains symbolic until definition artifacts exist.

Journey boundary: Journey/Solas material requires local path/line references and remains `journey_context_not_canon`.

Prose endcap: final prose must not claim validation, recovery, safety, proof, closure, or promotion.

## Open Blockers

The exact baseline equation set is still missing.

The reference state is still missing.

The expected output is still missing.

The residual tolerance policy is still missing.

The switch-leakage policy is still missing.

The `B_Psi` definition artifact is still absent.

The `V(Psi)` potential-rule artifact is still absent.

No null or baseline fixture was executed.

## Gate Result

All six GMUT gates remain open. The v3 x2 contribution is stricter guard readiness, not physics closure.
