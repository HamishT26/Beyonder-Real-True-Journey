# schema_delta

Compare declared field types without inferring migration permission.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A target schema adds one field

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "a": "integer"
  },
  "args": {
    "target": {
      "a": "integer",
      "b": "string"
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
    "added": [
      "b"
    ],
    "removed": [],
    "changed": [],
    "unchanged": [
      "a"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## A removed field remains an explicit obligation

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "old": "string",
    "x": "boolean"
  },
  "args": {
    "target": {
      "x": "boolean"
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
    "added": [],
    "removed": [
      "old"
    ],
    "changed": [],
    "unchanged": [
      "x"
    ]
  },
  "error": null,
  "external_credit": false
}
```

## A scalar type change is not an automatic conversion

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "value": "integer"
  },
  "args": {
    "target": {
      "value": "string"
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
    "added": [],
    "removed": [],
    "changed": [
      {
        "field": "value",
        "from": "integer",
        "to": "string"
      }
    ],
    "unchanged": []
  },
  "error": null,
  "external_credit": false
}
```

## Two empty schemas have no inferred fields

Request:
```json
{
  "op": "schema_delta",
  "record": {},
  "args": {
    "target": {}
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "added": [],
    "removed": [],
    "changed": [],
    "unchanged": []
  },
  "error": null,
  "external_credit": false
}
```

## Addition removal and type change remain separate

Request:
```json
{
  "op": "schema_delta",
  "record": {
    "x": "null",
    "y": "array"
  },
  "args": {
    "target": {
      "x": "object",
      "z": "array"
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
    "added": [
      "z"
    ],
    "removed": [
      "y"
    ],
    "changed": [
      {
        "field": "x",
        "from": "null",
        "to": "object"
      }
    ],
    "unchanged": []
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
