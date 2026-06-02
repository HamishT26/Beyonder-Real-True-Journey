# v470 THOS v8 x1 Missing-Required Self-Test

Self-test: `missing_required_reason_codes_detection_v1`

Status: `PASS_SHAPE_ONLY`

## What Was Proven

The evaluator reports a missing required code when an expected code is absent, while also reporting an unexpected extra code when an observed code is outside the expected plus allowed set.

## Expected And Observed

- Matched: `REQUIRED_PRESENT`
- Missing required: `REQUIRED_MISSING`
- Unexpected extra: `UNEXPECTED_EXTRA`

## Boundary

The self-test is local and non-mutating. It does not touch connectors, cloud state, cleanup surfaces, sibling worktrees, or GMUT gates.
