# v499 GMUT/THOS v35 v3 x1 CLI Lane Launch Receipt

- generated_utc: `2026-06-07T05:55:07Z`
- overall_status: `PASS_CLI_LANES_LAUNCHED_WITH_FALLBACK_WATCH`
- first_manual_status_check_not_before_utc: `2026-06-07T06:06:22Z`
- manual_babysitting_required: `false`
- watcher_supervision_required: `true`

## Lanes

- Arby: existing read-only CLI lane launched at `2026-06-07T05:51:22Z`; short launcher wait did not complete, as expected for an elaborate x1 advisory run.
- Aster Vale: existing read-only CLI lane launched at `2026-06-07T05:51:22Z`; short launcher wait did not complete, as expected for an elaborate x1 advisory run.

## Watcher Fallback

- CLI watcher-control start timed out at the launcher-control layer.
- This is carried as a watcher-control open gap, not as a sibling-lane failure.
- No CLI output should be inspected before the x1 cadence gate.
- If no background completion receipt appears by the cadence gate, run the one-shot CLI completion notifier.

Raw lane output remains unpublished.
