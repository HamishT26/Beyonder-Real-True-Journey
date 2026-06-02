# v476 THOS v3 x1 Handoff Contract

NZ start: `2026-06-03T10:06:36+12:00`
Generated UTC: `2026-06-02T22:06:36+00:00`

Status: `PASS_SHAPE_ONLY_V476_HANDOFF_CONTRACT_READY`

This artifact turns the v476 v2 required-row gate into a handoff contract for later THOS phases. It is metadata-only: no command, skill, connector, dashboard, or system-expansion candidate is installed or promoted here.

Contract rows:

- `command_candidate_contract`: `PASS_SHAPE_ONLY`, materialization `candidate_only_not_installed`
- `skill_candidate_contract`: `PASS_SHAPE_ONLY`, materialization `candidate_only_not_installed`
- `system_expansion_candidate_contract`: `PASS_SHAPE_ONLY`, materialization `candidate_only_not_installed`
- `script_inventory_contract`: `PASS_SHAPE_ONLY`, materialization `candidate_only_not_installed`
- `connector_plugin_boundary_contract`: `PASS_SHAPE_ONLY`, materialization `candidate_only_not_installed`
- `dashboard_sync_contract`: `PASS_SHAPE_ONLY`, materialization `candidate_only_not_installed`
- `receipt_freshness_contract`: `PASS_SHAPE_ONLY`, materialization `candidate_only_not_installed`
- `publication_guard_contract`: `PASS_SHAPE_ONLY`, materialization `evidence_contract_only`
- `negative_fixture_contract`: `PASS_SHAPE_ONLY`, materialization `evidence_contract_only`
- `source_hash_chain_contract`: `PASS_SHAPE_ONLY`, materialization `evidence_contract_only`
- `async_cli_lane_contract`: `PASS_SHAPE_ONLY`, materialization `async_advisory_lane_temp_transport_only`
- `gmut_open_boundary_contract`: `PASS_SHAPE_ONLY`, materialization `evidence_contract_only`

Arby/Aster lane policy:

- Arby: launcher `0`, sandbox `read-only`, target `60` minutes
- Aster Vale: launcher `0`, sandbox `read-only`, target `60` minutes

Watcher poll seconds: `120`
Watcher timeout seconds: `72000`
Execution mode: `live_launch`

Raw lane transport remains local temp-only and unpublished. The watcher may write a curated completion notice pair for metadata only.

All six GMUT gates remain open.
