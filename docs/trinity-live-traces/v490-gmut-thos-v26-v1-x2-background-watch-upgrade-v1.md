# v490 GMUT/THOS v26 v1 x2 Background Watch Upgrade

Generated NZ: `2026-06-06T02:52:00+12:00`

Status: `PASS_BACKGROUND_START_WITH_OPEN_PROBE_EVIDENCE`

Updated script: `scripts/thos_council_app_lane_notifier_runner.py`

New flag: `--background-watch`

Behavior:
- Starts the existing app-lane watcher stack as a detached background process.
- Returns immediately after process start.
- Discards raw stdout/stderr rather than publishing raw transport.
- Expects the lower-level watch launcher and completion notifier to write their own status receipts.
- Lets Aletheon continue source refresh, next-phase planning, guardrail refinement, runner work, and approval packet preparation while the lanes run.

Smoke probe:
- Runner status: `PASS_BACKGROUND_WATCH_STARTED`
- Watch launcher status: `OPEN_GAP_APP_LANE_LAUNCH`
- Completion notifier status: `OPEN_GAP_APP_LANE_PROBE`
- Interpretation: the top-level background start succeeded and returned immediately. The non-notifying lower-level probe found one busy/resume-blocked app lane while two lanes probed cleanly, so this is an app-lane state gap rather than a background-launch failure.

Mandatory future rule:
- Future x1 app-lane calls should use `--background-watch --notify` when the goal is to send once and keep working while watcher/notifier helpers observe completion.
- A background start is not completion proof; completion still requires later watcher/notifier receipts or a blocker receipt.
- Keep all GMUT empirical, physics, consciousness, and canon gates open.
