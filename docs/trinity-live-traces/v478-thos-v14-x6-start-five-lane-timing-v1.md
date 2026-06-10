# v478-thos-v14-x6-start Five-Lane Start Timing

- generated_nz: `2026-06-05T10:32:26+12:00`
- overall_status: `PASS_FIVE_LANE_START`
- observation_run_index_today: `4`
- observation_window_seconds: `1800`
- average_response_seconds_this_run: `955.265`
- soft_timeout_baseline_status: `THREE_RUN_BASELINE_ALREADY_READY_X6_OVER_WINDOW_COMPLETION_OBSERVED`
- publication boundary: lane body text, local temp paths, transport output, sessions, screenshots, and credentials are not published.
- claim boundary: start timing only; all GMUT gates remain open.

## Lane Timing
- Cicero / codex_app_local_server: `completed`, start `2026-06-04T21:52:35+00:00`, completion `2026-06-04T21:56:27+00:00`, duration `232.156`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Kierkegaard / codex_app_local_server: `completed`, start `2026-06-04T21:56:27+00:00`, completion `2026-06-04T21:58:03+00:00`, duration `96.75`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Aristotle / codex_app_local_server: `completed`, start `2026-06-04T21:58:03+00:00`, completion `2026-06-04T21:59:49+00:00`, duration `105.734`, basis `derived_from_app_receipt_generated_utc_and_sequential_lane_duration`.
- Arby / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T21:52:30+00:00`, completion `2026-06-04T22:29:15+00:00`, duration `2205.164`, basis `observed_process_start_arg_and_final_message_mtime`.
- Aster Vale / codex_cli_read_only: `FINAL_MESSAGE_READY`, start `2026-06-04T21:52:30+00:00`, completion `2026-06-04T22:28:06+00:00`, duration `2136.519`, basis `observed_process_start_arg_and_final_message_mtime`.

## Handoff
- Treat this as a post-baseline observation showing formal CLI completion can arrive after the 30-minute observation window.
- Keep the original three-run `312.832` second average as the soft future wait foothold; do not replace it with this over-window run unless a rolling-average policy is approved.
- Keep the every-second-session five-lane rule active at both start and closeout boundaries.
- Use idle notifier time for source, command, stale-flow, and approval prep rather than manual polling.
- Carry Arby's marker-review resolution and the CLI over-window behavior into the next retry2/direct-advisory planning pass.
