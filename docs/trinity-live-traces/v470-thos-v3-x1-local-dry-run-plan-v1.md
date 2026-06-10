# v470 THOS v3 x1 Local Dry-Run Plan

Probe level: `P1_dry_run_guard_probe`

This is a plan for local dry-run validation, not execution of a full validator.

## Planned Checks

- Current-phase allowlist check.
- JSON parse check.
- Forbidden path check.
- Credential-pattern check.
- Trailing whitespace check.
- Generic `PASS` forbidden check.
- `gmut_gate_effect` invariant check.
- Mutation-claim check.

## Output Status Values

Allowed: `PASS_SHAPE_ONLY`, `FAIL_BLOCKER`, `OPEN_GAP`, `NOT_RUN`.

Blocked: `PASS`, `VALIDATED`, `EXECUTED`, `CLEANED`, `MUTATED`, `GMUT_VALIDATED`, `GATE_CLOSED`.

## Boundary

This plan does not perform cleanup, connector writes, cloud mutation, automation mutation, GMUT validation, or gate closure.
