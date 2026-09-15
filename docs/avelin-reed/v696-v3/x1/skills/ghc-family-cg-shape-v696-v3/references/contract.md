# Complete coalition table contract

Operation: `cg_shape`. Return the ordered three-symbol coalition table with every declared worth.

```json
{"operation":"cg_shape","game":{"players":["A","B","C"],"values":[0,1,2,5,0,2,3,9]},"allocation":[[9,1],[1,1],[0,1]]}
```

Expected complete envelope:

```json
{"ok":true,"value":{"players":["A","B","C"],"coalitions":[{"mask":0,"members":[],"worth":0},{"mask":1,"members":["A"],"worth":1},{"mask":2,"members":["B"],"worth":2},{"mask":3,"members":["A","B"],"worth":5},{"mask":4,"members":["C"],"worth":0},{"mask":5,"members":["A","C"],"worth":2},{"mask":6,"members":["B","C"],"worth":3},{"mask":7,"members":["A","B","C"],"worth":9}],"grand_worth":9},"error":null}
```

Reject unknown fields, other symbol sets, wrong vector sizes, noninteger or out-of-range worths, nonzero empty worth and malformed rational pairs. The request remains unchanged. The integer grid, where used, covers only the zero-to-twelve cube; it does not establish a continuous-core result. Historical and current callers remain available. A correction is additive and never replays a successful domain session or canonical.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20.
