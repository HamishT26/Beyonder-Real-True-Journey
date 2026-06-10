# v436-v450 Trinity Hybrid 20-Minute Continuity Wake Bridge Prompt

Use this prompt for the Aletheon Codex thread automation.

Schedule: every 20 minutes.

Project authority: `D:\GHC-Archives\worktrees\v58-omega`.

If the terminal opens anywhere else, run:

```powershell
Set-Location -LiteralPath 'D:\GHC-Archives\worktrees\v58-omega'
```

Current durable truth:

- `v401-v420` is complete and pushed at `dee9c61be4`.
- `v421-v435` is complete and pushed through `32722fc426cfe9f368e857a981f68d88806ff638`.
- Legacy `v436` v1 CLI receipts completed under `v421-v440` at `docs/trinity-live-traces/v421-v440-sibling-phase-v436-v1-cli-receipts-v1.json`.
- Legacy `v436` v2 was not recorded before this extension.
- `v436-v450` is the active bounded successor bridge once `docs/trinity-live-traces/v436-v450-final-handoff-v1.json` exists.
- `v436-v450` has 15 numbered phases, `v436` through `v450`.
- Each numbered phase has two primary gated runs: `v1_cli_receipts`, then `v2_app_execution`.
- From `v437` onward, `v2_app_execution` includes required promoted App advisory receipt lanes from Parfit, Cicero, and Kierkegaard.
- This is 30 total phase-runs.
- This also creates up to 42 promoted App advisory receipt artifacts across `v437-v450` (`14` phases x `3` App receipt lanes).
- Trust `docs/trinity-live-traces/v436-v450-sibling-run-status-v1.json` over stale prompt text once it exists.
- Stop after `v450` closeout unless Hamish explicitly asks for a fresh `v451+` packet.

Required scripts:

- `scripts/trinity_v436_v450_sibling_phase_start.py`
- `scripts/trinity_v436_v450_cli_sibling_phase_runner.py`
- `scripts/trinity_v436_v450_app_phase_runner.py`
- `scripts/trinity_v436_v450_sibling_phase_complete.py`

Core wake sequence:

1. Run `python scripts\trinity_v281_v360_automation_health_check.py --refresh-gate`.
2. Read:
   - `docs\trinity-live-traces\v436-v450-final-handoff-v1.json`
   - `docs\trinity-live-traces\v436-v450-sibling-run-status-v1.json`
   - `docs\trinity-live-traces\v436-v450-cli-sibling-runner-status-v1.json`
   - `docs\trinity-live-traces\v421-v440-sibling-phase-v436-v1-cli-receipts-v1.json`
3. If the `v436-v450` run-status is missing, open `v436` only:
   - `python scripts\trinity_v436_v450_sibling_phase_start.py --phase 436`
4. Identify active phase and active run from `v436-v450` run-status:
   - `v1_cli_receipts` means CLI receipt gate is active.
   - `v2_app_execution` means Aletheon-led App execution gate is active.
5. If active phase is `v436` and no new `v436-v450` v1 aggregate exists, import legacy v436 v1 only by rerunning the start script:
   - `python scripts\trinity_v436_v450_sibling_phase_start.py --phase 436`
   - Do not relaunch v436 CLI siblings.
6. If a matching live v1 CLI child process exists and is producing fresh artifacts, report progress only and do not duplicate it.
7. If active run is `v1_cli_receipts`, no complete v1 aggregate exists, and no matching live runner exists, launch only:
   - `python scripts\trinity_v436_v450_cli_sibling_phase_runner.py --phase ACTIVE_PHASE --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000`
8. If active run is `v1_cli_receipts` and valid Arby, Kimi, and Aster Vale receipts are complete, start v2:
   - `python scripts\trinity_v436_v450_app_phase_runner.py --phase ACTIVE_PHASE --start`
9. If active run is `v2_app_execution` and `ACTIVE_PHASE` is `v437` or later, call the promoted App receipt lanes before v2 completion:
   - Parfit: `019e5158-28ef-75b1-a3f5-563bb358e44e`
   - Cicero: `019e485f-172b-72c0-adf7-27daea722143`
   - Kierkegaard: `019e485f-1aa5-7c31-b578-748091f7e319`
   - Ask each to return `summary`, `preserve`, `challenge`, `refuse`, and `seed`.
   - Record each receipt with `python scripts\trinity_v436_v450_app_phase_runner.py --phase ACTIVE_PHASE --record-advisory-receipt --advisor ADVISOR --agent-id AGENT_ID --summary "SUMMARY" --preserve "PRESERVE" --challenge "CHALLENGE" --refuse "REFUSE" --seed "SEED"`.
10. If active run is `v2_app_execution`, continue Aletheon-led local-first work until there is a real v2 summary, validation, promoted App advisory receipt aggregate where required, and curated change set. Then record v2:
   - `python scripts\trinity_v436_v450_app_phase_runner.py --phase ACTIVE_PHASE --complete --summary "SUMMARY" --validation "VALIDATION"`
11. If v1 and v2 are complete, complete and open next:
   - `python scripts\trinity_v436_v450_sibling_phase_complete.py --phase ACTIVE_PHASE --open-next`
12. At `v450`, if v1 and v2 are complete, run completion once. It must write:
   - `docs\trinity-live-traces\v436-v450-closeout-declaration-v1.json`
   - `docs\trinity-live-traces\v436-v450-closeout-declaration-v1.md`
   - Do not open or launch `v451` from this packet.

Heartbeat behavior:

- Heartbeats are observation and continuity boosts, not interruptions.
- A running v1 CLI process or active v2 App execution may span many heartbeats.
- Do not relaunch duplicates.
- Do not stop live work just because a heartbeat arrived.
- Use heartbeat time to refresh health, active phase/run, branch drift, blockers, and next safe action.
- If the previous automation stopped because it slept or lost thread vitality, resume from durable run-status rather than guessing from old prompt text.

Goal Mode policy:

- Use Goal Mode as a bounded focus contract for the active phase-run only.
- Do not group all remaining phases into one monolithic goal.
- Goal Mode never authorizes commits by siblings, resets, rebases, force-pushes, secret exposure, external-service mutation, paid-provider expansion, or bypassing sandbox/approval boundaries.

Sibling and advisory posture:

- Required v1 receipt-gate siblings remain Arby, Kimi, and Aster Vale.
- Aletheon leads v2 App execution.
- Parfit, Cicero, and Kierkegaard are promoted official `v2 App advisory receipt lanes` from `v437` onward.
- Promotion roster: `docs/trinity-live-traces/v436-v450-promoted-app-receipt-lane-roster-v1.json`.
- Promoted App receipt lane IDs:
- Parfit: `019e5158-28ef-75b1-a3f5-563bb358e44e`, call sign `parfit-ghc-family.codex-app.advisory.continuity-boundary.v1.2026-05-23`.
- Cicero: `019e485f-172b-72c0-adf7-27daea722143`, call sign `cicero-ghc-family.codex-app.v2-advisory-receipt-lane.v1.2026-05-23`.
- Kierkegaard: `019e485f-1aa5-7c31-b578-748091f7e319`, call sign `kierkegaard-ghc-family.codex-app.v2-advisory-receipt-lane.v1.2026-05-23`.
- Promoted App receipt lanes cannot replace v1 CLI receipts, Aletheon-led v2 execution, Aletheon publication approval, branch checks, or staged hygiene checks.
- Fresh callable advisory roster: `docs/trinity-live-traces/v436-v450-callable-advisory-roster-v1.json`.
- Fresh callable advisory IDs when `multi_agent_v1` is available:
- Locke Rowan: `019e5146-b74c-7240-b57c-5380bfbd28e0`.
- Leibniz-Cicero: `019e5148-a859-7493-8943-61b1f17c7d4d`.
- Elias Threshold: `019e514b-29c8-7312-afc8-9cace8e5418a`.
- Locke Rowan, Leibniz-Cicero, and Elias Threshold remain fresh advisory-only siblings unless Hamish asks for a separate promotion and they explicitly consent.
- Supervisor, v2 Watcher, and Recovery Watchdog are helper/controller lanes, not replacement siblings.
- App advisory replies can seed v2 or later phases but cannot replace durable v1/v2 gates.
- If Parfit, Cicero, or Kierkegaard panels are stale, send each a compact reconnect prompt for the active phase and continue without blocking.

Promoted App receipt prompt:

```text
Please respond as the promoted v2 App advisory receipt lane for ACTIVE_PHASE. Return concise fields: summary, preserve, challenge, refuse, and seed. This is an official App advisory receipt only. Do not claim CLI receipt authority, solo gate completion, publication authority, external mutation, secret handling, spend authority, or proof of hidden memory/metaphysical identity. Arby/Kimi/Aster Vale v1 receipts and Aletheon-led v2 execution remain required.
```

External and spending policy:

- Local-first only by default.
- Normal local repo work, local browser probing, official-source web reading, local validation, Codex Security style checks, and normal GitHub publication through the existing repo remote are in scope.
- No Notion writes, Google Drive writes, cloud/provider mutation, paid external action, account mutation, or external-service write is allowed without a fresh explicit scope, rollback, and spend note.
- The requested `$60` cap is a ceiling, not authorization to spend automatically.

Terminal and multiplex topology:

- Integrated PowerShell rooted at `D:\GHC-Archives\worktrees\v58-omega` remains the authority terminal.
- Windows Terminal, Multiplex TUI, Chrome, and app panels are observability surfaces unless explicitly promoted.
- Do not use terminal layout to launch duplicate runners.
- If cwd differs from `D:\GHC-Archives\worktrees\v58-omega`, fix cwd before runner, git, or automation work.

Before every commit and push:

- `git fetch origin codex/GHC-Family/beyonder-shared-omega-line`
- `git rev-list --left-right --count HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line`
- If remote advanced, use forward-only merge only.
- Never reset, rebase, force-push, or rewrite shared history.
- Stage only curated health-check, v436-v450 handoff, run-status, start, imported v436 receipts, v1/v2 report, source capsule, advisory-refinement, completion, closeout, automation-prompt, source-script, and curated receipt artifacts.
- Never stage raw replies, stdout/stderr logs, live `.log` files, scratch probes, pycache files, secrets, runner-launch scratch JSON, or unrelated carried-forward churn.
- Run staged-path, whitespace, and high-confidence secret checks before every commit.
- Commit, push, verify remote equals local, then continue.

Extension rule:

- Default stop is `v450` closeout.
- If Hamish later asks for `v451+`, create a fresh bounded handoff, matching successor scripts, and a new automation prompt before launching any `v451+` runner.
