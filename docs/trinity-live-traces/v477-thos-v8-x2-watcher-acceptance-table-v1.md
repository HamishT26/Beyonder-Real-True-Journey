# v477 THOS v8 x2 Watcher Acceptance Table

- generated_nz: `2026-06-04T08:27:16+12:00`
- overall_status: `PASS_WITH_CLI_OPEN_GAP`

## Criteria
- `app_read`: `PASS` — thread read returns ok.
- `app_resume`: `PASS` — thread resume returns ok under read-only request.
- `app_turn_start`: `PASS` — turn start returns ok.
- `app_turn_complete`: `PASS` — turn completion event observed.
- `cli_final_marker`: `OPEN_GAP` — final-message marker found in temp-only watcher output.
- `cli_timeout`: `PASS` — timeout without final marker is non-blocking if app lanes pass.
- `no_duplicate_polling`: `PASS` — one bounded CLI poll per x2 closeout.
- `no_transport_publication`: `PASS` — transport payloads remain unpublished.
