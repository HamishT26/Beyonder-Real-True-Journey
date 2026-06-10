# v499 GMUT/THOS v35 v6 x1 Helper Launch Defect Hypothesis

- generated_utc: `2026-06-07T09:32:30Z`
- overall_status: `PASS_PRODUCTIVE_WAIT_HELPER_DEFECT_HYPOTHESIS_READY`
- next_direct_repair_check_not_before_utc: `2026-06-07T09:40:43Z`
- manual_repair_output_checked: `false`

## Evidence

- The strict helper launch receipt reported process starts for Arby and Aster Vale.
- No expected final-message files existed at the cadence gate.
- No strict helper stdout/stderr files existed at the cadence gate.
- App lanes passed independently.
- A direct no-space bridge repair launched for both CLI lanes.

## Hypotheses

- Python-launched detached PowerShell wrappers may have exited or been suppressed before executing the wrapper body.
- `process_started` proves launch attempt only, not execution proof.
- Discarded wrapper stdout/stderr makes helper failures invisible.

## x2 Build Candidates

- Add wrapper-start and wrapper-exit sentinel files, surfaced only through status receipts.
- Avoid detached wrapper mode until sentinel proof exists.
- Prefer the direct Start-Process bridge until the Python helper proves wrapper execution.
- Treat process start as launch attempt, never completion or execution proof.
