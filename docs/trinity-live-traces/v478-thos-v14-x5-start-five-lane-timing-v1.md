# v478-thos-v14-x5-start Five-Lane Start Timing

- generated_nz: `2026-06-05T09:21:13+12:00`
- overall_status: `PASS_FIVE_LANE_START`
- observation_run_index_today: `2`
- observation_window_seconds: `1800`
- average_response_seconds_this_run: `188.248`
- soft_timeout_baseline_status: `ONE_OF_THREE_OBSERVATIONS_RECORDED`
- publication boundary: lane body text, local temp paths, transport output, sessions, screenshots, and credentials are not published.
- claim boundary: start timing only; all GMUT gates remain open.

## Lane Timing
- Cicero / codex_app_local_server: `completed`, start `2026-06-04T21:02:32+00:00`, completion `2026-06-04T21:05:52+00:00`, duration `200.422`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Kierkegaard / codex_app_local_server: `completed`, start `2026-06-04T21:05:52+00:00`, completion `2026-06-04T21:07:15+00:00`, duration `82.594`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Aristotle / codex_app_local_server: `completed`, start `2026-06-04T21:07:15+00:00`, completion `2026-06-04T21:08:35+00:00`, duration `80.359`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Arby / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T21:02:29+00:00`, completion `2026-06-04T21:08:38+00:00`, duration `369.758`, basis `observed_process_start_arg_and_final_message_mtime`.
- Aster Vale / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T21:02:28+00:00`, completion `2026-06-04T21:05:56+00:00`, duration `208.109`, basis `observed_process_start_arg_and_final_message_mtime`.

## Handoff
- Treat this as observation run 2 of 3 for the five-sibling timing baseline.
- Repeat the same timing ledger until three five-sibling observations exist before deriving the soft future timeout average.
- Keep the every-second-session five-lane rule active at both start and closeout boundaries.
- Use idle notifier time for source, command, stale-flow, and approval prep rather than manual polling.
