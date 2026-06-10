# v467A GMUT v6 x1 Claim Envelope Plan

Status: CLAIM_ENVELOPE_DESIGN_READY_NOT_IMPLEMENTED

Prepared: 2026-06-01T21:44:49+12:00

## Envelope Fields

The claim envelope should include record ID, schema version, claim ID, claim text, classification, status, source routes, source authority class, provenance triple, witness bundle, normalized key, raw source text reference, derivation depth, comparison scope, comparability status, conflict state, refusal code, open gaps, confidence band, and non-implications.

## Gap Taxonomy

Use a finite gap taxonomy: missing literal, missing provenance, identity ambiguous, type unresolved, unit unresolved, comparison blocked, conflict unresolved, derivation unsupported, and test not run.

## Refusal Vocabulary

Use a closed refusal vocabulary: unsupported authority, missing provenance, conflicting authority, comparison leakage risk, out of scope, insufficient evidence, and unsafe to promote.

## Rules

Normalize only for lookup and dedupe, never for display or meaning.

Separate record identity from semantic identity.

Keep literals immutable and keep derived claims in a separate lane.

Typed comparison requires declared type, parse status, unit/domain normalization, and comparability verdict.

Preserve conflicts losslessly.

Do not merge entities from name similarity alone.

Do not infer absence from silence.

Do not close gaps from derived output.

Refusal blocks promotion but does not erase the input.

## Boundary

This plan is not implemented and not executed. It is schema governance for v6_x2 synthesis.
