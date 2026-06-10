# v497 GMUT/THOS v33 v7 x1 Command Overlay Compatibility Register

- overall_status: `PASS_COMMAND_OVERLAY_REGISTER_READY`
- generated_utc: `2026-06-06T22:00:10Z`
- lane_status_harvested: `false`

## Command Groups

- Preflight: repo drift check, scoped status check, and version/readiness receipt.
- Launch: app watcher launch, CLI read-only advisory launch, and prompt policy generation.
- Cadence: x1 15-minute cadence guard and x2 10-minute prep guard.
- Completion: app completion gate, CLI completion notifier, and CLI quality gate.
- Publication: JSON parse, script compile, whitespace check, guard scan, exact stage, commit, push, and remote equality.

## Blocked Commands

Reset, rebase, force-push, broad staging, destructive cleanup, plugin-cache mutation, and user-skill mutation without exact approval remain blocked.
