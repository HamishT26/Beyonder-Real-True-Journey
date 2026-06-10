# v470 THOS v7 x8 to v8 x1 Handoff

Next expected phase: `v470_THOS_v8_x1`

## Carry Forward

- Consolidate dashboard-facing report fields: `dominant_reason_code`, `reason_codes`, `allowed_extra_reason_codes`, `unexpected_extra_reason_codes`, and `primary_selection_mode`.
- Consider adding explicit `missing_required_reason_codes` for easier rendering.
- Keep full `reason_codes` mandatory whenever `dominant_reason_code` is present.
- Keep connector writes, cloud writes, destructive cleanup, publication authority, and GMUT gate movement outside this local guard lane.
- Keep renderer migration blocked until broader manifest-aware assertion coverage remains green.

## Open Blockers

- Local harness enforcement does not certify platform-wide safety.
- Missing-required-code reporting is not a separate dashboard field yet.
- Arby and Aster Vale internal shell inspection remains blocked by Windows sandbox spawn setup refresh.
- All six GMUT gates remain open.
