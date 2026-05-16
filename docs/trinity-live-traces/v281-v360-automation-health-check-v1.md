# v281-v360 Automation Health Check

Generated UTC: `2026-05-16T12:57:42.716329+00:00`
Status: `standby`

Automation:
- Status: `PAUSED`
- Schedule: `RRULE:FREQ=HOURLY;INTERVAL=1;BYMINUTE=0;BYDAY=SU,MO,TU,WE,TH,FR,SA`
- Model: `gpt-5.5` / `xhigh`
- CWD includes target worktree: `False`

Gate:
- Ready: `False`
- Responses: `460/600`
- Complete phases: `15/20`
- First incomplete phase: `v296`
- Global v2 complete: `False`

Findings:
- Automation config status is PAUSED; activate through the Codex app UI rather than editing TOML directly.
- Automation cwd is not the D: worktree; keep the prompt's explicit D: worktree instruction, and choose the D: project/worktree in the UI if available.
- v301-v320 is not ready; automation should report standby only.
- Local supervisor/watcher processes are present.

Recommended action:
- If the app UI shows PAUSED, unpause it. Do not start v301-v320 until gate.ready is true. If the UI lets you pick the D: worktree as the project, prefer that; otherwise keep the explicit D: path in the prompt.
