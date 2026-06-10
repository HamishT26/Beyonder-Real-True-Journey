# v504-gmut-thos-v40-v1-x2 CLI Quality Regression Tracker

Generated UTC: `2026-06-08T22:49:18Z`

Status: `PASS_CLI_QUALITY_REGRESSION_TRACKER_BUILT`

## Repair Story

- r1: `OPEN_GAP_CLI_ELABORATION_REPAIR_NEEDED`
- r1 Arby: `2086` words
- r1 Aster Vale: `1371` words
- r2: `PASS_ALL_CLI_LANES_ELABORATE`
- r2 Arby: `6056` words
- r2 Aster Vale: `5481` words

## Continuity Rules

- Short structured responses are useful but do not satisfy the long-form x1 gate.
- Repair prompts must request fresh standalone artifacts, not small addenda.
- Minimum word count, heading coverage, item coverage, strict marker count, and marker review must all pass.
- Do not advance from x1 to x2 until CLI repair passes when CLI lanes are required.
