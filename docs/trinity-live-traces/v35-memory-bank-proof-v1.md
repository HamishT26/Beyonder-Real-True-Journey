# V35 Memory Bank Proof

- Generated UTC: `2026-04-06T15:31:14+00:00`
- Overall status: `WARN`
- Proof state: `agent_engine_start_failed_after_upload`
- Memory bank state: `repo_memory_bank_validated_live_start_failed`
- Agent Engine state: `live_start_failed`
- Selected region: `unresolved`

## Completed Steps

- `mint_primary_token`
- `vertex_service_enabled`
- `repo_memory_bank_sync_ran`
- `repo_memory_bank_validator_ran`
- `live_agent_engine_create_attempted`

## Blockers

- The live Agent Engine create path staged successfully enough to attempt startup, but the reasoning engine failed to start and never stabilized into a visible Memory Bank session.
- Observed reasoning-engine references: projects/649817769181/locations/australia-southeast1/reasoningEngines/9165528929140736000, projects/649817769181/locations/australia-southeast1/reasoningEngines/9165528929140736000/operations/8439496662308618240
