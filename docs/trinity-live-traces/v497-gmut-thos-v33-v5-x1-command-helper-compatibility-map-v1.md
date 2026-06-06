# v497 GMUT/THOS v33 v5 x1 Command + Helper Compatibility Map

- overall_status: `PASS_COMPATIBILITY_MAP_READY_FOR_X2`
- generated_utc: `2026-06-06T19:23:00Z`

## Usable Helpers

- `thos_codex_cli_advisory_launcher.py`: launch existing read-only CLI advisory lanes with redacted launch receipts and temp-only outputs.
- `thos_cli_lane_completion_notifier.py`: produce status-only CLI completion receipts at scheduled cadence marks or explicit repair checks.
- `thos_cli_elaboration_quality_gate.py`: count words, headings, category items, and sensitive/path markers without publishing raw text.
- `thos_app_lane_completion_notifier.py`: read/resume existing app lanes and avoid duplicate notifications when completion receipts already exist.
- `thos_council_app_lane_notifier_runner.py`: prefer background-watch mode so Aletheon can keep preparing instead of babysitting.
- `thos_status_check_cadence_guard.py`: keep first x1 checks at 15 minutes and x2 prep checks at 10 minutes unless a new packet changes cadence.
- `thos_five_lane_status_normalizer.py`: normalize app and CLI receipts into a five-lane board, with x2 follow-up needed for explicit `repair_state`.
- `thos_stale_flow_refresh_runner.py`: classify repeated blockers and stale-flow watch items without destructive repair.
- `thos_publication_provenance_receipt.py`: produce subject-file hash provenance receipts.
- `thos_v497_v4_x1_closeout_x2_builder.py`: reuse as a design pattern for a v5-specific closeout/x2 builder.

## Blocked Or Deferred

- Raw lane readers: blocked for publication.
- New sibling/thread creators: blocked because existing lanes only.
- Destructive cleanup commands: blocked because no destructive cleanup is approved.

All GMUT and canon gates remain open. No raw/private material is published.
