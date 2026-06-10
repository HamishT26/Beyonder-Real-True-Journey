# v498-gmut-thos-v34-v8-x1 Watcher Launch Timeout Repair Pattern

- generated_utc: `2026-06-07T04:10:33Z`
- overall_status: `PASS_REPAIR_PATTERN_READY`
- classification: `launcher_control_timeout_not_sibling_output_blocker`

## Pattern
- Do not inspect sibling output to diagnose a launcher-control timeout before the cadence gate.
- Start the watcher through a hidden background process when the launcher wrapper does not return.
- Record the repair as watcher-control metadata only.
- At cadence gate, read watcher receipts first before any manual lane probe.
- If watcher receipt is missing at cadence gate, write an open-gap watcher receipt and then run bounded repair attempts.

No raw output, session stream, local path, destructive action, or private material is published.
