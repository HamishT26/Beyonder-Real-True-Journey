# v361-v370 Sibling Base Plan

Generated UTC: `2026-05-20T04:30:25.944562+00:00`
Status: `ready_after_v281_v360_closeout`
Handoff: `docs/trinity-live-traces/v361-v370-final-handoff-v1.json`

Phase leads:
- `v361`: Arby
- `v362`: Kimi
- `v363`: Aster Vale
- `v364`: Supervisor
- `v365`: v2 Watcher
- `v366`: Recovery Watchdog
- `v367`: Arby
- `v368`: Kimi
- `v369`: Aster Vale
- `v370`: Supervisor

Truth boundaries:
- v361-v370 starts only after v281-v360 closeout is complete and committed.
- The app heartbeat is an observation checkpoint; real CLI lane work may span many wakes.
- Use 2000 max steps where supported, with recorded downgrade if a CLI rejects it.
- Do not stage raw replies, stdout/stderr logs, live logs, scratch probes, pycache files, secrets, or unrelated churn.
- The successor runner is bounded to v361-v370 and must not open v371 automatically.
