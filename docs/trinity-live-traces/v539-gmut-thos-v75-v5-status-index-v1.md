# v539-gmut-thos-v75-v5 Phase Status Index

Generated UTC: `2026-06-15T22:24:32Z`

Status: `PASS_PHASE_STATUS_INDEX`

Scanned JSON files: `25`

## Status Counts

- PASS: `1`
- PASS_ASSISTANT_MARKER_SOURCE_VERIFIED: `1`
- PASS_CURATED_SOURCE_REFRESH_LEDGER: `2`
- PASS_EXPOSURE_GUARD: `1`
- PASS_GROUPED_FULL_PHASE_GUARD: `1`
- PASS_GROUPED_LANE_X1_STATUS: `1`
- PASS_GROUPED_X2_BUILD_USE_CLOSEOUT: `1`
- PASS_GROUPED_X2_LANE_STATE_REDUCER: `1`
- PASS_GROUPED_X2_ROUTE_FAMILY_MANIFEST: `1`
- PASS_LUMEN_BROWSER_MARKER_STATUS: `2`
- PASS_PHASE_STATUS_INDEX: `1`
- PASS_WAIT_WORK_SOURCE_LEDGER: `1`
- READY_FOR_GROUPED_ROUND_ROBIN_X1: `1`
- READY_FOR_GROUPED_X2_BUILD_USE: `1`
- READY_FOR_HAMISH_REVIEW_OR_EXISTING_APPROVAL_FLOW: `3`
- READY_FOR_NEXT_GROUPED_X1: `2`
- READY_FOR_X2_AFTER_LUMEN_MARKER: `1`
- READY_FOR_X2_BUILD_USE_AND_NEXT_PHASE_PREP: `2`
- STATUS_NOT_FOUND: `1`

## Rows

- v539-gmut-thos-v75-v5-exposure-guard-v1.json: `PASS_EXPOSURE_GUARD`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-status-index-v1.json: `PASS_PHASE_STATUS_INDEX`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-approval-packets-v1.json: `READY_FOR_HAMISH_REVIEW_OR_EXISTING_APPROVAL_FLOW`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-continuity-handoff-v1.json: `READY_FOR_NEXT_GROUPED_X1`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-eureka-tasks-v1.json: `READY_FOR_X2_BUILD_USE_AND_NEXT_PHASE_PREP`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-grouped-lane-receipt-v1.json: `PASS_GROUPED_LANE_X1_STATUS`; lanes `Lumen Vale`; private flag `false`
- v539-gmut-thos-v75-v5-x1-guard-v1.json: `PASS`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-lumen-browser-route-receipt-v1.json: `STATUS_NOT_FOUND`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-lumen-marker-receipt-v1.json: `PASS_LUMEN_BROWSER_MARKER_STATUS`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-lumen-marker-source-validator-v1.json: `PASS_ASSISTANT_MARKER_SOURCE_VERIFIED`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-lumen-wait-approval-packets-v1.json: `READY_FOR_HAMISH_REVIEW_OR_EXISTING_APPROVAL_FLOW`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-lumen-wait-continuity-handoff-v1.json: `READY_FOR_X2_AFTER_LUMEN_MARKER`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-lumen-wait-source-ledger-v1.json: `PASS_WAIT_WORK_SOURCE_LEDGER`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-lumen-wait-work-receipt-v1.json: `PASS_LUMEN_BROWSER_MARKER_STATUS`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-next-group-prep-card-v1.json: `READY_FOR_GROUPED_ROUND_ROBIN_X1`; lanes `Lumen Vale`; private flag `false`
- v539-gmut-thos-v75-v5-x1-source-ledger-v1.json: `PASS_CURATED_SOURCE_REFRESH_LEDGER`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x1-to-x2-handoff-v1.json: `READY_FOR_GROUPED_X2_BUILD_USE`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x2-approval-packets-v1.json: `READY_FOR_HAMISH_REVIEW_OR_EXISTING_APPROVAL_FLOW`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x2-closeout-v1.json: `PASS_GROUPED_X2_BUILD_USE_CLOSEOUT`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x2-continuity-handoff-v1.json: `READY_FOR_NEXT_GROUPED_X1`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x2-eureka-tasks-v1.json: `READY_FOR_X2_BUILD_USE_AND_NEXT_PHASE_PREP`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x2-full-phase-guard-v1.json: `PASS_GROUPED_FULL_PHASE_GUARD`; lanes `none`; private flag `false`
- v539-gmut-thos-v75-v5-x2-lane-state-reducer-v1.json: `PASS_GROUPED_X2_LANE_STATE_REDUCER`; lanes `Lumen Vale`; private flag `false`
- v539-gmut-thos-v75-v5-x2-route-family-manifest-v1.json: `PASS_GROUPED_X2_ROUTE_FAMILY_MANIFEST`; lanes `Lumen Vale`; private flag `false`
- v539-gmut-thos-v75-v5-x2-source-ledger-v1.json: `PASS_CURATED_SOURCE_REFRESH_LEDGER`; lanes `none`; private flag `false`

## Boundary

This index publishes status rows only. It does not publish raw receipt payloads, sibling text, private browser URLs, route or callable IDs, credentials, screenshots, or local absolute paths.
