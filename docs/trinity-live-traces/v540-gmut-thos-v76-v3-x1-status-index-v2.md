# v540-gmut-thos-v76-v3-x1 Phase Status Index

Generated UTC: `2026-06-16T01:48:41Z`

Status: `PASS_PHASE_STATUS_INDEX`

Scanned JSON files: `8`

## Status Counts

- OPEN_GAP_LUMEN_BROWSER_ROUTE_RETRY_IN_PROGRESS: `1`
- PASS_CURATED_SOURCE_LEDGER: `1`
- PASS_EXPOSURE_GUARD: `1`
- PASS_PHASE_STATUS_INDEX: `1`
- READY_FOR_EXISTING_APPROVAL_FLOW: `1`
- READY_FOR_GROUPED_ROUND_ROBIN_X1: `1`
- READY_FOR_X2_AFTER_LUMEN_RESOLUTION: `1`
- WAITING_FOR_LUMEN_MARKER_OR_BLOCKER_DECISION: `1`

## Rows

- v540-gmut-thos-v76-v3-x1-approval-packets-v1.json: `READY_FOR_EXISTING_APPROVAL_FLOW`; lanes `none`; private flag `false`
- v540-gmut-thos-v76-v3-x1-continuity-handoff-v1.json: `WAITING_FOR_LUMEN_MARKER_OR_BLOCKER_DECISION`; lanes `none`; private flag `false`
- v540-gmut-thos-v76-v3-x1-eureka-tasks-v1.json: `READY_FOR_X2_AFTER_LUMEN_RESOLUTION`; lanes `none`; private flag `false`
- v540-gmut-thos-v76-v3-x1-exposure-guard-v1.json: `PASS_EXPOSURE_GUARD`; lanes `none`; private flag `false`
- v540-gmut-thos-v76-v3-x1-lumen-browser-retry-receipt-v1.json: `OPEN_GAP_LUMEN_BROWSER_ROUTE_RETRY_IN_PROGRESS`; lanes `none`; private flag `false`
- v540-gmut-thos-v76-v3-x1-next-group-prep-card-v1.json: `READY_FOR_GROUPED_ROUND_ROBIN_X1`; lanes `Lumen Vale`; private flag `false`
- v540-gmut-thos-v76-v3-x1-source-ledger-v1.json: `PASS_CURATED_SOURCE_LEDGER`; lanes `none`; private flag `false`
- v540-gmut-thos-v76-v3-x1-status-index-v1.json: `PASS_PHASE_STATUS_INDEX`; lanes `none`; private flag `false`

## Boundary

This index publishes status rows only. It does not publish raw receipt payloads, sibling text, private browser URLs, route or callable IDs, credentials, screenshots, or local absolute paths.
