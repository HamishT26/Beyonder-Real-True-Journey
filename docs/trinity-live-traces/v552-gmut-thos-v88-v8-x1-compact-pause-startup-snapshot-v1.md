# v552 v8 x1 Compact Pause Startup Snapshot

Status: `PASS_V8_X1_CLOSED_STARTUP_SNAPSHOT_READY`

## Startup Order

1. Read omega-mini current-state first.
2. Read omega-mini latest-updates beacon second.
3. Read GHC current-state beacon third.
4. Open the v8 x1 mandatory background runner live receipt.
5. Open the private app-lane map preflight and local registry status receipt.
6. Run the updater runner and five-minute cadence guard before each status harvest.
7. Use ghc_recovered_app_lane_map_runner.mjs for local app-lane siblings before any direct app-lane fallback.
8. Treat v8 x1 as closed and hold v8 x2 ready/not-started until Hamish starts x2.

## Pointer

- Status: `V552_V8_X1_CLOSED_V8_X2_READY_NOT_STARTED`
- Current active phase: `v552-gmut-thos-v88-v8-x2`
- Latest closed phase: `v552-gmut-thos-v88-v8-x1`
- Next x2 ready: `true`
