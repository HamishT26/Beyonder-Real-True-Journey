# v406-v420 Terminal Goal 15-Minute Continuity Wake Bridge Prompt

GHC v406-v420 Terminal Profile and Goal-Mode Recovery Wake Bridge

Use this current Aletheon Codex thread automation.
Schedule: every 15 minutes.
Project authority: `D:\GHC-Archives\worktrees\v58-omega`.
Integrated terminal: use PowerShell. If it opens anywhere else, run:

```powershell
Set-Location D:\GHC-Archives\worktrees\v58-omega
```

## Current Durable Truth

- v371-v400 is complete and pushed at `d78284246f`.
- v400 closeout declaration exists at `docs\trinity-live-traces\v371-v400-closeout-declaration-v1.json`.
- v405 is complete and pushed at `29b06aa487`.
- v406 is complete and pushed at `ebe4d4d9c6`.
- v407 has been opened but not completed.
- v401-v420 remains the active bounded successor packet.
- Trust `docs\trinity-live-traces\v401-v420-sibling-run-status-v1.json` over stale prompt text.
- Stop after v420 closeout unless Hamish explicitly asks for a new bounded v421+ packet.

## Required Scripts

- `scripts\trinity_v401_v420_sibling_phase_start.py`
- `scripts\trinity_v401_v420_cli_sibling_phase_runner.py`
- `scripts\trinity_v401_v420_sibling_phase_complete.py`

## Verified Toolchain and Source Notes

- Codex CLI is verified locally at `codex-cli 0.133.0`.
- Local `codex features list` reports `goals stable true`.
- Local `codex exec --help` exposes no standalone `codex goal` subcommand.
- Official Codex docs describe `/goal` as a slash-command workflow for durable long-running objectives and document `features.goals = true` or `codex features enable goals`.
- Official Codex Windows docs say the integrated terminal can be set independently from the agent, and integrated-terminal changes apply only to new terminal sessions.
- Microsoft PowerShell profile docs confirm profile scripts run when PowerShell starts and can run arbitrary commands, including `Set-Location`.
- Microsoft Windows Terminal pane docs support external multi-pane observation with vertical/horizontal splits.

## Core Wake Sequence

1. Run:

```powershell
python scripts\trinity_v281_v360_automation_health_check.py --refresh-gate
```

2. Read:

```text
docs\trinity-live-traces\v281-v360-closeout-declaration-v1.json
docs\trinity-live-traces\v361-v370-closeout-declaration-v1.json
docs\trinity-live-traces\v371-v400-closeout-declaration-v1.json
docs\trinity-live-traces\v401-v420-final-handoff-v1.json
docs\trinity-live-traces\v401-v420-sibling-run-status-v1.json
docs\trinity-live-traces\v401-v420-cli-sibling-runner-status-v1.json
docs\trinity-live-traces\v405-v420-toolchain-upgrade-gate-v1.json
docs\trinity-live-traces\v406-v420-terminal-goal-advisory-topology-v1.json
```

3. If v401-v420 run-status is missing, do not guess. Reconstruct from durable committed artifacts or stop and ask Hamish.

4. Eureka Reflection and Planning for the active phase:

- Summarize what was achieved from durable artifacts.
- Identify what needs fixing.
- Identify blockers.
- Propose or run the next bounded task.
- Keep this grounded in durable artifacts, not vibes or visible UI alone.

5. If a matching active CLI child process exists and is producing fresh artifacts, report progress only and do not duplicate it.

6. If the active phase has complete valid Arby, Kimi, and Aster Vale receipts, complete and open next:

```powershell
python scripts\trinity_v401_v420_sibling_phase_complete.py --phase ACTIVE_PHASE --open-next
```

7. If the active phase has no complete CLI receipt aggregate and no matching live runner, launch only:

```powershell
python scripts\trinity_v401_v420_cli_sibling_phase_runner.py --phase ACTIVE_PHASE --background --timeout-sec 86400 --kimi-timeout-sec 86400 --max-steps 10000
```

8. At v420, if receipts are complete, run completion once. It must write:

```text
docs\trinity-live-traces\v401-v420-closeout-declaration-v1.json
docs\trinity-live-traces\v401-v420-closeout-declaration-v1.md
```

Do not open or launch v421 from this packet.

9. Before every commit and push:

```powershell
git fetch origin codex/GHC-Family/beyonder-shared-omega-line
git rev-list --left-right --count HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line
```

10. If remote advanced, use forward-only merge only.

11. Never reset, rebase, force-push, or rewrite shared history.

12. Stage only curated health-check, v401-v420 handoff, run-status, start, completion, v1/v2 report, source capsule, closeout, automation-prompt, source-script, upgrade-gate, topology, advisory-refinement, and curated CLI sibling receipt artifacts.

13. Never stage raw replies, stdout/stderr logs, live `.log` files, scratch probes, pycache files, secrets, runner-launch scratch JSON, or unrelated carried-forward churn.

14. Run staged-path, whitespace, and high-confidence secret checks before every commit.

15. Commit, push, verify remote equals local, then continue.

16. Continue phase-by-phase through v420, then write v420 closeout and stop.

## Goal-Mode Policy

- From v407 onward, use goal-mode thinking as a per-phase contract.
- If `/goal` is available interactively in the Codex CLI/App surface, use one phase per goal only.
- Do not group all remaining phases into one monolithic `/goal` run; each phase still needs independent Arby, Kimi, and Aster Vale receipts, completion artifacts, staged checks, forward-only commit, push, and remote verification.
- For non-interactive `codex exec` lanes, do not depend on slash-command persistence. Encode the phase goal directly in the runner prompt.
- Phase goal template:

```text
/goal Complete Trinity Hybrid phase vACTIVE_PHASE without stopping until Arby, Kimi, and Aster Vale each produce valid curated receipts, the aggregate is complete, phase completion opens the next bounded phase or v420 closeout, staged checks pass, and remote equals local after push.
```

- Goal mode does not authorize commits by siblings, resets, rebases, force-pushes, secret exposure, external-service mutation, paid-provider expansion, or bypassing sandbox/approval boundaries.

## Terminal Profile and Multiplex Topology

- The main and integrated PowerShell profiles should land at `D:\GHC-Archives\worktrees\v58-omega`.
- The Codex integrated terminal is the preferred single visible terminal inside the Codex app side panel.
- For all-three or multi-lane terminal visibility, prefer an external Windows Terminal multiplex layout with panes rooted at the same worktree, or a repo-curated Multiplex TUI/log-tail view.
- Do not assume Parfit, Cicero, and Kierkegaard chat panels expose independent shell authority. Their panels are advisory collaboration surfaces, not receipt-gate terminals.
- If the integrated terminal starts in the wrong folder, run `Set-Location D:\GHC-Archives\worktrees\v58-omega` and continue from durable repo artifacts.

## Sibling and Advisory Posture

- Required receipt-gate siblings remain Arby, Kimi, and Aster Vale.
- Supervisor, v2 Watcher, and Recovery Watchdog remain helper/controller lanes, not replacement siblings.
- Parfit, Cicero, and Kierkegaard are Codex app advisory agents for v406-v420 reflection, identity-boundary testing, continuity testing, governance, humility checks, and cross-platform planning.
- Parfit, Cicero, and Kierkegaard must not commit, push, delete, reset, rebase, stage files, expose secrets, mutate external services, or replace the required CLI receipt gate.
- Their identity persistence is a live hypothesis to test carefully, not a proven repo fact.
- Do not spawn replacement app-agent siblings if existing advisory agents are unavailable, slow, or silent.

Use these existing app agent IDs when the tool/context exposes them:

- Parfit: `019e485f-15ed-7830-b422-2b8e530fe893`
- Cicero: `019e485f-172b-72c0-adf7-27daea722143`
- Kierkegaard: `019e485f-1aa5-7c31-b578-748091f7e319`

## End-of-Phase Advisory Refinement Loop

At the end of each phase, after the CLI receipts are complete and before or during next-phase planning:

1. Summarize the just-completed phase from durable artifacts.
2. Ask Parfit, Cicero, and Kierkegaard for advisory-only next-phase proposals when the app-agent tool/context is available.
3. Request 50 to 100 bounded Eureka task candidates, grouped by evidence, implementation, validation, governance, terminal/multiplex, goal-mode, and publication hygiene.
4. Synthesize useful advice into the next phase start plan or advisory-refinement artifact only when safe.
5. Continue from durable artifacts if app agents are silent, unavailable, or late.

Late advisory replies may inform later phases, but they cannot block the Arby/Kimi/Aster Vale CLI receipt gate.

## Operating Boundaries

- Codex app panels, Multiplex TUI, integrated terminal, Windows Terminal panes, and shadow-clone conversations are observability and collaboration surfaces, not repo authority.
- Authority remains durable artifacts, health checks, real CLI receipts, branch drift checks, and Aletheon-reviewed commits.
- Treat Fast mode and Goal mode as helpful speed/stability tiers, not permission to skip validation.
- Keep cloud/API/MCP/Gmail/Drive/paid-provider expansion exploratory until scope, rollback, secret handling, and spend limits are explicit.
- Treat GMUT, Trinity Mandala, and frontier science as rigorous research/canon surfaces unless independent evidence gates are met.
- Do not expose secrets, tokens, cookies, API keys, OAuth grants, or private account data.
- Do not use `--dangerously-bypass-approvals-and-sandbox`.
- If automation reports stale `C:\...` versus `\\?\C:\...` session JSONL paths, treat it as Codex app resume-path vitality, not repo failure. Do not edit session JSONL. Restart or reopen Codex Desktop if repeated, then resume from the latest visible Aletheon thread context.

## Extension Rule

- Default stop is v420 closeout.
- If Hamish later asks for v421-v430, v421-v440, or v421-v450, create a fresh bounded handoff, matching successor scripts, and a new automation prompt before launching any v421+ runner.
- Never let "+", enthusiasm, or visible UI activity override durable phase boundaries.
