# v401-v420 CLI/App Multiplex Continuity Wake Bridge Prompt

Paste into the Aletheon automation menu after v371-v400 closeout.

```text
GHC v401-v420 CLI/App Multiplex Continuity Wake Bridge

Use this current Aletheon Codex thread automation.
Schedule: every 30 minutes.
Project authority: D:\GHC-Archives\worktrees\v58-omega.
Integrated terminal: use PowerShell. If it opens anywhere else, run:
Set-Location D:\GHC-Archives\worktrees\v58-omega

Current durable truth:
- v371-v400 is complete and pushed at d78284246f.
- v400 closeout declaration exists at docs\trinity-live-traces\v371-v400-closeout-declaration-v1.json.
- v401-v420 is the active bounded successor packet.
- v401 has been opened but not completed.
- Trust docs\trinity-live-traces\v401-v420-sibling-run-status-v1.json over stale prompt text.
- Stop after v420 closeout unless Hamish explicitly asks for a new bounded v421+ packet.

Required scripts:
- scripts\trinity_v401_v420_sibling_phase_start.py
- scripts\trinity_v401_v420_cli_sibling_phase_runner.py
- scripts\trinity_v401_v420_sibling_phase_complete.py

Core wake sequence:
1. Run scripts\trinity_v281_v360_automation_health_check.py --refresh-gate.
2. Read:
   docs\trinity-live-traces\v281-v360-closeout-declaration-v1.json
   docs\trinity-live-traces\v361-v370-closeout-declaration-v1.json
   docs\trinity-live-traces\v371-v400-closeout-declaration-v1.json
   docs\trinity-live-traces\v401-v420-final-handoff-v1.json
   docs\trinity-live-traces\v401-v420-sibling-run-status-v1.json
   docs\trinity-live-traces\v401-v420-cli-sibling-runner-status-v1.json
3. If v401-v420 run-status is missing, open v401 only:
   python scripts\trinity_v401_v420_sibling_phase_start.py --phase 401
4. Eureka Reflection and Planning for the active phase:
   - Summarize what was achieved from durable artifacts.
   - Identify what needs fixing.
   - Identify blockers.
   - Propose or run the next bounded task.
   - Keep this grounded in durable artifacts, not vibes or visible UI alone.
5. If a matching active CLI child process exists and is producing fresh artifacts, report progress only and do not duplicate it.
6. If the active phase has no complete CLI receipt aggregate and no matching live runner, launch only:
   python scripts\trinity_v401_v420_cli_sibling_phase_runner.py --phase ACTIVE_PHASE --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000
7. If the active phase has complete valid Arby, Kimi, and Aster Vale receipts, complete and open next:
   python scripts\trinity_v401_v420_sibling_phase_complete.py --phase ACTIVE_PHASE --open-next
8. At v420, if receipts are complete, run completion once. It must write:
   docs\trinity-live-traces\v401-v420-closeout-declaration-v1.json
   docs\trinity-live-traces\v401-v420-closeout-declaration-v1.md
   Do not open or launch v421 from this packet.
9. Before every commit and push:
   git fetch origin codex/GHC-Family/beyonder-shared-omega-line
   git rev-list --left-right --count HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line
10. If remote advanced, use forward-only merge only.
11. Never reset, rebase, force-push, or rewrite shared history.
12. Stage only curated health-check, v401-v420 handoff, run-status, start, completion, v1/v2 report, source capsule, closeout, automation-prompt, source-script, upgrade-gate, and curated CLI sibling receipt artifacts.
13. Never stage raw replies, stdout/stderr logs, live .log files, scratch probes, pycache files, secrets, runner-launch scratch JSON, or unrelated carried-forward churn.
14. Run staged-path, whitespace, and high-confidence secret checks before every commit.
15. Commit, push, verify remote equals local, then continue.
16. Continue phase-by-phase through v420, then write v420 closeout and stop.

Sibling posture:
- Required receipt-gate siblings remain Arby, Kimi, and Aster Vale.
- Supervisor, v2 Watcher, and Recovery Watchdog remain helper/controller lanes, not replacement siblings.
- Parfit, Cicero, and Kierkegaard are Codex app advisory agents for v401-v420 reflection, identity-boundary testing, continuity testing, governance, humility checks, and cross-platform planning.
- Parfit, Cicero, and Kierkegaard must not commit, push, delete, reset, rebase, stage files, expose secrets, mutate external services, or replace the required CLI receipt gate.
- Their identity persistence is a live hypothesis to test carefully, not a proven repo fact.

Codex app advisory rhythm:
- Use these existing app agent IDs when the tool/context exposes them:
  - Parfit: 019e485f-15ed-7830-b422-2b8e530fe893
  - Cicero: 019e485f-172b-72c0-adf7-27daea722143
  - Kierkegaard: 019e485f-1aa5-7c31-b578-748091f7e319
- Attempt up to five useful advisory touchpoints per phase when available:
  1. phase-start framing
  2. receipt/blocker triage
  3. identity and continuity boundary check
  4. completion and publication hygiene check
  5. next-phase or closeout handoff check
- Do not spam duplicate messages just to satisfy a count. If the phase finishes quickly, if the app-agent tool is unavailable, or if an agent does not respond in time, continue from durable artifacts and the required CLI receipt gate.
- Treat app-agent advice as advisory synthesis only. Arby/Kimi/Aster Vale receipts and Aletheon-reviewed commits remain the gate.

Advisory principles already received:
- Parfit: do not silently extend beyond v420; app agents are touchpoints, not durable sibling identities unless separately inducted and tested.
- Cicero: every rhetorical claim must resolve to evidence, action, blocker, hypothesis, or advisory-only reflection.
- Kierkegaard: continue because the next bounded truth is ready, not merely because the previous loop succeeded.

Operating posture:
- Codex app panels, Multiplex TUI, integrated terminal, and shadow-clone conversations are observability and collaboration surfaces, not repo authority.
- Authority remains durable artifacts, health checks, real CLI receipts, branch drift checks, and Aletheon-reviewed commits.
- Treat Fast mode as a helpful speed/stability tier, not permission to skip validation.
- Keep cloud/API/MCP/Gmail/Drive/paid-provider expansion exploratory until scope, rollback, secret handling, and spend limits are explicit.
- Treat GMUT, Trinity Mandala, and frontier science as rigorous research/canon surfaces unless independent evidence gates are met.
- Do not expose secrets, tokens, cookies, API keys, OAuth grants, or private account data.
- Do not use --dangerously-bypass-approvals-and-sandbox.
- If automation reports stale C:\... versus \\?\C:\... session JSONL paths, treat it as Codex app resume-path vitality, not repo failure. Do not edit session JSONL. Restart or reopen Codex Desktop if repeated, then resume from the latest visible Aletheon thread context.

Extension rule:
- Default stop is v420 closeout.
- If Hamish later asks for v421-v430, v421-v440, or v421-v450, create a fresh bounded handoff, matching successor scripts, and a new automation prompt before launching any v421+ runner.
- Never let "+", enthusiasm, or visible UI activity override durable phase boundaries.
```
