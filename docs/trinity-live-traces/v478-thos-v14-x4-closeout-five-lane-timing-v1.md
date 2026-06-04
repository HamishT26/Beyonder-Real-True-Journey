# v478-thos-v14-x4-closeout Five-Lane Closeout Timing

- generated_nz: `2026-06-05T08:45:41+12:00`
- overall_status: `PASS_FIVE_LANE_CLOSEOUT`
- observation_run_index_today: `1`
- observation_window_seconds: `1800`
- average_response_seconds_this_run: `506.815`
- soft_timeout_baseline_status: `ONE_OF_THREE_OBSERVATIONS_RECORDED`
- publication boundary: raw lane text, local temp paths, transport output, sessions, screenshots, and credentials are not published.
- claim boundary: closeout timing only; all GMUT gates remain open.

## Lane Timing
- Cicero / codex_app_local_server: `completed`, start `2026-06-04T20:20:06+00:00`, completion `2026-06-04T20:24:27+00:00`, duration `261.86`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Kierkegaard / codex_app_local_server: `completed`, start `2026-06-04T20:24:27+00:00`, completion `2026-06-04T20:26:31+00:00`, duration `123.843`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Aristotle / codex_app_local_server: `completed`, start `2026-06-04T20:26:31+00:00`, completion `2026-06-04T20:28:37+00:00`, duration `125.735`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Arby / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T20:20:02+00:00`, completion `2026-06-04T20:45:02+00:00`, duration `1500.722`, basis `observed_process_start_arg_and_final_message_mtime`.
- Aster Vale / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T20:20:02+00:00`, completion `2026-06-04T20:28:43+00:00`, duration `521.915`, basis `observed_process_start_arg_and_final_message_mtime`.

## Handoff
- Treat this as observation run 1 of 3 for the five-sibling timing baseline.
- Repeat the same timing ledger for the next two five-sibling runs before deriving the soft future timeout average.
- Keep the every-second-session five-lane rule active at both start and closeout boundaries.
- Use idle notifier time for source, command, stale-flow, and approval prep rather than manual polling.
