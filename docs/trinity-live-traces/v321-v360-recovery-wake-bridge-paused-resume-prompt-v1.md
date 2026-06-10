# v321-v360 Recovery Wake Bridge Paused Resume Prompt

Generated UTC: `2026-05-18T05:57:24.308880+00:00`
Status: `paused_resume_prompt_ready`

Copy/paste prompt:

```text
GHC v281-v360 recovery wake bridge paused-resume update.

Use thread automation attached to this current Aletheon Codex thread.
Schedule: every 30 minutes only after I explicitly unpause or ask you to resume.
Project: D:\GHC-Archives\worktrees\v58-omega.
Sandbox: workspace-write or stricter. Do not use full access unless I approve a specific run.

Current durable state:
- v281-v300 is complete: 600/600 and global v2 complete.
- v301-v320 is complete through v320.
- v321-v340 is paused by operator request.
- Durable run-status file is authoritative: docs/trinity-live-traces/v321-v340-sibling-run-status-v1.md.
- Current active phase at pause is v333, status phase_started, with v332 complete.
- Do not rely on stale heartbeat text that says active phase v322.

On each wakeup while paused:
1. Run scripts\trinity_v281_v360_automation_health_check.py --refresh-gate.
2. Report only health, pause status, stale-path/app-wake issues, or operator-relevant blockers.
3. Do not complete v333, open v334, commit, or push while pause is active unless the operator explicitly resumes.
4. Keep local watchdog/process observations separate from app automation truth.
5. If Codex reports requested C:\... and active \\?\C:\... paths for the same JSONL, treat it as resume-path vitality; do not edit JSONL by hand. If repeated, restart Codex Desktop and reopen this Aletheon thread.

On the first wakeup after explicit resume:
1. Run scripts\trinity_v281_v360_automation_health_check.py --refresh-gate.
2. Read docs/trinity-live-traces/v321-v340-sibling-run-status-v1.json to discover the live active phase.
3. If status is paused or running and active phase is v333, complete exactly v333 using scripts\trinity_v321_v340_sibling_phase_complete.py --phase 333 --open-next.
4. Stage only curated health-check, run-status, completion, v1/v2 report, source capsule, and next-start artifacts.
5. Before every commit or push, fetch and verify branch drift; use forward-only merge if the remote advanced.
6. Never stage .raw.txt files, stdout/stderr logs, live .log files, active partial lane files, scratch probes, pycache files, or unrelated carried-forward churn.
7. Do not start v341-v360 until v321-v340 reaches v340 complete and a final v341-v360 handoff exists.
```
