# v499 GMUT/THOS v35 v5 x2 to v499 v6 x1 Launch Readiness

- generated_utc: `2026-06-07T09:01:42Z`
- overall_status: `PASS_NEXT_X1_READY_AFTER_X2_PUBLICATION`
- next_phase_slug: `v499-gmut-thos-v35-v6-x1`

## Readiness Conditions

- Publish and remote-verify v499 v5 x2 first.
- Confirm fetch/drift is zero before launch.
- Use all five existing lanes.
- App lanes use the background council notifier runner.
- CLI lanes use `thos_cli_strict_stdin_lane_launcher.py` with safe internal filenames.
- Aletheon performs productive wait work until the x1 cadence mark.
- Five-lane normalizer must pass before x1 closeout.
