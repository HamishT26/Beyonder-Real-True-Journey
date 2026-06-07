# v500 GMUT/THOS v36 v2 x2 Marker Review Helper Build

- generated_utc: `2026-06-07T13:00:02Z`
- overall_status: `PASS_MARKER_REVIEW_HELPER_BUILT_AND_USED`
- helper_script: `scripts/thos_cli_marker_review_ledger.py`

The marker review helper was built to separate ordinary generic marker warnings from strict safety/path marker failures. It consumes curated notifier and quality receipts only.

Live v500 v2 x1 result:

- Arby: `PASS_FALSE_POSITIVE_GENERIC_MARKER_REVIEW`, generic marker count `1`, strict count `0`, quality `PASS_ELABORATION_GATE`
- Aster Vale: `PASS_FALSE_POSITIVE_GENERIC_MARKER_REVIEW`, generic marker count `2`, strict count `0`, quality `PASS_ELABORATION_GATE`

Default use policy: run this helper after CLI notifier plus quality gate whenever generic marker warnings appear. Do not read or publish raw lane text. If strict markers are nonzero or quality fails, keep the issue open instead of smoothing it over.
