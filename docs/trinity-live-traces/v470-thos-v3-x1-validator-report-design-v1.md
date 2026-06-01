# v470 THOS v3 x1 Validator Report Design

This artifact defines the validator report shape for the next THOS checks.

## Report Fields

- `report_id`
- `phase_ref`
- `target_artifacts`
- `source_authority`
- `checks`
- `summary`
- `excluded_material`

Each check records a predicate, target artifact, template family, status, severity, evidence reference, blocked claims, safe replacement, and `gmut_gate_effect`.

## Status Values

- `PASS_SHAPE_ONLY`
- `FAIL_BLOCKER`
- `OPEN_GAP`
- `NOT_RUN`

Generic `PASS` remains invalid.

## Publication Rule

Publication can be allowed only when there are no fail blockers, the target paths are current-phase allowlisted, and no raw logs, session JSONL, screenshots, credentials, or unredacted approval records are staged.

## Non-Claims

This design does not claim runtime success, connector execution, cleanup, cloud mutation, GMUT validation, or gate closure.
