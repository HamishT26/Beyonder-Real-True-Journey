# v470 THOS v5 x1 Supervisor Registry

This artifact defines a local, non-mutating THOS supervisor registry for `v470_THOS_v5_x1`.

The registry does not authorize connector writes, cleanup, external spend, sibling spawning, or GMUT gate closure. It records the request envelope and helper boundaries needed before later THOS phases can safely run command, skill, plugin, connector, or watcher actions.

## Request Envelope

Every proposed action should be normalized before routing:

- `request_id`
- `actor`
- `target_surface`
- `mutation_class`
- `operation`
- `scope`
- `bounded_scope`
- `approval_status`
- `spend_limit_usd`
- `validators`
- `provenance_ref`

## Helper Boundaries

- `aletheon_supervisor_gate`: local dry validator only; it classifies proposed actions and emits a decision report.
- `phase_watcher_template`: observe-only helper pattern; it can inspect or summarize but cannot stage, commit, push, upload, delete, or mutate connector state.
- `connector_mutation_gate`: dry validator only; it blocks connector writes unless named scope, spend boundary, and separate approval are present.

## Aggregation Rule

`FAIL_BLOCKER` dominates `OPEN_GAP`; `OPEN_GAP` dominates `NOT_RUN` and `PASS_SHAPE_ONLY`; `PASS_SHAPE_ONLY` means shape readiness only.

## Claim Ceiling

This registry supports THOS operating classification only. It does not validate GMUT, close physics gates, prove consciousness, or promote canon.
