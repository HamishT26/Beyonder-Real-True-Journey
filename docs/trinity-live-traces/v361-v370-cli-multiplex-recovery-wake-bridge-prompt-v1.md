# GHC v361-v370 CLI Multiplex Recovery Wake Bridge

Use thread automation attached to this current Aletheon Codex thread.
Schedule: every 30 minutes.
Project: `D:\GHC-Archives\worktrees\v58-omega`.
Sandbox: workspace-write or stricter. Do not use full access or Administrator terminals unless Hamish explicitly approves a specific run.

## Current State

- `v281-v360` is complete and pushed at `1b0d0c69df`.
- Current durable closeout is `docs\trinity-live-traces\v281-v360-closeout-declaration-v1.json`.
- `v361-v370` handoff is `docs\trinity-live-traces\v361-v370-final-handoff-v1.json`.
- Use only bounded `v361-v370` scripts for v361-v370.
- Stop after v370 closeout.

## Runtime Contract

- Use real CLI lanes for substantive phase work.
- Target up to 2000 useful steps per real CLI sibling lane per phase, and up to 2000 useful Aletheon synthesis/cleanup steps when needed.
- Use `--max-steps 2000` where the runner supports it.
- If a real CLI rejects 2000, retry once with the highest supported value discovered from CLI help/error output and record the downgrade in the phase receipt.
- Each lane may run for up to 24 hours when useful.
- Heartbeats are observation checkpoints, not interruption points.
- If a matching active CLI child process is alive and producing fresh artifacts, report progress only and do not duplicate it.
- If a lane is stale for two heartbeat windows without fresh artifacts, write a blocker/progress artifact and let Aletheon decide whether to resume, relaunch, or stop.
- Do not use `--dangerously-bypass-approvals-and-sandbox`.

## Phase Progression

1. Run `scripts\trinity_v281_v360_automation_health_check.py --refresh-gate`.
2. Read `docs\trinity-live-traces\v281-v360-closeout-declaration-v1.json`.
3. Read `docs\trinity-live-traces\v361-v370-final-handoff-v1.json`.
4. Read `docs\trinity-live-traces\v361-v370-sibling-run-status-v1.json` before deciding anything.
5. Trust durable run-status over stale prompt text.
6. Continue exactly the active phase.
7. If no matching CLI receipt process is running and the active phase has no complete CLI receipt aggregate, launch or resume the bounded successor runner with `scripts\trinity_v361_v370_cli_sibling_phase_runner.py --phase ACTIVE_PHASE --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 2000`.
8. Complete a phase only after valid real CLI receipts exist for Arby, Kimi, and Aster Vale, or after an explicit blocker decision is recorded.
9. After CLI receipts, Aletheon performs cleanup, synthesis, validation, curated staging, commit, push, and next-phase opening.
10. Stop after v370 closeout.

## Publication Rules

- Before every commit or push, fetch and verify branch drift.
- Use forward-only merge only if the remote advanced.
- Never reset, rebase, force-push, or rewrite shared branch history.
- Stage only curated health-check, run-status, start, completion, v1/v2 report, source capsule, source-script, handoff, closeout, automation-prompt, and curated CLI sibling receipt artifacts.
- Never stage raw replies, stdout/stderr logs, live `.log` files, scratch probes, pycache files, secrets, or unrelated carried-forward churn.
- Sibling lanes must not commit or push. Aletheon remains the commit/push approver.

## Operating Posture

- Keep the Multiplex TUI as observability, not authority.
- Authority remains in durable artifacts, health checks, lane receipts, and Aletheon-reviewed commits.
- Keep cloud/API/MCP expansion exploratory until scope, rollback, and spend limits are explicit.
- Keep work grounded in committed artifacts, durable run-status, and branch drift truth.
