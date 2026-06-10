# v470 THOS v5 x2 Visualization Dataset

This is a schema-first visualization dataset derived from supervisor dry-run rows.

It is not a rendered dashboard yet. It is safe to visualize because it contains normalized fixture IDs, rule IDs, statuses, risks, and expected interpretations only. It does not include raw logs, screenshots, credentials, private Drive contents, or session JSONL.

## Dataset Meaning

- `PASS_SHAPE_ONLY` rows show local shape checks and observe-only routes.
- `OPEN_GAP` rows show approval or scope gaps.
- `FAIL_BLOCKER` rows show active guardrails.

Expected-failure rows should be labeled as active guardrails, not defects.
