# v498-gmut-thos-v34-v8-x2 Runner-Control Timeout Repair Receipt

- generated_utc: `2026-06-07T04:27:04Z`
- overall_status: `PASS_REPAIR_RECEIPT_BUILT`
- repair_class: `watcher_launcher_return_timeout`
- used_in_v8_x1: `true`

## Safe Repair Ladder
- Classify timeout as launcher-control issue, not sibling-output issue.
- Avoid raw sibling-output inspection before cadence gate.
- Start watcher directly through hidden background process when wrapper does not return.
- Record watcher-control metadata only.
- At cadence gate, harvest watcher receipts first and only then run bounded repair if missing.
