# v467A GMUT v6 x1 Precondition Card Skeletons

Status: SKELETONS_ONLY_NOT_EXECUTED

Prepared: 2026-06-01T21:44:49+12:00

## Card Set

`baseline_card` requires card ID, claim class, baseline equation reference, source anchor, source authority class, affected expressions, assumptions, symbol table, active terms, `execution_status:not_run`, and `result_status:no_result`. It forbids observed result, recovered, validated, and gate closed fields.

`reference_card` requires reference state ID, state definition, variables, assumptions, coordinate context, valid scope, comparison scope, and `execution_status:not_run`. It forbids comparison-ready, known-recovered, and fixture-output language.

`expected_output_card` requires expected output ID, expected equation form, expected removed terms, expected retained terms, comparison rule, residual policy, and `result_status:no_result`. It forbids actual output, matches expected, and pass hygiene wording.

`source_to_claim_row` requires claim ID, claim text, claim class, source references, source authority class, and support/context-only flag. It forbids source-free support and advisory-as-evidence.

`term_manifest` requires active, absent, disabled, held, quarantined, and symbolic terms, plus `switch_target:full_scalar_disablement`. It forbids silence-as-absence and coupling-to-zero as a substitute.

`B_Psi_card` keeps `B_Psi` quarantined or demoted unless a separate definition artifact exists.

`V_Psi_card` keeps `V(Psi)` symbolic unless potential and derivative rules exist.

`gate_verdict_carry` keeps all six gates `OPEN_NOT_TESTED`.

## Boundary

These are skeletons only. They do not execute fixtures, compute residuals, recover baselines, validate GMUT, or close gates.
