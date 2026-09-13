# loss_snapshot

Retain exact removed and overwritten values in a recoverable source snapshot.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Removed integer values remain recoverable

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "a": 1,
      "b": 2
    },
    "after": {
      "a": 1
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [
      {
        "field": "b",
        "value": 2
      }
    ],
    "overwritten": [],
    "added": [],
    "snapshot": {
      "a": 1,
      "b": 2
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## Boolean-to-integer replacement retains the prior type

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "v": true
    },
    "after": {
      "v": 1
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [
      {
        "field": "v",
        "before": true,
        "after": 1
      }
    ],
    "added": [],
    "snapshot": {
      "v": true
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## A newly added null does not become a removed value

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {},
    "after": {
      "a": null
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [],
    "added": [
      {
        "field": "a",
        "value": null
      }
    ],
    "snapshot": {},
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## Array replacement preserves the complete previous array

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "arr": [
        1
      ]
    },
    "after": {
      "arr": [
        2
      ]
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [
      {
        "field": "arr",
        "before": [
          1
        ],
        "after": [
          2
        ]
      }
    ],
    "added": [],
    "snapshot": {
      "arr": [
        1
      ]
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## An unchanged record retains an explicit recovery snapshot

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "v": null,
      "k": false
    },
    "after": {
      "v": null,
      "k": false
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [],
    "added": [],
    "snapshot": {
      "v": null,
      "k": false
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
