# v499 GMUT/THOS v35 v3 x2 Five-Lane Evidence Matrix

- generated_utc: `2026-06-07T07:07:53Z`
- overall_status: `PASS_EVIDENCE_MATRIX_BUILT`
- x1_result: `PASS_FIVE_LANE_READY_AFTER_REPAIR`

## Required For X1 Closeout

- Five-lane launch receipt.
- Productive wait contract.
- App completion gate.
- CLI completion notifier.
- CLI elaboration quality gate.
- Marker review when notifier flags markers.
- Five-lane normalized status board.
- Exposure guard.
- Exact staging.
- Remote-equals-local verification.

## Refusal Conditions

- Raw lane output appears in staged files.
- App thread IDs are unredacted.
- CLI quality gate fails.
- Five-lane normalizer is not `PASS_FIVE_LANE_READY`.
- Remote drift is nonzero before publication.
