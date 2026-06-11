# v507 GMUT/THOS v43 v6 x1 App-Lane Private ID Contract

- overall_status: `PASS_PRIVATE_ID_CONTRACT_RECORDED`
- reason: app-lane callable IDs are needed for local routing but must not be published in repo artifacts or scripts.
- runner: `scripts/thos_app_lane_completion_notifier.py`
- private input surface: `THOS_APP_LANE_IDS_JSON`
- supported lanes: `Cicero`, `Kierkegaard`, `Aristotle`
- repository publishes raw callable IDs: `false`
- receipts publish short digest only: `true`

The safe contract is simple: the repo carries the reusable runner logic, while private callable IDs remain a local runtime input. Generated receipts can confirm lane identity through lane names and short digests without exposing raw app metadata.
