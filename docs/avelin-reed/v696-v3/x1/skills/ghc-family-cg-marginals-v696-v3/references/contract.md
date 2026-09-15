# Marginal contribution table contract

Operation: `cg_marginals`. List all twelve one-symbol marginal contributions with their exact source and destination coalitions.

```json
{"operation":"cg_marginals","game":{"players":["A","B","C"],"values":[0,1,2,5,0,2,3,9]},"allocation":[[9,1],[1,1],[0,1]]}
```

Expected complete envelope:

```json
{"ok":true,"value":[{"player":"A","before":0,"after":1,"delta":1},{"player":"A","before":2,"after":3,"delta":3},{"player":"A","before":4,"after":5,"delta":2},{"player":"A","before":6,"after":7,"delta":6},{"player":"B","before":0,"after":2,"delta":2},{"player":"B","before":1,"after":3,"delta":4},{"player":"B","before":4,"after":6,"delta":3},{"player":"B","before":5,"after":7,"delta":7},{"player":"C","before":0,"after":4,"delta":0},{"player":"C","before":1,"after":5,"delta":1},{"player":"C","before":2,"after":6,"delta":1},{"player":"C","before":3,"after":7,"delta":4}],"error":null}
```

Reject unknown fields, other symbol sets, wrong vector sizes, noninteger or out-of-range worths, nonzero empty worth and malformed rational pairs. The request remains unchanged. The integer grid, where used, covers only the zero-to-twelve cube; it does not establish a continuous-core result. Historical and current callers remain available. A correction is additive and never replays a successful domain session or canonical.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20.
