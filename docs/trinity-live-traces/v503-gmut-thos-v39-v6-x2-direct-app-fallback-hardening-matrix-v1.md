# v503-gmut-thos-v39-v6-x2 Direct App Fallback Hardening Matrix

- generated_utc: `2026-06-08T19:22:56Z`
- overall_status: `PASS_DIRECT_APP_FALLBACK_MATRIX_BUILT`
- v6_x1_direct_repair_gate: `PASS_APP_LANE_COMPLETION_GATE`

## Fallback Flow

- Background wrapper waiting: trust watcher, do not poll before the cadence mark.
- Wrapper completion receipt missing: after cadence allows a check, run a probe-only direct existing-lane diagnostic.
- Probe passed: redact the diagnostic, then run the direct completion notifier once.
- Direct notify passed: redact the notifier receipt, then run the direct repair gate.
- Direct repair gate passed: normalize app and CLI evidence into five-lane readiness.
- Direct repair gate failed: publish a bounded blocker receipt and pause only if the failure escapes approved scope.

## Acceptance Criteria

- No raw app thread text, private runtime traces, screenshots, credentials, or private dumps are published.
- Existing callable app lanes only; no new thread, replacement sibling, or old-style subagent.
- Five-lane readiness requires app and CLI evidence together.
