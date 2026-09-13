# rename_cycle_analysis

Separate rename cycles, chains, fixed points and duplicate targets.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A two-cycle needs simultaneous evaluation

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "mapping": {
      "a": "b",
      "b": "a"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [
      [
        "a",
        "b"
      ]
    ],
    "chains": [],
    "fixed_points": [],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## A rename chain terminates at a fresh target

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "mapping": {
      "a": "b",
      "b": "c"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [
      [
        "a",
        "b",
        "c"
      ]
    ],
    "fixed_points": [],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## A fixed point is distinct from a cycle

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1
  },
  "args": {
    "mapping": {
      "a": "a"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [],
    "fixed_points": [
      "a"
    ],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## Independent rename chains remain separate

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "c": 2
  },
  "args": {
    "mapping": {
      "a": "b",
      "c": "d"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [
      [
        "a",
        "b"
      ],
      [
        "c",
        "d"
      ]
    ],
    "fixed_points": [],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## Converging chains expose a duplicate target

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "mapping": {
      "a": "c",
      "b": "c"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [
      [
        "a",
        "c"
      ],
      [
        "b",
        "c"
      ]
    ],
    "fixed_points": [],
    "duplicate_targets": [
      "c"
    ]
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
