# v501-gmut-thos-v37-v6-x1 Launch Timeout Regression Prep

- generated_at_utc: `2026-06-08T01:36:05Z`
- overall_status: `PASS_LAUNCH_TIMEOUT_REGRESSION_PREP_RECORDED`
- manual_lane_polling_performed: `False`
- status_only: `True`

## Observed Regression
The first v6 CLI launcher foreground command exceeded its shell timeout before writing a receipt; a retry with a longer foreground window wrote the launch receipt and started both lanes.

## X2 Hardening Candidates
1. Add a launcher-start receipt stage that writes a planned-start status before process creation.
2. Separate shell foreground timeout from lane-output readiness in closeout synthesis.
3. Keep repair actions scoped to relaunching existing CLI lanes when no launch receipt exists.
4. Do not treat missing launch receipt as sibling failure until start receipt, process status, and output alias evidence are checked after a cadence gate.
5. Keep all local temp paths, command lines, process IDs, stdout, stderr, and raw final messages unpublished.

## Boundary
Status-only. No raw lane text, raw logs, local temp paths, session streams, screenshots, credentials, private dumps, or closure overclaims are included.
