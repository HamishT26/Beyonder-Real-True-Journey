# v499 GMUT/THOS v35 v4 x2 Marker Review Simplifier

- generated_utc: `2026-06-07T07:56:22Z`
- overall_status: `PASS_MARKER_REVIEW_SIMPLIFIER_READY`

## Finding

The strict CLI notifier raised a marker-review gap, but the strict quality gate showed zero strict sensitive/path markers and both CLI lanes passed elaboration. This means the marker workflow should distinguish generic vocabulary review from real exposure risk.

## Simplified Decision Tree

- Hold publication if strict sensitive/path markers are greater than zero.
- Fail if raw local paths, credentials, session streams, screenshots, or private transport are present.
- Treat generic ordinary-word flags as a review item, not automatic failure, when strict exposure markers are zero.
- Publish only status summaries, hashes, byte counts, word counts, and category counts.

This keeps the review strict without letting false positives become stale-flow blockers.
