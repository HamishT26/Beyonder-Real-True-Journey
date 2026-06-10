# v498 GMUT/THOS v34 v7 x1 CLI Lane Launch Receipt

- generated_utc: `2026-06-07T03:18:25Z`
- overall_status: `PASS_CLI_LANES_LAUNCHED`
- first_manual_status_check_not_before_utc: `2026-06-07T03:31:56Z`
- manual_babysitting_required: `false`
- watcher_supervision_required: `true`

## Lanes

- Arby: existing read-only CLI lane launched at `2026-06-07T03:16:56Z`; short launcher wait did not complete, as expected for the extended x1 advisory run.
- Aster Vale: existing read-only CLI lane launched at `2026-06-07T03:16:56Z`; short launcher wait did not complete, as expected for the extended x1 advisory run.

## Carry Forward Controls

- Watchers supervise lanes.
- No manual status check before the cadence gate.
- Run exposure guard before publication.
- Redact app thread IDs before closeout staging.

Raw lane output remains unpublished.
