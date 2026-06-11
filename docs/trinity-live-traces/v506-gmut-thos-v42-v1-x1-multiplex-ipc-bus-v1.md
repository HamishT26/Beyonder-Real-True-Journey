# v506-gmut-thos-v42-v1-x1 GHC Multiplex IPC Bus Manifest

- generated_utc: `2026-06-11T07:33:15Z`
- overall_status: `PASS_GHC_MULTIPLEX_IPC_BUS_SCAFFOLD`
- daemon_started: `false`
- publication: `status_only`

## Preferred Routes
- cli: `node_codex_entrypoint_first_then_windows_fallback`
- app: `background_watch_then_gate_only_harvest_then_direct_repair`
- phase: `five_minute_blocker_checks_with_all_five_lane_closeout`
- continuity: `vision_card_at_phase_start_and_compact_refresh`

## Message Types
- `phase_start`
- `compact_refresh`
- `app_lane_event`
- `cli_lane_event`
- `watcher_status`
- `repair_status`
- `gate_status`
- `approval_packet`
- `branch_plan`
- `source_ledger`
- `vision_card`

## Cadence Policy
- blocker_check_minutes: `5`
- x1_carryover_minutes: `15`
- x2_prep_minimum_minutes: `10`
- duration_is_completion_proof: `false`
- phase_advance_requires_all_five_lanes_or_blocker_receipts: `true`

## Boundary

This manifest defines a status-only coordination contract. It does not start a daemon, read raw sibling output, publish raw logs, mutate accounts, create new threads, spawn old-style subagents, or claim GMUT/canon closure.
