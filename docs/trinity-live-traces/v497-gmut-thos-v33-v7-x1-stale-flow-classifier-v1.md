# v497 GMUT/THOS v33 v7 x1 Stale-Flow Classifier

- overall_status: `PASS_STALE_FLOW_CLASSIFIER_READY`
- generated_utc: `2026-06-06T22:05:20Z`
- lane_status_harvested: `false`

## Classes

- `APP_WATCHER_STARTED_COMPLETION_MISSING`: phase-blocking until resolved. Safe attempts are confirm runner receipt, confirm missing completion notifier, retry existing app watcher with distinct receipt prefix, wait until retry check window, and publish a blocker receipt if retry still fails.
- `CLI_FINAL_MESSAGE_MARKER_REVIEW`: review-required but not phase-blocking after quality pass. Safe attempts are hash final message, count bytes, run elaboration gate, confirm strict sensitive/path markers zero, and publish status-only quality receipt.
- `AGGREGATE_STALE_ROW_COMPLETE`: warning when lane rows are completed. Safe attempts are read completed row statuses, avoid raw message bodies, normalize aggregate state, publish repair-state note, and carry warning forward.

The classifier is repair planning only. GMUT and canon gates remain open.
