# V43 Automation Registry

- Generated UTC: `2026-04-18T13:48:15+00:00`
- Overall status: `PASS`
- Automation registry state: `scheduler_fallback_verified_with_lane_residuals`
- Automation backend state: `windows_task_scheduler_authoritative`
- Native automation state: `tool_unavailable_in_session`

## Existing V42 Tasks

- `Codex V42 V42 API Health 0330`: state=`3`
- `Codex V42 V42 API Health 1530`: state=`3`
- `Codex V42 V42 GMUT Lab 0345`: state=`3`
- `Codex V42 V42 GMUT Lab 1545`: state=`3`
- `Codex V42 V42 Vesper Sync 0400`: state=`3`
- `Codex V42 V42 Vesper Sync 1600`: state=`3`

## Admitted V43 Automations

- `V43 WSL Health`: tier=`core`, entrypoint=`scripts/trinity_v43_scheduled_cycle.ps1 -Lane wsl_health`, proof=`docs/trinity-live-traces/v43-wsl-resurrection-v1.json`
- `V43 API Health`: tier=`core`, entrypoint=`scripts/trinity_v43_scheduled_cycle.ps1 -Lane api_health`, proof=`docs/trinity-live-traces/v43-cloud-carry-forward-v1.json`
- `V43 GMUT Lab`: tier=`core`, entrypoint=`scripts/trinity_v43_scheduled_cycle.ps1 -Lane gmut_lab`, proof=`docs/trinity-live-traces/v43-gmut-lab-bundle-v1.json`
- `V43 Vesper Sync`: tier=`core`, entrypoint=`scripts/trinity_v43_scheduled_cycle.ps1 -Lane vesper_sync`, proof=`docs/trinity-live-traces/v43-vesper-memory-cognitive-bridge-v1.json`

## Deferred Candidates

- `run_all_trinity_systems`: `Too broad for unattended twice-daily recurrence and not restricted to a bounded proof surface.`
- `trinity_background_os`: `Needs additional runtime guardrails before unattended scheduling.`
- `broad_trinity_wave`: `Candidate inventory remains too wide for safe recurring admission in V43.`

## Lane Residuals

- `wsl_health=WARN`
- `api_health=WARN`
- `vesper_sync=FAIL`
