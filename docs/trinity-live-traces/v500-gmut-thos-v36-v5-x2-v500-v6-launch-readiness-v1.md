# v500 GMUT/THOS v36 v5 x2 to v500 v6 x1 Launch Readiness

- generated_utc: `2026-06-07T19:50:12Z`
- overall_status: `PASS_READY_FOR_V500_V6_X1_AFTER_PUBLICATION`
- next_phase_slug: `v500-gmut-thos-v36-v6-x1`

## Required Before Launch

- Commit, push, and remote-verify the v500 v5 x2 package.
- Launch app lanes through existing local app-server callable routes.
- Launch CLI lanes with the temp `.cmd` bridge launcher.
- Publish launch-safe receipts only.
- Wait until the 15-minute x1 cadence mark before completion checks.
- Work on source-safe preparation during the wait instead of polling lane status.

## Repair Policy

- If expected CLI final surfaces are missing, attempt bridge repair before retry.
- If generic marker count conflicts with strict quality markers, run marker review ledger.
- If classifier finds a new receipt type, patch classifier coverage before publication.

GMUT, physics, consciousness, and canon gates remain open.
