# v498 GMUT/THOS v34 v5 x1 CLI Lane Launch Receipt

- generated_utc: `2026-06-07T02:08:18Z`
- overall_status: `PASS_CLI_LANES_LAUNCHED`
- first_manual_status_check_not_before_utc: `2026-06-07T02:20:51Z`
- manual_babysitting_required: `false`
- watcher_supervision_required: `true`

## Lanes

- Arby: existing read-only CLI lane launched at `2026-06-07T02:05:50Z`; short launcher wait did not complete, as expected for the extended x1 advisory run.
- Aster Vale: existing read-only CLI lane launched at `2026-06-07T02:05:51Z`; short launcher wait did not complete, as expected for the extended x1 advisory run.

## Carry Forward Controls

- Use the status receipt exposure guard before publication.
- Do not manually poll before the cadence gate.
- Redact app thread IDs before publication.

Raw lane output remains unpublished.
