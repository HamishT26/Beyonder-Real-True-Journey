# v503-gmut-thos-v39-v8-x2 CLI Quality Regression Tracker

Generated UTC: `2026-06-08T21:45:22Z`

Status: `PASS_CLI_QUALITY_REGRESSION_TRACKER_BUILT`

## v8 Metrics

- Arby: `PASS_ELABORATION_GATE`, `5184` words, `84` counted items, strict marker count `0`.
- Aster Vale: `PASS_ELABORATION_GATE`, `4565` words, `80` counted items, strict marker count `0`.
- Aster Vale generic marker warning: reviewed as `PASS_FALSE_POSITIVE_GENERIC_MARKER_REVIEW`.

## Regression Rules

- Require final-message-ready status before quality pass.
- Require minimum word count and required headings for both CLI lanes.
- Review generic marker warnings against strict quality marker counts before blocking.
- Publish only hashes, counts, and status summaries.

Raw CLI text remains temp-only.
