# Real-utility observation gap contract

Operation: `cg_observation_gap`. Bind missing observation, calibration and independent-review prerequisites to this synthetic game.

```json
{"operation":"cg_observation_gap","game":{"players":["A","B","C"],"values":[0,1,2,5,0,2,3,9]},"allocation":[[9,1],[1,1],[0,1]]}
```

Expected complete envelope:

```json
{"ok":true,"value":{"game_sha256":"d832885bf9c7c6a006791efd2a52c514ba7d84ce6dbd1bf24047e826f8affade","required":["observations","calibration","uncertainty","independent-review"],"real_rows":0,"outcome":"open_gap"},"error":null}
```

Reject unknown fields, other symbol sets, wrong vector sizes, noninteger or out-of-range worths, nonzero empty worth and malformed rational pairs. The request remains unchanged. The integer grid, where used, covers only the zero-to-twelve cube; it does not establish a continuous-core result. Historical and current callers remain available. A correction is additive and never replays a successful domain session or canonical.

Same-owner synthetic evidence only; NOT_READY_FOR_STAGE_20.
