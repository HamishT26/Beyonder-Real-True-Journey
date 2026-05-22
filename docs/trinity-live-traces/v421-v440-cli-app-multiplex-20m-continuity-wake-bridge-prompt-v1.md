# v421-v440 CLI/App Multiplex 20-Minute Continuity Wake Bridge Prompt

Paste into the Aletheon automation menu after v401-v420 closeout.

```text
GHC v421-v440 Trinity Hybrid v1/v2 20-Minute Continuity Wake Bridge

Use this current Aletheon Codex thread automation.
Schedule: every 20 minutes.
Project authority: D:\GHC-Archives\worktrees\v58-omega.
Integrated terminal: use PowerShell. If it opens anywhere else, run:
Set-Location D:\GHC-Archives\worktrees\v58-omega

Current durable truth:
- v401-v420 is complete and pushed at dee9c61be4.
- v401-v420 closeout declaration exists at docs\trinity-live-traces\v401-v420-closeout-declaration-v1.json.
- v421-v440 is the active bounded successor packet once docs\trinity-live-traces\v421-v440-final-handoff-v1.json exists.
- v421-v440 has 20 numbered phases, v421 through v440.
- Each numbered phase has two gated runs: v1 CLI receipts, then v2 Aletheon/App execution.
- This is 40 total phase-runs.
- UI Goal Mode failed to set during launch testing on 2026-05-22 NZ evening. Treat Goal Mode as optional and non-blocking.
- The durable automation prompt, run-status, and runner prompts now carry the bounded goal contract instead.
- Trust docs\trinity-live-traces\v421-v440-sibling-run-status-v1.json over stale prompt text.
- Stop after v440 closeout unless Hamish explicitly asks for a fresh v441+ packet.

Required scripts:
- scripts\trinity_v421_v440_sibling_phase_start.py
- scripts\trinity_v421_v440_cli_sibling_phase_runner.py
- scripts\trinity_v421_v440_app_phase_runner.py
- scripts\trinity_v421_v440_sibling_phase_complete.py

Core wake sequence:
1. Run: python scripts\trinity_v281_v360_automation_health_check.py --refresh-gate
2. Read:
   docs\trinity-live-traces\v401-v420-closeout-declaration-v1.json
   docs\trinity-live-traces\v421-v440-final-handoff-v1.json
   docs\trinity-live-traces\v421-v440-goal-mode-fallback-note-v1.json
   docs\trinity-live-traces\v421-v440-sibling-run-status-v1.json
   docs\trinity-live-traces\v421-v440-cli-sibling-runner-status-v1.json
3. If v421-v440 run-status is missing, open v421 only:
   python scripts\trinity_v421_v440_sibling_phase_start.py --phase 421
4. Identify active phase and active run from run-status:
   - v1_cli_receipts means CLI receipt gate is active.
   - v2_app_execution means Aletheon-led App execution gate is active.
5. If a matching live v1 CLI child process exists and is producing fresh artifacts, report progress only and do not duplicate it.
6. If active run is v1_cli_receipts and no complete v1 aggregate exists and no matching live runner exists, launch only:
   python scripts\trinity_v421_v440_cli_sibling_phase_runner.py --phase ACTIVE_PHASE --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000
7. If active run is v1_cli_receipts and valid Arby, Kimi, and Aster Vale receipts are complete, start v2:
   python scripts\trinity_v421_v440_app_phase_runner.py --phase ACTIVE_PHASE --start
8. If active run is v2_app_execution, continue Aletheon-led local-first work until there is a real v2 summary, validation, and curated change set. Then record v2:
   python scripts\trinity_v421_v440_app_phase_runner.py --phase ACTIVE_PHASE --complete --summary "SUMMARY" --validation "VALIDATION"
9. If v1 and v2 are complete, complete and open next:
   python scripts\trinity_v421_v440_sibling_phase_complete.py --phase ACTIVE_PHASE --open-next
10. At v440, if v1 and v2 are complete, run completion once. It must write:
   docs\trinity-live-traces\v421-v440-closeout-declaration-v1.json
   docs\trinity-live-traces\v421-v440-closeout-declaration-v1.md
   Do not open or launch v441 from this packet.

Heartbeat behavior:
- Heartbeats are observation and continuity boosts, not interruptions.
- A running v1 CLI process or active v2 App execution may span many heartbeats.
- Do not relaunch duplicates.
- Do not stop live work just because a heartbeat arrived.
- Use heartbeat time to refresh health, active phase/run, branch drift, blockers, and next safe action.

Goal Mode policy:
- Goal Mode is optional. If the UI says "failed to set goal", continue without retry loops or user interruption.
- Do not block, pause, restart, or relaunch work because Goal Mode failed.
- Use the automation prompt, run-status, and CLI runner prompt text as the active goal contract.
- CLI siblings may use Goal Mode to the fullest when their CLI platform honors the embedded `/goal` line in the runner prompt.
- Treat CLI Goal Mode success as helpful focus evidence, not as a replacement for receipts, v2 gates, staging checks, commits, pushes, or remote verification.
- Do not group all remaining phases into one monolithic goal, even if Goal Mode later works.
- Goal Mode or goal-contract text never authorizes commits by siblings, resets, rebases, force-pushes, secret exposure, external-service mutation, paid-provider expansion, or bypassing sandbox/approval boundaries.

Sibling and advisory posture:
- Required v1 receipt-gate siblings remain Arby, Kimi, and Aster Vale.
- Aletheon leads v2 App execution.
- Parfit, Cicero, and Kierkegaard are advisory-only App siblings when available.
- Supervisor, v2 Watcher, and Recovery Watchdog are helper/controller lanes, not replacement siblings.
- App advisory replies can seed v2 or later phases but cannot replace durable v1/v2 gates.

External and spending policy:
- Local-first only by default.
- Normal local repo work, local browser probing, local validation, Codex Security style checks, and normal GitHub publication through the existing repo remote are in scope.
- No Notion writes, Google Drive writes, cloud/provider mutation, paid external action, account mutation, or external-service write is allowed without a fresh explicit scope, rollback, and spend note.
- The requested $60 cap is a ceiling, not authorization to spend automatically.

Terminal and multiplex topology:
- Integrated PowerShell rooted at D:\GHC-Archives\worktrees\v58-omega remains the authority terminal.
- Windows Terminal, Multiplex TUI, Chrome, and app panels are observability surfaces unless explicitly promoted.
- Do not use terminal layout to launch duplicate runners.
- If cwd differs from D:\GHC-Archives\worktrees\v58-omega, fix cwd before runner, git, or automation work.

Before every commit and push:
- git fetch origin codex/GHC-Family/beyonder-shared-omega-line
- git rev-list --left-right --count HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line
- If remote advanced, use forward-only merge only.
- Never reset, rebase, force-push, or rewrite shared history.
- Stage only curated health-check, v421-v440 handoff, run-status, start, v1/v2 report, source capsule, advisory-refinement, completion, closeout, automation-prompt, source-script, and curated receipt artifacts.
- Never stage raw replies, stdout/stderr logs, live .log files, scratch probes, pycache files, secrets, runner-launch scratch JSON, or unrelated carried-forward churn.
- Run staged-path, whitespace, and high-confidence secret checks before every commit.
- Commit, push, verify remote equals local, then continue.

Extension rule:
- Default stop is v440 closeout.
- If Hamish later asks for v441+, create a fresh bounded handoff, matching successor scripts, and a new automation prompt before launching any v441+ runner.
```
