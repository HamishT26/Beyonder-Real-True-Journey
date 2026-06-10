# v499-gmut-thos-v35-v1-x2 Slow-Startup Warning Classifier

- generated_utc: `2026-06-07T05:00:49Z`
- overall_status: `PASS_CLASSIFIER_BUILT`

## Rules
- Slow SQL startup warnings are stale-flow watch items when final artifacts and quality gates pass.
- They become repair candidates after three consecutive phases where they correlate with missing final artifacts.
- They do not justify destructive cleanup, cache deletion, or active package mutation without exact approval.
- Watcher-control timeout risk is recorded separately from sibling completion state.
