# v470 THOS v6 x4 Row-Universe Reconciliation

This artifact reconciles the v6 x2 local report row universe at count level.

## Result

- Supervisor export rows: `8`.
- Regression execution rows: `4`.
- Unreconciled exception rows: `0`.
- Visualization embedded supervisor rows: `8`.
- Visualization embedded regression rows: `4`.
- Reconciliation status: `PASS_SHAPE_ONLY`.

## Open Gap

The visualization currently embeds local rows inside HTML. v6 x5 should externalize those rows as JSON or add a safe extractor so row-universe digests can be checked mechanically, not just by count.
