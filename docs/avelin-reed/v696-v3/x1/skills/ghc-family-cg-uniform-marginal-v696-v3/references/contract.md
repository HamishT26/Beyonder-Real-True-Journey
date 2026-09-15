# Uniform-subset marginal mean contract

Operation: `cg_uniform_marginal`. Average the four marginal contributions for each symbol; do not assume their sum is the grand worth.

```json
{"operation":"cg_uniform_marginal","game":{"players":["A","B","C"],"values":[0,1,2,5,0,2,3,9]},"allocation":[[9,1],[1,1],[0,1]]}
```

Expected complete envelope:

```json
{"ok":true,"value":[[3,1],[4,1],[3,2]],"error":null}
```

Reject unknown fields, other symbol sets, wrong vector sizes, noninteger or out-of-range worths, nonzero empty worth and malformed rational pairs. The request remains unchanged. The integer grid, where used, covers only the zero-to-twelve cube; it does not establish a continuous-core result. Historical and current callers remain available. A correction is additive and never replays a successful domain session or canonical.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20.
