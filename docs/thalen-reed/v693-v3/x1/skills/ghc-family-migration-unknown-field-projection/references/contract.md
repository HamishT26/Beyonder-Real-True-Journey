# unknown_field_projection

Project declared fields while retaining unknown fields in quarantine.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A known field is selected and its neighbour quarantined

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "known": 1,
    "extra": 2
  },
  "args": {
    "allowed": [
      "known"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {
      "known": 1
    },
    "quarantine": {
      "extra": 2
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Explicit null stays selected

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "n": null,
    "x": false
  },
  "args": {
    "allowed": [
      "n"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {
      "n": null
    },
    "quarantine": {
      "x": false
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An empty allowlist quarantines all data

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "a": [
      1
    ],
    "b": {}
  },
  "args": {
    "allowed": []
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {},
    "quarantine": {
      "a": [
        1
      ],
      "b": {}
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## All declared fields remain in the selected view

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "a": 1,
    "b": "two"
  },
  "args": {
    "allowed": [
      "b",
      "a"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {
      "a": 1,
      "b": "two"
    },
    "quarantine": {},
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An absent allowed field is not invented

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "existing": true
  },
  "args": {
    "allowed": [
      "absent"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {},
    "quarantine": {
      "existing": true
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
