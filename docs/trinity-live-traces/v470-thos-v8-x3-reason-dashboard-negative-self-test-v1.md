# v470 THOS v8 x3 Reason Dashboard Negative Self-Test

Self-test: `reason_dashboard_fixture_negative_detection_v1`

Status: `PASS_SHAPE_ONLY`

## What Was Proven

The assertion script rejects a deliberately inconsistent compact fixture. The expected-negative report produced `FAIL_BLOCKER` for hidden missing/extra row logic, a non-empty missing-required list that was not blocked, summary mismatch, and aggregate-status mismatch.

## Boundary

This is a local negative self-test only. It does not touch connectors, cloud state, cleanup surfaces, sibling worktrees, renderer migration, or GMUT gates.
