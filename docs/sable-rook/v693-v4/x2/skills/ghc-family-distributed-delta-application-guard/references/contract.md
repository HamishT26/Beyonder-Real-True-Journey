# delta_application_guard

Preview a delta only when its source digest and next sequence exactly match.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Matching digest and sequence add a value

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1
  },
  "args": {
    "delta": {
      "base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
      "sequence": 2,
      "changes": {
        "b": {
          "value": 2
        }
      }
    },
    "current_sequence": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "a": 1,
      "b": 2
    },
    "reason": null,
    "actual_base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
    "next_sequence": 2,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Matching digest and sequence remove a value

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "delta": {
      "base_digest": "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
      "sequence": 1,
      "changes": {
        "b": {
          "remove": true
        }
      }
    },
    "current_sequence": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "a": 1
    },
    "reason": null,
    "actual_base_digest": "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Wrong base digest preserves source

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1
  },
  "args": {
    "delta": {
      "base_digest": "0000000000000000000000000000000000000000000000000000000000000000",
      "sequence": 2,
      "changes": {
        "b": {
          "value": 2
        }
      }
    },
    "current_sequence": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": false,
    "result": {
      "a": 1
    },
    "reason": "BASE_DIGEST",
    "actual_base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Skipped sequence preserves source

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1
  },
  "args": {
    "delta": {
      "base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
      "sequence": 3,
      "changes": {
        "b": {
          "value": 2
        }
      }
    },
    "current_sequence": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": false,
    "result": {
      "a": 1
    },
    "reason": "SEQUENCE",
    "actual_base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Empty next delta is an explicit no-op

Request:
```json
{
  "op": "delta_application_guard",
  "record": {},
  "args": {
    "delta": {
      "base_digest": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
      "sequence": 1,
      "changes": {}
    },
    "current_sequence": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {},
    "reason": null,
    "actual_base_digest": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
