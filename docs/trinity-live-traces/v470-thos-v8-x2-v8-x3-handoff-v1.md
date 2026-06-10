# v470 THOS v8 x2 to v8 x3 Handoff

Next expected phase: `v470_THOS_v8_x3`

## Carry Forward

- Add compact-fixture assertion coverage.
- Check required row fields and summary consistency.
- Ensure non-empty missing-required or unexpected-extra lists force `FAIL_BLOCKER`.
- Keep full `reason_codes` mandatory whenever a dominant reason exists.
- Keep renderer migration blocked until compact-fixture assertion coverage remains green.

## Open Blockers

- Local fixture generation does not certify platform-wide safety.
- Thread/app-lane send tools were not exposed in this turn.
- Arby and Aster Vale internal shell inspection remains blocked by Windows sandbox spawn setup refresh.
- All six GMUT gates remain open.
