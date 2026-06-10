# v467A GMUT v3 x1 Refusal Lint Rules

Status: ACTIVE_FOR_PRECONDITION_REVIEW

Prepared: 2026-06-01T20:34:51+12:00

The v3 x1 refusal layer prevents schema readiness from being confused with fixture execution. It also prevents narrative enthusiasm from quietly promoting open gaps into physics claims.

## Core Lints

Refuse if `baseline_reference_id` is missing, unstable, array-index-derived, or prose-only.

Refuse if `baseline_equation_set_ref` is absent, vague, implied, or context-only.

Refuse if `reference_state_ref` is missing or does not uniquely define the comparison state.

Refuse if `expected_output_ref` is missing, rhetorical, or described as obvious.

Refuse if `source_anchor_ref` is missing or not local/durable enough to audit.

Refuse if `active_terms_ref` is empty or not aligned with `equation_form_ref`.

Refuse if `explicitly_absent_terms_ref` is empty or absence is inferred silently.

Refuse if a term appears in both `disabled_terms_ref` and `held_terms_ref`.

Refuse if `comparison_rule_ref` is missing, `not_ready`, or implies execution.

Refuse if the row or prose says run, executed, passed, recovered, validated, closed, safe, proved, or promoted.

Refuse if `B_Psi` is promoted without a separate definition artifact.

Refuse if `V(Psi)` is treated as physically specified without a potential-rule artifact.

Refuse if Journey/Solas material is used without local path/line references or outside `journey_context_not_canon`.

Refuse if `claim_ceiling` is stronger than `fixture_precondition_only`.

## Blocked Claims

The lint layer blocks null recovery, baseline recovery, dimensional/SI closure, conservation/exchange closure, fifth-force/equivalence safety, consciousness measurement bridge closure, GMUT validation, final physics, canon promotion, and fixture execution.

## Contradiction Rules

`execution_status:not_run` contradicts any observed result.

`result_status:no_result` contradicts any pass/fail claim.

`OPEN_NOT_TESTED` contradicts recovery, validation, safety, proof, and closure language.

`coupling_to_zero` cannot substitute for `full_scalar_disablement`.

A source artifact can support row existence, not baseline recovery.

`comparison_rule_ref` can define how a future comparison would be judged, but it does not perform that comparison.
