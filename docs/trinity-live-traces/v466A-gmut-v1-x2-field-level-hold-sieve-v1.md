# v466A GMUT v1 x2 Field-Level Hold Sieve

Phase: `v466A_GMUT_v1_x2`

Status: `FIELD_LEVEL_PROVENANCE_SCHEMA_OVERLAY_HOLD`

## Hold Triggers

- Hold when a support-bearing field lacks stable `source_id` or `statement_id`.
- Hold when `supports`, `does_not_support`, or `constrains` are free text rather than stable claim IDs.
- Hold when observation, derivation, assumption, and interpretation are mixed without `interpretation_type`.
- Hold when measured, bounded, or converted values lack uncertainty semantics.
- Hold when coefficient rows lack SI dimension vector, canonical unit, or conversion assumptions.
- Hold when external constraint rows lack regime, range, coupling basis, or composition basis.
- Hold when null results or exclusion bounds are promoted into positive existence, safety, or compatibility claims.
- Hold when Journey/Solas context is treated as physics evidence instead of `journey_context_not_canon`.
- Hold when any row implies GMUT validation, final physics, fifth-force safety, solved consciousness, empirical spiritual proof, or canon promotion.
- Hold when metric/action or scalar-variation rows lack boundary-term or integration-by-parts policy.

## Current Limit

The maximum current posture remains `HOLD_PENDING_EXACT_ROW`. `PASS_SCHEMA_ONLY` is not assigned in this x2 phase because no local row instances with stable claim IDs were materialized.

All six GMUT gates remain open.
