# conflict_kinds

Classify concurrent additions, different edits and delete-versus-modify conflicts.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Unilateral deletion is not a conflict

Request:
```json
{
  "op": "conflict_kinds",
  "record": {
    "base": {
      "v": 1
    },
    "left": {},
    "right": {
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
    "fields": 1,
    "conflict_count": 0,
    "kinds": {
      "different_edits": [],
      "delete_modify": [],
      "concurrent_add": []
    }
  },
  "error": null,
  "external_credit": false
}
```

## Different edits are classified by field

Request:
```json
{
  "op": "conflict_kinds",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
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
    "fields": 1,
    "conflict_count": 1,
    "kinds": {
      "different_edits": [
        "v"
      ],
      "delete_modify": [],
      "concurrent_add": []
    }
  },
  "error": null,
  "external_credit": false
}
```

## Delete-versus-modify is its own category

Request:
```json
{
  "op": "conflict_kinds",
  "record": {
    "base": {
      "v": 1
    },
    "left": {},
    "right": {
      "v": 2
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
    "fields": 1,
    "conflict_count": 1,
    "kinds": {
      "different_edits": [],
      "delete_modify": [
        "v"
      ],
      "concurrent_add": []
    }
  },
  "error": null,
  "external_credit": false
}
```

## Concurrent additions preserve their category

Request:
```json
{
  "op": "conflict_kinds",
  "record": {
    "base": {},
    "left": {
      "v": null
    },
    "right": {
      "v": false
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
    "fields": 1,
    "conflict_count": 1,
    "kinds": {
      "different_edits": [],
      "delete_modify": [],
      "concurrent_add": [
        "v"
      ]
    }
  },
  "error": null,
  "external_credit": false
}
```

## Multiple categories are counted without collapsing fields

Request:
```json
{
  "op": "conflict_kinds",
  "record": {
    "base": {
      "a": 1,
      "b": 1
    },
    "left": {
      "a": 2,
      "c": true
    },
    "right": {
      "a": 3,
      "b": 2,
      "c": false
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
    "fields": 3,
    "conflict_count": 3,
    "kinds": {
      "different_edits": [
        "a"
      ],
      "delete_modify": [
        "b"
      ],
      "concurrent_add": [
        "c"
      ]
    }
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
