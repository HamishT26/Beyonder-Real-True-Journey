# field_correspondence

Expose missing sources and duplicate destinations in a declared field correspondence.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## One declared field resolves to a new label

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "alpha": 1,
    "beta": 2
  },
  "args": {
    "mapping": {
      "alpha": "value"
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
    "resolved": [
      {
        "from": "alpha",
        "to": "value",
        "present": true,
        "source_type": "integer"
      }
    ],
    "target_collisions": [],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

## Swap correspondences remain simultaneous

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "left": true,
    "right": false
  },
  "args": {
    "mapping": {
      "left": "right",
      "right": "left"
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
    "resolved": [
      {
        "from": "left",
        "to": "right",
        "present": true,
        "source_type": "boolean"
      },
      {
        "from": "right",
        "to": "left",
        "present": true,
        "source_type": "boolean"
      }
    ],
    "target_collisions": [],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

## Two sources targeting one field are exposed

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "a": 1,
    "b": "two"
  },
  "args": {
    "mapping": {
      "a": "x",
      "b": "x"
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
    "resolved": [
      {
        "from": "a",
        "to": "x",
        "present": true,
        "source_type": "integer"
      },
      {
        "from": "b",
        "to": "x",
        "present": true,
        "source_type": "string"
      }
    ],
    "target_collisions": [
      {
        "target": "x",
        "sources": [
          "a",
          "b"
        ]
      }
    ],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

## An absent source cannot become a null value

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "a": 1
  },
  "args": {
    "mapping": {
      "z": "zeta"
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
    "resolved": [
      {
        "from": "z",
        "to": "zeta",
        "present": false,
        "source_type": "absent"
      }
    ],
    "target_collisions": [],
    "missing_sources": [
      "z"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## Identity correspondence preserves an array field

Request:
```json
{
  "op": "field_correspondence",
  "record": {
    "x": [
      1
    ],
    "meta": null
  },
  "args": {
    "mapping": {
      "x": "x"
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
    "resolved": [
      {
        "from": "x",
        "to": "x",
        "present": true,
        "source_type": "array"
      }
    ],
    "target_collisions": [],
    "missing_sources": []
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
