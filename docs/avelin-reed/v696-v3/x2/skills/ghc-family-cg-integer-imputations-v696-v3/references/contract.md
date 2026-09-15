# Bounded integer imputation grid contract

Operation: `cg_integer_imputations`. Enumerate nonnegative integer allocations in the zero-to-twelve cube satisfying efficiency and standalone constraints.

```json
{"operation":"cg_integer_imputations","game":{"players":["A","B","C"],"values":[0,1,2,5,0,2,3,9]},"allocation":[[9,1],[1,1],[0,1]]}
```

Expected complete envelope:

```json
{"ok":true,"value":{"grid_min":0,"grid_max":12,"allocations":[[1,2,6],[1,3,5],[1,4,4],[1,5,3],[1,6,2],[1,7,1],[1,8,0],[2,2,5],[2,3,4],[2,4,3],[2,5,2],[2,6,1],[2,7,0],[3,2,4],[3,3,3],[3,4,2],[3,5,1],[3,6,0],[4,2,3],[4,3,2],[4,4,1],[4,5,0],[5,2,2],[5,3,1],[5,4,0],[6,2,1],[6,3,0],[7,2,0]],"continuous_core_claim":false},"error":null}
```

Reject unknown fields, other symbol sets, wrong vector sizes, noninteger or out-of-range worths, nonzero empty worth and malformed rational pairs. The request remains unchanged. The integer grid, where used, covers only the zero-to-twelve cube; it does not establish a continuous-core result. Historical and current callers remain available. A correction is additive and never replays a successful domain session or canonical.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20.
