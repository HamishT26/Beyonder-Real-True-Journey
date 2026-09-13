# required_field_check

Distinguish missing required fields from present null or false values.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A complete required set is present

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "required": [
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
    "present": [
      "a",
      "b"
    ],
    "missing": [],
    "complete": true
  },
  "error": null,
  "external_credit": false
}
```

## A missing field remains distinct from null

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "a": null
  },
  "args": {
    "required": [
      "a",
      "b"
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
    "present": [
      "a"
    ],
    "missing": [
      "b"
    ],
    "complete": false
  },
  "error": null,
  "external_credit": false
}
```

## False and zero satisfy presence only

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "enabled": false,
    "retries": 0
  },
  "args": {
    "required": [
      "enabled",
      "retries"
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
    "present": [
      "enabled",
      "retries"
    ],
    "missing": [],
    "complete": true
  },
  "error": null,
  "external_credit": false
}
```

## No fields cannot satisfy a nonempty requirement

Request:
```json
{
  "op": "required_field_check",
  "record": {},
  "args": {
    "required": [
      "x"
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
    "present": [],
    "missing": [
      "x"
    ],
    "complete": false
  },
  "error": null,
  "external_credit": false
}
```

## An empty requirement list is explicitly vacuous

Request:
```json
{
  "op": "required_field_check",
  "record": {
    "x": 1
  },
  "args": {
    "required": []
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "present": [],
    "missing": [],
    "complete": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
