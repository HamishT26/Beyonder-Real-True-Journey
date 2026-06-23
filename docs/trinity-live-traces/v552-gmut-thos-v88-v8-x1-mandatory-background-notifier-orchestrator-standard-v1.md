# v552 v8 x1 Mandatory Background Notifier Orchestrator Standard

Status: `PASS_MANDATORY_BACKGROUND_NOTIFIER_ORCHESTRATOR_STANDARD_RECORDED`

## Mandatory Rules

1. Use ghc_main_orchestrator_runner.mjs as the promoted main orchestration runner for this route family.
2. Use ghc_recovered_app_lane_map_runner.mjs by default for local app-lane siblings that are not main-thread agents.
3. When invoking ghc_recovered_app_lane_map_runner.mjs, pass explicit paired values for boolean flags so fallback and background-watch flags are both preserved.
4. Use recovered notifier/background/orchestrator runners first for existing inducted app-lane siblings.
5. Do not downgrade to stale direct/manual foreground modes when the background route is available.
6. Use updater runners at startup, resume, and compact-pause boundaries before harvesting lane truth.
7. Run five-minute status cadence checks while siblings continue in the background, continuously do safe-now approval packet, eureka, cleanup, validation, and orchestration work between marks, and harvest at the next natural safe pause after a mark.
8. Use safe runner orchestrator during background waiting instead of babysitting.
9. Use the full-tools support worktree for private-map preflights, app-lane notifier runners, completion gates, strict CLI cycles, and richer helper tooling.
10. Keep private lane IDs in a local ignored registry or shell environment only; publish sanitized presence/open-gap receipts to omega-mini.
11. Watcher start is not completion proof; harvest notifier and completion-gate receipts.
12. If private app-lane map material is missing, publish a recoverable open-gap receipt and keep the phase active.
13. Do not spawn new agents or activate held main-thread siblings without Hamish explicitly asking.

Applies to: `Cicero, Kierkegaard, Aristotle, Arby, Aster Vale`
