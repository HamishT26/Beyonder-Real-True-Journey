# Coalition excess profile contract

Operation: `cg_excesses`. Report every coalition worth minus its assigned allocation sum.

```json
{"operation":"cg_excesses","game":{"players":["A","B","C"],"values":[0,1,2,5,0,2,3,9]},"allocation":[[9,1],[1,1],[0,1]]}
```

Expected complete envelope:

```json
{"ok":true,"value":[{"mask":0,"excess":[0,1]},{"mask":1,"excess":[-8,1]},{"mask":2,"excess":[1,1]},{"mask":3,"excess":[-5,1]},{"mask":4,"excess":[0,1]},{"mask":5,"excess":[-7,1]},{"mask":6,"excess":[2,1]},{"mask":7,"excess":[-1,1]}],"error":null}
```

Reject unknown fields, other symbol sets, wrong vector sizes, noninteger or out-of-range worths, nonzero empty worth and malformed rational pairs. The request remains unchanged. The integer grid, where used, covers only the zero-to-twelve cube; it does not establish a continuous-core result. Historical and current callers remain available. A correction is additive and never replays a successful domain session or canonical.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20.
