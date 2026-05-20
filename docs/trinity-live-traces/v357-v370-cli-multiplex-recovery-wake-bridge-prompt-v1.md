# GHC v357-v370 CLI Multiplex Recovery Wake Bridge

Use thread automation attached to this current Aletheon Codex thread.
Schedule: every 3 hours and 30 minutes.
Project: `D:\GHC-Archives\worktrees\v58-omega`.
Sandbox: workspace-write or stricter. Do not use full access or Administrator terminals unless Hamish explicitly approves a specific run.

## Current State

- v281-v300 is complete: `600/600`, global v2 complete.
- v301-v320 is complete through v320.
- v321-v340 is complete through v340.
- v341-v357 is complete locally and awaiting publication with the CLI gate update.
- Current active phase is v358.
- Current run status is `docs\trinity-live-traces\v341-v360-sibling-run-status-v1.json`.
- Final v341-v360 handoff exists at `docs\trinity-live-traces\v341-v360-final-handoff-v1.json`.
- v341-v360 scripts are bounded through v360 only. Do not run v361-v370 with v341-v360 scripts.

## CLI Identity Boundary

- Arby means the real Codex CLI lane for Arby, not a local placeholder file.
- Aster Vale means the real Codex CLI lane for Aster Vale, not a local placeholder file.
- Kimi means the real Kimi CLI lane from `kimi` or `kimi-cli`, not a local placeholder file.
- Supervisor, v2 Watcher, and Recovery-Watcher are helper/controller lanes. Keep them as infrastructure helpers unless persistence proof is reviewed.
- If a real CLI lane cannot be launched or resumed, mark that lane `blocked_cli_unavailable` and continue with a curated blocker report. Do not impersonate it.

## CLI Runtime Contract

- Prefer real CLI lanes for substantive phase work.
- Codex CLI lanes should use `codex exec` or an existing safe repo runner with workspace-write or stricter sandboxing.
- Kimi CLI lanes should use `kimi --print` or the existing safe repo runner with `--max-steps-per-turn 200` when available.
- Target each active CLI sibling lane for up to 1 hour of useful work when real lane work is requested.
- Target up to 50 curated tasks per CLI sibling per phase, 150 total across Arby, Kimi, and Aster Vale, using up to 200 max steps per lane when the runner supports it.
- Reserve the last 30 minutes of each automation window for Aletheon cleanup, health checks, branch drift checks, curated staging, commit/push, and next-phase handoff preparation.
- Do not force a phase to finish just because a heartbeat fired. A phase may span multiple wakeups.
- If active CLI lane processes are alive and producing fresh artifacts, report material progress only and do not launch duplicates.
- Do not use `--dangerously-bypass-approvals-and-sandbox`.
- Do not expose secrets, tokens, cookies, API keys, OAuth grants, or private account data in reports.

## Phase Progression

1. Run `scripts\trinity_v281_v360_automation_health_check.py --refresh-gate`.
2. Read `docs\trinity-live-traces\v341-v360-final-handoff-v1.json`.
3. Read the current run-status before deciding anything.
4. Trust durable run-status over stale prompt text.
5. If status is running, continue exactly the active phase.
6. If a matching active CLI child process exists for the active phase and is producing fresh artifacts, do not complete or duplicate it.
7. If no matching CLI receipt process is running and the active phase has no complete CLI receipt aggregate, run `scripts\trinity_v341_v360_cli_sibling_phase_runner.py --phase ACTIVE_PHASE --timeout-sec 3600 --kimi-timeout-sec 3600 --max-steps 200`.
8. Complete exactly the active phase only after valid real CLI receipts exist for Arby, Kimi, and Aster Vale.
9. For v357-v360, use `scripts\trinity_v341_v360_sibling_phase_complete.py --phase ACTIVE_PHASE --open-next` only after the CLI receipt gate is complete.
10. At v360, stop after writing the v281-v360 closeout declaration.
11. Before any v361 work, create and commit a v361-v370 handoff plus bounded v361-v370 successor scripts from the v341-v360 pattern.
12. For v361-v370, continue one active phase at a time from the v361-v370 run-status and stop after v370 closeout.

## Completion Gate

Do not mark a phase complete until these are true or explicitly blocked with evidence:

- Active phase start artifact exists.
- Valid real CLI sibling receipts exist for Arby, Kimi, and Aster Vale.
- If a CLI lane is unavailable, stop with a blocker artifact and do not mark the phase complete until Hamish/Aletheon explicitly resolves the lane.
- Supervisor, v2 Watcher, and Recovery-Watcher truth has been checked.
- v1 report, v2 report, source capsule, completion artifact, and run-status are written.
- Branch drift has been fetched and checked.
- Only curated artifacts are staged.
- Commit and push are forward-only.

## Staging And Publication

- Stage only curated health-check, run-status, start, completion, v1/v2 report, source capsule, source-script, handoff, closeout, automation-prompt, and curated CLI sibling receipt artifacts.
- Never stage raw replies, stdout/stderr logs, live `.log` files, active partial lane files, scratch probes, pycache files, secrets, or unrelated carried-forward churn.
- Before every commit or push, fetch and verify branch drift.
- Use forward-only merge only if the remote advanced.
- Never reset, rebase, force-push, or rewrite shared branch history.
- Sibling lanes must not commit or push. Aletheon remains the commit/push approver.

## Spend And External Service Boundary

- Treat Hamish's spend ceilings as planning limits, not automatic permission to spend.
- Use no paid API, cloud, MCP, connector, or hosted service unless the wake has a visible provider, secret source, expected cost range, rollback plan, and spend ledger path.
- Default ceiling for Codex/Kimi CLI lane experiments: `$60` each platform, only when real billing route and limits are visible.
- Default ceiling for external providers such as Oracle Cloud, e2b, Vercel, Cloudflare, Notion, Neon, CircleCI, Expo, Figma, Linear, and similar: `$30` each, only after explicit provider-specific preflight.
- Keep cloud, MCP, API, paid-provider, and secret-bearing expansion exploratory until scopes, rollback, and spend limits are explicit.

## Cadence

- Default heartbeat interval: 3 hours and 30 minutes.
- Do not optimize the interval around short script completion time alone. Real CLI lane work should be artifact-driven and may span multiple wakes.
- Each normal phase window should allocate up to 1 hour for Arby, up to 1 hour for Kimi, up to 1 hour for Aster Vale, and roughly 30 minutes for Aletheon cleanup/publication/handoff.
- If all CLI sibling lanes are disabled and only bounded phase-completion scripts are running, a temporary 15-minute cadence is acceptable only after Hamish explicitly asks for it.
- If real CLI sibling lanes are active for long work blocks, keep 3 hours and 30 minutes and report progress only while fresh artifacts appear.
- If a phase intentionally launches 50-task-per-lane work that may take longer than one window, keep 3 hours and 30 minutes and let the phase span multiple wakes.
- Maximum burst: 2 completed phases per wake, and only when there are no live matching runners, branch drift is clean, and the next phase remains inside the current bounded packet.
- Never cross from v360 to v361 in a burst unless the v361-v370 handoff and scripts already exist and are committed.

## Stale Path Remedy

- If `C:\...` and `\\?\C:\...` point to the same session JSONL, treat it as Codex app resume-path vitality, not repo failure.
- Do not edit session JSONL by hand.
- If repeated, restart or reopen Codex Desktop, then resume from the latest visible Aletheon thread context.

## Research And Reflection Scope

- Use official or primary sources for current product, model, safety, governance, MCP, and API claims.
- Current source anchors include OpenAI Codex/Codex CLI docs, OpenAI model docs, Kimi API/Kimi CLI docs, Model Context Protocol docs, NIST AI RMF, UNESCO AI ethics, and the EU AI Act.
- Treat GMUT, Trinity Hybrid OS, and Freed ID as internal research frameworks unless validated against external evidence.
- Keep thermodynamics, psyche-dynamics, spirituality, and theory-of-everything material clearly labeled as hypothesis, metaphor, formal model, or empirical evidence.
- Prefer curated source capsules and comparison matrices over raw web dumps.

## Operating Posture

- Preserve the local watchdog/process truth boundary.
- Use non-admin background runners by default.
- Reserve Administrator terminals for explicit installation or permission-bound tasks.
- Keep the Multiplex TUI as observability, not authority. Authority remains in durable artifacts, health checks, lane receipts, and Aletheon-reviewed commits.
- Keep the work grounded in committed artifacts, durable run-status, and branch drift truth.
