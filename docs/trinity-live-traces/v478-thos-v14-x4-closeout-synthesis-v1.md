# v478 THOS v14 x4 Closeout Synthesis

- generated_nz: `2026-06-05T08:47:00+12:00`
- overall_status: `PASS_X4_CLOSEOUT_WITH_FIVE_LANE_EVIDENCE`
- claim boundary: v478 THOS v14 x4 closeout only; all GMUT gates remain open; no canon promotion; lane body text stays unpublished.

## Evidence

- App lanes: `PASS` in `v478-thos-v14-x4-closeout-background-council-app-completion-v1.json`.
- Cicero completed in `261.86` seconds.
- Kierkegaard completed in `123.843` seconds.
- Aristotle completed in `125.735` seconds.
- CLI lanes: `FINAL_MESSAGES_READY` in `v478-thos-v14-x4-closeout-cli-completion-v1.json`.
- Arby completed in `1500.722` seconds with `1705` final-message bytes and no final marker-review flag.
- Aster Vale completed in `521.915` seconds with `978` final-message bytes and no final marker-review flag.
- Multiplex board: `ALL_LANES_READY` in `v478-thos-v14-x4-closeout-local-multiplex-tui-app-server-runner-v1.json`.
- Timing receipt: observation run `1` of `3`, average `506.815` seconds, baseline still pending.
- Source refresh: compact public-source ledger published in `v478-thos-v14-x4-closeout-source-refresh-v1.json`.

## Lessons

- The local app-server route remains healthy for Cicero, Kierkegaard, and Aristotle.
- The CLI route remains viable for Arby and Aster Vale when launched read-only with fresh temp output and status-only receipts.
- Arby can take much longer than Aster Vale while still completing inside the 30-minute observation window.
- The multiplex board needed one compatibility patch to recognize the closeout CLI receipt naming shape.
- The three-run timing baseline should remain pending until two more five-lane observations are recorded.

## v14 x5 Handoff

- Use v478 THOS v14 x5 start as observation run 2 of 3 if the lanes are called again immediately.
- Keep the 30-minute observation ceiling for all five lanes.
- Continue useful approved work during idle waits: command index compatibility, v54/v55 handoff surfacing, source refresh, stale-flow refresh, and approval-packet preparation.
- After observation run 3, rerun the timing baseline aggregator and use the computed average only as a soft wait baseline, never as completion proof.
- Keep all GMUT gates open and leave lane body text unpublished.
