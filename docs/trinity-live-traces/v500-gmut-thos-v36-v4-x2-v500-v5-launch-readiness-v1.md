# v500 GMUT/THOS v36 v4 x2 to v500 v5 x1 Launch Readiness

- generated_utc: `2026-06-07T19:06:15Z`
- overall_status: `PASS_READY_FOR_V500_V5_X1_AFTER_PUBLICATION`
- next_phase_slug: `v500-gmut-thos-v36-v5-x1`

## Required Before Launch

- Commit, push, and remote-verify the v500 v4 x2 package.
- Launch Cicero, Kierkegaard, and Aristotle through existing local app-server callable routes.
- Launch Arby and Aster Vale through `thos_cli_direct_bridge_cmd_launcher.py`.
- Publish launch-safe receipts only.
- Wait until the 15-minute x1 cadence mark before completion checks.
- Use the wait window for preparation and source-safe synthesis instead of polling lane status.

## Watcher Policy

Trust watcher/notifier helpers until the cadence mark. If a hard blocker appears, record a status-only receipt. For CLI final surface gaps, use repair-before-retry. Do not move to x2 closeout until all five lane statuses are normalized ready or an explicit blocker receipt is published.

GMUT, physics, consciousness, and canon gates remain open.
