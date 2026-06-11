# v508-gmut-thos-v44-v1-x1 Runner Compatibility Ledger

Generated UTC: `2026-06-11T18:37:59Z`

Status: `RUNNER_COMPATIBILITY_LEDGER_READY`

Runner count: `24`

## Node Entrypoint Policy

- Default entrypoint: Node.
- Windows fallback: Only when a Node helper does not cover the required safe action.
- No deletion, cleanup, or process-control authority is granted by this ledger.

## Recommended v508 Sequence

- approval activation and carry gate
- read-only lane authorization intake
- x1 cadence work queue
- current source reflection ledger
- route-family status board
- no-replacement, exposure, and no-overclaim guards
- compact-refresh card

## Runners By Tier

### route_recovery_or_fallback

- ghc_app_lane_private_map_preflight.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_app_server_capability_probe.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_live_adapter_no_advance_gate.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_live_adapter_repair_checklist_builder.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_marker_source_validator.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_phase_boundary_orchestrator.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_route_family_validator.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_route_state_validator.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_strict_cli_lane_cycle.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_v506_readiness_node_entrypoint.mjs: Use only when current route recovery requires this narrower probe or validator.
- ghc_v507_round_robin_route_planner.mjs: Use only when current route recovery requires this narrower probe or validator.

### current_v508_essential

- ghc_approval_activation_carry_gate.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_approval_candidate_index.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_blocker_boundary_packet_builder.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_compact_refresh_card_builder.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_no_replacement_sibling_guard.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_phase_advance_guard.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_phase_prep_queue_builder.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_phase_start_readiness_gate.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_read_only_lane_authorization_intake.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_route_family_status_board.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_source_reflection_ledger_builder.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.
- ghc_x1_cadence_work_queue_builder.mjs: Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.

### unclassified_legacy_or_experimental

- ghc_runner_compatibility_ledger_builder.mjs: Do not use by default; review before invoking in a live phase.

## Usage Rules

- Use current_v508_essential runners before older route-recovery helpers.
- Use route_recovery_or_fallback runners only to refresh evidence or publish blocker receipts.
- Do not invoke unclassified runners in live phase work without a fresh receipt or approval packet.
- Do not let any runner publish raw lane text, private IDs, credentials, screenshots, local absolute paths, or raw app-server payloads.
- Do not use any runner output as phase completion proof unless a phase gate explicitly says it is sufficient.

## Boundary

This ledger classifies runners for v508-v515 preparation. It does not prove every helper is complete, does not start or close v508, does not delete or mutate old helpers, and does not publish raw or private material.
