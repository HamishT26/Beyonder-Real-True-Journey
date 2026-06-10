# v470 THOS v2 x2 Required Field And Enum Checks

This artifact converts the v2 x1 THOS templates into concrete required-field and enum checks.

## Required Families

- Command surface registry entries must declare command identity, pattern, intent, cwd scope, surface class, mutation level, approval policy, dirty-worktree policy, source authority, retention class, safe output claim, and blocked actions.
- Plugin, MCP, and skill boundary cards must declare capability, write/network/credential posture, consent, approval, human trigger, inputs, outputs, data classes, retention mode, blocked actions, audit events, and action status.
- Cleanup candidate manifests must remain inventory-only and include risk, retention, approval, rollback, and `action_status`.
- Connector write approval packets must include scoped consent, write scope, data touched, privacy impact, risk, rollback, approver, and decision.
- Advisory lane receipts must declare authority, boundary, mutations not performed, publication authority, GMUT validation not performed, and all six GMUT gates open.

## Enum Rules

- Allowed check statuses are `PASS_SHAPE_ONLY`, `FAIL_BLOCKER`, `OPEN_GAP`, and `NOT_RUN`.
- Forbidden statuses include generic `PASS`, `VALIDATED`, `EXECUTED`, `CLEANED`, `MUTATED`, `GMUT_VALIDATED`, and `GATE_CLOSED`.
- `gmut_gate_effect` must be `none_open_not_tested`.

## Blocking Rules

Missing source authority, missing retention class, missing consent artifact, missing rollback plan, raw logs marked publishable, screenshots/session JSONL staged as current-phase artifacts, or any THOS-to-GMUT validation wording are all `FAIL_BLOCKER`.
