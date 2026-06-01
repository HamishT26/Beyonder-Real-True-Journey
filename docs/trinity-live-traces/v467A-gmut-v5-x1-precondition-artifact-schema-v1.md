# v467A GMUT v5 x1 Precondition Artifact Schema

Status: PRECONDITION_SCHEMA_ONLY_NO_FIXTURE_EXECUTION

Prepared: 2026-06-01T21:28:49+12:00

## Global Locks

Every precondition artifact row requires `execution_status:not_run`, `result_status:no_result`, `claim_ceiling:fixture_precondition_only`, `source_authority_class`, `source_anchor_ref`, `next_missing_artifact`, `blocked_claims`, and `six_gate_status:all_open`.

Every precondition artifact row forbids fixture result, recovery result, validation status, canon promotion status, fifth-force safety status, consciousness proof status, spiritual proof status, final physics status, and gate closure.

## Artifact Families

`baseline_equation_card` requires baseline equation reference, equation source anchor, convention card, affected expressions, symbol scope, active terms, disabled terms, and held terms. It forbids observed result, recovered, validated, and unanchored equation text.

`reference_state_card` requires reference state ID, state definition, state variables, assumptions, boundary conditions, and comparison scope. It forbids empirical satisfaction, fixture output, and known-recovered language.

`expected_output_card` requires expected output ID, expected recovery behavior, expected shape, expected removed terms, expected retained terms, and comparison rule reference. It forbids actual output, match status, pass hygiene, and numeric result claims.

`term_manifest_packet` requires active, absent, disabled, held, quarantined, and symbolic term lists with source references. It forbids silence-as-absence, disabled-means-disproven, and held-means-solved language.

`comparison_boundary` requires comparison mode `not_run`, allowed future comparison type, comparison scope, exactness class, failure condition, and non-support claim IDs. It forbids current match, current fail, current pass, and recovery conclusion.

`residual_tolerance_policy` requires tolerance kind, symbolic-or-numeric mode, pre-execution-only flag, dependencies, zero-required terms, allowed residuals, and blocked residuals. It forbids within-tolerance, measured residual, and closure inference.

`switch_leakage_policy` requires full scalar disablement, leakage targets, coefficient aliases, hidden couplings, boundary leakage, source leakage, Journey/Solas leakage, and a coupling-to-zero optional diagnostic appendix. It forbids leakage-absent result, fifth-force-safe result, and coupling-to-zero as the primary switch.

`source_to_claim_row` requires claim ID, claim text, claim class, source references, source authority class, support/context-only flag, and blocked claims. It forbids source-free support, Journey/Solas canon support, and advisory-as-evidence.

`gate_verdict_carry` requires all six gate verdicts to remain `OPEN_NOT_TESTED`, with null closure artifact reference and reason `no_exact_closure_artifact`. It forbids closed, validated, satisfied, safe, or confirmed verdicts.

`B_Psi_quarantine_card` requires `B_Psi_status:quarantined_or_demoted`, definition artifact null-or-ref, promotion allowed false, and blocked claims. It forbids tensor/source promotion, definition by association, and implicit definition.

`V_Psi_symbolic_hold_card` requires symbolic placeholder status, potential rule null-or-ref, derivative rule null-or-ref, and blocked claims. It forbids specified potential without rule, derivative use without rule, and residual assumption.

## Interpretation

This schema can support v5_x2 blocker synthesis and future linting. It does not execute GMUT, compare equations, test null recovery, validate SI consistency, prove conservation, recover baselines, establish fifth-force/equivalence safety, or bridge consciousness measurements.
