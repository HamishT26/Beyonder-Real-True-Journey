# GHC v341-v360 Final Recovery Wake Bridge

Use thread automation attached to this current Aletheon Codex thread.
Schedule: every 30 minutes.
Project: `D:\GHC-Archives\worktrees\v58-omega`.
Sandbox: workspace-write or stricter. Do not use full access unless Hamish explicitly approves a specific run.

Current state:
- v281-v300 is complete: `600/600`, global v2 complete.
- v301-v320 is complete through v320.
- v321-v340 is complete through v340.
- Final handoff exists at `docs\trinity-live-traces\v341-v360-final-handoff-v1.json`.
- v341 has not started yet.

On each wakeup:
1. Run `scripts\trinity_v281_v360_automation_health_check.py --refresh-gate`.
2. Read `docs\trinity-live-traces\v341-v360-final-handoff-v1.json` before deciding anything.
3. If v341-v360 start or completion scripts do not yet exist, create a bounded successor from the v321-v340 script pattern before starting v341.
4. If v341-v360 status is running, complete only the active phase and open the next phase only when it is within v341-v360.
5. If no matching active child is running, complete exactly the active phase; do not launch duplicate phase runners.
6. Stop after v360 completes, write the v281-v360 closeout declaration, then ask Hamish whether to archive this automation or update it for the next packet.
7. Stage only curated health-check, run-status, start, completion, v1/v2 report, source capsule, source-script, handoff, closeout, and automation-prompt artifacts.
8. Never stage raw replies, stdout/stderr logs, live `.log` files, active partial lane files, scratch probes, pycache files, or unrelated carried-forward churn.
9. Before every commit or push, fetch and verify branch drift; use forward-only merge only if the remote advanced.
10. If `C:\...` and `\\?\C:\...` point to the same session JSONL, treat it as app resume-path vitality, not repo failure; do not edit session JSONL by hand.

Operating posture:
- Keep the app heartbeat at 30 minutes unless Hamish explicitly asks for a short diagnostic burst.
- Preserve the local watchdog/process truth boundary.
- Use non-admin background runners by default; reserve Administrator terminals for explicit installation or permission-bound tasks.
- Keep cloud, MCP, API, and paid-provider expansion exploratory until secrets, scopes, rollback, and spend limits are explicit.
- Keep one active phase per wake unless Hamish explicitly requests a different cadence.
