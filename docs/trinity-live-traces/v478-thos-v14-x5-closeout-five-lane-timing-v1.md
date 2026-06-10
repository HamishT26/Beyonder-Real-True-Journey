# v478-thos-v14-x5-closeout Five-Lane Closeout Timing

- generated_nz: `2026-06-05T09:33:58+12:00`
- overall_status: `PASS_FIVE_LANE_CLOSEOUT`
- observation_run_index_today: `3`
- observation_window_seconds: `1800`
- average_response_seconds_this_run: `243.431`
- soft_timeout_baseline_status: `READY_TO_COMPUTE_THREE_RUN_AVERAGE`
- publication boundary: lane body text, local temp paths, transport output, sessions, screenshots, and credentials are not published.
- claim boundary: closeout timing only; all GMUT gates remain open.

## Lane Timing
- Cicero / codex_app_local_server: `completed`, start `2026-06-04T21:25:58+00:00`, completion `2026-06-04T21:29:50+00:00`, duration `232.046`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Kierkegaard / codex_app_local_server: `completed`, start `2026-06-04T21:29:50+00:00`, completion `2026-06-04T21:31:20+00:00`, duration `90.485`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Aristotle / codex_app_local_server: `completed`, start `2026-06-04T21:31:20+00:00`, completion `2026-06-04T21:32:51+00:00`, duration `91.125`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Arby / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T21:25:56+00:00`, completion `2026-06-04T21:32:49+00:00`, duration `413.912`, basis `observed_process_start_arg_and_final_message_mtime`.
- Aster Vale / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T21:25:56+00:00`, completion `2026-06-04T21:32:25+00:00`, duration `389.588`, basis `observed_process_start_arg_and_final_message_mtime`.

## Handoff
- Treat this as observation run 3 of 3 for the five-sibling timing baseline.
- Repeat the same timing ledger until three five-sibling observations exist before deriving the soft future timeout average.
- Keep the every-second-session five-lane rule active at both start and closeout boundaries.
- Use idle notifier time for source, command, stale-flow, and approval prep rather than manual polling.
