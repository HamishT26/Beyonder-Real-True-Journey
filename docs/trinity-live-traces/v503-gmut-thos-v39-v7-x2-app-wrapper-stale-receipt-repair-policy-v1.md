# v503-gmut-thos-v39-v7-x2 App Wrapper Stale Receipt Repair Policy

- generated_utc: `2026-06-08T20:33:03Z`
- overall_status: `PASS_APP_WRAPPER_STALE_RECEIPT_REPAIR_POLICY_BUILT`

## Policy Steps

- Wait for cadence gate.
- Probe existing app lanes only.
- Redact the probe receipt.
- Direct notify existing lanes once.
- Redact the notifier receipt.
- Run the direct repair gate.
- Normalize app and CLI evidence into five-lane readiness.

## Non-Goals

- No new app threads.
- No old-style subagent spawning.
- No raw app thread publication.
- No account or plugin-cache mutation.
- No phase advancement from duration alone.

Boundary: status-only repair policy; no raw lane text or private traces.
