# v499 GMUT/THOS v35 v6 x2 Direct Bridge Fallback Policy

- generated_utc: `2026-06-07T09:57:10Z`
- overall_status: `PASS_DIRECT_BRIDGE_FALLBACK_POLICY_READY`

## Policy

- Missing wrapper-start sentinel means helper execution gap.
- Wrapper-start without wrapper-exit means wrapper still running or hung.
- Wrapper-exit without expected notifier file means bridge-copy repair may be needed after the cadence gate.
- Raw bridge output plus strict quality pass allows five-lane normalization after copy.
- Do not advance phase while either CLI lane lacks final-message quality pass.
- Publish only status receipts, hashes, counts, and redacted telemetry.
