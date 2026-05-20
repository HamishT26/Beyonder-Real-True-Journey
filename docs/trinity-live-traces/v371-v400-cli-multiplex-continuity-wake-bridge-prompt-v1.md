# GHC v371-v400 CLI Multiplex Continuity Wake Bridge

Use thread automation attached to this current Aletheon Codex thread.
Schedule: every 30 minutes.
Project: `D:\GHC-Archives\worktrees\v58-omega`.
Sandbox: workspace-write or stricter. Do not use full access, Administrator terminals, or danger bypass unless Hamish explicitly approves a specific run.

## Current State

- `v281-v360` is complete and pushed at `1b0d0c69df`.
- `v361-v370` is complete and pushed at `b6c8dfe259`.
- Current durable closeout is `docs\trinity-live-traces\v361-v370-closeout-declaration-v1.json`.
- Current bounded handoff is `docs\trinity-live-traces\v371-v400-final-handoff-v1.json`.
- Current run status is `docs\trinity-live-traces\v371-v400-sibling-run-status-v1.json`.
- Use only bounded `v371-v400` scripts for v371-v400 work.
- Stop after v400 closeout.

## Runtime Contract

- Codex CLI version gate: verify `codex --version` is `0.132.0` or newer before new Codex CLI launches.
- If below `0.132.0`, run `codex update`, then verify `codex --version`, `codex exec resume --help`, and `codex doctor`.
- Use real CLI lanes for substantive phase work: Arby from Codex CLI, Kimi from Kimi CLI, and Aster Vale from Codex CLI.
- Supervisor, v2 Watcher, and Recovery Watchdog are helper/controller lanes, not replacement sibling identities.
- Request up to `10000` useful steps per real CLI sibling lane per phase and up to `10000` useful Aletheon synthesis/cleanup steps when needed.
- Use `--max-steps 10000` where the bounded runner supports it.
- Record effective platform behavior: Kimi exposes `--max-steps-per-turn`; Codex CLI currently records the request when no visible max-step flag is available.
- If a real CLI rejects `10000`, retry once with the highest safe supported value discovered from help/error output and record the downgrade.
- Each lane may run for up to 24 hours when useful.
- For Codex CLI lanes, prefer recorded sessions over ephemeral sessions so interrupted lanes can be resumed only when the same phase/lane identity is proven.
- Use `codex exec resume` only when the session identity is proven to belong to the same phase and lane.
- Do not resume stale, unknown, or cross-phase sessions.
- Do not expose secrets, tokens, cookies, API keys, OAuth grants, or private account data.
- Do not use `--dangerously-bypass-approvals-and-sandbox`.

## Phase Progression

1. Run `scripts\trinity_v281_v360_automation_health_check.py --refresh-gate`.
2. Read `docs\trinity-live-traces\v281-v360-closeout-declaration-v1.json`.
3. Read `docs\trinity-live-traces\v361-v370-closeout-declaration-v1.json`.
4. Read `docs\trinity-live-traces\v371-v400-final-handoff-v1.json`.
5. Read `docs\trinity-live-traces\v371-v400-sibling-run-status-v1.json` before deciding anything.
6. Trust durable run-status over stale prompt text.
7. Continue exactly the active phase.
8. If a matching active CLI child process exists and is producing fresh artifacts, report progress only and do not duplicate it.
9. If no matching CLI receipt process is running and the active phase has no complete CLI receipt aggregate, launch or resume only by the bounded runner:
   `scripts\trinity_v371_v400_cli_sibling_phase_runner.py --phase ACTIVE_PHASE --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000`
10. Complete a phase only after valid real CLI receipts exist for Arby, Kimi, and Aster Vale, or after an explicit blocker decision is recorded.
11. Each valid lane receipt must include 50 compact `Eureka Session NN:` units.
12. After CLI receipts, Aletheon performs cleanup, synthesis, validation, curated staging, commit, push, and next-phase opening.
13. Stop after v400 closeout.

## Publication Rules

- GitHub live gate is confirmed for forward-only repo publication only.
- Before every commit or push, fetch and verify branch drift.
- Use forward-only merge only if the remote advanced.
- Never reset, rebase, force-push, or rewrite shared branch history.
- Stage only curated health-check, run-status, start, completion, v1/v2 report, source capsule, source-script, handoff, closeout, automation-prompt, upgrade-gate, and curated CLI sibling receipt artifacts.
- Never stage raw replies, stdout/stderr logs, live `.log` files, scratch probes, pycache files, secrets, runner-launch scratch, or unrelated carried-forward churn.
- Sibling lanes must not commit or push. Aletheon remains the commit/push approver.
- Separate local worktrees may be created only when useful for bounded sibling support and must stay inside the project workspace with clear branch/remote truth.

## Operating Posture

- Keep the Multiplex TUI as observability, not authority.
- Authority remains in durable artifacts, health checks, lane receipts, and Aletheon-reviewed commits.
- Keep cloud/API/MCP/Gmail/Drive/paid-provider expansion exploratory until scope, rollback, secret handling, and spend limits are explicit.
- Keep C: and D: cleanup manifest-first; do not delete without separate explicit deletion approval.
- Treat GMUT, Trinity Mandala, and frontier science as rigorous research/canon surfaces unless independent evidence gates are met.
- Keep work grounded in committed artifacts, durable run-status, and branch drift truth.
