# v466A GMUT v2 x1 Claim-ID Dictionary

Phase: `v466A_GMUT_v2_x1`

Status: `HOLD_PENDING_EXACT_ROW`

## ID Style

- Primary claim pattern: `clm.<family>.<subject>.<assertion>`.
- Primary statement pattern: `st.<domain>.<topic>.<predicate>`.
- Row pattern: `row.<domain>.<subject>.<index>`.

## Claim Families

- Convention claims are notation-only and cannot support derivation.
- Coefficient claims are dictionary/unit-slot rows only until values, units, uncertainty, regime, and source role are bound.
- Baseline/null claims are scaffold-only until fixture execution exists.
- External constraint claims are routing-only until observables, regimes, and bounds are mapped.
- Consciousness proxy claims are protocol-boundary rows only.
- Journey/Solas claims are `journey_context_not_canon` only.

## Unsupported Guard Claims

- `clm.guard.gmut_validated`
- `clm.guard.final_physics`
- `clm.guard.solved_consciousness`
- `clm.guard.empirical_spiritual_proof`
- `clm.guard.fifth_force_safe`
- `clm.guard.canon_promotion`

The dictionary is a schema scaffold. It does not validate GMUT or close any gate.
