# Allocation conservation residual contract

Operation: `cg_efficiency`. Compare the exact allocation sum with grand-coalition worth without rounding.

```json
{"operation":"cg_efficiency","game":{"players":["A","B","C"],"values":[0,1,2,5,0,2,3,9]},"allocation":[[9,1],[1,1],[0,1]]}
```

Expected complete envelope:

```json
{"ok":true,"value":{"allocation_sum":[10,1],"grand_worth":9,"gap":[-1,1],"efficient":false},"error":null}
```

Reject unknown fields, other symbol sets, wrong vector sizes, noninteger or out-of-range worths, nonzero empty worth and malformed rational pairs. The request remains unchanged. The integer grid, where used, covers only the zero-to-twelve cube; it does not establish a continuous-core result. Historical and current callers remain available. A correction is additive and never replays a successful domain session or canonical.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20.
