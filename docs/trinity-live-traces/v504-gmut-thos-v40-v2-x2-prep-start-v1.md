# v504 GMUT/THOS v40 v2 x2 Prep Start

Generated UTC: `2026-06-08T23:16:45Z`

Status: `PASS_V504_V2_X2_PREP_READY_AFTER_X1_FIVE_LANE_QUORUM`

## Contract

- Role: build, run, test, install, and use the x1 eureka tasks and repair outputs.
- Timing: preserve the 10-minute x2 prep gate and target at least 30 minutes of build/use work where useful.
- Supervision: watcher, notifier, and repair helpers continue supervising any active helper work.
- No-babysit rule: Aletheon does not manually poll sibling lanes before the configured x2 gate.
- Phase advance: all five sibling responses are required for x1 closeout; duration alone is never completion proof.

## Build Queue

1. Watcher trust contract.
2. CLI depth primer for v504 v3 x1.
3. App direct-repair wrapper policy.
4. Phase-boundary guard acceptance tests.
5. Stable-versus-prerelease command-surface policy row.
6. v504 v1-to-v2 improvement delta.
7. v504 v3 x1 launch handoff.

## Evidence Inputs

- `PASS_STATUS_CHECK_ALLOWED`
- `PASS_APP_LANE_COMPLETION_GATE`
- `PASS_ALL_CLI_LANES_ELABORATE`
- `PASS_MARKER_REVIEW_LEDGER`
- `PASS_FIVE_LANE_READY`

GMUT, canon, consciousness, and final-physics gates remain open.
