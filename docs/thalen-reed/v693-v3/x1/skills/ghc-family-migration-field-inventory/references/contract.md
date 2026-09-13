# field_inventory

Inventory exact top-level field names and JSON types.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Integer and Boolean fields stay distinct

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "count": 1,
    "enabled": true
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
    "fields": [
      {
        "name": "count",
        "type": "integer"
      },
      {
        "name": "enabled",
        "type": "boolean"
      }
    ],
    "count": 2
  },
  "error": null,
  "external_credit": false
}
```

## Explicit null remains a present field

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "label": "north",
    "flag": false,
    "detail": null
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
    "fields": [
      {
        "name": "detail",
        "type": "null"
      },
      {
        "name": "flag",
        "type": "boolean"
      },
      {
        "name": "label",
        "type": "string"
      }
    ],
    "count": 3
  },
  "error": null,
  "external_credit": false
}
```

## Array and object containers have separate types

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "list": [
      1,
      2
    ],
    "opts": {
      "mode": "x"
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
    "fields": [
      {
        "name": "list",
        "type": "array"
      },
      {
        "name": "opts",
        "type": "object"
      }
    ],
    "count": 2
  },
  "error": null,
  "external_credit": false
}
```

## Empty object and empty string are not absence

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "empty": {},
    "zero": 0,
    "blanks": ""
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
    "fields": [
      {
        "name": "blanks",
        "type": "string"
      },
      {
        "name": "empty",
        "type": "object"
      },
      {
        "name": "zero",
        "type": "integer"
      }
    ],
    "count": 3
  },
  "error": null,
  "external_credit": false
}
```

## Negative integer, empty array and null retain their types

Request:
```json
{
  "op": "field_inventory",
  "record": {
    "negative": -2,
    "tags": [],
    "nullable": null
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
    "fields": [
      {
        "name": "negative",
        "type": "integer"
      },
      {
        "name": "nullable",
        "type": "null"
      },
      {
        "name": "tags",
        "type": "array"
      }
    ],
    "count": 3
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
