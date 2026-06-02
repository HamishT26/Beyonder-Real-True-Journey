# v470 THOS v7 x7 to v7 x8 Handoff

Next expected phase: `v470_THOS_v7_x8`

## Carry Forward

- Move required secondary reason codes and allowed extra reason codes into the regression harness itself.
- Consider publishing a stable reason-code priority table artifact for dashboard consumers.
- Keep the full `reason_codes` array mandatory whenever `dominant_reason_code` is present.
- Keep connector writes, cloud writes, destructive cleanup, publication authority, and GMUT gate movement outside this local guard lane.
- Keep renderer migration blocked until broader manifest-aware assertion coverage remains green.

## Open Blockers

- Allowed-extra reason-code policy is documented but not enforced as a distinct harness field yet.
- Local receipts do not certify platform safety or authorize external actions.
- Arby and Aster Vale internal shell inspection remains blocked by Windows sandbox spawn setup refresh.
- All six GMUT gates remain open.
