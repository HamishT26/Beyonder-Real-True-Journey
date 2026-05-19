# v333-v360 Recovery Wake Bridge Resume Prompt v2

Generated NZT: `2026-05-19T16:08:42+12:00`
Status: `copy_paste_ready`

Copy/paste prompt:

```text
GHC v333-v360 recovery wake bridge resume update.

Use thread automation attached to this current Aletheon Codex thread.
Schedule: every 30 minutes.
Project: D:\GHC-Archives\worktrees\v58-omega.
Sandbox: workspace-write or stricter. Do not use full access unless I approve a specific run.

Resume authority:
- Installing, unpausing, or running this prompt is operator approval to resume from the durable v333 pause.
- Do not use stale heartbeat text that says active phase v322.
- The durable run-status JSON is authoritative.

Current durable state to verify on every wake:
- v281-v300 is complete: 600/600 and global v2 complete.
- v301-v320 is complete through v320.
- v321-v340 is paused at v333 phase_started, with v332 complete.
- Authoritative status file: docs/trinity-live-traces/v321-v340-sibling-run-status-v1.json.

On every wakeup:
1. Run scripts\trinity_v281_v360_automation_health_check.py --refresh-gate.
2. Read docs\trinity-live-traces\v321-v340-sibling-run-status-v1.json before deciding anything.
3. If status is paused or running and active_phase is between 333 and 340, continue exactly that active phase only.
4. Before launching work for a phase, check whether a matching active child process already exists. If a matching child is running and producing fresh artifacts, report material progress only and do not launch a duplicate.
5. If no matching active child is running, complete exactly the active phase with scripts\trinity_v321_v340_sibling_phase_complete.py --phase ACTIVE_PHASE --open-next.
6. After completing a phase, verify valid completion, v1 report, v2 report, source capsule, run-status, health-check, and next-start artifacts.
7. Stage only curated v321-v340 health-check, run-status, start, completion, v1/v2 report, source capsule, source-script, and handoff artifacts.
8. Never stage .raw.txt files, stdout/stderr logs, live .log files, active partial lane files, scratch probes, pycache files, or unrelated carried-forward churn.
9. Before every commit or push, fetch and verify branch drift; use forward-only merge if the remote advanced. Never reset, rebase, or force-push this shared line.
10. If the laptop lid was partly closed, Codex cannot resume, or C:\... and \\?\C:\... point to the same session JSONL, treat it first as host wake/app resume-path vitality, not repo failure. Do not edit session JSONL by hand; if repeated, restart Codex Desktop and reopen this Aletheon thread.

Cadence policy:
- Keep the app heartbeat at 30 minutes by default because recent phase timings cluster near 30 minutes.
- Use a 10-minute diagnostic burst only if I explicitly ask for app-wake testing.
- Do not change to 1, 5, or 10 minute phase cadence unless the phase runner has duplicate-child protection active.
- Do not change to hourly or multi-hour cadence unless laptop availability matters more than phase throughput.

Team and identity boundary:
- Aletheon leads the thread and approves commits/pushes.
- Arby, Kimi, and Aster Vale are durable sibling lanes through artifacts and count as live CLI agents only when matching sessions/processes are visible.
- Supervisor, v2 Watcher, and Recovery Watchdog are automation/helper roles unless a live model session plus durable persistence proof exists.
- Keep long CLI sibling reports in worktree artifacts, not terminal scrollback.
- No provider spend, external paid writes, personal-account mutation, secret transmission, or admin/elevated terminal use without explicit scoped approval.

Codex 0.131.0 update check:
- Record local codex --version on wake.
- If below 0.131.0, report that an upgrade is recommended for codex doctor, richer TUI status, unified @ mentions, plugin sharing, remote-control improvements, Python SDK changes, and Windows sandbox hardening.
- Do not run codex --upgrade, npm install, or any installation/update command unattended unless I explicitly approve that update action.

Research and source-capsule priority for v333-v360:
- Integrate the new v43 journey file and my paused-resume proposal into source capsules and handoffs.
- Continue Thermo/Psyche Dynamics, GMUT, Trinity Hybrid OS, Freed ID, Cosmic Bill of Rights, and Trinity Hybrid OS - Beyonder AI work as candidate-framework research with explicit evidence boundaries.
- Compare GMUT and the Mandala Field Equation against primary/official sources where possible: general relativity, quantum field theory, Standard Model, string theory, loop quantum gravity, computational irreducibility, complexity theory, AI safety/governance, verifiable credentials, MCP security, and AI risk frameworks.
- Do not claim a final Theory of Everything, ASI platform, or governance paradigm is proven unless the artifact includes falsifiable evidence, source comparison, and unresolved-risk notes.

v341-v360 gate:
- Do not start v341-v360 until v321-v340 reaches v340 complete and a final v341-v360 handoff exists.
- The v341-v360 handoff must include gate evidence, watcher/process state, staged-artifact boundaries, Codex version/update posture, source-capsule summary, and remaining blockers.

Stop condition:
- After v360 is complete and a final v281-v360 closeout/handoff exists, ask whether to archive this automation or replace it with the next bridge.
```
