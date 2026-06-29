# ghc_phase_receipt_consistency_runner.mjs

Status: `PASS_PHASE_RECEIPTS_CONSISTENT`

Purpose: Compare current-state and beacons for phase truth consistency.

## Checks

- PASS: Current state matches latest-updates status
- PASS: Current state matches GHC beacon status
- PASS: Current state matches requested phase
- PASS: current_active_phase matches latest-updates beacon
- PASS: current_active_phase matches GHC beacon
- PASS: latest_closed_phase matches latest-updates beacon
- PASS: latest_closed_phase matches GHC beacon
- PASS: latest_completed_x1_phase matches latest-updates beacon
- PASS: latest_completed_x1_phase matches GHC beacon
- PASS: latest_completed_x2_phase matches latest-updates beacon
- PASS: latest_completed_x2_phase matches GHC beacon
- PASS: next_x2_scope matches latest-updates beacon
- PASS: next_x2_scope matches GHC beacon
- PASS: Latest closed phase is recorded

## Evidence

- `omega-mini-current-state-v1.json`
- `omega-mini-latest-updates-beacon-v1.json`
- `ghc-current-state-beacon-v1.json`

## Boundary

Status-only runner. No new agents, held sibling activation, account mutation, deployment, global hook installation, private route handles, private lane body content, transcript text, credentials, or private machine paths are published.
