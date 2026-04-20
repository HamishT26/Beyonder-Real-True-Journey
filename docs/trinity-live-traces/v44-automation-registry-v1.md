# V44 Automation Registry

- Generated UTC: `2026-04-20T04:13:26+00:00`
- Overall status: `PASS`
- Automation registry state: `scheduler_fallback_verified_with_lane_residuals`
- Automation backend state: `windows_task_scheduler_authoritative`
- Native automation state: `tool_unavailable_in_session`

## Existing Tasks

- `V42::Codex V42 V42 API Health 0330`: state=`3`
- `V42::Codex V42 V42 API Health 1530`: state=`3`
- `V42::Codex V42 V42 GMUT Lab 0345`: state=`3`
- `V42::Codex V42 V42 GMUT Lab 1545`: state=`3`
- `V42::Codex V42 V42 Vesper Sync 0400`: state=`3`
- `V42::Codex V42 V42 Vesper Sync 1600`: state=`3`
- `V43::Codex V43 V43 API Health 0330`: state=`3`
- `V43::Codex V43 V43 API Health 1530`: state=`3`
- `V43::Codex V43 V43 GMUT Lab 0345`: state=`3`
- `V43::Codex V43 V43 GMUT Lab 1545`: state=`3`
- `V43::Codex V43 V43 Vesper Sync 0400`: state=`3`
- `V43::Codex V43 V43 Vesper Sync 1600`: state=`3`
- `V43::Codex V43 V43 WSL Health 0315`: state=`3`
- `V43::Codex V43 V43 WSL Health 1515`: state=`3`

## Admitted V44 Automations

- `V44 PowerShell Health`: tier=`core`, entrypoint=`scripts/trinity_v44_scheduled_cycle.ps1 -Lane powershell_health`, proof=`docs/trinity-live-traces/v44-operator-surface-probe-v1.json`
- `V44 API Health`: tier=`core`, entrypoint=`scripts/trinity_v44_scheduled_cycle.ps1 -Lane api_health`, proof=`docs/trinity-live-traces/v44-cloud-sweep-v1.json`
- `V44 GMUT Lab`: tier=`core`, entrypoint=`scripts/trinity_v44_scheduled_cycle.ps1 -Lane gmut_lab`, proof=`docs/trinity-live-traces/v44-gmut-lab-bundle-v1.json`
- `V44 Vesper Sync`: tier=`core`, entrypoint=`scripts/trinity_v44_scheduled_cycle.ps1 -Lane vesper_sync`, proof=`docs/trinity-live-traces/v44-vesper-memory-cognitive-bridge-v1.json`

## Lane Residuals

- `api_health=WARN`
- `vesper_sync=WARN`
