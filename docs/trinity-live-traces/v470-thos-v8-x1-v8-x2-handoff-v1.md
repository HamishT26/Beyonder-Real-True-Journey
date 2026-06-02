# v470 THOS v8 x1 to v8 x2 Handoff

Next expected phase: `v470_THOS_v8_x2`

## Carry Forward

- Add a dashboard-facing fixture for `missing_required_reason_codes`.
- Keep `reason_codes` mandatory when `dominant_reason_code` is present.
- Render required, matched, missing, allowed-extra, unexpected-extra, and dominant reason fields together.
- Keep connector writes, cloud writes, destructive cleanup, publication authority, and GMUT gate movement outside this local guard lane.
- Keep renderer migration blocked until broader manifest-aware assertion coverage remains green.

## Open Blockers

- Local harness enforcement does not certify platform-wide safety.
- Thread/app-lane send tools were not exposed in this turn.
- Arby and Aster Vale internal shell inspection remains blocked by Windows sandbox spawn setup refresh.
- All six GMUT gates remain open.
